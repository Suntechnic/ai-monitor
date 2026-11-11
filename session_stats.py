#!/usr/bin/env python3
"""Пометки сессий OpenCode и статистика по тегам для калибровки profiles.yml.

Теги совместимы с плагином opencode-session-tags: массив в
metadata["opencode-session-tags"]["tags"], пишется через
PATCH /api/session/{id} и читается из /api/session вместе с токенами.

Команды:
  list                     все сессии с токенами: теги, папка, название, токены
                           (окно LIMIT_SESSIONS последних сессий, старые не участвуют)
  tag <id|last|префикс> <ключ профиля>   поставить типовой тег («-» снять)
  show <id|last|префикс>   сырые поля одной сессии
  collect                  собрать локальные сессии и все хосты из stats-hosts.yml
                           по SSH, пересчитать runs/session-stats/summary.yml
                           и runs/session-stats/models.yml
  collect --host имя       обновить только один хост
  collect --local          обновить только локальный снимок
  stats                    таблица по снимкам (без записи summary)
  export                   JSON сессий для удалённого сбора; не требует
                           profiles.yml и репозитория (скрипт идёт через stdin)

Снимки: runs/session-stats/<host>.json (local — для этой машины).
Окно сбора: до LIMIT_SESSIONS последних сессий каждого хоста по времени
обновления, без фильтрации по токенам. Для каждой сессии читается история
сообщений (пагинация): из ответов ассистента извлекаются использованные
агенты и модели (providerID + model.id) со временем сообщений. Снимки
формата 2 содержат поля agents и models; снимки формата 1 пригодны
только для токенной статистики.

summary.yml совместим с profiles.yml: копируйте нужные блоки вручную.
models.yml — использование моделей по паре providerID + model.id:
sessions (уникальные сессии), tags, week (7 дней), month (30 дней),
trand — изменение week относительно предыдущих 7 дней в процентах
(null при росте с нуля, -100.0 при прекращении). Периоды считаются от
времени формирования по времени сообщений модели; при обрезке выборки
лимитом показатели могут быть занижены (отмечается в комментариях).
"""
import argparse
import datetime as dt
import json
import os
import re
import shlex
import statistics
import subprocess
import sys
import tempfile
import time
from collections import defaultdict
from pathlib import Path

_SELF = globals().get('__file__')
ROOT = Path(_SELF).resolve().parent if _SELF else Path.cwd()
TAG_KEY = 'opencode-session-tags'
FORMAT = 2
LIMIT_SESSIONS = 200
DAY_MS = 24 * 60 * 60 * 1000
SNAPSHOT_DIR = ROOT / 'runs' / 'session-stats'
SUMMARY_PATH = SNAPSHOT_DIR / 'summary.yml'
MODELS_PATH = SNAPSHOT_DIR / 'models.yml'
TAG_RE = re.compile(r'[a-z0-9_-]+')
COLLECT_TIMEOUT = 600
LOCAL_HOST = 'local'
OPENCODE = 'opencode'


def now_iso():
    return dt.datetime.now().astimezone().isoformat(timespec='seconds')


def api(path):
    """GET через opencode api; возвращает (data, cursor)."""
    result = subprocess.run([OPENCODE, 'api', 'get', path],
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'opencode api failed: {result.stderr.strip()}')
    data = json.loads(result.stdout)
    if isinstance(data, dict):
        return data.get('data', data), data.get('cursor') or {}
    return data, {}


def _page_url(path, cursor):
    """URL следующей страницы: исходные параметры + новый cursor."""
    base, _, query = path.partition('?')
    kept = [p for p in query.split('&') if p and not p.startswith('cursor=')]
    prefix = base + '?' + ('&'.join(kept) + '&' if kept else '')
    return f'{prefix}cursor={cursor}'


