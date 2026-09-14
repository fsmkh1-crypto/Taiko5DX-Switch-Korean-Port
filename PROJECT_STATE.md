# PROJECT_STATE

Last updated: 2026-09-14 (KST)

This file is the sole project-resume authority.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION_MATERIALIZED","scope_kind":"REPOSITORY_WRITE","status":"STOPPED_AWAITING_USER_SIGNAL","last_closed_validation_id":"V264","last_closed_stage_commit":"ffa4adc9c83923267c4372feeeccfe0c1786b890","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","mapping_10036_runtime_validation":"docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","mapping_10036_runtime_manifest":"data/post_freeze/mapping_10036_runtime_forward_reverse_hardware_validation_v1/MANIFEST.json","portability_action_population":"docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","portability_action_population_manifest":"data/post_freeze/portability_matrix_action_ledger_population_v1/MANIFEST.json","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md","docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","data/post_freeze/portability_matrix_action_ledger_population_v1/MANIFEST.json","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md","docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md","docs/SWITCH_COUNTERPART_SURVEY_RULES.md","docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","data/post_freeze/mapping_10036_runtime_forward_reverse_hardware_validation_v1/MANIFEST.json","docs/F1_STATIC_WRITE_AUTHORIZATION.md","docs/GITHUB_AND_CI_POLICY.md"]}
PROJECT_RESUME_V2 -->

## Current canonical state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Inherited without revalidation: Stage1, Stage2, F1, FZ001, forward-986, Oracle/Assisted/Astra/TRACE closure, full-corpus coverage/semantic-owner/action-collapse overlays, pointer-56 closure, and Mapping 10,036 through Eden forward/reverse runtime V260.

Canonical inline source accounting remains exactly:

```text
Stage2 affine verified    13,771
F1 accepted mapped         1,311
forward                       986
unique-only gap             1,035
TOTAL                       17,103
```

Existing explicit static WRITE_SAFE authority remains:

```text
F1                         158
Mapping 10,036               4
TOTAL                       162
```

This is not final full-port Action Ledger cardinality.

## Mapping 10,036 current state — through V260

Effective Mapping realization remains four physical actions:

```text
MAP10036_FWD_MISS_HOOK_V1
MAP10036_REV_MISS_HOOK_V1
MAP10036_HELPER_TEXT_V2
MAP10036_DELTA_RODATA_V1
```

All four remain WRITE_SAFE. The exact controlled diagnostic package passed delivery validation, and Eden Android v0.2.1 runtime observation closed the tested Korean forward/reverse route:

```text
forward mapping      PASS
reverse mapping      PASS
runtime round-trip   PASS
renderer/font        NOT VALIDATED BY MAPPING-ONLY BUILD
physical Switch      NOT TESTED
```

Do not reopen Mapping because the Mapping-only diagnostic renders Korean game-field glyphs incorrectly. The same committed `가사힝` value was restored exactly when the surname software keyboard was reopened, separating Mapping conversion/storage from renderer/font work.

Helper coordinate provenance is closed: `0x58CE60` equals decimal `5820000`. Earlier handoff decimal `5811808` was an arithmetic transcription error and must not be reused.

## Portability Matrix / Action Ledger population — V261–V264

The current effective source state and already-canonical structural/counterpart closures are now materialized as a source-complete planning population.

### Inline structural graph

```text
inline source rows                                      17,103
Stage2-internal reduction                                  414
gap-internal + gap/forward net reduction                    69
F1 cross-boundary reduction                                 17
pre-Stage2 <-> Stage2 reduction                             10
                                                      --------
current inline structural owner/action nodes             16,593
```

The 16,593 figure is a structural planning graph only. It is before unresolved terminal/action-ID, pointer cross-axis, visible-yomi, write-safety and implementation closures. It must not be described as final global Action Ledger cardinality.

### F1 planning state

- 158 actions: `DIRECT_PORT / P1 / WRITE_SAFE`.
- 75 padding-reconstruction rows: P1 candidate only after reconstruction safety closes.
- 25 shared-owner rows: target/owner known; final P1/P3 realization and write safety open.
- 4 capacity/NUL failures: realization open; translation shortening is not authorized.
- No other F1 row receives implied WRITE_SAFE from target/sequence closure alone.

