from pathlib import Path
import hashlib
import unittest

from builder.selective_event import EventPartition, GroupedItem, ParsedEventTs5, SelectiveEventError
from builder.selective_event_suffix3 import (
    APPLICABILITY_SHA256,
    EXPECTED_ROW_IDS,
    TOTAL_GROWTH,
    Suffix3ApplicabilityRecord,
    apply_suffix3_rows,
    load_suffix3_applicability,
)

class Suffix3Tests(unittest.TestCase):
    def test_canonical_manifest(self):
        root=Path(__file__).resolve().parents[1]
        blob=(root/'selective_ko/artifacts/ecf00000_v360_suffix3_post_v357_event_v1/APPLICABILITY.jsonl').read_bytes()
        self.assertEqual(hashlib.sha256(blob).hexdigest(), APPLICABILITY_SHA256)
        rows=load_suffix3_applicability(blob)
        self.assertEqual(tuple(r.row_id for r in rows), EXPECTED_ROW_IDS)
        self.assertEqual(sum(r.growth for r in rows), TOTAL_GROWTH)
        self.assertEqual({r.tai5msg_local for r in rows}, {209,349,395})

    def test_synthetic_exact_apply(self):
        source=b'\x11\x00\x00\x00ABCD'
        target=b'\x11\x00\x00\x00\\%21WXYZ'
        row=Suffix3ApplicabilityRecord(
            row_id=1,partition=0,original_offset=0x20,ko_offset=0,opcode=0x11,
            original_command_length=len(source),ko_command_length=len(target),macro='\\%21',
            tai5msg_block=0,tai5msg_local=349,original_sha256=hashlib.sha256(source).hexdigest(),
            ko_sha256=hashlib.sha256(target).hexdigest(),tai5msg_target_sha256='0'*64,growth=len(target)-len(source),
        )
        parsed=ParsedEventTs5(partitions=(EventPartition(0,(GroupedItem(0x20,source),)),))
        current=((source,),)
        out,report=apply_suffix3_rows(parsed,target,current,(row,),require_canonical=False)
        self.assertEqual(out[0][0],target)
        self.assertEqual(report.payload_growth,len(target)-len(source))

    def test_baseline_guard(self):
        source=b'\x11\x00\x00\x00ABCD'
        target=b'\x11\x00\x00\x00\\%21WXYZ'
        row=Suffix3ApplicabilityRecord(
            row_id=1,partition=0,original_offset=0x20,ko_offset=0,opcode=0x11,
            original_command_length=len(source),ko_command_length=len(target),macro='\\%21',
            tai5msg_block=0,tai5msg_local=349,original_sha256=hashlib.sha256(source).hexdigest(),
            ko_sha256=hashlib.sha256(target).hexdigest(),tai5msg_target_sha256='0'*64,growth=len(target)-len(source),
        )
        parsed=ParsedEventTs5(partitions=(EventPartition(0,(GroupedItem(0x20,source),)),))
        with self.assertRaises(SelectiveEventError):
            apply_suffix3_rows(parsed,target,((b'\x11\x00\x00\x00ZZZZ',),),(row,),require_canonical=False)

if __name__=='__main__': unittest.main()
