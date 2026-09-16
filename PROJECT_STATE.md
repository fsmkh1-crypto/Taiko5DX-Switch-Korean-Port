# PROJECT_STATE

Last updated: 2026-09-16 (KST)

This file is the sole project-resume authority.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"KO_GRAMMAR_FLATTENING_ADVERSARIAL_REVIEW_MATERIALIZED_NEXT_567_MATRIX","scope_kind":"READ_ONLY","status":"KO_GRAMMAR_FLATTENING_REVIEW_MATERIALIZED_NEXT_READ_ONLY","last_closed_validation_id":"V281","last_closed_stage_commit":"22f46107cd1638d9069d9416dff296a9655d6b72","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","schema_freeze_declaration":"data/pilot/f1_v1_candidate/schema_freeze_declaration.json","schema_freeze_declaration_git_blob_sha":"6c726b7d004753e2f49f63640bd4f6df343dd736","schema_freeze_basis_validation_id":"V107","schema_freeze_basis_ci_run_id":34691523117,"schema_freeze_basis_head":"ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_allowed":["PASS","NOT_APPLICABLE"],"runtime_byte_route_latest_commit":"39e5999d5bc24173b39521acec459a205ae42540","dialogue_formatter_graph_diff":"docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md","dialogue_formatter_ko_design":"docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","dialogue_formatter_ko_review_validation":"V281","priority_next_scope":"KO_GRAMMAR_FLATTEN_CALLER_STYLE_BRANCH_AVAILABLE_567_MATRIX_READ_ONLY","mapping_10036_runtime_validation":"docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","portability_action_population":"docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","runtime_byte_copy_census":"docs/RUNTIME_BYTE_VALIDATION_COPY_CONSUMER_CENSUS.txt","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md","docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md","docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md","docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","docs/VALIDATION_LEDGER_KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.txt","docs/RUNTIME_BYTE_VALIDATION_COPY_CONSUMER_CENSUS.txt","docs/RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_PROGRESS_20260915.md","docs/RUNTIME_BYTE_COPY_NORMALIZATION_LOWLEVEL_OWNER_CHECKPOINT_20260915.md","docs/RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_C2_TABLE_CLOSURE_20260915.md","docs/RUNTIME_BYTE_COPY_NORMALIZATION_GENERIC_PARSER_OWNER_CLOSURE_20260915.md","docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","docs/F1_STATIC_WRITE_AUTHORIZATION.md","docs/GITHUB_AND_CI_POLICY.md"]}
PROJECT_RESUME_V2 -->

## 1. Current canonical state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Inherited without revalidation:

- Stage1, Stage2, F1, FZ001;
- forward-986 and Oracle/Assisted/Astra/TRACE closure;
- full-corpus coverage / semantic-owner / action-collapse overlays;
- pointer-56 closure;
- Mapping 10,036 through Eden forward/reverse runtime V260;
- portability/action population V261-V264;
- runtime-byte validation/copy census V265-V270;
- post-V270 runtime-byte route-binding checkpoints;
- issue-C PC original -> PC Korean formatter graph-diff closure materialized on 2026-09-16;
- document-governance drift repair V271;
- Korean dialogue grammar-responsibility analysis and initial `KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1` design materialization V272-V276;
- whole grammar-family census, caller migration census, and adversarial speech-style/morphology review V277-V281.

A new chat/model/automation run is not a reason to reopen VERIFIED facts.

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

The Korean grammar-flattening design and V277-V281 review add no WRITE_SAFE,
implementation authorization, build authorization, or gameplay-data mutation authority.

## 2. Mandatory PC patch oracle entry gate

Status: `MANDATORY`.

Allowed continuation states only:

```text
PC_PATCH_ORACLE_GATE=PASS
PC_PATCH_ORACLE_GATE=NOT_APPLICABLE
```

`UNKNOWN` blocks Switch-side root-cause analysis and design.

Mandatory order:

