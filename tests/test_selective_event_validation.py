from pathlib import Path
import unittest

from builder.selective_event import SelectiveEventError
from builder.selective_event_validation import (
    ALIAS_NOVEL_ELIGIBLE, StateAwareAliasRecord, StateAwareResidual,
    canonical_v339_residual, decode_event_01020e0f_parent_length,
    load_stateaware_alias_ledger, validate_stateaware_residual_delta,
)

ARTIFACT = Path(__file__).resolve().parents[1] / 'selective_ko' / 'artifacts' / 'ecf00000_v344_particle_preimplementation_v1' / 'STATEAWARE_ALIAS_COMPACT.bin'

def tiny_ts5(payload: bytes) -> bytes:
    first=16
    return b'HEAD' + (1).to_bytes(4,'little') + first.to_bytes(4,'little') + (first+len(payload)).to_bytes(4,'little') + payload

class StateAwareResidualGateTests(unittest.TestCase):
    def test_0e_length_formula(self):
        self.assertEqual(decode_event_01020e0f_parent_length(bytes.fromhex('0e02d51f')), 0x7F5408)

    def test_inherited_shifted_residual_nonblocking(self):
        r=validate_stateaware_residual_delta((canonical_v339_residual(),))
        self.assertEqual(r.inherited_residuals,1); self.assertEqual(r.source_alias_residuals,0); self.assertFalse(r.blocking)

    def test_duplicate_state_observations_collapse_when_same_offset(self):
        row=canonical_v339_residual(); r=validate_stateaware_residual_delta((row,row))
        self.assertEqual(r.candidate_observations,2); self.assertEqual(r.candidate_residuals,1)

    def test_same_key_different_current_offset_is_ambiguous(self):
        a=canonical_v339_residual(); b=StateAwareResidual(a.partition,a.original_offset,a.current_offset+4,a.opcode,a.decoded_length)
        with self.assertRaises(SelectiveEventError) as cm: validate_stateaware_residual_delta((a,b))
        self.assertEqual(cm.exception.code,'EVENT_STATEAWARE_AMBIGUOUS_RESIDUAL')

    def test_canonical_alias_ledger(self):
        rows=load_stateaware_alias_ledger(ARTIFACT.read_bytes())
        self.assertEqual(len(rows),52); self.assertEqual(sum(r.disposition==ALIAS_NOVEL_ELIGIBLE for r in rows),48)

    def test_source_proven_alias_passes_with_exact_current_bytes(self):
        # Synthetic offsets, same structural proof shape as canonical aliases.
        parent=bytes.fromhex('0bdc1700')  # event 0B len 8
        alias=bytes.fromhex('0e009d06')   # decoded 0x1A7400
        blob=tiny_ts5(parent+alias+b'\0\0\0\0')
        rec=StateAwareAliasRecord(0,16,20,int.from_bytes(parent,'little'),8,int.from_bytes(alias,'little'),0x1A7400,ALIAS_NOVEL_ELIGIBLE,1)
        residual=StateAwareResidual(0,20,20,0x0E,0x1A7400)
        r=validate_stateaware_residual_delta((residual,residual), baseline_residuals=(), alias_records=(rec,), current_blob=blob)
        self.assertEqual(r.candidate_observations,2); self.assertEqual(r.source_alias_residuals,1); self.assertFalse(r.blocking)

    def test_alias_without_current_byte_proof_blocks(self):
        rec=StateAwareAliasRecord(0,16,20,int.from_bytes(bytes.fromhex('0bdc1700'),'little'),8,int.from_bytes(bytes.fromhex('0e009d06'),'little'),0x1A7400,ALIAS_NOVEL_ELIGIBLE,1)
        residual=StateAwareResidual(0,20,20,0x0E,0x1A7400)
        with self.assertRaises(SelectiveEventError) as cm: validate_stateaware_residual_delta((residual,),baseline_residuals=(),alias_records=(rec,))
        self.assertEqual(cm.exception.code,'EVENT_STATEAWARE_NOVEL_RESIDUAL')

    def test_changed_parent_header_blocks_alias(self):
        parent=bytes.fromhex('0bdc1900'); alias=bytes.fromhex('0e009d06')
        blob=tiny_ts5(parent+alias+b'\0\0\0\0')
        rec=StateAwareAliasRecord(0,16,20,int.from_bytes(bytes.fromhex('0bdc1700'),'little'),8,int.from_bytes(alias,'little'),0x1A7400,ALIAS_NOVEL_ELIGIBLE,1)
        residual=StateAwareResidual(0,20,20,0x0E,0x1A7400)
        with self.assertRaises(SelectiveEventError) as cm: validate_stateaware_residual_delta((residual,),baseline_residuals=(),alias_records=(rec,),current_blob=blob)
        self.assertEqual(cm.exception.code,'EVENT_STATEAWARE_NOVEL_RESIDUAL')

if __name__=='__main__': unittest.main()
