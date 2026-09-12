#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from machine_accounting_v1_candidate_lib import (
    ValidationError,
    canonical_json_sha256,
    coverage_status_allowed,
    git_blob_sha1,
    invariant_result,
    load_action_manifest,
    load_grouped_migration,
    load_sharded_jsonl,
    materialize_action,
    materialize_edge,
    materialize_effective_claims,
    materialize_source_state,
    require,
    semantic_rows_hash,
    sha256,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    root = args.repo_root.resolve()

    checks = {}
    def ck(name, condition, detail=None):
        if not condition:
            raise ValidationError(f"{name}: {detail}")
        checks[name] = {"pass": True, "detail": detail}

    try:
        candidate = root / "data/pilot/f1_v1_candidate"
        bindings = json.loads((candidate / "bindings.json").read_text(encoding="utf-8"))
        contract = json.loads((candidate / "materialization_contract.json").read_text(encoding="utf-8"))
        amendments = json.loads((candidate / "claim_amendments.json").read_text(encoding="utf-8"))
        fixture = json.loads((root / "tests/fixtures/machine_accounting_schema_v1.json").read_text(encoding="utf-8"))

        ck("semantic_schema_version", bindings["semantic_schema_version"] == "1.0-candidate.1")
        ck("transport_version_separate", bindings["transport_format_version"] == "F1_PILOT_TRANSPORT_V0_1")
        ck("contract_hash", canonical_json_sha256(contract) == bindings["materialization_contract"]["canonical_json_sha256"])
        ck("amendment_hash", canonical_json_sha256(amendments) == bindings["claim_amendments"]["canonical_json_sha256"])

        seed_states, state_idx = load_sharded_jsonl(root / bindings["source_state_seed"]["path"])
        edge_seeds, edge_idx = load_sharded_jsonl(root / bindings["source_action_edge_seed"]["path"])
        base_claims, claim_idx = load_sharded_jsonl(root / bindings["base_claims"]["path"])
        coverage, coverage_idx = load_sharded_jsonl(root / bindings["source_anchor_coverage"]["path"])
        migration_groups, migration_idx, migration_logical_hash = load_grouped_migration(root / bindings["legacy_migration_manifest"]["path"])

        ck("state_seed_hash", state_idx["logical_content_sha256"] == bindings["source_state_seed"]["logical_content_sha256"])
        ck("edge_seed_hash", edge_idx["logical_content_sha256"] == bindings["source_action_edge_seed"]["logical_content_sha256"])
        ck("base_claim_hash", claim_idx["logical_content_sha256"] == bindings["base_claims"]["logical_content_sha256"])
        ck("coverage_seed_hash", coverage_idx["logical_content_sha256"] == bindings["source_anchor_coverage"]["logical_content_sha256"])

        states = [materialize_source_state(row, contract) for row in seed_states]
        edges = [materialize_edge(row, contract) for row in edge_seeds]
        claims = materialize_effective_claims(base_claims, amendments)

        expected = bindings["expected_counts"]
        ck("sources_278", len(states) == expected["sources"] == len({x["source_id"] for x in states}))
        ck("accounting_role_obligation", all(x["accounting_role"] == "OBLIGATION" for x in states))
        ck("revision1_migration", all(x["revision"] == 1 and x["changed_by"]["type"] == "MIGRATION" for x in states))
        ck("no_exclusions", all(x["applicability_state"] == "APPLICABLE" and x["exclusion_claim_id"] is None for x in states))
        ck("resolved_262", sum(x["target_status"] == "RESOLVED" for x in states) == 262)
        ck("analyzed_unresolved_16", sum(x["analysis_state"] == "ANALYZED_UNRESOLVED" for x in states) == 16)
        ck("closed_158", sum(x["closure_state"] == "CLOSED" for x in states) == 158)

        blocker_counts = Counter(x["blocker"] or "NONE" for x in states)
        ck("blocker_distribution", blocker_counts == Counter({
            "NONE": 158,
            "PADDING_RECONSTRUCTION_REQUIRED": 75,
            "SHARED_OWNER_BINDING_REQUIRED": 25,
            "TERMINATOR_CAPACITY_FAIL": 4,
            "F1_RULE_REJECTED_MIN_FINAL_INTERVAL": 16,
        }), dict(blocker_counts))

        mem = json.loads((root / bindings["membership_snapshot"]["path"]).read_text(encoding="utf-8"))
        all_ids_hash = sha256("\n".join(x["source_id"] for x in states).encode("utf-8"))
        ck("exact_source_membership_hash", all_ids_hash == bindings["membership_snapshot"]["all_source_ids_sha256"], all_ids_hash)
        category_key = {
            "DIRECT": "DIRECT_PORT_AUTHORIZED",
            "REJECT": "F1_RULE_REJECTED",
            "PADDING": "PADDING_RECONSTRUCTION_REQUIRED",
            "SHARED": "SHARED_OWNER_BINDING_REQUIRED",
            "CAPACITY": "TERMINATOR_CAPACITY_FAIL",
        }
        for category, snapshot_key in category_key.items():
            actual = [seed["pc_record"] for seed in seed_states if seed["category"] == category]
            ck(f"exact_membership_{category}", actual == mem["pc_records"][snapshot_key], {"actual": len(actual), "expected": len(mem["pc_records"][snapshot_key])})

        action_binding = json.loads((root / bindings["action_table"]["binding_path"]).read_text(encoding="utf-8"))
        manifest_path = root / bindings["action_table"]["manifest_path"]
        raw, uncompressed, manifest_rows, manifest_transport_recovered, canonical_gzip = load_action_manifest(manifest_path)
        action_repository_file_sha256 = sha256(raw)
        action_transport_exact = action_repository_file_sha256 == bindings["action_table"]["manifest_file_sha256"]
        ck("action_canonical_gzip_hash", sha256(canonical_gzip) == bindings["action_table"]["manifest_file_sha256"], sha256(canonical_gzip))
        ck("action_content_hash", sha256(uncompressed) == bindings["action_table"]["manifest_content_sha256"], sha256(uncompressed))
        ck("action_binding_consistency", action_binding["manifest_file_sha256"] == bindings["action_table"]["manifest_file_sha256"] and action_binding["manifest_content_sha256"] == bindings["action_table"]["manifest_content_sha256"])

        actions = [materialize_action(row, contract) for row in manifest_rows]
        ck("actions_158", len(actions) == expected["actions"] == len({x["action_id"] for x in actions}))
        ck("action_sources_unique", len({x["input_source_ids"][0] for x in actions}) == 158)
        ck("action_required_semantics", all(
            x["conflict_state"] == "NONE"
            and x["guards"][0]["pass"]
            and x["guards"][1]["pass"]
            and x["storage_class"] == "STATIC_RODATA"
            and x["language_domain"] == "JP_ONLY"
            for x in actions
        ))

        edge_pairs = [(x["source_id"], x["action_id"]) for x in edges]
        action_pairs = [(x["input_source_ids"][0], x["action_id"]) for x in actions]
        ck("edges_158", len(edges) == expected["edges"])
        ck("edge_full_materialization", all(set(x) == {"source_id","action_id","role","source_byte_range","target_byte_range","claim_refs","legacy_evidence_refs"} for x in edges))
        ck("edges_match_actions", edge_pairs == action_pairs)
        ck("edges_primary", all(x["role"] == "PRIMARY" for x in edges))
        closed_sources = {x["source_id"] for x in states if x["closure_state"] == "CLOSED"}
        ck("actions_only_closed", {x["input_source_ids"][0] for x in actions} == closed_sources)

        all_claim_ids = {x["claim_id"] for x in claims}
        active_claim_ids = {x["claim_id"] for x in claims if x["lifecycle_state"] == "ACTIVE"}
        ck("base_claim_count", len(base_claims) == expected["base_claims"])
        ck("new_claim_count", len(claims) - len(base_claims) == expected["new_claims"])
        ck("effective_claim_count", len(claims) == expected["effective_claims"])
        ck("active_claim_count", len(active_claim_ids) == expected["active_claims"])
        split_sources = {x["claim_id"] for x in amendments["splits"]}
        ck("split_sources_superseded", all(next(c for c in claims if c["claim_id"] == cid)["lifecycle_state"] == "SUPERSEDED" for cid in split_sources))
        ck("active_claim_referential_integrity", all(
            ref in all_claim_ids
            for c in claims
            for ref in c.get("supersedes", []) + c.get("superseded_by", [])
        ))
        ck("active_claim_refs_from_state", all(ref in active_claim_ids for s in states for ref in s.get("claim_refs", [])))
        ck("active_claim_refs_from_actions", all(ref in active_claim_ids for a in actions for ref in a.get("claim_refs", [])))
        ck("active_claim_refs_from_edges", all(ref in active_claim_ids for e in edges for ref in e.get("claim_refs", [])))

        structured_exceptions = {x["claim_id"] for x in amendments["structured_atomic_exceptions"]}
        forbidden_active_composites = []
        for c in claims:
            if c["lifecycle_state"] != "ACTIVE" or c["claim_id"] in structured_exceptions:
                continue
            if c["claim_id"] in {"V090.C01"}:
                continue
            if isinstance(c.get("value"), dict) and len(c["value"]) > 1 and c.get("predicate") in {"counts","rule","cardinality_and_safety"}:
                forbidden_active_composites.append(c["claim_id"])
        ck("atomic_claim_policy", not forbidden_active_composites, forbidden_active_composites)

        doc_cache = {}
        for claim in base_claims:
            anchor = claim["source_anchor"]
            path = root / anchor["document_path"]
            if path not in doc_cache:
                raw_doc = path.read_bytes()
                doc_cache[path] = raw_doc
            raw_doc = doc_cache[path]
            ck(f"anchor_blob_{claim['claim_id']}", git_blob_sha1(raw_doc) == anchor["document_git_blob_sha"])
            ck(f"anchor_text_hash_{claim['claim_id']}", sha256(anchor["anchor_text"].encode("utf-8")) == anchor["anchor_text_sha256"])
            ck(f"anchor_text_present_{claim['claim_id']}", anchor["anchor_text"] in raw_doc.decode("utf-8"))

        by_field = Counter()
        blocked = set()
        for state in states:
            for unknown in state["unknown_fields"]:
                by_field[unknown["field"]] += 1
                if "WRITE_AUTHORIZATION" in unknown["blocks"]:
                    blocked.add(state["source_id"])
                ck(f"unknown_claim_refs_{state['source_id']}", all(ref in active_claim_ids for ref in unknown.get("claim_refs", [])))
        ck("unknown_distribution", by_field == Counter({"owner_binding":25,"target_identity":16}), dict(by_field))
        ck("unknown_blocks_authorization", all(s["write_authority"] != "AUTHORIZED" for s in states if s["source_id"] in blocked))

        ck("coverage_blocks_61", len(coverage) == expected["coverage_blocks"])
        ck("coverage_current_no_unexplained", all(x["coverage_status"] != "UNEXPLAINED" for x in coverage))
        ck("coverage_current_allowed", all(coverage_status_allowed(x["assertion_bearing"], x["coverage_status"], []) for x in coverage))
        for case in fixture["coverage_statuses"]:
            ck(f"fixture_coverage_{case['expected_allowed']}_{len(case['supersession_refs'])}", coverage_status_allowed(case["assertion_bearing"], case["coverage_status"], case["supersession_refs"]) == case["expected_allowed"])

        inv = fixture["invariant_staleness"]
        for case in inv["cases"]:
            result = invariant_result(inv["last_evaluated_against"], case["current"], "PASS")
            ck(f"fixture_invariant_{case['name']}", result == case["expected"], result)
        ck("stale_not_fail", invariant_result(inv["last_evaluated_against"], inv["cases"][1]["current"], "PASS") == "STALE")

        status_counts = Counter(row["migration_status"] for row in fixture["migration_statuses"]["rows"])
        ck("fixture_migration_mixed_status", dict(status_counts) == fixture["migration_statuses"]["expected"], dict(status_counts))
        ck("legacy_migration_entries", migration_idx["total_entries"] == expected["legacy_migration_entries"])
        candidate_migration_entries = migration_idx["total_entries"] + expected["new_claims"]
        ck("candidate_migration_entries", candidate_migration_entries == expected["candidate_migration_entries"])

        roundtrip = json.loads((root / "generated/pilot/f1/roundtrip_result.json").read_text(encoding="utf-8"))
        audit_doc = (root / roundtrip["source_document"]).read_bytes()
        ck("audit_doc_blob", git_blob_sha1(audit_doc) == roundtrip["source_git_blob_sha"])
        ck("audit_roundtrip_still_exact", roundtrip["exact_textual_roundtrip"] and roundtrip["unexplained_roundtrip_diff_count"] == 0 and roundtrip["unexplained_blocks"] == 0)

        total = len(states)
        applicable = sum(s["applicability_state"] == "APPLICABLE" for s in states)
        target_resolved = sum(s["target_status"] == "RESOLVED" for s in states)
        excluded = total - applicable
        closed = sum(s["closure_state"] == "CLOSED" for s in states)
        progress = {
            "target_resolution": {
                "resolved_over_applicable": [target_resolved, applicable],
                "resolved_over_total": [target_resolved, total],
                "excluded_over_total": [excluded, total],
            },
            "closure": {"closed_over_applicable": [closed, applicable], "closed_over_total": [closed, total]},
        }
        ck("progress_triplet", progress["target_resolution"] == {
            "resolved_over_applicable":[262,278],
            "resolved_over_total":[262,278],
            "excluded_over_total":[0,278],
        })

        semantic_hashes = {
            "source_state": semantic_rows_hash(states),
            "actions": semantic_rows_hash(actions),
            "source_action_edges": semantic_rows_hash(edges),
            "effective_claims": semantic_rows_hash(claims),
        }
        for binding_key, hash_key in [
            ("source_state_seed","source_state"),
            ("source_action_edge_seed","source_action_edges"),
            ("base_claims","effective_claims"),
            ("action_table","actions"),
        ]:
            expected_hash = bindings[binding_key].get("expected_materialized_semantic_sha256") if binding_key != "base_claims" else bindings[binding_key].get("expected_effective_claims_sha256")
            if expected_hash is not None:
                ck(f"pinned_semantic_hash_{hash_key}", semantic_hashes[hash_key] == expected_hash, semantic_hashes[hash_key])

        result_state = "PASS" if all(
            (bindings["source_state_seed"]["expected_materialized_semantic_sha256"],
             bindings["source_action_edge_seed"]["expected_materialized_semantic_sha256"],
             bindings["base_claims"]["expected_effective_claims_sha256"],
             bindings["action_table"]["expected_materialized_semantic_sha256"])
        ) else "PREPIN_PASS"

        result = {
            "schema": "MACHINE_ACCOUNTING_SCHEMA_V1_CANDIDATE_VALIDATION",
            "result": result_state,
            "semantic_schema_version": bindings["semantic_schema_version"],
            "transport_format_version": bindings["transport_format_version"],
            "counts": {
                "sources": len(states),
                "actions": len(actions),
                "edges": len(edges),
                "base_claims": len(base_claims),
                "effective_claims": len(claims),
                "active_claims": len(active_claim_ids),
                "coverage_blocks": len(coverage),
                "legacy_migration_entries": migration_idx["total_entries"],
                "candidate_migration_entries": candidate_migration_entries,
            },
            "progress": progress,
            "semantic_hashes": semantic_hashes,
            "legacy_migration_logical_hash": migration_logical_hash,
            "action_manifest_transport": {
                "repository_file_sha256": action_repository_file_sha256,
                "canonical_file_sha256": bindings["action_table"]["manifest_file_sha256"],
                "exact": action_transport_exact,
                "recovered_from_truncated_transport": manifest_transport_recovered,
                "repair_required_before_freeze": not action_transport_exact,
            },
            "checks_passed": sorted(checks),
        }
        output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        print(output, end="")
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
        return 0
    except (ValidationError, KeyError, ValueError, OSError, json.JSONDecodeError) as exc:
        result = {
            "schema": "MACHINE_ACCOUNTING_SCHEMA_V1_CANDIDATE_VALIDATION",
            "result": "FAIL",
            "error": str(exc),
            "checks_passed": sorted(checks),
        }
        output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        print(output, end="")
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
