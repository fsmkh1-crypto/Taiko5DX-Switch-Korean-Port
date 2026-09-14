# PROJECT_STATE

Last updated: 2026-09-14 (KST)

This file is the sole project-resume authority.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"RUNTIME_BYTE_VALIDATION_COPY_CONSUMER_CENSUS_MATERIALIZED","scope_kind":"REPOSITORY_WRITE","status":"STOPPED_AWAITING_USER_SIGNAL","last_closed_validation_id":"V270","last_closed_stage_commit":"c49b3410c32ab5428c494a6841dcf7c3c825eb9f","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","mapping_10036_runtime_validation":"docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","mapping_10036_runtime_manifest":"data/post_freeze/mapping_10036_runtime_forward_reverse_hardware_validation_v1/MANIFEST.json","portability_action_population":"docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","portability_action_population_manifest":"data/post_freeze/portability_matrix_action_ledger_population_v1/MANIFEST.json","runtime_byte_copy_census":"docs/RUNTIME_BYTE_VALIDATION_COPY_CONSUMER_CENSUS.txt","runtime_byte_copy_manifest":"data/post_freeze/runtime_byte_validation_copy_consumer_census_v1/MANIFEST.json","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md","docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","data/post_freeze/portability_matrix_action_ledger_population_v1/MANIFEST.json","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md","docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md","docs/SWITCH_COUNTERPART_SURVEY_RULES.md","docs/RUNTIME_BYTE_VALIDATION_COPY_CONSUMER_CENSUS.txt","data/post_freeze/runtime_byte_validation_copy_consumer_census_v1/MANIFEST.json","docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","data/post_freeze/mapping_10036_runtime_forward_reverse_hardware_validation_v1/MANIFEST.json","docs/F1_STATIC_WRITE_AUTHORIZATION.md","docs/GITHUB_AND_CI_POLICY.md"]}
PROJECT_RESUME_V2 -->

## Current canonical state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Inherited without revalidation: Stage1, Stage2, F1, FZ001, forward-986, Oracle/Assisted/Astra/TRACE closure, full-corpus coverage/semantic-owner/action-collapse overlays, pointer-56 closure, Mapping 10,036 through Eden forward/reverse runtime V260, and portability/action population V261-V264.

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

The current effective source state and already-canonical structural/counterpart closures remain materialized as a source-complete planning population.

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

The closed Switch miss-fallback realization preserves the PC 10,036-entry semantic obligation through a structurally different mechanism. Derived planning portability remains:

`P3 — SEMANTIC_PORTABLE / MECHANIC_NOT_PORTABLE`

The four physical Mapping actions remain the implementation realization. No additional mapping count/address action is implied.

## Runtime byte-validation/copy counterpart census — V265–V270

This family is now canonically separated into downstream renderer/decode compatibility and upstream normalization/copy behavior.

### Downstream renderer/decode layer

Surveyed Switch per-character decode family around mapped `0x445C60`:

```text
direct callers                  6
A1..DF one-byte handling        preserved
81..9F / E0..FC two-byte leads  supported
EB..F8 Korean lead subset       included
```

A compact Korean byte that reaches this layer is not rejected by the renderer/decode logic itself.

### Upstream normalization/copy layer

A distinct generic parsing/normalization path exists before rendering. Default Japanese halfwidth handling can transform the `0xA6..0xDF` range rather than raw-preserve it. That range overlaps compact Korean single-byte values used by the PC patch.

The representative generic parser/wrapper family has:

```text
direct call sites  1,078
```

Separate text-object paths expose per-slot conversion controls, with observed OFF/ON patterns consistent with main-text versus auxiliary/yomi separation. Therefore Japanese halfwidth normalization must not be globally disabled.

### PC compact-byte source exposure

Within the canonical 17,103 PC inline replacements:

```text
records containing A1..DF compact byte   2,474
records containing A6..DF susceptible    2,057
```

These values are source-risk upper bounds, not action counts. They do not imply that all 2,057 rows traverse the generic normalizer.

### Family disposition

Current canonical planning result:

