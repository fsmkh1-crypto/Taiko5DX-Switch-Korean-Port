from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

from builder.selective_event import SelectiveEventError


CANONICAL_STOCK_MAIN_SHA256 = "b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b"
CANONICAL_V339_DIAGNOSTIC_SHA256 = "9d5821f0cc35356f68d1f243adc644c4be635e62ca4d9154bfe665cb612fd40c"


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
        # current_offset is intentionally excluded: relocation can move the
        # same original logical object in a valid selective layout.
        return (
            self.kind,
            self.partition,
            self.original_offset,
            self.opcode,
            self.decoded_length,
        )


@dataclass(frozen=True)
class StateAwareResidualGateReport:
    baseline_residuals: int
    candidate_residuals: int
    inherited_residuals: int
    resolved_baseline_residuals: int
    novel_residuals: int
    blocking: bool

    def to_dict(self) -> dict:
        return asdict(self)


CANONICAL_STOCK_STATEAWARE_RESIDUALS = (
    StateAwareResidual(
        partition=593,
        original_offset=0xBDD78,
        current_offset=0xBDD78,
        opcode=0x0E,
        decoded_length=0x7F5408,
    ),
)


def _fail(code: str, detail: str) -> None:
    raise SelectiveEventError(code, detail)


def decode_event_01020e0f_parent_length(header: bytes) -> int:
    if len(header) != 4 or header[0] not in (0x01, 0x02, 0x0E, 0x0F):
        _fail("EVENT_PARENT_LENGTH_HEADER_FAIL", header.hex())
    word = int.from_bytes(header, "little")
    return (word >> 6) & 0x3FFFFFC


def _unique_by_logical_key(
    residuals: Sequence[StateAwareResidual] | Iterable[StateAwareResidual],
    *,
    label: str,
) -> dict[tuple[str, int, int, int, int], StateAwareResidual]:
    result: dict[tuple[str, int, int, int, int], StateAwareResidual] = {}
    for residual in residuals:
        key = residual.logical_key
        if key in result:
            _fail(
                "EVENT_STATEAWARE_DUPLICATE_RESIDUAL",
                f"{label} duplicate={key}",
            )
        result[key] = residual
    return result


def validate_stateaware_residual_delta(
    candidate_residuals: Sequence[StateAwareResidual] | Iterable[StateAwareResidual],
    *,
    baseline_residuals: Sequence[StateAwareResidual] | Iterable[StateAwareResidual] = CANONICAL_STOCK_STATEAWARE_RESIDUALS,
) -> StateAwareResidualGateReport:
    """Reject only state-aware structural residuals that are novel vs stock.

    The V340 gate is differential rather than zero-error. A residual is
    inherited only when its original logical anchor, opcode, decoded length,
    and residual kind exactly match stock. current_offset may differ because
    valid selective payload growth relocates the same logical object.
    """
    baseline = _unique_by_logical_key(tuple(baseline_residuals), label="baseline")
    candidate = _unique_by_logical_key(tuple(candidate_residuals), label="candidate")

    baseline_keys = set(baseline)
    candidate_keys = set(candidate)
    novel = candidate_keys - baseline_keys
    inherited = candidate_keys & baseline_keys
    resolved = baseline_keys - candidate_keys

    if novel:
        detail = ", ".join(repr(key) for key in sorted(novel))
        _fail("EVENT_STATEAWARE_NOVEL_RESIDUAL", detail)

    return StateAwareResidualGateReport(
        baseline_residuals=len(baseline_keys),
        candidate_residuals=len(candidate_keys),
        inherited_residuals=len(inherited),
        resolved_baseline_residuals=len(resolved),
        novel_residuals=0,
        blocking=False,
    )


def canonical_v339_residual() -> StateAwareResidual:
    return StateAwareResidual(
        partition=593,
        original_offset=0xBDD78,
        current_offset=0xDDD84,
        opcode=0x0E,
        decoded_length=decode_event_01020e0f_parent_length(bytes.fromhex("0e02d51f")),
    )
