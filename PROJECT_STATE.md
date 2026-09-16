# PROJECT_STATE

Last updated: 2026-09-17 (KST)

This file is the sole project-resume authority.

The previous canonical state remains an immutable inherited base:

```text
commit  f556429814f72565bcb0a6cb5485f8ebed934951
path    PROJECT_STATE.md
blob    0e530a12def42f8f6fe3415256017573d23f2a3a
```

All facts, closed validations, rejected hypotheses, provenance, FZ001 state, unrelated
project queues, and WRITE_SAFE authority in that snapshot are inherited without
revalidation unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"KO_GRAMMAR_REGISTER_NORMALIZE_125_V290_BUILD_VALIDATED_NEXT_HARDWARE_PACKAGE","scope_kind":"BUILD_VALIDATION","status":"KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILD_VALIDATED_V290_CLOSED","last_closed_validation_id":"V290","last_closed_stage_commit":"619fdb25a9fc6c4086865d083e24180f37cf9a67","canonical_base_commit":"f556429814f72565bcb0a6cb5485f8ebed934951","canonical_base_project_state_blob":"0e530a12def42f8f6fe3415256017573d23f2a3a","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_status":"PASS","explicit_write_safe_total":287,"grammar125_write_safe_rows":125,"grammar125_implemented":true,"grammar125_build_validated":true,"grammar125_manifest_index":"selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json","grammar125_manifest_set_sha256":"a17b5b493a4f529e6aa308954242434e13bede0dda14b075cc13a3a890bc254c","grammar125_authorized_output_sha256":"993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06","grammar125_builder_blob":"a1400db06828174fb6193eccb447bc16d7c2749e","priority_next_scope":"KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_VALIDATION_PACKAGE","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_V288.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILDER_IMPLEMENTATION_V289.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILD_VALIDATION_V290.md","selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json","builder/tai5msg.py","builder/build.py","docs/GITHUB_AND_CI_POLICY.md","docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md","docs/PC_RUNTIME_DLL_SPEC.md"]}
PROJECT_RESUME_V2 -->

## 1. Inherited state

Inherit `PROJECT_STATE.md@f5564298...` in full. In particular:

- V272-V289 remain valid and are not reopened;
- FZ001 remains frozen;
- `PC_PATCH_ORACLE_GATE=PASS`;
- V288 grants exactly 125 grammar125 WRITE_SAFE rows;
- explicit WRITE_SAFE remains F1 158 + Mapping 4 + grammar125 125 = 287;
- V289 grammar125 builder implementation remains canonical;
- unrelated F1, Mapping, CWTDAT, name/yomi, pointer, formatter/runtime, and other queues
  remain unchanged.

## 2. V290 — grammar125 integrated build validation

V290 executed the exact V289 canonical builder sources against the actual Switch v1.1.3
reference files and the exact PC Korean v1.02 patcher EXE.

V290 materialization commit:

```text
commit = 619fdb25a9fc6c4086865d083e24180f37cf9a67
tree   = dbc52295355a577e34d6b2d4bd711d6c4f8f2369
doc    = docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILD_VALIDATION_V290.md
```

Authoritative emitted TAI5MSG result:

```text
bytes   = 2,134,366
sha256  = 993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06
blocks  = 33
messages= 14,832
changed messages = 158
affected blocks = 17
grown blocks = 0
compact occurrences = 44
```

This exactly reproduces the V288 authorized whole-file identity through `builder/build.py`.

Additional emitted identities:

```text
FONT_JPN.G1T sha256 = c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
IPS sha256          = ea6bd258e459e913356be68a177efdb48e33eb103cb0c10e378d88133b57408d
BUILD_REPORT sha256 = f826622c02c8941551a3c268364ab08e98d31a5c9028b98c5814269a28adf13f
```

## 3. Current authorization boundary

Grammar125 is now closed through static-write authorization, builder implementation, and
integrated build validation.

V290 does not constitute hardware/runtime validation and adds no new WRITE_SAFE rows.

The emitted build is a scratch validation output and is not committed to GitHub. Large
hardware-test packages belong in the project Google Drive.

## 4. Next scope

Under a fresh explicit user execution signal, the next eligible single scope is:

`KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_VALIDATION_PACKAGE`

That scope may package the already validated V290 output and upload the large test package
to the project Drive with an exact package SHA-256. It must not mix new fixes or other
cause families into the package.

Hardware execution/test remains a separate subsequent scope.

## 5. Repository write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

`create_file`, `update_file`, `delete_file`, `create_branch`, force push, and alternate
write routes remain prohibited.

A fresh explicit user execution signal is required before the next scope.