def api_all(path, limit=None, limit_key='id'):
    """GET с пагинацией по cursor.next; не более limit уникальных записей.

    Возвращает (записи, True если достигнут limit). Записи без limit_key
    не дедуплицируются между собой. Повтор курса — ошибка (защита от цикла).
    """
    items = []
    seen = set()
    page = path
    seen_pages = set()
    for _ in range(10000):
        if page in seen_pages:
            raise RuntimeError(f'opencode api: повтор курсора для {path}')
        seen_pages.add(page)
        data, cursor = api(page)
        if not isinstance(data, list):
            raise RuntimeError(f'opencode api: ожидался список для {path}')
        for entry in data:
            key = entry.get(limit_key) if isinstance(entry, dict) else None
            fresh = key is None or key not in seen
            if key is not None:
                seen.add(key)
            if fresh:
                items.append(entry)
                if limit is not None and len(items) >= limit:
                    return items, True
        nxt = cursor.get('next')
        if not nxt:
            return items, False
        page = _page_url(path, nxt)
    raise RuntimeError(f'opencode api: слишком много страниц для {path}')


def patch_session(session_id, body):
    result = subprocess.run(
        [OPENCODE, 'api', 'patch', f'/api/session/{session_id}',
         '--data', json.dumps(body, ensure_ascii=False)],
        capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'opencode api failed: {result.stderr.strip()}')


def real_sessions():
    """Сессии с непустыми токенами, отсортированные по времени обновления.

    Скользящее окно: LIMIT_SESSIONS последних сессий, более старые не попадают.
    """
    items, _ = window_sessions()
    items = [s for s in items if s.get('tokens')]
    items = [s for s in items
             if sum([s['tokens'].get('input', 0), s['tokens'].get('output', 0),
                     s['tokens'].get('reasoning', 0),
                     s['tokens'].get('cache', {}).get('read', 0)]) > 0]
    items.sort(key=lambda s: s.get('time', {}).get('updated', 0))
    return items


def window_sessions():
    """Окно сбора: LIMIT_SESSIONS последних сессий без фильтрации по токенам.

    Запрашивает на одну сессию больше, чтобы отличить «ровно LIMIT_SESSIONS
    сессий» (truncated=False) от «сессий больше лимита» (truncated=True).
    """
    items, _ = api_all('/api/session', limit=LIMIT_SESSIONS + 1)
    truncated = len(items) > LIMIT_SESSIONS
    items.sort(key=lambda s: s.get('time', {}).get('updated', 0))
    return items[:LIMIT_SESSIONS], truncated


def message_history(session_id):
    """Все сообщения сессии с пагинацией."""
    items, _ = api_all(f'/api/session/{session_id}/message', limit_key='id')
    return items


def session_models_and_agents(messages):
    """Из сообщений: ({(providerID, modelID): [времена]}, set(агенты))."""
    models = defaultdict(set)
    agents = set()
    for message in messages:
        info = message.get('info') or message
        if info.get('type') != 'assistant':
            continue
        created = (info.get('time') or {}).get('created')
        agent = info.get('agent')
        if agent:
            agents.add(agent)
        model = info.get('model') or {}
        provider = model.get('providerID')
        model_id = model.get('id')
        if provider and model_id:
            if created:
                models[(provider, model_id)].add(int(created))
            else:
                models[(provider, model_id)].add(0)
    return models, agents


def tags_of(session):
    metadata = session.get('metadata') or {}
    tags = (metadata.get(TAG_KEY) or {}).get('tags') or []
    if not isinstance(tags, list):
        raise RuntimeError(f'Unexpected {TAG_KEY}.tags in {session["id"]}')
    return tags


def session_record(session, messages=None):
    tokens = session.get('tokens') or {}
    record = {
        'id': session['id'],
        'updated': (session.get('time') or {}).get('updated', 0),
        'tags': tags_of(session),
        'input': tokens.get('input', 0),
        'cache_read': (tokens.get('cache') or {}).get('read', 0),
        'output': tokens.get('output', 0),
        'reasoning': tokens.get('reasoning', 0),
    }
    if messages is not None:
        models, agents = session_models_and_agents(messages)
        record['models'] = [
            {'provider': provider, 'model': model_id, 'times': sorted(times)}
            for (provider, model_id), times in sorted(models.items())]
        record['agents'] = sorted(agents)
    return record


