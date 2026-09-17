# PROJECT_STATE

Last updated: 2026-09-18 (KST)

This file is the sole repository-level project-resume authority.

Current canonical overlay:

```text
scope   SELECTIVE_KO_INLINE_R1_STATIC_47_CANDIDATE_CLASSIFICATION_MATERIALIZATION / V300
parent  76de9d78d46eebafee08f432ca9184415a9fb904 / V299
```

All earlier VERIFIED/CLOSED facts, FZ001, Stage1/Stage2, forward-986, Mapping 10,036, Pointer-56, TAI5MSG structure, F1 provenance, V292-V299 policy/results, rejected hypotheses, and Git write restrictions remain inherited unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"SELECTIVE_KO_INLINE_R1_STATIC_47_CANDIDATE_CLASSIFICATION_V300_MATERIALIZED","scope_kind":"CANDIDATE_CLASSIFICATION_MATERIALIZATION","status":"V300_MATERIALIZED_R1_STATIC_47_INCLUDED_INLINE_R1_139_OF_141_NO_BUILD","last_closed_validation_id":"V300","canonical_base_commit":"76de9d78d46eebafee08f432ca9184415a9fb904","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"repository_update_ref_force":false,"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","active_product_track":"SWITCH_SELECTIVE_KOREANIZATION","selective_subtree_resume_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","exact_next_scope_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","priority_next_scope":"SELECTIVE_KO_TAI5MSG_SELECTIVE_MESSAGE_CLASSIFICATION_READ_ONLY","priority_next_focus":"TAI5MSG_R1_R2_USAGE_MECHANISM_OWNER_CLASSIFICATION_KEEP_R2884_R2885_EVIDENCE_WAIT","historical_full_port_track_status":"FROZEN_DIAGNOSTIC_REFERENCE_CLAIM_SCOPED","legacy_evidence_claim_strength_policy":"selective_ko/LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md","inline_v297_authority":"selective_ko/INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md","ending_help_v298_authority":"selective_ko/ENDING_HELP_39_CANDIDATE_CLASSIFICATION_V298.md","ending_help_v298_artifact":"selective_ko/artifacts/ending_help_39_candidate_classification_v1/INDEX.json","numeric_v299_authority":"selective_ko/INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299.md","numeric_v299_artifact":"selective_ko/artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json","static_v300_authority":"selective_ko/INLINE_R1_STATIC_47_CANDIDATE_CLASSIFICATION_V300.md","static_v300_artifact":"selective_ko/artifacts/inline_r1_static_47_candidate_classification_v1/INDEX.json","inline_r1_source_role_objects":141,"inline_r1_materialized_rows":139,"inline_r1_unresolved_rows":2,"inline_r1_unresolved_rnums":["R2884","R2885"],"selective_candidate_ids":139,"selective_classification_ids":139,"selective_include_ko_rows":139,"selective_r1_materialized_rows":139,"selective_builder_status":"NOT_IMPLEMENTED","selective_build_status":"NONE","identity_presentation_fields":"KEEP_JP","authored_korean_prose_identity_literals":"PRESERVE_AS_AUTHORED_KO","runtime_inserted_identity":"KEEP_JP","identity_reverse_substitution":"FORBIDDEN","switch_original_romfs_status":"NOT_YET_SUPPLIED","required_reads":["selective_ko/INLINE_R1_STATIC_47_CANDIDATE_CLASSIFICATION_V300.md","selective_ko/artifacts/inline_r1_static_47_candidate_classification_v1/INDEX.json","selective_ko/INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299.md","selective_ko/artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json","selective_ko/ENDING_HELP_39_CANDIDATE_CLASSIFICATION_V298.md","selective_ko/artifacts/ending_help_39_candidate_classification_v1/INDEX.json","selective_ko/INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md","selective_ko/LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md","selective_ko/CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md","selective_ko/SELECTIVE_PROJECT_STATE.md","selective_ko/CLASSIFICATION_SCHEMA.md","selective_ko/SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md","selective_ko/KNOWN_FAILURES.md","selective_ko/SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md","selective_ko/IDENTITY_IN_PROSE_POLICY.md","docs/MASTER_RULE_REGISTRY.md","docs/GITHUB_AND_CI_POLICY.md"]}
PROJECT_RESUME_V2 -->

## 1. V300 — ordinary-inline static R1 47 rows materialized

Canonical V300 authority:

`selective_ko/INLINE_R1_STATIC_47_CANDIDATE_CLASSIFICATION_V300.md`

Canonical row artifact:

`selective_ko/artifacts/inline_r1_static_47_candidate_classification_v1/INDEX.json`

V300 adds:

```text
candidate IDs              = 47
classification IDs         = 47
INCLUDE_KO rows            = 47
ID ranges                  = SEL-CAND/SEL-CLS-000093..000139
builder                     = NOT IMPLEMENTED
build / IPS / runtime write = NONE
```

