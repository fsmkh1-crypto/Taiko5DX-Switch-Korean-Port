"""Synthetic extent/identity regressions; no actual-game authority is invented."""
from dataclasses import replace
from unittest.mock import patch
import struct
import unittest

from builder.selective_event_contracts import (
    ConsumerContract, ContractError, OwnerContract, Proof, ProtectedRange,
    RecipeContract, RecipeKind, RegionAuthority, Route, Span, sha256,
)
from builder.selective_event_contract_catalog import ContractCatalog, PLAN_SHA256
from builder.selective_event_final_layout import FinalLayout, SourceIdentity
from builder.selective_event_obligation_catalog import ObligationCatalog, freeze
from builder.selective_event_obligation_receipts import (
    ObligationEngine, ReceiptState, _Evaluation,
)
from builder.selective_event_overlap import FileRequest, IntegratedSerializer
from test_selective_event_role_policy import fixture as app_fixture, OWNER as APP_OWNER

P = Proof('SYNTHETIC_V371_OWNER_EXTENT', sha256(b'owner extent regression'),
          'TEST_ONLY_NOT_CANONICAL_AUTHORITY')
F = 'EXTENT.TS5'
K = F + ':20'
H = bytes.fromhex('11010000')


def fixture(route=Route.PRESERVE, *, observed_end=44, recipe_end=36,
            consumer=False, bad_consumer=False, relation=False, crossing_relation=False):
    source = bytearray(b'EXT!' + struct.pack('<IIII', 2, 20, 36, 64) + b'Z' * 44)
    source[32:36] = H
    source[24:28] = H
    source = bytes(source)
    specs = [(K, 32, observed_end, route)]
    if relation:
        end = 44 if crossing_relation else 36
        specs = [(F + ':18', 24, end, Route.PRESERVE), (K, 32, end, Route.PRESERVE)]
    owners = {}; raw = {}; recipes = {}; assets = {}
    for key, start, end, rt in specs:
        unit = 'T01' if relation else None
        rid = None if rt == Route.PRESERVE else 'R:' + key
        o = OwnerContract(key, F, 0, Span(start, end), source[start:start+4], rt,
                          P, 'SYNTHETIC_EXACT_BOUNDARY', rid, unit)
        owners[key] = o
        raw[key] = {'owner': key, 'file': F, 'partition': 0, 'unit': unit,
                    'draft_route': rt.value, 'source_header_hex': o.source_header.hex(),
                    'applicability_obligation': None}
        if rid is not None:
            data = source[start:recipe_end]
            recipes[key] = RecipeContract(key, rid, RecipeKind.DIRECT, 'stock:' + F,
                RegionAuthority(Span(start, recipe_end), sha256(data), P), P, o.source_header,
                'pc:' + key, RegionAuthority(Span(0, len(data)), sha256(data), P), o.source_header)
            assets['pc:' + key] = data
    consumers = {}
    if consumer:
        expected = source[32:44]
        if bad_consumer:
            expected = expected[:8] + b'FAIL'
        c = ConsumerContract('FULL_CONSUMER', K, 'EXPLICIT_PROTECTED_VIEW', 'TEST_PARENT',
                             (ProtectedRange('FULL', Span(32, 44), expected, P),), P)
        consumers[c.id] = c
    relations = {}; units = {}
    if relation:
        relations['REL:TEST'] = {'unit': 'T01', 'canonical_edge': {
            'edge_id': 'TEST', 'outer_owner': F + ':18', 'inner_owner': K, 'cluster_id': 'C01',
            'source_relation_type': 'SHARED_END_SUFFIX', 'source_overlap_range': [32, 36]}}
        units['T01'] = {'file': F, 'cluster_ids': ['C01']}
    im = ContractCatalog(owners, {}, consumers, [], PLAN_SHA256, {})
    oc = ObligationCatalog(freeze({}), freeze({}), freeze(relations), freeze({}), freeze({}),
                           freeze({}), freeze(units), freeze(raw), freeze({}), (),
                           sha256(b'SYNTHETIC_EXTENT_CATALOG'))
    co = IntegratedSerializer(im, ObligationEngine(oc, im, recipes))
    q = FileRequest(F, source, SourceIdentity(F, len(source), sha256(source), P), assets)
    return co, q


