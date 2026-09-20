from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import struct
from typing import Sequence

from builder.selective_event import ParsedEventTs5, SelectiveEventError, STOCK_SHA256, STOCK_SIZE, rebuild_event_ts5

PC_KO_SIZE = 1_156_480
PC_KO_SHA256 = "0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe"
ONEE_LEDGER_RECORD = struct.Struct("<HHIIHHBB")
ONEE_LEDGER_RECORD_COUNT = 461
ONEE_LEDGER_SHA256 = "4e84b8278e1fe6b13a7945c6ba13a5b2922cb686b79746a510c92fd2ce856b35"
ONEE_ALL_ROWSET_SHA256 = "50f296c1fa044020d48024c52b41f9409e06c453d24dff5d7a8c3257f01b1046"
ONEE_READY_ROWSET_SHA256 = "0011c816ae8519750c79b3a1917b830decce3b7f466fe6735212f433859fc38d"
ONEE_PENDING_ROWSET_SHA256 = "42d87f675644aeaf995e9a3beac217acdb21164b10b3e3d2461feeec9f4566cd"

PRESERVE_IDENTICAL = 0
KEEP_JP_IDENTITY = 1
INCLUDE_KO_READY = 2
INCLUDE_KO_RUNTIME_PENDING = 3

EXPECTED_DISPOSITIONS = {
    PRESERVE_IDENTICAL: 73,
    KEEP_JP_IDENTITY: 344,
    INCLUDE_KO_READY: 23,
    INCLUDE_KO_RUNTIME_PENDING: 21,
}
EXPECTED_READY_PARTITIONS = (0, 11, 72, 161, 681)
EXPECTED_READY_GROWTH = 8
EXPECTED_READY_SAME_LENGTH = 21
EXPECTED_READY_PLUS4 = 2


@dataclass(frozen=True)
class OneELedgerRecord:
    partition: int
    ordinal: int
    original_offset: int
    ko_offset: int
    original_length: int
    ko_length: int
    disposition: int
    subtype: int


@dataclass(frozen=True)
class OneEApplicationReport:
    ledger_rows: int
    ready_rows: int
    keep_jp_identity_rows: int
    preserve_identical_rows: int
    runtime_pending_rows: int
    same_length_ready_rows: int
    plus4_ready_rows: int
    growth_bytes: int
    ready_partitions: tuple[int, ...]
    unauthorized_preexisting_onee_mutations: int
    rowset_sha256: str

    def to_dict(self) -> dict:
        return asdict(self)


def _fail(code: str, detail: str) -> None:
    raise SelectiveEventError(code, detail)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _rowset_hash(rows: Sequence[OneELedgerRecord]) -> str:
    raw = b"".join(
        struct.pack("<HHII", row.partition, row.ordinal, row.original_offset, row.ko_offset)
        for row in sorted(rows, key=lambda row: (row.partition, row.ordinal, row.original_offset, row.ko_offset))
    )
    return _sha256(raw)


def load_onee_ledger(blob: bytes, *, require_canonical: bool = True) -> tuple[OneELedgerRecord, ...]:
    if len(blob) % ONEE_LEDGER_RECORD.size:
        _fail("ONEE_LEDGER_SIZE_FAIL", f"bytes={len(blob)}")
    if require_canonical:
        if len(blob) != ONEE_LEDGER_RECORD_COUNT * ONEE_LEDGER_RECORD.size:
            _fail("ONEE_LEDGER_COUNT_FAIL", f"bytes={len(blob)}")
        actual = _sha256(blob)
        if actual != ONEE_LEDGER_SHA256:
            _fail("ONEE_LEDGER_SHA_FAIL", actual)

    rows = tuple(OneELedgerRecord(*values) for values in ONEE_LEDGER_RECORD.iter_unpack(blob))
    if len({row.original_offset for row in rows}) != len(rows):
        _fail("ONEE_LEDGER_ORIGINAL_COLLISION", "duplicate original offset")
    if len({row.ko_offset for row in rows}) != len(rows):
        _fail("ONEE_LEDGER_KO_COLLISION", "duplicate KO offset")
    if any(row.disposition not in EXPECTED_DISPOSITIONS for row in rows):
        _fail("ONEE_LEDGER_DISPOSITION_FAIL", "unknown disposition")

    if require_canonical:
        counts = Counter(row.disposition for row in rows)
        if dict(counts) != EXPECTED_DISPOSITIONS:
            _fail("ONEE_LEDGER_DISPOSITION_COUNT_FAIL", repr(dict(counts)))
        if _rowset_hash(rows) != ONEE_ALL_ROWSET_SHA256:
            _fail("ONEE_LEDGER_ROWSET_FAIL", _rowset_hash(rows))
        ready = tuple(row for row in rows if row.disposition == INCLUDE_KO_READY)
        pending = tuple(row for row in rows if row.disposition == INCLUDE_KO_RUNTIME_PENDING)
        if _rowset_hash(ready) != ONEE_READY_ROWSET_SHA256:
            _fail("ONEE_READY_ROWSET_FAIL", _rowset_hash(ready))
        if _rowset_hash(pending) != ONEE_PENDING_ROWSET_SHA256:
            _fail("ONEE_PENDING_ROWSET_FAIL", _rowset_hash(pending))
    return rows


