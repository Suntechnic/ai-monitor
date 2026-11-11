#!/usr/bin/env python3
"""Пометки сессий OpenCode и статистика для калибровки profiles.yml.

Тег хранится в metadata.tag сессии (PATCH /api/session/{id}) и читается
обратно из /api/session вместе с токенами. Данные через `opencode api`,
который сам находит фоновый сервер и авторизацию.

Команды:
  list                     все сессии с токенами: тег, папка, название, токены
  tag <id|last|префикс> <тег>   поставить тег («-» снять)
  stats                    средние по тегам: вход / кеш / выход+reasoning
  show <id|last|префикс>   сырые поля одной сессии

Рекомендуемые теги: admin, ii, scripting, php, php-tosir.
"""
import argparse
import json
import statistics
import subprocess
import sys
from collections import defaultdict

HOME = '/home/alex/'


def api(path):
    result = subprocess.run(['opencode', 'api', 'get', path],
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'opencode api failed: {result.stderr.strip()}')
    data = json.loads(result.stdout)
    return data.get('data', data) if isinstance(data, dict) else data


def patch_session(session_id, body):
    result = subprocess.run(
        ['opencode', 'api', 'patch', f'/api/session/{session_id}',
         '--data', json.dumps(body, ensure_ascii=False)],
        capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'opencode api failed: {result.stderr.strip()}')


def real_sessions():
    """Сессии с непустыми токенами, отсортированные по времени обновления."""
    items = [s for s in api('/api/session') if s.get('tokens')]
    items = [s for s in items
             if sum([s['tokens'].get('input', 0), s['tokens'].get('output', 0),
                     s['tokens'].get('reasoning', 0),
                     s['tokens'].get('cache', {}).get('read', 0)]) > 0]
    items.sort(key=lambda s: s.get('time', {}).get('updated', 0))
    return items


def resolve(pattern, items):
    if pattern == 'last':
        return items[-1]
    matches = [s for s in items if s['id'] == pattern]
    if not matches:
        matches = [s for s in items if s['id'].startswith(pattern)]
    if len(matches) != 1:
        raise SystemExit(f'Pattern {pattern!r} matches {len(matches)} sessions; use more characters')
    return matches[0]


def out_in_cache(session):
    tokens = session['tokens']
    return (tokens.get('input', 0),
            tokens.get('cache', {}).get('read', 0),
            tokens.get('output', 0) + tokens.get('reasoning', 0))


def row(session):
    session_id, tag = session['id'], (session.get('metadata') or {}).get('tag') or '—'
    directory = (session.get('location') or {}).get('directory', '?').replace(HOME, '~')
    title = (session.get('title') or '(без названия)')[:42]
    model = (session.get('model') or {}).get('id') or '?'
    cost = session.get('cost') or 0
    return session_id, tag, directory, title, model, cost


def cmd_list(_args):
    print(f"{'id':20} {'тег':12} {'папка':28} {'название':42} {'модель':28} {'вход':>9} {'кеш':>9} {'выход':>9} {'$':>9}")
    for session in real_sessions():
        session_id, tag, directory, title, model, cost = row(session)
        enter, cache, output = out_in_cache(session)
        print(f'{session_id:20} {tag:12} {directory:28} {title:42} {model:28} {enter:9} {cache:9} {output:9} {cost:9.4f}')


def cmd_tag(args):
    items = real_sessions()
    session = resolve(args.session, items)
    metadata = session.get('metadata') or {}
    if args.tag == '-':
        metadata.pop('tag', None)
    else:
        metadata['tag'] = args.tag
    patch_session(session['id'], {'metadata': metadata})
    title = (session.get('title') or '')[:50]
    print(f"{session['id']} tag={metadata.get('tag', '—')} | {title}")


def cmd_stats(_args):
    groups = defaultdict(list)
    for session in real_sessions():
        groups[(session.get('metadata') or {}).get('tag') or '—'].append(session)
    print(f"{'тег':12} {'n':>3} {'вход':>12} {'кеш':>12} {'выход':>10} {'соотн.':>8}")
    for tag, sessions in sorted(groups.items()):
        if tag == '—':
            continue
        columns = list(zip(*[out_in_cache(s) for s in sessions]))
        enter, cache, output = (statistics.mean(c) for c in columns)
        ratio = (enter + cache) / output if output else 0
        print(f'{tag:12} {len(sessions):3} {enter:12.0f} {cache:12.0f} {output:10.0f} {ratio:8.1f}')
    untagged = len(groups.get('—', []))
    if untagged:
        print(f'без тега: {untagged} сессий')


def cmd_show(args):
    session = resolve(args.session, real_sessions())
    print(json.dumps(session, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('list').set_defaults(func=cmd_list)
    tag = commands.add_parser('tag')
    tag.add_argument('session')
    tag.add_argument('tag')
    tag.set_defaults(func=cmd_tag)
    commands.add_parser('stats').set_defaults(func=cmd_stats)
    show = commands.add_parser('show')
    show.add_argument('session')
    show.set_defaults(func=cmd_show)
    args = parser.parse_args()
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
