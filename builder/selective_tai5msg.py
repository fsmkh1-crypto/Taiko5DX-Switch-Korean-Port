from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import struct
from typing import AbstractSet, Iterable, Mapping, Sequence

from builder.tai5msg_corrections import CorrectionOverlayError, MessageCorrection, apply_correction, load_overlay

STOCK_SIZE = 1_810_889
STOCK_SHA256 = "aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f"
PC_KO_SIZE = 2_134_366
PC_KO_SHA256 = "e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090"

V315_INTERMEDIATE_SIZE = 1_840_073
V315_INTERMEDIATE_SHA256 = "b212da65010d3a2e7ff6f7b8e10ce57371cb67e3093f58a6ad16a085399a8d0d"

BLOCK_COUNT = 33
MESSAGE_COUNT = 14_832
HEADER_SIZE = 0x140
HEADER_PAIR_BYTES = BLOCK_COUNT * 8
ALIGN = 0x40
RUNTIME_BLOCK_CAPACITY = 0x20000

EXPECTED_SELECTED = 3_179
EXPECTED_UNSELECTED = 11_653
EXPECTED_R1 = 3_158
EXPECTED_R2 = 21
EXPECTED_GROWTH = 0x70C0
EXPECTED_FINAL_SIZE = 0x1C1289
EXPECTED_B32_OFFSET = 0x1B4840
EXPECTED_B32_USED_END = 0xB8D5
EXPECTED_B32_DECLARED = 0xCA80
EXPECTED_B32_PHYSICAL = 0xCA49
EXPECTED_B32_OMITTED = 0x37
EXPECTED_LARGEST_DECLARED = 0x12B00
EXPECTED_DIAGNOSTIC_SHA256 = "fd4c8b9f527f67f667d5fded6bdb4703607b70e8b6addf1f41c5d11ebf93e85c"

EXPECTED_UNIQUE_TWO_BYTE_CODES = 1_011
EXPECTED_TWO_BYTE_OCCURRENCES = 225_719
EXPECTED_UNIQUE_KOREAN_ADDED_CODES = 992
EXPECTED_KOREAN_ADDED_OCCURRENCES = 219_210

V303_DIR = Path("selective_ko/artifacts/tai5msg_caller_resolved_3179_candidate_classification_v1")
V304_DIR = Path("selective_ko/artifacts/tai5msg_v303_pc_payload_defect_correction_2_v1")
V315_DIR = Path("selective_ko/artifacts/tai5msg_b24_semantic_layout_correction_v1")
V320_DIR = Path("selective_ko/artifacts/tai5msg_b24_native_wrap_layout_correction_v1")
STRUCTURE_DIR = Path("selective_ko/artifacts/tai5msg_structure_index_v1")


class SelectiveTai5MsgError(RuntimeError):
    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class ParsedBlock:
    index: int
    file_offset: int
    declared_size: int
    physical_size: int
    message_count: int
    table_end: int
    offsets: tuple[int, ...]
    messages: tuple[bytes, ...]
    used_end: int
    physical_filler_bytes: int
    declared_minus_physical: int


@dataclass(frozen=True)
class ParsedTai5Msg:
    header: bytes
    pairs: tuple[tuple[int, int], ...]
    blocks: tuple[ParsedBlock, ...]

    @property
    def message_count(self) -> int:
        return sum(block.message_count for block in self.blocks)


@dataclass(frozen=True)
class V303Membership:
    rows: tuple[dict, ...]
    locators: frozenset[tuple[int, int]]


@dataclass(frozen=True)
class V304Correction:
    candidate_id: str
    classification_id: str
    block: int
    local: int
    source_length: int
    source_sha256: str
    source_bytes: bytes
    delete_offset: int
    target_length: int
    target_sha256: str
    target_bytes: bytes


@dataclass(frozen=True)
class MetadataPreflightReport:
    selected_rows: int
    growth: int
    final_size: int
    b32_offset: int
    b32_used_end: int
    b32_declared: int
    b32_physical: int
    b32_filler: int
    b32_omitted: int
    largest_declared: int
    growth_blocks: tuple[tuple[int, int], ...]

    def to_dict(self) -> dict:
        out = asdict(self)
        out["growth_blocks"] = [list(x) for x in self.growth_blocks]
        return out


@dataclass(frozen=True)
class SelectiveSerializationReport:
    input_stock_sha256: str
    input_pc_ko_sha256: str
    output_sha256: str
    block_count: int
    message_count: int
    selected_rows: int
    unselected_rows: int
    growth: int
    final_size: int
    b32_offset: int
    b32_used_end: int
    b32_declared: int
    b32_physical: int
    b32_filler: int
    b32_omitted: int
    largest_declared: int
    unique_two_byte_codes: int
    two_byte_occurrences: int
    unique_korean_added_codes: int
    korean_added_occurrences: int
    diagnostic_sha_match: bool

    def to_dict(self) -> dict:
        return asdict(self)


def _fail(code: str, detail: str) -> None:
    raise SelectiveTai5MsgError(code, detail)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_guarded(path: Path, expected_size: int, expected_sha256: str, code: str) -> bytes:
    data = path.read_bytes()
    if len(data) != expected_size or _sha(data) != expected_sha256:
        _fail(code, f"artifact identity mismatch: {path}")
    return data


def _decrypt(data: bytes) -> bytes:
    return bytes((x + 0x5B) & 0xFF for x in data)


def _encrypt(data: bytes) -> bytes:
    return bytes((x - 0x5B) & 0xFF for x in data)


def _align_up(value: int, align: int = ALIGN) -> int:
    return (value + align - 1) & ~(align - 1)


def _trailing_value_count(data: bytes, value: int) -> int:
    pos = len(data)
    while pos and data[pos - 1] == value:
        pos -= 1
    return len(data) - pos


def _is_two_byte_lead(value: int) -> bool:
    return 0x81 <= value <= 0x9F or 0xE0 <= value <= 0xFC


