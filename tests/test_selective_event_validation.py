import unittest

from builder.selective_event import SelectiveEventError
from builder.selective_event_validation import (
    CANONICAL_STOCK_STATEAWARE_RESIDUALS,
    StateAwareResidual,
    canonical_v339_residual,
    decode_event_01020e0f_parent_length,
    validate_stateaware_residual_delta,
)


class StateAwareResidualGateTests(unittest.TestCase):
    def test_canonical_stock_residual(self):
        self.assertEqual(len(CANONICAL_STOCK_STATEAWARE_RESIDUALS), 1)
        row = CANONICAL_STOCK_STATEAWARE_RESIDUALS[0]
        self.assertEqual(row.partition, 593)
        self.assertEqual(row.original_offset, 0xBDD78)
        self.assertEqual(row.opcode, 0x0E)
        self.assertEqual(row.decoded_length, 0x7F5408)

    def test_0e_length_formula(self):
        self.assertEqual(
            decode_event_01020e0f_parent_length(bytes.fromhex("0e02d51f")),
            0x7F5408,
        )

    def test_shifted_same_logical_residual_is_nonblocking(self):
        report = validate_stateaware_residual_delta((canonical_v339_residual(),))
        self.assertEqual(report.baseline_residuals, 1)
        self.assertEqual(report.candidate_residuals, 1)
        self.assertEqual(report.inherited_residuals, 1)
        self.assertEqual(report.novel_residuals, 0)
        self.assertFalse(report.blocking)

    def test_resolved_stock_residual_is_nonblocking(self):
        report = validate_stateaware_residual_delta(())
        self.assertEqual(report.resolved_baseline_residuals, 1)
        self.assertEqual(report.novel_residuals, 0)
        self.assertFalse(report.blocking)

    def test_novel_residual_is_blocking(self):
        novel = StateAwareResidual(593, 0xBDD7C, 0xDDD88, 0x80, 4)
        with self.assertRaises(SelectiveEventError) as cm:
            validate_stateaware_residual_delta((canonical_v339_residual(), novel))
        self.assertEqual(cm.exception.code, "EVENT_STATEAWARE_NOVEL_RESIDUAL")

    def test_changed_length_same_anchor_is_blocking(self):
        changed = StateAwareResidual(593, 0xBDD78, 0xDDD84, 0x0E, 0x7F540C)
        with self.assertRaises(SelectiveEventError) as cm:
            validate_stateaware_residual_delta((changed,))
        self.assertEqual(cm.exception.code, "EVENT_STATEAWARE_NOVEL_RESIDUAL")

    def test_duplicate_candidate_residual_is_rejected(self):
        row = canonical_v339_residual()
        with self.assertRaises(SelectiveEventError) as cm:
            validate_stateaware_residual_delta((row, row))
        self.assertEqual(cm.exception.code, "EVENT_STATEAWARE_DUPLICATE_RESIDUAL")


if __name__ == "__main__":
    unittest.main()
