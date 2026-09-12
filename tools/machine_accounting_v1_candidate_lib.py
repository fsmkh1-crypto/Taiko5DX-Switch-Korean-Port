from __future__ import annotations

import gzip
import io
import zlib
import hashlib
import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_sha256(obj) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw)


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _part_sort_key(name: str):
    m = re.fullmatch(r"part-(\d+)\.(jsonl|json)", name)
    return (0, int(m.group(1))) if m else (1, name)


def load_sharded_jsonl(directory: Path):
    idx_path = directory / "INDEX.json"
    require(idx_path.is_file(), f"missing index: {idx_path}")
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    parts = idx.get("parts", [])
    names = [p["file"] for p in parts]
    require(len(names) == len(set(names)), f"duplicate shard names in {idx_path}")
    require(names == sorted(names, key=_part_sort_key), f"reordered shard list in {idx_path}")

    actual_files = {p.name for p in directory.iterdir() if p.is_file()}
    expected_files = {"INDEX.json", *names}
    require(actual_files == expected_files, f"unindexed/missing files in {directory}: actual={sorted(actual_files)} expected={sorted(expected_files)}")

    rows = []
    logical = b""
    for part in parts:
        path = directory / part["file"]
        raw = path.read_bytes()
        require(sha256(raw) == part["sha256"], f"hash mismatch: {path}")
        lines = raw.decode("utf-8").splitlines(True)
        require(len(lines) == part["rows"], f"row count mismatch: {path}")
        logical += raw
        rows.extend(json.loads(line) for line in lines if line.strip())

    require(len(rows) == idx["total_rows"], f"total row mismatch: {directory}")
    require(sha256(logical) == idx["logical_content_sha256"], f"logical hash mismatch: {directory}")
    return rows, idx


def load_grouped_migration(directory: Path):
    idx_path = directory / "INDEX.json"
    require(idx_path.is_file(), f"missing index: {idx_path}")
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    parts = idx.get("parts", [])
    names = [p["file"] for p in parts]
    require(len(names) == len(set(names)), f"duplicate migration part names: {idx_path}")
    require(len({p["entity_type"] for p in parts}) == len(parts), f"duplicate migration entity_type: {idx_path}")
    actual_files = {p.name for p in directory.iterdir() if p.is_file()}
    expected_files = {"INDEX.json", *names}
    require(actual_files == expected_files, f"unindexed/missing migration files: actual={sorted(actual_files)} expected={sorted(expected_files)}")

    groups = {}
    logical_rows = []
    total = 0
    for part in parts:
        path = directory / part["file"]
        raw = path.read_bytes()
        require(sha256(raw) == part["sha256"], f"migration hash mismatch: {path}")
        obj = json.loads(raw)
        require(obj["entity_type"] == part["entity_type"], f"migration entity_type mismatch: {path}")
        ids = obj["entity_ids"]
        require(len(ids) == part["rows"], f"migration row count mismatch: {path}")
        require(len(ids) == len(set(ids)), f"duplicate migration entity id: {path}")
        groups[obj["entity_type"]] = ids
        logical_rows.extend((obj["entity_type"], entity_id) for entity_id in ids)
        total += len(ids)
    require(total == idx["total_entries"], f"migration total mismatch: {directory}")
    logical_hash = sha256("\n".join(f"{t}:{i}" for t, i in logical_rows).encode("utf-8"))
    return groups, idx, logical_hash


def _target_identity(seed):
    return {
        "family": "F1_LOCALIZATION_SEQUENCE",
        "localization_id": seed["localization_id"],
        "target_object": seed["target_object"],
        "segment_delta": seed["segment_delta"],
    }


