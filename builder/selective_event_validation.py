from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import struct
from typing import Iterable, Sequence

from builder.selective_event import SelectiveEventError

CANONICAL_STOCK_MAIN_SHA256 = "b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b"
CANONICAL_V339_DIAGNOSTIC_SHA256 = "9d5821f0cc35356f68d1f243adc644c4be635e62ca4d9154bfe665cb612fd40c"

ALIAS_LEDGER_RECORD = struct.Struct("<HIIIHIIBB")
ALIAS_LEDGER_RECORD_COUNT = 52
ALIAS_LEDGER_SHA256 = "62e2d01d5aab9b8bc9a156e04acf3842cdef8ca58bbc29c8629228aec651518c"
ALIAS_INHERITED_STOCK_RESIDUAL = 1
ALIAS_NOVEL_ELIGIBLE = 2
ALIAS_NOT_GATE_ELIGIBLE = 3
EXPECTED_ALIAS_DISPOSITIONS = {
    ALIAS_INHERITED_STOCK_RESIDUAL: 1,
    ALIAS_NOVEL_ELIGIBLE: 48,
    ALIAS_NOT_GATE_ELIGIBLE: 3,
}

@dataclass(frozen=True)
class StateAwareResidual:
    partition: int
    original_offset: int
    current_offset: int | None
    opcode: int
    decoded_length: int
    kind: str = "EVENT_PARENT_OVERRUN"

    @property
    def logical_key(self) -> tuple[str, int, int, int, int]:
        return (self.kind, self.partition, self.original_offset, self.opcode, self.decoded_length)

@dataclass(frozen=True)
class StateAwareAliasRecord:
    partition: int
    parent_original_offset: int
    alias_original_offset: int
    parent_header: int
    parent_length: int
    alias_header: int
    alias_decoded_length: int
    disposition: int
    flags: int

    @property
    def logical_key(self) -> tuple[int, int, int, int]:
        return (self.partition, self.alias_original_offset, self.alias_header & 0xFF, self.alias_decoded_length)

@dataclass(frozen=True)
class StateAwareResidualGateReport:
    baseline_residuals: int
    candidate_observations: int
    candidate_residuals: int
    inherited_residuals: int
    source_alias_residuals: int
    resolved_baseline_residuals: int
    novel_residuals: int
    blocking: bool

    def to_dict(self) -> dict:
        return asdict(self)

CANONICAL_STOCK_STATEAWARE_RESIDUALS = (
    StateAwareResidual(593, 0xBDD78, 0xBDD78, 0x0E, 0x7F5408),
)

def _fail(code: str, detail: str) -> None:
    raise SelectiveEventError(code, detail)

def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def decode_event_01020e0f_parent_length(header: bytes) -> int:
    if len(header) != 4 or header[0] not in (0x01, 0x02, 0x0E, 0x0F):
        _fail("EVENT_PARENT_LENGTH_HEADER_FAIL", header.hex())
    return (int.from_bytes(header, "little") >> 6) & 0x3FFFFFC

def decode_event_04050a0b_parent_length(header: bytes) -> int:
    if len(header) != 4 or header[0] not in (0x04, 0x05, 0x0A, 0x0B):
        _fail("EVENT_CONTAINER_LENGTH_HEADER_FAIL", header.hex())
    return (int.from_bytes(header, "little") >> 17) & 0x7FFC

def load_stateaware_alias_ledger(blob: bytes, *, require_canonical: bool = True) -> tuple[StateAwareAliasRecord, ...]:
    if len(blob) % ALIAS_LEDGER_RECORD.size:
        _fail("EVENT_ALIAS_LEDGER_SIZE_FAIL", f"bytes={len(blob)}")
    if require_canonical:
        if len(blob) != ALIAS_LEDGER_RECORD_COUNT * ALIAS_LEDGER_RECORD.size:
            _fail("EVENT_ALIAS_LEDGER_COUNT_FAIL", f"bytes={len(blob)}")
        if _sha256(blob) != ALIAS_LEDGER_SHA256:
            _fail("EVENT_ALIAS_LEDGER_SHA_FAIL", _sha256(blob))
    rows = tuple(StateAwareAliasRecord(*v) for v in ALIAS_LEDGER_RECORD.iter_unpack(blob))
    if len({(r.partition, r.alias_original_offset) for r in rows}) != len(rows):
        _fail("EVENT_ALIAS_LEDGER_COLLISION", "duplicate alias original offset")
    if require_canonical:
        from collections import Counter
        counts = Counter(r.disposition for r in rows)
        if dict(counts) != EXPECTED_ALIAS_DISPOSITIONS:
            _fail("EVENT_ALIAS_LEDGER_DISPOSITION_FAIL", repr(dict(counts)))
    return rows

def _unique_baseline(residuals: Sequence[StateAwareResidual] | Iterable[StateAwareResidual]):
    out = {}
    for r in residuals:
        if r.logical_key in out:
            _fail("EVENT_STATEAWARE_DUPLICATE_BASELINE", repr(r.logical_key))
        out[r.logical_key] = r
    return out

