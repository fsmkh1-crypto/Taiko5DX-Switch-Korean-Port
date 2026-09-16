# PROJECT_STATE

Last updated: 2026-09-17 (KST)

This file is the sole project-resume authority.

The previous canonical state remains an immutable inherited base:

```text
commit  29002c496bc3e11c7e7fac0d72af100d55d46098
path    PROJECT_STATE.md
blob    6258f9727cf9bc5b45668b7e65e8d62a042266b4
```

All facts, closed validations, rejected hypotheses, provenance, FZ001 state, unrelated
project queues, and WRITE_SAFE authority in that snapshot are inherited without
revalidation unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"KO_GRAMMAR_REGISTER_NORMALIZE_125_V289_IMPLEMENTED_NEXT_BUILD_VALIDATION","scope_kind":"IMPLEMENTATION_NO_BUILD","status":"KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILDER_IMPLEMENTED_V289_CLOSED","last_closed_validation_id":"V289","last_closed_stage_commit":"13a7fae6ce2737a7bd3e5f22d1e306a906168673","canonical_base_commit":"29002c496bc3e11c7e7fac0d72af100d55d46098","canonical_base_project_state_blob":"6258f9727cf9bc5b45668b7e65e8d62a042266b4","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_status":"PASS","explicit_write_safe_total":287,"grammar125_write_safe_rows":125,"grammar125_implemented":true,"grammar125_manifest_index":"selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json","grammar125_manifest_set_sha256":"a17b5b493a4f529e6aa308954242434e13bede0dda14b075cc13a3a890bc254c","grammar125_authorized_output_sha256":"993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06","grammar125_builder_blob":"a1400db06828174fb6193eccb447bc16d7c2749e","priority_next_scope":"KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILD_VALIDATION","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_V288.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILDER_IMPLEMENTATION_V289.md","selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json","builder/tai5msg.py","docs/GITHUB_AND_CI_POLICY.md","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md"]}
PROJECT_RESUME_V2 -->

## 1. Inherited state

Inherit `PROJECT_STATE.md@29002c49...` in full. In particular:

- V272-V288 remain valid and are not reopened;
- FZ001 remains frozen;
- `PC_PATCH_ORACLE_GATE=PASS`;
- V288 grants exactly 125 grammar125 WRITE_SAFE rows;
- explicit WRITE_SAFE remains F1 158 + Mapping 4 + grammar125 125 = 287;
- the canonical V288 manifest and wording authority are unchanged;
- unrelated F1, Mapping, CWTDAT, name/yomi, formatter/runtime, and other queues are unchanged.

## 2. V289 — grammar125 builder implementation closure

Canonical implementation commit:

```text
commit = 13a7fae6ce2737a7bd3e5f22d1e306a906168673
tree   = fa0a80a6c9efd59e08820c47ded60efeae606c58
doc    = docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILDER_IMPLEMENTATION_V289.md
```

Implemented builder identity:

```text
path        = builder/tai5msg.py
Git blob    = a1400db06828174fb6193eccb447bc16d7c2749e
UTF-8 bytes = 15,336
SHA-256     = 7398b48626dc641fc995ee1c7e1215d37d0bfb901d6496056a36324ada1f7a62
```

The builder now consumes the V288 manifest directly in one canonical-input transaction:

```text
canonical input guard
-> parse once
-> verify V288 INDEX + ordered shards
-> verify/apply exact 125 source-coordinate edits
-> verify exact 125 targets
-> apply existing compact33 preservation
-> rebuild affected blocks once at fixed physical sizes
-> reparse and verify V288 accounting
-> enforce output SHA-256 993d3fc2...
```

The old two-pass grammar-intermediate route remains forbidden and is not implemented.

## 3. Implementation validation performed in V289

V289 performed function-level validation only; it did not execute `builder/build.py`.

```text
python syntax compilation          PASS
canonical TAI5MSG function replay  PASS
second deterministic replay        byte-identical PASS
output SHA-256                     993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06
input/output size                  2,134,366 / 2,134,366
blocks/messages                    33 / 14,832
changed messages                   158
affected blocks                    17
grown blocks                       0
compact occurrences                44
input one-byte mutation            correctly rejected
manifest shard byte mutation       correctly rejected
```

These checks validate the implementation path against the V288 deterministic identity.
They are not a build, IPS generation, or hardware test.

## 4. Current authorization boundary

V289 implemented only the already-authorized grammar125 TAI5MSG path.

V289 did not:

- add or remove WRITE_SAFE rows;
- modify the V288 manifest or wording targets;
- emit gameplay output into the repository;
- run a diagnostic/release build;
- generate IPS output;
- perform hardware/runtime validation;
- alter unrelated project queues.

No build has yet validated `builder/build.py` end-to-end with this implementation.

## 5. Next scope

Under a fresh explicit user execution signal, the next eligible single scope is:

`KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILD_VALIDATION`

That scope may perform one build whose newly introduced cause-family delta is V289
`grammar125`, verify the emitted `TAI5MSG_JP.DAT` SHA/size and build report against V288,
and record build-level closure. It must not mix unrelated new hypotheses or fixes into
that build.

Hardware validation remains a separate later scope.

## 6. Repository write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

`create_file`, `update_file`, `delete_file`, `create_branch`, force push, and alternate
write routes remain prohibited.

A fresh explicit user execution signal is required before the next scope.
