# PROJECT_STATE

Last updated: 2026-09-17 (KST)

This file is the sole project-resume authority.

The previous canonical state remains an immutable inherited base:

```text
commit  dcf52f08a0d52ba3aff604cf4bfc8d14aa4bdfcd
path    PROJECT_STATE.md
blob    0ced346f12ccb7dad72cdafab646d9c1385fb88b
```

All facts, closed validations, rejected hypotheses, provenance, FZ001 state, unrelated
project queues, and prior WRITE_SAFE authority in that snapshot are inherited without
revalidation unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"KO_GRAMMAR_REGISTER_NORMALIZE_125_V288_MATERIALIZED_NEXT_BUILDER_IMPLEMENTATION_NO_BUILD","scope_kind":"MATERIALIZED_AUTHORIZATION","status":"KO_GRAMMAR_REGISTER_NORMALIZE_125_WRITE_SAFE_125_V288_CLOSED","last_closed_validation_id":"V288","last_closed_stage_commit":"b6167d48e9a8b54158865dd68950bb9bc8f083b1","canonical_base_commit":"dcf52f08a0d52ba3aff604cf4bfc8d14aa4bdfcd","canonical_base_project_state_blob":"0ced346f12ccb7dad72cdafab646d9c1385fb88b","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_status":"PASS","dialogue_formatter_ko_review_validation":"V288","explicit_write_safe_total":287,"grammar125_write_safe_rows":125,"grammar125_manifest_index":"selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json","grammar125_manifest_set_sha256":"a17b5b493a4f529e6aa308954242434e13bede0dda14b075cc13a3a890bc254c","grammar125_authorized_output_sha256":"993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06","priority_next_scope":"KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILDER_IMPLEMENTATION_NO_BUILD","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_V288.md","selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json","docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md","docs/VALIDATION_LEDGER_KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.txt","builder/tai5msg.py","docs/GITHUB_AND_CI_POLICY.md","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md"]}
PROJECT_RESUME_V2 -->

## 1. Inherited state

Inherit `PROJECT_STATE.md@dcf52f08...` in full. In particular:

- V272-V287 remain valid and are not reopened;
- FZ001 remains frozen;
- `PC_PATCH_ORACLE_GATE=PASS`;
- the canonical PC Korean v1.02 TAI5MSG input remains
  `2,134,366 bytes / e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090`;
- V285 exact membership/responsibility, V286 wording authority, and V287 one-transaction
  reconstruction design remain the direct predecessors of V288;
- unrelated F1, Mapping, CWTDAT, name/yomi, formatter runtime, and other queues are
  unchanged.

## 2. V288 — grammar125 exact static-write authorization

V288 canonical materialization commit:

```text
commit = b6167d48e9a8b54158865dd68950bb9bc8f083b1
tree   = 1b0de155f6feb2205b2a1e779b8c24077c7f78c5
doc    = docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_V288.md
```

Canonical exact-action artifact:

```text
index = selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json
index logical SHA-256 = 587464c402538b31ffc10c4726e953f5c54b33cfd92f6fd9c14cd37de27c7a00
ordered row shards = 4
rows = 125
manifest-set SHA-256 = a17b5b493a4f529e6aa308954242434e13bede0dda14b075cc13a3a890bc254c
```

The row shards must be consumed in the order and with the hashes declared by `INDEX.json`.
Do not substitute a re-census or re-adjudicated wording set.

V288 closure:

```text
rows                                  125
unique locators                        125
grammar calls removed                  177
target grammar residual                  0
preserved non-register calls           125
non-register sequence mismatches         0
control/branch mismatches                0
grammar logical byte delta            -645
grammar125 ∩ compact33                    0
UNKNOWN                                  0
UNRESOLVED                               0
CONFLICT                                 0
```

Three same-input deterministic replays reproduced:

`993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06`

with 33 blocks, 14,832 messages, unchanged file size/header block pairs, 44/44 compact
occurrences protected, zero unprotected, zero grown blocks, and minimum remaining affected
block padding 13 bytes.

## 3. WRITE_SAFE authority

V288 adds exactly 125 WRITE_SAFE rows.

Current explicit WRITE_SAFE authority is now:

```text
F1 DIRECT_PORT        158
Mapping                 4
grammar125            125
TOTAL                  287
```

This is static-write authorization only. It does not mean the 125 rows have been
implemented or built.

## 4. Failed/rejected variant provenance

Preserve the V288 rejection:

- changing the pre-existing `...` / `......` punctuation in `6:211` and `21:458` as part
  of this grammar family is rejected;
- that variant produced non-erasure delta `-101` instead of `-93` and failed the V287
  deterministic whole-file identity;
- the source punctuation is therefore preserved by the authorized manifest.

All V285-V287 rejected global cleanup/formatter-blanking/SC-TW wording/two-pass
intermediate interpretations remain rejected.

## 5. Current authorization boundary

V288 performed documentation/authorization materialization only.

It did not modify:

- `builder/tai5msg.py`;
- TAI5MSG gameplay payloads;
- IPS/build outputs;
- runtime code;
- hardware-test artifacts.

No build or diagnostic build is authorized by this state.

## 6. Next scope

Under a fresh explicit user execution signal, the next eligible single scope is:

`KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILDER_IMPLEMENTATION_NO_BUILD`

That scope may modify the builder to consume the V288 manifest in the V287-required
single canonical-input transaction:

```text
parse canonical input once
-> verify exact 125 source guards
-> apply exact 125 manifest edits
-> apply existing compact preservation
-> rebuild message offsets once
-> preserve fixed block sizes
-> encrypt once
-> enforce output SHA-256 993d3fc2...
```

It must not build, generate IPS, or perform hardware validation. Those remain separate
future scopes.

## 7. Repository write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

`create_file`, `update_file`, `delete_file`, `create_branch`, force push, and alternate
write routes remain prohibited.

A fresh explicit user execution signal is required before the next scope.