def export_payload():
    sessions, truncated = window_sessions()
    records = []
    for session in sessions:
        try:
            messages = message_history(session['id'])
        except (RuntimeError, OSError) as exc:
            raise RuntimeError(f'сессия {session["id"]}: {exc}') from None
        records.append(session_record(session, messages))
    return {
        'format': FORMAT,
        'exported_at': now_iso(),
        'limit': LIMIT_SESSIONS,
        'truncated': truncated,
        'sessions': records,
    }


def validate_export(data):
    """Проверяет export/снимок; формат 1 — только токены, формат 2 — с моделями."""
    fmt = data.get('format') if isinstance(data, dict) else None
    if fmt not in (1, FORMAT) or not isinstance(data.get('sessions'), list):
        raise ValueError('неожиданный формат export (поддерживаются 1 и 2)')
    for session in data['sessions']:
        if not isinstance(session, dict) or not isinstance(session.get('id'), str) \
                or not isinstance(session.get('updated'), int) \
                or not isinstance(session.get('tags'), list) \
                or not all(isinstance(t, str) for t in session['tags']) \
                or any(not isinstance(session.get(k), int) for k in ('input', 'cache_read', 'output', 'reasoning')):
            raise ValueError('некорректная запись сессии в export')
        if fmt < FORMAT:
            continue
        if not isinstance(session.get('models'), list) \
                or not isinstance(session.get('agents'), list):
            raise ValueError('некорректная запись сессии в export (нет моделей/агентов)')
        for entry in session['models']:
            if not isinstance(entry, dict) \
                    or not isinstance(entry.get('provider'), str) \
                    or not isinstance(entry.get('model'), str) \
                    or not isinstance(entry.get('times'), list) \
                    or any(not isinstance(t, int) for t in entry['times']):
                raise ValueError(f'некорректная модель в сессии {session["id"]}')
        if any(not isinstance(a, str) for a in session['agents']):
            raise ValueError(f'некорректный агент в сессии {session["id"]}')
    return data['sessions']


def resolve(pattern, items):
    if pattern == 'last':
        return items[-1]
    matches = [s for s in items if s['id'] == pattern]
    if not matches:
        matches = [s for s in items if s['id'].startswith(pattern)]
    if len(matches) != 1:
        raise SystemExit(f'Pattern {pattern!r} matches {len(matches)} sessions; use more characters')
    return matches[0]


def cmd_list(args):
    header = f"{'id':20} {'теги':22} {'папка':28} {'название':42} {'модель':28} {'вход':>9} {'кеш':>9} {'выход':>9} {'$':>9}"
    print(header)
    for session in real_sessions():
        tags = ','.join(tags_of(session)) or '—'
        directory = (session.get('location') or {}).get('directory', '?').replace(str(Path.home()) + '/', '~/')
        title = (session.get('title') or '(без названия)')[:42]
        model = (session.get('model') or {}).get('id') or '?'
        cost = session.get('cost') or 0
        record = session_record(session)
        print(f"{session['id']:20} {tags:22} {directory:28} {title:42} {model:28} "
              f"{record['input']:9} {record['cache_read']:9} {record['output']:9} {cost:9.4f}")


def cmd_tag(args):
    from ai_monitor import load_profiles
    profiles = load_profiles(args.profiles)
    items = real_sessions()
    session = resolve(args.session, items)
    if args.tag != '-' and args.tag not in profiles:
        raise SystemExit('Допустимые теги (ключи profiles.yml): ' + ', '.join(profiles))
    metadata = session.get('metadata') or {}
    record = metadata.get(TAG_KEY) or {}
    tags = [t for t in (record.get('tags') or []) if t not in profiles]
    if args.tag != '-':
        tags.append(args.tag)
    metadata[TAG_KEY] = {'version': record.get('version', 1), 'tags': tags}
    patch_session(session['id'], {'metadata': metadata})
    title = (session.get('title') or '')[:50]
    print(f"{session['id']} tags={','.join(tags) or '—'} | {title}")


