from pathlib import Path
import struct
import unittest

from builder.selective_event import parse_event_ts5
from builder.selective_event_5a import (
    FIVEA_MAPPING_RECORD_COUNT,
    FIVEA_MAPPING_ROWSET_SHA256,
    FiveAMappingRecord,
    SelectiveEventError,
    compose_fivea,
    load_fivea_mapping,
    solve_fivea_composites,
    split_fivea_fields,
    switch_fivea_runtime_length,
)

ARTIFACT = (
    Path(__file__).resolve().parents[1]
    / 'selective_ko'
    / 'artifacts'
    / 'ecf00000_v339_5a_composite_v1'
    / 'MAPPING_ORIGINAL_KO_5A_COMPACT.bin'
)


def field(value: bytes) -> bytes:
    raw = value + b'\x00'
    return raw + b'\x00' * ((-len(raw)) % 4)


def fivea(name1: bytes, name2: bytes, dialogue: bytes, header=b'\x5A\x10\x20\x30') -> bytes:
    return header + field(name1) + field(name2) + field(dialogue)


def synthetic_ts5(part: bytes) -> bytes:
    first = 16
    return b'HEAD' + struct.pack('<I', 1) + struct.pack('<II', first, first + len(part)) + part


class FiveAUnitTests(unittest.TestCase):
    def test_canonical_compact_mapping(self):
        rows = load_fivea_mapping(ARTIFACT.read_bytes())
        self.assertEqual(len(rows), FIVEA_MAPPING_RECORD_COUNT)
        self.assertEqual(rows[0].partition, 42)
        self.assertEqual(rows[0].original_offset, 0x20B38)

    def test_bad_mapping_sha_rejected(self):
        blob = bytearray(ARTIFACT.read_bytes())
        blob[-1] ^= 1
        with self.assertRaises(SelectiveEventError) as cm:
            load_fivea_mapping(bytes(blob))
        self.assertEqual(cm.exception.code, 'FIVEA_MAPPING_SHA_FAIL')

    def test_composite_preserves_jp_names_and_uses_ko_dialogue(self):
        original = fivea(b'JP1', b'JP2', b'JP DIALOGUE')
        korean = fivea(b'KO1', b'KO2', b'KO DIALOGUE')
        result = compose_fivea(original, korean)
        fields = split_fivea_fields(result)
        self.assertEqual(fields[0][0], b'JP1')
        self.assertEqual(fields[1][0], b'JP2')
        self.assertEqual(fields[2][0], b'KO DIALOGUE')

    def test_name2_and_dialogue_padding_are_inside_visible_field(self):
        original = fivea(b'A', b'B', b'C')
        korean = fivea(b'X', b'Y', b'Z')
        result = compose_fivea(original, korean, name2_spaces=2, dialogue_spaces=3)
        fields = split_fivea_fields(result)
        self.assertEqual(fields[0][0], b'A')
        self.assertEqual(fields[1][0], b'B  ')
        self.assertEqual(fields[2][0], b'Z   ')

    def test_runtime_length_matches_real_stock_fixture(self):
        data = bytes.fromhex(
            '5a20d3ff8e7300008e4f985900000000'
            'b2b4bfb3b2b3dcb982c5ca82b282b4b2cfbedd00'
        )
        self.assertEqual(len(data), 36)
        self.assertEqual(switch_fivea_runtime_length(data), 36)

    def test_small_solver_preserves_name_only_original(self):
        original_item = fivea(b'JP', b'NAME', b'SAME')
        ko_item = fivea(b'KO', b'IREUM', b'SAME')
        original = parse_event_ts5(synthetic_ts5(original_item + b'\x00\x00\x00\x00'))
        ko = parse_event_ts5(synthetic_ts5(ko_item + b'\x00\x00\x00\x00'))
        rec = FiveAMappingRecord(0, 0, 16, 16, len(original_item), len(ko_item))
        current = [[item.data for item in original.partitions[0].grouped_items]]
        identity = lambda partition_index, items: tuple(items)
        solved, report, resolutions = solve_fivea_composites(
            original, ko, current, (rec,), require_canonical_counts=False, structure_repair=identity
        )
        self.assertEqual(solved[0][0], original_item)
        self.assertEqual(report.name_only_preserved_rows, 1)
        self.assertEqual(report.translated_rows, 0)
        self.assertEqual(resolutions, ())


if __name__ == '__main__':
    unittest.main()
