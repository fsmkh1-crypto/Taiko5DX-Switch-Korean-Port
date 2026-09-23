"""IM02 exact obligation receipt engine, with NO serializer or product writer.

Claims are deliberately local. A receipt binds actual supplied candidate bytes,
input authority, exact occurrence identity, mapping witnesses and selected writer
responsibility. It does not prove that caller-provided IM03 mapping/locator proofs
are semantically true or that the final file has passed every global invariant.
Missing evidence remains NOT_OBSERVED; malformed/conflicting evidence is BLOCKED.
Canonical admission is never recomputed, and family labels select no byte rewrite.
"""
from __future__ import annotations
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from dataclasses import dataclass, field, fields as dataclass_fields, is_dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from .selective_event_contracts import (
    ContractError, PreparedRecipe, Proof, RecipeContract, Route, Span, Status,
    Window, prepare_recipe, require, sha256, valid_sha,
)
from .selective_event_contract_catalog import ContractCatalog, CANONICAL_HEAD
from .selective_event_root_values import SerializedRootValues
from .selective_event_obligation_catalog import (
    ObligationCatalog, canonical_json, freeze, thaw,
)


def evidence_value(value: Any) -> Any:
    """Stable witness identity without embedding full input/output buffers."""
    if type(value) is bytes:
        return {'byte_size':len(value),'byte_sha256':sha256(value)}
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {f.name:evidence_value(getattr(value,f.name)) for f in dataclass_fields(value)}
    if isinstance(value, Mapping):
        return {k:evidence_value(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):
        return [evidence_value(v) for v in value]
    return value


ANY_UNIT = object()


class ReceiptState(str, Enum):
    SATISFIED = 'SATISFIED_LOCAL_OBLIGATION'
    BLOCKED = 'BLOCKED'
    NOT_OBSERVED = 'NOT_OBSERVED'


class Action(str, Enum):
    PRESERVE = 'AUTHORED_PRESERVATION'
    TRANSFORM = 'APPROVED_TRANSFORM'
    NOOP = 'PROVEN_NOOP'
    DELEGATE = 'PROVEN_DELEGATION'


@dataclass(frozen=True)
class Receipt:
    obligation: str
    state: ReceiptState
    outcome: str
    candidate_fingerprint: str | None
    catalog_fingerprint: str
    checks: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    dependencies: tuple[tuple[str, str], ...] = ()
    details: Mapping[str, Any] = field(default_factory=dict)
    product_accepted: bool = field(default=False, init=False)

    def __post_init__(self):
        object.__setattr__(self, 'details', freeze(dict(self.details)))

    def __bool__(self):
        raise TypeError('Use receipt.state; a receipt is not product acceptance.')

    def to_dict(self) -> dict:
        return {'obligation': self.obligation, 'state': self.state.value,
                'outcome': self.outcome, 'candidate_fingerprint': self.candidate_fingerprint,
                'catalog_fingerprint': self.catalog_fingerprint, 'checks': list(self.checks),
                'reasons': list(self.reasons), 'dependencies': [list(x) for x in self.dependencies],
                'details': thaw(self.details), 'product_accepted': False}

    @property
    def fingerprint(self) -> str:
        return sha256(canonical_json(self.to_dict()))


@dataclass(frozen=True)
class Candidate:
    """Immutable snapshot of provided buffers, not an EVENT file emitter.

    Keys: EVENT:<filename>, STOCK:<filename>, TAI5MSG:FINAL. Keeping source
    buffers here binds preservation checks to the same reproducible snapshot.
    """
    run_id: str
    catalog_fingerprint: str
    buffers: Mapping[str, bytes]
    canonical_head: str = CANONICAL_HEAD
    fingerprint: str = field(init=False)
    hashes: Mapping[str, str] = field(init=False)

    def __post_init__(self):
        require(isinstance(self.run_id, str) and bool(self.run_id), 'INVALID_RUN_ID', '')
        require(self.canonical_head == CANONICAL_HEAD and valid_sha(self.catalog_fingerprint),
                'CANDIDATE_AUTHORITY', '')
        require(all(isinstance(k, str) and k and type(v) is bytes for k,v in self.buffers.items()),
                'CANDIDATE_IMMUTABLE_BYTES_REQUIRED', '')
        copied = dict(self.buffers); hs = {k: sha256(v) for k,v in copied.items()}
        object.__setattr__(self, 'buffers', MappingProxyType(copied))
        object.__setattr__(self, 'hashes', MappingProxyType(hs))
        fp = sha256(canonical_json({'run_id': self.run_id, 'head': self.canonical_head,
                 'catalog': self.catalog_fingerprint,
                 'artifacts': {k: {'sha256': hs[k], 'size': len(v)} for k,v in copied.items()}}))
        object.__setattr__(self, 'fingerprint', fp)


@dataclass(frozen=True)
class Placement:
    """An explicit final-coordinate witness from IM03, never a guessed delta."""
    artifact: str
    artifact_sha256: str
    candidate_fingerprint: str
    span: Span
    partition: int
    unit: str | None
    proof: Proof


@dataclass(frozen=True)
class OwnerView:
    owner: str
    placement: Placement
    mode: str  # DELEGATED_VIEW / MEMBER_VIEW / PRESERVED_VIEW
    # ESTABLISHED_VIEW keeps the pre-existing explicit-witness API. The active
    # bridge always supplies one of the other three, more specific bases.
    extent_basis: str = 'ESTABLISHED_VIEW'
    recipe_placement: Placement | None = None


@dataclass(frozen=True)
class RecipeInput:
    owner: str
    source: Window | None
    pc: Window | None


@dataclass(frozen=True)
class OccurrenceSubmission:
    id: str
    owner: str
    pc_span: Span
    placement: Placement
    action: Action
    rewrite_id: str | None = None
    delegate_to: str | None = None
    preservation_permit: str | None = None


@dataclass(frozen=True)
class RootBinding:
    id: str
    block: int
    local: int
    placement: Placement
    locator_proof: Proof


@dataclass(frozen=True)
class UnitRegion:
    unit: str
    cluster: str
    placement: Placement


@dataclass(frozen=True)
class SupportSubmission:
    id: str
    owner: str
    source_span: Span
    placement: Placement


@dataclass(frozen=True)
class WriterRange:
    """Final ownership only; staging/supersession reconciliation is IM03.

    These are not writes executed by this engine. Equal duplicate declarations
    still conflict; the caller must send the selected final responsibility.
    """
    artifact: str
    span: Span
    writer: str
    unit: str | None
    candidate_fingerprint: str


@dataclass(frozen=True)
class ExactRewrite:
    """Already reviewed byte-exact rule for one occurrence/recipe preimage.

    A Proof is a pinned reference, not proof of its own semantic truth. Trusted
    caller provisioning is required; a family name or boolean cannot create one.
    No real new grammar rule is shipped or selected automatically by IM02.
    """
    id: str
    occurrence: str
    recipe_id: str
    before: bytes
    after: bytes
    prepared_sha256: str
    authority: Proof

    def __post_init__(self):
        require(bool(self.id) and bool(self.occurrence) and bool(self.recipe_id) and
                type(self.before) is bytes and len(self.before) > 0 and
                type(self.after) is bytes and len(self.after) > 0 and
                valid_sha(self.prepared_sha256) and isinstance(self.authority, Proof),
                'INVALID_EXACT_REWRITE', self.id)


@dataclass(frozen=True)
class PreservationPermit:
    """Reviewed action disposition, separate from semantic INCLUDE_KO.

    Exact copied bytes alone do not authorize skipping a required transform.
    The actual adapter must provide this action authority. Tests use conspicuously
    synthetic permits; no real preservation/no-op decisions are issued here.
    """
    id: str
    occurrence: str
    recipe_id: str
    before_sha256: str
    authority: Proof

    def __post_init__(self):
        require(bool(self.id) and bool(self.occurrence) and bool(self.recipe_id) and
                valid_sha(self.before_sha256) and isinstance(self.authority, Proof),
                'INVALID_PRESERVATION_PERMIT', self.id)


class RewriteRegistry:
    """Explicit evidence registry. Deliberately has no cause-family lookup."""
    def __init__(self, rules: Iterable[ExactRewrite] = (), permits: Iterable[PreservationPermit] = ()):
        permits = tuple(permits)
        require(all(isinstance(p, PreservationPermit) for p in permits), 'PERMIT_TYPE', '')
        require(len({p.id for p in permits}) == len(permits), 'DUPLICATE_PRESERVATION_PERMIT', '')
        self.permits = MappingProxyType({p.id:p for p in permits})
        rules = tuple(rules)
        require(all(isinstance(r, ExactRewrite) for r in rules), 'REWRITE_TYPE', '')
        require(len({r.id for r in rules}) == len(rules), 'DUPLICATE_REWRITE_ID', '')
        self.rules = MappingProxyType({r.id:r for r in rules})
        rule_rows = [
            {'id':r.id, 'occurrence':r.occurrence, 'recipe_id':r.recipe_id,
             'before':r.before.hex(), 'after':r.after.hex(), 'prepared':r.prepared_sha256,
             'authority': {'document':r.authority.document, 'sha256':r.authority.sha256,
                           'claim':r.authority.claim, 'row':r.authority.row}}
            for r in sorted(rules, key=lambda r:r.id)]
        permit_rows = [{'id':p.id, 'occurrence':p.occurrence, 'recipe_id':p.recipe_id,
                        'before_sha256':p.before_sha256,
                        'authority':{'document':p.authority.document,'sha256':p.authority.sha256,
                                     'claim':p.authority.claim,'row':p.authority.row}}
                       for p in sorted(permits,key=lambda p:p.id)]
        self.fingerprint = sha256(canonical_json({'rules':rule_rows,'permits':permit_rows}))


@dataclass(frozen=True)
class EvidenceBundle:
    candidate: Candidate
    owner_views: tuple[OwnerView, ...] = ()
    recipe_inputs: tuple[RecipeInput, ...] = ()
    occurrences: tuple[OccurrenceSubmission, ...] = ()
    roots: tuple[RootBinding, ...] = ()
    supports: tuple[SupportSubmission, ...] = ()
    unit_regions: tuple[UnitRegion, ...] = ()
    writers: tuple[WriterRange, ...] = ()

    def __post_init__(self):
        # Snapshot sequences as tuples so caller lists cannot mutate the batch.
        for key in ('owner_views', 'recipe_inputs', 'occurrences', 'roots', 'supports', 'unit_regions', 'writers'):
            object.__setattr__(self, key, tuple(getattr(self, key)))


class _Missing(ContractError):
    pass


def need(condition: bool, code: str, detail: Any = ''):
    if not condition:
        raise _Missing(code, str(detail))


def overlap(a: Span, b: Span) -> Span | None:
    lo, hi = max(a.start, b.start), min(a.end, b.end)
    return Span(lo, hi) if lo < hi else None


class WriterIndex:
    """Interval queries for local receipt coverage, not global final accounting."""
    def __init__(self, rows: tuple[WriterRange, ...], candidate: Candidate):
        tables = defaultdict(list)
        for r in rows:
            require(isinstance(r, WriterRange) and r.candidate_fingerprint == candidate.fingerprint,
                    'STALE_OR_INVALID_WRITER_WITNESS', '')
            require(r.artifact in candidate.buffers and r.span.end <= len(candidate.buffers[r.artifact]) and
                    isinstance(r.writer, str) and bool(r.writer), 'WRITER_ENVELOPE', r.artifact)
            tables[r.artifact].append(r)
        self.tables = {}
        for k, rr in tables.items():
            rr.sort(key=lambda r:(r.span.start, r.span.end, r.writer))
            running = 0; maxima = []
            for r in rr:
                running = max(running, r.span.end); maxima.append(running)
            self.tables[k] = (rr, [r.span.start for r in rr], maxima)

    def cover(self, artifact: str, span: Span, unit: str | None | object = ANY_UNIT) -> tuple[str, ...]:
        need(artifact in self.tables, 'FINAL_WRITER_WITNESS_NOT_OBSERVED', artifact)
        rr, starts, maxima = self.tables[artifact]
        rows = rr[bisect_right(maxima, span.start):bisect_left(starts, span.end)]
        events = defaultdict(lambda: [[], []])
        for i, r in enumerate(rows):
            s = overlap(span, r.span)
            if s is not None:
                events[s.start][0].append(i); events[s.end][1].append(i)
        points = sorted({span.start, span.end, *events}); active = set(); writers = set()
        for i, p in enumerate(points[:-1]):
            active.difference_update(events[p][1]); active.update(events[p][0])
            require(len(active) == 1, 'MISSING_OR_MULTIPLE_FINAL_WRITERS', (artifact,p,points[i+1],len(active)))
            r = rows[next(iter(active))]
            require(unit is ANY_UNIT or r.unit == unit, 'WRONG_CANONICAL_WRITER_UNIT', (r.unit,unit))
            writers.add(r.writer)
        return tuple(sorted(writers))


@dataclass(frozen=True)
class BatchReport:
    receipts: tuple[Receipt, ...]
    extra_errors: tuple[str, ...]
    catalog_fingerprint: str
    candidate_fingerprint: str | None
    rewrite_registry_fingerprint: str
    expected_obligation_ids: frozenset[str]
    product_accepted: bool = field(default=False, init=False)

    def __bool__(self):
        raise TypeError('Use local_complete explicitly; it is not V371 PASS.')

    @property
    def local_complete(self) -> bool:
        return (not self.extra_errors and self.candidate_fingerprint is not None and
                len(self.receipts) == len(self.expected_obligation_ids) > 0 and
                {r.obligation for r in self.receipts} == self.expected_obligation_ids and
                all(r.state == ReceiptState.SATISFIED and
                    r.candidate_fingerprint == self.candidate_fingerprint and
                    r.catalog_fingerprint == self.catalog_fingerprint for r in self.receipts))

    def summary(self) -> dict:
        grouped = defaultdict(Counter)
        for r in self.receipts:
            grouped[r.obligation.split(':')[0]][r.state.value] += 1
        return {'scope': 'IM02_LOCAL_OBLIGATION_RECEIPTS_ONLY',
                'catalog_fingerprint': self.catalog_fingerprint,
                'candidate_fingerprint': self.candidate_fingerprint,
                'rewrite_registry_fingerprint': self.rewrite_registry_fingerprint,
                'required_obligations': len(self.expected_obligation_ids),
                'receipt_rows': len(self.receipts),
                'missing_receipt_ids': sorted(self.expected_obligation_ids-{r.obligation for r in self.receipts}),
                'unexpected_receipt_ids': sorted({r.obligation for r in self.receipts}-self.expected_obligation_ids),
                'states': dict(Counter(r.state.value for r in self.receipts)),
                'by_kind': {k:dict(v) for k,v in sorted(grouped.items())},
                'extra_errors': list(self.extra_errors), 'local_complete': self.local_complete,
                'product_accepted': False, 'V371_closed': False,
                'pending_global_gates': ['IM03_ACTUAL_MAPPING_AND_FINAL_WRITER', 'H01_H02_NECESSARY_DISPOSITIONS',
                                          'FULL_INPUT_AUTHORITY', 'VAL01_169_FILE_OUTPUT_VALIDATION']}


class ObligationEngine:
    def __init__(self, catalog: ObligationCatalog, im01: ContractCatalog,
                 recipes: Mapping[str, RecipeContract], rewrites: RewriteRegistry | None = None):
        require(im01.plan_sha256 == catalog.plan_sha256, 'IM01_IM02_PLAN_MISMATCH', '')
        require(set(im01.owners) == set(catalog.owners), 'IM01_IM02_OWNER_SET_MISMATCH', '')
        self.catalog = catalog; self.im01 = im01
        self.recipes = MappingProxyType(dict(recipes))
        self.recipe_fingerprint = sha256(canonical_json(evidence_value(self.recipes)))
        self.rewrites = rewrites if rewrites is not None else RewriteRegistry()
        # Canonical source file identities, where present. No hash of the current
        # source is invented as its own expected authority.
        stock = {}
        for a in catalog.apps.values():
            cr = a['canonical_row']; f = cr['file']; h = cr['source_file_sha256']
            require(f not in stock or stock[f] == h, 'CONFLICTING_CANONICAL_SOURCE_IDENTITIES', f)
            stock[f] = h
        self.stock_hashes = MappingProxyType(stock)

    def verify(self, evidence: EvidenceBundle | None = None) -> BatchReport:
        return _Evaluation(self, evidence).run()

    def check_one(self, obligation: str, evidence: EvidenceBundle | None = None) -> Receipt:
        """Local diagnostic; cannot claim catalog coverage or product acceptance."""
        require(obligation in self.catalog.ids, 'UNKNOWN_REQUIRED_OBLIGATION', obligation)
        ev = _Evaluation(self, evidence)
        if ev.errors and ev.global_error is None:
            ev.global_error = ContractError('EXTRA_OR_DUPLICATE_SUBMISSIONS', ';'.join(ev.errors))
        dispatch = {'APP':ev.check_app,'OCC':ev.check_occ,'REL':ev.check_relation,
                    'SUP':ev.check_support,'ROOTREF':ev.check_root_ref,'ROOT':ev.check_root}
        return dispatch[obligation.split(':')[0]](obligation)

    def emit(self, *args, **kwargs):
        raise ContractError('PRODUCT_EMISSION_DISABLED_IM02', 'Receipt engine has no product writer.')


class _Evaluation:
    def __init__(self, engine: ObligationEngine, evidence: EvidenceBundle | None):
        self.e = engine; self.c = engine.catalog; self.bundle = evidence
        self.candidate = None if evidence is None else evidence.candidate
        self.fp = None if self.candidate is None else self.candidate.fingerprint
        self.witness_fp = None if evidence is None else sha256(canonical_json(evidence_value(evidence)))
        self.receipts: dict[str, Receipt] = {}; self.prepared = {}; self.prep_errors = {}
        self.serialized_roots = None
        self.errors: list[str] = []; self.global_error: ContractError | None = None
        self.views = {}; self.inputs = {}; self.occs = {}; self.roots = {}; self.supports = {}; self.regions = {}
        self.duplicates: dict[str,set] = defaultdict(set)
        self.writer_index = None
        if evidence is None:
            return
        try:
            require(self.candidate.catalog_fingerprint == self.c.fingerprint, 'STALE_CATALOG_FOR_CANDIDATE', '')
            self.views = self.index('VIEW', evidence.owner_views, 'owner', set(self.c.owners))
            self.inputs = self.index('RECIPE', evidence.recipe_inputs, 'owner', set(self.c.owners))
            self.occs = self.index('OCC', evidence.occurrences, 'id', set(self.c.occurrences))
            self.roots = self.index('ROOT', evidence.roots, 'id', set(self.c.roots))
            self.supports = self.index('SUP', evidence.supports, 'id', set(self.c.supports))
            self.regions = self.index('REGION', evidence.unit_regions, 'cluster',
                    {c for u in self.c.units.values() for c in u['cluster_ids']})
            self.writer_index = WriterIndex(evidence.writers, self.candidate)
            for w in evidence.writers:
                require(w.unit is None or w.unit in self.c.units, 'UNKNOWN_FINAL_WRITER_UNIT', w.unit)
            for r in evidence.unit_regions:
                require(r.unit in self.c.units and r.cluster in self.c.units[r.unit]['cluster_ids'],
                        'UNIT_REGION_MEMBERSHIP', r.cluster)
        except ContractError as ex:
            self.global_error = ex; self.errors.append(str(ex))

    def index(self, kind, rows, attr, allowed):
        groups = defaultdict(list)
        for r in rows:
            key = getattr(r, attr, None)
            require(isinstance(key, str), 'INVALID_SUBMISSION_KEY', kind)
            groups[key].append(r)
            if key not in allowed:
                self.errors.append(f'EXTRA_{kind}_SUBMISSION:{key}')
        for key, values in groups.items():
            if len(values) != 1:
                self.duplicates[kind].add(key)
                self.errors.append(f'DUPLICATE_{kind}_SUBMISSION:{key}')
        return {k:v[0] for k,v in groups.items() if len(v) == 1 and k in allowed}

    def get(self, kind, key, table):
        require(key not in self.duplicates[kind], 'DUPLICATE_REQUIRED_SUBMISSION', (kind,key))
        need(key in table, f'{kind}_NOT_OBSERVED', key)
        return table[key]

    def slice(self, p: Placement, artifact: str | None = None) -> bytes:
        need(self.candidate is not None, 'CANDIDATE_NOT_OBSERVED')
        require(isinstance(p, Placement) and isinstance(p.proof, Proof), 'PLACEMENT_TYPE_OR_PROOF', '')
        require(p.candidate_fingerprint == self.fp, 'STALE_PLACEMENT', p.artifact)
        require(artifact is None or p.artifact == artifact, 'PLACEMENT_WRONG_ARTIFACT', p.artifact)
        need(p.artifact in self.candidate.buffers, 'FINAL_ARTIFACT_NOT_OBSERVED', p.artifact)
        require(p.artifact_sha256 == self.candidate.hashes[p.artifact], 'PLACEMENT_ARTIFACT_HASH_MISMATCH', p.artifact)
        require(type(p.partition) is int and p.partition >= 0 and isinstance(p.span, Span), 'PLACEMENT_GEOMETRY', p.artifact)
        require(p.span.end <= len(self.candidate.buffers[p.artifact]), 'PLACEMENT_OUT_OF_BOUNDS', p.artifact)
        return self.candidate.buffers[p.artifact][p.span.start:p.span.end]

    def view(self, owner: str) -> OwnerView:
        v = self.get('VIEW', owner, self.views); o = self.c.owners[owner]
        data = self.slice(v.placement, 'EVENT:'+o['file'])
        require(v.placement.partition == o['partition'] and v.placement.unit == o['unit'], 'VIEW_OWNER_PARTITION_UNIT', owner)
        expected_mode = {'DELEGATED_GRAPH_OUTER':'DELEGATED_VIEW',
                         'SELECTED_REPLACEMENT_CANDIDATE':'MEMBER_VIEW',
                         'PRESERVATION_CANDIDATE':'PRESERVED_VIEW'}[o['draft_route']]
        require(v.mode == expected_mode, 'INDEPENDENT_OUTER_WRITE_OR_WRONG_VIEW_MODE', owner)
        require(v.extent_basis in ('ESTABLISHED_VIEW','EXACT_RECIPE_VIEW',
                                  'FROZEN_RELATION_VIEW','IDENTITY_ONLY'),
                'UNKNOWN_OWNER_EXTENT_BASIS', owner)
        if v.extent_basis == 'IDENTITY_ONLY':
            require(v.placement.span.size == 4 and v.recipe_placement is None,
                    'IDENTITY_ONLY_VIEW_CANNOT_CARRY_RANGE', owner)
        if v.extent_basis == 'EXACT_RECIPE_VIEW':
            require(v.recipe_placement == v.placement, 'EXACT_RECIPE_VIEW_MISMATCH', owner)
        if v.recipe_placement is not None:
            rp = v.recipe_placement; payload = self.slice(rp, v.placement.artifact)
            require(rp.partition == v.placement.partition and rp.unit == v.placement.unit
                    and rp.span.start == v.placement.span.start and rp.span.size >= 4
                    and rp.span.size % 4 == 0 and payload[:4] == bytes.fromhex(o['source_header_hex']),
                    'RECIPE_VIEW_IDENTITY_PARTITION_OR_ALIGNMENT', owner)
        require(v.placement.span.start % 4 == 0 and v.placement.span.size % 4 == 0 and
                data[:4] == bytes.fromhex(o['source_header_hex']), 'FINAL_VIEW_HEADER_OR_ALIGNMENT', owner)
        return v

    def recipe_view(self, owner: str) -> Placement:
        v = self.view(owner)
        if v.recipe_placement is not None:
            return v.recipe_placement
        # A header-only witness or a topology view is not payload authority.
        # Older callers can still submit their pre-existing explicit view.
        require(v.extent_basis == 'ESTABLISHED_VIEW', 'EXACT_RECIPE_VIEW_NOT_PROVISIONED', owner)
        return v.placement

    def range_view(self, owner: str, *, relation: bool = False) -> Placement:
        v = self.view(owner)
        require(v.extent_basis != 'IDENTITY_ONLY', 'IDENTITY_ONLY_IS_NOT_RANGE_AUTHORITY', owner)
        if relation:
            require(v.extent_basis in ('ESTABLISHED_VIEW','FROZEN_RELATION_VIEW'),
                    'FROZEN_RELATION_VIEW_NOT_PROVISIONED', owner)
        return v.placement

    def prepare(self, owner: str) -> PreparedRecipe:
        if owner in self.prep_errors:
            raise self.prep_errors[owner]
        if owner in self.prepared:
            return self.prepared[owner]
        try:
            ri = self.get('RECIPE', owner, self.inputs)
            p = prepare_recipe(self.e.im01.owners[owner], self.e.recipes.get(owner), ri.source, ri.pc)
            require(p.result.status == Status.PREPARED, 'IM01_PREPARATION_NOT_SATISFIED', p.result.reasons)
            aid = self.c.owners[owner]['applicability_obligation']
            if aid is not None:
                cr = self.c.apps[aid]['canonical_row']; pc = ri.pc; source = ri.source
                require(pc is not None and source is not None and
                        pc.span == Span(*cr['pc_ko_runtime_span']) and sha256(pc.data) == cr['pc_ko_runtime_bytes_sha256'] and
                        source.span == Span(*cr['source_runtime_span']) and sha256(source.data) == cr['source_runtime_bytes_sha256'],
                        'PREPARED_CANONICAL_APP_WINDOWS', owner)
                require(p.data == source.data[:4]+pc.data[4:], 'PREPARED_SOURCE_HEADER_PC_PAYLOAD', owner)
            self.prepared[owner] = p
            return p
        except ContractError as ex:
            self.prep_errors[owner] = ex
            raise

    def result(self, oid, fn) -> Receipt:
        if oid in self.receipts:
            return self.receipts[oid]
        try:
            if self.global_error is not None:
                raise self.global_error
            need(self.candidate is not None, 'CANDIDATE_NOT_OBSERVED')
            outcome, checks, deps, details = fn()
            r = Receipt(oid, ReceiptState.SATISFIED, outcome, self.fp, self.c.fingerprint,
                        tuple(checks), dependencies=tuple((d.obligation,d.fingerprint) for d in deps), details={**details,**self.provenance()})
        except _Missing as ex:
            r = Receipt(oid, ReceiptState.NOT_OBSERVED, 'NO_SUCCESS_CLAIM', self.fp, self.c.fingerprint,
                        reasons=(ex.code,), details={'detail':str(ex),**self.provenance()})
        except ContractError as ex:
            r = Receipt(oid, ReceiptState.BLOCKED, 'NO_SUCCESS_CLAIM', self.fp, self.c.fingerprint,
                        reasons=(ex.code,), details={'detail':str(ex),**self.provenance()})
        self.receipts[oid] = r
        return r

    def provenance(self) -> dict:
        return {'witness_set_sha256':self.witness_fp,
                'action_registry_sha256':self.e.rewrites.fingerprint,
                'input_recipe_registry_sha256':self.e.recipe_fingerprint}

    def dep(self, r: Receipt) -> Receipt:
        if r.state == ReceiptState.NOT_OBSERVED:
            raise _Missing('REQUIRED_RECEIPT_NOT_OBSERVED', r.obligation+':'+','.join(r.reasons))
        require(r.state == ReceiptState.SATISFIED and r.candidate_fingerprint == self.fp and
                r.catalog_fingerprint == self.c.fingerprint, 'REQUIRED_RECEIPT_BLOCKED_OR_STALE', r.obligation)
        return r

    def check_root(self, oid):
        def fn():
            r = self.c.roots[oid]['proof']; b = self.get('ROOT',oid,self.roots)
            require(b.block == r['block'] and type(b.block) is int and b.local == r['local'] and type(b.local) is int and
                    isinstance(b.locator_proof, Proof), 'ROOT_LOCATOR_IDENTITY', oid)
            # Placement authenticates the encoded candidate; its claimed range
            # must then equal the independently parsed message locator.
            self.slice(b.placement, 'TAI5MSG:FINAL')
            require(b.placement.partition == b.block and b.placement.unit is None,
                    'ROOT_BLOCK_PARTITION_OR_UNIT', oid)
            if self.serialized_roots is None:
                self.serialized_roots = SerializedRootValues(self.candidate.buffers['TAI5MSG:FINAL'])
            actual, structural = self.serialized_roots.value(b.block, b.local, b.placement.span)
            require(len(actual) == r['target_length'] and sha256(actual) == r['target_sha256'],
                    'ROOT_FINAL_VALUE_IDENTITY_MISMATCH', oid)
            return 'ROOT_VALUE_VERIFIED_LOCAL', ['ACTUAL_FINAL_DECODED_VALUE_SIZE_SHA256',
                    'PARSED_SERIALIZED_BLOCK_LOCAL_LOCATOR','SAME_CANDIDATE_ENCODED_ARTIFACT'], [], {
                'root':r['owner'],'sha256':sha256(actual),'size':len(actual),'final_range':[b.placement.span.start,b.placement.span.end],
                'locator_authority':b.locator_proof.document, 'structural_receipt':structural,
                'expected_decoded_size':r['target_length'], 'expected_decoded_sha256':r['target_sha256'],
                'value_encoding':'DECODED', 'final_range_encoding':'SERIALIZED',
                'claim':'PARSED_LOCATOR_AND_DECODED_VALUE_ONLY; semantic/caller and TAI5MSG-wide product acceptance remain external'}
        return self.result(oid,fn)

    def check_root_ref(self, oid):
        def fn():
            r = self.c.root_refs[oid]; root = self.dep(self.check_root('ROOT:'+r['root']))
            return 'EXACT_ROOT_REFERENCE_LINKED', ['EXACT_APP_OWNER_ROOT_JOIN','SAME_CANDIDATE_ROOT_RECEIPT'], [root], {
                'owner':r['owner'],'app_id':r['app_id'],'root':r['root']}
        return self.result(oid,fn)

    def check_occ(self, oid, visiting=frozenset()):
        def fn():
            require(oid not in visiting, 'DELEGATION_RECEIPT_CYCLE', oid)
            r = self.c.occurrences[oid]; a = self.c.apps[r['app_id']]; cr = a['canonical_row']; x = r['exact_occurrence']
            sub = self.get('OCC',oid,self.occs)
            require(sub.owner == r['owner'] and sub.pc_span == Span(x['escape_start'],x['literal_end']) and
                    isinstance(sub.action, Action), 'EXACT_OCCURRENCE_KEY_RANGE_OR_ACTION', oid)
            vp = self.recipe_view(sub.owner); p = self.prepare(sub.owner)
            actual = self.slice(sub.placement, vp.artifact)
            require(sub.placement.partition == vp.partition and sub.placement.unit == vp.unit and
                    vp.span.start+4 <= sub.placement.span.start < sub.placement.span.end <= vp.span.end,
                    'OCCURRENCE_OUTSIDE_FINAL_OWNER', oid)
            expected = x['escape'].encode('ascii')+bytes.fromhex(x['literal_hex'])
            pc0 = cr['pc_ko_runtime_span'][0]
            require(p.data is not None and p.data[sub.pc_span.start-pc0:sub.pc_span.end-pc0] == expected,
                    'EXACT_OCCURRENCE_PREIMAGE', oid)
            deps = []
            root = x.get('required_root')
            if root is not None:
                rootkey = root if isinstance(root,str) else root['owner']
                deps.append(self.dep(self.check_root_ref(f"ROOTREF:{a['source_line']}:{rootkey}")))
            child = self.c.delegate_occurrences.get(oid)
            if child is not None:
                require(sub.action == Action.DELEGATE and sub.delegate_to == child and sub.rewrite_id is None and sub.preservation_permit is None,
                        'EXACT_DELEGATION_REQUIRED', oid)
                deps.append(self.dep(self.check_occ(child, visiting | {oid})))
                cs = self.get('OCC',child,self.occs)
                require(cs.pc_span == sub.pc_span and cs.placement.artifact == sub.placement.artifact and
                        cs.placement.span == sub.placement.span and cs.placement.unit == sub.placement.unit,
                        'DELEGATION_FINAL_VIEW_MISMATCH', oid)
                require(a['unit'] is not None, 'DELEGATION_RESPONSIBILITY_MISSING', oid)
                # Child already checks exact output bytes and writer. Parent has
                # its own preparation, view and exact-occurrence receipt too.
                checks = ['UPSTREAM_DELEGATE_PREPARED','IDENTICAL_ABSOLUTE_OCCURRENCE', 'SAME_FINAL_RANGE_AND_UNIT']
            else:
                require(sub.delegate_to is None and sub.action != Action.DELEGATE, 'UNAUTHORIZED_DELEGATION', oid)
                checks = ['EXACT_OWNER_PC_OCCURRENCE_PREIMAGE','ACTUAL_FINAL_BYTES']
                if sub.action == Action.PRESERVE:
                    require(sub.rewrite_id is None, 'PRESERVATION_WITH_HIDDEN_REWRITE', oid)
                    need(sub.preservation_permit in self.e.rewrites.permits,
                         'EXPLICIT_PRESERVATION_DISPOSITION_NOT_PROVISIONED', oid)
                    permit = self.e.rewrites.permits[sub.preservation_permit]
                    require(permit.occurrence == oid and permit.recipe_id == p.recipe_id and
                            permit.before_sha256 == sha256(expected), 'PRESERVATION_PERMIT_SCOPE', oid)
                    checks.append('EXPLICIT_ACTION_DISPOSITION_NOT_JUST_UNCHANGED_BYTES')
                else:
                    require(sub.preservation_permit is None, 'TRANSFORM_WITH_EXTRA_PERMIT', oid)
                    need(sub.rewrite_id in self.e.rewrites.rules, 'APPROVED_EXACT_REWRITE_NOT_PROVISIONED', oid)
                    rule = self.e.rewrites.rules[sub.rewrite_id]
                    require(rule.occurrence == oid and rule.recipe_id == p.recipe_id and rule.before == expected and
                            rule.prepared_sha256 == p.data_sha256, 'REWRITE_SCOPE_OR_PREIMAGE_MISMATCH', oid)
                    require((sub.action == Action.NOOP) == (rule.before == rule.after), 'NOOP_TRANSFORM_DISPOSITION_MISMATCH', oid)
                    expected = rule.after
                    checks.append('EXPLICIT_EXACT_REWRITE_AUTHORITY_NOT_FAMILY_LABEL')
                require(actual == expected, 'OCCURRENCE_OUTPUT_BYTES_MISMATCH', oid)
            need(self.writer_index is not None, 'FINAL_WRITER_WITNESS_NOT_OBSERVED')
            writers = self.writer_index.cover(sub.placement.artifact,sub.placement.span,a['unit'])
            checks.append('UNIQUE_LOCAL_FINAL_WRITER')
            return sub.action.value, checks, deps, {'owner':sub.owner,'pc_range':[sub.pc_span.start,sub.pc_span.end],
                'final_range':[sub.placement.span.start,sub.placement.span.end], 'output_sha256':sha256(actual),
                'output_artifact_sha256':sub.placement.artifact_sha256,'writer_ids':writers,
                'rewrite_id':sub.rewrite_id,'delegate_to':sub.delegate_to,'preservation_permit':sub.preservation_permit}
        return self.result(oid,fn)

    def check_app(self, oid):
        def fn():
            a = self.c.apps[oid]; cr = a['canonical_row']; p = self.prepare(a['owner']); v = self.view(a['owner'])
            # Never trust the family string or missing/satisfied counters.
            deps = [self.dep(self.check_occ(o)) for o in a['occurrence_ids']]
            deps += [self.dep(self.check_root_ref(f"ROOTREF:{a['source_line']}:{key}")) for key in a['required_root_refs']]
            projections = [self.occs[o].placement.span for o in a['occurrence_ids']]
            original = [self.c.occurrences[o]['exact_occurrence'] for o in a['occurrence_ids']]
            order = sorted(range(len(original)),key=lambda i:original[i]['escape_start'])
            require(all(projections[i].end <= projections[j].start for i,j in zip(order,order[1:])),
                    'FINAL_OCCURRENCE_ORDER_OR_ALIAS_CONFLICT', oid)
            require(p.source_span == Span(*cr['source_runtime_span']) and v.placement.unit == a['unit'],
                    'APP_SOURCE_OR_UNIT', oid)
            return 'APP_APPLICABLE_OBLIGATIONS_SATISFIED_LOCAL', ['EXACT_UPSTREAM_RECIPE','EVERY_OCCURRENCE_RECEIPT',
                'REQUIRED_ROOT_RECEIPTS','OCCURRENCE_IDENTITY_ORDER','SOURCE_STRUCTURAL_HEADER'], deps, {
                'owner':a['owner'],'occurrences':len(projections),'root_refs':len(a['required_root_refs']),
                'scope':'APPLICABILITY_ONLY_NOT_COMPLETE_OWNER_PAYLOAD_OR_GLOBAL_LAYOUT_ACCEPTANCE'}
        return self.result(oid,fn)

    def region(self, unit: str, cluster: str) -> UnitRegion:
        region = self.get('REGION',cluster,self.regions)
        require(region.unit == unit and cluster in self.c.units[unit]['cluster_ids'] and region.placement.unit == unit,
                'REGION_CANONICAL_RESPONSIBILITY', cluster)
        self.slice(region.placement, 'EVENT:'+self.c.units[unit]['file'])
        return region

    def check_relation(self, oid):
        def fn():
            r = self.c.relations[oid]; e = r['canonical_edge']; u = r['unit']
            a = self.range_view(e['outer_owner'], relation=True)
            b = self.range_view(e['inner_owner'], relation=True)
            region = self.region(u,e['cluster_id']).placement
            require(a.artifact == b.artifact == region.artifact and a.unit == b.unit == u and
                    a.partition == b.partition == region.partition, 'RELATION_PARTITION_OR_UNIT_MISMATCH', oid)
            sa,sb = a.span,b.span; kind = e['source_relation_type']; inter = overlap(sa,sb)
            require(inter is not None, 'RELATION_LOST_OVERLAP', oid)
            if kind == 'SHARED_END_SUFFIX':
                require(sa.start < sb.start and sa.end == sb.end, 'RELATION_SHARED_END_CHANGED', oid)
            elif kind == 'STRICT_CONTAINMENT':
                require(sa.start < sb.start and sb.end < sa.end, 'RELATION_CONTAINMENT_CHANGED', oid)
            elif kind == 'PARTIAL_OVERLAP':
                require(sa.start < sb.start < sa.end < sb.end, 'RELATION_PARTIAL_OVERLAP_CHANGED', oid)
            else:
                raise ContractError('UNSUPPORTED_FROZEN_RELATION', kind)
            union = Span(min(sa.start,sb.start),max(sa.end,sb.end))
            require(region.span.start <= union.start and union.end <= region.span.end, 'RELATION_UNION_TRUNCATED', oid)
            need(self.writer_index is not None, 'FINAL_WRITER_WITNESS_NOT_OBSERVED')
            writers = self.writer_index.cover(a.artifact, union, u)
            return 'RELATION_AND_UNIT_SATISFIED_LOCAL', ['EXACT_CANONICAL_EDGE','FINAL_VIEW_HEADERS',
                'RELATION_TOPOLOGY','FULL_UNION_NOT_OUTER_ENDPOINT','UNIQUE_CANONICAL_UNIT_WRITERS'], [], {
                'edge_id':e['edge_id'],'unit':u,'cluster':e['cluster_id'],'relation_type':kind,
                'source_overlap_retained_as_provenance':list(e['source_overlap_range']),
                'final_overlap':[inter.start,inter.end],'final_union':[union.start,union.end],
                'writer_ids':writers,'claim':'LOCAL_RELATION; individual consumer and full layout gates remain separate'}
        return self.result(oid,fn)

    def check_support(self, oid):
        def fn():
            r = self.c.supports[oid]; c = r['canonical_support']; owner = c['node_id']; u = r['unit']
            sub = self.get('SUP',oid,self.supports); o = self.c.owners[owner]
            require(sub.owner == owner and sub.source_span == Span(*c['source_runtime_span']), 'SUPPORT_EXACT_SOURCE_KEY', oid)
            actual = self.slice(sub.placement,'EVENT:'+o['file'])
            require(sub.placement.partition == o['partition'] and sub.placement.unit == u,
                    'SUPPORT_PARTITION_OR_UNIT', oid)
            need(self.candidate is not None, 'CANDIDATE_NOT_OBSERVED')
            source_key = 'STOCK:'+o['file']
            need(source_key in self.candidate.buffers, 'PRESERVATION_SOURCE_NOT_OBSERVED', oid)
            need(o['file'] in self.e.stock_hashes, 'SOURCE_FILE_IDENTITY_AUTHORITY_NOT_PROVISIONED', oid)
            require(self.candidate.hashes[source_key] == self.e.stock_hashes[o['file']], 'PRESERVATION_SOURCE_IDENTITY', oid)
            source = self.candidate.buffers[source_key]
            require(sub.source_span.end <= len(source), 'SUPPORT_SOURCE_BOUNDS', oid)
            expected = source[sub.source_span.start:sub.source_span.end]
            require(len(actual) == len(expected) and actual == expected, 'SUPPORT_PROTECTED_BYTES_CHANGED', oid)
            region = self.region(u,c['cluster_id']).placement
            require(region.artifact == sub.placement.artifact and region.partition == sub.placement.partition,
                    'SUPPORT_REGION_IDENTITY', oid)
            need(self.writer_index is not None, 'FINAL_WRITER_WITNESS_NOT_OBSERVED')
            self.writer_index.cover(sub.placement.artifact,sub.placement.span)
            if c['role'] == 'NON_KOREAN_EXTERNAL_HEADER_OVERLAP':
                v = self.range_view(c['overlapped_node'])
                inter = overlap(sub.placement.span,v.span)
                require(inter is not None and inter == Span(v.span.start,v.span.start+4),
                        'SUPPORT_EXTERNAL_HEADER_BOUNDARY_CHANGED', oid)
                require(region.span.start <= inter.start and inter.end <= region.span.end, 'SUPPORT_EXTERNAL_UNION', oid)
                self.writer_index.cover(sub.placement.artifact,inter,u)
            else:
                require(region.span.start <= sub.placement.span.start and sub.placement.span.end <= region.span.end,
                        'SUPPORT_INSIDE_UNION_BOUNDARY_CHANGED', oid)
                self.writer_index.cover(sub.placement.artifact,sub.placement.span,u)
            return 'SUPPORT_BYTES_PRESERVED_LOCAL', ['CANONICAL_NON_KOREAN_BOUNDARY','ACTUAL_SOURCE_FILE_IDENTITY',
                'EXACT_PROTECTED_BYTES','EXACT_SUPPORT_FORM','LOCAL_WRITER_RESPONSIBILITY'], [], {
                'owner':owner,'unit':u,'support_form':c['role'],'size':len(actual),'sha256':sha256(actual),
                'source_range':[sub.source_span.start,sub.source_span.end],
                'final_range':[sub.placement.span.start,sub.placement.span.end]}
        return self.result(oid,fn)

    def run(self) -> BatchReport:
        for oid in self.c.roots: self.check_root(oid)
        for oid in self.c.root_refs: self.check_root_ref(oid)
        for oid in self.c.occurrences: self.check_occ(oid)
        for oid in self.c.apps: self.check_app(oid)
        for oid in self.c.relations: self.check_relation(oid)
        for oid in self.c.supports: self.check_support(oid)
        require(set(self.receipts) == self.c.ids, 'INTERNAL_RECEIPT_ACCOUNTING_GAP', '')
        return BatchReport(tuple(self.receipts[k] for k in sorted(self.c.ids)), tuple(self.errors),
                           self.c.fingerprint,self.fp,self.e.rewrites.fingerprint,self.c.ids)
