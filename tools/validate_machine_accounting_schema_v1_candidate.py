#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path

from machine_accounting_v1_candidate_lib import (
    ValidationError,
    canonical_json_sha256,
    coverage_status_allowed,
    git_blob_sha1,
    invariant_result,
    load_action_manifest as load_legacy_action_manifest,
    load_grouped_migration,
    load_sharded_jsonl,
    materialize_action,
    materialize_edge,
    materialize_effective_claims,
    materialize_source_state,
    semantic_rows_hash,
    sha256,
)

VALIDATION_EXCEPTIONS = (ValidationError, KeyError, ValueError, OSError, json.JSONDecodeError)

# These are machine-gate dependency namespaces, not invitations to reanalyse
# already-VERIFIED historical technical facts.
GROUP_NAMESPACE_DEPENDENCIES = {
    "configuration": {"schema_rules", "bindings", "materialization_contract", "claim_amendments", "fixtures"},
    "source_materialization": {"source_seed", "bindings", "materialization_contract"},
    "membership": {"source_seed", "membership_snapshot", "bindings"},
    "action_materialization": {"action_transport", "action_binding", "bindings", "materialization_contract"},
    "edge_materialization": {"edge_seed", "action_transport", "bindings", "materialization_contract"},
    "claims": {"claims_seed", "claim_amendments", "bindings", "materialization_contract"},
    "source_anchors": {"claims_seed", "claim_amendments", "source_anchor_overrides", "canonical_evidence_docs"},
    "unknowns": {"source_seed", "claim_amendments", "materialization_contract"},
    "coverage": {"coverage_seed", "fixtures"},
    "migration": {"migration_seed", "claim_amendments", "bindings", "fixtures"},
    "roundtrip": {"coverage_seed", "canonical_evidence_docs"},
    "progress": {"source_seed", "materialization_contract"},
    "semantic_hashes": {"source_seed", "edge_seed", "action_transport", "claims_seed", "claim_amendments", "source_anchor_overrides", "materialization_contract"},
}

GROUP_DEPENDENCIES = {
    "configuration": set(),
    "source_materialization": {"configuration"},
    "membership": {"source_materialization"},
    "action_materialization": {"configuration"},
    "edge_materialization": {"source_materialization", "action_materialization"},
    "claims": {"configuration"},
    "source_anchors": {"claims"},
    "unknowns": {"source_materialization", "action_materialization", "edge_materialization", "claims"},
    "coverage": {"configuration"},
    "migration": {"configuration", "claims"},
    "roundtrip": {"coverage"},
    "progress": {"source_materialization"},
    "semantic_hashes": {"source_materialization", "action_materialization", "edge_materialization", "claims"},
}


class GateCollector:
    def __init__(self, mode: str) -> None:
        if mode not in {"fail_fast", "collect_all"}:
            raise ValueError(f"unsupported validation mode: {mode}")
        self.mode = mode
        self.checks: dict[str, dict] = {}
        self.groups: dict[str, str] = {}
        self._current_group: str | None = None

    def start_group(self, name: str) -> bool:
        deps = GROUP_DEPENDENCIES.get(name, set())
        blocked_by = sorted(dep for dep in deps if self.groups.get(dep) != "PASS")
        if blocked_by:
            self.groups[name] = "BLOCKED"
            self.checks[f"group_{name}"] = {
                "status": "BLOCKED",
                "detail": {"blocked_by": blocked_by},
            }
            return False
        self._current_group = name
        return True

    def end_group(self, name: str) -> None:
        if self.groups.get(name) == "BLOCKED":
            return
        prefix = f"{name}:"
        statuses = [v["status"] for k, v in self.checks.items() if k.startswith(prefix)]
        self.groups[name] = "FAIL" if "FAIL" in statuses else "PASS"
        self._current_group = None

    def check(self, name: str, condition: bool, detail=None) -> bool:
        key = f"{self._current_group}:{name}" if self._current_group else name
        if condition:
            self.checks[key] = {"status": "PASS", "detail": detail}
            return True
        self.checks[key] = {"status": "FAIL", "detail": detail}
        if self.mode == "fail_fast":
            raise ValidationError(f"{name}: {detail}")
        return False

    def fail_group(self, name: str, exc: Exception) -> None:
        self.groups[name] = "FAIL"
        self.checks[f"group_{name}"] = {"status": "FAIL", "detail": str(exc)}
        self._current_group = None
        if self.mode == "fail_fast":
            raise exc

    def summary(self) -> dict[str, int]:
        counts = Counter(item["status"] for item in self.checks.values())
        return {status: counts.get(status, 0) for status in ("PASS", "FAIL", "BLOCKED", "STALE")}


def _run_group(gates: GateCollector, name: str, fn) -> None:
    if not gates.start_group(name):
        return
    try:
        fn()
        gates.end_group(name)
    except VALIDATION_EXCEPTIONS as exc:
        gates.fail_group(name, exc)


