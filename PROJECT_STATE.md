# PROJECT_STATE

Last updated: 2026-09-17 (KST)

This file is the sole repository-level project-resume authority.

The previous canonical state remains an immutable inherited base:

```text
commit  a954885f7f59c64b18cd969e3178397604e02d58
scope   SELECTIVE_KO_NEXT_SCOPE_AUTHORITY_RECONCILIATION_V293_MATERIALIZED
```

All facts, closed validations, rejected hypotheses, provenance, FZ001 state, V292/V293 routing and Git-incident recovery, historical WRITE_SAFE authority, V290/V291 exclusion, ART-00000005 boundary, owner-coverage boundary, and mixed-script requirement in that snapshot are inherited without revalidation unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"SELECTIVE_KO_IDENTITY_IN_PROSE_V1_MATERIALIZED","scope_kind":"PRODUCT_POLICY_MATERIALIZATION","status":"IDENTITY_IN_PROSE_PRODUCT_DECISION_CLOSED","last_closed_validation_id":"V294","canonical_base_commit":"a954885f7f59c64b18cd969e3178397604e02d58","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","active_product_track":"SWITCH_SELECTIVE_KOREANIZATION","selective_subtree_resume_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","exact_next_scope_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","priority_next_scope":"SEE_SELECTIVE_PROJECT_STATE","historical_full_port_track_status":"FROZEN_DIAGNOSTIC_REFERENCE","v290_selective_product_status":"EXCLUDE_FROM_SELECTIVE_PRODUCT","v291_selective_product_status":"EXCLUDE_FROM_SELECTIVE_PRODUCT","v291_evidence_role":"HISTORICAL_FAILURE_EVIDENCE","grammar125_selective_role":"OPTIONAL_R4_GRAMMAR_EVIDENCE","selective_candidate_ids":0,"selective_tai5msg_classification_rows":0,"selective_include_ko_rows":0,"selective_builder_status":"NOT_IMPLEMENTED","identity_in_prose_policy":"RESOLVED_IDENTITY_IN_PROSE_V1","identity_presentation_fields":"KEEP_JP","authored_korean_prose_identity_literals":"PRESERVE_AS_AUTHORED_KO","runtime_inserted_identity":"KEEP_JP","identity_reverse_substitution":"FORBIDDEN","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/SELECTIVE_KO_DIRECTION_RECONCILIATION_V292.md","docs/SELECTIVE_KO_NEXT_SCOPE_AUTHORITY_RECONCILIATION_V293.md","docs/GIT_OBJECT_WRITE_INCIDENT_RECOVERY_20260917.md","selective_ko/IDENTITY_IN_PROSE_POLICY.md","selective_ko/SELECTIVE_PROJECT_STATE.md","selective_ko/ARCHITECTURE.md","selective_ko/CLASSIFICATION_SCHEMA.md","selective_ko/SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md","selective_ko/KNOWN_FAILURES.md","selective_ko/FIXED_PARTICLE_POLICY.md","selective_ko/TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION.md","selective_ko/artifacts/tai5msg_structure_index_v1/INDEX.json","docs/GITHUB_AND_CI_POLICY.md"]}
PROJECT_RESUME_V2 -->

## 1. V294 — identity-in-prose product policy

V294 closes the unresolved identity-in-prose product decision identified during the selective-design audit.

Canonical policy:

`selective_ko/IDENTITY_IN_PROSE_POLICY.md`

First-release decision:

```text
identity presentation fields            = KEEP_JP
PC Korean prose identity literals        = PRESERVE_AS_AUTHORED_KO
runtime-inserted person/place identity   = KEEP_JP
Korean-prose identity reverse transform  = FORBIDDEN
```

This intentionally accepts Japanese identity presentation alongside Korean prose spelling where they differ.

The mismatch is a deliberate low-cost first-release tradeoff, not a release blocker.

## 2. Product-boundary effect

The following remain Japanese by default:

- person-name fields;
- place-name fields;
- yomi/readings/sort keys;
- surname/given-name composition;
- calendar/date identity presentation;
- Korean name entry;
- runtime-inserted person/place identity values.

The following are not rewritten merely for identity consistency:

- Korean person/place names already authored inside selected PC Korean prose;
- surrounding Korean prose solely because a Japanese runtime identity token may appear in the same sentence.

No CWTDAT/yomi/name-composition work is authorized by this policy.

## 3. Authority and classification boundary

PC Korean authored prose remains content authority. Switch identity/runtime structure remains structural authority.

Future corpus rows may carry `identity_token_policy` metadata, but that field does not confer `INCLUDE_KO` and does not alter mechanism/applicability/realization axes.

Normal owner/caller/risk/capacity/provenance gates remain mandatory.

## 4. Mixed-script boundary

Mixed Japanese/Korean output is permitted by product policy.

Route-wide safety is still not assumed globally. Each selected family that mixes scripts must preserve both Japanese and Korean mapping/font/transport behavior on its actual Switch route.

## 5. Current selective state

No corpus row, gameplay-data rewrite, builder, IPS, build, or runtime artifact is created by V294.

Current counts remain:

```text
candidate IDs                 0
TAI5MSG classification rows   0
selective INCLUDE_KO rows     0
selective builder             NOT IMPLEMENTED
selective build               NONE
```

## 6. Next-scope routing

The repository-level state does not duplicate the exact executable selective next scope.

For the current next scope, read:

`selective_ko/SELECTIVE_PROJECT_STATE.md`

V294 closes the policy question only. It does not authorize the next read-only inventory automatically.

## 7. Repository write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No `create_file`, `update_file`, `delete_file`, `create_branch`, or force update is permitted.

A fresh explicit user execution signal is required before the next scope.
