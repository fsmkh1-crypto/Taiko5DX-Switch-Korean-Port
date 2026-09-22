"""Self-contained regression tests for the V371 role-aware field adapter.

These fixtures are synthetic.  The full 24,305-row ledger validation is kept in
V371's external validation package and is not replaced by these tests.
"""
from __future__ import annotations

from dataclasses import replace
import struct
import unittest

from builder.selective_event_contract_catalog import ContractCatalog, PLAN_SHA256
from builder.selective_event_contracts import (
    ConsumerContract, FieldContract, FieldState, OwnerContract, Proof,
    ProtectedRange, RecipeContract, RecipeKind, RegionAuthority, Route, Span,
    sha256,
)
from builder.selective_event_field_policy import (
    FieldPolicyCatalog, FieldPolicyCategory, FieldPolicyEntry,
)
from builder.selective_event_final_layout import SourceIdentity
from builder.selective_event_obligation_catalog import ObligationCatalog, freeze
from builder.selective_event_obligation_receipts import (
    Action, ObligationEngine, PreservationPermit, RewriteRegistry,
)
from builder.selective_event_overlap import (
    FileRequest, IntegratedSerializer, OccurrenceAction,
)
from builder.selective_event_relocation_adapter import ReviewedFieldRule

P=Proof('SYNTHETIC_V371_FIELD_POLICY_TEST',sha256(b'v371-field-policy-test'),
        'TEST_ONLY_NOT_CANONICAL_AUTHORITY',1)
FILE='TEST.TS5'; OWNER=FILE+':10'; SCALAR=FILE+':30'; EXTRA=FILE+':2C'; FIELD=FILE+':28'
HEAD=b'\x11\0\0\0'; BEFORE=b'\\#07F0A'; PC=HEAD+BEFORE+b'\0'*5


def source_image():
    body=bytearray(b'\0'*80)
    body[0:16]=HEAD+b'JP_ORIGINAL\0'
    body[24:28]=(0x104|(2<<19)).to_bytes(4,'little')
    body[28:32]=b'\x11\x03\0\0';body[32:36]=b'\x11\0\x28\x0d'
    return b'TEST'+struct.pack('<III',1,16,96)+bytes(body)


def fixture(*,grow=False,state=FieldState.CONTEXT,contact_prefix='CONTACT:O:'):
    source=source_image();owners={};rawowners={};recipes={}
    def add(key,start,end,route,pc=None):
        o=OwnerContract(key,FILE,0,Span(start,end),source[start:start+4],route,P,'TEST_BOUNDARY',
                        None if route==Route.PRESERVE else 'R:'+key)
        owners[key]=o
        rawowners[key]={'owner':key,'file':FILE,'partition':0,'unit':None,
            'draft_route':route.value,'source_header_hex':o.source_header.hex(),
            'applicability_obligation':'APP:1' if key==OWNER else None}
        if route!=Route.PRESERVE:
            recipes[key]=RecipeContract(key,o.recipe_id,RecipeKind.DIRECT,'stock:'+FILE,
                RegionAuthority(Span(start,end),sha256(source[start:end]),P),P,o.source_header,
                'pc:'+key,RegionAuthority(Span(0,len(pc)),sha256(pc),P),o.source_header)
    add(OWNER,16,32,Route.DIRECT,PC);add(SCALAR,48,56,Route.PRESERVE)
    if grow:add(EXTRA,44,48,Route.DIRECT,source[44:48]+b'GROW'*2)
    consumer=ConsumerContract('SCALAR_VIEW',SCALAR,'CONDITIONAL_VALUE_OPERAND','TEST_PARENT',
        (ProtectedRange('VALUE',Span(48,52),source[48:52],P),),P)
    deps=('A:'+FILE+':28','A:'+FILE+':30','A:'+FILE+':2C',contact_prefix+SCALAR,'ROLE_POLICY:'+FIELD)
    field=FieldContract(FIELD,Span(40,44),source[40:44],48,0,None,state,P,deps,
        (ProtectedRange('VALUE',Span(48,52),source[48:52],P),),('SCALAR_VIEW',))
    catalog=ContractCatalog(owners,{FIELD:field},{consumer.id:consumer},[],PLAN_SHA256,{})
    exact={'escape_start':4,'escape_end':10,'literal_start':10,'literal_end':11,
           'escape':'\\#07F0','literal_hex':'41','required_root':None}
    canonical={'file':FILE,'source_file_sha256':sha256(source),'source_runtime_span':[16,32],
        'pc_ko_runtime_span':[0,16],'source_runtime_bytes_sha256':sha256(source[16:32]),
        'pc_ko_runtime_bytes_sha256':sha256(PC),'partition_index':0}
    apps={'APP:1':{'owner':OWNER,'canonical_row':canonical,'unit':None,'source_line':1,
                   'occurrence_ids':['OCC:1:0'],'required_root_refs':[]}}
    occ={'OCC:1:0':{'owner':OWNER,'app_id':'APP:1','exact_occurrence':exact}}
    obligations=ObligationCatalog(freeze(apps),freeze(occ),freeze({}),freeze({}),freeze({}),
        freeze({}),freeze({}),freeze(rawowners),freeze({}),(),sha256(b'TEST_CATALOG'))
    permit=PreservationPermit('TEST_PRESERVE','OCC:1:0','R:'+OWNER,sha256(BEFORE),P)
    engine=ObligationEngine(obligations,catalog,recipes,RewriteRegistry(permits=(permit,)))
    assets={'pc:'+OWNER:PC}
    if grow:assets['pc:'+EXTRA]=source[44:48]+b'GROW'*2
    request=FileRequest(FILE,source,SourceIdentity(FILE,len(source),sha256(source),P),assets,
        occurrence_actions=(OccurrenceAction('OCC:1:0',Action.PRESERVE,
                            preservation_permit='TEST_PRESERVE'),))
    return catalog,engine,request


