#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import io
import json
import re
import sys
from copy import deepcopy
from pathlib import Path

import validate_machine_accounting_schema_v1_candidate as base
from machine_accounting_v1_candidate_lib import ValidationError, require, sha256

_ORIGINAL_LOAD_ACTION_MANIFEST = base.load_action_manifest
_ORIGINAL_LOAD_SHARDED_JSONL = base.load_sharded_jsonl
_SOURCE_ANCHOR_OVERRIDES: dict[str, dict] = {}


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

    return index_raw, logical_bytes, rows, False, index_raw


def _repo_root_from_argv(argv: list[str]) -> Path:
    root = Path(".")
    for idx, arg in enumerate(argv):
        if arg == "--repo-root" and idx + 1 < len(argv):
            root = Path(argv[idx + 1])
        elif arg.startswith("--repo-root="):
            root = Path(arg.split("=", 1)[1])
    return root.resolve()


def _apply_source_anchor_overrides(claims: list[dict]) -> list[dict]:
    if not _SOURCE_ANCHOR_OVERRIDES:
        return claims
    out = []
    for claim in claims:
        item = deepcopy(claim)
        override = _SOURCE_ANCHOR_OVERRIDES.get(item.get("claim_id"))
        if override is not None:
            item["source_anchor"] = deepcopy(override)
        out.append(item)
    return out


def load_sharded_jsonl_v2(directory: Path):
    rows, index = _ORIGINAL_LOAD_SHARDED_JSONL(directory)
    if rows and any(isinstance(row, dict) and "claim_id" in row for row in rows):
        rows = _apply_source_anchor_overrides(rows)
    return rows, index


def configure_source_anchor_overrides(root: Path) -> None:
    global _SOURCE_ANCHOR_OVERRIDES

    candidate = root / "data/pilot/f1_v1_candidate"
    bindings = json.loads((candidate / "bindings.json").read_text(encoding="utf-8"))
    binding = bindings.get("source_anchor_overrides")
    require(isinstance(binding, dict), "missing source_anchor_overrides binding")
    path = root / binding["path"]
    require(path.is_file(), f"missing source-anchor override file: {path}")
    obj = json.loads(path.read_text(encoding="utf-8"))
    require(obj.get("schema") == "SOURCE_ANCHOR_OVERRIDES_V1_CANDIDATE", "unexpected source-anchor override schema")
    require(obj.get("semantic_schema_version") == bindings["semantic_schema_version"], "source-anchor override schema version mismatch")
    require(base.canonical_json_sha256(obj) == binding["canonical_json_sha256"], "source-anchor override canonical hash mismatch")

    entries = obj.get("overrides", [])
    ids = [entry["claim_id"] for entry in entries]
    require(len(ids) == len(set(ids)), "duplicate source-anchor override claim IDs")
    for entry in entries:
        require(isinstance(entry.get("reason"), str) and entry["reason"].strip(), f"source-anchor override missing reason: {entry.get('claim_id')}")
        anchor = entry.get("source_anchor")
        require(isinstance(anchor, dict), f"source-anchor override missing anchor: {entry['claim_id']}")
        require(set(anchor) == {
            "document_path", "document_git_blob_sha", "heading_path", "anchor_text", "anchor_text_sha256"
        }, f"source-anchor override malformed: {entry['claim_id']}")

    _SOURCE_ANCHOR_OVERRIDES = {
        entry["claim_id"]: deepcopy(entry["source_anchor"])
        for entry in entries
    }


def _heading_section(document_text: str, heading_path: str) -> str:
    if heading_path == "ROOT":
        return document_text

    lines = document_text.splitlines(keepends=True)
    headings = []
    for idx, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line.rstrip("\r\n"))
        if m:
            headings.append((idx, len(m.group(1)), m.group(2).strip()))

    def matches(title: str) -> bool:
        return title == heading_path or title.startswith(heading_path + " ")

    found = [(idx, level, title) for idx, level, title in headings if matches(title)]
    require(len(found) == 1, f"heading_path resolution failed: {heading_path!r} matches={[(x[0], x[2]) for x in found]}")
    start, level, _ = found[0]
    end = len(lines)
    for idx, next_level, _ in headings:
        if idx > start and next_level <= level:
            end = idx
            break
    return "".join(lines[start:end])


def validate_effective_source_anchors(root: Path) -> None:
    candidate = root / "data/pilot/f1_v1_candidate"
    bindings = json.loads((candidate / "bindings.json").read_text(encoding="utf-8"))
    amendments = json.loads((candidate / "claim_amendments.json").read_text(encoding="utf-8"))

    base_claims, _ = base.load_sharded_jsonl(root / bindings["base_claims"]["path"])
    claims = base.materialize_effective_claims(base_claims, amendments)
    claims = _apply_source_anchor_overrides(claims)

    all_ids = {claim["claim_id"] for claim in claims}
    require(set(_SOURCE_ANCHOR_OVERRIDES) <= all_ids,
            f"source-anchor override references unknown claim: {sorted(set(_SOURCE_ANCHOR_OVERRIDES) - all_ids)}")

    doc_cache: dict[Path, tuple[bytes, str]] = {}
    for claim in claims:
        anchor = claim.get("source_anchor")
        require(isinstance(anchor, dict), f"claim missing source_anchor: {claim['claim_id']}")
        path = root / anchor["document_path"]
        require(path.is_file(), f"anchor document missing for {claim['claim_id']}: {path}")
        if path not in doc_cache:
            raw = path.read_bytes()
            doc_cache[path] = (raw, raw.decode("utf-8"))
        raw_doc, text = doc_cache[path]

        require(base.git_blob_sha1(raw_doc) == anchor["document_git_blob_sha"],
                f"anchor_blob_{claim['claim_id']}")
        require(sha256(anchor["anchor_text"].encode("utf-8")) == anchor["anchor_text_sha256"],
                f"anchor_text_hash_{claim['claim_id']}")
        section = _heading_section(text, anchor["heading_path"])
        require(anchor["anchor_text"] in section,
                f"anchor_text_in_heading_{claim['claim_id']}: heading={anchor['heading_path']!r}")

    require(len(claims) == 97, f"effective source-anchor audit expected 97 claims, got {len(claims)}")


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
base.load_sharded_jsonl = load_sharded_jsonl_v2

if __name__ == "__main__":
    repo_root = _repo_root_from_argv(sys.argv[1:])
    configure_source_anchor_overrides(repo_root)
    validate_structured_claim_registry(repo_root)
    validate_effective_source_anchors(repo_root)
    raise SystemExit(base.main())