def materialize_source_state(seed: dict, contract: dict) -> dict:
    category = seed["category"]
    require(category in contract["categories"], f"unknown source-state category {category}")
    rule = deepcopy(contract["categories"][category])
    state = {
        "source_id": seed["source_id"],
        "pc_record": seed["pc_record"],
        "revision": contract["revision"],
        "source_family": contract["source_family"],
        "accounting_role": contract["accounting_role"],
        "exclusion_claim_id": None,
        "changed_by": deepcopy(contract["changed_by"]),
        "supersedes_revision": None,
    }
    state.update({k: deepcopy(v) for k, v in rule.items() if k not in {"unknown"}})
    state["logical_owner_count"] = seed.get("logical_owner_count") if category != "REJECT" else None

    identity = _target_identity(seed)
    if category == "REJECT":
        state["target_identity"] = None
        state["candidate_target_identity"] = {**identity, "promotion_status": "F1_UNPROMOTED"}
    else:
        state["target_identity"] = identity
        state["candidate_target_identity"] = None

    state["unknown_fields"] = []
    if rule.get("unknown"):
        state["unknown_fields"].append(deepcopy(rule["unknown"]))
    return state


def materialize_action(row: dict, contract: dict) -> dict:
    cfg = contract["action_materialization"]
    required = [
        "authorization_action_id", "source_id", "action_family", "storage_class", "language_domain",
        "target_object", "write_start", "write_end_exclusive", "replacement_hex", "original_hex",
        "original_guard_exact", "terminator_mode", "terminator_preserved", "apply_priority",
        "action_status", "runtime_validation_required", "evidence_ids"
    ]
    missing = [k for k in required if k not in row]
    require(not missing, f"action manifest row missing fields: {missing}")
    return {
        "action_id": row["authorization_action_id"],
        "revision": cfg["revision"],
        "lifecycle_state": cfg["lifecycle_state"],
        "action_family": row["action_family"],
        "storage_class": row["storage_class"],
        "language_domain": row["language_domain"],
        "switch_object_or_code_sites": [{
            "target_object": row["target_object"],
            "write_start": row["write_start"],
            "write_end_exclusive": row["write_end_exclusive"],
        }],
        "input_source_ids": [row["source_id"]],
        "replacement_or_behavior": {"replacement_hex": row["replacement_hex"]},
        "guards": [
            {"type": "EXACT_ORIGINAL_BYTES", "original_hex": row["original_hex"], "pass": bool(row["original_guard_exact"])},
            {"type": "TERMINATOR_PRESERVATION", "mode": row["terminator_mode"], "pass": bool(row["terminator_preserved"])},
        ],
        "apply_priority": row["apply_priority"],
        "capacity_requirement": {"terminator_preserved": bool(row["terminator_preserved"])},
        "conflict_state": cfg["conflict_state"],
        "runtime_test_family": None,
        "runtime_validation_required": bool(row["runtime_validation_required"]),
        "status": row["action_status"],
        "claim_refs": deepcopy(cfg["claim_refs"]),
        "legacy_evidence_refs": list(row[cfg["legacy_evidence_refs_from"]]),
        "changed_by": deepcopy(cfg["changed_by"]),
        "supersedes_revision": None,
    }


def materialize_edge(seed: dict, contract: dict) -> dict:
    cfg = contract["edge_materialization"]
    return {
        "source_id": seed["source_id"],
        "action_id": seed["action_id"],
        "role": cfg["role"],
        "source_byte_range": cfg["source_byte_range"],
        "target_byte_range": cfg["target_byte_range"],
        "claim_refs": deepcopy(cfg["claim_refs"]),
        "legacy_evidence_refs": deepcopy(cfg["legacy_evidence_refs"]),
    }


def _new_claim_from(old: dict, spec: dict) -> dict:
    new = deepcopy(old)
    new["claim_id"] = spec["claim_id"]
    new["predicate"] = spec["predicate"]
    new["lifecycle_state"] = "ACTIVE"
    new["superseded_by"] = []
    new["supersedes"] = [old["claim_id"]]
    new["legacy_supersedes_refs"] = list(spec.get("legacy_supersedes_refs", []))
    if spec.get("copy_scalar_value"):
        new["value"] = deepcopy(old["value"])
    else:
        key = spec["value_key"]
        require(isinstance(old["value"], dict) and key in old["value"], f"missing value key {key} in {old['claim_id']}")
        new["value"] = deepcopy(old["value"][key])
    return new