def _part_sort_key(name: str):
    match = re.fullmatch(r"part-(\d+)\.jsonl", name)
    return int(match.group(1)) if match else None


def load_action_manifest_current(path: Path):
    if not path.is_dir():
        return load_legacy_action_manifest(path)

    index_path = path / "INDEX.json"
    if not index_path.is_file():
        raise ValidationError(f"missing V094 transport index: {index_path}")
    index_raw = index_path.read_bytes()
    index = json.loads(index_raw.decode("utf-8"))
    if index.get("schema") != "V094_STATIC_AUTHORIZATION_TRANSPORT_V1":
        raise ValidationError("unexpected V094 transport schema")

    semantic = index["semantic_identity"]
    current = index["current_transport"]
    historical = index["historical_transport"]
    parts = current["parts"]
    if current.get("format") != "PLAIN_JSONL_SHARDS":
        raise ValidationError("unexpected V094 current transport format")
    if current.get("shard_count") != len(parts):
        raise ValidationError("V094 shard_count mismatch")

    names = [part["name"] for part in parts]
    numeric = [_part_sort_key(name) for name in names]
    if any(value is None for value in numeric) or numeric != list(range(1, len(parts) + 1)):
        raise ValidationError("V094 shard order is not contiguous")
    if len(names) != len(set(names)):
        raise ValidationError("duplicate V094 shard name")

    actual_files = {entry.name for entry in path.iterdir() if entry.is_file()}
    expected_files = {"INDEX.json", *names}
    if actual_files != expected_files:
        raise ValidationError(
            f"unindexed/missing V094 shards: actual={sorted(actual_files)} expected={sorted(expected_files)}"
        )

    rows: list[dict] = []
    logical = bytearray()
    for part in parts:
        shard_path = path / part["name"]
        raw = shard_path.read_bytes()
        if len(raw) != part["bytes"]:
            raise ValidationError(f"V094 shard byte count mismatch: {shard_path}")
        if sha256(raw) != part["sha256"]:
            raise ValidationError(f"V094 shard hash mismatch: {shard_path}")
        if not raw.endswith(b"\n"):
            raise ValidationError(f"V094 shard final row is not LF-terminated: {shard_path}")
        lines = raw.decode("utf-8").splitlines(True)
        if len(lines) != part["rows"]:
            raise ValidationError(f"V094 shard row count mismatch: {shard_path}")
        parsed = [json.loads(line) for line in lines if line.strip()]
        if len(parsed) != part["rows"]:
            raise ValidationError(f"V094 shard parsed row count mismatch: {shard_path}")
        if parsed[0]["authorization_action_id"] != part["first_action_id"]:
            raise ValidationError(f"V094 first action mismatch: {shard_path}")
        if parsed[-1]["authorization_action_id"] != part["last_action_id"]:
            raise ValidationError(f"V094 last action mismatch: {shard_path}")
        rows.extend(parsed)
        logical.extend(raw)

    logical_bytes = bytes(logical)
    if len(rows) != semantic["rows"] or len(rows) != 158:
        raise ValidationError("V094 total action row mismatch")
    if sha256(logical_bytes) != semantic["logical_content_sha256"]:
        raise ValidationError("V094 logical content hash mismatch")
    source_ids_hash = hashlib.sha256("\n".join(row["source_id"] for row in rows).encode("utf-8")).hexdigest()
    if source_ids_hash != semantic["ordered_source_ids_sha256"]:
        raise ValidationError("V094 ordered source-ID hash mismatch")

    out = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0, compresslevel=9) as gz:
        gz.write(logical_bytes)
    historical_gzip = out.getvalue()
    if sha256(historical_gzip) != historical["gzip_sha256"]:
        raise ValidationError("V094 historical gzip provenance mismatch")

    # For current transport, the INDEX bytes are the repository transport identity.
    return index_raw, logical_bytes, rows, False, index_raw


def _load_source_anchor_overrides(root: Path, bindings: dict) -> dict[str, dict]:
    binding = bindings.get("source_anchor_overrides")
    if not isinstance(binding, dict):
        raise ValidationError("missing source_anchor_overrides binding")
    path = root / binding["path"]
    if not path.is_file():
        raise ValidationError(f"missing source-anchor override file: {path}")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schema") != "SOURCE_ANCHOR_OVERRIDES_V1_CANDIDATE":
        raise ValidationError("unexpected source-anchor override schema")
    if obj.get("semantic_schema_version") != bindings["semantic_schema_version"]:
        raise ValidationError("source-anchor override schema version mismatch")
    if canonical_json_sha256(obj) != binding["canonical_json_sha256"]:
        raise ValidationError("source-anchor override canonical hash mismatch")
    entries = obj.get("overrides", [])
    ids = [entry["claim_id"] for entry in entries]
    if len(ids) != len(set(ids)):
        raise ValidationError("duplicate source-anchor override claim IDs")
    out: dict[str, dict] = {}
    for entry in entries:
        if not isinstance(entry.get("reason"), str) or not entry["reason"].strip():
            raise ValidationError(f"source-anchor override missing reason: {entry.get('claim_id')}")
        anchor = entry.get("source_anchor")
        if not isinstance(anchor, dict):
            raise ValidationError(f"source-anchor override missing anchor: {entry['claim_id']}")
        expected_fields = {
            "document_path", "document_git_blob_sha", "heading_path", "anchor_text", "anchor_text_sha256"
        }
        if set(anchor) != expected_fields:
            raise ValidationError(f"source-anchor override malformed: {entry['claim_id']}")
        out[entry["claim_id"]] = deepcopy(anchor)
    return out