def _is_valid_trail(value: int) -> bool:
    return 0x40 <= value <= 0x7E or 0x80 <= value <= 0xFC


def _is_korean_added_code(code: int) -> bool:
    lead = (code >> 8) & 0xFF
    trail = code & 0xFF
    if not _is_valid_trail(trail):
        return False
    if 0xEB <= lead <= 0xF7:
        return True
    return lead == 0xF8 and trail <= 0xA2


def korean_added_code_domain() -> frozenset[int]:
    out: set[int] = set()
    for lead in range(0xEB, 0xF9):
        for trail in list(range(0x40, 0x7F)) + list(range(0x80, 0xFD)):
            code = (lead << 8) | trail
            if _is_korean_added_code(code):
                out.add(code)
    if len(out) != 2_542:
        _fail("MAPPING_DOMAIN_MISS", f"internal Korean-added domain cardinality is {len(out)}")
    return frozenset(out)


def _header_pairs(blob: bytes) -> tuple[tuple[int, int], ...]:
    if len(blob) < HEADER_SIZE:
        _fail("STOCK_IDENTITY_MISMATCH", "TAI5MSG shorter than header")
    pairs = tuple(struct.unpack_from("<II", blob, i * 8) for i in range(BLOCK_COUNT))
    if pairs[0][0] != HEADER_SIZE:
        _fail("STOCK_IDENTITY_MISMATCH", f"first block offset {pairs[0][0]:#x} != {HEADER_SIZE:#x}")
    for i in range(BLOCK_COUNT - 1):
        off, declared = pairs[i]
        next_off = pairs[i + 1][0]
        if off % ALIGN or declared % ALIGN:
            _fail("POST_OFFSET_FAIL", f"block {i} alignment invalid")
        if off + declared != next_off:
            _fail("POST_OFFSET_FAIL", f"block {i} declared extent does not reach block {i + 1}")
    last_off, last_declared = pairs[-1]
    if last_off % ALIGN or last_declared % ALIGN:
        _fail("POST_OFFSET_FAIL", "final block alignment invalid")
    if last_off >= len(blob) or len(blob) - last_off > last_declared:
        _fail("POST_OFFSET_FAIL", "final block physical extent invalid")
    return pairs


def parse_tai5msg(blob: bytes) -> ParsedTai5Msg:
    pairs = _header_pairs(blob)
    blocks: list[ParsedBlock] = []
    for index, (file_offset, declared_size) in enumerate(pairs):
        physical_end = pairs[index + 1][0] if index + 1 < BLOCK_COUNT else len(blob)
        raw = blob[file_offset:physical_end]
        physical_size = len(raw)
        if index < BLOCK_COUNT - 1 and physical_size != declared_size:
            _fail("POST_OFFSET_FAIL", f"block {index} physical/declaration mismatch")
        if physical_size > declared_size:
            _fail("POST_OFFSET_FAIL", f"block {index} physical size exceeds declaration")

        plain = _decrypt(raw)
        if len(plain) < 2:
            _fail("POST_REPARSE_COUNT_FAIL", f"block {index} truncated")
        count = struct.unpack_from("<H", plain, 0)[0]
        table_end = 2 + 4 * count
        if table_end > len(plain):
            _fail("POST_OFFSET_FAIL", f"block {index} offset table truncated")
        offsets = tuple(struct.unpack_from("<I", plain, 2 + 4 * i)[0] for i in range(count))
        if not offsets or offsets[0] != table_end:
            _fail("POST_OFFSET_FAIL", f"block {index} first offset invalid")
        if any(offsets[i] >= offsets[i + 1] for i in range(len(offsets) - 1)):
            _fail("POST_OFFSET_FAIL", f"block {index} offsets not strictly increasing")

        filler = _trailing_value_count(plain, 0x5B)
        used_end = len(plain) - filler
        if offsets[-1] >= used_end:
            _fail("POST_OFFSET_FAIL", f"block {index} final message offset invalid")

        messages: list[bytes] = []
        for i, start in enumerate(offsets):
            stop = offsets[i + 1] if i + 1 < count else used_end
            if not start < stop <= used_end:
                _fail("POST_OFFSET_FAIL", f"block {index} message {i} bounds invalid")
            messages.append(plain[start:stop])

        blocks.append(
            ParsedBlock(
                index=index,
                file_offset=file_offset,
                declared_size=declared_size,
                physical_size=physical_size,
                message_count=count,
                table_end=table_end,
                offsets=offsets,
                messages=tuple(messages),
                used_end=used_end,
                physical_filler_bytes=filler,
                declared_minus_physical=declared_size - physical_size,
            )
        )

    parsed = ParsedTai5Msg(header=blob[:HEADER_SIZE], pairs=pairs, blocks=tuple(blocks))
    if parsed.message_count != MESSAGE_COUNT:
        _fail("POST_REPARSE_COUNT_FAIL", f"message count {parsed.message_count} != {MESSAGE_COUNT}")
    return parsed


def _parse_wait_expression(expr: str) -> set[tuple[int, int]]:
    block_text, members = expr.split(":", 1)
    block = int(block_text[1:])
    out: set[tuple[int, int]] = set()
    for segment in members.split(","):
        if ".." in segment:
            start, stop = map(int, segment.split("..", 1))
            out.update((block, value) for value in range(start, stop + 1))
        else:
            out.add((block, int(segment)))
    return out


