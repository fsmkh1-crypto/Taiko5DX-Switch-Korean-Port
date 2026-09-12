#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_machine_accounting_schema_v1_candidate import (
    VALIDATION_EXCEPTIONS,
    _write_result,
    impact_report,
    validate_candidate,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect-all machine-gate diagnostic for the schema-v1 candidate."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path)
    parser.add_argument(
        "--changed-namespace",
        action="append",
        default=[],
        help="Report dependency impact only. Repeat for multiple changed namespaces.",
    )
    args = parser.parse_args()

    if args.changed_namespace:
        result = impact_report(set(args.changed_namespace))
        output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        print(output, end="")
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
        return 0

    try:
        result, code = validate_candidate(args.repo_root, mode="collect_all")
    except VALIDATION_EXCEPTIONS as exc:
        result, code = {
            "schema": "MACHINE_ACCOUNTING_SCHEMA_V1_CANDIDATE_VALIDATION",
            "mode": "COLLECT_ALL_MACHINE_GATES",
            "result": "DIAGNOSTIC_ISSUES",
            "semantic_reanalysis": False,
            "error": str(exc),
        }, 1
    _write_result(result, args.out)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