```text
COUNTERPART_FOUND
NATIVE_EQUIVALENT_REJECTED
RUNTIME_PORT_REQUIRED_CANDIDATE
P3 candidate — SEMANTIC_PORTABLE / MECHANIC_NOT_PORTABLE
```

Reason: downstream decode is compatible, but upstream Switch-native Japanese halfwidth normalization can alter overlapping compact Korean values before rendering. The likely solution must preserve Korean compact semantics inside the existing Switch parser/normalization ownership model rather than mechanically transplant the PC x86 helper.

This is not yet a final terminal action. Exact source-family -> route -> minimum runtime-owner binding remains open.

Rejected hypotheses preserved canonically:
- decoder acceptance alone proves family-level native equivalence;
- all compact Korean bytes fail on all Switch paths;
- the cause is limited to one previously observed glyph;
- Japanese halfwidth normalization may be globally disabled;
- the PC x86 helper should be mechanically transplanted.

New WRITE_SAFE authority from V265-V270: 0.

## Descriptor/helper scope boundary

The broader five-family survey was not promoted by V265-V270. This stage only canonicalizes `runtime_byte_validation/copy`.

Therefore `ui_width`, `description_font`, `font_page_limit/raw threshold`, and `runtime_page_mapper` retain their prior canonical status unless and until separately materialized. Do not infer new terminal disposition or WRITE_SAFE for those four families from this state.

## RomFS planning state

RomFS denominator remains 208. Current framework planning model remains:

```text
207 direct-replacement-path items
  1 CWTDAT_JP.TR5 Switch-native reconstruction item
208 total
```

No item-level terminal disposition is added here.

## Current open queues

Keep these axes separate:

- compact Korean source/storage -> normalization/renderer route binding for the 2,057 risk-bearing upper-bound rows;
- the four other remaining descriptor/helper families unless separately canonicalized;
- broad inline terminal/action-ID and write-safety closure beyond current exact authorizations;
- pointer 602-byte replacement-pool storage and pointer write safety;
- Stage2 visible-yomi runtime/render owner closure;
- RomFS 208 item-level compatibility/disposition;
- final global Action Ledger cardinality;
- final release integration and physical-Switch validation.

## Astra escalation rule

No Astra escalation is indicated for the next scope. The remaining byte-copy work is deterministic storage/consumer/control-flow route binding. Use Astra only if deterministic evidence is exhausted and a genuine semantic/context ambiguity remains.

## Write boundary

Remote GitHub writes remain restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

`create_file`, `update_file`, `delete_file`, `create_branch`, force push, manual text Base64 generation and alternate write routes remain excluded unless a fresh explicit scope changes the transport policy.

## STOP boundary

Status: `STOPPED_AWAITING_USER_SIGNAL`.

Next recommended scope: **`RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_READ_ONLY`**.

That scope must group the 2,057 risk-bearing source rows by storage/consumer family rather than inspect isolated records, bind each family to direct-renderer/generic-normalizer/explicit-yomi or any other proven route, determine the active normalization mode/context and output-preservation behavior, and STOP before any implementation, write-safety authorization, diagnostic build, pointer storage work, RomFS work, or unrelated descriptor-family implementation.

## A auxiliary name-row hold — 2026-09-14

Status: `HOLD_FOR_CWTDAT`.

Reference: `docs/CWTDAT_AUXILIARY_NAME_ROW_HOLD.md`.

Current read-only work narrowed the observed garbled protagonist-selection/dialogue auxiliary name rows away from the previously tested shared-yomi/Y0 route and toward the person-reading data relationship between SNR display names and `CWTDAT_JP.TR5`. The PC data comparison indicates a parallel 1,244-person Japanese reading table in CWTDAT aligned by person index; exact PC final-draw XREF remains open, so this is retained as a strong working conclusion rather than final runtime proof.

Do not create a standalone A fix before CWTDAT work. When Switch-native `CWTDAT_JP.TR5` reconstruction is explicitly started, the 1,244-person reading-table counterpart and both affected UI rows are mandatory validation items. Reopen A as an independent runtime binding family only if a structurally correct CWTDAT reconstruction leaves the rows broken.
