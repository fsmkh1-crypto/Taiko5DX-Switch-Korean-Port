"""Boundary regressions derived from the target interpreter, not translation guesses."""
import unittest
from switch_vm_fields import inspect, structural_signature
M=set(range(32,127)) | {0xef8d,0xf6d6}
class Fields(unittest.TestCase):
 def test_optional_property_rewinds_control(self):
  r=inspect(bytes.fromhex('026f050505'),M)
  self.assertTrue(r['complete']);self.assertEqual(r['atoms'],[(0,2)])
 def test_property_consumes_high_byte_not_a_glyph(self):
  r=inspect(bytes.fromhex('026fef8d20050505'),M)
  self.assertFalse(r['complete']);self.assertEqual(r['atoms'],[(0,3)])
 def test_condition_digits_are_not_literal(self):
  d=bytes.fromhex('050504026f64043d323433050505')
  r=inspect(d,M);self.assertTrue(r['complete']);self.assertFalse(any(x['kind']=='LITERAL' for x in r['fields']))
 def test_assignment_expression_operand_is_preserved(self):
  a=bytes.fromhex('014d02013234050505');b=bytes.fromhex('014d02013235050505')
  self.assertNotEqual(structural_signature(a,inspect(a,M)),structural_signature(b,inspect(b,M)))
 def test_call_and_jump_are_distinct_global_ids(self):
  r=inspect(bytes.fromhex('01433300014ad30f050505'),M)
  self.assertTrue(r['complete']);self.assertEqual([(x['operation'],x['target']) for x in r['edges']],[('CALL','B0:51'),('JUMP','B4:51')])
 def test_unknown_control_fails_closed(self):
  self.assertFalse(inspect(bytes.fromhex('014102f502050505'),M)['complete'])
 def test_c8_nested_arguments(self):
  r=inspect(bytes.fromhex('02c88a020164020264050505'),M)
  self.assertTrue(r['complete']);self.assertIn((0,9),r['atoms'])
if __name__=='__main__':unittest.main()