def load_v303_membership(repo_root: Path) -> V303Membership:
    root = repo_root / V303_DIR
    index = json.loads((root / "INDEX.json").read_text(encoding="utf-8"))
    if index.get("schema") != "TAI5MSG_CALLER_RESOLVED_3179_CANDIDATE_CLASSIFICATION_V1":
        _fail("V303_INDEX_OR_SHARD_INTEGRITY_FAIL", "unexpected V303 schema")
    if index.get("validation_id") != "V303":
        _fail("V303_INDEX_OR_SHARD_INTEGRITY_FAIL", "unexpected V303 validation id")

    source_identity = index.get("source_identity", {})
    if source_identity.get("pc_original") != {"size": STOCK_SIZE, "sha256": STOCK_SHA256}:
        _fail("V303_INDEX_OR_SHARD_INTEGRITY_FAIL", "V303 stock source identity mismatch")
    if source_identity.get("pc_korean") != {"size": PC_KO_SIZE, "sha256": PC_KO_SHA256}:
        _fail("V303_INDEX_OR_SHARD_INTEGRITY_FAIL", "V303 PC-KO source identity mismatch")

    rows: list[dict] = []
    concatenated = bytearray()
    for meta in index.get("shards", []):
        path = root / meta["path"]
        payload = _read_guarded(
            path,
            int(meta["size"]),
            str(meta["sha256"]),
            "V303_INDEX_OR_SHARD_INTEGRITY_FAIL",
        )
        concatenated += payload
        part = [json.loads(line) for line in payload.decode("utf-8").splitlines() if line]
        if len(part) != int(meta["row_count"]):
            _fail("V303_INDEX_OR_SHARD_INTEGRITY_FAIL", f"row count mismatch: {meta['path']}")
        rows.extend(part)

    rowset = index.get("rowset", {})
    if len(concatenated) != int(rowset.get("uncompressed_bytes", -1)):
        _fail("V303_INDEX_OR_SHARD_INTEGRITY_FAIL", "V303 concatenated rowset size mismatch")
    if _sha(bytes(concatenated)) != rowset.get("uncompressed_sha256"):
        _fail("V303_INDEX_OR_SHARD_INTEGRITY_FAIL", "V303 concatenated rowset hash mismatch")
    if len(rows) != EXPECTED_SELECTED:
        _fail("V303_MEMBERSHIP_FAIL", f"V303 row count {len(rows)}")

    locators: set[tuple[int, int]] = set()
    usage = Counter()
    realization = Counter()
    by_block = Counter()
    previous = (-1, -1)

    for ordinal, row in enumerate(rows, start=140):
        expected_candidate = f"SEL-CAND-{ordinal:06d}"
        expected_classification = f"SEL-CLS-{ordinal:06d}"
        if row.get("candidate_id") != expected_candidate or row.get("classification_id") != expected_classification:
            _fail("V303_MEMBERSHIP_FAIL", f"non-contiguous V303 id at ordinal {ordinal}")
        if row.get("derived_disposition") != "INCLUDE_KO":
            _fail("V303_MEMBERSHIP_FAIL", f"non-INCLUDE_KO row: {expected_candidate}")
        if row.get("mechanism_class") != "STATIC_COMPLETE" or row.get("investigation_status") != "RESOLVED":
            _fail("V303_MEMBERSHIP_FAIL", f"unresolved/non-static row: {expected_candidate}")

        locator = (int(row["block"]), int(row["local"]))
        if locator in locators:
            _fail("V303_DUPLICATE_LOCATOR", f"duplicate locator {locator}")
        if locator <= previous:
            _fail("V303_MEMBERSHIP_FAIL", f"row order is not strictly ascending at {locator}")
        previous = locator
        locators.add(locator)
        usage[str(row["usage_class"])] += 1
        realization[str(row["realization"])] += 1
        by_block[str(locator[0])] += 1

    if usage != Counter({"UI_DESCRIPTION": EXPECTED_R1, "NARRATION_SYSTEM": EXPECTED_R2}):
        _fail("V303_MEMBERSHIP_FAIL", f"usage census mismatch: {dict(usage)}")
    if realization != Counter({"REBUILT_BLOCK_GROWTH": 2004, "CURRENT_BLOCK_ENVELOPE": 1175}):
        _fail("V303_MEMBERSHIP_FAIL", f"realization census mismatch: {dict(realization)}")
    if dict(by_block) != {str(k): int(v) for k, v in index["resolved_by_block"].items()}:
        _fail("V303_MEMBERSHIP_FAIL", "per-block V303 census mismatch")

    wait: set[tuple[int, int]] = set()
    for key in index.get("wait_exclusions", {}):
        if key != "total":
            wait.update(_parse_wait_expression(key))
    intersection = locators & wait
    if intersection:
        _fail("V303_MEMBERSHIP_FAIL", f"V303 membership intersects wait set: {sorted(intersection)[:4]}")

    return V303Membership(rows=tuple(rows), locators=frozenset(locators))