def _apply_source_anchor_overrides(claims: list[dict], overrides: dict[str, dict]) -> list[dict]:
    result = []
    for claim in claims:
        item = deepcopy(claim)
        if item["claim_id"] in overrides:
            item["source_anchor"] = deepcopy(overrides[item["claim_id"]])
        result.append(item)
    return result


def _heading_section(document_text: str, heading_path: str) -> str:
    if heading_path == "ROOT":
        return document_text
    lines = document_text.splitlines(keepends=True)
    headings: list[tuple[int, int, str]] = []
    for idx, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line.rstrip("\r\n"))
        if match:
            headings.append((idx, len(match.group(1)), match.group(2).strip()))

    def matches(title: str) -> bool:
        return title == heading_path or title.startswith(heading_path + " ")

    found = [(idx, level, title) for idx, level, title in headings if matches(title)]
    if len(found) != 1:
        raise ValidationError(
            f"heading_path resolution failed: {heading_path!r} matches={[(item[0], item[2]) for item in found]}"
        )
    start, level, _ = found[0]
    end = len(lines)
    for idx, next_level, _ in headings:
        if idx > start and next_level <= level:
            end = idx
            break
    return "".join(lines[start:end])


def impact_report(changed_namespaces: set[str]) -> dict:
    direct = {
        group for group, namespaces in GROUP_NAMESPACE_DEPENDENCIES.items()
        if namespaces & changed_namespaces
    }
    stale = set(direct)
    changed = True
    while changed:
        changed = False
        for group, deps in GROUP_DEPENDENCIES.items():
            if group not in stale and deps & stale:
                stale.add(group)
                changed = True
    all_groups = set(GROUP_NAMESPACE_DEPENDENCIES)
    return {
        "schema": "MACHINE_ACCOUNTING_SCHEMA_V1_CANDIDATE_IMPACT",
        "result": "IMPACT_ONLY",
        "changed_namespaces": sorted(changed_namespaces),
        "stale_groups": sorted(stale),
        "unaffected_groups": sorted(all_groups - stale),
        "semantic_reanalysis": False,
        "note": "STALE marks machine-gate dependencies only; previously VERIFIED historical technical facts are not reopened without a legitimate revalidation trigger.",
    }


