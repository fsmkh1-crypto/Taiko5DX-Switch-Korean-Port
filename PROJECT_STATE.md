# PROJECT_STATE

Last updated: 2026-09-16 (KST)

This file is the sole project-resume authority.

The previous canonical state remains an immutable inherited base:

```text
commit  b1d6a1369a1733cd34b0314beeb4cfadd2ec2ecd
path    PROJECT_STATE.md
blob    a73a2546520cee07d9a5be1fbf0eea1a0c650c08
```

All facts, closed validations, rejected hypotheses, required provenance, FZ001 state,
write-safety boundaries, issue-A hold, runtime-byte queue, and remaining project queues
in that snapshot are inherited without revalidation unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"KO_GRAMMAR_ROOT_STYLE_ONLY_253_TONE_POLICY_V284_MATERIALIZED_NEXT_REGISTER_NORMALIZE_125","scope_kind":"READ_ONLY","status":"KO_GRAMMAR_TONE_POLICY_V284_MATERIALIZED_NEXT_READ_ONLY","last_closed_validation_id":"V284","last_closed_stage_commit":"b1d6a1369a1733cd34b0314beeb4cfadd2ec2ecd","canonical_base_commit":"b1d6a1369a1733cd34b0314beeb4cfadd2ec2ecd","canonical_base_project_state_blob":"a73a2546520cee07d9a5be1fbf0eea1a0c650c08","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_allowed":["PASS","NOT_APPLICABLE"],"dialogue_formatter_ko_design":"docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","dialogue_formatter_ko_review_validation":"V284","priority_next_scope":"KO_GRAMMAR_REGISTER_NORMALIZE_CANDIDATE_125_BRANCH_WORDING_READ_ONLY","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","docs/VALIDATION_LEDGER_KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.txt","docs/WRITE_TRANSPORT_INCIDENT_20260916_1.txt","docs/GITHUB_AND_CI_POLICY.md","docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md"]}
PROJECT_RESUME_V2 -->

## 1. Inherited state

Inherit the full canonical project state from `PROJECT_STATE.md@b1d6a136...` without
revalidation. In particular:

- V272-V283 Korean grammar-flattening analysis remains valid;
- exact PC v1.02 target EXE remains unavailable and must not be re-searched merely for
  this design;
- `PC_PATCH_ORACLE_GATE=PASS` remains valid for the localization-data/design question;
- FZ001 remains frozen;
- existing explicit WRITE_SAFE authority remains exactly F1 158 + Mapping 4 = 162;
- V284 adds no gameplay-data mutation, builder, build, IPS, runtime-patch, or WRITE_SAFE
  authority.

## 2. V284 — ROOT_STYLE_ONLY 253 tone policy

The least structurally noisy root-style population is exactly:

```text
ROOT_STYLE_ONLY callers                 253
grammar edges                           406
callers carrying dynamic values          91
dynamic-semantic edges                  226
```

Of the 253 callers, 250 have a simple two-arm `0x6A` structure. Among those 250,
210 callers already contain one branch arm with zero grammar calls while the opposite
arm still carries inherited grammar calls. The grammar-bearing opposite arms contain
290 grammar edges.

This is direct PC Korean corpus evidence that branch-local complete Korean wording is
already used at scale inside the same caller structures; full-sentence flattening is
not justified solely by SC/TW analogy.

For all 253 compared callers:

```text
SC grammar residual                         0
TW grammar residual                         0
SC dynamic-call sequence mismatch           0
TW dynamic-call sequence mismatch           0
```

Do not assign a global semantic label such as formal/informal, male/female, polite/plain
to `0x6A=0` or `0x6A=1`. The caller's existing branch wording is the local tone authority.

### 2.1 Family responsibility classes

All 34 grammar entry families used by this 253-caller tranche are classified; unresolved
family count is zero.

