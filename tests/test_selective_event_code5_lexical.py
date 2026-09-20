import unittest
import hashlib
from pathlib import Path
from builder.selective_event import GroupedItem, EventPartition, ParsedEventTs5, SelectiveEventError
from builder.selective_event_code5_lexical import *

ART = Path(__file__).resolve().parents[1] / 'artifact' / 'APPLICABILITY.jsonl'

def cmd(op: int, payload: bytes) -> bytes:
    raw = bytes((op,0,0,0)) + payload + b'\0'
    return raw + b'\0' * ((-len(raw)) % 4)

class LexicalFalsePositiveTests(unittest.TestCase):
    def test_canonical_applicability(self):
        rows = load_lexical_applicability(ART.read_bytes())
        self.assertEqual(len(rows),12)
        self.assertEqual(sum(r.growth for r in rows),200)
        self.assertEqual(tuple(r.row_id for r in rows),EXPECTED_ROW_IDS)

    def test_bad_sha_rejected(self):
        b=bytearray(ART.read_bytes()); b[-2]^=1
        with self.assertRaises(SelectiveEventError) as cm:
            load_lexical_applicability(bytes(b))
        self.assertEqual(cm.exception.code,'LEXICAL_APP_SHA_FAIL')

    def test_synthetic_exact_raw_ko_replacement(self):
        original_item=cmd(0x11,b'JP')
        ko_item=cmd(0x11,b'KO')
        row=LexicalApplicabilityRecord(1,0,16,16,0x11,len(original_item),len(ko_item),'\\#0001',hashlib.sha256(original_item).hexdigest(),hashlib.sha256(ko_item).hexdigest(),len(ko_item)-len(original_item))
        parsed=ParsedEventTs5((EventPartition(0,(GroupedItem(16,original_item),)),))
        blob=b'X'*16+ko_item
        solved,report=apply_lexical_false_positive_rows(parsed,blob,((original_item,),),(row,),require_canonical=False)
        self.assertEqual(solved[0][0],ko_item)
        self.assertEqual(report.rows,1)

    def test_bad_baseline_rejected(self):
        original_item=cmd(0x11,b'JP'); ko_item=cmd(0x11,b'KO')
        row=LexicalApplicabilityRecord(1,0,16,16,0x11,len(original_item),len(ko_item),'\\#0001',hashlib.sha256(original_item).hexdigest(),hashlib.sha256(ko_item).hexdigest(),len(ko_item)-len(original_item))
        parsed=ParsedEventTs5((EventPartition(0,(GroupedItem(16,original_item),)),))
        with self.assertRaises(SelectiveEventError) as cm:
            apply_lexical_false_positive_rows(parsed,b'X'*16+ko_item,((cmd(0x11,b'OTHER'),),),(row,),require_canonical=False)
        self.assertEqual(cm.exception.code,'LEXICAL_BASELINE_FAIL')

    def test_bad_ko_hash_rejected(self):
        original_item=cmd(0x11,b'JP'); ko_item=cmd(0x11,b'KO')
        row=LexicalApplicabilityRecord(1,0,16,16,0x11,len(original_item),len(ko_item),'\\#0001',hashlib.sha256(original_item).hexdigest(),'0'*64,len(ko_item)-len(original_item))
        parsed=ParsedEventTs5((EventPartition(0,(GroupedItem(16,original_item),)),))
        with self.assertRaises(SelectiveEventError) as cm:
            apply_lexical_false_positive_rows(parsed,b'X'*16+ko_item,((original_item,),),(row,),require_canonical=False)
        self.assertEqual(cm.exception.code,'LEXICAL_KO_HASH_FAIL')

if __name__=='__main__': unittest.main()