### Pointer 56 planning state

```text
source pointer records             56
Switch destination-owner groups    49
mode-1 replacement owners          47
  inline companion groups          43
  pointer-only groups               4
mode-0 destination groups           2
```

All exact 43 mode-1 inline companion sources remain terminal `SUBSUMED_BY` their corresponding non-SUBSUMED pointer redirect logical action. Pointer planning realization is `REDIRECT_PORT / P1` at the static RELA/reference-owner layer.

Still open:
- verified physical storage for the exact 602-byte replacement pool;
- final physical mode-0 destinations for R2411/R2412;
- pointer write safety/runtime/delivery.

Pointer new WRITE_SAFE remains 0.

### Mapping portability state

The closed Switch miss-fallback realization preserves the PC 10,036-entry semantic obligation through a structurally different mechanism. Derived planning portability is:

`P3 — SEMANTIC_PORTABLE / MECHANIC_NOT_PORTABLE`

The four physical Mapping actions remain the implementation realization. No additional mapping count/address action is implied.

### Descriptor/helper population after Mapping closure

PC `mapping_lookup_1` + `mapping_lookup_2` comprise 2 descriptor containers / 5 subpatches. Their table-address/count semantics are represented by the closed Mapping family and are now planning-level `SUBSUMED` candidates.

A final terminal `SUBSUMED_BY` link is not issued yet because a single final non-SUBSUMED logical Mapping action identity above the four physical actions has not been materialized.

Remaining descriptor population:

```text
containers      9
subpatches      9
semantic families 5
```

The five families are:
1. `ui_width` — 4 subpatches;
2. `description_font` — 2 subpatches;
3. `runtime_byte_validation/copy` — 1 subpatch;
4. `font_page_limit/raw threshold` — 1 subpatch;
5. `runtime_page_mapper` — 1 subpatch.

The PC helper's two semantic entries feed `runtime_byte_validation/copy` and `runtime_page_mapper`; they are not counted as two additional independent action families.

These five families remain pending complete Switch counterpart survey and therefore have no final P2/P3/native-equivalent disposition or WRITE_SAFE expansion yet.

### RomFS planning state

RomFS denominator remains 208. Current framework planning model remains:

```text
207 direct-replacement-path items
  1 CWTDAT_JP.TR5 Switch-native reconstruction item
208 total
```

This materialization does not promote the 208 items to item-level terminal dispositions; compatibility/path/format closure remains separate.

## Current open queues

The project must not collapse these independent axes:

- remaining descriptor/helper five-family counterpart completeness;
- broad inline terminal/action-ID and write-safety closure beyond current exact authorizations;
- pointer 602-byte replacement-pool storage and pointer write safety;
- Stage2 visible-yomi runtime/render owner closure;
- RomFS 208 item-level compatibility/disposition;
- final global Action Ledger cardinality;
- final release integration and physical-Switch validation.

Mapping 10,036 is no longer the next Eden-runtime blocker.

## Astra escalation rule

No Astra escalation is indicated for the next scope. Current open work is deterministic counterpart, ownership, capacity/storage and write-safety analysis. Use Astra only if deterministic evidence is exhausted and a genuine semantic/context ambiguity remains.

## Write boundary

Remote GitHub writes remain restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

`create_file`, `update_file`, `delete_file`, `create_branch`, force push, manual text Base64 generation and alternate write routes remain excluded unless a fresh explicit scope changes the transport policy.

## STOP boundary

Status: `STOPPED_AWAITING_USER_SIGNAL`.

Next recommended scope: **`RUNTIME_DESCRIPTOR_HELPER_5_FAMILY_COUNTERPART_SURVEY_READ_ONLY`**.

That scope must survey only the remaining `ui_width`, `description_font`, `runtime_byte_validation/copy`, `font_page_limit/raw threshold`, and `runtime_page_mapper` semantic families. It should inherit Mapping V260 and this V261–V264 population without revalidation, enumerate all Switch counterparts or native-equivalent evidence, derive portability candidates, report unresolved queues, and STOP before any write-safety authorization, diagnostic build, pointer storage work, RomFS work, or broad inline implementation.
