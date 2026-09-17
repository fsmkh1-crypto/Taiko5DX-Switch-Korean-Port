# PROJECT_STATE

Last updated: 2026-09-18 (KST)

This file is the sole repository-level project-resume authority.

Current canonical overlay:

```text
scope   SELECTIVE_KO_INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_MATERIALIZATION / V299
parent  f9bf016e647c62644a96d088d0dd10c904cbb3a5 / V298
```

All earlier VERIFIED/CLOSED facts, FZ001, Stage1/Stage2, forward-986, Mapping 10,036, Pointer-56, TAI5MSG structure, F1 provenance, V292-V298 policy/results, rejected hypotheses, and Git write restrictions remain inherited unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"SELECTIVE_KO_INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299_MATERIALIZED","scope_kind":"CANDIDATE_CLASSIFICATION_MATERIALIZATION","status":"V299_MATERIALIZED_R1_NUMERIC_53_INCLUDED_NO_BUILD","last_closed_validation_id":"V299","canonical_base_commit":"f9bf016e647c62644a96d088d0dd10c904cbb3a5","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"repository_update_ref_force":false,"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","active_product_track":"SWITCH_SELECTIVE_KOREANIZATION","selective_subtree_resume_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","exact_next_scope_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","priority_next_scope":"SELECTIVE_KO_REMAINING_STATIC_47_CANDIDATE_CLASSIFICATION_MATERIALIZATION","priority_next_focus":"MATERIALIZE_47_RESOLVED_STATIC_R1_ROWS_KEEP_R2884_R2885_UNRESOLVED","historical_full_port_track_status":"FROZEN_DIAGNOSTIC_REFERENCE_CLAIM_SCOPED","legacy_evidence_claim_strength_policy":"selective_ko/LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md","inline_v297_authority":"selective_ko/INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md","ending_help_v298_authority":"selective_ko/ENDING_HELP_39_CANDIDATE_CLASSIFICATION_V298.md","ending_help_v298_artifact":"selective_ko/artifacts/ending_help_39_candidate_classification_v1/INDEX.json","numeric_v299_authority":"selective_ko/INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299.md","numeric_v299_artifact":"selective_ko/artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json","inline_r1_source_role_objects":141,"remaining_ordinary_inline_r1_objects":102,"remaining_static_like_objects":49,"remaining_static_resolved_not_materialized":47,"remaining_static_unresolved":2,"remaining_static_unresolved_rnums":["R2884","R2885"],"numeric_variable_insert_objects":53,"selective_candidate_ids":92,"selective_classification_ids":92,"selective_include_ko_rows":92,"selective_r1_materialized_rows":92,"selective_builder_status":"NOT_IMPLEMENTED","selective_build_status":"NONE","identity_presentation_fields":"KEEP_JP","authored_korean_prose_identity_literals":"PRESERVE_AS_AUTHORED_KO","runtime_inserted_identity":"KEEP_JP","identity_reverse_substitution":"FORBIDDEN","switch_original_romfs_status":"NOT_YET_SUPPLIED","required_reads":["selective_ko/INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299.md","selective_ko/artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json","selective_ko/ENDING_HELP_39_CANDIDATE_CLASSIFICATION_V298.md","selective_ko/artifacts/ending_help_39_candidate_classification_v1/INDEX.json","selective_ko/INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md","selective_ko/LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md","selective_ko/CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md","selective_ko/SELECTIVE_PROJECT_STATE.md","selective_ko/CLASSIFICATION_SCHEMA.md","selective_ko/SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md","selective_ko/KNOWN_FAILURES.md","selective_ko/SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md","selective_ko/IDENTITY_IN_PROSE_POLICY.md","docs/MASTER_RULE_REGISTRY.md","docs/GITHUB_AND_CI_POLICY.md"]}
PROJECT_RESUME_V2 -->

## 1. V299 — numeric R1 53 rows materialized

Canonical V299 authority:

`selective_ko/INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299.md`

Canonical row artifact:

`selective_ko/artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json`

V299 adds:

```text
candidate IDs              = 53
classification IDs         = 53
INCLUDE_KO rows            = 53
ID ranges                  = SEL-CAND/SEL-CLS-000040..000092
builder                     = NOT IMPLEMENTED
build / IPS / runtime write = NONE
```