```text
PC counterpart/applicability
-> actual PC Korean-patch evidence / semantic obligation
-> Switch native counterpart / root-cause analysis
-> Switch realization/design
```

Rules:

- Existing VERIFIED exact-family PC evidence may satisfy the gate without revalidation.
- Inspect actual replacement data, runtime/helper descriptors, mapping, pointer behavior,
  encoding and output semantics before Switch-specific hypotheses.
- Reproduce PC semantic obligations, not Windows/x86 mechanics.
- If PC patch data and Switch runtime output differ, treat the mismatch as
  port/runtime/composition/normalization/rendering evidence before modifying source data.
- Korean names, place names, readings, glyph codes and translations available from the
  PC patch are never guessed.
- When exact PC runtime provenance is unavailable, do not promote a different PC build
  to exact-target authority. Record the limitation and proceed only on evidence that is
  actually available for the selected design question.

## 3. Mapping 10,036 — closed realization through V260

Effective physical actions remain:

```text
MAP10036_FWD_MISS_HOOK_V1
MAP10036_REV_MISS_HOOK_V1
MAP10036_HELPER_TEXT_V2
MAP10036_DELTA_RODATA_V1
```

All four remain WRITE_SAFE.

Eden Android runtime observation closed the tested mapping route:

```text
forward mapping      PASS
reverse mapping      PASS
runtime round-trip   PASS
renderer/font        NOT VALIDATED BY MAPPING-ONLY BUILD
physical Switch      NOT TESTED
```

Do not reopen Mapping because of unrelated renderer/font/dialogue symptoms.

## 4. Portability / Action Ledger planning state — V261-V264

Current inline structural owner/action nodes: `16,593` from the canonical 17,103
inline source rows after verified structural reductions. This remains a planning
graph, not final global Action Ledger cardinality.

F1:

- 158 `DIRECT_PORT / P1 / WRITE_SAFE`;
- 75 padding-reconstruction rows remain non-authorized;
- 25 shared-owner rows remain realization/write-safety open;
- 4 capacity/NUL failures remain realization open;
- target resolution alone does not create WRITE_SAFE.

Pointer 56:

```text
source pointer records             56
Switch destination-owner groups    49
mode-1 replacement owners          47
  inline companion groups          43
  pointer-only groups               4
mode-0 destination groups           2
```

Open pointer items remain 602-byte replacement-pool physical storage, final mode-0
destinations for R2411/R2412, and pointer write safety/runtime/delivery.
Pointer new WRITE_SAFE = 0.

## 5. Runtime byte-validation/copy — V265-V270 baseline

Downstream Switch per-character decoder family around `0x445C60` accepts the relevant
compact Korean one-byte values and ordinary two-byte lead ranges when bytes reach it.

PC compact-byte exposure within the 17,103 inline source rows:

```text
records containing A1..DF compact byte   2,474
records containing A6..DF susceptible    2,057
```

The 2,057 figure is a source-risk upper bound, not an action count.

V270 family disposition remains:

```text
COUNTERPART_FOUND
NATIVE_EQUIVALENT_REJECTED
RUNTIME_PORT_REQUIRED_CANDIDATE
P3 candidate — SEMANTIC_PORTABLE / MECHANIC_NOT_PORTABLE
```

Global Japanese halfwidth disable and mechanical PC x86-helper transplant remain rejected.

## 6. Post-V270 runtime-byte route-binding checkpoints — canonical analysis evidence

Canonical commits:

```text
d448be60739c5e3b81ddaf4f1d4b4652bc2669a9  route-binding progress
00c83f1972f67eb05cd57515304ec563d8fc32c5  low-level halfwidth owner binding
a5ba9b35f6c5c301bc6536763f15b05cf3aca2c8  dominant C2 table consumer closure
39e5999d5bc24173b39521acec459a205ae42540  generic parser owner closure
```

These are read-only analysis checkpoints layered on V270. They do not alter frozen
accounting or authorize a build.

### 6.1 Risk-row partition

