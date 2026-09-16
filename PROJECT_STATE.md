# PROJECT_STATE

Last updated: 2026-09-16 (KST)

This file is the sole project-resume authority.

The previous full-state snapshot remains an immutable inherited base:

```text
commit  9e542568849b4644c094395fc1e4698ac47b08af
path    PROJECT_STATE.md
blob    2a870e114c28abe5951fce49db10b337ae6b3ef3
```

All facts, closed validations, rejected hypotheses, required provenance, FZ001 state,
write-safety boundaries, and remaining non-dialogue project queues in that snapshot are
inherited without revalidation unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"KO_GRAMMAR_TONE_OBLIGATION_V283_MATERIALIZED_NEXT_ROOT_STYLE_ONLY_253_TONE_POLICY","scope_kind":"READ_ONLY","status":"KO_GRAMMAR_567_AND_460_TONE_REVIEW_MATERIALIZED_NEXT_READ_ONLY","last_closed_validation_id":"V283","last_closed_stage_commit":"9e542568849b4644c094395fc1e4698ac47b08af","canonical_base_commit":"9e542568849b4644c094395fc1e4698ac47b08af","canonical_base_project_state_blob":"2a870e114c28abe5951fce49db10b337ae6b3ef3","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","schema_freeze_declaration":"data/pilot/f1_v1_candidate/schema_freeze_declaration.json","schema_freeze_declaration_git_blob_sha":"6c726b7d004753e2f49f63640bd4f6df343dd736","schema_freeze_basis_validation_id":"V107","schema_freeze_basis_ci_run_id":34691523117,"schema_freeze_basis_head":"ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_allowed":["PASS","NOT_APPLICABLE"],"dialogue_formatter_ko_design":"docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","dialogue_formatter_ko_review_validation":"V283","priority_next_scope":"KO_GRAMMAR_ROOT_STYLE_ONLY_253_TONE_POLICY_READ_ONLY","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","docs/VALIDATION_LEDGER_KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.txt","docs/GITHUB_AND_CI_POLICY.md","docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md"]}
PROJECT_RESUME_V2 -->

## 1. Inherited project state

The canonical base snapshot at commit `9e542568...` remains valid in full except for the
issue-C next-scope pointer and the narrower tone-preservation interpretation superseded
by V282-V283 below.

In particular, inherit without revalidation:

- Stage1, Stage2, F1, FZ001;
- forward-986 and Oracle/Assisted/Astra/TRACE closure;
- pointer-56 closure and its still-open realization items;
- Mapping 10,036 through V260 and the exact four existing WRITE_SAFE actions;
- portability/action planning V261-V264;
- runtime-byte validation/copy V265-V270 and post-V270 route-binding checkpoints;
- dialogue graph-diff closure and PC-patch data provenance;
- V271 document-governance closure;
- Korean grammar-flattening V272-V281;
- CWTDAT issue A hold and all other project queues from the base snapshot.

Existing explicit static WRITE_SAFE authority remains unchanged:

```text
F1                         158
Mapping 10,036               4
TOTAL                       162
```

V282-V283 add no WRITE_SAFE, implementation authorization, gameplay-data mutation,
builder modification, build authorization, IPS authorization, or runtime-patch authority.

## 2. Issue C — canonical design basis through V281

Current design authority remains:

`docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md`

Core design remains:

`preserve dynamic meaning / flatten inherited Japanese dynamic grammar`

Canonical whole-family census remains:

```text
external block-0 entry families          73
GRAMMAR_FLATTEN families                  42 / 2,364 KO calls
DYNAMIC_MEANING_RETAIN families           31 / 4,254 KO calls
unique grammar caller messages         1,013
callers also carrying dynamic values      386
```

The grammar cluster recursively covers `C65..C358`, 294 nodes, with no internal edge
crossing into the retained dynamic-semantic clusters.

The exact PC v1.02 target EXE remains unavailable. Data-level `PC_PATCH_ORACLE_GATE=PASS`
remains sufficient for this design question; exact target PC runtime cursor/return parity
must not be claimed. Do not reopen the abandoned exact-EXE search merely for this design.

## 3. V282 — 567 caller-style-branch detailed matrix

The former `CALLER_STYLE_BRANCH_AVAILABLE` population is exactly:

```text
567 callers / 1,356 grammar edges
```

It is not one homogeneous direct-migration class. Detailed caller topology is:

```text
ROOT_STYLE_ONLY                         253 callers / 406 grammar edges
ROOT_STYLE_PLUS_SECONDARY               207 callers / 657 grammar edges
NESTED_STYLE_BEFORE_ALL_GRAMMAR          64 callers / 166 grammar edges
PRE_STYLE_GRAMMAR_MIXED                  43 callers / 127 grammar edges
TOTAL                                   567 callers / 1,356 grammar edges
```

Dynamic-semantic obligations inside the same 567 callers are:

```text
callers carrying dynamic values         220
dynamic-semantic edges                  749
```

