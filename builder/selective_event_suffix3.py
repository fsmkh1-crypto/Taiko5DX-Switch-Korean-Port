from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Sequence

from builder.selective_event import ParsedEventTs5, SelectiveEventError

CANONICAL_PC_KO_SIZE = 1_156_480
CANONICAL_PC_KO_SHA256 = "0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe"
CANONICAL_V352_SIZE = 1_109_356
CANONICAL_V352_SHA256 = "e61569508ffc9995f78df51f01b42be5402b79d5e26a8c8f3e71c0448d8eaaeb"
REQUIRED_V357_TAI5MSG_SHA256 = "ad91776d47c3170573bed063dd6677716833e3a138be27474373ef5d2782e794"
APPLICABILITY_ROWS = 3
APPLICABILITY_SHA256 = "f92b9e8f2ad7ff5c904cbbbd3ca1932f70a85050ed93591ff718f597cd777b5b"
TOTAL_GROWTH = 84
EXPECTED_TRANSFORMED_CORPUS_SHA256 = "8ab2e7701676348e1434674135a97fa3140f8c17276ca7f88489155060e40bfe"
EXPECTED_ROW_IDS = (4743, 5059, 11440)
EXPECTED_ROOTS = {4743: 349, 5059: 209, 11440: 395}
EXPECTED_ROOT_TARGET_SHA256 = {
    209: "05e3c0397482ce98b34f89de3e67cc32e1e070e05801ff72b2790ebcbf441267",
    349: "706bfadf482b6848c058e242994288529380ad5b1113282987bde80987e4d98e",
    395: "ad90e66db5e87b245a5ee6ad03243f7b6f4edac6dde2a33a59564f77e049c545",
}
EXPECTED_MACROS = {4743: "\\%21", 5059: "\\%15", 11440: "\\%2A"}


@dataclass(frozen=True)
class Suffix3ApplicabilityRecord:
    row_id: int
    partition: int
    original_offset: int
    ko_offset: int
    opcode: int
    original_command_length: int
    ko_command_length: int
    macro: str
    tai5msg_block: int
    tai5msg_local: int
    original_sha256: str
    ko_sha256: str
    tai5msg_target_sha256: str
    growth: int


@dataclass(frozen=True)
class Suffix3OverlayReport:
    rows: int
    original_bytes: int
    target_bytes: int
    payload_growth: int
    opcode_counts: dict[int, int]
    row_ids: tuple[int, ...]
    tai5msg_roots: tuple[int, ...]
    transformed_corpus_sha256: str

    def to_dict(self) -> dict:
        return asdict(self)


def _fail(code: str, detail: str) -> None:
    raise SelectiveEventError(code, detail)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _int(obj: dict, name: str) -> int:
    value = obj.get(name)
    if not isinstance(value, int) or isinstance(value, bool):
        _fail("SUFFIX3_FIELD_FAIL", f"{name}={value!r}")
    return value