def cmd_show(args):
    session = resolve(args.session, real_sessions())
    print(json.dumps(session, ensure_ascii=False, indent=2))


def read_snapshots():
    """Все снимки из SNAPSHOT_DIR: (записи с полем host, список источников)."""
    records = []
    sources = []
    if not SNAPSHOT_DIR.is_dir():
        return records, sources
    for path in sorted(SNAPSHOT_DIR.glob('*.json')):
        try:
            snapshot = json.loads(path.read_text(encoding='utf-8'))
            host = snapshot['host']
            data = {'format': snapshot.get('format'), 'sessions': snapshot['sessions']}
            sessions = validate_export(data)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise RuntimeError(f'Не читается снимок {path.name}: {exc}') from None
        sources.append({'host': host, 'collected_at': snapshot.get('collected_at') or '?',
                        'count': len(sessions),
                        'truncated': bool(snapshot.get('truncated')),
                        'exported_at': snapshot.get('exported_at') or '?'})
        records.extend({**s, 'host': host} for s in sessions)
    return records, sources


def dedupe(records):
    best = {}
    for record in records:
        key = (record['host'], record['id'])
        if key not in best or record['updated'] > best[key]['updated']:
            best[key] = record
    return list(best.values())


def aggregate(records):
    groups = defaultdict(list)
    untagged = 0
    multi = []
    for record in records:
        tags = list(dict.fromkeys(t for t in record['tags'] if t))
        if not tags:
            untagged += 1
            continue
        if len(tags) > 1:
            multi.append((record, tags))
        for tag in tags:
            groups[tag].append(record)
    rows = {}
    for tag in sorted(groups):
        sessions = groups[tag]
        columns = [[s['input'] for s in sessions],
                   [s['cache_read'] for s in sessions],
                   [s['output'] + s['reasoning'] for s in sessions]]
        rows[tag] = {'n': len(sessions),
                     'means': [round(statistics.mean(c)) for c in columns],
                     'medians': [round(statistics.median(c)) for c in columns]}
    return rows, untagged, multi


def model_usage(records, now_ms=None):
    """Использование моделей по записям снимков (формат 2).

    Возвращает ({(provider, model): {'sessions', 'tags', 'week', 'month',
    'trand'}}, число записей без поля models).
    """
    if now_ms is None:
        now_ms = int(time.time() * 1000)
    week_start, prev_start, prev_end, month_start = (
        now_ms - 7 * DAY_MS, now_ms - 14 * DAY_MS, now_ms - 7 * DAY_MS,
        now_ms - 30 * DAY_MS)
    groups = defaultdict(lambda: {'sessions': set(), 'tags': set(),
                                  'week': set(), 'prev_week': set(), 'month': set()})
    legacy = 0
    for record in records:
        tags = {t for t in record['tags'] if t}
        for entry in record.get('models') or []:
            key = (entry['provider'], entry['model'])
            group = groups[key]
            group['sessions'].add(record['id'])
            group['tags'] |= tags
            for created in entry['times']:
                if created >= month_start:
                    group['month'].add(record['id'])
                if created >= week_start:
                    group['week'].add(record['id'])
                if prev_start <= created < prev_end:
                    group['prev_week'].add(record['id'])
        if record.get('models') is None:
            legacy += 1
    rows = {}
    for (provider, model_id), group in sorted(groups.items()):
        week, prev = len(group['week']), len(group['prev_week'])
        if prev == 0:
            trand = None if week > 0 else 0.0
        else:
            trand = round((week - prev) / prev * 100, 1)
        rows[(provider, model_id)] = {
            'sessions': len(group['sessions']),
            'tags': sorted(group['tags']),
            'week': week,
            'month': len(group['month']),
            'trand': trand,
        }
    return rows, legacy