Cumulative selective corpus:

```text
candidate IDs              = 139
classification IDs         = 139
INCLUDE_KO rows            = 139
R1 materialized rows       = 139
```

## 2. Inline R1 closure state

Canonical inline R1 source-role census remains:

```text
INLINE R1 total                         141

V298 ending-help STATIC_COMPLETE         39  materialized INCLUDE_KO
V299 numeric VARIABLE_INSERT             53  materialized INCLUDE_KO
V300 ordinary-inline STATIC_COMPLETE     47  materialized INCLUDE_KO
unresolved static consumer semantics      2  R2884 / R2885
```

Therefore:

```text
materialized = 139
unresolved   = 2
```

`R2884` and `R2885` are evidence waits, not rejected rows. Do not sweep them into inclusion without consumer-length/terminator semantics.

## 3. V300 population invariants

```text
47 unique physical owners
49 unique contributing PC inline records
47 unique R_AARCH64_RELATIVE consumer slots
47 owners with exactly one slot
shared-consumer owners 0
original-guard failures 0
terminator failures 0
capacity failures 0
risk-flagged rows 0
manual overrides 0
INCLUDE_KO 47/47
```

Classification:

```text
usage_class             UI_DESCRIPTION
mechanism_class         STATIC_COMPLETE
investigation_status    RESOLVED
variable_source_kind    NONE
append_after            NO
dynamic_counter_decision NO
```

Special resolved reconstruction cases retained:

```text
R234       fixed prefix inside owner 0x68A2F2
R235       fixed prefix inside owner 0x69DD4F
R485+R486 split PC diff -> owner 0x6A0570
R642+R643 split PC diff -> owner 0x69F2E1
```

The split PC records do not imply runtime fragment composition.

## 4. V299 census correction remains binding

Do not reuse superseded intermediate counts:

```text
numeric objects                         50 -> 53
%d occurrences                         57 -> 60
remaining ordinary inline R1 objects   99 -> 102
inline R1 source-role objects          138 -> 141
```

`%u = 10` remains unchanged.

## 5. Reusable ordinary-inline consumer rule

For these ordinary-inline families, direct code XREF absence is not consumer absence.

Verified route:

```text
.rela.dyn R_AARCH64_RELATIVE (0x403)
 -> r_offset runtime source/consumer slot
 -> r_addend Switch physical text owner
```

Use this route before declaring a similar ordinary-inline owner caller-unknown solely because direct ADR/ADRP string XREF is absent.

This rule is reusable evidence methodology only; it is not blanket inclusion authority for other families.

## 6. V298 / V297 remain inherited

V298 remains authority for ending-help 39.

V297 remains authority for:

- 17,103 inline raw records / 8,751 exact pairs;
- Korean-bearing external positive 204 groups / 206 occurrences;
- 191 single-location occurrences -> 189 logical objects;
- positive multi-match groups 13;
- UNC zero-match correction: 8 padding/NUL + 3 UTF-16LE;
- ending-table structure and reconstruction method;
- R651 selected-use target resolution to `0x6A7C21`;
- reusable diff-run/object-first/source-sequence/fixed-stride/decoder rules.

## 7. Claim boundary

V296 remains binding:

```text
target resolved != WRITE_SAFE
WRITE_SAFE != INCLUDE_KO
INCLUDE_KO != implementation/runtime PASS
build/package PASS != gameplay PASS
```

V300 creates no builder/game write authorization.

## 8. Identity policy

V294 remains closed:

```text
identity presentation fields            = KEEP_JP
authored Korean prose identity literals = PRESERVE_AS_AUTHORED_KO
runtime-inserted identity                = KEEP_JP
identity reverse substitution            = FORBIDDEN
```

## 9. Other containers remain open

Still open:

- `R2884/R2885` consumer/terminator semantics, retained as evidence waits;
- TAI5MSG selective message classification;
- EVENT/TS5 production parser/caller inventory;
- SNR field/record selective parser;
- R2/R3 selective corpus;
- builder/serializer/IPS/build;
- runtime font/layout/translation QA.

The exact PC v1.2.1.0 build-9163702 executable remains unavailable. PC whole-program runtime-parity claims depending on it remain HINT/reference only.

## 10. Next scope

The sole executable next-scope authority is `selective_ko/SELECTIVE_PROJECT_STATE.md`.

After a fresh explicit user signal, resume:

`SELECTIVE_KO_TAI5MSG_SELECTIVE_MESSAGE_CLASSIFICATION_READ_ONLY`

Keep `R2884` and `R2885` as evidence waits unless new shared-route evidence independently resolves them during later work.

Do not begin builder/build/IPS in that scope.

## 11. Repository write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
