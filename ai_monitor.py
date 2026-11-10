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
        if provider.get('summary') not in (None, 'openrouter'):
            raise ValueError(f'Unsupported summary for {key}')
        if 'token' in provider and (not isinstance(provider['token'], str) or not provider['token'].strip()):
            raise ValueError(f'Invalid token for {key}')
    return providers


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
    parser.add_argument('--config', type=Path, default=ROOT / 'vars.yml')
    args = parser.parse_args()
    if args.days < 1 or args.timeout < 1:
        parser.error('--days and --timeout must be positive')
    free_model = args.model == DEFAULT_MODEL or args.model.startswith('tokenator/free-')
    if not args.allow_paid_model and not free_model:
        parser.error('Use the default free model or tokenator/free-*, or --allow-paid-model')
    if not shutil.which('opencode'):
        parser.error('opencode not found in PATH')
    providers = load_providers(args.config)
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
        for key, provider in providers.items():
            url = provider['url']
            name = f'{key}.{provider["format"]}'
            item = {field: provider[field] for field in ('name', 'url', 'format', 'access', 'pricing_notes')}
            item.update(provider=key, file=name, requires_auth=bool(provider.get('token')))
            try:
                fetch(url, run / name, provider.get('token'))
                if provider['format'] == 'json':
                    raw = json.loads((run / name).read_text(encoding='utf-8'))
                item['status'] = 'ok'
                if provider.get('summary') == 'openrouter':
                    models = [{k: m.get(k) for k in (
                        'id', 'name', 'context_length', 'pricing',
                        'supported_parameters', 'top_provider')} for m in raw.get('data', [])]
                    summary = f'{key}-summary.json'
                    (run / summary).write_text(
                        json.dumps(models, ensure_ascii=False, indent=2), encoding='utf-8')
                    item['file'] = summary
            except Exception as exc:
                error = str(exc)
                for configured in providers.values():
                    if configured.get('token'):
                        error = error.replace(configured['token'], '[REDACTED]')
                item.update(status='error', error=error)
            manifest['sources'].append(item)
        (run / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        previous = list((ROOT / 'reports').glob('*.md')) + list((ROOT / 'reports').glob('*/report.md'))
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
        print(destination / 'report.md')


if __name__ == '__main__':
    try:
        main()
    except (Exception, KeyboardInterrupt) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
