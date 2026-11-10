#!/usr/bin/env python3
import argparse
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL = 'opencode/glm-5.3-flash-free'

def load_providers(path):
    try:
        import yaml
    except ImportError:
        raise RuntimeError('Install dependencies: python3 -m pip install -r requirements.txt') from None
    providers = yaml.safe_load(path.read_text(encoding='utf-8'))
    if not isinstance(providers, dict) or not providers:
        raise ValueError('Provider config must be a non-empty mapping')
    for key, provider in providers.items():
        if not isinstance(key, str) or not key or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789_-' for c in key):
            raise ValueError('Invalid provider key')
        if not isinstance(provider, dict):
            raise ValueError(f'Invalid config for {key}')
        for field in ('name', 'url', 'format', 'access', 'pricing_notes'):
            if not isinstance(provider.get(field), str) or not provider[field].strip():
                raise ValueError(f'Missing or invalid {field} for {key}')
        if not provider['url'].startswith('https://'):
            raise ValueError(f'HTTPS URL required for {key}')
        if provider['format'] not in ('json', 'html'):
            raise ValueError(f'Unsupported format for {key}')
        if provider.get('summary') not in (None, 'openrouter', 'tokenator', 'vantyr'):
            raise ValueError(f'Unsupported summary for {key}')
        if 'token' in provider and (not isinstance(provider['token'], str) or not provider['token'].strip()):
            raise ValueError(f'Invalid token for {key}')
    return providers


def load_profiles(path):
    try:
        import yaml
    except ImportError:
        raise RuntimeError('Install dependencies: python3 -m pip install -r requirements.txt') from None
    profiles = yaml.safe_load(path.read_text(encoding='utf-8'))
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError('Profiles config must be a non-empty mapping')
    for key, profile in profiles.items():
        if not isinstance(key, str) or not key or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789_-' for c in key):
            raise ValueError('Invalid profile key')
        if not isinstance(profile, dict):
            raise ValueError(f'Invalid config for {key}')
        if not isinstance(profile.get('title'), str) or not profile['title'].strip():
            raise ValueError(f'Missing or invalid title for {key}')
        for field in ('input', 'output'):
            value = profile.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f'Missing or invalid {field} for {key}')
        cache = profile.get('cache_read', 0)
        if not isinstance(cache, int) or isinstance(cache, bool) or cache < 0:
            raise ValueError(f'Invalid cache_read for {key}')
        note = profile.get('note')
        if note is not None and (not isinstance(note, str) or not note.strip()):
            raise ValueError(f'Invalid note for {key}')
    return profiles


def summarize_tokenator(html_text):
    import re
    for block in re.findall(r'<script[^>]*>([\s\S]*?)</script>', html_text):
        text = block.strip()
        if not text.startswith('{'):
            continue
        try:
            payload = json.loads(text)
        except ValueError:
            continue
        if isinstance(payload, dict) and isinstance(payload.get('models'), list):
            models = []
            for m in payload['models']:
                if m.get('free') or any(m.get(k) for k in ('is_image', 'is_video', 'is_speech', 'is_embedding', 'is_decision')):
                    continue
                mult_min = m.get('token_multiplier_min', m.get('token_multiplier'))
                mult_max = m.get('token_multiplier_max', mult_min)
                usd_min = round(0.27 * mult_min, 4) if isinstance(mult_min, (int, float)) else None
                usd_max = round(0.27 * mult_max, 4) if isinstance(mult_max, (int, float)) else None
                models.append({
                    'id': m.get('id'),
                    'name': m.get('display_name'),
                    'owned_by': m.get('owned_by'),
                    'context_length': m.get('context_length'),
                    'operational': m.get('operational', True),
                    'unstable': bool(m.get('unstable')),
                    'multiplier_min': mult_min,
                    'multiplier_max': mult_max,
                    'input_usd_per_1m': usd_min if usd_min == usd_max else {'min': usd_min, 'max': usd_max},
                    'output_usd_per_1m': usd_min if usd_min == usd_max else {'min': usd_min, 'max': usd_max},
                })
            return models
    raise ValueError('Tokenator models JSON not found in HTML')