def validate_candidate(root: Path, mode: str = "fail_fast") -> tuple[dict, int]:
    root = root.resolve()
    gates = GateCollector(mode)
    ctx: dict = {}

    def configuration() -> None:
        candidate = root / "data/pilot/f1_v1_candidate"
        bindings = json.loads((candidate / "bindings.json").read_text(encoding="utf-8"))
        contract = json.loads((candidate / "materialization_contract.json").read_text(encoding="utf-8"))
        amendments = json.loads((candidate / "claim_amendments.json").read_text(encoding="utf-8"))
        fixture = json.loads((root / "tests/fixtures/machine_accounting_schema_v1.json").read_text(encoding="utf-8"))
        overrides = _load_source_anchor_overrides(root, bindings)
        gates.check("semantic_schema_version", bindings["semantic_schema_version"] == "1.0-candidate.1")
        gates.check("transport_version_separate", bindings["transport_format_version"] == "F1_PILOT_TRANSPORT_V0_1")
        gates.check("contract_hash", canonical_json_sha256(contract) == bindings["materialization_contract"]["canonical_json_sha256"])
        gates.check("amendment_hash", canonical_json_sha256(amendments) == bindings["claim_amendments"]["canonical_json_sha256"])
        ctx.update(candidate=candidate, bindings=bindings, contract=contract, amendments=amendments, fixture=fixture, overrides=overrides)

    _run_group(gates, "configuration", configuration)

    def source_materialization() -> None:
        bindings = ctx["bindings"]
        contract = ctx["contract"]
        seed_states, state_idx = load_sharded_jsonl(root / bindings["source_state_seed"]["path"])
        states = [materialize_source_state(row, contract) for row in seed_states]
        expected = bindings["expected_counts"]
        gates.check("state_seed_hash", state_idx["logical_content_sha256"] == bindings["source_state_seed"]["logical_content_sha256"])
        gates.check("sources_278", len(states) == expected["sources"] == len({item["source_id"] for item in states}))
        gates.check("accounting_role_obligation", all(item["accounting_role"] == "OBLIGATION" for item in states))
        gates.check("revision1_migration", all(item["revision"] == 1 and item["changed_by"]["type"] == "MIGRATION" for item in states))
        gates.check("no_exclusions", all(item["applicability_state"] == "APPLICABLE" and item["exclusion_claim_id"] is None for item in states))
        gates.check("resolved_262", sum(item["target_status"] == "RESOLVED" for item in states) == 262)
        gates.check("analyzed_unresolved_16", sum(item["analysis_state"] == "ANALYZED_UNRESOLVED" for item in states) == 16)
        gates.check("closed_158", sum(item["closure_state"] == "CLOSED" for item in states) == 158)
        blockers = Counter(item["blocker"] or "NONE" for item in states)
        gates.check("blocker_distribution", blockers == Counter({
            "NONE": 158,
            "PADDING_RECONSTRUCTION_REQUIRED": 75,
            "SHARED_OWNER_BINDING_REQUIRED": 25,
            "TERMINATOR_CAPACITY_FAIL": 4,
            "F1_RULE_REJECTED_MIN_FINAL_INTERVAL": 16,
        }), dict(blockers))
        ctx.update(seed_states=seed_states, states=states, state_idx=state_idx, expected=expected)

    _run_group(gates, "source_materialization", source_materialization)

    def membership() -> None:
        bindings = ctx["bindings"]
        states = ctx["states"]
        seed_states = ctx["seed_states"]
        mem = json.loads((root / bindings["membership_snapshot"]["path"]).read_text(encoding="utf-8"))
        all_ids_hash = sha256("\n".join(item["source_id"] for item in states).encode("utf-8"))
        gates.check("exact_source_membership_hash", all_ids_hash == bindings["membership_snapshot"]["all_source_ids_sha256"], all_ids_hash)
        category_key = {
            "DIRECT": "DIRECT_PORT_AUTHORIZED",
            "REJECT": "F1_RULE_REJECTED",
            "PADDING": "PADDING_RECONSTRUCTION_REQUIRED",
            "SHARED": "SHARED_OWNER_BINDING_REQUIRED",
            "CAPACITY": "TERMINATOR_CAPACITY_FAIL",
        }
        for category, snapshot_key in category_key.items():
            actual = [seed["pc_record"] for seed in seed_states if seed["category"] == category]
            gates.check(
                f"exact_membership_{category}",
                actual == mem["pc_records"][snapshot_key],
                {"actual": len(actual), "expected": len(mem["pc_records"][snapshot_key])},
            )
        ctx["membership_snapshot"] = mem

    _run_group(gates, "membership", membership)

    def action_materialization() -> None:
        bindings = ctx["bindings"]
        contract = ctx["contract"]
        expected = ctx["expected"]
        action_binding = json.loads((root / bindings["action_table"]["binding_path"]).read_text(encoding="utf-8"))
        manifest_path = root / bindings["action_table"]["manifest_path"]
        raw, uncompressed, manifest_rows, recovered, canonical_transport = load_action_manifest_current(manifest_path)
        repository_sha = sha256(raw)
        transport_exact = repository_sha == bindings["action_table"]["current_transport_index_sha256"]
        gates.check(
            "action_current_transport_index_hash",
            sha256(canonical_transport) == bindings["action_table"]["current_transport_index_sha256"],
            sha256(canonical_transport),
        )
        gates.check("action_content_hash", sha256(uncompressed) == bindings["action_table"]["manifest_content_sha256"], sha256(uncompressed))
        gates.check(
            "action_binding_consistency",
            action_binding["current_transport"]["index_sha256"] == bindings["action_table"]["current_transport_index_sha256"]
            and action_binding["current_transport"]["format"] == bindings["action_table"]["current_transport_format"]
            and action_binding["manifest_file_sha256"] == action_binding["current_transport"]["index_sha256"]
            and action_binding["manifest_file_sha256_semantics"] == "CURRENT_TRANSPORT_ROOT_INDEX_SHA256_COMPATIBILITY_FIELD"
            and action_binding["manifest_content_sha256"] == bindings["action_table"]["manifest_content_sha256"]
            and action_binding["historical_transport"]["gzip_sha256"] == bindings["action_table"]["historical_gzip_sha256"],
        )
        actions = [materialize_action(row, contract) for row in manifest_rows]
        gates.check("actions_158", len(actions) == expected["actions"] == len({item["action_id"] for item in actions}))
        gates.check("action_sources_unique", len({item["input_source_ids"][0] for item in actions}) == 158)
        gates.check("action_required_semantics", all(
            item["conflict_state"] == "NONE"
            and item["guards"][0]["pass"]
            and item["guards"][1]["pass"]
            and item["storage_class"] == "STATIC_RODATA"
            and item["language_domain"] == "JP_ONLY"
            for item in actions
        ))
        ctx.update(
            action_binding=action_binding,
            manifest_rows=manifest_rows,
            actions=actions,
            action_repository_file_sha256=repository_sha,
            action_transport_exact=transport_exact,
            manifest_transport_recovered=recovered,
        )

    _run_group(gates, "action_materialization", action_materialization)

    def edge_materialization() -> None:
        bindings = ctx["bindings"]
        contract = ctx["contract"]
        expected = ctx["expected"]
        edge_seeds, edge_idx = load_sharded_jsonl(root / bindings["source_action_edge_seed"]["path"])
        gates.check("edge_seed_hash", edge_idx["logical_content_sha256"] == bindings["source_action_edge_seed"]["logical_content_sha256"])
        edges = [materialize_edge(row, contract) for row in edge_seeds]
        actions = ctx["actions"]
        states = ctx["states"]
        edge_pairs = [(item["source_id"], item["action_id"]) for item in edges]
        action_pairs = [(item["input_source_ids"][0], item["action_id"]) for item in actions]
        gates.check("edges_158", len(edges) == expected["edges"])
        gates.check("edge_full_materialization", all(set(item) == {"source_id", "action_id", "role", "source_byte_range", "target_byte_range", "claim_refs", "legacy_evidence_refs"} for item in edges))
        gates.check("edges_match_actions", edge_pairs == action_pairs)
        gates.check("edges_primary", all(item["role"] == "PRIMARY" for item in edges))
        closed_sources = {item["source_id"] for item in states if item["closure_state"] == "CLOSED"}
        gates.check("actions_only_closed", {item["input_source_ids"][0] for item in actions} == closed_sources)
        ctx.update(edge_seeds=edge_seeds, edge_idx=edge_idx, edges=edges)

    _run_group(gates, "edge_materialization", edge_materialization)

    def claims_group() -> None:
        bindings = ctx["bindings"]
        amendments = ctx["amendments"]
        expected = ctx["expected"]
        base_claims, claim_idx = load_sharded_jsonl(root / bindings["base_claims"]["path"])
        gates.check("base_claim_hash", claim_idx["logical_content_sha256"] == bindings["base_claims"]["logical_content_sha256"])
        claims = materialize_effective_claims(base_claims, amendments)
        claims = _apply_source_anchor_overrides(claims, ctx["overrides"])
        all_claim_ids = {item["claim_id"] for item in claims}
        active_claim_ids = {item["claim_id"] for item in claims if item["lifecycle_state"] == "ACTIVE"}
        gates.check("base_claim_count", len(base_claims) == expected["base_claims"])
        gates.check("new_claim_count", len(claims) - len(base_claims) == expected["new_claims"])
        gates.check("effective_claim_count", len(claims) == expected["effective_claims"])
        gates.check("active_claim_count", len(active_claim_ids) == expected["active_claims"])
        split_sources = {item["claim_id"] for item in amendments["splits"]}
        gates.check("split_sources_superseded", all(next(claim for claim in claims if claim["claim_id"] == claim_id)["lifecycle_state"] == "SUPERSEDED" for claim_id in split_sources))
        gates.check("active_claim_referential_integrity", all(
            ref in all_claim_ids
            for claim in claims
            for ref in claim.get("supersedes", []) + claim.get("superseded_by", [])
        ))
        registry_entries = amendments.get("structured_atomic_exceptions", [])
        registry_ids = [entry["claim_id"] for entry in registry_entries]
        gates.check("structured_registry_unique", len(registry_ids) == len(set(registry_ids)))
        gates.check("structured_registry_reasons", all(isinstance(entry.get("reason"), str) and entry["reason"].strip() for entry in registry_entries))
        active_structured = {
            claim["claim_id"] for claim in claims
            if claim["lifecycle_state"] == "ACTIVE" and isinstance(claim.get("value"), (dict, list))
        }
        registry = set(registry_ids)
        gates.check(
            "atomic_claim_policy",
            active_structured == registry,
            {"unclassified": sorted(active_structured - registry), "non_active_or_scalar": sorted(registry - active_structured)},
        )
        gates.check("structured_split_disjoint", not (split_sources & registry), sorted(split_sources & registry))
        ctx.update(
            base_claims=base_claims,
            claim_idx=claim_idx,
            claims=claims,
            all_claim_ids=all_claim_ids,
            active_claim_ids=active_claim_ids,
            split_sources=split_sources,
        )

    _run_group(gates, "claims", claims_group)

    def source_anchors() -> None:
        claims = ctx["claims"]
        overrides = ctx["overrides"]
        all_ids = {claim["claim_id"] for claim in claims}
        gates.check("override_ids_resolve", set(overrides) <= all_ids, sorted(set(overrides) - all_ids))
        doc_cache: dict[Path, tuple[bytes, str]] = {}
        for claim in claims:
            anchor = claim.get("source_anchor")
            if not isinstance(anchor, dict):
                gates.check(f"anchor_present_{claim['claim_id']}", False, "missing source_anchor")
                continue
            path = root / anchor["document_path"]
            if not path.is_file():
                gates.check(f"anchor_document_{claim['claim_id']}", False, str(path))
                continue
            if path not in doc_cache:
                raw = path.read_bytes()
                doc_cache[path] = (raw, raw.decode("utf-8"))
            raw_doc, text = doc_cache[path]
            gates.check(f"anchor_blob_{claim['claim_id']}", git_blob_sha1(raw_doc) == anchor["document_git_blob_sha"])
            gates.check(f"anchor_text_hash_{claim['claim_id']}", sha256(anchor["anchor_text"].encode("utf-8")) == anchor["anchor_text_sha256"])
            try:
                section = _heading_section(text, anchor["heading_path"])
            except ValidationError as exc:
                gates.check(f"anchor_heading_{claim['claim_id']}", False, str(exc))
                continue
            gates.check(f"anchor_text_in_heading_{claim['claim_id']}", anchor["anchor_text"] in section, anchor["heading_path"])
        gates.check("effective_source_anchor_count", len(claims) == 97, len(claims))

    _run_group(gates, "source_anchors", source_anchors)

    def unknowns() -> None:
        states = ctx["states"]
        active_claim_ids = ctx["active_claim_ids"]
        actions = ctx["actions"]
        edges = ctx["edges"]
        gates.check("active_claim_refs_from_state", all(ref in active_claim_ids for state in states for ref in state.get("claim_refs", [])))
        gates.check("active_claim_refs_from_actions", all(ref in active_claim_ids for action in actions for ref in action.get("claim_refs", [])))
        gates.check("active_claim_refs_from_edges", all(ref in active_claim_ids for edge in edges for ref in edge.get("claim_refs", [])))
        by_field = Counter()
        blocked: set[str] = set()
        for state in states:
            for unknown in state["unknown_fields"]:
                by_field[unknown["field"]] += 1
                if "WRITE_AUTHORIZATION" in unknown["blocks"]:
                    blocked.add(state["source_id"])
                gates.check(f"unknown_claim_refs_{state['source_id']}", all(ref in active_claim_ids for ref in unknown.get("claim_refs", [])))
        gates.check("unknown_distribution", by_field == Counter({"owner_binding": 25, "target_identity": 16}), dict(by_field))
        gates.check("unknown_blocks_authorization", all(state["write_authority"] != "AUTHORIZED" for state in states if state["source_id"] in blocked))

    _run_group(gates, "unknowns", unknowns)

    def coverage_group() -> None:
        bindings = ctx["bindings"]
        expected = ctx["expected"]
        fixture = ctx["fixture"]
        coverage, coverage_idx = load_sharded_jsonl(root / bindings["source_anchor_coverage"]["path"])
        gates.check("coverage_seed_hash", coverage_idx["logical_content_sha256"] == bindings["source_anchor_coverage"]["logical_content_sha256"])
        gates.check("coverage_blocks_61", len(coverage) == expected["coverage_blocks"])
        gates.check("coverage_current_no_unexplained", all(item["coverage_status"] != "UNEXPLAINED" for item in coverage))
        gates.check("coverage_current_allowed", all(coverage_status_allowed(item["assertion_bearing"], item["coverage_status"], []) for item in coverage))
        for case in fixture["coverage_statuses"]:
            gates.check(
                f"fixture_coverage_{case['expected_allowed']}_{len(case['supersession_refs'])}",
                coverage_status_allowed(case["assertion_bearing"], case["coverage_status"], case["supersession_refs"]) == case["expected_allowed"],
            )
        inv = fixture["invariant_staleness"]
        for case in inv["cases"]:
            result = invariant_result(inv["last_evaluated_against"], case["current"], "PASS")
            gates.check(f"fixture_invariant_{case['name']}", result == case["expected"], result)
        gates.check("stale_not_fail", invariant_result(inv["last_evaluated_against"], inv["cases"][1]["current"], "PASS") == "STALE")
        ctx.update(coverage=coverage, coverage_idx=coverage_idx)

    _run_group(gates, "coverage", coverage_group)

    def migration_group() -> None:
        bindings = ctx["bindings"]
        expected = ctx["expected"]
        fixture = ctx["fixture"]
        _, migration_idx, migration_logical_hash = load_grouped_migration(root / bindings["legacy_migration_manifest"]["path"])
        status_counts = Counter(row["migration_status"] for row in fixture["migration_statuses"]["rows"])
        gates.check("fixture_migration_mixed_status", dict(status_counts) == fixture["migration_statuses"]["expected"], dict(status_counts))
        gates.check("legacy_migration_entries", migration_idx["total_entries"] == expected["legacy_migration_entries"])
        candidate_migration_entries = migration_idx["total_entries"] + expected["new_claims"]
        gates.check("candidate_migration_entries", candidate_migration_entries == expected["candidate_migration_entries"])
        ctx.update(
            migration_idx=migration_idx,
            migration_logical_hash=migration_logical_hash,
            candidate_migration_entries=candidate_migration_entries,
        )

    _run_group(gates, "migration", migration_group)

    def roundtrip_group() -> None:
        coverage = sorted(ctx["coverage"], key=lambda item: item["block_ordinal"])
        ordinals = [item["block_ordinal"] for item in coverage]
        gates.check("roundtrip_block_ordinals", ordinals == list(range(1, len(coverage) + 1)), ordinals)

        document_paths = {item["document_path"] for item in coverage}
        if len(document_paths) != 1:
            raise ValidationError(f"roundtrip must bind exactly one source document: {sorted(document_paths)}")
        document_path = next(iter(document_paths))
        audit_doc = (root / document_path).read_bytes()
        lines = audit_doc.decode("utf-8").splitlines(keepends=True)

        expected_blob_ids = {item["document_git_blob_sha"] for item in coverage}
        expected_doc_hashes = {item["document_sha256"] for item in coverage}
        gates.check("roundtrip_single_blob_identity", len(expected_blob_ids) == 1, sorted(expected_blob_ids))
        gates.check("roundtrip_single_document_sha", len(expected_doc_hashes) == 1, sorted(expected_doc_hashes))
        gates.check(
            "roundtrip_document_blob",
            len(expected_blob_ids) == 1 and git_blob_sha1(audit_doc) == next(iter(expected_blob_ids)),
            git_blob_sha1(audit_doc),
        )
        gates.check(
            "roundtrip_document_sha",
            len(expected_doc_hashes) == 1 and sha256(audit_doc) == next(iter(expected_doc_hashes)),
            sha256(audit_doc),
        )

        rebuilt = bytearray()
        next_line = 1
        for item in coverage:
            start = item["line_start"]
            end = item["line_end"]
            gates.check(
                f"roundtrip_contiguous_{item['coverage_id']}",
                start == next_line,
                {"expected": next_line, "actual": start},
            )
            if not (1 <= start <= end <= len(lines)):
                gates.check(
                    f"roundtrip_bounds_{item['coverage_id']}",
                    False,
                    {"start": start, "end": end, "line_count": len(lines)},
                )
                next_line = end + 1
                continue
            gates.check(
                f"roundtrip_bounds_{item['coverage_id']}",
                True,
                {"start": start, "end": end, "line_count": len(lines)},
            )
            block_bytes = "".join(lines[start - 1:end]).encode("utf-8")
            gates.check(
                f"roundtrip_block_hash_{item['coverage_id']}",
                sha256(block_bytes) == item["block_sha256"],
                sha256(block_bytes),
            )
            rebuilt.extend(block_bytes)
            next_line = end + 1

        gates.check(
            "roundtrip_eof_coverage",
            next_line == len(lines) + 1,
            {"next_line": next_line, "line_count": len(lines)},
        )
        rebuilt_bytes = bytes(rebuilt)
        gates.check("roundtrip_exact_bytes", rebuilt_bytes == audit_doc)
        gates.check("roundtrip_rebuilt_sha", sha256(rebuilt_bytes) == sha256(audit_doc), sha256(rebuilt_bytes))
        gates.check("roundtrip_unexplained_zero", all(item["coverage_status"] != "UNEXPLAINED" for item in coverage))
        ctx["roundtrip"] = {
            "source_document": document_path,
            "document_git_blob_sha": git_blob_sha1(audit_doc),
            "document_sha256": sha256(audit_doc),
            "coverage_blocks": len(coverage),
            "line_count": len(lines),
            "exact_textual_roundtrip": rebuilt_bytes == audit_doc,
            "unexplained_blocks": sum(item["coverage_status"] == "UNEXPLAINED" for item in coverage),
        }

    _run_group(gates, "roundtrip", roundtrip_group)

    def progress_group() -> None:
        states = ctx["states"]
        total = len(states)
        applicable = sum(state["applicability_state"] == "APPLICABLE" for state in states)
        target_resolved = sum(state["target_status"] == "RESOLVED" for state in states)
        excluded = total - applicable
        closed = sum(state["closure_state"] == "CLOSED" for state in states)
        progress = {
            "target_resolution": {
                "resolved_over_applicable": [target_resolved, applicable],
                "resolved_over_total": [target_resolved, total],
                "excluded_over_total": [excluded, total],
            },
            "closure": {
                "closed_over_applicable": [closed, applicable],
                "closed_over_total": [closed, total],
            },
        }
        gates.check("progress_triplet", progress["target_resolution"] == {
            "resolved_over_applicable": [262, 278],
            "resolved_over_total": [262, 278],
            "excluded_over_total": [0, 278],
        })
        ctx["progress"] = progress

    _run_group(gates, "progress", progress_group)

    def semantic_hashes_group() -> None:
        bindings = ctx["bindings"]
        semantic_hashes = {
            "source_state": semantic_rows_hash(ctx["states"]),
            "actions": semantic_rows_hash(ctx["actions"]),
            "source_action_edges": semantic_rows_hash(ctx["edges"]),
            "effective_claims": semantic_rows_hash(ctx["claims"]),
        }
        for binding_key, hash_key in [
            ("source_state_seed", "source_state"),
            ("source_action_edge_seed", "source_action_edges"),
            ("base_claims", "effective_claims"),
            ("action_table", "actions"),
        ]:
            if binding_key == "base_claims":
                expected_hash = bindings[binding_key].get("expected_effective_claims_sha256")
            else:
                expected_hash = bindings[binding_key].get("expected_materialized_semantic_sha256")
            if expected_hash is not None:
                gates.check(f"pinned_semantic_hash_{hash_key}", semantic_hashes[hash_key] == expected_hash, semantic_hashes[hash_key])
        ctx["semantic_hashes"] = semantic_hashes

    _run_group(gates, "semantic_hashes", semantic_hashes_group)

    summary = gates.summary()
    has_issues = summary["FAIL"] or summary["BLOCKED"] or summary["STALE"]
    bindings = ctx.get("bindings", {})
    all_pinned = False
    if bindings:
        try:
            all_pinned = all((
                bindings["source_state_seed"]["expected_materialized_semantic_sha256"],
                bindings["source_action_edge_seed"]["expected_materialized_semantic_sha256"],
                bindings["base_claims"]["expected_effective_claims_sha256"],
                bindings["action_table"]["expected_materialized_semantic_sha256"],
            ))
        except KeyError:
            all_pinned = False

    if has_issues:
        result_state = "FAIL" if mode == "fail_fast" else "DIAGNOSTIC_ISSUES"
        exit_code = 1
    else:
        result_state = "PASS" if all_pinned else "PREPIN_PASS"
        exit_code = 0

    result = {
        "schema": "MACHINE_ACCOUNTING_SCHEMA_V1_CANDIDATE_VALIDATION",
        "mode": "RELEASE_FAIL_FAST" if mode == "fail_fast" else "COLLECT_ALL_MACHINE_GATES",
        "result": result_state,
        "semantic_reanalysis": False,
        "gate_summary": summary,
        "groups": gates.groups,
        "checks": gates.checks if mode == "collect_all" else None,
        "checks_passed": sorted(key for key, value in gates.checks.items() if value["status"] == "PASS"),
    }
    if bindings:
        result["semantic_schema_version"] = bindings.get("semantic_schema_version")
        result["transport_format_version"] = bindings.get("transport_format_version")
    if all(key in ctx for key in ("states", "actions", "edges", "base_claims", "claims")):
        result["counts"] = {
            "sources": len(ctx["states"]),
            "actions": len(ctx["actions"]),
            "edges": len(ctx["edges"]),
            "base_claims": len(ctx["base_claims"]),
            "effective_claims": len(ctx["claims"]),
            "active_claims": len(ctx.get("active_claim_ids", [])),
            "coverage_blocks": len(ctx.get("coverage", [])),
            "legacy_migration_entries": ctx.get("migration_idx", {}).get("total_entries"),
            "candidate_migration_entries": ctx.get("candidate_migration_entries"),
        }
    if "progress" in ctx:
        result["progress"] = ctx["progress"]
    if "semantic_hashes" in ctx:
        result["semantic_hashes"] = ctx["semantic_hashes"]
    if "migration_logical_hash" in ctx:
        result["legacy_migration_logical_hash"] = ctx["migration_logical_hash"]
    if "action_repository_file_sha256" in ctx:
        result["action_manifest_transport"] = {
            "repository_file_sha256": ctx["action_repository_file_sha256"],
            "current_transport_index_sha256": bindings["action_table"]["current_transport_index_sha256"],
            "exact": ctx["action_transport_exact"],
            "recovered_from_truncated_transport": ctx["manifest_transport_recovered"],
            "repair_required_before_freeze": not ctx["action_transport_exact"],
        }
    if mode == "collect_all":
        result["diagnostic_contract"] = {
            "scope": "current machine gates only",
            "reopens_verified_historical_facts": False,
            "status_meanings": {
                "PASS": "gate evaluated and satisfied",
                "FAIL": "gate evaluated and violated",
                "BLOCKED": "gate could not run because a prerequisite group did not pass",
                "STALE": "dependency identity changed; reevaluation required, not technical disproof",
            },
        }
    return result, exit_code


def _write_result(result: dict, out_path: Path | None) -> None:
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(output, end="")
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result, code = validate_candidate(args.repo_root, mode="fail_fast")
    except VALIDATION_EXCEPTIONS as exc:
        result, code = {
            "schema": "MACHINE_ACCOUNTING_SCHEMA_V1_CANDIDATE_VALIDATION",
            "mode": "RELEASE_FAIL_FAST",
            "result": "FAIL",
            "error": str(exc),
        }, 1
    _write_result(result, args.out)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