def _find_exact_onee(items, offset: int, expected_length: int) -> int:
    for index, item in enumerate(items):
        if item.start == offset:
            if item.opcode != 0x1E:
                _fail("ONEE_ITEM_OPCODE_FAIL", f"offset={offset:#x} opcode={item.opcode:#x}")
            if len(item.data) != expected_length:
                _fail("ONEE_ITEM_LENGTH_FAIL", f"offset={offset:#x} len={len(item.data)} expected={expected_length}")
            return index
    _fail("ONEE_ITEM_NOT_FOUND", f"offset={offset:#x}")


def apply_onee_ready(
    original: ParsedEventTs5,
    pc_ko: ParsedEventTs5,
    current_item_bytes: Sequence[Sequence[bytes]],
    ledger: Sequence[OneELedgerRecord],
    *,
    require_canonical: bool = True,
) -> tuple[tuple[tuple[bytes, ...], ...], OneEApplicationReport]:
    if len(original.partitions) != len(pc_ko.partitions) or len(current_item_bytes) != len(original.partitions):
        _fail("ONEE_PARTITION_COUNT_FAIL", "partition count mismatch")

    if require_canonical:
        original_blob = rebuild_event_ts5(original)
        ko_blob = rebuild_event_ts5(pc_ko)
        if len(original_blob) != STOCK_SIZE or _sha256(original_blob) != STOCK_SHA256:
            _fail("ONEE_ORIGINAL_IDENTITY_FAIL", f"size={len(original_blob)} sha256={_sha256(original_blob)}")
        if len(ko_blob) != PC_KO_SIZE or _sha256(ko_blob) != PC_KO_SHA256:
            _fail("ONEE_PC_KO_IDENTITY_FAIL", f"size={len(ko_blob)} sha256={_sha256(ko_blob)}")

    current = [list(map(bytes, part)) for part in current_item_bytes]
    ready = []
    unauthorized = []

    for row in ledger:
        if row.partition >= len(original.partitions):
            _fail("ONEE_LEDGER_PARTITION_FAIL", str(row.partition))
        opart = original.partitions[row.partition]
        kpart = pc_ko.partitions[row.partition]
        if len(current[row.partition]) != len(opart.grouped_items):
            _fail("ONEE_CURRENT_ITEM_COUNT_FAIL", f"partition={row.partition}")

        oidx = _find_exact_onee(opart.grouped_items, row.original_offset, row.original_length)
        kidx = _find_exact_onee(kpart.grouped_items, row.ko_offset, row.ko_length)
        oordinal = sum(item.opcode == 0x1E for item in opart.grouped_items[:oidx])
        kordinal = sum(item.opcode == 0x1E for item in kpart.grouped_items[:kidx])
        if oordinal != row.ordinal or kordinal != row.ordinal:
            _fail(
                "ONEE_LEDGER_ORDINAL_FAIL",
                f"partition={row.partition} expected={row.ordinal} original={oordinal} ko={kordinal}",
            )

        oitem = opart.grouped_items[oidx]
        kitem = kpart.grouped_items[kidx]
        if oitem.data[:4] != kitem.data[:4]:
            _fail("ONEE_HEADER_MISMATCH", f"original={row.original_offset:#x} ko={row.ko_offset:#x}")

        if current[row.partition][oidx] != oitem.data:
            unauthorized.append((row.partition, row.original_offset, row.disposition))
            continue

        if row.disposition == INCLUDE_KO_READY:
            if kitem.data == oitem.data:
                _fail("ONEE_READY_PAYLOAD_IDENTICAL", f"offset={row.original_offset:#x}")
            if len(kitem.data) % 4:
                _fail("ONEE_READY_ALIGNMENT_FAIL", f"offset={row.original_offset:#x} len={len(kitem.data)}")
            current[row.partition][oidx] = kitem.data
            ready.append(row)

    if unauthorized:
        _fail("ONEE_UNAUTHORIZED_PREEXISTING_MUTATION", repr(unauthorized[:20]))

    same_length = sum(row.ko_length == row.original_length for row in ready)
    plus4 = sum(row.ko_length - row.original_length == 4 for row in ready)
    growth = sum(row.ko_length - row.original_length for row in ready)
    partitions = tuple(sorted({row.partition for row in ready}))
    report = OneEApplicationReport(
        ledger_rows=len(ledger),
        ready_rows=len(ready),
        keep_jp_identity_rows=sum(row.disposition == KEEP_JP_IDENTITY for row in ledger),
        preserve_identical_rows=sum(row.disposition == PRESERVE_IDENTICAL for row in ledger),
        runtime_pending_rows=sum(row.disposition == INCLUDE_KO_RUNTIME_PENDING for row in ledger),
        same_length_ready_rows=same_length,
        plus4_ready_rows=plus4,
        growth_bytes=growth,
        ready_partitions=partitions,
        unauthorized_preexisting_onee_mutations=0,
        rowset_sha256=_rowset_hash(tuple(ready)),
    )

    if require_canonical:
        expected = {
            "ledger_rows": 461,
            "ready_rows": 23,
            "keep_jp_identity_rows": 344,
            "preserve_identical_rows": 73,
            "runtime_pending_rows": 21,
            "same_length_ready_rows": EXPECTED_READY_SAME_LENGTH,
            "plus4_ready_rows": EXPECTED_READY_PLUS4,
            "growth_bytes": EXPECTED_READY_GROWTH,
            "ready_partitions": EXPECTED_READY_PARTITIONS,
            "rowset_sha256": ONEE_READY_ROWSET_SHA256,
        }
        for field, value in expected.items():
            actual = getattr(report, field)
            if actual != value:
                _fail("ONEE_CANONICAL_REPORT_FAIL", f"{field}={actual!r} expected={value!r}")

    return tuple(tuple(part) for part in current), report