def summarize_vantyr(raw):
    import re
    group_ratio = (raw.get('group_ratio') or {}).get('default', 1)
    models = []
    for m in raw.get('data', []):
        entry = {
            'id': m.get('model_name'),
            'description': m.get('description'),
            'billing_mode': m.get('billing_mode') or 'ratio',
            'enable_groups': m.get('enable_groups'),
            'supported_endpoint_types': m.get('supported_endpoint_types'),
            'official_input_usd': m.get('official_input_usd'),
            'official_output_usd': m.get('official_output_usd'),
            'official_cache_usd': m.get('official_cache_usd'),
        }
        expr = m.get('billing_expr') or ''
        if entry['billing_mode'] == 'tiered_expr' and expr:
            entry['billing_expr'] = expr
            rates = {k: float(v) for k, v in re.findall(r'\b(p|c|cr|cc|cc1h)\s*\*\s*([0-9.]+)', expr)}
            entry['input_usd_per_1m'] = rates.get('p')
            entry['output_usd_per_1m'] = rates.get('c')
            entry['cache_read_usd_per_1m'] = rates.get('cr')
        else:
            ratio = m.get('model_ratio')
            comp = m.get('completion_ratio')
            cache = m.get('cache_ratio')
            inp = round(2.0 * ratio * group_ratio, 6) if isinstance(ratio, (int, float)) else None
            entry['model_ratio'] = ratio
            entry['completion_ratio'] = comp
            entry['cache_ratio'] = cache
            entry['input_usd_per_1m'] = inp
            entry['output_usd_per_1m'] = round(inp * comp, 6) if inp is not None and isinstance(comp, (int, float)) else None
            entry['cache_read_usd_per_1m'] = round(inp * cache, 6) if inp is not None and isinstance(cache, (int, float)) else None
        models.append(entry)
    return models


