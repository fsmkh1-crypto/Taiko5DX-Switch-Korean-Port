# PROJECT_STATE

Last updated: 2026-09-16 (KST)

This file is the sole project-resume authority.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"C_FORMATTER_GRAPH_DIFF_MATERIALIZED_PREDICATE_PARITY_NEXT","scope_kind":"CANONICAL_STATE_OVERLAY","status":"C_GRAPH_DIFF_CLOSED_NEXT_READ_ONLY","last_closed_validation_id":"V270","last_closed_stage_commit":"c49b3410c32ab5428c494a6841dcf7c3c825eb9f","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_allowed":["PASS","NOT_APPLICABLE"],"runtime_byte_route_latest_commit":"39e5999d5bc24173b39521acec459a205ae42540","dialogue_formatter_graph_diff":"docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md","priority_next_scope":"DIALOGUE_FORMATTER_PC_SWITCH_PREDICATE_STATE_PARITY_READ_ONLY","mapping_10036_runtime_validation":"docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","portability_action_population":"docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","runtime_byte_copy_census":"docs/RUNTIME_BYTE_VALIDATION_COPY_CONSUMER_CENSUS.txt","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md","docs/PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION.txt","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md","docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md","docs/RUNTIME_BYTE_VALIDATION_COPY_CONSUMER_CENSUS.txt","docs/RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_PROGRESS_20260915.md","docs/RUNTIME_BYTE_COPY_NORMALIZATION_LOWLEVEL_OWNER_CHECKPOINT_20260915.md","docs/RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_C2_TABLE_CLOSURE_20260915.md","docs/RUNTIME_BYTE_COPY_NORMALIZATION_GENERIC_PARSER_OWNER_CLOSURE_20260915.md","docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","docs/F1_STATIC_WRITE_AUTHORIZATION.md","docs/GITHUB_AND_CI_POLICY.md"]}
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
- issue-C PC original -> PC Korean formatter graph-diff closure materialized on 2026-09-16.

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

The issue-C graph-diff closure adds no WRITE_SAFE, implementation authorization,
build authorization, or new validation ID.

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
  port/runtime/composition/normalization/rendering evidence rather than rewriting
  Korean source text.
- Korean names, place names, readings, glyph codes and translations available from the
  PC patch are never guessed.

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

Do not reopen Mapping because of unrelated renderer/font symptoms.

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

After issue C is closed, resume this family by:

- classifying the nine `0x157C30` caller contexts by canonical source/storage owner;
- materializing exact route membership/cardinality for all 2,057 risk rows;
- binding remaining Stage2 block families;
- reusing existing F1/forward/gap provenance for the 64 non-Stage2 rows;
- identifying a safe Korean compact-data/context discriminant before any parser patch design.

No implementation or diagnostic build is authorized yet.

## 7. Dialogue malformed-ending issue C — GRAPH DIFF CLOSED / PREDICATE PARITY NEXT

Status: `GRAPH_DIFF_CLOSED_NEXT_READ_ONLY`.

Representative real-device symptoms:

- `야규님입니다인가`
- `조금 과음한 모양이오군`
- normal and malformed lines can coexist within one event.

### 7.1 PC_PATCH_ORACLE_GATE

`PASS`.

Canonical materialized evidence:

`docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md`

Exact PC source identities used by that closure:

```text
PC original TAI5MSG_JP.DAT
  size    1,810,889
  sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f

PC Korean v1.02 TAI5MSG_JP.DAT
  size    2,134,366
  sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
```

The PC runtime descriptor/helper census still contains no separate dialogue-formatter
VM hook. The semantic obligation remains TAI5MSG formatter data plus the game's
existing VM/state behavior.

### 7.2 Materialized graph-diff closure

The comparison population is:

```text
blocks                 33 / 33
messages           14,832 / 14,832
block-0 messages      471 / 471
```

Across all 471 block-0 messages:

```text
condition / predicate expressions     PRESERVED
lower-message call IDs / graph edges  PRESERVED
branch/default topology               PRESERVED
empty-output topology                 PRESERVED
literal/output fragments              CHANGED where translated
```

Observed content-level block-0 changes:

```text
changed messages   366
identical messages 105
TOTAL              471
```

The closure analysis observed 14,590 graph/control events with corresponding
event sequence/value structure preserved between PC original and PC Korean v1.02.

Therefore the PC Korean patch does **not** redesign the formatter graph for this
family. It retains the original control graph and supplies Korean output fragments.

### 7.3 Confirmed C facts

- Not a font/glyph cause.
- Not a Mapping 10,036 cause.
- Do not repair individual translated sentences.
- The current Switch TAI5MSG reconstruction does not intentionally redesign block-0
  formatter semantics.
- Problematic dialogue can be `body -> common formatter call -> following suffix`.
- Switch contains native condition/state families referenced by the formatter; absence
  of the basic fields is not established as the cause.
- No separate PC runtime formatter hook has been found in the canonical descriptor/helper census.
- Missing PC-Korean formatter graph transformation is not the cause because no such
  transformation exists in the canonical PC graph comparison.

### 7.4 Rejected/superseded C hypotheses

- `0x01 prefix unsupported` as a proven cause — REJECTED.
- local sentence-by-sentence translation correction — REJECTED.
- global runtime-state normalization — REJECTED.
- font/mapping as primary cause — REJECTED.
- Stage1 `storage_mutability=CODE` count as formatter-code-patch count — REJECTED.
- PC Korean formatter graph redesign missing on Switch — REJECTED.

### 7.5 Exact next closure question

Next scope:

`DIALOGUE_FORMATTER_PC_SWITCH_PREDICATE_STATE_PARITY_READ_ONLY`

The next analysis must bind representative malformed composition paths to their exact
block-0 condition/state references, then compare PC and Switch for:

1. predicate expression semantics;
2. state/reference semantic ownership;
3. producer and value domain;
4. evaluation timing / call context;
5. native Switch counterpart behavior.

No field inversion, forced runtime value, global normalization, code patch, diagnostic
build, or translation change is authorized.

C remains the top priority. Predicate/state parity must be closed before C
implementation design, CWTDAT implementation work, or unrelated realization work resumes.

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

The graph-diff scope is canonically materialized and closed.

Current priority next scope is:

**`DIALOGUE_FORMATTER_PC_SWITCH_PREDICATE_STATE_PARITY_READ_ONLY`**

A fresh explicit user execution signal is required before beginning that analysis.

No C implementation/write/build is authorized by the graph-diff closure.
