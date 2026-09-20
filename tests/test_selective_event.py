from __future__ import annotations

import struct
import unittest

from builder.selective_event import (
    HEADER_SIZE,
    SelectiveEventError,
    group_partition,
    parse_event_ts5,
    rebuild_event_ts5,
)


def _synthetic_ts5(partitions: list[bytes], prefix: bytes = b"HEAD") -> bytes:
    count = len(partitions)
    first = 8 + 4 * (count + 1)
    offsets = [first]
    for part in partitions:
        offsets.append(offsets[-1] + len(part))
    return prefix + struct.pack("<I", count) + b"".join(struct.pack("<I", x) for x in offsets) + b"".join(partitions)


class SelectiveEventUnitTests(unittest.TestCase):
    def test_synthetic_parse_rebuild_identity(self) -> None:
        blob = _synthetic_ts5([b"\x03\x00\x00\x00", b"\x11\x00\x00\x00AB\x00\x00"])
        parsed = parse_event_ts5(blob)
        self.assertEqual(parsed.count, 2)
        self.assertEqual(len(parsed.offsets), 3)
        self.assertEqual(rebuild_event_ts5(parsed), blob)

    def test_textish_grouping_and_trap(self) -> None:
        data = (
            b"\x11\x00\x00\x00"
            b"ABC\x01"
            b"DEF\x00"
            b"\x04\x00\x00\x00"
        )
        items = group_partition(data, 0x100)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].start, 0x100)
        self.assertEqual(items[0].data, data[:12])
        self.assertEqual(items[1].opcode, 0x04)

    def test_disguised_15_does_not_merge(self) -> None:
        data = b"\x15\x02\x00\x03" + b"ABC\x00"
        items = group_partition(data)
        self.assertEqual(len(items), 2)
        self.assertTrue(items[0].disguised_15)
        self.assertEqual(len(items[0].data), 4)

    def test_choice_merge_and_forced_break(self) -> None:
        ordinary = b"\x15\x02\x00\x00" + b"A\x00\x00\x00" + b"B\x00\x00\x00"
        items = group_partition(ordinary)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].data, ordinary)

        forced = b"\x15\x02\x00\x00" + b"\x0A\x80\x1C\x00" + b"TAIL"
        items = group_partition(forced)
        self.assertEqual(items[0].data, forced[:8])
        self.assertEqual(items[1].data, b"TAIL")

    def test_false_04_guards(self) -> None:
        cases = [
            (b"\x16\x00\x00\x00" + b"\x04\x01\x02\x03", "16_18_plus_04"),
            (b"\x0B\x00\x17\x00" + b"\x04\x00\x02\x03", "0b17_plus_0400"),
            (b"\x04\x00\x01\x0E" + b"\x04\x00\x02\x0E", "04000e_pair"),
        ]
        for data, guard in cases:
            with self.subTest(guard=guard):
                items = group_partition(data)
                self.assertEqual(len(items), 1)
                self.assertEqual(items[0].guard_merge, guard)
                self.assertEqual(items[0].data, data)

    def test_5a_and_3c_group_string_payloads(self) -> None:
        data_5a = b"\x5A\x00\x00\x00" + b"A\x00\x00\x00" + b"B\x00\x00\x00" + b"C\x00\x00\x00"
        self.assertEqual(len(group_partition(data_5a)), 1)

        data_3c = (
            b"\x3C\x00\x00\x00"
            + b"A\x00\x00\x00"
            + b"B\x00\x00\x00"
            + b"C\x00\x00\x00"
            + b"D\x00\x00\x00"
        )
        self.assertEqual(len(group_partition(data_3c)), 1)

    def test_misaligned_partition_rejected(self) -> None:
        with self.assertRaises(SelectiveEventError) as cm:
            group_partition(b"abc")
        self.assertEqual(cm.exception.code, "PARTITION_ALIGNMENT_FAIL")

    def test_stock_header_geometry_constant(self) -> None:
        self.assertEqual(HEADER_SIZE, 8 + 4 * (782 + 1))


if __name__ == "__main__":
    unittest.main()