def render_models(rows, sources, legacy, generated):
    import yaml
    header = [f'# Использование моделей по сообщениям сессий (провайдер + модель)',
              f'# Сформировано: {generated}',
              f'# Окно: до {LIMIT_SESSIONS} последних сессий каждого хоста (LIMIT_SESSIONS)',
              '# Единица: уникальная сессия, в которой модель отвечала; week — за 7 дней,',
              '# month — за 30 дней, trand — % изменения week к предыдущим 7 дням',
              '# (null — рост с нуля; 0.0 — не использовалась в обоих периодах).',
              '# Периоды считаются по времени сообщений от момента формирования;',
              '# при обрезке выборки лимитом показатели могут быть занижены.',
              '# Источники:']
    full_month = True
    for s in sources:
        header.append(f"#   {s['host']}: собрано {s['collected_at']}, сессий {s['count']}"
                      + (', ВЫБОРКА ОБРЕЗАНА ЛИМИТОМ' if s['truncated'] else ''))
        if s['truncated']:
            full_month = False
    if legacy:
        header.append(f'# ВНИМАНИЕ: снимков формата 1 (без данных о моделях) — {legacy};'
                      ' статистика по ним неполна, выполните collect')
    if not full_month:
        header.append('# ВНИМАНИЕ: хотя бы один хост обрезан лимитом;'
                      ' week/month/trand могут быть занижены')
    data = {}
    for (provider, model_id), row in rows.items():
        data.setdefault(provider, {})[model_id] = {
            'sessions': row['sessions'],
            'tags': row['tags'],
            'week': row['week'],
            'month': row['month'],
            'trand': row['trand'],
        }
    body = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False) if data else '{}\n'
    return '\n'.join(header) + '\n\n' + body


def print_table(rows, untagged, multi, total):
    print(f"{'тег':14} {'n':>3} | {'вход':>12} {'кеш':>12} {'выход+reas':>11} |"
          f" {'вход(med)':>12} {'кеш(med)':>12} {'выход(med)':>12}")
    for tag, row in rows.items():
        m, d = row['means'], row['medians']
        print(f"{tag:14} {row['n']:3} | {m[0]:12} {m[1]:12} {m[2]:11} |"
              f" {d[0]:12} {d[1]:12} {d[2]:12}")
    print(f'сессий после дедупликации: {total}, без тегов: {untagged}')
    if multi:
        print('несколько тегов (учтены в каждом): '
              + ', '.join(f"{r['host']}:{r['id']}" for r, _ in multi))


def print_sources(sources):
    print('источники:')
    for s in sources:
        print(f"  {s['host']}: {s['count']} сессий (собрано {s['collected_at']})")


def print_models(rows):
    if not rows:
        print('модели: нет данных формата 2, выполните collect')
        return
    print(f"{'провайдер':16} {'модель':28} {'сессий':>6} {'нед':>4} {'30д':>4} {'тренд%':>7}  теги")
    for (provider, model_id), row in rows.items():
        trand = 'null' if row['trand'] is None else f"{row['trand']:+.1f}"
        tags = ','.join(row['tags']) or '—'
        print(f"{provider:16} {model_id:28} {row['sessions']:6} {row['week']:4} "
              f"{row['month']:4} {trand:>7}  {tags}")


def cmd_stats(args):
    records, sources = read_snapshots()
    if not sources:
        raise RuntimeError('нет снимков: сначала запустите collect')
    records = dedupe(records)
    rows, untagged, multi = aggregate(records)
    models, legacy = model_usage(records)
    print_sources(sources)
    print_table(rows, untagged, multi, len(records))
    print()
    print_models(models)
    if legacy:
        print(f'внимание: {legacy} записей формата 1 без данных о моделях')