```text
REGISTER_NORMALIZE_CANDIDATE
  families: C73 C82 C100 C109 C118 C195 C202 C209 C244 C272 C279 C286 C300 C328 C335
  241 grammar edges / 174 callers

LEXICAL_MOOD_REWRITE_REQUIRED
  families: C125 C132 C146 C160 C174 C181 C188 C216 C223 C230 C237 C251 C265
  109 grammar edges / 92 callers

ZERO_OUTPUT_STRUCTURAL_EXCEPTION
  families: C91 C342
  42 grammar edges / 37 callers

HONORIFIC_ROLE_TONE_CRITICAL
  families: C167 C258 C349 C356
  14 grammar edges / 9 callers
```

Caller sets overlap across family classes. For execution-order planning, assigning each
caller to its highest-risk class yields exactly:

```text
pure REGISTER_NORMALIZE_CANDIDATE      125 callers
LEXICAL_MOOD_REWRITE_REQUIRED           86 callers
ZERO_OUTPUT_STRUCTURAL_EXCEPTION        33 callers
HONORIFIC_ROLE_TONE_CRITICAL             9 callers
TOTAL                                   253 callers
```

### 2.2 V1 tone policy

Current Korean V1 tone policy is:

1. preserve caller-owned `0x6A` and all caller control branches;
2. preserve dynamic-semantic call IDs/order;
3. normalize formatter-only simple register variation into natural branch-local Korean;
4. do not mechanically rewrite request, intention, proposal, or lexical-mood families;
5. isolate C91/C342 empty/non-empty output behavior as a structural exception family;
6. preserve/review honorific-role distinctions such as `-시-`, `말씀-`, `드리-` as
   `TONE_CRITICAL_EXCEPTION` obligations;
7. use JP meaning + actual PC Korean wording + caller branch context as Korean wording
   authority; SC/TW remains structural evidence only.

V284 does not authorize Korean text mutation. It only establishes the policy used for
subsequent READ_ONLY branch-local wording design.

## 3. Prohibited/superseded interpretations

Remain rejected or superseded:

- global repeated-syllable cleanup, `이이 -> 이`, `하하 -> 하`;
- fixed prefix/suffix trimming or first-syllable deletion;
- forced C8:87 or global `0x6A` inversion;
- globally blanking C65..C358 before every caller obligation is accounted;
- treating the former 913, 567, 460, or 253 populations as one automatic migration set;
- treating `0x6A=0/1` as globally named Korean tone classes;
- treating SC/TW wording as Korean tone authority;
- reimplementing the complete Japanese relationship/register formatter merely to retain
  every nested PC formatter variant;
- reopening the unavailable exact PC target EXE search for this design.

## 4. Exact next READ_ONLY scope

Current priority next scope:

`KO_GRAMMAR_REGISTER_NORMALIZE_CANDIDATE_125_BRANCH_WORDING_READ_ONLY`

Purpose: inspect only the 125 callers whose highest-risk class is
`REGISTER_NORMALIZE_CANDIDATE`, bind each grammar edge to its caller branch, preserve
all dynamic-semantic obligations, and design/validate branch-local Korean wording
responsibility without mutating TAI5MSG.

This next scope may not change Korean text in the repository, modify TAI5MSG/builder,
generate IPS, create a diagnostic build, patch runtime code, or add WRITE_SAFE.

## 5. Write-transport incident and recovery

During the attempted V284 materialization, a prohibited GitHub Contents API
`create_file` call created commit
`68ac474558f69ba3eca357d8a8f8bb8c95c2d748` from parent `b1d6a136...` and added only
root file `__DO_NOT_USE__` containing `x`. No legitimate project file was modified by
that accidental commit.

Recovery is forward-only. Preserve the accidental commit in history, remove the root
file from the next tree, materialize V284, and advance `main` only through the allowed
Git-object route.

## 6. Write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

`create_file`, `update_file`, `delete_file`, `create_branch`, force push, and alternate
write routes are prohibited.

A fresh explicit user execution signal is required before the next READ_ONLY scope.