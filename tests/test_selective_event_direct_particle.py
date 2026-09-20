import unittest
from pathlib import Path
from builder.selective_event import GroupedItem, EventPartition, ParsedEventTs5, SelectiveEventError
from builder.selective_event_direct_particle import *

ART = Path(__file__).resolve().parents[1] / 'selective_ko' / 'artifacts' / 'ecf00000_v348_direct_escape_particle_policy_v1'

def field(value:bytes):
    raw=value+b'\0'; return raw+b'\0'*((-len(raw))%4)
def msg(op,value): return bytes((op,0,0,0))+field(value)

class DirectEscapeParticleTests(unittest.TestCase):
    def test_canonical_v348_ledgers(self):
        app,occ=load_direct_escape_ledgers((ART/'APPLICABILITY.jsonl').read_bytes(),(ART/'OCCURRENCES.jsonl').read_bytes())
        self.assertEqual(len(app),DIRECT_APPLICABILITY_ROWS)
        self.assertEqual(len(occ),DIRECT_OCCURRENCES)
        self.assertEqual(sum(x.substitute for x in occ),DIRECT_SUBSTITUTIONS)
        self.assertEqual(sum(x.normalization_occurrences>0 for x in app),DIRECT_NORMALIZATION_ROWS)
    def test_bad_app_sha_rejected(self):
        app=bytearray((ART/'APPLICABILITY.jsonl').read_bytes()); app[-2]^=1
        with self.assertRaises(SelectiveEventError) as cm:
            load_direct_escape_ledgers(bytes(app),(ART/'OCCURRENCES.jsonl').read_bytes())
        self.assertEqual(cm.exception.code,'DIRECT_APP_SHA_FAIL')
    def test_transform_repeated(self):
        src=PARTICLE_BYTES['은']; tgt=PARTICLE_BYTES['는']
        cmd=msg(0x11,b'A\\%00'+src+b'B\\%00'+src+b'C')
        occ=(
          DirectOccurrenceRecord(1,0,16,16,0x11,0,0,1,'\\%00','은','는',src,tgt,True),
          DirectOccurrenceRecord(1,0,16,16,0x11,1,0,6,'\\%00','은','는',src,tgt,True),
        )
        out,sc,tc=transform_direct_escape_command(cmd,occ)
        self.assertEqual(len(out),len(cmd)); self.assertEqual(sc['은'],2);self.assertEqual(tc['는'],2)
        self.assertNotIn(b'\\%00'+src,out);self.assertEqual(out.count(b'\\%00'+tgt),2)
    def test_unexpected_extra_same_needle_rejected(self):
        src=PARTICLE_BYTES['은']; tgt=PARTICLE_BYTES['는']
        cmd=msg(0x11,b'\\%00'+src+b'X\\%00'+src)
        occ=(DirectOccurrenceRecord(1,0,16,16,0x11,0,0,0,'\\%00','은','는',src,tgt,True),)
        with self.assertRaises(SelectiveEventError) as cm: transform_direct_escape_command(cmd,occ)
        self.assertEqual(cm.exception.code,'DIRECT_RAW_NEEDLE_MULTIPLICITY_FAIL')
    def test_apply_synthetic(self):
        src=PARTICLE_BYTES['은'];tgt=PARTICLE_BYTES['는']
        original_item=msg(0x11,b'JP');ko_item=msg(0x11,b'K\\%00'+src)
        parsed=ParsedEventTs5((EventPartition(0,(GroupedItem(16,original_item),)),));ko=b'X'*16+ko_item
        app=(DirectApplicabilityRecord(1,0,16,16,0x11,len(original_item),len(ko_item),1,1),)
        occ=(DirectOccurrenceRecord(1,0,16,16,0x11,0,0,1,'\\%00','은','는',src,tgt,True),)
        solved,report=apply_direct_escape_particles(parsed,ko,((original_item,),),app,occ,require_canonical=False)
        self.assertEqual(len(solved[0][0]),len(ko_item));self.assertIn(b'\\%00'+tgt,solved[0][0]);self.assertEqual(report.substitutions,1)
    def test_bad_baseline_rejected(self):
        src=PARTICLE_BYTES['은'];tgt=PARTICLE_BYTES['는'];original_item=msg(0x11,b'JP');ko_item=msg(0x11,b'K\\%00'+src)
        parsed=ParsedEventTs5((EventPartition(0,(GroupedItem(16,original_item),)),));ko=b'X'*16+ko_item
        app=(DirectApplicabilityRecord(1,0,16,16,0x11,len(original_item),len(ko_item),1,1),)
        occ=(DirectOccurrenceRecord(1,0,16,16,0x11,0,0,1,'\\%00','은','는',src,tgt,True),)
        with self.assertRaises(SelectiveEventError) as cm: apply_direct_escape_particles(parsed,ko,((msg(0x11,b'OTHER'),),),app,occ,require_canonical=False)
        self.assertEqual(cm.exception.code,'DIRECT_BASELINE_FAIL')

if __name__=='__main__': unittest.main()
