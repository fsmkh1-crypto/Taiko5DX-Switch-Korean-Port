#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PLAN_TERMS = (
    "next stage",
    "next step",
    "current plan",
    "recommended next",
    "현재 계획",
    "다음 단계",
    "다음 작업",
)
MACHINE_FACT_START = "<!-- MACHINE_FACTS_V1"
MACHINE_FACT_END = "MACHINE_FACTS_V1 -->"
GENERATED_AUTHORITY_KEYS = {
    "next_required_stage",
    "project_resume_authority",
    "scope_id",
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(msg: str) -> None:
    raise RuntimeError(msg)


def extract_resume(state_text: str) -> dict:
    match = re.search(
        r"<!-- PROJECT_RESUME_V2\s*(\{.*?\})\s*PROJECT_RESUME_V2 -->",
        state_text,
        re.S,
    )
    if not match:
        fail("INV-DOC-04 PROJECT_RESUME_V2 marker missing")
    return json.loads(match.group(1))


def extract_machine_facts(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    pattern = re.escape(MACHINE_FACT_START) + r"\s*(\{.*?\})\s*" + re.escape(MACHINE_FACT_END)
    matches = re.findall(pattern, text, re.S)
    if len(matches) != 1:
        fail(f"INV-DOC-06 machine-fact block count must be exactly 1: {path}")
    obj = json.loads(matches[0])
    if obj.get("schema") != "MACHINE_FACTS_V1":
        fail(f"INV-DOC-06 unexpected machine-fact schema: {path}")
    if not isinstance(obj.get("facts"), dict):
        fail(f"INV-DOC-06 missing machine-fact payload: {path}")
    return obj["facts"]


def anchor_gate_registry(root: Path) -> list[str]:
    path = root / "tools/validate_machine_accounting_schema_v1_candidate.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    funcs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "source_anchors"]
    if len(funcs) != 1:
        fail(f"INV-DOC-06 expected one source_anchors implementation, found {len(funcs)}")
    found: set[str] = set()
    for node in ast.walk(funcs[0]):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "check" or not node.args:
            continue
        first = node.args[0]
        if not isinstance(first, ast.JoinedStr):
            continue
        literal = "".join(
            part.value
            for part in first.values
            if isinstance(part, ast.Constant) and isinstance(part.value, str)
        )
        if literal.startswith("anchor_"):
            found.add(literal)
    return sorted(found)


def collect_markdown_scope(root: Path) -> list[str]:
    actual: set[str] = set()
    actual.update(
        str(path.relative_to(root)).replace("\\", "/")
        for path in root.glob("*.md")
        if path.is_file()
    )
    actual.update(
        str(path.relative_to(root)).replace("\\", "/")
        for path in (root / "docs").rglob("*.md")
        if path.is_file()
    )
    builder_readme = root / "builder/README.md"
    if builder_readme.is_file():
        actual.add("builder/README.md")
    return sorted(actual)


def expand_document_authority_index(root: Path, index: dict) -> list[dict]:
    schema = index.get("schema")
    if schema == "DOCUMENT_AUTHORITY_INDEX_V1":
        entries = index.get("documents", [])
        if not isinstance(entries, list):
            fail("INV-DOC-05 malformed V1 document registry")
        return entries

    if schema != "DOCUMENT_AUTHORITY_INDEX_V2":
        fail(f"INV-DOC-05 unsupported document-authority schema: {schema!r}")

    default = index.get("default_classification")
    current = index.get("current_authorities")
    anchors = index.get("anchor_protected")
    if not isinstance(default, dict) or not isinstance(current, list) or not isinstance(anchors, list):
        fail("INV-DOC-05 malformed V2 document-authority registry")

    current_map = {}
    for item in current:
        path = item.get("path")
        if not isinstance(path, str) or not path or path in current_map:
            fail(f"INV-DOC-05 duplicate/malformed current-authority path: {path!r}")
        current_map[path] = item

    anchor_map = {}
    for item in anchors:
        path = item.get("path")
        sha = item.get("registered_blob_sha")
        if not isinstance(path, str) or not path or path in anchor_map:
            fail(f"INV-DOC-05 duplicate/malformed anchor path: {path!r}")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
            fail(f"INV-DOC-05 malformed anchor blob SHA: {path}")
        anchor_map[path] = sha

    actual = collect_markdown_scope(root)
    missing_declared = sorted((set(current_map) | set(anchor_map)) - set(actual))
    if missing_declared:
        fail(f"INV-DOC-05 declared authority/anchor paths missing: {missing_declared}")

    entries = []
    for path in actual:
        item = dict(default)
        item["path"] = path
        if path in current_map:
            declared = current_map[path]
            item.update({
                "doc_role": declared.get("doc_role"),
                "authority_scope": declared.get("authority_scope"),
                "current_authority": True,
                "evidence_still_valid": True,
                "superseded_as_plan_by": None,
            })
        if path in anchor_map:
            item["anchor_protected"] = True
            item["registered_blob_sha"] = anchor_map[path]
        entries.append(item)
    return entries


def check_machine_facts(root: Path, entries: list[dict]) -> None:
    required = [
        entry["path"]
        for entry in entries
        if entry.get("current_authority")
        and entry.get("authority_scope") == "MACHINE_ACCOUNTING_CANDIDATE"
    ]
    if sorted(required) != sorted(
        ["docs/CLAIM_EXTRACTION_RULES.md", "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md"]
    ):
        fail(f"INV-DOC-06 unexpected machine-accounting authority set: {required}")

    facts = {path: extract_machine_facts(root / path) for path in required}

    index_path = root / "docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST/INDEX.json"
    index_raw = index_path.read_bytes()
    index = json.loads(index_raw)
    current = index["current_transport"]
    semantic = index["semantic_identity"]

    schema_facts = facts["docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md"]
    expected_schema_facts = {
        "v094_current_transport_format": current["format"],
        "v094_current_transport_path": "docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST",
        "v094_current_transport_index_sha256": sha256(index_raw),
        "v094_semantic_rows": semantic["rows"],
        "v094_semantic_sha256": semantic["logical_content_sha256"],
    }
    if schema_facts != expected_schema_facts:
        fail(
            "INV-DOC-06 schema authority facts drift "
            f"declared={schema_facts} actual={expected_schema_facts}"
        )

    bindings = json.loads(
        (root / "data/pilot/f1_v1_candidate/bindings.json").read_text(encoding="utf-8")
    )
    action_binding = bindings["action_table"]
    binding_checks = {
        "current_transport_format": current["format"],
        "current_transport_index_sha256": sha256(index_raw),
        "manifest_content_sha256": semantic["logical_content_sha256"],
        "manifest_path": "docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST",
    }
    for key, actual in binding_checks.items():
        if action_binding.get(key) != actual:
            fail(
                f"INV-DOC-06 bindings/action transport drift: {key} "
                f"declared={action_binding.get(key)!r} actual={actual!r}"
            )

    amendments = json.loads(
        (root / "data/pilot/f1_v1_candidate/claim_amendments.json").read_text(encoding="utf-8")
    )
    exceptions = amendments.get("structured_atomic_exceptions")
    if not isinstance(exceptions, list):
        fail("INV-DOC-06 structured_atomic_exceptions registry missing")
    exception_ids = [item.get("claim_id") for item in exceptions]
    if any(not isinstance(item, str) for item in exception_ids):
        fail("INV-DOC-06 malformed structured atomic exception registry")
    if len(exception_ids) != len(set(exception_ids)):
        fail("INV-DOC-06 duplicate structured atomic exception IDs")

    claim_facts = facts["docs/CLAIM_EXTRACTION_RULES.md"]
    expected_claim_facts = {
        "source_anchor_gate_registry": anchor_gate_registry(root),
        "structured_atomic_exception_count": len(exception_ids),
        "structured_atomic_exception_ids": exception_ids,
        "structured_atomic_registry_path": "data/pilot/f1_v1_candidate/claim_amendments.json",
    }
    if claim_facts != expected_claim_facts:
        fail(
            "INV-DOC-06 claim authority facts drift "
            f"declared={claim_facts} actual={expected_claim_facts}"
        )


def check_generated_boundary(root: Path, entries: list[dict], resume_obj: dict) -> None:
    for path in resume_obj.get("required_reads", []):
        if path.startswith("generated/"):
            fail(f"INV-DOC-07 generated artifact cannot be a required read: {path}")
    for entry in entries:
        if entry.get("current_authority") and entry["path"].startswith("generated/"):
            fail(f"INV-DOC-07 generated artifact cannot be current authority: {entry['path']}")

    generated = root / "generated"
    if not generated.is_dir():
        return
    for path in generated.rglob("*.json"):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(obj, dict):
            continue
        bad = sorted(GENERATED_AUTHORITY_KEYS & set(obj))
        if bad:
            rel = str(path.relative_to(root)).replace("\\", "/")
            fail(f"INV-DOC-07 generated artifact carries authority/next-step keys: {rel} {bad}")


def check_scope_read_policy(root: Path, resume_obj: dict) -> None:
    scope_kind = resume_obj.get("scope_kind")
    if scope_kind not in {"READ_ONLY", "REPOSITORY_WRITE"}:
        fail(f"INV-DOC-09 invalid scope_kind: {scope_kind!r}")

    required = resume_obj.get("required_reads")
    if not isinstance(required, list) or not required:
        fail("INV-DOC-09 required_reads must be a non-empty active bootstrap list")
    if any(not isinstance(path, str) or not path for path in required):
        fail("INV-DOC-09 required_reads contains a malformed path")
    if len(required) != len(set(required)):
        fail("INV-DOC-09 required_reads contains duplicates")

    budget = resume_obj.get("active_read_budget_max", 16)
    if not isinstance(budget, int) or budget < 1:
        fail(f"INV-DOC-09 invalid active_read_budget_max: {budget!r}")
    if len(required) > budget:
        fail(
            f"INV-DOC-09 active required_reads exceed budget: "
            f"count={len(required)} budget={budget}"
        )

    historical_catalog = resume_obj.get("historical_dependency_catalog")
    if not isinstance(historical_catalog, str) or not historical_catalog:
        fail("INV-DOC-09 historical_dependency_catalog missing")
    if historical_catalog in required:
        fail("INV-DOC-09 historical dependency catalog must remain lazy, not a bootstrap read")
    if not (root / historical_catalog).is_file():
        fail(f"INV-DOC-09 historical dependency catalog missing: {historical_catalog}")

    failure_index = resume_obj.get("failure_discovery_index")
    if not isinstance(failure_index, str) or not failure_index:
        fail("INV-DOC-09 failure_discovery_index missing")
    if not (root / failure_index).is_file():
        fail(f"INV-DOC-09 failure discovery index missing: {failure_index}")

    if "selective_ko/KNOWN_FAILURES.md" in required:
        fail("INV-DOC-09 full KNOWN_FAILURES.md must not be a mandatory bootstrap read")

    if scope_kind == "REPOSITORY_WRITE":
        if "docs/GITHUB_AND_CI_POLICY.md" not in set(required):
            fail("INV-DOC-09 repository-writing scope must require docs/GITHUB_AND_CI_POLICY.md")


def check_schema_freeze(root: Path, resume_obj: dict) -> None:
    status = resume_obj.get("schema_freeze_status")
    if status is None:
        return
    if status != "FROZEN_FZ001":
        fail(f"INV-DOC-10 unexpected schema_freeze_status: {status!r}")

    rel = resume_obj.get("schema_freeze_declaration")
    if rel != "data/pilot/f1_v1_candidate/schema_freeze_declaration.json":
        fail(f"INV-DOC-10 unexpected freeze declaration path: {rel!r}")
    path = root / rel
    if not path.is_file():
        fail(f"INV-DOC-10 freeze declaration missing: {rel}")

    raw = path.read_bytes()
    declared_blob = resume_obj.get("schema_freeze_declaration_git_blob_sha")
    if declared_blob != git_blob_sha1(raw):
        fail(
            "INV-DOC-10 freeze declaration blob drift "
            f"declared={declared_blob!r} actual={git_blob_sha1(raw)!r}"
        )

    obj = json.loads(raw)
    if obj.get("schema") != "MACHINE_ACCOUNTING_SCHEMA_V1_FREEZE_DECLARATION":
        fail("INV-DOC-10 unexpected freeze declaration schema")
    if obj.get("freeze_id") != "FZ001" or obj.get("state") != "FROZEN":
        fail("INV-DOC-10 freeze declaration identity/state mismatch")

    basis = obj.get("basis", {})
    machine = basis.get("machine_validation", {})
    if machine.get("validation_id") != resume_obj.get("schema_freeze_basis_validation_id"):
        fail("INV-DOC-10 freeze validation-id provenance mismatch")
    if machine.get("run_id") != resume_obj.get("schema_freeze_basis_ci_run_id"):
        fail("INV-DOC-10 freeze CI-run provenance mismatch")
    if machine.get("head") != resume_obj.get("schema_freeze_basis_head"):
        fail("INV-DOC-10 freeze basis-head provenance mismatch")
    if machine.get("release_fail_fast") != "PASS" or machine.get("collect_all") != "PASS":
        fail("INV-DOC-10 freeze basis is not PASS/PASS")

    pre_head = basis.get("pre_freeze_head")
    if not isinstance(pre_head, str) or not re.fullmatch(r"[0-9a-f]{40}", pre_head):
        fail("INV-DOC-10 invalid pre-freeze head")
    result = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", pre_head, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        fail(f"INV-DOC-10 pre-freeze head is not an ancestor of HEAD: {pre_head}")

    authority = obj.get("authority_documents", {})
    expected_docs = {
        "machine_accounting_schema": "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md",
        "claim_extraction_rules": "docs/CLAIM_EXTRACTION_RULES.md",
    }
    for key, expected_path in expected_docs.items():
        item = authority.get(key, {})
        if item.get("path") != expected_path:
            fail(f"INV-DOC-10 freeze authority path mismatch: {key}")
        actual_blob = git_blob_sha1((root / expected_path).read_bytes())
        if item.get("git_blob_sha") != actual_blob:
            fail(
                f"INV-DOC-10 frozen authority blob drift: {expected_path} "
                f"declared={item.get('git_blob_sha')!r} actual={actual_blob!r}"
            )

    bindings_path = root / "data/pilot/f1_v1_candidate/bindings.json"
    bindings_raw = bindings_path.read_bytes()
    bindings = json.loads(bindings_raw)
    frozen_bindings = obj.get("bindings", {})
    if frozen_bindings.get("path") != "data/pilot/f1_v1_candidate/bindings.json":
        fail("INV-DOC-10 freeze bindings path mismatch")
    if frozen_bindings.get("git_blob_sha") != git_blob_sha1(bindings_raw):
        fail("INV-DOC-10 freeze bindings blob drift")
    if obj.get("semantic_schema_version") != bindings.get("semantic_schema_version"):
        fail("INV-DOC-10 frozen semantic schema version drift")

    expected_pins = {
        "source_state": bindings["source_state_seed"]["expected_materialized_semantic_sha256"],
        "actions": bindings["action_table"]["expected_materialized_semantic_sha256"],
        "source_action_edges": bindings["source_action_edge_seed"]["expected_materialized_semantic_sha256"],
        "effective_claims": bindings["base_claims"]["expected_effective_claims_sha256"],
    }
    if frozen_bindings.get("semantic_pins") != expected_pins:
        fail("INV-DOC-10 frozen semantic pins drift")

    expected_hash_bindings = {
        "materialization_contract_canonical_json_sha256": bindings["materialization_contract"]["canonical_json_sha256"],
        "claim_amendments_canonical_json_sha256": bindings["claim_amendments"]["canonical_json_sha256"],
        "source_anchor_overrides_canonical_json_sha256": bindings["source_anchor_overrides"]["canonical_json_sha256"],
    }
    for key, expected in expected_hash_bindings.items():
        if frozen_bindings.get(key) != expected:
            fail(f"INV-DOC-10 frozen binding identity drift: {key}")

    boundary = obj.get("authorization_boundary", {})
    if any(boundary.get(key) is not False for key in (
        "full_migration_authorized",
        "residual_797_analysis_authorized",
        "builder_ips_runtime_authorized",
        "game_file_modification_authorized",
    )):
        fail("INV-DOC-10 freeze declaration silently authorizes a later scope")


def check_master_rule_registry(root: Path, entries: list[dict]) -> None:
    authority = [
        item["path"] for item in entries
        if item.get("current_authority") and item.get("authority_scope") == "RULE_DISCOVERY_INDEX"
    ]
    if authority != ["docs/MASTER_RULE_REGISTRY.md"]:
        fail(f"INV-DOC-11 master rule authority mismatch: {authority}")

    index_path = root / "data/post_freeze/master_rule_registry_v1/INDEX.json"
    rules_path = root / "data/post_freeze/master_rule_registry_v1/RULES.json"
    ledger_path = root / "docs/VALIDATION_LEDGER_MASTER_RULE_REGISTRY.txt"
    for path in (index_path, rules_path, ledger_path):
        if not path.is_file():
            fail(f"INV-DOC-11 master rule artifact missing: {path.relative_to(root)}")

    index_raw = index_path.read_bytes()
    rules_raw = rules_path.read_bytes()
    index = json.loads(index_raw)
    rules_obj = json.loads(rules_raw)
    if index.get("schema") != "MASTER_RULE_REGISTRY_INDEX_V1":
        fail("INV-DOC-11 unexpected master rule index schema")
    if rules_obj.get("schema") != "MASTER_RULE_REGISTRY_V1":
        fail("INV-DOC-11 unexpected master rule registry schema")
    rules = rules_obj.get("rules")
    if not isinstance(rules, list) or not rules:
        fail("INV-DOC-11 master rule registry is empty")
    ids = [item.get("rule_id") for item in rules]
    if any(not isinstance(value, str) or not value for value in ids):
        fail("INV-DOC-11 malformed master rule ID")
    if len(ids) != len(set(ids)):
        fail("INV-DOC-11 duplicate master rule ID")
    if index.get("rule_count") != len(rules):
        fail("INV-DOC-11 master rule count mismatch")
    if index.get("rules_sha256") != sha256(rules_raw):
        fail("INV-DOC-11 master rule hash mismatch")
    if index.get("human_report") != "docs/MASTER_RULE_REGISTRY.md":
        fail("INV-DOC-11 master rule human-report path mismatch")
    if index.get("validation_ledger") != "docs/VALIDATION_LEDGER_MASTER_RULE_REGISTRY.txt":
        fail("INV-DOC-11 master rule validation-ledger path mismatch")
    if index.get("boundaries", {}).get("new_switch_write_authorizations") != 0:
        fail("INV-DOC-11 master rule registry silently authorizes Switch writes")

    allowed_status = {
        "NORMATIVE", "VERIFIED", "PROMOTED_RULE", "BOUNDARY",
        "REJECTED", "SUPERSEDED", "HISTORICAL_PROVENANCE",
    }
    for item in rules:
        if item.get("status") not in allowed_status:
            fail(f"INV-DOC-11 invalid master rule status: {item.get('rule_id')}")
        if not isinstance(item.get("rule_class"), str) or not item["rule_class"]:
            fail(f"INV-DOC-11 invalid master rule class: {item.get('rule_id')}")
        sources = item.get("source_documents")
        if not isinstance(sources, list) or not sources:
            fail(f"INV-DOC-11 missing rule source documents: {item.get('rule_id')}")
        missing = [path for path in sources if not (root / path).is_file()]
        if missing:
            fail(f"INV-DOC-11 rule source missing: {item.get('rule_id')} {missing}")


def check_closure_identity(root: Path, resume_obj: dict) -> None:
    declared = resume_obj.get("last_closed_validation_id")
    track = resume_obj.get("active_product_track")

    if track == "SWITCH_SELECTIVE_KOREANIZATION":
        rel = resume_obj.get("validation_index")
        if rel != "selective_ko/VALIDATION_INDEX.json":
            fail(f"INV-DOC-08 unexpected selective validation index: {rel!r}")
        index_path = root / rel
        if not index_path.is_file():
            fail(f"INV-DOC-08 selective validation index missing: {rel}")
        obj = json.loads(index_path.read_text(encoding="utf-8"))
        if obj.get("schema") != "SELECTIVE_VALIDATION_INDEX_V1":
            fail(f"INV-DOC-08 unexpected selective validation-index schema: {obj.get('schema')!r}")
        actual = obj.get("current_validation_id")
        checkpoint = obj.get("current_checkpoint")
        declared_checkpoint = resume_obj.get("current_checkpoint_authority")
        if checkpoint != declared_checkpoint:
            fail(
                "INV-DOC-08 current checkpoint mismatch "
                f"resume={declared_checkpoint!r} index={checkpoint!r}"
            )
        if not isinstance(checkpoint, str) or not (root / checkpoint).is_file():
            fail(f"INV-DOC-08 current checkpoint missing: {checkpoint!r}")
    else:
        index_path = root / "docs/VALIDATION_LEDGER.md"
        ledger_index = index_path.read_text(encoding="utf-8")
        nums = [int(value) for value in re.findall(r"\bV(\d{3})\b", ledger_index)]
        if not nums:
            fail("INV-DOC-08 central validation index has no Vnnn entries")
        actual = f"V{max(nums):03d}"

    if declared != actual:
        fail(
            "INV-DOC-08 PROJECT_RESUME/validation-index closure mismatch: "
            f"declared={declared} actual={actual}"
        )

    commit = resume_obj.get("canonical_base_commit") or resume_obj.get("last_closed_stage_commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        fail("INV-DOC-08 invalid canonical_base_commit")
    result = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", commit, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        fail(f"INV-DOC-08 canonical_base_commit is not an ancestor of HEAD: {commit}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.repo_root.resolve()

    index_path = root / "docs/DOCUMENT_AUTHORITY_INDEX.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    entries = expand_document_authority_index(root, index)
    paths = [entry["path"] for entry in entries]

    if len(paths) != len(set(paths)):
        fail("INV-DOC-05 duplicate registry path")
    if paths.count("docs/DOCUMENT_AUTHORITY_INDEX.json") != 1:
        fail("INV-DOC-05 registry must self-register exactly once")
    missing = [path for path in paths if not (root / path).is_file()]
    if missing:
        fail(f"INV-DOC-05 indexed nonexistent paths: {missing}")

    actual: set[str] = set()
    actual.update(
        str(path.relative_to(root)).replace("\\", "/")
        for path in root.glob("*.md")
        if path.is_file()
    )
    actual.update(
        str(path.relative_to(root)).replace("\\", "/")
        for path in (root / "docs").rglob("*.md")
        if path.is_file()
    )
    builder_readme = root / "builder/README.md"
    if builder_readme.is_file():
        actual.add("builder/README.md")
    indexed_md = {path for path in paths if path.endswith(".md")}
    if actual != indexed_md:
        fail(
            "INV-DOC-05 markdown coverage mismatch "
            f"missing_from_index={sorted(actual-indexed_md)} "
            f"nonexistent_indexed={sorted(indexed_md-actual)}"
        )

    resume = [
        entry["path"]
        for entry in entries
        if entry["authority_scope"] == "PROJECT_RESUME" and entry["current_authority"]
    ]
    if resume != ["PROJECT_STATE.md"]:
        fail(f"INV-DOC-01 project resume authority: {resume}")

    for item in entries:
        path = item["path"]
        if not path.endswith(".md") or item["current_authority"]:
            continue
        text = (root / path).read_text(encoding="utf-8", errors="replace").lower()
        if any(term in text for term in PLAN_TERMS):
            superseding = item.get("superseded_as_plan_by")
            if not superseding or not (root / superseding).is_file():
                fail(f"INV-DOC-02 stale plan language lacks supersession metadata: {path}")

    for item in entries:
        if not item.get("anchor_protected"):
            continue
        data = (root / item["path"]).read_bytes()
        got = git_blob_sha1(data)
        if got != item.get("registered_blob_sha"):
            fail(f"INV-DOC-03 anchor-protected blob changed: {item['path']} {got}")

    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    if "AGENTS.md -> PROJECT_STATE.md -> PROJECT_STATE.required_reads" not in agents:
        fail("INV-DOC-04 fixed read chain missing")
    if "as applicable" in agents.lower():
        fail("INV-DOC-04 open-ended pre-read wording reintroduced")

    state = (root / "PROJECT_STATE.md").read_text(encoding="utf-8")
    resume_obj = extract_resume(state)
    for path in resume_obj.get("required_reads", []):
        if not (root / path).is_file():
            fail(f"INV-DOC-04 required read missing: {path}")

    check_machine_facts(root, entries)
    check_generated_boundary(root, entries, resume_obj)
    check_scope_read_policy(root, resume_obj)
    check_schema_freeze(root, resume_obj)
    check_master_rule_registry(root, entries)
    check_closure_identity(root, resume_obj)

    output = {
        "schema": "DOCUMENT_GOVERNANCE_VALIDATION_V2",
        "result": "PASS",
        "invariants": [
            "INV-DOC-01",
            "INV-DOC-02",
            "INV-DOC-03",
            "INV-DOC-04",
            "INV-DOC-05",
            "INV-DOC-06",
            "INV-DOC-07",
            "INV-DOC-08",
            "INV-DOC-09",
            "INV-DOC-10",
            "INV-DOC-11",
        ],
        "registered_documents": len(entries),
        "registered_markdown": len(indexed_md),
        "project_resume_authority": "PROJECT_STATE.md",
        "required_reads": resume_obj.get("required_reads", []),
        "last_closed_validation_id": resume_obj.get("last_closed_validation_id"),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            json.dumps(
                {
                    "schema": "DOCUMENT_GOVERNANCE_VALIDATION_V2",
                    "result": "FAIL",
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