def load_v304_corrections(repo_root: Path) -> Mapping[tuple[int, int], V304Correction]:
    root = repo_root / V304_DIR
    index = json.loads((root / "INDEX.json").read_text(encoding="utf-8"))
    if index.get("schema") != "TAI5MSG_V303_PC_PAYLOAD_DEFECT_CORRECTION_2_V1":
        _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", "unexpected V304 schema")
    if index.get("validation_id") != "V304" or int(index.get("row_count", -1)) != 2:
        _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", "unexpected V304 identity/count")
    if index.get("source_pc_korean_tai5msg") != {"size": PC_KO_SIZE, "sha256": PC_KO_SHA256}:
        _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", "V304 source identity mismatch")

    rows_meta = index["rows"]
    payload = _read_guarded(
        root / rows_meta["path"],
        int(rows_meta["bytes"]),
        str(rows_meta["sha256"]),
        "V304_INDEX_OR_ROWS_INTEGRITY_FAIL",
    )
    rows = [json.loads(line) for line in payload.decode("utf-8").splitlines() if line]
    if len(rows) != 2:
        _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", "V304 row count mismatch")

    out: dict[tuple[int, int], V304Correction] = {}
    for row in rows:
        locator = (int(row["block"]), int(row["local"]))
        source = bytes.fromhex(row["source_message_hex"])
        target = bytes.fromhex(row["target_message_hex"])
        edit = row["edit"]
        offset = int(edit["byte_offset_zero_based"])

        if len(source) != int(row["source_message_length"]) or _sha(source) != row["source_message_sha256"]:
            _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", f"V304 source artifact mismatch at {locator}")
        if len(target) != int(row["target_message_length"]) or _sha(target) != row["target_message_sha256"]:
            _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", f"V304 target artifact mismatch at {locator}")
        if edit.get("operation") != "DELETE_EXACT_BYTE" or source[offset] != 0xFB:
            _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", f"V304 edit contract mismatch at {locator}")
        if source[offset + 1:offset + 4] != b"\x05\x05\x05":
            _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", f"V304 following terminal mismatch at {locator}")
        if source[:offset] + source[offset + 1:] != target:
            _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", f"V304 exact deletion mismatch at {locator}")
        if locator in out:
            _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", f"duplicate V304 locator {locator}")

        out[locator] = V304Correction(
            candidate_id=str(row["candidate_id"]),
            classification_id=str(row["classification_id"]),
            block=locator[0],
            local=locator[1],
            source_length=len(source),
            source_sha256=str(row["source_message_sha256"]),
            source_bytes=source,
            delete_offset=offset,
            target_length=len(target),
            target_sha256=str(row["target_message_sha256"]),
            target_bytes=target,
        )

    expected = {(19, 58), (30, 58)}
    if set(out) != expected:
        _fail("V304_INDEX_OR_ROWS_INTEGRITY_FAIL", f"unexpected V304 locator set: {sorted(out)}")
    return out


def load_v315_corrections(repo_root: Path) -> Mapping[tuple[int, int], MessageCorrection]:
    index_path = repo_root / V315_DIR / "INDEX.json"
    try:
        out = load_overlay(index_path, expected_source_identity={"size": PC_KO_SIZE, "sha256": PC_KO_SHA256})
    except (CorrectionOverlayError, OSError, ValueError, KeyError, TypeError) as exc:
        _fail("V315_INDEX_OR_ROWS_INTEGRITY_FAIL", str(exc))
    untouched = {232, 238, 249, 252, 256, 270, 279, 285, 287, 300, 307, 317, 319, 335, 341}
    expected = {(24, local) for local in range(221, 345) if local not in untouched}
    if len(out) != 109 or set(out) != expected:
        _fail("V315_INDEX_OR_ROWS_INTEGRITY_FAIL", f"unexpected V315 locator set/count: {len(out)}")
    for locator, correction in out.items():
        local = locator[1]
        ordinal = 2234 + (local - 221)
        if correction.candidate_id != f"SEL-CAND-{ordinal:06d}" or correction.classification_id != f"SEL-CLS-{ordinal:06d}":
            _fail("V315_INDEX_OR_ROWS_INTEGRITY_FAIL", f"id mismatch at {locator}")
        if correction.operation != "EXACT_REPLACE_MESSAGE":
            _fail("V315_INDEX_OR_ROWS_INTEGRITY_FAIL", f"operation mismatch at {locator}")
    return out


