import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

from builder.selective_event import GroupedItem, EventPartition, ParsedEventTs5, SelectiveEventError
from builder.selective_event_derived_surface import *

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifact_v351'
ROWS=ART/'ROWS.jsonl'
OCC=ART/'OCCURRENCES.jsonl'
MIXED=ART/'MIXED_COMPOSITE.jsonl'
BIND=ART/'BINDINGS_V334_HASHED.jsonl'

def cmd(op:int,payload:bytes)->bytes:
    raw=bytes((op,0,0,0))+payload+b'\0'
    return raw+b'\0'*((-len(raw))%4)

class DerivedSurfaceTests(unittest.TestCase):
    def test_canonical_authority(self):
        rows,occ,edits=load_derived_surface_authority(ROWS.read_bytes(),OCC.read_bytes(),MIXED.read_bytes(),BIND.read_bytes())
        self.assertEqual((len(rows),len(occ),len(edits)),(61,62,3))
        self.assertEqual(sum(r.raw_growth for r in rows),972)
        self.assertEqual(Counter(r.opcode for r in rows),Counter({0x11:32,0x12:5,0x13:24}))
        raw=[json.loads(x) for x in BIND.read_text(encoding='utf-8').splitlines() if x]
        self.assertEqual(Counter(x['v334_mapping_method'] for x in raw),Counter(EXPECTED_V334_MAPPING_METHOD_COUNTS))

    def test_rows_sha_rejected(self):
        b=bytearray(ROWS.read_bytes()); b[-2]^=1
        with self.assertRaises(SelectiveEventError) as cm:
            load_derived_surface_authority(bytes(b),OCC.read_bytes(),MIXED.read_bytes(),BIND.read_bytes())
        self.assertEqual(cm.exception.code,'DERIVED_ROWS_SHA_FAIL')

    def test_synthetic_pure_raw_overlay(self):
        original_item=cmd(0x11,b'JP')
        ko_item=cmd(0x11,b'KO')
        row=DerivedBindingRecord(1,0,16,16,0x11,len(original_item),len(ko_item),hashlib.sha256(original_item).hexdigest(),hashlib.sha256(ko_item).hexdigest(),'COPULA_DERIVED_ONLY','RAW_PC_KO_PRESERVE_AUTHORED_DERIVED_SURFACE',len(ko_item)-len(original_item))
        occ=(DerivedOccurrenceRecord(1,0,'\\X','이었다',False,False),)
        parsed=ParsedEventTs5((EventPartition(0,(GroupedItem(16,original_item),)),))
        solved,rep=apply_pc_authored_derived_surfaces(parsed,b'X'*16+ko_item,((original_item,),),(row,),occ,(),require_canonical=False)
        self.assertEqual(solved[0][0],ko_item)
        self.assertEqual(rep.rows,1)

    def test_synthetic_mixed_exact_edit(self):
        original_item=cmd(0x11,b'JP')
        ko_item=cmd(0x11,b'\\%00'+bytes.fromhex('f36b')+b' T')
        target=cmd(0x11,b'\\%00'+bytes.fromhex('eb40')+b' T')
        row=DerivedBindingRecord(1,0,16,16,0x11,len(original_item),len(ko_item),hashlib.sha256(original_item).hexdigest(),hashlib.sha256(ko_item).hexdigest(),'MIXED_DIRECT_AND_DERIVED_RISK','RAW_PC_KO_THEN_EXACT_DIRECT_PARTICLE_NORMALIZATION',len(ko_item)-len(original_item))
        occ=(DerivedOccurrenceRecord(1,1,'\\Z001','이었나',False,False),)
        edits=(MixedDirectEdit(1,0,'\\%00','이','가'),)
        parsed=ParsedEventTs5((EventPartition(0,(GroupedItem(16,original_item),)),))
        solved,_=apply_pc_authored_derived_surfaces(parsed,b'X'*16+ko_item,((original_item,),),(row,),occ,edits,require_canonical=False)
        self.assertEqual(solved[0][0],target)

    def test_mixed_needle_multiplicity_rejected(self):
        original_item=cmd(0x11,b'JP')
        needle=b'\\%00'+bytes.fromhex('f36b')
        ko_item=cmd(0x11,needle+b' '+needle)
        row=DerivedBindingRecord(1,0,16,16,0x11,len(original_item),len(ko_item),hashlib.sha256(original_item).hexdigest(),hashlib.sha256(ko_item).hexdigest(),'MIXED_DIRECT_AND_DERIVED_RISK','RAW_PC_KO_THEN_EXACT_DIRECT_PARTICLE_NORMALIZATION',len(ko_item)-len(original_item))
        occ=(DerivedOccurrenceRecord(1,1,'\\Z001','이었나',False,False),)
        edits=(MixedDirectEdit(1,0,'\\%00','이','가'),)
        parsed=ParsedEventTs5((EventPartition(0,(GroupedItem(16,original_item),)),))
        with self.assertRaises(SelectiveEventError) as cm:
            apply_pc_authored_derived_surfaces(parsed,b'X'*16+ko_item,((original_item,),),(row,),occ,edits,require_canonical=False)
        self.assertEqual(cm.exception.code,'DERIVED_MIXED_NEEDLE_MULTIPLICITY_FAIL')

    def test_bad_baseline_rejected(self):
        original_item=cmd(0x11,b'JP'); ko_item=cmd(0x11,b'KO')
        row=DerivedBindingRecord(1,0,16,16,0x11,len(original_item),len(ko_item),hashlib.sha256(original_item).hexdigest(),hashlib.sha256(ko_item).hexdigest(),'COPULA_DERIVED_ONLY','RAW_PC_KO_PRESERVE_AUTHORED_DERIVED_SURFACE',len(ko_item)-len(original_item))
        occ=(DerivedOccurrenceRecord(1,0,'\\X','이었다',False,False),)
        parsed=ParsedEventTs5((EventPartition(0,(GroupedItem(16,original_item),)),))
        with self.assertRaises(SelectiveEventError) as cm:
            apply_pc_authored_derived_surfaces(parsed,b'X'*16+ko_item,((cmd(0x11,b'OTHER'),),),(row,),occ,(),require_canonical=False)
        self.assertEqual(cm.exception.code,'DERIVED_BASELINE_FAIL')

if __name__=='__main__': unittest.main()