def run(co, q):
    return co.run((q,), run_id='SYNTHETIC_EXTENT_REGRESSION')


class OwnerExtentTests(unittest.TestCase):
    def test_preservation_observation_crossing_partition_is_not_runtime_extent(self):
        co, q = fixture(); r = run(co, q); f = r.files[0]
        self.assertTrue(f.local_complete, f.summary())
        self.assertEqual(f.owner_identity_spans[K], Span(32, 36))
        self.assertNotIn(K, f.owner_recipe_spans)
        self.assertEqual(r.evidence.owner_views[0].extent_basis, 'IDENTITY_ONLY')
        self.assertEqual(f.assembled.data, q.source)

    def test_direct_uses_exact_recipe_not_longer_observation(self):
        co, q = fixture(Route.DIRECT); f = run(co, q).files[0]
        self.assertTrue(f.local_complete, f.summary())
        self.assertEqual(f.owner_recipe_spans[K], Span(32, 36))

    def test_delegate_uses_exact_recipe_not_longer_observation(self):
        co, q = fixture(Route.DELEGATE); r = run(co, q); f = r.files[0]
        self.assertTrue(f.local_complete, f.summary())
        self.assertEqual(f.owner_recipe_spans[K], Span(32, 36))
        self.assertEqual(r.evidence.owner_views[0].mode, 'DELEGATED_VIEW')
        self.assertFalse(any(j.kind == 'PREPARED_PAYLOAD' for j in f.assembled.journal))

    def test_delegate_missing_recipe_remains_blocked(self):
        co, q = fixture(Route.DELEGATE)
        co = IntegratedSerializer(co.catalog, ObligationEngine(co.engine.catalog, co.catalog, {}))
        self.assertFalse(run(co, q).files[0].local_complete)

    def test_real_recipe_crossing_partition_remains_blocked(self):
        for route in (Route.DIRECT, Route.DELEGATE):
            with self.subTest(route=route):
                co, q = fixture(route, recipe_end=44); f = run(co, q).files[0]
                self.assertFalse(f.local_complete)
                self.assertIn('EXACT_RECIPE_CROSSES_PARTITION', [x for a in f.attempts for x in a.reasons])

    def test_wrong_identity_partition_remains_blocked(self):
        co, q = fixture(); o = replace(co.catalog.owners[K], partition=1)
        co.catalog.owners[K] = o; co.owners_by_file[F][K] = o
        self.assertFalse(run(co, q).files[0].local_complete)

    def test_wrong_identity_header_remains_blocked(self):
        co, q = fixture(); o = replace(co.catalog.owners[K], source_header=b'FAIL')
        co.catalog.owners[K] = o; co.owners_by_file[F][K] = o
        self.assertFalse(run(co, q).files[0].local_complete)

    def test_identity_mapping_cannot_be_unaligned(self):
        co, q = fixture(); original = FinalLayout.anchor
        def wrong(layout, offset):
            return 33 if offset == 32 else original(layout, offset)
        with patch.object(FinalLayout, 'anchor', wrong):
            f = run(co, q).files[0]
        self.assertFalse(f.local_complete)
        self.assertIn('FINAL_OWNER_IDENTITY_WIDTH_OR_ALIGNMENT', [x for a in f.attempts for x in a.reasons])

    def test_consumer_range_not_truncated_to_identity(self):
        co, q = fixture(consumer=True); f = run(co, q).files[0]
        self.assertTrue(f.local_complete, f.summary())
        self.assertEqual(co.catalog.consumers['FULL_CONSUMER'].ranges[0].source_span, Span(32, 44))
        self.assertTrue(any(a.operation == 'VIEW:FULL_CONSUMER' for a in f.attempts))

    def test_consumer_mismatch_after_identity_still_blocks(self):
        co, q = fixture(consumer=True, bad_consumer=True); f = run(co, q).files[0]
        self.assertFalse(f.local_complete)
        self.assertTrue(any(a.operation == 'VIEW:FULL_CONSUMER' and a.reasons for a in f.attempts))

    def test_relation_views_and_union_are_not_shrunk(self):
        co, q = fixture(relation=True); r = run(co, q); f = r.files[0]
        self.assertTrue(r.complete_local_pipeline, r.summary())
        self.assertEqual(f.owner_relation_spans[F + ':18'], Span(24, 36))
        self.assertEqual(f.owner_identity_spans[F + ':18'], Span(24, 28))
        self.assertEqual(r.evidence.unit_regions[0].placement.span, Span(24, 36))
        self.assertEqual(r.obligations.receipts[0].state, ReceiptState.SATISFIED)

    def test_genuine_relation_union_crossing_partition_stays_blocked(self):
        co, q = fixture(relation=True, crossing_relation=True)
        self.assertFalse(run(co, q).files[0].local_complete)

    def test_identity_only_cannot_authorize_relation(self):
        co, q = fixture(relation=True); r = run(co, q)
        views = tuple(replace(v, extent_basis='IDENTITY_ONLY',
                      placement=replace(v.placement, span=Span(v.placement.span.start, v.placement.span.start+4)))
                      for v in r.evidence.owner_views)
        receipt = co.engine.check_one('REL:TEST', replace(r.evidence, owner_views=views))
        self.assertEqual(receipt.state, ReceiptState.BLOCKED)
        self.assertIn('IDENTITY_ONLY_IS_NOT_RANGE_AUTHORITY', receipt.reasons)

    def test_identity_only_cannot_authorize_support_range(self):
        co, q = fixture(); r = run(co, q)
        with self.assertRaisesRegex(ContractError, 'IDENTITY_ONLY_IS_NOT_RANGE_AUTHORITY'):
            _Evaluation(co.engine, r.evidence).range_view(K)

    def test_final_table_remains_last_writer(self):
        co, q = fixture(); f = run(co, q).files[0]
        self.assertEqual(f.assembled.journal[-1].writer, 'FINAL_TABLE')
        self.assertTrue(f.assembled.audit.local_complete)

    def test_no_product_acceptance_or_export(self):
        co, q = fixture(); r = run(co, q)
        self.assertFalse(r.product_accepted)
        with self.assertRaisesRegex(ContractError, 'VAL01'):
            r.emit_product()


