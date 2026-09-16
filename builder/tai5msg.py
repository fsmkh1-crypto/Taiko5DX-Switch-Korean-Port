from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import struct

INPUT_SHA = "e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090"
OUTPUT_SHA = "993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06"
INDEX_SHA = "587464c402538b31ffc10c4726e953f5c54b33cfd92f6fd9c14cd37de27c7a00"
MANIFEST_SET_SHA = "a17b5b493a4f529e6aa308954242434e13bede0dda14b075cc13a3a890bc254c"
TAI5MSG_BLOCK_COUNT = 33
TAI5MSG_MESSAGE_COUNT = 14_832
COMPACT_OCCURRENCES = 44
COMPACT_MESSAGES = 33
COMBINED_MESSAGES = 158
COMBINED_BLOCKS = {1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,21,24}
COMPACT_BLOCKS = {1:4,2:2,3:2,4:6,6:1,8:5,9:8,10:5,11:1,13:2,14:1,15:5,16:2}
MANIFEST_ROWS = 125
GRAMMAR_REMOVED = 177
PRESERVED_CALLS = 125
GRAMMAR_DELTA = -645
ALIGN = 0x40
PRESERVE_ON = b"\x1b\x6b"
PRESERVE_OFF = b"\x1b\x48"
MANIFEST_REL = Path("selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1")

# Backward-compatible public constants used by the builder/reporting code.
TAI5MSG_INPUT_SHA256 = INPUT_SHA
TAI5MSG_OUTPUT_SHA256 = OUTPUT_SHA
TAI5MSG_EXPECTED_COMPACT_OCCURRENCES = COMPACT_OCCURRENCES
TAI5MSG_EXPECTED_CHANGED_MESSAGES = COMBINED_MESSAGES
TAI5MSG_EXPECTED_SIZE_GROWTH = 0


@dataclass(frozen=True)
class Tai5MsgReconstructionReport:
    input_sha256: str
    output_sha256: str
    block_count: int
    message_count: int
    compact_occurrences: int
    changed_messages: int
    affected_blocks: int
    grown_blocks: int
    input_size: int
    output_size: int
    size_growth: int

    def to_dict(self) -> dict[str, int | str]:
        return asdict(self)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _decrypt(data: bytes) -> bytes:
    return bytes((x + 0x5B) & 0xFF for x in data)


def _encrypt(data: bytes) -> bytes:
    return bytes((x - 0x5B) & 0xFF for x in data)


def _trailing(data: bytes, value: int) -> int:
    p = len(data)
    while p and data[p - 1] == value:
        p -= 1
    return len(data) - p


def _lead(x: int) -> bool:
    return 0x81 <= x <= 0x9F or 0xE0 <= x <= 0xFC


def _compact_positions(message: bytes) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    state = "DEFAULT_OFF"
    p = 0
    while p < len(message):
        x = message[p]
        if x == 0x02 and p + 2 < len(message):
            p += 3
            continue
        if x in (0x1A, 0x1B) and p + 1 < len(message):
            sub = message[p + 1]
            if x == 0x1B:
                if sub == 0x6B: state = "ON"
                elif sub == 0x48: state = "OFF_H"
                elif sub == 0x4B: state = "OFF_K"
            p += 3 if sub == 0x43 and p + 2 < len(message) else 2
            continue
        if x == 0x01 and p + 1 < len(message):
            sub = message[p + 1]
            p += 4 if sub in (0x43, 0x4A) and p + 3 < len(message) else 2
            continue
        if x == 0x05 and p + 2 < len(message) and message[p + 1] == 0x05 and 0x04 <= message[p + 2] <= 0x09:
            p += 3
            continue
        if _lead(x) and p + 1 < len(message):
            p += 2
            continue
        if 0xA6 <= x <= 0xDF:
            out.append((p, state))
        p += 1
    return out


def _header(blob: bytes) -> list[tuple[int, int]]:
    if len(blob) < 0x140:
        raise RuntimeError("TAI5MSG too short")
    pairs = [struct.unpack_from("<II", blob, i * 8) for i in range(TAI5MSG_BLOCK_COUNT)]
    if pairs[0][0] != 0x140:
        raise RuntimeError("TAI5MSG header guard failed")
    for i in range(TAI5MSG_BLOCK_COUNT - 1):
        off, size = pairs[i]
        if off % ALIGN or size % ALIGN or off + size != pairs[i + 1][0]:
            raise RuntimeError("TAI5MSG block-layout guard failed")
    if pairs[-1][0] >= len(blob):
        raise RuntimeError("TAI5MSG final-block guard failed")
    return pairs


