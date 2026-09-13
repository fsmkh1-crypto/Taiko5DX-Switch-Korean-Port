# PROJECT_STATE

Last updated: 2026-09-14 (KST)

This file is the sole project-resume authority.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"MAPPING_10036_SURVEY_AND_REALIZATION_DESIGN_CANONICALIZED","scope_kind":"READ_ONLY","status":"STOPPED_AWAITING_USER_SIGNAL","last_closed_validation_id":"V224","last_closed_stage_commit":"69249d2b32631635a1d728cb4420bd37d2b076e7","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","mapping_10036_survey":"docs/MAPPING_10036_SWITCH_COUNTERPART_SURVEY.txt","mapping_10036_realization_design":"docs/MAPPING_10036_REALIZATION_DESIGN.txt","mapping_10036_index":"data/post_freeze/mapping_10036_canonicalization_v1/INDEX.json","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md","docs/POINTER_56_COMPANION_TERMINAL_DISPOSITION.txt","docs/MAPPING_10036_SWITCH_COUNTERPART_SURVEY.txt","docs/MAPPING_10036_REALIZATION_DESIGN.txt","data/post_freeze/mapping_10036_canonicalization_v1/MEMBERSHIP.json","docs/VALIDATION_LEDGER_MAPPING_10036_CANONICALIZATION.txt","docs/WRITE_TRANSPORT_INCIDENT_20260914.txt","docs/F1_STATIC_WRITE_AUTHORIZATION.md","docs/PC_PATCH_ORACLE_TRACE_19_CLOSURE.md"]}
PROJECT_RESUME_V2 -->

## Current canonical state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Inherited without revalidation: Stage1, Stage2, F1, FZ001, forward-986, Oracle/Assisted/Astra/TRACE closure, full-corpus coverage/semantic-owner/action-collapse overlays, pointer-56 counterpart/cross-axis/non-RELA/terminal closure, and prior validation through V221.

Canonical source accounting remains:

```text
Stage2 13,771
F1 1,311
forward 986
gap 1,035
TOTAL 17,103
```

Existing F1 static WRITE_SAFE authority remains 158. No new WRITE_SAFE is granted here.

## Pointer-56 terminal state

The exact 43 mode-1 inline-zero companion sources are terminally `SUBSUMED` through 43 direct `SUBSUMED_BY` edges to stable non-SUBSUMED pointer redirect actions. Unresolved terminal relations: 0. Mode-1 storage and pointer write safety remain open. Mode-0 final physical owners for `R2411` / `R2412` remain open.

## Mapping 10,036 counterpart survey

Canonical evidence: `docs/MAPPING_10036_SWITCH_COUNTERPART_SURVEY.txt`.

Closed facts:

```text
PC mapping total                         10,036
original mapping                         7,494
Korean suffix                            2,542
Switch direct table-address sites            4
Switch semantic count sites                  2
Korean exact pairs present in original main  0
count-only 7,494 -> 10,036            REJECTED
new WRITE_SAFE                               0
```

The Switch original 7,494-entry mapping prefix is byte-identical to the PC original prefix. Both lookup loops are six-entry equality-terminated scans; 10,036 mod 6 = 4, so direct count replacement is unsafe.

## Mapping 10,036 realization design

Canonical evidence: `docs/MAPPING_10036_REALIZATION_DESIGN.txt`.

Preferred design family: `MAPPING_KOREAN_MISS_FALLBACK_COMPACT_V1`.

Closed design facts:

- original and Korean game-code domains overlap by 0;
- original and Korean Unicode domains overlap by 0;
- keep the original 7,494 table, four direct table references, two count literals and both six-entry loops unchanged;
- handle only genuine original-table misses with Korean fallback;
- Korean game-code side is exactly arithmetic for all 2,542 keys;
- Korean Unicode side is exactly reconstructible using 2,349 one-byte deltas plus fixed PUA arithmetic;
- TEXT alignment padding = 416 bytes;
- RODATA alignment padding = 4,072 bytes;
- private sizing prototype = 324 bytes;
- compact delta stream = 2,349 bytes;
- numerical fit does not authorize storage or write safety.

No storage location is authorized and no implementation has started.

## Remaining mapping open items

- runtime/delivery proof for using the observed TEXT/RODATA alignment padding;
- exact helper bytes and original-byte guards;
- final Action Ledger action identities and write safety;
- runtime Korean round-trip verification and delivery-control validation.

## Write boundary

Allowed remote writes are only `create_blob`, `create_tree`, `create_commit`, `update_ref(force=false)`.

Historical forbidden Contents-API incidents remain provenance only and do not change canonical semantic state. During this canonicalization, transient commit `4de32ce893568ab95c570c4fc697783d6910afa6` created root file `NOPE2`; canonical materialization commit `69249d2b32631635a1d728cb4420bd37d2b076e7` removed it without force/history rewrite and recorded V224.

## STOP boundary

Status: `STOPPED_AWAITING_USER_SIGNAL`.

Next recommended scope: **`MAPPING_10036_ALIGNMENT_PADDING_RUNTIME_VALIDITY_READ_ONLY`**.

That scope is limited to proving or rejecting the runtime/delivery suitability of the already-observed TEXT/RODATA alignment padding for the mapping fallback design. It must not yet implement the fallback, expand WRITE_SAFE, modify builder/runtime/game files, or combine unrelated descriptor families.