def fetch(url, target, token=None):
    headers = {'User-Agent': 'ai-monitor/2.0'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(20_000_001)
    if len(data) > 20_000_000:
        raise ValueError('Source exceeds 20 MB')
    target.write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description='AI pricing and recommendations via OpenCode')
    parser.add_argument('--model', default=DEFAULT_MODEL)
    parser.add_argument('--days', type=int, default=7)
    parser.add_argument('--timeout', type=int, default=1800)
    parser.add_argument('--allow-paid-model', action='store_true')
    parser.add_argument('--config', type=Path, default=ROOT / 'providers.yml')
    parser.add_argument('--profiles', type=Path, default=ROOT / 'profiles.yml')
    parser.add_argument('--dry-run', action='store_true',
                        help='Prepare snapshots, manifest and prompt, then exit before OpenCode')
    args = parser.parse_args()
    if args.days < 1 or args.timeout < 1:
        parser.error('--days and --timeout must be positive')
    free_model = args.model == DEFAULT_MODEL or args.model.startswith('tokenator/free-')
    if not args.allow_paid_model and not free_model:
        parser.error('Use the default free model or tokenator/free-*, or --allow-paid-model')
    if not shutil.which('opencode'):
        parser.error('opencode not found in PATH')
    providers = load_providers(args.config)
    profiles = load_profiles(args.profiles)
    template = (ROOT / 'prompt.md').read_text(encoding='utf-8')
    for name in ('reports', 'runs'):
        (ROOT / name).mkdir(exist_ok=True)
    with (ROOT / '.monitor.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Another run is already active')
        now = dt.datetime.now().astimezone()
        run = Path(tempfile.mkdtemp(prefix=now.strftime('%Y-%m-%d_%H-%M-%S-'), dir=ROOT / 'runs'))
        manifest = {'time': now.isoformat(), 'model': args.model, 'sources': []}
        shutil.copyfile(args.profiles, run / 'profiles.yml')
        manifest['profiles'] = {'file': 'profiles.yml', 'count': len(profiles)}
        for key, provider in providers.items():
            url = provider['url']
            name = f'{key}.{provider["format"]}'
            item = {field: provider[field] for field in ('name', 'url', 'format', 'access', 'pricing_notes')}
            item.update(provider=key, file=name, requires_auth=bool(provider.get('token')))
            try:
                fetch(url, run / name, provider.get('token'))
                if provider['format'] == 'json':
                    raw = json.loads((run / name).read_text(encoding='utf-8'))
                    (run / name).write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding='utf-8')
                item['status'] = 'ok'
                summary_type = provider.get('summary')
                if summary_type:
                    if summary_type == 'openrouter':
                        models = [{k: m.get(k) for k in (
                            'id', 'name', 'context_length', 'pricing',
                            'supported_parameters', 'top_provider')} for m in raw.get('data', [])]
                    elif summary_type == 'tokenator':
                        models = summarize_tokenator((run / name).read_text(encoding='utf-8'))
                    elif summary_type == 'vantyr':
                        models = summarize_vantyr(raw)
                    summary = f'{key}-summary.json'
                    (run / summary).write_text(
                        json.dumps(models, ensure_ascii=False, indent=2), encoding='utf-8')
                    item['file'] = summary
                    item['format'] = 'json'
            except Exception as exc:
                error = str(exc)
                for configured in providers.values():
                    if configured.get('token'):
                        error = error.replace(configured['token'], '[REDACTED]')
                item.update(status='error', error=error)
            manifest['sources'].append(item)
        (run / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        previous = list((ROOT / 'reports').glob('*.md')) + [
            p for p in (ROOT / 'reports').glob('*/report.md') if p.parent.name != 'actual'
        ]
        if previous:
            latest = max(previous, key=lambda p: p.stat().st_mtime)
            shutil.copyfile(latest, run / 'previous.md')
            if latest.name == 'report.md' and (latest.parent / 'prices.md').is_file():
                shutil.copyfile(latest.parent / 'prices.md', run / 'previous-prices.md')
        output = run / 'output'
        output.mkdir()
        prompt = template.replace('{{NOW}}', now.isoformat()).replace('{{DAYS}}', str(args.days))
        prompt = prompt.replace('{{RUN}}', str(run)).replace('{{OUTPUT}}', str(output))
        (run / 'prompt.txt').write_text(prompt, encoding='utf-8')
        if args.dry_run:
            print(f'dry run: {run}')
            print(run / 'prompt.txt')
            return
        command = ['opencode', '--standalone', 'run', '--auto', '-m', args.model, prompt]
        with (run / 'opencode.log').open('w', encoding='utf-8') as log:
            result = subprocess.run(command, cwd=run, stdout=log, stderr=subprocess.STDOUT,
                                    timeout=args.timeout, check=False)
        if result.returncode:
            raise RuntimeError(f'OpenCode exited {result.returncode}; see {run}/opencode.log')
        rules = {
            'report.md': (500, ['# Мониторинг ИИ', '## Рекомендации', '## Новости', '## Изменения']),
            'prices.md': (200, ['# Цены', 'https://']),
            'sources.md': (200, ['# Источники', 'https://']),
        }
        for name, (minimum, markers) in rules.items():
            path = output / name
            if not path.is_file() or path.is_symlink():
                raise RuntimeError(f'Missing regular file {path}; see {run}/opencode.log')
            text = path.read_text(encoding='utf-8')
            if len(text) < minimum or any(marker not in text for marker in markers):
                raise RuntimeError(f'Structural validation failed: {path}')
            if name == 'report.md':
                if '\n|' not in text or 'prices.md' not in text or 'sources.md' not in text:
                    raise RuntimeError(f'Missing table or companion links: {path}')
                if any(h in text for h in ('## Ограничения', '## Источники', '## Цены')):
                    raise RuntimeError(f'Unexpected detailed section: {path}')
        destination = ROOT / 'reports' / run.name
        os.replace(output, destination)
        actual = ROOT / 'reports' / 'actual'
        if actual.is_symlink() or actual.is_file():
            actual.unlink()
        elif actual.is_dir():
            shutil.rmtree(actual)
        shutil.copytree(destination, actual)
        print(destination / 'report.md')


if __name__ == '__main__':
    try:
        main()
    except (Exception, KeyboardInterrupt) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