def _b24_layout_line_widths(message: bytes) -> tuple[int, ...]:
    if not message.endswith(b"\x05\x05\x05"):
        _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", "B24 target terminal mismatch")
    body = message[:-3]
    widths: list[int] = []
    width = 0
    pos = 0
    while pos < len(body):
        value = body[pos]
        if value == 0x0A:
            widths.append(width)
            width = 0
            pos += 1
            continue
        if value == 0x1B:
            if pos + 1 >= len(body):
                _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", "truncated B24 control")
            sub = body[pos + 1]
            if sub in (0x48, 0x6B, 0x4B):
                pos += 2
                continue
            if sub == 0x43 and pos + 2 < len(body) and body[pos + 2] in (0x30, 0x31, 0x33):
                pos += 3
                continue
            _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", f"unknown B24 control {sub:#x}")
        if _is_two_byte_lead(value):
            if pos + 1 >= len(body) or not _is_valid_trail(body[pos + 1]):
                _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", "invalid B24 two-byte glyph")
            width += 2
            pos += 2
            continue
        width += 1
        pos += 1
    widths.append(width)
    return tuple(widths)


def _b24_nonlayout_signature(message: bytes) -> bytes:
    if not message.endswith(b"\x05\x05\x05"):
        _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", "B24 source/target terminal mismatch")
    body = message[:-3]
    out = bytearray()
    pos = 0
    while pos < len(body):
        if body[pos] in (0x0A, 0x20):
            pos += 1
            continue
        if body[pos:pos + 2] == b"\x81\x40":
            pos += 2
            continue
        if body[pos] == 0x1B:
            if pos + 1 >= len(body):
                _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", "truncated B24 control")
            sub = body[pos + 1]
            size = 3 if sub == 0x43 else 2
            if pos + size > len(body):
                _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", "truncated B24 control")
            out += body[pos:pos + size]
            pos += size
            continue
        if _is_two_byte_lead(body[pos]):
            if pos + 1 >= len(body) or not _is_valid_trail(body[pos + 1]):
                _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", "invalid B24 two-byte glyph")
            out += body[pos:pos + 2]
            pos += 2
            continue
        out.append(body[pos])
        pos += 1
    return bytes(out)


def load_v320_corrections(repo_root: Path) -> Mapping[tuple[int, int], MessageCorrection]:
    index_path = repo_root / V320_DIR / "INDEX.json"
    try:
        out = load_overlay(
            index_path,
            expected_source_identity={
                "size": V315_INTERMEDIATE_SIZE,
                "sha256": V315_INTERMEDIATE_SHA256,
            },
        )
    except (CorrectionOverlayError, OSError, ValueError, KeyError, TypeError) as exc:
        _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", str(exc))

    excluded = {228, 232, 238, 249, 252, 256, 270, 279, 285, 287, 300, 307, 317, 319, 335, 341}
    expected = {(24, local) for local in range(221, 345) if local not in excluded}
    if len(out) != 108 or set(out) != expected:
        _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", f"unexpected V320 locator set/count: {len(out)}")

    for locator, correction in out.items():
        local = locator[1]
        ordinal = 2234 + (local - 221)
        if correction.candidate_id != f"SEL-CAND-{ordinal:06d}" or correction.classification_id != f"SEL-CLS-{ordinal:06d}":
            _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", f"id mismatch at {locator}")
        if correction.operation != "EXACT_REPLACE_MESSAGE":
            _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", f"operation mismatch at {locator}")
        if _b24_nonlayout_signature(correction.source_bytes) != _b24_nonlayout_signature(correction.target_bytes):
            _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", f"semantic/control drift at {locator}")
        widths = _b24_layout_line_widths(correction.target_bytes)
        if not widths or len(widths) > 12 or max(widths) > 52:
            _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", f"52-unit/12-row contract failed at {locator}: {widths}")
    return out

def _validate_selected_message(
    message: bytes,
    locator: tuple[int, int],
    mapping_codes: AbstractSet[int],
) -> tuple[Counter[int], Counter[int]]:
    if locator == (32, 242):
        if not message.endswith(b"\x05\x05\x05\x00"):
            _fail("CONTROL_TOKEN_VALIDATION_FAIL", "B32:M242 final structural terminator mismatch")
        body = message[:-4]
    else:
        if not message.endswith(b"\x05\x05\x05"):
            _fail("CONTROL_TOKEN_VALIDATION_FAIL", f"terminal mismatch at {locator}")
        body = message[:-3]

    two_byte = Counter()
    korean_added = Counter()
    pos = 0
    while pos < len(body):
        value = body[pos]

        if value == 0x02:
            _fail("CONTROL_TOKEN_VALIDATION_FAIL", f"semantic 0x02 insertion at {locator}:{pos}")

        if value == 0x1B:
            if pos + 1 >= len(body):
                _fail("CONTROL_TOKEN_VALIDATION_FAIL", f"truncated 0x1B control at {locator}:{pos}")
            sub = body[pos + 1]
            if sub in (0x48, 0x6B, 0x4B):
                pos += 2
                continue
            if sub == 0x43:
                if pos + 2 >= len(body) or body[pos + 2] not in (0x30, 0x31, 0x33):
                    _fail("CONTROL_TOKEN_VALIDATION_FAIL", f"unknown 1B43 control at {locator}:{pos}")
                pos += 3
                continue
            _fail("CONTROL_TOKEN_VALIDATION_FAIL", f"unknown 0x1B control {sub:#x} at {locator}:{pos}")

        if _is_two_byte_lead(value):
            if pos + 1 >= len(body):
                _fail("CONTROL_TOKEN_VALIDATION_FAIL", f"truncated lead {value:#x} at {locator}:{pos}")
            trail = body[pos + 1]
            if not _is_valid_trail(trail):
                _fail("CONTROL_TOKEN_VALIDATION_FAIL", f"invalid trail {trail:#x} after {value:#x} at {locator}:{pos}")
            code = (value << 8) | trail
            if code not in mapping_codes:
                _fail("MAPPING_DOMAIN_MISS", f"two-byte code {code:#06x} absent at {locator}:{pos}")
            two_byte[code] += 1
            if _is_korean_added_code(code):
                korean_added[code] += 1
            pos += 2
            continue

        if value == 0x20:
            pos += 1
            continue
        if value not in mapping_codes:
            _fail("MAPPING_DOMAIN_MISS", f"single-byte code {value:#04x} absent at {locator}:{pos}")
        pos += 1

    return two_byte, korean_added


def _messages_matrix(parsed: ParsedTai5Msg) -> list[list[bytes]]:
    return [list(block.messages) for block in parsed.blocks]


def _serialize_from_messages(
    stock: ParsedTai5Msg,
    target_messages: Sequence[Sequence[bytes]],
) -> tuple[bytes, tuple[dict, ...]]:
    if len(target_messages) != BLOCK_COUNT:
        _fail("POST_REPARSE_COUNT_FAIL", "target block count mismatch")

    header = bytearray(stock.header)
    if len(header) != HEADER_SIZE:
        _fail("STOCK_IDENTITY_MISMATCH", "stock header length mismatch")

    raw_blocks: list[bytes] = []
    metas: list[dict] = []
    file_offset = HEADER_SIZE

    for block_index, messages_like in enumerate(target_messages):
        messages = tuple(messages_like)
        stock_block = stock.blocks[block_index]
        if len(messages) != stock_block.message_count:
            _fail("POST_REPARSE_COUNT_FAIL", f"block {block_index} message count changed")

        table_end = 2 + 4 * len(messages)
        used_end = table_end + sum(map(len, messages))

        if block_index < 32:
            required = _align_up(used_end, ALIGN)
            declared = max(stock_block.declared_size, required)
            physical = declared
        else:
            declared = stock_block.declared_size
            physical = stock_block.physical_size
            if used_end > physical:
                _fail("B32_PHYSICAL_CONTRACT_FAIL", f"B32 used end {used_end:#x} > physical {physical:#x}")

        if declared > RUNTIME_BLOCK_CAPACITY:
            _fail("BLOCK_RUNTIME_CAPACITY_FAIL", f"block {block_index} declared {declared:#x}")

        offsets: list[int] = []
        cursor = table_end
        for message in messages:
            offsets.append(cursor)
            cursor += len(message)

        plain = bytearray(struct.pack("<H", len(messages)))
        for offset in offsets:
            if offset > 0xFFFFFFFF:
                _fail("POST_OFFSET_FAIL", f"block {block_index} offset does not fit u32")
            plain += struct.pack("<I", offset)
        plain += b"".join(messages)

        if len(plain) != used_end:
            _fail("POST_OFFSET_FAIL", f"block {block_index} used-end accounting mismatch")
        if len(plain) > physical:
            code = "B32_PHYSICAL_CONTRACT_FAIL" if block_index == 32 else "BLOCK_RUNTIME_CAPACITY_FAIL"
            _fail(code, f"block {block_index} plaintext exceeds physical extent")

        plain += bytes([0x5B]) * (physical - len(plain))
        raw_blocks.append(_encrypt(bytes(plain)))

        struct.pack_into("<II", header, block_index * 8, file_offset, declared)
        metas.append(
            {
                "block": block_index,
                "offset": file_offset,
                "stock_declared": stock_block.declared_size,
                "declared": declared,
                "physical": physical,
                "used_end": used_end,
                "filler": physical - used_end,
                "omitted": declared - physical,
                "growth": declared - stock_block.declared_size,
            }
        )
        file_offset += declared

    emitted = bytes(header) + b"".join(raw_blocks)
    return emitted, tuple(metas)


def _apply_v304(
    pc_ko: ParsedTai5Msg,
    corrections: Mapping[tuple[int, int], V304Correction],
) -> dict[tuple[int, int], bytes]:
    out: dict[tuple[int, int], bytes] = {}
    for locator, correction in corrections.items():
        block, local = locator
        if block >= len(pc_ko.blocks) or local >= pc_ko.blocks[block].message_count:
            _fail("LOCATOR_OUT_OF_RANGE", f"V304 locator {locator}")
        source = pc_ko.blocks[block].messages[local]
        if len(source) != correction.source_length or _sha(source) != correction.source_sha256:
            _fail("V304_SOURCE_GUARD_FAIL", f"source mismatch at {locator}")
        if source != correction.source_bytes:
            _fail("V304_SOURCE_GUARD_FAIL", f"source bytes mismatch at {locator}")
        offset = correction.delete_offset
        if source[offset] != 0xFB or source[offset + 1:offset + 4] != b"\x05\x05\x05":
            _fail("V304_SOURCE_GUARD_FAIL", f"edit bytes mismatch at {locator}")
        target = source[:offset] + source[offset + 1:]
        if len(target) != correction.target_length or _sha(target) != correction.target_sha256:
            _fail("V304_TARGET_GUARD_FAIL", f"target mismatch at {locator}")
        if target != correction.target_bytes:
            _fail("V304_TARGET_GUARD_FAIL", f"target bytes mismatch at {locator}")
        out[locator] = target
    return out


def _apply_v315(
    pc_ko: ParsedTai5Msg,
    corrections: Mapping[tuple[int, int], MessageCorrection],
) -> dict[tuple[int, int], bytes]:
    out: dict[tuple[int, int], bytes] = {}
    for locator, correction in corrections.items():
        block, local = locator
        if block >= len(pc_ko.blocks) or local >= pc_ko.blocks[block].message_count:
            _fail("LOCATOR_OUT_OF_RANGE", f"V315 locator {locator}")
        try:
            out[locator] = apply_correction(pc_ko.blocks[block].messages[local], correction)
        except CorrectionOverlayError as exc:
            _fail("V315_SOURCE_GUARD_FAIL", f"{locator}: {exc}")
    return out


def _apply_v320(
    v315_corrected: Mapping[tuple[int, int], bytes],
    corrections: Mapping[tuple[int, int], MessageCorrection],
) -> dict[tuple[int, int], bytes]:
    out: dict[tuple[int, int], bytes] = {}
    for locator, correction in corrections.items():
        source = v315_corrected.get(locator)
        if source is None:
            _fail("V320_SOURCE_GUARD_FAIL", f"missing V315 intermediate source at {locator}")
        try:
            out[locator] = apply_correction(source, correction)
        except CorrectionOverlayError as exc:
            _fail("V320_SOURCE_GUARD_FAIL", f"{locator}: {exc}")
    return out

def _validate_current_postconditions(
    stock_blob: bytes,
    emitted: bytes,
    metas: Sequence[Mapping[str, int]],
) -> None:
    growth = len(emitted) - len(stock_blob)
    if growth != EXPECTED_GROWTH:
        _fail("OUTPUT_GROWTH_POSTCONDITION_FAIL", f"{growth:#x} != {EXPECTED_GROWTH:#x}")
    if len(emitted) != EXPECTED_FINAL_SIZE:
        _fail("OUTPUT_SIZE_POSTCONDITION_FAIL", f"{len(emitted):#x} != {EXPECTED_FINAL_SIZE:#x}")

    b32 = metas[32]
    checks = {
        "offset": EXPECTED_B32_OFFSET,
        "used_end": EXPECTED_B32_USED_END,
        "declared": EXPECTED_B32_DECLARED,
        "physical": EXPECTED_B32_PHYSICAL,
        "omitted": EXPECTED_B32_OMITTED,
    }
    for key, expected in checks.items():
        actual = int(b32[key])
        if actual != expected:
            _fail("B32_PHYSICAL_CONTRACT_FAIL", f"B32 {key} {actual:#x} != {expected:#x}")
    if max(int(meta["declared"]) for meta in metas) != EXPECTED_LARGEST_DECLARED:
        _fail("BLOCK_RUNTIME_CAPACITY_FAIL", "largest rebuilt block postcondition mismatch")


def metadata_preflight(repo_root: Path) -> MetadataPreflightReport:
    membership = load_v303_membership(repo_root)
    corrections = load_v304_corrections(repo_root)
    b24_corrections = load_v315_corrections(repo_root)
    native_wrap_corrections = load_v320_corrections(repo_root)
    if set(corrections) & set(b24_corrections):
        _fail("V315_INDEX_OR_ROWS_INTEGRITY_FAIL", "V304/V315 correction overlap")
    if set(native_wrap_corrections) != set(b24_corrections) - {(24, 228)}:
        _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", "V320 must equal V315 layout population exactly")

    root = repo_root / STRUCTURE_DIR
    index = json.loads((root / "INDEX.json").read_text(encoding="utf-8"))

    blocks_meta = index["block_descriptors"]
    blocks_raw = _read_guarded(
        repo_root / blocks_meta["path"],
        int(blocks_meta["bytes"]),
        str(blocks_meta["sha256"]),
        "V303_INDEX_OR_SHARD_INTEGRITY_FAIL",
    )
    descriptors = [json.loads(line) for line in blocks_raw.decode("utf-8").splitlines() if line]
    if len(descriptors) != BLOCK_COUNT:
        _fail("POST_REPARSE_COUNT_FAIL", "structure block-descriptor count mismatch")

    lengths_by_block: dict[int, dict] = {}
    for meta in index["message_shards"]["ordered_shards"]:
        raw = _read_guarded(
            repo_root / meta["path"],
            int(meta["bytes"]),
            str(meta["sha256"]),
            "V303_INDEX_OR_SHARD_INTEGRITY_FAIL",
        )
        obj = json.loads(raw.decode("utf-8"))
        block_index = int(obj["block_index"])
        if int(obj["message_count"]) != int(meta["message_count"]):
            _fail("POST_REPARSE_COUNT_FAIL", f"structure message-count mismatch B{block_index}")
        lengths_by_block[block_index] = obj

    if len(lengths_by_block) != BLOCK_COUNT:
        _fail("POST_REPARSE_COUNT_FAIL", "structure message-shard count mismatch")

    correction_delta = {
        locator: correction.target_length - correction.source_length
        for locator, correction in corrections.items()
    }
    correction_delta.update({
        locator: len(correction.target_bytes) - len(correction.source_bytes)
        for locator, correction in b24_corrections.items()
    })
    correction_delta.update({
        locator: len(correction.target_bytes) - len(correction.source_bytes)
        for locator, correction in native_wrap_corrections.items()
    })

    metas: list[dict] = []
    file_offset = HEADER_SIZE
    selected_seen = 0

    for block_index in range(BLOCK_COUNT):
        lengths = lengths_by_block[block_index]
        descriptor = descriptors[block_index]
        original_lengths = lengths["original_lengths"]
        korean_lengths = lengths["korean_lengths"]
        if len(original_lengths) != int(lengths["message_count"]) or len(korean_lengths) != len(original_lengths):
            _fail("POST_REPARSE_COUNT_FAIL", f"length lattice mismatch B{block_index}")

        total = 0
        for local in range(len(original_lengths)):
            locator = (block_index, local)
            if locator in membership.locators:
                length = int(korean_lengths[local])
                selected_seen += 1
            else:
                length = int(original_lengths[local])
            length += correction_delta.get(locator, 0)
            total += length

        used_end = int(lengths["table_end"]) + total
        stock_declared = int(descriptor["original"]["declared_size"])
        stock_physical = int(descriptor["original"]["physical_size"])

        if block_index < 32:
            declared = max(stock_declared, _align_up(used_end, ALIGN))
            physical = declared
        else:
            declared = stock_declared
            physical = stock_physical
            if used_end > physical:
                _fail("B32_PHYSICAL_CONTRACT_FAIL", "metadata B32 used end exceeds physical extent")

        if declared > RUNTIME_BLOCK_CAPACITY:
            _fail("BLOCK_RUNTIME_CAPACITY_FAIL", f"metadata block {block_index} exceeds runtime capacity")

        metas.append(
            {
                "block": block_index,
                "offset": file_offset,
                "stock_declared": stock_declared,
                "declared": declared,
                "physical": physical,
                "used_end": used_end,
                "filler": physical - used_end,
                "omitted": declared - physical,
                "growth": declared - stock_declared,
            }
        )
        file_offset += declared

    if selected_seen != EXPECTED_SELECTED:
        _fail("V303_MEMBERSHIP_FAIL", f"metadata selected count {selected_seen}")

    b32 = metas[32]
    final_size = int(b32["offset"]) + int(b32["physical"])
    growth = sum(int(meta["growth"]) for meta in metas)
    growth_blocks = tuple((int(meta["block"]), int(meta["growth"])) for meta in metas if int(meta["growth"]))
    report = MetadataPreflightReport(
        selected_rows=selected_seen,
        growth=growth,
        final_size=final_size,
        b32_offset=int(b32["offset"]),
        b32_used_end=int(b32["used_end"]),
        b32_declared=int(b32["declared"]),
        b32_physical=int(b32["physical"]),
        b32_filler=int(b32["filler"]),
        b32_omitted=int(b32["omitted"]),
        largest_declared=max(int(meta["declared"]) for meta in metas),
        growth_blocks=growth_blocks,
    )

    expected_growth_blocks = (
        (17, 0x340),
        (19, 0xA80),
        (20, 0x6C0),
        (21, 0x1C0),
        (22, 0x4340),
        (23, 0xFC0),
        (24, 0x780),
    )
    expected = {
        "selected_rows": EXPECTED_SELECTED,
        "growth": EXPECTED_GROWTH,
        "final_size": EXPECTED_FINAL_SIZE,
        "b32_offset": EXPECTED_B32_OFFSET,
        "b32_used_end": EXPECTED_B32_USED_END,
        "b32_declared": EXPECTED_B32_DECLARED,
        "b32_physical": EXPECTED_B32_PHYSICAL,
        "b32_filler": EXPECTED_B32_PHYSICAL - EXPECTED_B32_USED_END,
        "b32_omitted": EXPECTED_B32_OMITTED,
        "largest_declared": EXPECTED_LARGEST_DECLARED,
    }
    for key, value in expected.items():
        if getattr(report, key) != value:
            _fail("OUTPUT_SIZE_POSTCONDITION_FAIL", f"metadata {key} mismatch")
    if report.growth_blocks != expected_growth_blocks:
        _fail("OUTPUT_GROWTH_POSTCONDITION_FAIL", f"metadata growth blocks {report.growth_blocks}")

    return report


def reconstruct_selective_tai5msg(
    stock_blob: bytes,
    pc_ko_blob: bytes,
    repo_root: Path,
    mapping_codes: AbstractSet[int],
    *,
    require_diagnostic_sha: bool = True,
) -> tuple[bytes, SelectiveSerializationReport]:
    if len(stock_blob) != STOCK_SIZE or _sha(stock_blob) != STOCK_SHA256:
        _fail("STOCK_IDENTITY_MISMATCH", "canonical stock TAI5MSG required")
    if len(pc_ko_blob) != PC_KO_SIZE or _sha(pc_ko_blob) != PC_KO_SHA256:
        _fail("PC_KO_IDENTITY_MISMATCH", "canonical PC-KO TAI5MSG required")

    membership = load_v303_membership(repo_root)
    corrections = load_v304_corrections(repo_root)
    b24_corrections = load_v315_corrections(repo_root)
    native_wrap_corrections = load_v320_corrections(repo_root)
    if set(corrections) & set(b24_corrections):
        _fail("V315_INDEX_OR_ROWS_INTEGRITY_FAIL", "V304/V315 correction overlap")
    if set(native_wrap_corrections) != set(b24_corrections) - {(24, 228)}:
        _fail("V320_INDEX_OR_ROWS_INTEGRITY_FAIL", "V320 must equal V315 layout population exactly")

    stock = parse_tai5msg(stock_blob)
    pc_ko = parse_tai5msg(pc_ko_blob)
    if [b.message_count for b in stock.blocks] != [b.message_count for b in pc_ko.blocks]:
        _fail("POST_REPARSE_COUNT_FAIL", "stock/PC-KO per-block message counts differ")

    zero_messages = _messages_matrix(stock)
    zero_rebuilt, _zero_meta = _serialize_from_messages(stock, zero_messages)
    if zero_rebuilt != stock_blob:
        _fail("STOCK_IDENTITY_MISMATCH", "zero-replacement identity rebuild is not byte-identical")

    corrected = _apply_v304(pc_ko, corrections)
    v315_corrected = _apply_v315(pc_ko, b24_corrections)
    corrected.update(v315_corrected)
    corrected.update(_apply_v320(v315_corrected, native_wrap_corrections))
    targets = _messages_matrix(stock)
    two_byte = Counter()
    korean_added = Counter()

    for row in membership.rows:
        locator = (int(row["block"]), int(row["local"]))
        block, local = locator
        if block >= BLOCK_COUNT or local >= len(targets[block]):
            _fail("LOCATOR_OUT_OF_RANGE", f"V303 locator {locator}")
        payload = corrected.get(locator, pc_ko.blocks[block].messages[local])
        targets[block][local] = payload
        tb, ka = _validate_selected_message(payload, locator, mapping_codes)
        two_byte.update(tb)
        korean_added.update(ka)

    if len(two_byte) != EXPECTED_UNIQUE_TWO_BYTE_CODES or sum(two_byte.values()) != EXPECTED_TWO_BYTE_OCCURRENCES:
        _fail("MAPPING_DOMAIN_MISS", "effective two-byte code census differs from V306")
    if len(korean_added) != EXPECTED_UNIQUE_KOREAN_ADDED_CODES or sum(korean_added.values()) != EXPECTED_KOREAN_ADDED_OCCURRENCES:
        _fail("MAPPING_DOMAIN_MISS", "effective Korean-added code census differs from V306")

    emitted, metas = _serialize_from_messages(stock, targets)
    _validate_current_postconditions(stock_blob, emitted, metas)

    post = parse_tai5msg(emitted)
    selected_matches = 0
    unselected_matches = 0
    for block_index in range(BLOCK_COUNT):
        for local, message in enumerate(post.blocks[block_index].messages):
            locator = (block_index, local)
            if locator in membership.locators:
                if message != targets[block_index][local]:
                    _fail("POST_SELECTED_PAYLOAD_FAIL", f"selected mismatch at {locator}")
                selected_matches += 1
            else:
                if message != stock.blocks[block_index].messages[local]:
                    _fail("POST_UNSELECTED_JP_MUTATION", f"unselected mutation at {locator}")
                unselected_matches += 1

    if selected_matches != EXPECTED_SELECTED or unselected_matches != EXPECTED_UNSELECTED:
        _fail("POST_REPARSE_COUNT_FAIL", "selected/unselected post-reparse census mismatch")

    output_sha = _sha(emitted)
    diagnostic_match = output_sha == EXPECTED_DIAGNOSTIC_SHA256
    if require_diagnostic_sha and not diagnostic_match:
        _fail(
            "OUTPUT_DIAGNOSTIC_SHA_POSTCONDITION_FAIL",
            f"{output_sha} != {EXPECTED_DIAGNOSTIC_SHA256}",
        )

    b32 = metas[32]
    report = SelectiveSerializationReport(
        input_stock_sha256=STOCK_SHA256,
        input_pc_ko_sha256=PC_KO_SHA256,
        output_sha256=output_sha,
        block_count=BLOCK_COUNT,
        message_count=MESSAGE_COUNT,
        selected_rows=selected_matches,
        unselected_rows=unselected_matches,
        growth=len(emitted) - len(stock_blob),
        final_size=len(emitted),
        b32_offset=int(b32["offset"]),
        b32_used_end=int(b32["used_end"]),
        b32_declared=int(b32["declared"]),
        b32_physical=int(b32["physical"]),
        b32_filler=int(b32["filler"]),
        b32_omitted=int(b32["omitted"]),
        largest_declared=max(int(meta["declared"]) for meta in metas),
        unique_two_byte_codes=len(two_byte),
        two_byte_occurrences=sum(two_byte.values()),
        unique_korean_added_codes=len(korean_added),
        korean_added_occurrences=sum(korean_added.values()),
        diagnostic_sha_match=diagnostic_match,
    )
    return emitted, report


def mapping_code_set(entries: Iterable[tuple[int, int]]) -> frozenset[int]:
    return frozenset(int(game_code) for game_code, _unicode_value in entries)