Exact denominator remains 2,057:

```text
Stage2 affine target-resolved   1,993
non-Stage2                         64
TOTAL                           2,057

Stage2 RODATA                   1,953
Stage2 DATA                        40
```

Major Stage2 families:

- `0x711DA0 / stride 0xC2` structured RODATA family: 1,686 risk rows;
- place-table: 32 = 17 display-name starts + 15 yomi starts;
- remaining Stage2 RODATA/DATA grouped families remain open.

### 6.2 Concrete Switch normalization owners

Behaviorally verified:

```text
ordinary halfwidth-kana mapper        0x43497C
unique direct mapper call             0x156F30
generic parser body                   0x156D80
generic parser external wrapper       0x157C30
wrapper direct callers                9
C2 auxiliary conversion boundary      0x43FD20
canonical per-character decoder       0x445C60
```

`0x43497C` maps ordinary Japanese halfwidth `0xA6..0xDD` through RODATA `0x6A856A`;
`0xDE/0xDF` belong to an adjacent modifier/composition family.

`0x263C5C` is explicitly rejected as normalizer owner; its earlier 1,078-caller count
was numerical coincidence.

### 6.3 Dominant C2 route separation

The same `0xC2` record family has distinct semantics:

```text
primary/display record uses         direct text/render-decode consumers
eight display slots +0x28..+0x9F   direct text/render-decode consumers
+0x11 auxiliary field               explicit conversion via 0x43FD20
```

Observed display routes reach `0x445C60` without the `0x43FD20` auxiliary conversion
boundary. A table-wide/global normalization override is therefore rejected.

### 6.4 Generic parser owner closure

The halfwidth mapper call is inside parser body `0x156D80`; wrapper `0x157C30` has
exactly nine direct callers. Wrapper integer arguments are not a simple halfwidth
ON/OFF flag; that hypothesis is rejected.

The C2 `+0x11 -> 0x43FD20` conversion route is separate from the generic parser
halfwidth route.

### 6.5 Remaining runtime-byte work

After issue C is structurally closed, resume this family by:

- classifying the nine `0x157C30` caller contexts by canonical source/storage owner;
- materializing exact route membership/cardinality for all 2,057 risk rows;
- binding remaining Stage2 block families;
- reusing existing F1/forward/gap provenance for the 64 non-Stage2 rows;
- identifying a safe Korean compact-data/context discriminant before any parser patch design.

No implementation or diagnostic build is authorized yet.

## 7. Dialogue malformed-ending issue C — REVIEWED KOREAN GRAMMAR-FLATTENING DESIGN

Status: `KO_GRAMMAR_FLATTENING_REVIEW_MATERIALIZED_NEXT_READ_ONLY`.

Current design authority:

`docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md`

Current validation authority for this family:

`docs/VALIDATION_LEDGER_KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.txt` through V281.

Representative real-device symptoms include:

- `조금 과음한 모양이이오군`
- `오늘은 이만 실례하하겠습니다`
- `야규님입니다인가`

### 7.1 PC_PATCH_ORACLE_GATE and data authority

`PASS` for the data/design question.

Canonical source identities:

```text
JP original TAI5MSG_JP.DAT
  size    1,810,889
  sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f

PC Korean v1.02 TAI5MSG_JP.DAT
  size    2,134,366
  sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090

Official SC TAI5MSG_SC.DAT
  size    1,918,773
  sha256  04ff8afe290b12f2f7b93e174952f5c7550acff1ef0fe17b96d889170e0a706e

Official TW TAI5MSG_TW.DAT
  size    1,944,333
  sha256  bf165a3f30b72045ea5f92e5acca45a950be4d94294cc10e82576f3fffcb0294
```

The earlier graph-diff closure remains valid: all 471 PC original -> PC Korean block-0
messages preserve their control/graph skeleton while literals change where translated.

### 7.2 Exact PC runtime provenance correction

The exact PC executable required by v1.02 is unavailable.

Required target:

