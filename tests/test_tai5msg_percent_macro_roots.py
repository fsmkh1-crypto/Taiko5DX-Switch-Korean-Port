from pathlib import Path
import unittest

from builder.tai5msg_percent_macro_roots import (
    EXPECTED_PAYLOAD_DELTA,
    EXPECTED_ROOTS,
    PercentMacroRootError,
    load_v356_percent_macro_root_specs,
    resolve_v356_percent_macro_root_targets,
)


class PercentMacroRootUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_v356_manifest_integrity(self) -> None:
        specs = load_v356_percent_macro_root_specs(self.repo_root)
        self.assertEqual(len(specs), EXPECTED_ROOTS)
        self.assertEqual(sum(spec.delta for spec in specs.values()), EXPECTED_PAYLOAD_DELTA)
        self.assertTrue(all(block == 0 for block, _local in specs))
        self.assertNotIn((0, 10), specs)
        self.assertNotIn((0, 11), specs)

    def test_exact_source_target_guards(self) -> None:
        specs = load_v356_percent_macro_root_specs(self.repo_root)
        max_local = max(local for _block, local in specs)
        stock = [[b"x"] * (max_local + 1)]
        ko = [[b"y"] * (max_local + 1)]
        first = next(iter(specs.values()))
        stock[0][first.local] = b"x" * first.source_length
        ko[0][first.local] = b"y" * first.target_length
        with self.assertRaises(PercentMacroRootError):
            resolve_v356_percent_macro_root_targets(stock, ko, specs)


if __name__ == "__main__":
    unittest.main()
