"""V371 IM01: source observations, exact recipes, and contextual field gates.

This module has NO file writer, serializer, grouping-based selector, or universal
runtime_end acceptance rule. Inputs are evidence-bound contracts; a local result
is never full product acceptance. IM02 receipts and IM03 layout/ownership are
separate gates. No new translation or runtime interpretation is performed here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
from typing import Any, Iterable


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ContractError(ValueError):
    def __init__(self, code: str, detail: str):
        self.code = code
        super().__init__(f"{code}: {detail}")


def require(condition: bool, code: str, detail: Any) -> None:
    if not condition:
        raise ContractError(code, str(detail))


def valid_sha(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


@dataclass(frozen=True)
class Span:
    start: int
    end: int

    def __post_init__(self) -> None:
        require(type(self.start) is int and type(self.end) is int and 0 <= self.start < self.end,
                'INVALID_SPAN', (self.start, self.end))

    @property
    def size(self) -> int:
        return self.end - self.start

    def overlaps(self, other: Span) -> bool:
        return self.start < other.end and other.start < self.end


@dataclass(frozen=True)
class Proof:
    """Location and bytes of already reviewed evidence, NOT an invented proof.

    The caller must provision the actual semantic authority. A content hash
    checks identity, not the truth of a document. The pinned-plan adapter binds
    these references to existing rows instead of accepting a boolean 'verified'.
    """
    document: str
    sha256: str
    claim: str
    row: int | None = None

    def __post_init__(self) -> None:
        require(bool(self.document) and valid_sha(self.sha256) and bool(self.claim),
                'INVALID_PROOF_REFERENCE', self.document)
        require(self.row is None or type(self.row) is int and self.row > 0,
                'INVALID_PROOF_ROW', self.row)


class Status(str, Enum):
    MEASURED = 'MEASURED_NOT_NORMATIVE'
    PREPARED = 'PREPARED_BEFORE_APPROVED_TRANSFORMS'
    SATISFIED = 'LOCAL_CONSTRAINT_SATISFIED'
    PRESERVED = 'LOCAL_PRESERVATION_IDENTITY'
    BLOCKED = 'BLOCKED'
    NOT_OBSERVED = 'NOT_OBSERVED'
    FAILED = 'OBSERVATION_FAILED'


@dataclass(frozen=True)
class Result:
    operation: str
    status: Status
    reasons: tuple[str, ...] = ()
    evidence: tuple[Proof, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)
    product_accepted: bool = field(default=False, init=False)

    def __bool__(self) -> bool:
        raise TypeError('Inspect result.status explicitly; a local result is not product PASS.')


def blocked(op: str, code: str, **details: Any) -> Result:
    return Result(op, Status.BLOCKED, (code,), details=details)


@dataclass(frozen=True)
class Observation:
    result: Result
    span: Span | None = None
    nul_offsets: tuple[int, ...] = ()


def observe_nul_view(data: bytes | None, start: int, limit: int, *, operation: str) -> Observation:
    """Bounded physical observation only; never authorizes a PC copy or mutation."""
    if data is None:
        return Observation(Result(operation, Status.NOT_OBSERVED, ('INPUT_NOT_AVAILABLE',)))
    if type(start) is not int or type(limit) is not int or not 0 <= start <= limit - 4 <= len(data) - 4:
        return Observation(Result(operation, Status.FAILED, ('HEADER_OR_LIMIT_OUT_OF_RANGE',)))
    opcode = data[start]
    if opcode not in (0x11, 0x12, 0x13, 0x15):
        return Observation(Result(operation, Status.FAILED, ('NOT_NUL_VIEW_HEADER',)))
    cursor = start + 4
    nuls: list[int] = []
    for _ in range(data[start + 1] if opcode == 0x15 else 1):
        end = data.find(b'\0', cursor, limit)
        if end < 0:
            return Observation(Result(operation, Status.FAILED, ('NUL_NOT_FOUND_WITHIN_LIMIT',),
                                      details={'cursor': cursor, 'limit': limit}), nul_offsets=tuple(nuls))
        nuls.append(end)
        cursor += (end - cursor + 4) & ~3
        if cursor > limit:
            return Observation(Result(operation, Status.FAILED, ('ALIGNED_VIEW_EXCEEDS_LIMIT',)),
                               nul_offsets=tuple(nuls))
    span = Span(start, cursor)
    return Observation(Result(operation, Status.MEASURED,
                              details={'method': 'BOUNDED_NUL_ALIGNED_VIEW',
                                       'measured_sha256': sha256(data[start:cursor]),
                                       'not_a_recipe_boundary_proof': True}), span, tuple(nuls))


class Route(str, Enum):
    DIRECT = 'SELECTED_REPLACEMENT_CANDIDATE'
    DELEGATE = 'DELEGATED_GRAPH_OUTER'
    PRESERVE = 'PRESERVATION_CANDIDATE'


@dataclass(frozen=True)
class OwnerContract:
    owner: str
    file: str
    partition: int
    observed_span: Span
    source_header: bytes
    route: Route
    binding: Proof
    recipe_kind: str
    recipe_id: str | None
    unit: str | None = None
    role_labels: tuple[str, ...] = ()
    holds: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require(self.owner == f'{self.file}:{self.observed_span.start:X}', 'OWNER_KEY_MISMATCH', self.owner)
        require(type(self.partition) is int and self.partition >= 0 and isinstance(self.source_header, bytes) and len(self.source_header) == 4,
                'INVALID_OWNER', self.owner)
        require(isinstance(self.route, Route), 'INVALID_OWNER_ROUTE', self.route)
        require((self.route == Route.PRESERVE and self.recipe_id is None) or
                (self.route != Route.PRESERVE and bool(self.recipe_id)), 'OWNER_RECIPE_ROUTE_MISMATCH', self.owner)

    @property
    def needs_upstream_recipe(self) -> bool:
        # Final delegation NEVER suppresses upstream preparation.
        return self.route in (Route.DIRECT, Route.DELEGATE)


@dataclass(frozen=True)
class RegionAuthority:
    span: Span
    sha256: str
    proof: Proof

    def __post_init__(self) -> None:
        require(valid_sha(self.sha256), 'INVALID_REGION_HASH', self.sha256)


@dataclass(frozen=True)
class Window:
    """An actual byte window in a named source/PC asset, not assumed whole-file identity."""
    asset: str
    span: Span
    data: bytes

    def __post_init__(self) -> None:
        require(bool(self.asset) and isinstance(self.data, bytes) and len(self.data) == self.span.size, 'INVALID_WINDOW', self.asset)


class RecipeKind(str, Enum):
    DIRECT = 'FROZEN_DIRECT_HEADER_PRESERVED'
    COMPOSITE = 'FROZEN_CANONICAL_COMPOSITE'


@dataclass(frozen=True)
class RecipeContract:
    owner: str
    recipe_id: str | None
    kind: RecipeKind
    source_asset: str
    source: RegionAuthority
    boundary_proof: Proof
    expected_source_header: bytes
    pc_asset: str | None = None
    pc: RegionAuthority | None = None
    expected_pc_header: bytes | None = None
    canonical_literal: bytes | None = None
    canonical_literal_sha256: str | None = None
    transform_obligations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require(isinstance(self.kind, RecipeKind) and isinstance(self.expected_source_header, bytes) and len(self.expected_source_header) == 4, 'INVALID_RECIPE_HEADER', self.owner)
        if self.kind == RecipeKind.DIRECT:
            require(self.pc is not None and self.pc_asset is not None and self.expected_pc_header is not None
                    and len(self.expected_pc_header) == 4 and self.canonical_literal is None,
                    'INCOMPLETE_DIRECT_RECIPE', self.owner)
        elif self.kind == RecipeKind.COMPOSITE:
            require(self.pc is None and self.canonical_literal is not None
                    and valid_sha(self.canonical_literal_sha256), 'INCOMPLETE_COMPOSITE_RECIPE', self.owner)
        else:
            raise ContractError('UNKNOWN_RECIPE_KIND', str(self.kind))


@dataclass(frozen=True)
class InteriorFieldBinding:
    """One exact subordinate four-byte field owned by a containing recipe.

    This is an applicability receipt, not an opcode-family permission.  The
    source envelope, materialized relative slot, target, codec and responsibility
    scope must all match the retained FieldContract and ReviewedFieldRule.
    """
    field: str
    source_span: Span
    relative: int
    source_word_sha256: str
    source_target: int
    codec: str
    partition: int
    unit: str | None

    def __post_init__(self) -> None:
        require(bool(self.field) and self.source_span.size == 4
                and type(self.relative) is int and self.relative >= 4 and self.relative % 4 == 0
                and valid_sha(self.source_word_sha256) and type(self.source_target) is int
                and self.source_target >= 0 and bool(self.codec)
                and type(self.partition) is int and self.partition >= 0,
                'INVALID_REVIEWED_INTERIOR_FIELD_BINDING', self.field)


@dataclass(frozen=True)
class ReviewedInteriorRecipe:
    """Narrow H01 discharge for an exact parent recipe and subordinate slots.

    The current implementation deliberately supports only a reviewed identity
    parent map: source and PC windows are byte-identical, and every subordinate
    field keeps its exact source-relative coordinate.  This prevents a generic
    H01 bypass and preserves the fail-closed behaviour for every other owner.
    """
    owner: str
    recipe_id: str
    source_span: Span
    source_sha256: str
    pc_span: Span
    pc_sha256: str
    payload_sha256: str
    identity_map: bool
    slots: tuple[InteriorFieldBinding, ...]
    proof: Proof

    def __post_init__(self) -> None:
        object.__setattr__(self, 'slots', tuple(self.slots))
        require(bool(self.owner) and bool(self.recipe_id)
                and valid_sha(self.source_sha256) and valid_sha(self.pc_sha256)
                and valid_sha(self.payload_sha256) and self.identity_map is True
                and self.source_span.size == self.pc_span.size
                and isinstance(self.proof, Proof) and bool(self.slots),
                'INVALID_REVIEWED_INTERIOR_RECIPE', self.owner)
        require(len({s.field for s in self.slots}) == len(self.slots),
                'DUPLICATE_REVIEWED_INTERIOR_FIELD', self.owner)
        for s in self.slots:
            require(self.source_span.start + 4 <= s.source_span.start
                    and s.source_span.end <= self.source_span.end
                    and s.relative == s.source_span.start - self.source_span.start
                    and s.relative + 4 <= self.source_span.size,
                    'REVIEWED_INTERIOR_IDENTITY_SLOT_MISMATCH', s.field)

    def slot(self, field: str) -> InteriorFieldBinding | None:
        return next((s for s in self.slots if s.field == field), None)

    def validate_recipe(self, owner: OwnerContract, recipe: RecipeContract,
                        source: Window, pc: Window, payload: bytes) -> None:
        require('H01' in owner.holds and self.owner == owner.owner
                and self.recipe_id == owner.recipe_id == recipe.recipe_id,
                'H01_REVIEWED_RECIPE_OWNER_SCOPE', owner.owner)
        require(recipe.kind == RecipeKind.DIRECT
                and recipe.source.span == self.source_span
                and recipe.pc is not None and recipe.pc.span == self.pc_span
                and recipe.source.sha256 == self.source_sha256
                and recipe.pc.sha256 == self.pc_sha256,
                'H01_REVIEWED_RECIPE_BOUNDARY_OR_HASH', owner.owner)
        require(source.span == self.source_span and pc.span == self.pc_span
                and sha256(source.data) == self.source_sha256
                and sha256(pc.data) == self.pc_sha256,
                'H01_REVIEWED_RECIPE_ACTUAL_WINDOW_IDENTITY', owner.owner)
        require(source.data == pc.data == payload
                and sha256(payload) == self.payload_sha256,
                'H01_REVIEWED_IDENTITY_PARENT_MISMATCH', owner.owner)

    def validate_directive(self, payload: bytes, field_slots: Iterable[Any]) -> None:
        supplied = tuple(field_slots)
        require(sha256(payload) == self.payload_sha256 and len(payload) == self.source_span.size,
                'H01_FINAL_PAYLOAD_IDENTITY', self.owner)
        actual = {(s.field, s.source_span.start, s.source_span.end, s.relative)
                  for s in supplied}
        expected = {(s.field, s.source_span.start, s.source_span.end, s.relative)
                    for s in self.slots}
        require(len(actual) == len(supplied) and actual == expected,
                'H01_EXACT_INTERIOR_SLOT_SET_REQUIRED', self.owner)

    def validate_field(self, contract: Any, rule: Any) -> None:
        slot = self.slot(contract.field)
        require(slot is not None and self.recipe_id in contract.interior_recipe_ids,
                'H01_FIELD_NOT_IN_REVIEWED_PARENT', contract.field)
        require(slot.source_span == contract.source_span
                and slot.source_word_sha256 == sha256(contract.source_header)
                and slot.source_target == contract.source_target
                and slot.partition == contract.partition and slot.unit == contract.unit,
                'H01_REVIEWED_FIELD_CONTRACT_SCOPE', contract.field)
        require(rule.field == slot.field and rule.codec == slot.codec
                and rule.source_word_sha256 == slot.source_word_sha256
                and rule.source_target == slot.source_target
                and rule.partition == slot.partition and rule.unit == slot.unit,
                'H01_REVIEWED_FIELD_RULE_SCOPE', contract.field)


@dataclass(frozen=True)
class PreparedRecipe:
    result: Result
    owner: str
    recipe_id: str | None
    source_span: Span | None = None
    data: bytes | None = None
    data_sha256: str | None = None
    route: Route | None = None
    pending_stages: tuple[str, ...] = ('IM02_EXACT_OBLIGATIONS', 'IM03_FINAL_LAYOUT_AND_WRITER', 'VAL01')


def _window_matches(window: Window | None, asset: str | None, authority: RegionAuthority | None) -> bool:
    return (window is not None and authority is not None and window.asset == asset
            and window.span == authority.span and sha256(window.data) == authority.sha256)


def prepare_recipe(owner: OwnerContract, recipe: RecipeContract | None,
                   source: Window | None, pc: Window | None = None,
                   interior: ReviewedInteriorRecipe | None = None) -> PreparedRecipe:
    """Prepare one exact, pre-transform command; NO NUL-derived fallback slice.

    Does not load fonts, execute a builder, choose translation, or emit a file.
    Fixed source headers and composite-before-transform ordering are preserved.
    """
    op = f'PREPARE:{owner.owner}'
    def fail(code: str) -> PreparedRecipe:
        return PreparedRecipe(blocked(op, code), owner.owner, owner.recipe_id, route=owner.route)
    if not owner.needs_upstream_recipe:
        return fail('PRESERVATION_ROUTE_HAS_NO_KO_RECIPE_OPERATION')
    if 'H01' in owner.holds and interior is None:
        return fail('H01_EXACT_INTERIOR_RECIPE_AND_WRITER_REQUIRED')
    if 'H01' not in owner.holds and interior is not None:
        return fail('UNEXPECTED_REVIEWED_INTERIOR_RECIPE')
    if recipe is None:
        return fail('MISSING_EXACT_RECIPE_BOUNDARY_AUTHORITY')
    if not isinstance(recipe, RecipeContract):
        return fail('OBSERVATION_OR_LABEL_IS_NOT_RECIPE_AUTHORITY')
    if recipe.owner != owner.owner or recipe.recipe_id != owner.recipe_id:
        return fail('RECIPE_OWNER_OR_BINDING_MISMATCH')
    if recipe.source.span.start != owner.observed_span.start:
        return fail('RECIPE_SOURCE_START_MISMATCH')
    # An approved recipe extent need not equal an old physical observation extent.
    if not _window_matches(source, recipe.source_asset, recipe.source):
        return fail('SOURCE_WINDOW_IDENTITY_OR_RANGE_MISMATCH')
    assert source is not None
    if source.data[:4] != owner.source_header or source.data[:4] != recipe.expected_source_header:
        return fail('SOURCE_HEADER_MISMATCH')
    evidence = [owner.binding, recipe.boundary_proof, recipe.source.proof]
    if recipe.kind == RecipeKind.DIRECT:
        if not _window_matches(pc, recipe.pc_asset, recipe.pc):
            return fail('PC_WINDOW_IDENTITY_OR_RANGE_MISMATCH')
        assert pc is not None and recipe.pc is not None
        if pc.data[:4] != recipe.expected_pc_header:
            return fail('PC_BOUND_HEADER_MISMATCH')
        payload = source.data[:4] + pc.data[4:]
        evidence.append(recipe.pc.proof)
    else:
        assert recipe.canonical_literal is not None
        if sha256(recipe.canonical_literal) != recipe.canonical_literal_sha256:
            return fail('CANONICAL_COMPOSITE_LITERAL_HASH_MISMATCH')
        payload = recipe.canonical_literal
    if interior is not None:
        try:
            require(source is not None and pc is not None,
                    'H01_ACTUAL_WINDOWS_REQUIRED', owner.owner)
            interior.validate_recipe(owner, recipe, source, pc, payload)
        except ContractError as ex:
            return fail(ex.code)
        evidence.append(interior.proof)
    if len(payload) < 4 or len(payload) % 4 or payload[:4] != owner.source_header:
        return fail('MATERIALIZED_HEADER_OR_ALIGNMENT_MISMATCH')
    result = Result(op, Status.PREPARED, evidence=tuple(evidence),
                    details={'route': owner.route.value, 'upstream_delegate_not_dropped': True,
                             'transform_obligations': list(recipe.transform_obligations),
                             'order': 'FROZEN_RECIPE_THEN_APPROVED_TRANSFORMS',
                             'extent_basis': 'EXPLICIT_RECIPE_NOT_NUL_OBSERVATION',
                             'reviewed_interior_identity_contract': interior is not None})
    return PreparedRecipe(result, owner.owner, owner.recipe_id, recipe.source.span, payload,
                          sha256(payload), owner.route)


def validate_prepared_payload(owner: OwnerContract, prepared: PreparedRecipe, payload: bytes) -> Result:
    """Third old call site: exact pre-transform recipe, not runtime_end(payload)."""
    op = f'PAYLOAD:{owner.owner}'
    if prepared.owner != owner.owner or prepared.recipe_id != owner.recipe_id:
        return blocked(op, 'PAYLOAD_RECIPE_OWNER_MISMATCH')
    if prepared.route != owner.route:
        return blocked(op, 'PREPARED_ROUTE_MISMATCH')
    if prepared.result.status != Status.PREPARED or prepared.data is None:
        return blocked(op, 'RECIPE_NOT_PREPARED')
    if payload != prepared.data or sha256(payload) != prepared.data_sha256:
        return blocked(op, 'PAYLOAD_DIFFERS_FROM_PREPARED_RECIPE')
    if payload[:4] != owner.source_header or len(payload) % 4:
        return blocked(op, 'PAYLOAD_STRUCTURAL_HEADER_OR_ALIGNMENT')
    return Result(op, Status.SATISFIED, evidence=prepared.result.evidence,
                  details={'stage': 'PRE_TRANSFORM_ONLY', 'pending_stages': list(prepared.pending_stages)})


@dataclass(frozen=True)
class ProtectedRange:
    id: str
    source_span: Span
    expected: bytes
    proof: Proof

    def __post_init__(self) -> None:
        require(bool(self.id) and isinstance(self.expected, bytes) and len(self.expected) == self.source_span.size,
                'INVALID_PROTECTED_RANGE', self.id)


@dataclass(frozen=True)
class ConsumerContract:
    id: str
    owner: str
    kind: str
    entry_condition: str
    ranges: tuple[ProtectedRange, ...]
    proof: Proof
    # No claim of complete reachability or global exclusion follows from this.
    other_entry_absence_proven: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        require(bool(self.id) and bool(self.entry_condition) and bool(self.ranges), 'INVALID_CONSUMER', self.id)
        require(len({r.id for r in self.ranges}) == len(self.ranges), 'DUPLICATE_VIEW_RANGE', self.id)


@dataclass(frozen=True)
class MappedWindow:
    range_id: str
    source_span: Span
    final_span: Span
    actual: bytes
    mapping_proof: Proof


def validate_consumer_view(contract: ConsumerContract, windows: Iterable[MappedWindow]) -> Result:
    """Fourth old call site: exact context-bound protected views, never whole-owner exemption.

    Mapping is an input from IM03, not guessed by this module. Conditions are
    retained conservatively: unknown guards do not authorize skipping a view.
    """
    op = f'VIEW:{contract.id}'
    samples = tuple(windows)
    if len({w.range_id for w in samples}) != len(samples):
        return blocked(op, 'DUPLICATE_MAPPED_VIEW_RANGE')
    by_id = {w.range_id: w for w in samples}
    if set(by_id) != {r.id for r in contract.ranges}:
        return blocked(op, 'MISSING_OR_EXTRA_MAPPED_VIEW_RANGE')
    evidence: list[Proof] = [contract.proof]
    displacements = set()
    for r in contract.ranges:
        w = by_id[r.id]
        if w.source_span != r.source_span or w.final_span.size != r.source_span.size:
            return blocked(op, 'VIEW_MAPPING_RANGE_MISMATCH', range_id=r.id)
        if len(w.actual) != w.final_span.size or w.actual != r.expected:
            return blocked(op, 'PROTECTED_CONTENT_CHANGED', range_id=r.id)
        displacements.add(w.final_span.start - r.source_span.start)
        evidence.extend((r.proof, w.mapping_proof))
    # These specific preservation recipes are contiguous identity views.
    if len(displacements) != 1:
        return blocked(op, 'PRESERVED_VIEW_CONTINUATION_NOT_CONTIGUOUS')
    return Result(op, Status.SATISFIED, evidence=tuple(evidence),
                  details={'owner': contract.owner, 'entry_condition': contract.entry_condition,
                           'kind': contract.kind, 'global_owner_exemption': False,
                           'claim': 'THIS_ESTABLISHED_VIEW_ONLY; FINAL_WRITER_AND_OTHER_VIEWS_STILL_REQUIRED'})


class FieldState(str, Enum):
    CONTEXT = 'INHERITED_CONTEXT_APPLICABILITY_PENDING_LAYOUT'
    UNKNOWN = 'EFFECT_DEPENDENT_HOLD'
    PAYLOAD = 'PRESERVE_PAYLOAD_CONTRACT_BOUND'
    BRANCH04 = 'TYPED_FIELD_CONTRACT_BOUND_PENDING_LAYOUT'
    SPECIAL = 'INHERITED_SPECIAL_RULE_BOUND_PENDING_LAYOUT'
    DISPOSITION = 'BLOCKED_CANONICAL_PLAN_DISPOSITION'


@dataclass(frozen=True)
class FieldContract:
    field: str
    source_span: Span
    source_header: bytes
    source_target: int
    partition: int
    unit: str | None
    state: FieldState
    proof: Proof
    dependency_ids: tuple[str, ...]
    protected_ranges: tuple[ProtectedRange, ...] = ()
    required_view_ids: tuple[str, ...] = ()
    interior_recipe_ids: tuple[str, ...] = ()
    candidate_retained: bool = field(default=True, init=False)

    def __post_init__(self) -> None:
        require(isinstance(self.source_header, bytes) and len(self.source_header) == self.source_span.size == 4, 'INVALID_FIELD_ENVELOPE', self.field)
        require(isinstance(self.state, FieldState), 'UNKNOWN_FIELD_STATE', self.state)
        require(bool(self.dependency_ids) and len(set(self.dependency_ids)) == len(self.dependency_ids),
                'INVALID_FIELD_DEPENDENCIES', self.field)
        require(len(set(self.required_view_ids)) == len(self.required_view_ids), 'DUPLICATE_REQUIRED_VIEW', self.field)


@dataclass(frozen=True)
class DependencyIdentity:
    id: str
    before_sha256: str
    after_sha256: str
    proof: Proof

    def __post_init__(self) -> None:
        require(valid_sha(self.before_sha256) and valid_sha(self.after_sha256), 'INVALID_DEPENDENCY_HASH', self.id)


@dataclass(frozen=True)
class FinalFieldAnchors:
    field: str
    source_field: int
    source_target: int
    final_field: int
    final_target: int
    final_storage_end: int
    source_partition: int
    final_field_partition: int
    final_target_partition: int
    unit: str | None
    proof: Proof


@dataclass(frozen=True)
class DispositionApproval:
    field: str
    unit: str
    expected_word_sha256: str
    disposition: str
    proof: Proof


@dataclass(frozen=True)
class FieldProposal:
    field: str
    before: bytes
    after: bytes | None
    dependencies: tuple[DependencyIdentity, ...] = ()
    anchors: FinalFieldAnchors | None = None
    approval: DispositionApproval | None = None
    additional_protections: tuple[ProtectedRange, ...] = ()


def check_field_proposal(contract: FieldContract, proposal: FieldProposal) -> Result:
    """Validate a four-byte proposal without writing any game bytes.

    Context labels alone do not select an encoder. Identity is not a relocation
    PASS. Accepted local proposals still require all contextual-view, exact
    canonical obligation and single-final-writer checks in later packages.
    """
    op = f'FIELD:{contract.field}'
    if proposal.field != contract.field or proposal.before != contract.source_header:
        return blocked(op, 'FIELD_INPUT_IDENTITY_MISMATCH')
    if proposal.after is None:
        return Result(op, Status.NOT_OBSERVED, ('PROPOSED_EFFECT_NOT_AVAILABLE',))
    if len(proposal.after) != 4:
        return blocked(op, 'FIELD_STORAGE_ENVELOPE_NOT_FOUR_BYTES')
    if contract.interior_recipe_ids:
        return blocked(op, 'H01_INTERIOR_MAPPING_AND_SINGLE_WRITER_REQUIRED',
                       recipes=list(contract.interior_recipe_ids))
    deps = {d.id: d for d in proposal.dependencies}
    if len(deps) != len(proposal.dependencies) or set(deps) != set(contract.dependency_ids):
        return blocked(op, 'MISSING_DUPLICATE_OR_EXTRA_DEPENDENCY_EVIDENCE')
    # Enforce the FULL physical envelope, not merely the presumed high-halfword.
    for p in contract.protected_ranges + proposal.additional_protections:
        if not p.source_span.overlaps(contract.source_span):
            continue
        lo = max(p.source_span.start, contract.source_span.start)
        hi = min(p.source_span.end, contract.source_span.end)
        original = p.expected[lo-p.source_span.start:hi-p.source_span.start]
        if proposal.before[lo-contract.source_span.start:hi-contract.source_span.start] != original:
            return blocked(op, 'PROTECTED_INPUT_IDENTITY_MISMATCH', view=p.id)
        if proposal.after[lo-contract.source_span.start:hi-contract.source_span.start] != original:
            return blocked(op, 'BLOCK_CONFLICT_PROTECTED_VIEW', view=p.id)
    if contract.state == FieldState.DISPOSITION:
        a = proposal.approval
        if (a is None or a.field != contract.field or a.unit != contract.unit
                or a.disposition != 'PRESERVE_SECONDARY_HEADER'
                or a.expected_word_sha256 != sha256(contract.source_header)):
            return blocked(op, 'H02_EXPLICIT_CANONICAL_PLAN_DISPOSITION_REQUIRED')
    evidence = (contract.proof,) + tuple(d.proof for d in proposal.dependencies)
    pending = {'required_final_view_ids': list(contract.required_view_ids),
               'pending_stages': ['IM02_EXACT_OBLIGATIONS', 'IM03_FINAL_WRITER', 'VAL01'],
               'candidate_retained': True, 'unit': contract.unit}
    identity = proposal.after == proposal.before
    if identity and any(d.before_sha256 != d.after_sha256 for d in proposal.dependencies):
        return blocked(op, 'IDENTITY_BYTES_WITH_CHANGED_DEPENDENCIES_NOT_DISCHARGED')
    typed_details: dict[str, Any] = {}
    # For a proved branch, equality of bytes is insufficient when an explicit
    # final map says the destination changed. Validate the map even on identity.
    if contract.state == FieldState.BRANCH04:
        a = proposal.anchors
        if a is None:
            return blocked(op, 'MISSING_FINAL_ANCHOR_PROOF')
        if (a.field != contract.field or a.source_field != contract.source_span.start
                or a.source_target != contract.source_target or a.source_partition != contract.partition
                or a.unit != contract.unit):
            return blocked(op, 'ANCHOR_TARGET_OR_RESPONSIBILITY_MISMATCH')
        if (any(type(v) is not int or v < 0 for v in
                (a.final_field, a.final_target, a.final_storage_end, a.final_field_partition, a.final_target_partition))
                or a.final_field % 4 or a.final_target % 4
                or a.final_storage_end != a.final_field + 4
                or a.final_field_partition != contract.partition
                or a.final_target_partition != contract.partition):
            return blocked(op, 'FIELD_ANCHOR_ALIGNMENT_ENVELOPE_OR_PARTITION')
        delta = a.final_target - a.final_field
        if delta % 4 or not 4 <= delta <= 32764:
            return blocked(op, 'EVENT04_SPAN_UNREPRESENTABLE', delta=delta)
        old = int.from_bytes(proposal.before, 'little')
        new = int.from_bytes(proposal.after, 'little')
        if old & 0xff != 0x04 or 4 * ((old >> 19) & 0x1fff) != contract.source_target - contract.source_span.start:
            return blocked(op, 'EVENT04_SOURCE_CONTRACT_MISMATCH')
        if ((old ^ new) & 0x0007ffff) != 0:
            return blocked(op, 'EVENT04_PROTECTED_OPCODE_SELECTOR_BITS_CHANGED')
        expected = (old & 0x0007ffff) | ((delta // 4) << 19)
        if new != expected:
            return blocked(op, 'EVENT04_ENCODED_DESTINATION_MISMATCH')
        evidence += (a.proof,)
        typed_details = {'span': delta, 'allowed_mask_numeric': '0xfff80000',
                         'actual_changed_offsets': [i for i in range(4) if proposal.before[i] != proposal.after[i]]}
    elif not identity:
        if contract.state == FieldState.SPECIAL:
            return blocked(op, 'EXISTING_SPECIAL_RULE_ADAPTER_NOT_CONNECTED', state=contract.state.value)
        return blocked(op, 'MISSING_APPLICABLE_NONIDENTITY_FIELD_RULE', state=contract.state.value)
    if identity:
        if proposal.approval is not None:
            evidence += (proposal.approval.proof,)
        return Result(op, Status.PRESERVED, evidence=evidence,
                      details={**pending, **typed_details, 'relocation_pass': False})
    return Result(op, Status.SATISFIED, evidence=evidence,
                  details={**pending, **typed_details, 'claim': 'LOCAL_TYPED_FIELD_RULE_ONLY'})


def require_all_view_results(required_ids: Iterable[str], results: Iterable[Result]) -> Result:
    """Joint known-view gate. A scalar path never deletes another known view."""
    required = tuple(required_ids)
    observed = tuple(results)
    if any(not r.operation.startswith('VIEW:') or not r.evidence for r in observed):
        return blocked('JOINT_VIEWS', 'NOT_AN_EVIDENCE_BOUND_VIEW_RESULT')
    keys = tuple(r.operation.removeprefix('VIEW:') for r in observed)
    if len(set(required)) != len(required) or len(set(keys)) != len(keys) or set(keys) != set(required):
        return blocked('JOINT_VIEWS', 'MISSING_DUPLICATE_OR_EXTRA_VIEW_RESULT')
    if not required:
        return blocked('JOINT_VIEWS', 'NO_APPLICABLE_CONSUMER_CONTRACT')
    if any(r.status != Status.SATISFIED for r in observed):
        return blocked('JOINT_VIEWS', 'ESTABLISHED_VIEW_NOT_SATISFIED')
    return Result('JOINT_VIEWS', Status.SATISFIED,
                  evidence=tuple(p for r in observed for p in r.evidence),
                  details={'global_owner_exemption': False, 'known_views': list(required)})


def emit_product(*args: Any, **kwargs: Any) -> None:
    """An explicit hard stop, not a partial serializer with a tempting --force."""
    raise ContractError('PRODUCT_EMISSION_DISABLED_IM01', 'IM02, IM03 and VAL01 are not satisfied.')
