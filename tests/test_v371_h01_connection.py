"""Bounded H01 release tests.  No generic interior-recipe permission is granted."""
from dataclasses import replace
import unittest

from builder.selective_event_contracts import (
    ContractError, FieldContract, FieldState, FinalFieldAnchors,
    InteriorFieldBinding, OwnerContract, Proof, RecipeContract, RecipeKind,
    RegionAuthority, ReviewedInteriorRecipe, Route, Span, Status, Window,
    prepare_recipe, sha256,
)
from builder.selective_event_final_layout import FieldSlot
from builder.selective_event_relocation_adapter import ReviewedFieldRule

P=Proof('SYNTHETIC_H01_TEST',sha256(b'h01-test'),'TEST_ONLY_NOT_PRODUCTION_AUTHORITY',1)
OWNER='fixture.TS5:0'; RECIPE='R:'+OWNER; FIELD='fixture.TS5:4'
HEADER=bytes.fromhex('15010000')
WORD=bytes.fromhex('04010800')
PAYLOAD=HEADER+WORD+bytes.fromhex('11000000')
SOURCE=Window('stock:fixture.TS5',Span(0,12),PAYLOAD)
PC=Window('pc:fixture.TS5',Span(32,44),PAYLOAD)
OWNER_CONTRACT=OwnerContract(OWNER,'fixture.TS5',0,Span(0,12),HEADER,Route.DIRECT,P,
                             'EXACT_TEST_RECIPE',RECIPE,holds=('H01',))
RECIPE_CONTRACT=RecipeContract(OWNER,RECIPE,RecipeKind.DIRECT,SOURCE.asset,
    RegionAuthority(SOURCE.span,sha256(PAYLOAD),P),P,HEADER,PC.asset,
    RegionAuthority(PC.span,sha256(PAYLOAD),P),HEADER)
BINDING=InteriorFieldBinding(FIELD,Span(4,8),4,sha256(WORD),8,'PC_EDITOR04',0,None)
INTERIOR=ReviewedInteriorRecipe(OWNER,RECIPE,SOURCE.span,sha256(PAYLOAD),PC.span,
    sha256(PAYLOAD),sha256(PAYLOAD),True,(BINDING,),P)
FIELD_CONTRACT=FieldContract(FIELD,Span(4,8),WORD,8,0,None,FieldState.CONTEXT,P,
    ('A:FIELD','A:TARGET','ROLE_POLICY:'+FIELD),interior_recipe_ids=(RECIPE,))
RULE=ReviewedFieldRule(FIELD,'PC_EDITOR04',sha256(WORD),8,0,None,0,P)
ANCHORS=FinalFieldAnchors(FIELD,4,8,4,8,8,0,0,0,None,P)


class ReviewedInteriorRecipeTests(unittest.TestCase):
    def test_h01_stays_blocked_without_exact_contract(self):
        self.assertEqual(prepare_recipe(OWNER_CONTRACT,RECIPE_CONTRACT,SOURCE,PC).result.reasons,
                         ('H01_EXACT_INTERIOR_RECIPE_AND_WRITER_REQUIRED',))

    def test_exact_identity_parent_prepares(self):
        result=prepare_recipe(OWNER_CONTRACT,RECIPE_CONTRACT,SOURCE,PC,INTERIOR)
        self.assertEqual(result.result.status,Status.PREPARED)
        self.assertEqual(result.data,PAYLOAD)
        self.assertTrue(result.result.details['reviewed_interior_identity_contract'])

    def test_changed_pc_or_parent_hash_does_not_release_h01(self):
        bad=replace(INTERIOR,pc_sha256=sha256(b'other'))
        self.assertEqual(prepare_recipe(OWNER_CONTRACT,RECIPE_CONTRACT,SOURCE,PC,bad).result.reasons,
                         ('H01_REVIEWED_RECIPE_BOUNDARY_OR_HASH',))

    def test_identity_slot_coordinates_are_exact(self):
        INTERIOR.validate_directive(PAYLOAD,(FieldSlot(FIELD,Span(4,8),4,P),))
        with self.assertRaisesRegex(ContractError,'EXACT_INTERIOR_SLOT_SET'):
            INTERIOR.validate_directive(PAYLOAD,(FieldSlot(FIELD,Span(4,8),8,P),))

    def test_reviewed_field_rule_needs_parent_contract(self):
        with self.assertRaisesRegex(ContractError,'H01_INTERIOR_ROLE'):
            RULE.propose(FIELD_CONTRACT,ANCHORS)
        self.assertEqual(RULE.propose(FIELD_CONTRACT,ANCHORS,INTERIOR),WORD)

    def test_wrong_codec_or_target_cannot_borrow_parent_contract(self):
        with self.assertRaisesRegex(ContractError,'H01_REVIEWED_FIELD_RULE_SCOPE'):
            replace(RULE,codec='SPECIAL04').propose(FIELD_CONTRACT,ANCHORS,INTERIOR)
        bad_contract=replace(FIELD_CONTRACT,source_target=12)
        bad_rule=replace(RULE,source_target=12)
        bad_anchors=replace(ANCHORS,source_target=12,final_target=12)
        with self.assertRaisesRegex(ContractError,'H01_REVIEWED_FIELD_CONTRACT_SCOPE'):
            bad_rule.propose(bad_contract,bad_anchors,INTERIOR)

    def test_unrelated_owner_cannot_use_reviewed_contract(self):
        other=replace(OWNER_CONTRACT,owner='fixture.TS5:C',observed_span=Span(12,24),recipe_id='R:fixture.TS5:C')
        self.assertEqual(prepare_recipe(other,RECIPE_CONTRACT,SOURCE,PC,INTERIOR).result.reasons,
                         ('RECIPE_OWNER_OR_BINDING_MISMATCH',))


if __name__=='__main__':unittest.main()