```text
size    18,685,960
sha256  10C69BAB50D29BAF6311360CAFBF7383716A126A6484D209F5E299E12AB565A2
```

The Drive EXE previously used for exploratory formatter disassembly is a different
18,479,304-byte build. Therefore any previous assertion that exact v1.02 PC and Switch
`0x43/0x4A` cursor/return semantics were proven equal is withdrawn from canonical
status. Exact target runtime parity remains unavailable/unproven.

Do not search for that missing EXE again merely to continue the selected Korean design.

### 7.3 Korean responsibility collision

Actual PC Korean formatter literals carry complete Korean inflectional/register material.
Representative boundaries are structurally equivalent to:

```text
`...모양이` + C73 branch `이오` + `군`
`...실례하` + C188 branch `하겠습니다`
C51 + C342 + `인가`
```

The issue is a shared Korean grammatical-responsibility boundary problem, not a local
repeated-syllable cleanup problem.

Raw identical-syllable overlap is only a lower-bound detector. Korean morphology can
already be owned by the caller without identical adjacent syllables, as illustrated by
C109 forms combined after caller material such as `기다리셨`, `기다렸`, or `실패했`.

### 7.4 Whole-family census — V277

The externally used block-0 entry population is closed at:

```text
external entry families             73
GRAMMAR_FLATTEN                       42 / 2,364 KO calls
DYNAMIC_MEANING_RETAIN                31 / 4,254 KO calls
MIXED_SPLIT_REQUIRED                   0
UNRESOLVED                             0
TOTAL external calls               6,618
```

The grammar cluster recursively covers exactly `C65..C358`, 294 nodes, with no
internal edge crossing into the retained dynamic-semantic clusters.

The 2,364 grammar edges occur in 1,013 unique caller messages; 386 of those callers also
carry dynamic semantic calls that must remain dynamic.

### 7.5 Initial caller matrix — V278

Initial structural reference classes were:

```text
DIRECT_STATIC_FLATTEN                 591 callers / 1,252 grammar edges
DIRECT_DYNAMIC_PRESERVE               322 callers /   835 grammar edges
CN_SEMANTIC_DIVERGENCE_REVIEW          42 callers /   168 grammar edges
GRAMMAR_RESIDUAL_EXCEPTION_REVIEW      58 callers /   109 grammar edges
TOTAL                               1,013 callers / 2,364 grammar edges
```

All 1,013 compared callers preserve their branch-marker sequence across JP/KO/SC/TW.
This supports control-skeleton preservation, not automatic Korean tone collapse.

The former 913 `DIRECT_*` callers are no longer treated as automatically migratable.
That interpretation is superseded by V279.

### 7.6 Adversarial speech-style review — V279

All 42 grammar families carry multiple Korean output/register variants. `0x6A` remains
a real speech-style selector; global inversion remains rejected.

Across all 1,013 callers:

```text
direct caller-level 0x6A branch      601 / 1,494 grammar edges
no direct caller-level 0x6A branch   412 /   870 grammar edges
```

Within the former 913 structurally-direct population:

```text
CALLER_STYLE_BRANCH_AVAILABLE         567 / 1,356 grammar edges
STYLE_COLLAPSE_REVIEW                 346 /   731 grammar edges
```

The 567 population is the preferred first detailed matrix because caller-local
style/control branches already exist and can be preserved. The 346 population must not
be auto-flattened; nested formatter register/tone loss requires explicit review.

### 7.7 Composition/morphology review — V280

Simple visible adjacency risk census:

```text
left-side stored overlap        604 grammar edges
right-side Hangul continuation  728 grammar edges
left only                        458
right only                       582
both                             146
neither                        1,178
```

At least 1,186 grammar edges across 601 callers are visibly composition-coupled. This is
a lower bound, not a rewrite classifier. Korean morphology can collide without literal
syllable equality, so dedup/prefix/suffix boundary rules remain rejected.

### 7.8 Reviewed Korean design contract — V281

Design remains:

`KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1`

Core rule remains:

`preserve dynamic meaning / flatten inherited Japanese dynamic grammar`

Current mandatory contract:

```text
preserve caller control/branch skeleton
preserve required dynamic semantic call IDs/order
flatten inherited Japanese grammar segmentation into branch-local natural Korean
never collapse nested formatter register/tone implicitly
explicitly adjudicate STYLE_COLLAPSE_REVIEW / TONE_CRITICAL_EXCEPTION where required
use SC/TW as structural evidence only, not Korean wording/tone authority
```

No grammar formatter family is globally blanked before all caller obligations are
migrated and residuals are explicitly accounted.

### 7.9 Prohibited C repair paths

Remain rejected:

- local screenshot-by-screenshot correction;
- global `하하 -> 하`;
- global `이이 -> 이`;
- repeated-syllable/longest-overlap dedup;
- fixed left/right prefix/suffix trimming;
- forced C8:87 result;
- global `0x6A` inversion;
- universal first-syllable stripping from C73/C188;
- globally blanking C65..C358 before every caller is migrated/accounted;
- treating official SC/TW as Korean tone/register authority;
- treating the former 913 structurally-direct callers as automatic migration authority;
- requiring recovery of the unavailable exact PC target EXE before design can proceed.

### 7.10 Exact next closure question

Current next scope:

`KO_GRAMMAR_FLATTEN_CALLER_STYLE_BRANCH_AVAILABLE_567_MATRIX_READ_ONLY`

That analysis may enumerate the 567 callers, each grammar-edge occurrence, caller branch
ownership, dynamic semantic obligations, speaker/tone obligations, and post-migration
invariants.

It may not mutate Korean text or TAI5MSG, modify the builder, patch runtime code,
generate IPS, create a diagnostic build, or add WRITE_SAFE authority.

Issue C remains the top priority until the caller migration obligations and exceptions
are structurally closed.

## 8. CWTDAT / issue A hold

Status: `HOLD_FOR_CWTDAT`.

Reference: `docs/CWTDAT_AUXILIARY_NAME_ROW_HOLD.md`.

The auxiliary protagonist-selection/dialogue name-row issue is parked under future
CWTDAT work. Existing comparison indicates a parallel 1,244-person Japanese reading
table aligned by person index; exact PC final-draw XREF remains open.

When CWTDAT work resumes after C:

1. decompose actual PC patched CWTDAT by semantic/function family;
2. find each Switch native counterpart/owner;
3. classify native equivalent / data reconstruction / runtime port / unresolved;
4. include the 1,244-person reading table and both affected UI rows as mandatory validation items;
5. do not overwrite the Switch file wholesale with the PC file.

## 9. RomFS / remaining project queues

RomFS denominator remains 208:

```text
207 direct-replacement-path items
  1 CWTDAT_JP.TR5 Switch-native reconstruction item
208 total
```

Other open axes after C, according to canonical priority:

- remaining runtime-byte route membership;
- four other descriptor/helper families unless separately materialized;
- broad inline terminal/action-ID and write-safety closure beyond exact authorizations;
- pointer replacement-pool storage and pointer write safety;
- Stage2 visible-yomi runtime/render owner closure;
- RomFS item-level compatibility/disposition;
- final global Action Ledger cardinality;
- release integration and physical-Switch validation.

## 10. Write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

Never use `create_file`, `update_file`, `delete_file`, `create_branch`, force push,
or alternate write routes.

## 11. Current STOP / priority boundary

The adversarial review through V281 is now the current canonical refinement of
`KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1`.

Current priority next scope is:

**`KO_GRAMMAR_FLATTEN_CALLER_STYLE_BRANCH_AVAILABLE_567_MATRIX_READ_ONLY`**

A fresh explicit user execution signal is required before beginning that analysis.

No C implementation, translation mutation, TAI5MSG rewrite, builder change, build, IPS,
runtime patch, or new WRITE_SAFE authority is authorized by this materialization.