def _collapse_candidate_observations(residuals: Sequence[StateAwareResidual] | Iterable[StateAwareResidual]):
    out = {}
    observations = 0
    for r in residuals:
        observations += 1
        prior = out.get(r.logical_key)
        if prior is not None and prior.current_offset != r.current_offset:
            _fail("EVENT_STATEAWARE_AMBIGUOUS_RESIDUAL", f"{r.logical_key}: {prior.current_offset} vs {r.current_offset}")
        out[r.logical_key] = r
    return out, observations

def _current_partition_bounds(blob: bytes, partition: int) -> tuple[int, int]:
    if len(blob) < 12:
        _fail("EVENT_ALIAS_CURRENT_BLOB_FAIL", "short TS5")
    count = int.from_bytes(blob[4:8], "little")
    if partition < 0 or partition >= count:
        _fail("EVENT_ALIAS_PARTITION_FAIL", str(partition))
    table_end = 8 + 4 * (count + 1)
    if table_end > len(blob):
        _fail("EVENT_ALIAS_CURRENT_BLOB_FAIL", "truncated offset table")
    a = int.from_bytes(blob[8 + 4 * partition:12 + 4 * partition], "little")
    b = int.from_bytes(blob[12 + 4 * partition:16 + 4 * partition], "little")
    return a, b

def _source_alias_matches(residual: StateAwareResidual, record: StateAwareAliasRecord, current_blob: bytes | None) -> bool:
    if record.disposition != ALIAS_NOVEL_ELIGIBLE or current_blob is None or residual.current_offset is None:
        return False
    if (residual.partition, residual.original_offset, residual.opcode, residual.decoded_length) != record.logical_key:
        return False
    a, b = _current_partition_bounds(current_blob, residual.partition)
    p = residual.current_offset
    if not (a + 4 <= p and p + 4 <= b):
        return False
    parent = current_blob[p-4:p]
    alias = current_blob[p:p+4]
    if len(parent) != 4 or len(alias) != 4:
        return False
    if int.from_bytes(parent, "little") != record.parent_header:
        return False
    if int.from_bytes(alias, "little") != record.alias_header:
        return False
    if parent[0] != 0x0B or alias[0] != 0x0E:
        return False
    if decode_event_04050a0b_parent_length(parent) != record.parent_length:
        return False
    if record.parent_original_offset + 4 != record.alias_original_offset:
        return False
    if not (4 < record.parent_length):
        return False
    if decode_event_01020e0f_parent_length(alias) != residual.decoded_length:
        return False
    return True

def validate_stateaware_residual_delta(
    candidate_residuals: Sequence[StateAwareResidual] | Iterable[StateAwareResidual],
    *,
    baseline_residuals: Sequence[StateAwareResidual] | Iterable[StateAwareResidual] = CANONICAL_STOCK_STATEAWARE_RESIDUALS,
    alias_records: Sequence[StateAwareAliasRecord] | Iterable[StateAwareAliasRecord] = (),
    current_blob: bytes | None = None,
) -> StateAwareResidualGateReport:
    """Block novel residuals except exact source-proven embedded aliases.

    Candidate observations may repeat the same logical residual under different
    conservative S/F states. They collapse only when the current physical
    offset is identical. Novel residuals are non-blocking only when an exact
    V344 alias record is NOVEL_ALIAS_ELIGIBLE and the current bytes prove the
    same 0x0B parent / +4 0x0E relation and decoded lengths.
    """
    baseline = _unique_baseline(tuple(baseline_residuals))
    candidate, observations = _collapse_candidate_observations(tuple(candidate_residuals))
    alias_index = {(r.partition, r.alias_original_offset, r.alias_header & 0xFF, r.alias_decoded_length): r for r in alias_records}

    inherited = set(candidate) & set(baseline)
    resolved = set(baseline) - set(candidate)
    source_alias = set()
    novel = set()
    for key, residual in candidate.items():
        if key in baseline:
            continue
        lookup = (residual.partition, residual.original_offset, residual.opcode, residual.decoded_length)
        record = alias_index.get(lookup)
        if record is not None and _source_alias_matches(residual, record, current_blob):
            source_alias.add(key)
        else:
            novel.add(key)
    if novel:
        _fail("EVENT_STATEAWARE_NOVEL_RESIDUAL", ", ".join(repr(x) for x in sorted(novel)))
    return StateAwareResidualGateReport(
        baseline_residuals=len(baseline), candidate_observations=observations, candidate_residuals=len(candidate),
        inherited_residuals=len(inherited), source_alias_residuals=len(source_alias), resolved_baseline_residuals=len(resolved),
        novel_residuals=0, blocking=False,
    )

def canonical_v339_residual() -> StateAwareResidual:
    return StateAwareResidual(593, 0xBDD78, 0xDDD84, 0x0E, decode_event_01020e0f_parent_length(bytes.fromhex("0e02d51f")))