class IM02ExtentBridgeTests(unittest.TestCase):
    def app(self):
        im, engine, q = app_fixture()
        co = IntegratedSerializer(im, engine)
        return engine, run(co, q)

    def test_exact_recipe_placement_reaches_occurrence_check(self):
        e, r = self.app(); v = next(v for v in r.evidence.owner_views if v.owner == APP_OWNER)
        self.assertEqual(v.extent_basis, 'EXACT_RECIPE_VIEW')
        self.assertEqual(v.recipe_placement, v.placement)
        self.assertEqual(e.check_one('OCC:1:0', r.evidence).state, ReceiptState.SATISFIED)

    def test_header_only_source_recipe_growth_keeps_four_byte_identity(self):
        im, e, q = app_fixture(grow=True)
        # Reuse the existing reviewed synthetic nonidentity field rule by the
        # actual role-policy fixture; this test needs only the bounded file gate.
        from test_selective_event_role_policy import policy, FIELD, FieldPolicyCategory
        field_policy = policy(im.fields[FIELD], FieldPolicyCategory.GENERIC_REENCODE,
                              16, bytes.fromhex('04012000'), True)
        r = run(IntegratedSerializer(im, e, field_policy), q)
        f = r.files[0]
        self.assertTrue(f.local_complete, f.summary())
        key = 'TEST.TS5:2C'
        self.assertEqual(f.owner_identity_spans[key], Span(44, 48))
        self.assertEqual(f.owner_recipe_spans[key], Span(44, 56))

    def test_identity_only_cannot_discharge_occurrence(self):
        e, r = self.app()
        views = tuple(replace(v, extent_basis='IDENTITY_ONLY', recipe_placement=None,
                      placement=replace(v.placement, span=Span(v.placement.span.start, v.placement.span.start+4)))
                      if v.owner == APP_OWNER else v for v in r.evidence.owner_views)
        x = e.check_one('OCC:1:0', replace(r.evidence, owner_views=views))
        self.assertEqual(x.state, ReceiptState.BLOCKED)
        self.assertIn('EXACT_RECIPE_VIEW_NOT_PROVISIONED', x.reasons)

    def test_relation_range_without_recipe_cannot_discharge_occurrence(self):
        e, r = self.app()
        views = tuple(replace(v, extent_basis='FROZEN_RELATION_VIEW', recipe_placement=None)
                      if v.owner == APP_OWNER else v for v in r.evidence.owner_views)
        x = e.check_one('OCC:1:0', replace(r.evidence, owner_views=views))
        self.assertEqual(x.state, ReceiptState.BLOCKED)
        self.assertIn('EXACT_RECIPE_VIEW_NOT_PROVISIONED', x.reasons)

    def test_occurrence_uses_recipe_range_not_shorter_relation_range(self):
        e, r = self.app()
        views = tuple(replace(v, extent_basis='FROZEN_RELATION_VIEW',
                      placement=replace(v.placement, span=Span(v.placement.span.start, v.placement.span.start+4)))
                      if v.owner == APP_OWNER else v for v in r.evidence.owner_views)
        x = e.check_one('OCC:1:0', replace(r.evidence, owner_views=views))
        self.assertEqual(x.state, ReceiptState.SATISFIED, x)

    def test_recipe_extent_cannot_silently_shrink(self):
        e, r = self.app()
        views = []
        for v in r.evidence.owner_views:
            if v.owner == APP_OWNER:
                rp = replace(v.placement, span=Span(v.placement.span.start, v.placement.span.start+4))
                v = replace(v, placement=rp, recipe_placement=rp)
            views.append(v)
        x = e.check_one('OCC:1:0', replace(r.evidence, owner_views=tuple(views)))
        self.assertEqual(x.state, ReceiptState.BLOCKED)
        self.assertIn('OCCURRENCE_OUTSIDE_FINAL_OWNER', x.reasons)

    def test_stale_recipe_placement_rejected(self):
        e, r = self.app()
        views = tuple(replace(v, extent_basis='FROZEN_RELATION_VIEW',
                      recipe_placement=replace(v.recipe_placement, candidate_fingerprint='0'*64))
                      if v.owner == APP_OWNER else v for v in r.evidence.owner_views)
        x = e.check_one('OCC:1:0', replace(r.evidence, owner_views=views))
        self.assertEqual(x.state, ReceiptState.BLOCKED)
        self.assertIn('STALE_PLACEMENT', x.reasons)

    def test_wrong_recipe_unit_rejected(self):
        e, r = self.app()
        views = tuple(replace(v, extent_basis='FROZEN_RELATION_VIEW',
                      recipe_placement=replace(v.recipe_placement, unit='T99'))
                      if v.owner == APP_OWNER else v for v in r.evidence.owner_views)
        x = e.check_one('OCC:1:0', replace(r.evidence, owner_views=views))
        self.assertEqual(x.state, ReceiptState.BLOCKED)
        self.assertIn('RECIPE_VIEW_IDENTITY_PARTITION_OR_ALIGNMENT', x.reasons)

    def test_missing_occurrence_action_stays_missing(self):
        im, e, q = app_fixture(); r = run(IntegratedSerializer(im, e), replace(q, occurrence_actions=()))
        self.assertFalse(r.obligations.local_complete)

    def test_unknown_extent_basis_fails_closed(self):
        e, r = self.app()
        views = tuple(replace(v, extent_basis='AD_HOC_OVERRIDE') if v.owner == APP_OWNER else v
                      for v in r.evidence.owner_views)
        x = e.check_one('OCC:1:0', replace(r.evidence, owner_views=views))
        self.assertEqual(x.state, ReceiptState.BLOCKED)
        self.assertIn('UNKNOWN_OWNER_EXTENT_BASIS', x.reasons)


if __name__ == '__main__':
    unittest.main()