def load_suffix3_applicability(blob: bytes, *, require_canonical: bool = True) -> tuple[Suffix3ApplicabilityRecord, ...]:
    if require_canonical and _sha256(blob) != APPLICABILITY_SHA256:
        _fail("SUFFIX3_APPLICABILITY_SHA_FAIL", _sha256(blob))
    try:
        text = blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        _fail("SUFFIX3_APPLICABILITY_UTF8_FAIL", str(exc))

    rows: list[Suffix3ApplicabilityRecord] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            _fail("SUFFIX3_APPLICABILITY_JSON_FAIL", f"line={line_no} {exc}")
        rec = Suffix3ApplicabilityRecord(
            row_id=_int(obj, "row_id"),
            partition=_int(obj, "partition"),
            original_offset=_int(obj, "original_offset"),
            ko_offset=_int(obj, "ko_offset"),
            opcode=_int(obj, "opcode"),
            original_command_length=_int(obj, "original_command_length"),
            ko_command_length=_int(obj, "ko_command_length"),
            macro=str(obj.get("macro")),
            tai5msg_block=_int(obj, "tai5msg_block"),
            tai5msg_local=_int(obj, "tai5msg_local"),
            original_sha256=str(obj.get("original_sha256")),
            ko_sha256=str(obj.get("ko_sha256")),
            tai5msg_target_sha256=str(obj.get("tai5msg_target_sha256")),
            growth=_int(obj, "growth"),
        )
        if rec.opcode != 0x11:
            _fail("SUFFIX3_OPCODE_FAIL", f"row={rec.row_id} opcode={rec.opcode:#x}")
        if rec.tai5msg_block != 0:
            _fail("SUFFIX3_TAI5MSG_BLOCK_FAIL", f"row={rec.row_id} block={rec.tai5msg_block}")
        if rec.original_command_length <= 0 or rec.ko_command_length <= 0:
            _fail("SUFFIX3_LENGTH_FAIL", f"row={rec.row_id}")
        if rec.original_command_length % 4 or rec.ko_command_length % 4:
            _fail("SUFFIX3_ALIGNMENT_FAIL", f"row={rec.row_id}")
        if rec.growth != rec.ko_command_length - rec.original_command_length:
            _fail("SUFFIX3_GROWTH_FAIL", f"row={rec.row_id}")
        if len(rec.original_sha256) != 64 or len(rec.ko_sha256) != 64 or len(rec.tai5msg_target_sha256) != 64:
            _fail("SUFFIX3_HASH_FIELD_FAIL", f"row={rec.row_id}")
        if not rec.macro.startswith("\\%") or len(rec.macro) != 4:
            _fail("SUFFIX3_MACRO_FAIL", f"row={rec.row_id} macro={rec.macro!r}")
        rows.append(rec)

    if len({r.row_id for r in rows}) != len(rows):
        _fail("SUFFIX3_ROW_COLLISION", "duplicate row_id")
    if len({(r.partition, r.original_offset) for r in rows}) != len(rows):
        _fail("SUFFIX3_ORIGINAL_COLLISION", "duplicate original binding")
    if len({r.ko_offset for r in rows}) != len(rows):
        _fail("SUFFIX3_KO_COLLISION", "duplicate KO binding")

    if require_canonical:
        if len(rows) != APPLICABILITY_ROWS:
            _fail("SUFFIX3_COUNT_FAIL", str(len(rows)))
        if tuple(r.row_id for r in rows) != EXPECTED_ROW_IDS:
            _fail("SUFFIX3_ROW_IDS_FAIL", repr(tuple(r.row_id for r in rows)))
        if sum(r.growth for r in rows) != TOTAL_GROWTH:
            _fail("SUFFIX3_TOTAL_GROWTH_FAIL", str(sum(r.growth for r in rows)))
        for r in rows:
            if r.tai5msg_local != EXPECTED_ROOTS[r.row_id]:
                _fail("SUFFIX3_ROOT_BINDING_FAIL", f"row={r.row_id} root={r.tai5msg_local}")
            if r.tai5msg_target_sha256 != EXPECTED_ROOT_TARGET_SHA256[r.tai5msg_local]:
                _fail("SUFFIX3_ROOT_TARGET_HASH_FAIL", f"row={r.row_id}")
            if r.macro != EXPECTED_MACROS[r.row_id]:
                _fail("SUFFIX3_MACRO_BINDING_FAIL", f"row={r.row_id} macro={r.macro!r}")
    return tuple(rows)


def _index_original(parsed: ParsedEventTs5) -> dict[tuple[int, int], tuple[int, bytes]]:
    result: dict[tuple[int, int], tuple[int, bytes]] = {}
    for partition in parsed.partitions:
        for item_index, item in enumerate(partition.grouped_items):
            result[(partition.index, item.start)] = (item_index, item.data)
    return result


