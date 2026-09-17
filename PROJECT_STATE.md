# PROJECT_STATE

Last updated: 2026-09-18 (KST)

This file is the sole repository-level project-resume authority.

The previous canonical state remains inherited in full unless explicitly superseded below.

Current canonical overlay to be materialized by this commit:

```text
scope   INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297
parent  13e51a34c98f9837ba0c6d3be2bb9da6c82acc52
```

All earlier VERIFIED/CLOSED facts, FZ001, Stage1/Stage2, forward-986, Mapping 10,036, Pointer-56, TAI5MSG structure, F1 provenance, V292-V296 policy, rejected hypotheses, and Git write restrictions remain inherited unless explicitly narrowed below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297_MATERIALIZED","scope_kind":"READ_ONLY_ANALYSIS_MATERIALIZATION","status":"V297_MATERIALIZED_ENDING_HELP_CANDIDATE_STAGE_NOT_STARTED","last_closed_validation_id":"V297","canonical_base_commit":"13e51a34c98f9837ba0c6d3be2bb9da6c82acc52","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"repository_update_ref_force":false,"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","active_product_track":"SWITCH_SELECTIVE_KOREANIZATION","selective_subtree_resume_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","exact_next_scope_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","priority_next_scope":"SELECTIVE_KO_ENDING_HELP_39_CANDIDATE_CLASSIFICATION_MATERIALIZATION","historical_full_port_track_status":"FROZEN_DIAGNOSTIC_REFERENCE_CLAIM_SCOPED","legacy_evidence_claim_strength_policy":"selective_ko/LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md","inline_v297_authority":"selective_ko/INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md","selective_candidate_ids":0,"selective_classification_ids":0,"selective_include_ko_rows":0,"selective_builder_status":"NOT_IMPLEMENTED","identity_presentation_fields":"KEEP_JP","authored_korean_prose_identity_literals":"PRESERVE_AS_AUTHORED_KO","runtime_inserted_identity":"KEEP_JP","identity_reverse_substitution":"FORBIDDEN","switch_original_romfs_status":"NOT_YET_SUPPLIED","required_reads":["selective_ko/INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md","selective_ko/LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md","selective_ko/CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md","selective_ko/SELECTIVE_PROJECT_STATE.md","selective_ko/CLASSIFICATION_SCHEMA.md","selective_ko/SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md","selective_ko/KNOWN_FAILURES.md","selective_ko/SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md","selective_ko/IDENTITY_IN_PROSE_POLICY.md","docs/MASTER_RULE_REGISTRY.md","docs/GITHUB_AND_CI_POLICY.md"]}
PROJECT_RESUME_V2 -->

## 1. V297 — inline R1 logical-object reconstruction materialized

Canonical analysis overlay:

`selective_ko/INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md`

This overlay records both the current results and the reusable reconstruction method.

Key source counts:

```text
PC inline raw records                         = 17,103
exact original/replacement semantic groups   = 8,751
external provisional YES                     = 205
external provisional UNCERTAIN               = 227
Korean-bearing external-positive groups      = 204
positive PC source occurrences               = 206
single Switch-location occurrences           = 191
those collapse to distinct logical objects   = 189
positive multi-match semantic groups         = 13
```

External semantic triage is a prefilter only and is not corpus authority.

## 2. V297 ending-table closure

The Switch ending table is structurally closed as:

```text
39 records
record stride = 0x3FF / 1023 bytes

per record:
  title      21 bytes
  help       501 bytes
  narration  501 bytes

offsets:
  help       +0x15
  narration  +0x20A
```

Therefore the table contains 117 text fields:

```text
39 title + 39 help + 39 narration
```

PC patch provenance:

```text
whole ending table PC inline records = 208
help-field PC inline records          = 102
original-byte mismatches              = 0
affine relative-offset violations     = 0
```

Do not repeat the superseded intermediate claim that 39 ending-help fields equal 208 PC records.

## 3. Ending-help 39 source/structure/capacity result

All 39 help fields have complete PC Korean logical payload reconstruction.

Current evidence:

```text
usage_class      = UI_DESCRIPTION
mechanism_class  = STATIC_COMPLETE
append_after     = NO
investigation    = RESOLVED for analyzed ending-help route
field capacity   = 501 bytes
max KO payload including NUL = 412 bytes
minimum slack    = 89 bytes
capacity PASS    = 39/39
```

These facts do not yet create `INCLUDE_KO` rows. Candidate/classification materialization is the next separate stage.

## 4. UI prompt multi-match closure

Previously outstanding prompt owners are now closed except only where historical artifacts remain as provenance.

