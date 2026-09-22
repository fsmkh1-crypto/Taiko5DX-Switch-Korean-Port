# PROJECT_STATE

Last updated: 2026-09-22 (KST)

This file is the sole repository-level project-resume authority.

Current canonical overlay:

```text
scope   REPOSITORY_BOUNDED_RESUME_AND_GOVERNANCE_COMPATIBILITY_MIGRATION / V370
parent  5fb2499d6bbbd4ffd4d0c7a4122d0a510f9e5f77 / V369
```

The current product milestone remains V369. V370 changes resume/governance architecture only; it does not alter V366-V369 technical findings, builder behavior, product bytes, build/package/IPS, or runtime evidence.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"REPOSITORY_BOUNDED_RESUME_AND_GOVERNANCE_COMPATIBILITY_MIGRATION_V370","scope_kind":"READ_ONLY","checkpoint_kind":"REPOSITORY_BOUNDED_RESUME_AND_GOVERNANCE_COMPATIBILITY_MIGRATION","status":"V370_BOUNDED_RESUME_GOVERNANCE_MIGRATION_CLOSED_AWAIT_SERIALIZER_INSTRUCTION","last_closed_validation_id":"V370","last_closed_stage_commit":"5fb2499d6bbbd4ffd4d0c7a4122d0a510f9e5f77","canonical_base_commit":"5fb2499d6bbbd4ffd4d0c7a4122d0a510f9e5f77","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"repository_update_ref_force":false,"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","schema_freeze_declaration":"data/pilot/f1_v1_candidate/schema_freeze_declaration.json","schema_freeze_declaration_git_blob_sha":"6c726b7d004753e2f49f63640bd4f6df343dd736","schema_freeze_basis_validation_id":"V107","schema_freeze_basis_ci_run_id":34691523117,"schema_freeze_basis_head":"ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea","active_product_track":"SWITCH_SELECTIVE_KOREANIZATION","selective_subtree_resume_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","exact_next_scope_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","current_checkpoint_authority":"selective_ko/REPOSITORY_BOUNDED_RESUME_AND_GOVERNANCE_COMPATIBILITY_MIGRATION_V370.md","validation_index":"selective_ko/VALIDATION_INDEX.json","historical_dependency_catalog":"selective_ko/RESUME_HISTORY_INDEX.json","failure_discovery_index":"selective_ko/KNOWN_FAILURES_INDEX.json","priority_next_scope":"AWAIT_FRESH_EXPLICIT_EVENT_SERIALIZER_IMPLEMENTATION_INSTRUCTION","priority_next_focus":"EVENT_169_80_UNIT_CLUSTER_ATOMIC_SERIALIZER_IMPLEMENTATION_OFFLINE_VALIDATION","active_read_budget_max":12,"required_reads":["selective_ko/SELECTIVE_PROJECT_STATE.md","selective_ko/REPOSITORY_BOUNDED_RESUME_AND_GOVERNANCE_COMPATIBILITY_MIGRATION_V370.md","selective_ko/VALIDATION_INDEX.json","selective_ko/BOUNDED_RESUME_READ_POLICY.md","selective_ko/EVENT_169_APPLICABILITY_AND_OVERLAP_CANONICALIZATION_V369.md","selective_ko/artifacts/event_169_v368_exact_applicability_v1/INDEX.json","selective_ko/artifacts/event_169_overlap_cluster_design_v1/INDEX.json","selective_ko/KNOWN_FAILURES_INDEX.json"],"v369_product_authority":"selective_ko/EVENT_169_APPLICABILITY_AND_OVERLAP_CANONICALIZATION_V369.md","v369_applicability_artifact":"selective_ko/artifacts/event_169_v368_exact_applicability_v1/INDEX.json","v369_overlap_artifact":"selective_ko/artifacts/event_169_overlap_cluster_design_v1/INDEX.json","event_169_source_owner_universe":66987,"event_169_direct_header_preserved":66956,"event_169_overlap_composite":31,"event_169_post_policy_include_ko":52491,"event_169_post_policy_unresolved":0,"event_169_post_policy_non_korean_target":14496,"event_169_overlap_nodes":210,"event_169_overlap_relations":130,"event_169_overlap_clusters":87,"event_169_final_write_responsibility_units":80}
PROJECT_RESUME_V2 -->

## Current product boundary

The selective product track is frozen at V369 until a fresh explicit instruction authorizes the next product stage.

```text
EVENT source owners                  66,987
direct/header-preserved              66,956
overlap-composite                        31

post-policy INCLUDE_KO               52,491
post-policy UNRESOLVED                    0
NON_KOREAN_TARGET                    14,496

overlap graph nodes                     210
overlap relations                       130
connected clusters                       87
final write-responsibility units         80
```

The exact product authority is:
`selective_ko/EVENT_169_APPLICABILITY_AND_OVERLAP_CANONICALIZATION_V369.md`.

## Resume contract

Normal resume is bounded:

```text
AGENTS.md
-> PROJECT_STATE.md
-> active required_reads only
-> exact-scope code/data inputs on demand
```

Historical provenance is discovered lazily through
`selective_ko/RESUME_HISTORY_INDEX.json`; it is not part of the mandatory bootstrap set.

Detailed rejected paths remain in `selective_ko/KNOWN_FAILURES.md`.
Use `selective_ko/KNOWN_FAILURES_INDEX.json` for topic-level discovery and read only the relevant detailed section.

## Protected invariants

- V366/V367/V368/V369 VERIFIED/CLOSED technical findings remain unchanged.
- FZ001 remains frozen.
- Historical commits and evidence remain intact; no history rewrite is authorized.
- Large canonical ledgers retain their pinned identities and storage locations.
- Git writes remain restricted to `create_blob -> create_tree -> create_commit -> update_ref(force=false)`.
- Product implementation, build/package/IPS, and hardware execution require a fresh explicit instruction.

## Exact next scope

After a fresh explicit user execution signal:

`EVENT_169_RUNTIME_OVERLAP_CLUSTER_SERIALIZER_IMPLEMENTATION_OFFLINE_VALIDATION`

Implementation must consume the frozen V369 applicability and 80-unit overlap-design authorities without redoing V366-V369 analysis.