def apply_suffix3_rows(
    original: ParsedEventTs5,
    korean_blob: bytes,
    current_item_bytes: Sequence[Sequence[bytes]],
    applicability: Sequence[Suffix3ApplicabilityRecord],
    *,
    require_canonical: bool = True,
) -> tuple[tuple[tuple[bytes, ...], ...], Suffix3OverlayReport]:
    if len(current_item_bytes) != len(original.partitions):
        _fail("SUFFIX3_PARTITION_COUNT_FAIL", f"current={len(current_item_bytes)} original={len(original.partitions)}")
    if require_canonical:
        if len(korean_blob) != CANONICAL_PC_KO_SIZE:
            _fail("SUFFIX3_KO_FILE_SIZE_FAIL", str(len(korean_blob)))
        if _sha256(korean_blob) != CANNICAL_PC_KO_SHA256:
            _fail("SUFFIX3_KO_FILE_SHA_FAIL", _sha256(korean_blob))

    original_index = _index_original(original)
    current = [list(map(bytes, part)) for part in current_item_bytes]
    h = hashlib.sha256()
    opcounts: Counter[int] = Counter()
    orig_total = target_total = 0

    for row in applicability:
        binding = original_index.get((row.partition, row.original_offset))
        if binding is None:
            _fail("SUFFIX3_ORIGINAL_BINDING_MISSING", f"row={row.row_id}")
        item_index, original_item = binding
        if item_index >= len(current[row.partition]):
            _fail("SUFFIX3_CURRENT_ITEM_RANGE_FAIL", f"row={row.row_id}")
        if len(original_item) != row.original_command_length or not original_item or original_item[0] != row.opcode:
            _fail("SUFFIX3_ORIGINAL_BINDING_FAIL", f"row={row.row_id}")
        if _sha256(original_item) != row.original_sha256:
            _fail("SUFFIX3_ORIGINAL_HASH_FAIL", f"row={row.row_id}")
        if current[row.partition][item_index] != original_item:
            _fail("SUFFIX3_BASELINE_FAIL", f"row={row.row_id} offset={row.original_offset:#x}")

        end = row.ko_offset + row.ko_command_length
        if row.ko_offset < 0 or end > len(korean_blob):
            _fail("SUFFIX3_KO_BINDING_RANGE_FAIL", f"row={row.row_id}")
        target = korean_blob[row.ko_offset:end]
        if len(target) != row.ko_command_length or not target or target[0] != row.opcode:
            _fail("SUFFIX3_KO_BINDING_FAIL", f"row={row.row_id}")
        if _sha256(target) != row.ko_sha256:
            _fail("SUFFIX3_KO_HASH_FAIL", f"row={row.row_id}")
        if target.count(row.macro.encode("ascii")) != 1:
            _fail("SUFFIX3_MACRO_OCCURRENCE_FAIL", f"row={row.row_id}")

        current[row.partition][item_index] = target
        orig_total += len(original_item)
        target_total += len(target)
        opcounts[row.opcode] += 1
        h.update(row.row_id.to_bytes(4, "little"))
        h.update(row.original_offset.to_bytes(4, "little"))
        h.update(row.ko_offset.to_bytes(4, "little"))
        h.update(hashlib.sha256(target).digest())

    report = Suffix3OverlayReport(
        rows=len(applicability),
        original_bytes=orig_total,
        target_bytes=target_total,
        payload_growth=target_total - orig_total,
        opcode_counts=dict(sorted(opcounts.items())),
        row_ids=tuple(r.row_id for r in applicability),
        tai5msg_roots=tuple(r.tai5msg_local for r in applicability),
        transformed_corpus_sha256=h.hexdigest(),
    )
    if require_canonical:
        if report.rows != APPLICABILITY_ROWS:
            _fail("SUFFIX3_REPORT_COUNT_FAIL", str(report.rows))
        if report.original_bytes != 184 or report.target_bytes != 268 or report.payload_growth != TOTAL_GROWTH:
            _fail("SUFFIX3_REPORT_BYTES_FAIL", repr(report.to_dict()))
        if report.opcode_counts != {0x11: 3}:
            _fail("SUFFIX3_REPORT_OPCODE_FAIL", repr(report.opcode_counts))
        if report.row_ids != EXPECTED_ROW_IDS:
            _fail("SUFFIX3_REPORT_ROW_IDS_FAIL", repr(report.row_ids))
        if report.tai5msg_roots != (349, 209, 395):
            _fail("SUFFIX3_REPORT_ROOTS_FAIL", repr(report.tai5msg_roots))
        if report.transformed_corpus_sha256 != EXPECTED_TRANSFORMED_CORPUS_SHA256:
            _fail("SUFFIX3_REPORT_CORPUS_HASH_FAIL", report.transformed_corpus_sha256)
    return tuple(tuple(part) for part in current), report