def policy(contract,category,final_span,output,changed):
    entry=FieldPolicyEntry(contract.field,FILE,contract.source_span.start,contract.source_header,
        contract.source_header[0],contract.source_target-contract.source_span.start,0,None,category,
        'GENERIC_PC_EDITOR_PLAN',changed,contract.source_span.start,
        contract.source_span.start+final_span,final_span,output,'TEST_WRITER',
        'TEST ORDER; PARTITION TABLE FINAL','TEST',(),P)
    return FieldPolicyCatalog({FIELD:entry},sha256(b'test-policy'),1,'SYNTHETIC')


class RoleAwareSerializerTests(unittest.TestCase):
    def test_generic_reencode_uses_final_anchors(self):
        catalog,engine,request=fixture(grow=True)
        active=IntegratedSerializer(catalog,engine,
            policy(catalog.fields[FIELD],FieldPolicyCategory.GENERIC_REENCODE,16,
                   bytes.fromhex('04012000'),True))
        run=active.run((request,),run_id='TEST')
        self.assertTrue(run.complete_local_pipeline,run.summary())
        write=next(j for j in run.files[0].assembled.journal if j.id=='FIELD:'+FIELD)
        self.assertEqual(write.data,bytes.fromhex('04012000'))

    def test_both_contact_dependency_prefixes_are_supported(self):
        for prefix in ('CONTACT:','CONTACT:O:'):
            catalog,engine,request=fixture(contact_prefix=prefix)
            active=IntegratedSerializer(catalog,engine,
                policy(catalog.fields[FIELD],FieldPolicyCategory.GENERIC_IDENTITY,8,
                       catalog.fields[FIELD].source_header,False))
            self.assertTrue(active.run((request,),run_id=prefix).complete_local_pipeline)

    def test_payload_preserve_has_no_field_writer(self):
        catalog,engine,request=fixture(state=FieldState.PAYLOAD)
        active=IntegratedSerializer(catalog,engine,
            policy(catalog.fields[FIELD],FieldPolicyCategory.PAYLOAD_PRESERVE,8,
                   catalog.fields[FIELD].source_header,False))
        run=active.run((request,),run_id='PRESERVE')
        self.assertTrue(run.complete_local_pipeline,run.summary())
        self.assertFalse(any(j.id=='FIELD:'+FIELD for j in run.files[0].assembled.journal))

    def test_request_cannot_override_policy_rule(self):
        catalog,engine,request=fixture()
        active=IntegratedSerializer(catalog,engine,
            policy(catalog.fields[FIELD],FieldPolicyCategory.GENERIC_IDENTITY,8,
                   catalog.fields[FIELD].source_header,False))
        c=catalog.fields[FIELD]
        override=ReviewedFieldRule(FIELD,'PC_EDITOR04',sha256(c.source_header),c.source_target,0,None,0,P)
        run=active.run((replace(request,field_rules=(override,)),),run_id='OVERRIDE')
        self.assertFalse(run.files[0].local_complete)
        self.assertTrue(any('FORBIDS_MANIFEST_FIELD_RULE_OVERRIDE' in reason
            for result in run.files[0].attempts for reason in result.reasons))


if __name__=='__main__':
    unittest.main()
