from __future__ import annotations

import struct
import unittest

from builder.selective_event import (
    BRANCH_ANALYSIS_ORDER,
    DYNAMIC_SWITCH_SPAN_ORIGINAL_STARTS,
    FALSE_EVENT_02_EXPRESSION_ORIGINAL_STARTS,
    GENERIC_BRANCH_EXCLUDED_ORIGINAL_STARTS,
    FalseEvent02NonOwner,
    GroupedItem,
    HEADER_SIZE,
    SelectiveEventError,
    SwitchSpecialSpanPlan,
    analyze_generic_branch_plans,
    group_partition,
    parse_event_ts5,
    rebuild_event_ts5,
    repair_generic_branch_items,
    repair_switch_special_span_items,
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

    def test_pc_editor_generic_relocation_all_families(self) -> None:
        def fixture(opcode: int, intrusion: int = 0) -> tuple[GroupedItem, GroupedItem]:
            span = 12
            if opcode == 0x02:
                header = b"\x02\x03\x00\x00"
            elif opcode == 0x04:
                header = b"\x04\x00\x18\x00"
            elif opcode in (0x06, 0x07):
                header = bytes((opcode, (span + intrusion) // 2, 0, 0))
            elif opcode == 0x08:
                header = b"\x08\xAA\x03\x00"
            else:
                header = bytes((0x09, 0xC3, span * 2 + intrusion, 0))
            return GroupedItem(0x100, header), GroupedItem(0x104, b"A" * 8)

        expected = {
            0x02: b"\x02\x04\x00\x00",
            0x04: b"\x04\x00\x20\x00",
            0x06: b"\x06\x09\x00\x00",
            0x07: b"\x07\x09\x00\x00",
            0x08: b"\x08\xAA\x04\x00",
            0x09: b"\x09\xC3\x23\x00",
        }

        for opcode in BRANCH_ANALYSIS_ORDER:
            intrusion = 2 if opcode in (0x06, 0x07) else 3 if opcode == 0x09 else 0
            items = fixture(opcode, intrusion)
            plans = analyze_generic_branch_plans(items, excluded_starts=frozenset())
            self.assertEqual(len(plans), 1)
            self.assertEqual(plans[0].stage_count, 2)
            self.assertEqual(plans[0].original_span, 12)
            self.assertEqual(plans[0].intrusion, intrusion)

            current = (items[0].data, items[1].data + b"BBBB")
            repaired = repair_generic_branch_items(items, current, plans=plans)
            self.assertEqual(repaired[0][:4], expected[opcode])

    def test_pc_editor_04_store_guards(self) -> None:
        odd = (GroupedItem(0, b"\x04\x00\x05\x00"),)
        high_second = (
            GroupedItem(0, b"\x04\x55\x08\x00"),
            GroupedItem(4, b"ABCD"),
        )
        merged_false_04 = (GroupedItem(0, b"\x04\x00\x08\x00XXXX"),)
        for items in (odd, high_second, merged_false_04):
            self.assertEqual(
                analyze_generic_branch_plans(items, excluded_starts=frozenset()),
                (),
            )

    def test_generic_special_owner_exclusion(self) -> None:
        items = (
            GroupedItem(0x7E1B0, b"\x09\xC3\x18\x00"),
            GroupedItem(0x7E1B4, b"A" * 8),
        )
        self.assertEqual(analyze_generic_branch_plans(items), ())
        self.assertEqual(
            len(analyze_generic_branch_plans(items, excluded_starts=frozenset())),
            1,
        )
        self.assertTrue(
            DYNAMIC_SWITCH_SPAN_ORIGINAL_STARTS
            <= GENERIC_BRANCH_EXCLUDED_ORIGINAL_STARTS
        )
        self.assertTrue(
            FALSE_EVENT_02_EXPRESSION_ORIGINAL_STARTS
            <= GENERIC_BRANCH_EXCLUDED_ORIGINAL_STARTS
        )

    def test_unrepresentable_generic_span_rejected(self) -> None:
        items = (
            GroupedItem(0x100, b"\x02\x03\x00\x00"),
            GroupedItem(0x104, b"A" * 8),
        )
        plans = analyze_generic_branch_plans(items, excluded_starts=frozenset())
        with self.assertRaises(SelectiveEventError) as cm:
            repair_generic_branch_items(
                items,
                (items[0].data, items[1].data + b"BB"),
                plans=plans,
            )
        self.assertEqual(cm.exception.code, "BRANCH_SPAN_NOT_REPRESENTABLE")

    def test_switch_special_event04_inner_owner_anchor(self) -> None:
        items = (
            GroupedItem(0xFC, b"\x17\x00\x19\x00\x04\x01\x18\x00"),
            GroupedItem(0x104, b"A" * 8),
            GroupedItem(0x10C, b"NEXT"),
        )
        plan = SwitchSpecialSpanPlan(
            kind="EVENT_04",
            partition_index=0,
            opcode=0x04,
            original_start=0x100,
            original_span=12,
            original_target=0x10C,
            owner_item_index=0,
            owner_inner_offset=4,
            target_item_index=2,
        )
        repaired = repair_switch_special_span_items(
            items,
            (items[0].data, items[1].data + b"BBBB", items[2].data),
            (plan,),
        )
        self.assertEqual(repaired[0][4:8], b"\x04\x01\x20\x00")

    def test_switch_special_branch09_runtime_bitfield(self) -> None:
        items = (
            GroupedItem(0x100, b"\x09\xF0\x6F\x14"),
            GroupedItem(0x104, b"A" * 8),
            GroupedItem(0x10C, b"NEXT"),
        )
        plan = SwitchSpecialSpanPlan(
            kind="BRANCH_09",
            partition_index=0,
            opcode=0x09,
            original_start=0x100,
            original_span=12,
            original_target=0x10C,
            owner_item_index=0,
            owner_inner_offset=0,
            target_item_index=2,
        )
        repaired = repair_switch_special_span_items(
            items,
            (items[0].data, items[1].data + b"BBBB", items[2].data),
            (plan,),
        )
        self.assertEqual(repaired[0][:4], b"\x09\xF0\x27\x00")
        self.assertEqual(
            int.from_bytes(repaired[0][:4], "little") & ((1 << 19) - 1),
            int.from_bytes(items[0].data, "little") & ((1 << 19) - 1),
        )

    def test_switch_special_branch09_rejects_non_multiple_of_four(self) -> None:
        items = (
            GroupedItem(0x100, b"\x09\xF0\x6F\x14"),
            GroupedItem(0x104, b"A" * 8),
            GroupedItem(0x10C, b"NEXT"),
        )
        plan = SwitchSpecialSpanPlan(
            kind="BRANCH_09",
            partition_index=0,
            opcode=0x09,
            original_start=0x100,
            original_span=12,
            original_target=0x10C,
            owner_item_index=0,
            owner_inner_offset=0,
            target_item_index=2,
        )
        with self.assertRaises(SelectiveEventError) as cm:
            repair_switch_special_span_items(
                items,
                (items[0].data, items[1].data + b"BB", items[2].data),
                (plan,),
            )
        self.assertEqual(cm.exception.code, "SPECIAL_SPAN_NOT_REPRESENTABLE")

    def test_false_event02_nonowner_constants_remain_excluded(self) -> None:
        self.assertEqual(
            FALSE_EVENT_02_EXPRESSION_ORIGINAL_STARTS,
            frozenset({0xAC470, 0x980C0}),
        )
        self.assertTrue(
            FALSE_EVENT_02_EXPRESSION_ORIGINAL_STARTS
            <= GENERIC_BRANCH_EXCLUDED_ORIGINAL_STARTS
        )


if __name__ == "__main__":
    unittest.main()
