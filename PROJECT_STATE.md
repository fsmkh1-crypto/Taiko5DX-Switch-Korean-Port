# PROJECT_STATE

Last updated: 2026-09-16 (KST)

This file is the sole project-resume authority.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN_MATERIALIZED_NEXT_CENSUS","scope_kind":"READ_ONLY","status":"KO_GRAMMAR_FLATTENING_DESIGN_MATERIALIZED_NEXT_READ_ONLY","last_closed_validation_id":"V276","last_closed_stage_commit":"44970ade58f09e70a9fdbec3a972ef6981a9eccb","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","schema_freeze_declaration":"data/pilot/f1_v1_candidate/schema_freeze_declaration.json","schema_freeze_declaration_git_blob_sha":"6c726b7d004753e2f49f63640bd4f6df343dd736","schema_freeze_basis_validation_id":"V107","schema_freeze_basis_ci_run_id":34691523117,"schema_freeze_basis_head":"ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_allowed":["PASS","NOT_APPLICABLE"],"runtime_byte_route_latest_commit":"39e5999d5bc24173b39521acec459a205ae42540","dialogue_formatter_graph_diff":"docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md","dialogue_formatter_ko_design":"docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","priority_next_scope":"DIALOGUE_FORMATTER_GRAMMAR_GENERATOR_FAMILY_CENSUS_AND_CLASSIFICATION_READ_ONLY","mapping_10036_runtime_validation":"docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","portability_action_population":"docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","runtime_byte_copy_census":"docs/RUNTIME_BYTE_VALIDATION_COPY_CONSUMER_CENSUS.txt","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md","docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md","docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md","docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","docs/RUNTIME_BYTE_VALIDATION_COPY_CONSUMER_CENSUS.txt","docs/RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_PROGRESS_20260915.md","docs/RUNTIME_BYTE_COPY_NORMALIZATION_LOWLEVEL_OWNER_CHECKPOINT_20260915.md","docs/RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_C2_TABLE_CLOSURE_20260915.md","docs/RUNTIME_BYTE_COPY_NORMALIZATION_GENERIC_PARSER_OWNER_CLOSURE_20260915.md","docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","docs/F1_STATIC_WRITE_AUTHORIZATION.md","docs/GITHUB_AND_CI_POLICY.md"]}
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
- Korean dialogue grammar-responsibility analysis and `KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1` design materialization V272-V276.

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

The Korean grammar-flattening design adds no WRITE_SAFE, implementation authorization,
build authorization, or gameplay-data mutation authority.

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

## 7. Dialogue malformed-ending issue C — KOREAN GRAMMAR-FLATTENING DESIGN MATERIALIZED

Status: `KO_GRAMMAR_FLATTENING_DESIGN_MATERIALIZED_NEXT_READ_ONLY`.

Current design authority:

`docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md`

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

Actual PC Korean formatter literals carry complete Korean inflectional material. Key
examples include C73 copula/register forms and C188 `하다` register forms.

Representative boundaries are structurally equivalent to:

```text
`...모양이` + C73 branch `이오` + `군`
`...실례하` + C188 branch `하겠습니다`
```

Whole-corpus caller-shape evidence:

```text
C73 calls immediately preceded by Korean code for `이`    97
C188 calls immediately preceded by Korean code for `하`   66
```

These are risk-shape counts, not rewrite counts.

The issue is therefore treated as a Korean grammatical responsibility-boundary
problem rather than a local repeated-syllable cleanup problem.

### 7.4 Official SC/TW structural reference

External non-block-0 -> block-0 call totals:

```text
JP original   6,618
PC Korean     6,618
Official SC   4,233
Official TW   4,263
```

Representative grammar families are largely flattened by SC/TW:

```text
          JP    KO    SC    TW
C73      660   660    13    21
C188     155   155     1     1
C342     154   154     0     0
C209     264   264     1     3
C125     192   192     1     1
C272      84    84     0     0
C244      76    76     1     1
C202      73    73     2     4
```

Dynamic semantic-value families are comparatively retained, including C51/C27/C16,
and C58 remains 317/317/317/317 across JP/KO/SC/TW.

SC/TW is a same-engine structural localization reference, not a Korean translation
oracle.

### 7.5 Selected Korean design

Design:

`KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1`

Core rule:

`preserve dynamic meaning / flatten inherited Japanese dynamic grammar`

Classification buckets for the next analysis:

```text
GRAMMAR_FLATTEN
DYNAMIC_MEANING_RETAIN
MIXED_SPLIT_REQUIRED
UNRESOLVED
```

A Korean grammatical unit has one owner. Japanese inflection/register generator calls
are candidates to be absorbed into natural Korean caller/full-sentence text. Dynamic
names, address forms, pronouns, numeric/context values and other semantic inserts remain
dynamic where required.

Full-sentence flattening does not mean making every sentence static.

### 7.6 Prohibited C repair paths

Remain rejected:

- local screenshot-by-screenshot correction;
- global `하하 -> 하`;
- global `이이 -> 이`;
- repeated-syllable/longest-overlap dedup;
- direct suffix deletion;
- forced C8:87 result;
- global `0x6A` inversion;
- universal first-syllable stripping from C73/C188;
- globally blanking grammar formatter families before every caller is migrated;
- retaining Japanese segmentation merely because PC Korean retained it;
- requiring recovery of the unavailable exact PC target EXE before design can proceed.

### 7.7 Exact next closure question

Next scope:

`DIALOGUE_FORMATTER_GRAMMAR_GENERATOR_FAMILY_CENSUS_AND_CLASSIFICATION_READ_ONLY`

That analysis must enumerate the externally used block-0 families, classify every
relevant family/caller obligation into the four design buckets, distinguish style-only
from semantic-bearing branches, and produce explicit residual/exception accounting.

No TAI5MSG rewrite, builder change, translation mutation, runtime patch, diagnostic
build, IPS generation, or new WRITE_SAFE authority is authorized.

Issue C remains the top priority until the full grammar-generator family census and
classification is closed.

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

`KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1` is canonically materialized as the current
Korean dialogue grammar design direction.

Current priority next scope is:

**`DIALOGUE_FORMATTER_GRAMMAR_GENERATOR_FAMILY_CENSUS_AND_CLASSIFICATION_READ_ONLY`**

A fresh explicit user execution signal is required before beginning that analysis.

No C implementation/write/build is authorized by this design materialization.