def _block(blob: bytes, pairs: list[tuple[int, int]], bi: int) -> tuple[bytes,int,list[int],list[bytes],int]:
    off, declared = pairs[bi]
    end = pairs[bi + 1][0] if bi + 1 < len(pairs) else len(blob)
    raw = blob[off:end]
    dec = _decrypt(raw)
    if len(dec) < 2:
        raise RuntimeError(f"TAI5MSG block {bi} truncated")
    count = struct.unpack_from("<H", dec, 0)[0]
    table_end = 2 + 4 * count
    if table_end > len(dec):
        raise RuntimeError(f"TAI5MSG block {bi} table truncated")
    offsets = [struct.unpack_from("<I", dec, 2 + 4 * i)[0] for i in range(count)]
    if not offsets or offsets[0] != table_end or offsets != sorted(offsets):
        raise RuntimeError(f"TAI5MSG block {bi} offsets invalid")
    core_end = len(dec) - _trailing(dec, 0x5B)
    if offsets[-1] >= core_end:
        raise RuntimeError(f"TAI5MSG block {bi} final offset invalid")
    messages = []
    for i, start in enumerate(offsets):
        stop = offsets[i + 1] if i + 1 < count else core_end
        if not start < stop <= core_end:
            raise RuntimeError(f"TAI5MSG block {bi} message bounds invalid")
        messages.append(dec[start:stop])
    return raw, declared, offsets, messages, len(dec) - core_end


def _manifest() -> tuple[dict, list[list]]:
    root = Path(__file__).resolve().parent.parent / MANIFEST_REL
    index_bytes = (root / "INDEX.json").read_bytes()
    if _sha(index_bytes) != INDEX_SHA:
        raise RuntimeError("TAI5MSG V288 manifest index hash failed")
    index = json.loads(index_bytes)
    if index.get("schema") != "KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_PATCH_V1" or index.get("validation_id") != "V288":
        raise RuntimeError("TAI5MSG V288 manifest identity failed")
    if index.get("canonical_input") != [2_134_366, INPUT_SHA, TAI5MSG_BLOCK_COUNT, TAI5MSG_MESSAGE_COUNT]:
        raise RuntimeError("TAI5MSG V288 manifest input failed")
    if index.get("authority") != [MANIFEST_ROWS, GRAMMAR_REMOVED, 113, 0, OUTPUT_SHA]:
        raise RuntimeError("TAI5MSG V288 manifest authority failed")
    if index.get("manifest_set_sha256") != MANIFEST_SET_SHA or index.get("row_count") != MANIFEST_ROWS:
        raise RuntimeError("TAI5MSG V288 manifest-set failed")
    checks = index.get("global_checks", {})
    expected = {
        "row_count": MANIFEST_ROWS,
        "grammar_removed_total": GRAMMAR_REMOVED,
        "grammar_target_residual_total": 0,
        "preserved_non_register_calls_total": PRESERVED_CALLS,
        "non_register_sequence_mismatches": 0,
        "control_branch_mismatches": 0,
        "grammar_logical_delta": GRAMMAR_DELTA,
        "grammar125_compact33_overlap": 0,
        "combined_changed_messages": COMBINED_MESSAGES,
        "grown_blocks": 0,
        "reconstructed_sha256": OUTPUT_SHA,
        "unknown_total": 0,
        "unresolved_total": 0,
        "conflict_total": 0,
    }
    if any(checks.get(k) != v for k, v in expected.items()):
        raise RuntimeError("TAI5MSG V288 manifest global guard failed")
    rows: list[list] = []
    hashes: list[str] = []
    start = 0
    shards = index.get("shards", [])
    if len(shards) != 4:
        raise RuntimeError("TAI5MSG V288 shard-count failed")
    for meta in shards:
        payload = (root / meta["path"]).read_bytes()
        ph = _sha(payload)
        if len(payload) != meta["bytes"] or ph != meta["sha256"]:
            raise RuntimeError(f"TAI5MSG V288 shard guard failed: {meta['path']}")
        obj = json.loads(payload)
        part = obj.get("rows")
        if obj.get("row_start") != start or obj.get("row_count") != meta["row_count"] or not isinstance(part, list) or len(part) != meta["row_count"]:
            raise RuntimeError(f"TAI5MSG V288 shard rows failed: {meta['path']}")
        rows.extend(part)
        hashes.append(ph)
        start += len(part)
    if _sha(("\n".join(hashes) + "\n").encode("ascii")) != MANIFEST_SET_SHA or len(rows) != MANIFEST_ROWS:
        raise RuntimeError("TAI5MSG V288 manifest replay failed")
    return index, rows