def load_titles(path):
    """Названия из profiles.yml для summary; без файла — названия тегов."""
    try:
        from ai_monitor import load_profiles
        return {key: profile['title'] for key, profile in load_profiles(path).items()}
    except (RuntimeError, ValueError, OSError) as exc:
        print(f'profiles.yml не загружен, названия = теги: {exc}', file=sys.stderr)
        return {}


def render_summary(rows, untagged, multi, total, sources, titles, generated):
    import yaml
    header = [f'# Сформировано: {generated}', '# Источники:']
    header += [f"#   {s['host']}: собрано {s['collected_at']}, сессий {s['count']}" for s in sources]
    header.append(f'# Сессий после дедупликации: {total}; без тегов: {untagged}')
    if multi:
        header.append('# Сессии с несколькими тегами (учтены в каждом):')
        header += [f"#   {r['host']}:{r['id']} [{', '.join(tags)}]" for r, tags in multi]
    warnings = []
    data = {}
    for tag, row in rows.items():
        m, d = row['means'], row['medians']
        if not TAG_RE.fullmatch(tag):
            warnings.append(f'тег {tag!r} не пройдёт проверку ключа profiles.yml')
        if m[0] <= 0 or m[2] <= 0:
            warnings.append(f'тег {tag!r}: среднее input или output = 0, profiles.yml такой не примет')
        data[tag] = {
            'title': titles.get(tag, tag),
            'input': m[0],
            'output': m[2],
            'cache_read': m[1],
            'note': f"n={row['n']}; медианы: input={d[0]}, cache_read={d[1]}, output={d[2]}",
        }
    header += [f'# ВНИМАНИЕ: {w}' for w in warnings]
    body = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False) if data else '{}\n'
    return '\n'.join(header) + '\n\n' + body


def write_atomic(path, text):
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + '.', suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(text)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def snapshot_of(host, payload, sessions):
    return {'host': host,
            'format': FORMAT,
            'collected_at': now_iso(),
            'exported_at': payload['exported_at'],
            'limit': payload.get('limit', LIMIT_SESSIONS),
            'truncated': bool(payload.get('truncated')),
            'sessions': sessions}


def load_hosts(path):
    if not path.exists():
        raise RuntimeError(f'Нет файла {path}: скопируйте stats-hosts.example.yml или используйте collect --local')
    import yaml
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    hosts = data.get('hosts') if isinstance(data, dict) else None
    if not isinstance(hosts, list) or not hosts:
        raise RuntimeError('stats-hosts.yml: нужен непустой список hosts')
    result = []
    names = set()
    for entry in hosts:
        if not isinstance(entry, dict):
            raise RuntimeError('stats-hosts.yml: каждый хост — mapping с полями name и ssh')
        name = entry.get('name')
        ssh = entry.get('ssh')
        if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', name) or name == LOCAL_HOST:
            raise RuntimeError(f'stats-hosts.yml: некорректное name {name!r}')
        if name in names:
            raise RuntimeError(f'stats-hosts.yml: повторяется name {name!r}')
        if not isinstance(ssh, str) or not ssh.strip() or ssh.startswith('-'):
            raise RuntimeError(f'stats-hosts.yml: некорректный ssh для {name}')
        python = entry.get('python', 'python3')
        opencode = entry.get('opencode', 'opencode')
        if not isinstance(python, str) or not isinstance(opencode, str):
            raise RuntimeError(f'stats-hosts.yml: python/opencode для {name} должны быть строками')
        names.add(name)
        result.append({'name': name, 'ssh': ssh.strip(), 'python': python, 'opencode': opencode})
    return result


def fetch_host(host, script):
    remote = f"{shlex.quote(host['python'])} - --opencode {shlex.quote(host['opencode'])} export"
    command = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10', host['ssh'], remote]
    result = subprocess.run(command, input=script, capture_output=True, timeout=COLLECT_TIMEOUT)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace').strip() or f'ssh exit {result.returncode}')
    return json.loads(result.stdout)


