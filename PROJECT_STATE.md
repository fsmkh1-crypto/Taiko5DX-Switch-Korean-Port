# PROJECT_STATE

Last updated: 2026-09-16 (KST)

This file is the sole project-resume authority.

The previous canonical state remains an immutable inherited base:

```text
commit  dfe3b4acaeecba9c28e33db3ad6112752a26defa
path    PROJECT_STATE.md
blob    eb2bfe53926b652c502537099cffdd4f58c9a2c8
```

All facts, closed validations, rejected hypotheses, provenance, FZ001 state, existing
WRITE_SAFE authority, Issue-A hold, runtime-byte queue, and unrelated project queues in
that snapshot are inherited without revalidation unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"KO_GRAMMAR_REGISTER_NORMALIZE_V285_V287_MATERIALIZED_NEXT_STATIC_WRITE_AUTHORIZATION_125","scope_kind":"READ_ONLY","status":"KO_GRAMMAR_REGISTER_NORMALIZE_125_DESIGN_MATERIALIZED_NEXT_WRITE_AUTH_READ_ONLY","last_closed_validation_id":"V287","last_closed_stage_commit":"e75233b9f7d2426a51d8be011c63f96a385eeb4a","canonical_base_commit":"dfe3b4acaeecba9c28e33db3ad6112752a26defa","canonical_base_project_state_blob":"eb2bfe53926b652c502537099cffdd4f58c9a2c8","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","schema_freeze_declaration":"data/pilot/f1_v1_candidate/schema_freeze_declaration.json","schema_freeze_declaration_git_blob_sha":"6c726b7d004753e2f49f63640bd4f6df343dd736","schema_freeze_basis_validation_id":"V107","schema_freeze_basis_ci_run_id":34691523117,"schema_freeze_basis_head":"ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_allowed":["PASS","NOT_APPLICABLE"],"pc_patch_oracle_gate_status":"PASS","dialogue_formatter_ko_design":"docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","dialogue_formatter_ko_review_validation":"V287","priority_next_scope":"KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_READ_ONLY","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","docs/VALIDATION_LEDGER_KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.txt","selective_ko/TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION.md","builder/tai5msg.py","docs/GITHUB_AND_CI_POLICY.md","docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md"]}
PROJECT_RESUME_V2 -->

## 1. Inherited state

Inherit `PROJECT_STATE.md@dfe3b4ac...` in full. In particular:

- V272-V284 remain valid and are not reopened;
- `PC_PATCH_ORACLE_GATE=PASS` remains sufficient for this localization-data family;
- the exact PC v1.02 target EXE remains unavailable and is not a blocker for this data design;
- FZ001 remains frozen;
- existing explicit WRITE_SAFE authority remains exactly F1 158 + Mapping 4 = 162;
- V285-V287 add no gameplay mutation, builder implementation, build, IPS, runtime patch,
  or new WRITE_SAFE authority.

The V284 next-scope pointer is superseded by the closures below.

## 2. V285 — pure REGISTER_NORMALIZE 125 branch wording closure

The pure register-normalization tranche is closed at caller-responsibility level:

```text
callers                              125
grammar edges                        177
callers with dynamic semantic values 47
dynamic-semantic edges               113
```

Disposition by caller:

```text
CALL_ERASURE_ONLY             99 callers / 138 grammar edges
CALLER_ENDING_MATERIALIZE     17 callers /  26 grammar edges
CALLER_PHRASE_REWRITE          6 callers /   9 grammar edges
BOUNDARY_JOIN_NORMALIZE        3 callers /   4 grammar edges
TOTAL                        125 callers / 177 grammar edges
```

Across all 125 callers, 148 grammar edges are removable without adding grammatical
material at that edge; 29 edges require caller-owned ending/phrase/boundary handling.
The 113 dynamic-semantic edges remain preserved.

Analysis scratch provenance:

```text
KO_GRAMMAR_REGISTER_NORMALIZE_CANDIDATE_125_BRANCH_WORDING_READ_ONLY.csv
rows      125
sha256    f638048e3f178551978dd3422e9c170532cfcfdcdc7190cfa179e36551693756
```

The exact 125-caller compact membership is preserved in the dedicated V-ledger.

## 3. V286 — 23 caller literal wording adjudication

The 17 `CALLER_ENDING_MATERIALIZE` and 6 `CALLER_PHRASE_REWRITE` callers are closed at
Korean wording-design level. These 23 callers contain 35 grammar edges; 26 require new
caller-owned Korean grammatical material while 9 co-resident grammar edges are still
simple erasures.

Wording authority is JP meaning + actual PC Korean wording + the same caller's local
branch tone/context. SC/TW remains structural evidence only. No claim is made that the
chosen wording reconstructs the unavailable exact PC v1.02 runtime formatter branch.

The three `BOUNDARY_JOIN_NORMALIZE` callers from V285 are separately closed by boundary
normalization after grammar removal and are not part of the 23.

Detailed wording targets are preserved in the dedicated V-ledger. Wording-design
UNRESOLVED count for the pure 125 tranche is zero.

## 4. V287 — 125 materialization/write-safety design closure

A virtual reconstruction of all 125 caller transforms was composed with the existing
Switch-native compact-byte preservation transform against canonical PC Korean v1.02
TAI5MSG input SHA-256
`e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090`.

Closed structural result:

```text
grammar callers changed                125
grammar calls removed                  177
grammar logical byte delta            -645
compact-only changed messages            33
grammar125 ∩ compact33                    0
combined changed logical messages       158
combined affected physical blocks        17
grown blocks                               0
block count                               33 unchanged
message count                         14,832 unchanged
file size                         2,134,366 unchanged
header block offsets/sizes                identical
compact occurrences                       44
compact protected                          44
compact unprotected                         0
combined used-data delta                 -469
```

Affected blocks are exactly:

`1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,21,24`.

The smallest remaining affected-block padding is 13 bytes in block 9. Therefore no
block relocation or file growth is required for this tranche.

Analysis candidate output SHA-256:

`993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06`

This hash is an analysis candidate, not yet a canonical emitted-build hash.

The preferred realization remains one canonical-input transaction:

`parse once -> apply exact 125 grammar manifest -> apply compact preservation -> rebuild offsets once -> encrypt once`

Do not create a grammar-modified intermediate and feed it back through the current
canonical-input hash guard.

## 5. Current authorization boundary

V285-V287 close wording responsibility and storage/reconstruction design only. They do
not yet grant a new WRITE_SAFE population because the exact per-caller write manifest
with original-message guards and target-message hashes has not been canonicalized.

Current priority next scope is therefore:

`KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_READ_ONLY`

That scope must produce exact row-level original/target message guards, target call
sequence/control fingerprints, deterministic reconstructed output identity, and a
specific authorization boundary before any builder/gameplay-data implementation.

No builder modification, TAI5MSG mutation, build, IPS, or hardware test is authorized by
this state.

## 6. Rejected/superseded interpretations

Remain rejected:

- global repeated-syllable cleanup such as `이이 -> 이` or `하하 -> 하`;
- family-wide fixed suffix/prefix trimming;
- family-wide formatter blanking before caller migration;
- treating all 125 as call-erasure-only;
- treating all 125 as one static tone;
- global `0x6A` tone labeling or inversion;
- using SC/TW wording as Korean wording authority;
- feeding a grammar-modified intermediate file into the current canonical-input
  `reconstruct_tai5msg_switch_native()` path.

## 7. Write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

`create_file`, `update_file`, `delete_file`, `create_branch`, force push, and alternate
write routes remain prohibited.

A fresh explicit user execution signal is required before the next scope.
