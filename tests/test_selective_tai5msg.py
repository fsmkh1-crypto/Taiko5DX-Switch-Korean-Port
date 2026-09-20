from pathlib import Path
import unittest

from builder.selective_tai5msg import (
    ALIGN,
    SelectiveTai5MsgError,
    _align_up,
    _b24_layout_line_widths,
    _b24_nonlayout_signature,
    _decrypt,
    _encrypt,
    _is_korean_added_code,
    _validate_selected_message,
    korean_added_code_domain,
    load_v315_corrections,
    load_v356_percent_macro_roots,
    load_v320_corrections,
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

    def test_v315_b24_correction_overlay(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        corrections = load_v315_corrections(repo_root)
        self.assertEqual(len(corrections), 109)
        self.assertNotIn((24, 232), corrections)
        self.assertNotIn((24, 341), corrections)
        self.assertEqual(corrections[(24, 227)].target_sha256, "63d1fbd8c880af1218fbd8a51779f02ca8f48e5ab92a8dedcdaeb1575b0e7c0c")
        self.assertEqual(corrections[(24, 228)].target_sha256, "5b570aa621967923597b2c1649b26abbb8a668c1e788204cf22a8a767e5d5210")
        self.assertEqual(corrections[(24, 229)].target_sha256, "14b5bd978a162b921c316f9a93b31fb19ecec4e038623583a9ae066e49b26178")

    def test_v320_b24_native_wrap_overlay(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        corrections = load_v320_corrections(repo_root)
        self.assertEqual(len(corrections), 108)
        self.assertIn((24, 221), corrections)
        self.assertNotIn((24, 228), corrections)
        self.assertEqual(
            corrections[(24, 221)].target_sha256,
            "ff2212aef28bce328d5a2564b8ea1ae499c3b068035794b00cb5212470a51442",
        )
        self.assertEqual(
            corrections[(24, 257)].target_sha256,
            "26acf8b1ecc24111b46ac25cc5e837e4875ef6b6e4f9629ac9e38e0edd86f288",
        )
        self.assertEqual(
            corrections[(24, 320)].target_sha256,
            "3834475a5aa1076c3bc43757d780f16a556e0c281dc540aecdc812e6885ad493",
        )
        for correction in corrections.values():
            widths = _b24_layout_line_widths(correction.target_bytes)
            self.assertLessEqual(len(widths), 12)
            self.assertLessEqual(max(widths), 52)
            self.assertEqual(
                _b24_nonlayout_signature(correction.source_bytes),
                _b24_nonlayout_signature(correction.target_bytes),
            )

    def test_v356_percent_macro_root_manifest(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        roots = load_v356_percent_macro_roots(repo_root)
        self.assertEqual(len(roots), 46)
        self.assertEqual(sum(spec.delta for spec in roots.values()), 578)
        self.assertNotIn((0, 10), roots)
        self.assertNotIn((0, 11), roots)

    def test_repository_metadata_preflight(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        report = metadata_preflight(repo_root)
        self.assertEqual(report.selected_rows, 3179)
        self.assertEqual(report.program_root_rows, 46)
        self.assertEqual(report.growth, 0x7300)
        self.assertEqual(report.final_size, 0x1C14C9)
        self.assertEqual(report.b32_offset, 0x1B4A80)
        self.assertEqual(report.b32_used_end, 0xB8D5)
        self.assertEqual(report.b32_declared, 0xCA80)
        self.assertEqual(report.b32_physical, 0xCA49)
        self.assertEqual(report.b32_omitted, 0x37)
        self.assertEqual(
            report.growth_blocks,
            ((0, 0x240), (17, 0x340), (19, 0xA80), (20, 0x6C0), (21, 0x1C0), (22, 0x4340), (23, 0xFC0), (24, 0x780)),
        )


if __name__ == "__main__":
    unittest.main()
