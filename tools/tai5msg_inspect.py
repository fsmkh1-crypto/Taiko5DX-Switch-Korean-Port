from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

DEFAULT_INDEX = Path('selective_ko/artifacts/tai5msg_fast_source_cache_v1/INDEX.json')
LOCATOR_RE = re.compile(r'^(?:TAI5MSG:)?B(\d+):M(\d+)$', re.I)
RANGE_RE = re.compile(r'^(?:TAI5MSG:)?B(\d+):M(\d+)\.\.M?(\d+)$', re.I)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _guard(path: Path, size: int, sha256: str) -> bytes:
    data = path.read_bytes()
    if len(data) != size or _sha(data) != sha256:
        raise SystemExit(f'cache integrity mismatch: {path}')
    return data


def _rows(raw: bytes) -> list[dict]:
    return [json.loads(line) for line in raw.decode('utf-8').splitlines() if line]


def load_cache(index_path: Path, full_cache: Path | None = None) -> tuple[dict, list[dict], str]:
    index = json.loads(index_path.read_text(encoding='utf-8'))
    if index.get('schema') != 'TAI5MSG_FAST_SOURCE_CACHE_V1':
        raise SystemExit(f'unsupported cache schema: {index.get("schema")}')
    if full_cache is not None:
        meta = index['drive_cache']['files']['b24_source_cache']
        raw = _guard(full_cache, int(meta['size']), str(meta['sha256']))
        rows = _rows(raw)
        if len(rows) != int(meta['rows']):
            raise SystemExit('full B24 cache row count mismatch')
        return index, rows, 'DRIVE_FULL_B24_CACHE'
    meta = index['git_anchor_cache']
    raw = _guard(index_path.parent / meta['path'], int(meta['bytes']), str(meta['sha256']))
    rows = _rows(raw)
    if len(rows) != int(meta['rows']):
        raise SystemExit('Git anchor cache row count mismatch')
    return index, rows, 'GIT_ANCHOR_CACHE'


def parse_locator(text: str) -> tuple[int, int]:
    m = LOCATOR_RE.match(text.strip())
    if not m:
        raise argparse.ArgumentTypeError(f'invalid locator: {text}')
    return int(m.group(1)), int(m.group(2))


def expand_range(text: str) -> list[tuple[int, int]]:
    m = RANGE_RE.match(text.strip())
    if not m:
        raise argparse.ArgumentTypeError(f'invalid range: {text}')
    block, start, stop = map(int, m.groups())
    if stop < start:
        raise argparse.ArgumentTypeError('range stop precedes start')
    return [(block, i) for i in range(start, stop + 1)]


def main() -> int:
    p = argparse.ArgumentParser(description='Fast TAI5MSG cache inspector. Uses canonical derived cache; never reopens the PC patcher.')
    p.add_argument('--index', type=Path, default=DEFAULT_INDEX)
    p.add_argument('--full-cache', type=Path, help='Materialized Drive B24_SOURCE_CACHE.jsonl for M221..M344; hash-guarded by INDEX.json')
    p.add_argument('--locator', action='append', default=[], help='e.g. B24:M229; repeatable')
    p.add_argument('--range', dest='ranges', action='append', default=[], help='e.g. B24:M221..M229; repeatable')
    p.add_argument('--json', action='store_true')
    p.add_argument('--hex', action='store_true', help='include raw message hex in text output')
    p.add_argument('--source-identities', action='store_true')
    args = p.parse_args()

    index, rows, cache_kind = load_cache(args.index, args.full_cache)
    by_key = {(int(r['block']), int(r['local'])): r for r in rows}
    wanted: list[tuple[int, int]] = []
    for item in args.locator:
        wanted.append(parse_locator(item))
    for item in args.ranges:
        wanted.extend(expand_range(item))
    if not wanted:
        wanted = [(24, 229)]
    wanted = list(dict.fromkeys(wanted))
    missing = [x for x in wanted if x not in by_key]
    if missing:
        hint = '' if args.full_cache else ' (materialize Drive B24_SOURCE_CACHE.jsonl and pass --full-cache for M221..M344)'
        raise SystemExit('locator not present in active cache: ' + ', '.join(f'B{b}:M{m}' for b, m in missing) + hint)
    selected = [by_key[x] for x in wanted]

    if args.json:
        payload: object = selected
        if args.source_identities:
            payload = {'cache_kind': cache_kind, 'source_identity': index['source_identity'], 'rows': selected}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f'cache={cache_kind}')
    if args.source_identities:
        print(json.dumps(index['source_identity'], ensure_ascii=False, indent=2))
    for row in selected:
        print(f"[{row['locator']}] runtime={row['runtime_message_id']}")
        for label in ('jp', 'pc_ko'):
            x = row[label]
            print(f"{label}: len={x['length']} sha256={x['sha256']}")
            print(x['decoded'])
            print('controls=' + json.dumps(x['controls'], ensure_ascii=False, separators=(',', ':')) + f" terminator={x['terminator_hex']}")
            if args.hex:
                print('hex=' + x['hex'])
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