For this 567 population, official SC and TW both remove the inherited grammar edges and
preserve required dynamic-semantic call ID/order in the compared structure:

```text
SC grammar residual                         0
TW grammar residual                         0
SC dynamic-call sequence mismatch           0
TW dynamic-call sequence mismatch           0
```

The 43 `PRE_STYLE_GRAMMAR_MIXED` callers contain grammar work before the first caller
`0x6A` style branch. That pre-style region contains 58 grammar edges spanning 16 grammar
families. Therefore caller-level `0x6A` presence alone cannot authorize flattening.

Most importantly:

`caller 0x6A branch != complete nested formatter register/tone dispatch`

The caller's direct predicate set does not fully reproduce the recursively used
formatter predicate/state dependencies. Therefore the former interpretation that all
567 callers already own every required tone distinction is rejected.

## 4. V283 — root-style-owner 460 tone-obligation matrix

The structurally cleanest root-style population is:

```text
ROOT_STYLE_ONLY                         253 callers / 406 grammar edges
ROOT_STYLE_PLUS_SECONDARY               207 callers / 657 grammar edges
TOTAL                                   460 callers / 1,063 grammar edges
```

Dynamic-semantic obligations in the same population are:

```text
callers carrying dynamic values         183
dynamic-semantic edges                  576
```

Official SC/TW structural reference remains clean for this population:

```text
SC grammar residual                         0
TW grammar residual                         0
SC dynamic-call sequence mismatch           0
TW dynamic-call sequence mismatch           0
```

These 460 callers use 34 grammar entry families. Their formatter graphs carry extensive
non-`0x6A` relationship/register state. Across the 34 used entries:

```text
common non-0x6A relation/register condition atoms    24
union non-0x6A relation/register condition atoms     28
```

Caller-side direct condition overlap with those formatter obligations is:

```text
435 callers   overlap 0
 18 callers   overlap 1
  7 callers   overlap 2
  0 callers   complete formatter-condition coverage
TOTAL 460
```

Therefore the strict disposition is:

```text
BRANCH_LOCAL_TONE_PRESERVABLE              0 / 460
EXPLICIT_TONE_COLLAPSE_REVIEW_REQUIRED    460 / 460
```

This does not reject full-sentence grammar flattening. It rejects only the assumption
that preserving caller `0x6A` plus caller-local secondary branches automatically
preserves all PC Korean nested formatter register variation.

The 460-row scratch matrix used for this closure had:

```text
SHA-256  84eae893bedb55dccb2cfeb7e3328861fed1501e618e868c75208c248f058d48
rows     460
```

It is analysis provenance only and is not WRITE_SAFE or a gameplay-data artifact.

## 5. Current Korean tone policy status

The following remains a design candidate, not an approved mutation policy:

1. preserve caller-owned `0x6A` and all existing caller control/secondary branches;
2. preserve dynamic-semantic call IDs/order;
3. flatten inherited Japanese grammar segmentation into natural branch-local Korean;
4. explicitly adjudicate formatter-only relationship/register variation;
5. allow normalization of formatter-only tone only when semantic/character loss is
   explicitly judged acceptable;
6. isolate meaningful speaker/relationship distinctions as `TONE_CRITICAL_EXCEPTION`.

No caller text may be rewritten merely because it belongs to the 460 population.

## 6. Rejected or superseded interpretations

Remain rejected:

- screenshot-by-screenshot local patching;
- global `이이 -> 이` or `하하 -> 하`;
- repeated-syllable or longest-overlap dedup;
- fixed prefix/suffix trimming;
- forced C8:87 result;
- global `0x6A` inversion;
- global blanking of C73/C188 or C65..C358 before caller obligations are closed;
- copying SC/TW wording or treating SC/TW as Korean tone authority;
- treating the former 913 structurally-direct callers as automatic migration authority;
- treating all 567 caller-style-branch callers as tone-preservable;
- treating the 460 root-style callers as direct text-migration authority;
- requiring recovery of the unavailable exact PC target EXE before design continues.

## 7. Exact next READ_ONLY scope

Current priority next scope is:

**`KO_GRAMMAR_ROOT_STYLE_ONLY_253_TONE_POLICY_READ_ONLY`**

Purpose:

- use the structurally least noisy 253 `ROOT_STYLE_ONLY` callers to determine which
  nested formatter register distinctions are semantically/character-critical in Korean;
- classify branch-local normalization candidates versus `TONE_CRITICAL_EXCEPTION`;
- define a reusable Korean tone policy before extending the decision to the 207
  secondary-condition callers, then the nested 64 and pre-style-mixed 43 populations.

This scope is analysis only. It may not mutate TAI5MSG, alter Korean translations,
modify the builder, generate IPS, create a diagnostic build, patch runtime code, or add
WRITE_SAFE authority.

## 8. Write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

Never use `create_file`, `update_file`, `delete_file`, `create_branch`, force push, or
alternate write routes.

A fresh explicit user execution signal is required before beginning the next READ_ONLY
analysis scope.