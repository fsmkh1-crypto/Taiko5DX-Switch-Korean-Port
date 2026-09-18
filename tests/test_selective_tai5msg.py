from pathlib import Path
import unittest

from builder.selective_tai5msg import (
    ALIGN,
    SelectiveTai5MsgError,
    _align_up,
    _decrypt,
    _encrypt,
    _is_korean_added_code,
    _validate_selected_message,
    korean_added_code_domain,
    metadata_preflight,
)


class SelectiveTai5MsgUnitTests(unittest.TestCase):
    def test_storage_transform_roundtrip(self) -> None:
        data = bytes(range(256))
        self.assertEqual(_decrypt(_encrypt(data)), data)
        self.assertEqual(_encrypt(_decrypt(data)), data)

    def test_align_up(self) -> None:
        self.assertEqual(_align_up(0xAED0, ALIGN), 0xAF00)
        self.assertEqual(_align_up(0xDDEA, ALIGN), 0xDE00)
        self.assertEqual(_align_up(0x12AF1, ALIGN), 0x12B00)

    def test_korean_added_domain(self) -> None:
        domain = korean_added_code_domain()
        self.assertEqual(len(domain), 2542)
        self.assertIn(0xEB40, domain)
        self.assertIn(0xF8A2, domain)
        self.assertNotIn(0xEAFC, domain)
        self.assertNotIn(0xF8A3, domain)
        self.assertFalse(_is_korean_added_code(0xEB7F))

    def test_known_control_and_mapping_validation(self) -> None:
        mapping = frozenset({0x0A, 0x8140, 0xEB40})
        message = b"\x1b\x48\xeb\x40 \x81\x40\x0a\x05\x05\x05"
        two_byte, korean = _validate_selected_message(message, (17, 0), mapping)
        self.assertEqual(two_byte[0xEB40], 1)
        self.assertEqual(two_byte[0x8140], 1)
        self.assertEqual(korean[0xEB40], 1)

    def test_semantic_02_is_rejected(self) -> None:
        with self.assertRaises(SelectiveTai5MsgError) as cm:
            _validate_selected_message(b"\x02\x00\x00\x05\x05\x05", (17, 0), frozenset())
        self.assertEqual(cm.exception.code, "CONTROL_TOKEN_VALIDATION_FAIL")

    def test_b32_structural_zero_only_for_final_slot(self) -> None:
        mapping = frozenset({0x8140})
        _validate_selected_message(b"\x81\x40\x05\x05\x05\x00", (32, 242), mapping)
        with self.assertRaises(SelectiveTai5MsgError):
            _validate_selected_message(b"\x81\x40\x05\x05\x05\x00", (32, 159), mapping)

    def test_repository_metadata_preflight(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        report = metadata_preflight(repo_root)
        self.assertEqual(report.selected_rows, 3179)
        self.assertEqual(report.growth, 0x7780)
        self.assertEqual(report.final_size, 0x1C1949)
        self.assertEqual(report.b32_offset, 0x1B4F00)
        self.assertEqual(report.b32_used_end, 0xB8D5)
        self.assertEqual(report.b32_declared, 0xCA80)
        self.assertEqual(report.b32_physical, 0xCA49)
        self.assertEqual(report.b32_omitted, 0x37)
        self.assertEqual(
            report.growth_blocks,
            ((17, 0x340), (19, 0xA80), (20, 0x6C0), (21, 0x1C0), (22, 0x4340), (23, 0xFC0), (24, 0xE40)),
        )


if __name__ == "__main__":
    unittest.main()