Verified row-level owners retained:

```text
R645 / INLINE:00644 -> target_object 6938194 / DIRECT / owner_count 1
R2799 / INLINE:02798 -> target_object 6862647 / DIRECT / owner_count 1
R2975 / INLINE:02974 -> target_object 6957335 / DIRECT / owner_count 1
R3013 / INLINE:03012 -> target_object 6921870 / DIRECT / owner_count 1
```

R651 was historically unresolved in L3. V297 resolves selected-use target binding by source-sequence evidence:

```text
R649 anchor `投資する` -> 0x6A7C18
R651 investment prompt -> 0x6A7C21
R652 suffix -> same object at 0x6A7C39
resulting object -> `いくら投資しますか？\n(1000～%d)`
```

The alternate raw candidate belongs to a different semantic object and fails the same source sequence.

Historical L3 files are retained unchanged as provenance; V297 supersedes only R651's selected-use target-resolution status.

## 5. Reusable method rules

The following are canonical reusable analysis rules from V297:

1. `PC diff-run != logical string`; reconstruct against Switch object/field boundaries before classification.
2. A PC replacement may consume original NUL padding; the Japanese first NUL is not automatically the Korean structural end.
3. Prefer object-first reconstruction: source diff -> Switch object -> complete Korean payload -> usage/mechanism -> owner/caller/capacity -> disposition.
4. Use original-byte guards plus family-bounded relative-offset affine validation for contiguous/table families.
5. For raw multi-match, use adjacent PC source sequence and same-object containment; raw equality/uniqueness alone is not owner proof.
6. Detect repeated tables through stable stride, stable field offsets, and caller indexing arithmetic.
7. PC inline decode precedence: compact one-byte Hangul 0xA1..0xDF -> Korean-added two-byte mapping domain -> ordinary CP932.
8. Do not use the whole Mapping 10,036 table as a naive inverse decoder because code aliases can misdecode ordinary CP932.
9. UTF-16/mixed PC UI strings are a distinct family and must not be counted as failed CP932 Switch matches.

## 6. Superseded intermediate claims

```text
`189 unique positive occurrences`
  -> correct: 191 single-location occurrences -> 189 logical objects

`39 ending-help = 208 PC records`
  -> correct: 39 help = 102 PC records; full ending table = 208

`UNC zero-match NUL/padding = 7`
  -> correct: 8 padding/NUL + 3 UTF-16LE

`R651 requires exact PC EXE to resolve target`
  -> rejected for selected-use target binding
```

## 7. V296 trust boundary remains binding

The full-port failure does not invalidate verified low-level data.

Still binding:

```text
target resolved != WRITE_SAFE
WRITE_SAFE != INCLUDE_KO
owner resolved != release inclusion
build/package PASS != gameplay PASS
exact-route runtime PASS != all-route PASS
```

V289-V291 full-port assembly remains excluded as selective product baseline.

## 8. Exact PC EXE limitation remains

The exact PC v1.2.1.0 build-9163702 executable remains unavailable.

Claims depending on exact PC whole-program XREF/call-site/runtime parity cannot exceed their existing evidence boundary. Do not restart a blanket exact-PC-EXE hunt merely because V297 exists.

This does not reopen V297 ending-help or R651 closure because those use exact PC patch bytes plus Switch-native structure/source sequence.

## 9. Current materialization counts

V297 creates analysis authority only.

```text
candidate IDs                 = 0
classification IDs            = 0
selective INCLUDE_KO rows     = 0
selective builder             = NOT IMPLEMENTED
selective build               = NONE
new gameplay WRITE_SAFE       = 0
IPS/runtime artifact          = NONE
```

## 10. Next scope

The next recommended scope, only after a fresh explicit user execution signal, is:

`SELECTIVE_KO_ENDING_HELP_39_CANDIDATE_CLASSIFICATION_MATERIALIZATION`

Purpose:

- materialize the 39 ending-help candidates with exact source/object provenance;
- carry forward `UI_DESCRIPTION + STATIC_COMPLETE + RESOLVED + 39/39 capacity PASS` evidence;
- derive dispositions only after all required common metadata/risk gates are represented;
- record the R651 selected-use resolution as provenance;
- do not mix builder/build/IPS work into the same stage.

The broader container inventory remains open for TAI5MSG/EVENT/SNR after the R1 ending-help candidate materialization stage.

## 11. Repository write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No `create_file`, `update_file`, `delete_file`, `create_branch`, issue/PR write, or force update is permitted.

A fresh explicit user execution signal is required after V297 materialization is reported before the next analysis/materialization/build stage.