def write_snapshot(name, snapshot):
    write_atomic(SNAPSHOT_DIR / f'{name}.json', json.dumps(snapshot, ensure_ascii=False, indent=1))


def cmd_collect(args):
    hosts = [] if args.local else load_hosts(args.hosts)
    if args.host:
        hosts = [h for h in hosts if h['name'] == args.host]
        if not hosts:
            raise SystemExit(f'Хост {args.host!r} не найден в {args.hosts}')
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    failed = []
    if args.local or not args.host:
        try:
            payload = export_payload()
            write_snapshot(LOCAL_HOST, snapshot_of(LOCAL_HOST, payload, payload['sessions']))
            print(f"{LOCAL_HOST}: {len(payload['sessions'])} сессий"
                  + (' (выборка обрезана лимитом)' if payload.get('truncated') else ''))
        except (RuntimeError, ValueError, OSError) as exc:
            failed.append(LOCAL_HOST)
            print(f"{LOCAL_HOST}: ОШИБКА: {exc} (прежний снимок сохранён)", file=sys.stderr)
    script = (ROOT / 'session_stats.py').read_bytes()
    for host in hosts:
        try:
            data = fetch_host(host, script)
            sessions = validate_export(data)
            write_snapshot(host['name'], snapshot_of(host['name'], data, sessions))
            print(f"{host['name']}: {len(sessions)} сессий"
                  + (' (выборка обрезана лимитом)' if data.get('truncated') else ''))
        except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as exc:
            failed.append(host['name'])
            print(f"{host['name']}: ОШИБКА: {exc} (прежний снимок сохранён)", file=sys.stderr)
    records, sources = read_snapshots()
    if not sources:
        raise RuntimeError('нет ни одного снимка для summary')
    records = dedupe(records)
    rows, untagged, multi = aggregate(records)
    titles = load_titles(args.profiles)
    generated = now_iso()
    write_atomic(SUMMARY_PATH, render_summary(rows, untagged, multi, len(records), sources, titles, generated))
    print(f'summary: {SUMMARY_PATH} (тегов {len(rows)}, сессий {len(records)})')
    models, legacy = model_usage(records)
    write_atomic(MODELS_PATH, render_models(models, sources, legacy, generated))
    print(f'models: {MODELS_PATH} (моделей {len(models)})')
    if failed:
        print('Частичный сбор, не удалось: ' + ', '.join(failed), file=sys.stderr)
        sys.exit(1)


def cmd_export(args):
    print(json.dumps(export_payload(), ensure_ascii=False))


def main():
    global OPENCODE
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--profiles', type=Path, default=ROOT / 'profiles.yml',
                        help='profiles.yml: ключи для tag, названия для summary')
    parser.add_argument('--opencode', default='opencode', help='путь к бинарнику opencode')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('list').set_defaults(func=cmd_list)
    tag = commands.add_parser('tag')
    tag.add_argument('session')
    tag.add_argument('tag')
    tag.set_defaults(func=cmd_tag)
    show = commands.add_parser('show')
    show.add_argument('session')
    show.set_defaults(func=cmd_show)
    commands.add_parser('stats').set_defaults(func=cmd_stats)
    collect = commands.add_parser('collect')
    scope = collect.add_mutually_exclusive_group()
    scope.add_argument('--host', help='обновить только этот хост из stats-hosts.yml')
    scope.add_argument('--local', action='store_true', help='обновить только локальный снимок')
    collect.add_argument('--hosts', type=Path, default=ROOT / 'stats-hosts.yml')
    collect.set_defaults(func=cmd_collect)
    commands.add_parser('export').set_defaults(func=cmd_export)
    args = parser.parse_args()
    OPENCODE = args.opencode
    import signal
    if hasattr(signal, 'SIGPIPE'):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    try:
        args.func(args)
    except RuntimeError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