def _grammar(parsed: list[tuple[bytes,int,list[int],list[bytes],int]], rows: list[list]) -> tuple[dict[tuple[int,int],bytes],set[int]]:
    targets: dict[tuple[int,int],bytes] = {}
    blocks: set[int] = set()
    removed = preserved = delta = 0
    for n, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 12:
            raise RuntimeError(f"TAI5MSG V288 row schema failed: {n}")
        bi, mi, _resp, slen, ssha, tlen, tsha, edits, _families, rem, calls, control = row
        loc = (bi, mi)
        if loc in targets or not (0 <= bi < len(parsed)) or not (0 <= mi < len(parsed[bi][3])):
            raise RuntimeError(f"TAI5MSG V288 locator failed: {bi}:{mi}")
        source = parsed[bi][3][mi]
        if len(source) != slen or _sha(source) != ssha or not isinstance(control, str) or len(control) != 64:
            raise RuntimeError(f"TAI5MSG V288 source guard failed: {bi}:{mi}")
        normalized = []
        for edit in edits:
            if not isinstance(edit, list) or len(edit) != 3:
                raise RuntimeError(f"TAI5MSG V288 edit schema failed: {bi}:{mi}")
            a, b, hx = edit
            if not (0 <= a <= b <= len(source)):
                raise RuntimeError(f"TAI5MSG V288 edit bounds failed: {bi}:{mi}")
            normalized.append((a, b, bytes.fromhex(hx)))
        target = source
        limit = len(source)
        for a, b, replacement in sorted(normalized, reverse=True):
            if b > limit:
                raise RuntimeError(f"TAI5MSG V288 edit overlap failed: {bi}:{mi}")
            target = target[:a] + replacement + target[b:]
            limit = a
        if len(target) != tlen or _sha(target) != tsha:
            raise RuntimeError(f"TAI5MSG V288 target guard failed: {bi}:{mi}")
        targets[loc] = target
        blocks.add(bi)
        removed += rem
        preserved += len(calls)
        delta += tlen - slen
    if len(targets) != MANIFEST_ROWS or removed != GRAMMAR_REMOVED or preserved != PRESERVED_CALLS or delta != GRAMMAR_DELTA:
        raise RuntimeError("TAI5MSG V288 grammar accounting failed")
    return targets, blocks