def materialize_effective_claims(base_claims: list[dict], amendments: dict):
    by_id = {c["claim_id"]: deepcopy(c) for c in base_claims}
    require(len(by_id) == len(base_claims), "duplicate base claim IDs")
    new_claims = []
    for split in amendments["splits"]:
        old_id = split["claim_id"]
        require(old_id in by_id, f"amendment source claim missing: {old_id}")
        old = by_id[old_id]
        require(old["lifecycle_state"] == "ACTIVE", f"split source not ACTIVE: {old_id}")
        replacement_ids = [s["claim_id"] for s in split["new_claims"]]
        require(len(replacement_ids) == len(set(replacement_ids)), f"duplicate replacement claim IDs for {old_id}")
        old["lifecycle_state"] = "SUPERSEDED"
        old["superseded_by"] = replacement_ids
        legacy = [x for x in old.get("supersedes", []) if not re.fullmatch(r"V\d{3}\.C\d+", x)]
        old["legacy_supersedes_refs"] = list(dict.fromkeys(old.get("legacy_supersedes_refs", []) + legacy))
        old["supersedes"] = [x for x in old.get("supersedes", []) if re.fullmatch(r"V\d{3}\.C\d+", x)]
        for spec in split["new_claims"]:
            new_claims.append(_new_claim_from(old, spec))

    all_claims = list(by_id.values()) + new_claims
    ids = [c["claim_id"] for c in all_claims]
    require(len(ids) == len(set(ids)), "duplicate effective claim IDs")
    all_ids = set(ids)
    for claim in all_claims:
        require(re.fullmatch(r"V\d{3}\.C\d+", claim["claim_id"]) is not None, f"invalid claim ID: {claim['claim_id']}")
        for ref in claim.get("supersedes", []):
            require(ref in all_ids, f"claim supersedes unknown claim: {claim['claim_id']} -> {ref}")
        for ref in claim.get("superseded_by", []):
            require(ref in all_ids, f"claim superseded_by unknown claim: {claim['claim_id']} -> {ref}")
    return all_claims


def invariant_result(last_evaluated_against: dict, current: dict, previous_result: str = "PASS") -> str:
    if any(last_evaluated_against.get(k) != current.get(k) for k in last_evaluated_against):
        return "STALE"
    return previous_result


def coverage_status_allowed(assertion_bearing: bool, coverage_status: str, supersession_refs: list[str] | None = None) -> bool:
    supersession_refs = supersession_refs or []
    if not assertion_bearing:
        return coverage_status in {"NARRATIVE_ONLY", "NON_ASSERTION_METADATA", "EXTRACTED", "SUPERSEDED_TEXT"}
    if coverage_status == "EXTRACTED":
        return True
    if coverage_status == "SUPERSEDED_TEXT":
        return bool(supersession_refs)
    return False


def load_action_manifest(path: Path):
    raw = path.read_bytes()
    recovered_from_truncated_transport = False
    try:
        uncompressed = gzip.decompress(raw)
    except (EOFError, gzip.BadGzipFile, zlib.error):
        decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
        try:
            uncompressed = decoder.decompress(raw) + decoder.flush()
        except zlib.error as exc:
            raise ValidationError(f"action manifest gzip is not recoverable: {exc}") from exc
        require(bool(uncompressed), "action manifest gzip yielded no recoverable payload")
        recovered_from_truncated_transport = not decoder.eof
    rows = [json.loads(line) for line in uncompressed.decode("utf-8").splitlines() if line.strip()]
    out = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0, compresslevel=9) as gz:
        gz.write(uncompressed)
    canonical_gzip = out.getvalue()
    return raw, uncompressed, rows, recovered_from_truncated_transport, canonical_gzip


def semantic_rows_hash(rows: list[dict]) -> str:
    data = "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) for r in rows).encode("utf-8")
    return sha256(data)