Cumulative selective corpus:

```text
candidate IDs              = 92
classification IDs         = 92
INCLUDE_KO rows            = 92
R1 materialized rows       = 92
```

V298 ending-help 39 remains unchanged.

## 2. V299 census corrections

The following earlier read-only intermediate values are superseded:

```text
numeric objects                         50 -> 53
%d occurrences                         57 -> 60
remaining ordinary inline R1 objects   99 -> 102
inline R1 source-role objects          138 -> 141
```

`%u occurrences = 10` remains unchanged.

Do not return to the superseded values.

## 3. Numeric 53 structural closure

Population invariants:

```text
53 unique physical owners
60 unique contributing PC inline records
54 unique R_AARCH64_RELATIVE consumer slots
52 owners with one slot
1 owner with two compatible slots
format-token sequence mismatch 0
particle-risk rows 0
dynamic-counter rows 0
capacity failures 0
risk-flagged rows 0
manual overrides 0
INCLUDE_KO 53/53
```

Classification:

```text
usage_class             UI_DESCRIPTION
mechanism_class         VARIABLE_INSERT
investigation_status    RESOLVED
variable_source_kind    RUNTIME_DATA
jp_particle_adjacency   NO
dynamic_counter_decision NO
```

The fixed-literal-unit rule is binding: `%d/%u` does not imply `NUMERIC_COUNTER_FORMAT`.

Direct code XREF absence is not consumer absence for this family. The verified consumer topology is carried by `.rela.dyn R_AARCH64_RELATIVE (0x403)` source slots.

## 4. Current inline R1 source-role state

Canonical source-role census after V299:

```text
INLINE R1 total                         141

V298 ending-help                        39  materialized INCLUDE_KO
ordinary inline                        102
  static-like                           49
    structurally resolved               47  not yet row-materialized
    unresolved consumer semantics        2  R2884 / R2885
  numeric VARIABLE_INSERT               53  V299 materialized INCLUDE_KO
```

The 47 static rows are the next materialization target. `R2884` and `R2885` remain `CALLER_UNKNOWN / UNRESOLVED` and must not be swept into the 47-row population.

## 5. V298 / V297 remain inherited

V298 remains authority for the 39 ending-help `STATIC_COMPLETE + UI_DESCRIPTION` rows.

V297 remains authority for:

- 17,103 inline raw records / 8,751 exact pairs;
- Korean-bearing external positive 204 groups / 206 occurrences;
- 191 single-location occurrences -> 189 logical objects;
- positive multi-match groups 13;
- UNC zero-match correction: 8 padding/NUL + 3 UTF-16LE;
- ending-table structure and reconstruction method;
- R651 selected-use target resolution to `0x6A7C21`;
- reusable diff-run/object-first/source-sequence/fixed-stride/decoder rules.

## 6. Claim boundary

V296 remains binding:

```text
target resolved != WRITE_SAFE
WRITE_SAFE != INCLUDE_KO
INCLUDE_KO != implementation/runtime PASS
build/package PASS != gameplay PASS
```

V299 classification does not authorize builder/game writes.

## 7. Identity policy

V294 remains closed:

```text
identity presentation fields            = KEEP_JP
authored Korean prose identity literals = PRESERVE_AS_AUTHORED_KO
runtime-inserted identity                = KEEP_JP
identity reverse substitution            = FORBIDDEN
```

## 8. Other containers remain open

Still open / not materialized:

- ordinary-inline static resolved 47 candidate/classification rows;
- R2884/R2885 terminator/consumer semantics;
- TAI5MSG selective message classification;
- EVENT/TS5 production parser/caller inventory;
- SNR field/record selective parser;
- R2/R3 selective corpus;
- builder/serializer/IPS/build;
- runtime translation/layout QA.

The exact PC v1.2.1.0 build-9163702 executable remains unavailable. PC whole-program runtime-parity claims depending on it remain HINT/reference only.

## 9. Next scope

The sole executable next-scope authority is `selective_ko/SELECTIVE_PROJECT_STATE.md`.

After a fresh explicit user signal, resume:

`SELECTIVE_KO_REMAINING_STATIC_47_CANDIDATE_CLASSIFICATION_MATERIALIZATION`

Keep `R2884` and `R2885` excluded from that 47-row materialization.

## 10. Repository write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