def reconstruct_tai5msg_switch_native(blob: bytes) -> tuple[bytes, Tai5MsgReconstructionReport]:
    input_sha = _sha(blob)
    if input_sha != INPUT_SHA:
        raise RuntimeError("TAI5MSG input hash guard failed; canonical PC v1.02 payload required")
    pairs = _header(blob)
    parsed = [_block(blob, pairs, bi) for bi in range(TAI5MSG_BLOCK_COUNT)]
    if sum(len(x[3]) for x in parsed) != TAI5MSG_MESSAGE_COUNT:
        raise RuntimeError("TAI5MSG message-count failed")

    compact: dict[tuple[int,int],list[int]] = {}
    histogram: Counter[int] = Counter()
    for bi, item in enumerate(parsed):
        for mi, message in enumerate(item[3]):
            scan = _compact_positions(message)
            if any(state not in ("DEFAULT_OFF", "OFF_H") for _p, state in scan):
                raise RuntimeError("TAI5MSG compact source state failed")
            pos = [p for p, _state in scan]
            if pos:
                compact[(bi, mi)] = pos
                histogram[bi] += len(pos)
    if sum(map(len, compact.values())) != COMPACT_OCCURRENCES or len(compact) != COMPACT_MESSAGES or dict(sorted(histogram.items())) != COMPACT_BLOCKS:
        raise RuntimeError("TAI5MSG compact census failed")

    index, rows = _manifest()
    grammar, grammar_blocks = _grammar(parsed, rows)
    if set(grammar) & set(compact):
        raise RuntimeError("TAI5MSG grammar/compact overlap failed")
    blocks = grammar_blocks | set(histogram)
    if blocks != COMBINED_BLOCKS:
        raise RuntimeError("TAI5MSG affected-block set failed")

    rebuilt_blocks: list[bytes] = []
    padding: dict[int,int] = {}
    for bi, (raw, declared, _offsets, messages, _trailing_count) in enumerate(parsed):
        if bi not in blocks:
            rebuilt_blocks.append(raw)
            continue
        if len(raw) != declared:
            raise RuntimeError(f"TAI5MSG affected block physical-size failed: {bi}")
        table_end = 2 + 4 * len(messages)
        updated = []
        for mi, source in enumerate(messages):
            loc = (bi, mi)
            message = grammar.get(loc, source)
            for p in sorted(compact.get(loc, []), reverse=True):
                message = message[:p] + PRESERVE_ON + message[p:p+1] + PRESERVE_OFF + message[p+1:]
            updated.append(message)
        used = table_end + sum(map(len, updated))
        if used > declared:
            raise RuntimeError(f"TAI5MSG fixed-block capacity failed: {bi}")
        padding[bi] = declared - used
        offsets = []
        cursor = table_end
        for message in updated:
            offsets.append(cursor)
            cursor += len(message)
        dec = bytearray(struct.pack("<H", len(updated)))
        for off in offsets:
            dec += struct.pack("<I", off)
        dec += b"".join(updated)
        dec += bytes([0x5B]) * (declared - len(dec))
        if len(dec) != declared:
            raise RuntimeError(f"TAI5MSG rebuilt-size failed: {bi}")
        rebuilt_blocks.append(_encrypt(bytes(dec)))

    expected_padding = {int(k): v for k, v in index.get("block_final_padding", {}).items()}
    if any(padding.get(k) != v for k, v in expected_padding.items()) or min(padding.values()) != 13:
        raise RuntimeError("TAI5MSG V288 padding ledger failed")
    rebuilt = blob[:pairs[0][0]] + b"".join(rebuilt_blocks)
    if len(rebuilt) != len(blob) or rebuilt[:pairs[0][0]] != blob[:pairs[0][0]] or _sha(rebuilt) != OUTPUT_SHA:
        raise RuntimeError("TAI5MSG V288 deterministic output failed")
    new_pairs = _header(rebuilt)
    if new_pairs != pairs:
        raise RuntimeError("TAI5MSG header-pair identity failed")

    post = [_block(rebuilt, new_pairs, bi) for bi in range(TAI5MSG_BLOCK_COUNT)]
    changed = 0
    changed_blocks: set[int] = set()
    protected = unprotected = 0
    post_by_loc: dict[tuple[int,int],bytes] = {}
    for bi, item in enumerate(post):
        for mi, message in enumerate(item[3]):
            post_by_loc[(bi, mi)] = message
            if message != parsed[bi][3][mi]:
                changed += 1
                changed_blocks.add(bi)
            for _p, state in _compact_positions(message):
                protected += state == "ON"
                unprotected += state != "ON"
    if sum(len(x[3]) for x in post) != TAI5MSG_MESSAGE_COUNT or changed != COMBINED_MESSAGES or changed_blocks != COMBINED_BLOCKS:
        raise RuntimeError("TAI5MSG V288 post-reparse accounting failed")
    if protected != COMPACT_OCCURRENCES or unprotected:
        raise RuntimeError("TAI5MSG compact preservation failed")
    for row in rows:
        message = post_by_loc[(row[0], row[1])]
        if len(message) != row[5] or _sha(message) != row[6]:
            raise RuntimeError(f"TAI5MSG V288 post-target failed: {row[0]}:{row[1]}")

    return rebuilt, Tai5MsgReconstructionReport(
        input_sha256=input_sha,
        output_sha256=OUTPUT_SHA,
        block_count=TAI5MSG_BLOCK_COUNT,
        message_count=TAI5MSG_MESSAGE_COUNT,
        compact_occurrences=COMPACT_OCCURRENCES,
        changed_messages=changed,
        affected_blocks=len(changed_blocks),
        grown_blocks=0,
        input_size=len(blob),
        output_size=len(rebuilt),
        size_growth=0,
    )
