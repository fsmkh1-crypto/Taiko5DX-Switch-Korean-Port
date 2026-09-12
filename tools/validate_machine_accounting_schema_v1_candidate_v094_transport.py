#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import io
import json
import re
import sys
from pathlib import Path

import validate_machine_accounting_schema_v1_candidate as base
from machine_accounting_v1_candidate_lib import ValidationError, require, sha256

_ORIGINAL_LOAD_ACTION_MANIFEST = base.load_action_manifest


def _part_sort_key(name: str):
    m = re.fullmatch(r"part-(\d+)\.jsonl", name)
    return int(m.group(1)) if m else None


def load_action_manifest_v2(path: Path):
    if not path.is_dir():
        return _ORIGINAL_LOAD_ACTION_MANIFEST(path)

    index_path = path / "INDEX.json"
    require(index_path.is_file(), f"missing V094 transport index: {index_path}")
    index_raw = index_path.read_bytes()
    index = json.loads(index_raw.decode("utf-8"))

    require(index.get("schema") == "V094_STATIC_AUTHORIZATION_TRANSPORT_V1", "unexpected V094 transport schema")
    semantic = index["semantic_identity"]
    current = index["current_transport"]
    historical = index["historical_transport"]
    parts = current["parts"]

    require(current["format"] == "PLAIN_JSONL_SHARDS", "unexpected V094 current transport format")
    require(current["shard_count"] == len(parts), "V094 shard_count mismatch")

    names = [part["name"] for part in parts]
    numeric = [_part_sort_key(name) for name in names]
    require(all(value is not None for value in numeric), "invalid V094 shard name")
    require(numeric == list(range(1, len(parts) + 1)), "V094 shard order is not contiguous")
    require(len(names) == len(set(names)), "duplicate V094 shard name")

    actual_files = {p.name for p in path.iterdir() if p.is_file()}
    expected_files = {"INDEX.json", *names}
    require(actual_files == expected_files, f"unindexed/missing V094 shards: actual={sorted(actual_files)} expected={sorted(expected_files)}")

    rows = []
    logical = bytearray()
    for part in parts:
        shard_path = path / part["name"]
        raw = shard_path.read_bytes()
        require(len(raw) == part["bytes"], f"V094 shard byte count mismatch: {shard_path}")
        require(sha256(raw) == part["sha256"], f"V094 shard hash mismatch: {shard_path}")
        require(raw.endswith(b"\n"), f"V094 shard final row is not LF-terminated: {shard_path}")
        lines = raw.decode("utf-8").splitlines(True)
        require(len(lines) == part["rows"], f"V094 shard row count mismatch: {shard_path}")
        parsed = [json.loads(line) for line in lines if line.strip()]
        require(len(parsed) == part["rows"], f"V094 shard parsed row count mismatch: {shard_path}")
        require(parsed[0]["authorization_action_id"] == part["first_action_id"], f"V094 first action mismatch: {shard_path}")
        require(parsed[-1]["authorization_action_id"] == part["last_action_id"], f"V094 last action mismatch: {shard_path}")
        rows.extend(parsed)
        logical.extend(raw)

    logical_bytes = bytes(logical)
    require(len(rows) == semantic["rows"] == 158, "V094 total action row mismatch")
    require(sha256(logical_bytes) == semantic["logical_content_sha256"], "V094 logical content hash mismatch")
    source_ids_hash = hashlib.sha256("\n".join(row["source_id"] for row in rows).encode("utf-8")).hexdigest()
    require(source_ids_hash == semantic["ordered_source_ids_sha256"], "V094 ordered source-ID hash mismatch")

    out = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0, compresslevel=9) as gz:
        gz.write(logical_bytes)
    historical_gzip = out.getvalue()
    require(sha256(historical_gzip) == historical["gzip_sha256"], "V094 historical gzip provenance mismatch")

    # Compatibility tuple for the existing candidate validator:
    # current transport root identity is INDEX.json, while the historical gzip
    # identity is verified above as independent provenance.
    return index_raw, logical_bytes, rows, False, index_raw


def _repo_root_from_argv(argv: list[str]) -> Path:
    root = Path(".")
    for idx, arg in enumerate(argv):
        if arg == "--repo-root" and idx + 1 < len(argv):
            root = Path(argv[idx + 1])
        elif arg.startswith("--repo-root="):
            root = Path(arg.split("=", 1)[1])
    return root.resolve()


def validate_structured_claim_registry(root: Path) -> None:
    candidate = root / "data/pilot/f1_v1_candidate"
    bindings = json.loads((candidate / "bindings.json").read_text(encoding="utf-8"))
    amendments = json.loads((candidate / "claim_amendments.json").read_text(encoding="utf-8"))

    base_claims, _ = base.load_sharded_jsonl(root / bindings["base_claims"]["path"])
    claims = base.materialize_effective_claims(base_claims, amendments)

    entries = amendments.get("structured_atomic_exceptions", [])
    registry_ids = [entry["claim_id"] for entry in entries]
    require(len(registry_ids) == len(set(registry_ids)), "duplicate structured-claim registry IDs")
    require(all(isinstance(entry.get("reason"), str) and entry["reason"].strip() for entry in entries),
            "structured-claim registry entry missing reason")

    active_structured = {
        claim["claim_id"]
        for claim in claims
        if claim["lifecycle_state"] == "ACTIVE"
        and isinstance(claim.get("value"), (dict, list))
    }
    registry = set(registry_ids)

    require(
        active_structured == registry,
        "structured-claim registry mismatch: "
        f"unclassified={sorted(active_structured - registry)} "
        f"non_active_or_scalar={sorted(registry - active_structured)}"
    )

    split_sources = {split["claim_id"] for split in amendments["splits"]}
    require(not (split_sources & registry),
            f"claim cannot be both split and ATOMIC_STRUCTURED: {sorted(split_sources & registry)}")


base.load_action_manifest = load_action_manifest_v2

if __name__ == "__main__":
    validate_structured_claim_registry(_repo_root_from_argv(sys.argv[1:]))
    raise SystemExit(base.main())
