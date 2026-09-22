# PROJECT_STATE

Last updated: 2026-09-23 (KST)

This file is the sole repository-level project-resume authority.

Current canonical overlay:

```text
scope   EVENT_169_ROLE_AWARE_FIELD_POLICY_ADAPTER_IMPLEMENTATION / V371
parent  fedf8f2dc7161f4aae145fa59fecfe47d0658389 / V370
implementation commit  4c5d2c4e010bf9c760337d39c0a64b6a82314918
```

The current **product milestone remains V369**. V371 closes the bounded implementation of the role-aware structural-field adapter; it does not claim a 169-file candidate, VAL01, IPS, or runtime acceptance.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"EVENT_169_ROLE_AWARE_FIELD_POLICY_ADAPTER_IMPLEMENTATION_V371","scope_kind":"BOUNDED_IMPLEMENTATION","checkpoint_kind":"ROLE_AWARE_FIELD_POLICY_ADAPTER_IMPLEMENTATION_AND_BOUNDED_VALIDATION","status":"V371_BOUNDED_ADAPTER_IMPLEMENTED_AWAIT_ACTIVE_REQUEST_AND_169_FILE_OFFLINE_VALIDATION","last_closed_validation_id":"V371","last_closed_stage_commit":"4c5d2c4e010bf9c760337d39c0a64b6a82314918","canonical_base_commit":"fedf8f2dc7161f4aae145fa59fecfe47d0658389","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"repository_update_ref_force":false,"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","schema_freeze_declaration":"data/pilot/f1_v1_candidate/schema_freeze_declaration.json","schema_freeze_declaration_git_blob_sha":"6c726b7d004753e2f49f63640bd4f6df343dd736","schema_freeze_basis_validation_id":"V107","schema_freeze_basis_ci_run_id":34691523117,"schema_freeze_basis_head":"ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea","active_product_track":"SWITCH_SELECTIVE_KOREANIZATION","selective_subtree_resume_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","exact_next_scope_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","current_checkpoint_authority":"selective_ko/EVENT_169_ROLE_AWARE_FIELD_POLICY_ADAPTER_IMPLEMENTATION_V371.md","current_artifact_index":"selective_ko/artifacts/event_169_role_aware_field_policy_adapter_v1/INDEX.json","validation_index":"selective_ko/VALIDATION_INDEX.json","historical_dependency_catalog":"selective_ko/RESUME_HISTORY_INDEX.json","failure_discovery_index":"selective_ko/KNOWN_FAILURES_INDEX.json","priority_next_scope":"AWAIT_EXPLICIT_ACTIVE_REQUEST_CONNECTION_AND_169_FILE_CANDIDATE_OFFLINE_VALIDATION","priority_next_focus":"V371_ACTIVE_REQUEST_CONNECTION_AND_169_FILE_CANDIDATE_OFFLINE_VALIDATION","active_read_budget_max":12,"required_reads":["selective_ko/SELECTIVE_PROJECT_STATE.md","selective_ko/EVENT_169_ROLE_AWARE_FIELD_POLICY_ADAPTER_IMPLEMENTATION_V371.md","selective_ko/artifacts/event_169_role_aware_field_policy_adapter_v1/INDEX.json","selective_ko/VALIDATION_INDEX.json","selective_ko/BOUNDED_RESUME_READ_POLICY.md","selective_ko/EVENT_169_APPLICABILITY_AND_OVERLAP_CANONICALIZATION_V369.md","selective_ko/artifacts/event_169_v368_exact_applicability_v1/INDEX.json","selective_ko/artifacts/event_169_overlap_cluster_design_v1/INDEX.json","selective_ko/KNOWN_FAILURES_INDEX.json"],"v369_product_authority":"selective_ko/EVENT_169_APPLICABILITY_AND_OVERLAP_CANONICALIZATION_V369.md","event_169_source_owner_universe":66987,"event_169_recipe_coverage":52491,"event_169_structural_fields":24305,"event_169_field_policy_writer_rows":24284,"event_169_field_policy_no_writer_rows":21,"event_169_final_write_responsibility_units":80,"bounded_tests_passed":731,"candidate_event_files_emitted":0,"product_milestone":"V369_UNCHANGED","runtime_hook_required":false,"exact_next_scope":"V371_ACTIVE_REQUEST_CONNECTION_AND_169_FILE_CANDIDATE_OFFLINE_VALIDATION"}
PROJECT_RESUME_V2 -->

## Current implementation boundary

```text
EVENT source owners                         66,987
post-policy INCLUDE_KO recipes              52,491
structural field-policy rows                24,305
  writer rows                               24,284
  no-field-writer preservation rows             21
final write-responsibility units                80

bounded regression tests                      731 PASS
full field-policy source/output oracles      24,305 / 24,305 PASS
candidate EVENT files emitted                    0
```

Implemented in V371:

- exact 24,305-row role-aware field-policy adapter;
- source-plan/stage-count generic re-encoding, not final-byte rediscovery;
- payload, secondary-header, and expression-operand no-writer preservation;
- Switch special 3, typed EVENT04 6, and dual-view subordinate slot 8 handling;
- both `CONTACT:<owner>` and legacy `CONTACT:O:<owner>` dependency forms;
- exact `ECF00000:E29F4` identity parent and two subordinate slots;
- writer order `parent payload -> subordinate slot -> final partition table`;
- manifest field-rule override rejection;
- bounded CI/regression workflow.

## Product boundary

The frozen V369 product authority remains:
`selective_ko/EVENT_169_APPLICABILITY_AND_OVERLAP_CANONICALIZATION_V369.md`.

V366/V367/V368/V369 VERIFIED/CLOSED findings, FZ001, 66,987-owner membership, 52,491 semantic admission, and 80-unit overlap authority are unchanged.

## Remaining work

- connect all actual 169-file requests to the 52,491 recipes and 24,305 field policies;
- resolve the separate 60-file source-identity authority gap;
- execute 80 transaction units with atomic commit/rollback;
- validate all 66,987 owners, protected bytes, branch destinations, partition table, and final-writer responsibility;
- read back TAI5MSG 5 roots / 19 references;
- run VAL01, IPS/package, Eden, and Switch validation in later separately authorized stages.

## Protected invariants

- Do not reopen V366-V369 closed analysis merely to resume.
- Do not rediscover field writers by reparsing final bytes.
- Do not classify the 11,764 geometry changes or 700 contact fields as individual exceptions.
- Do not implement a runtime hook unless static full replay proves an irreducible hard conflict.
- Git writes remain restricted to `create_blob -> create_tree -> create_commit -> update_ref(force=false)`.
- A bounded adapter PASS is not product acceptance.

## Exact next scope

After a fresh explicit user execution signal:

`V371_ACTIVE_REQUEST_CONNECTION_AND_169_FILE_CANDIDATE_OFFLINE_VALIDATION`

That stage must consume the existing authorities and adapter without a new role/rule census.
