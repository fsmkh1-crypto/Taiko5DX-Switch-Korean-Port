# PROJECT_STATE

Last updated: 2026-09-17 (KST)

This file is the sole project-resume authority.

The previous canonical state remains an immutable inherited base:

```text
commit  d78af420d83516adcdae607e3dadf2d7d01c8f6e
path    PROJECT_STATE.md
blob    d9eb6a9f1ae9b2b333374e773096438ec5a563c2
```

All facts, closed validations, rejected hypotheses, provenance, FZ001 state, unrelated project queues, and WRITE_SAFE authority in that snapshot are inherited without revalidation unless explicitly superseded below.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"KO_GRAMMAR_REGISTER_NORMALIZE_125_V291_PACKAGE_READY_NEXT_HARDWARE_EXECUTION","scope_kind":"HARDWARE_VALIDATION_PACKAGE","status":"KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_VALIDATION_PACKAGE_V291_READY","last_closed_validation_id":"V291","canonical_base_commit":"d78af420d83516adcdae607e3dadf2d7d01c8f6e","canonical_base_project_state_blob":"d9eb6a9f1ae9b2b333374e773096438ec5a563c2","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","schema_freeze_declaration_id":"FZ001","pc_patch_oracle_entry_gate":"MANDATORY","pc_patch_oracle_gate_status":"PASS","explicit_write_safe_total":287,"grammar125_write_safe_rows":125,"grammar125_implemented":true,"grammar125_build_validated":true,"grammar125_hardware_package_ready":true,"grammar125_hardware_validated":false,"grammar125_authorized_output_sha256":"993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06","v291_package_sha256":"c5a560a2fe4fdcec3c0ec5b6b2ac90efb2c3e57db211f65c2e6729ec38faba3d","v291_drive_folder_id":"1TZSn4_87QyQQhxf8CJ9beCAY9vQ5qCOq","priority_next_scope":"KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_EXECUTION_VALIDATION","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_V288.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILDER_IMPLEMENTATION_V289.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILD_VALIDATION_V290.md","docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_VALIDATION_PACKAGE_V291.md","selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json","builder/tai5msg.py","builder/build.py","docs/GITHUB_AND_CI_POLICY.md"]}
PROJECT_RESUME_V2 -->

## 1. Inherited state

Inherit `PROJECT_STATE.md@d78af420...` in full. V272-V290 remain closed, FZ001 remains frozen, `PC_PATCH_ORACLE_GATE=PASS`, and explicit WRITE_SAFE remains exactly 287 (F1 158 + Mapping 4 + grammar125 125). Unrelated F1, Mapping, CWTDAT, name/yomi, pointer, formatter/runtime, and other queues remain unchanged.

## 2. V291 — grammar125 hardware validation package

V291 did not rebuild or modify gameplay data. An already existing local package candidate was inspected and its authoritative V290 payload identities were checked directly.

```text
TAI5MSG_JP.DAT sha256 = 993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06
FONT_JPN.G1T sha256   = c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
IPS sha256            = ea6bd258e459e913356be68a177efdb48e33eb103cb0c10e378d88133b57408d
```

All three exactly match V290.

Package identity:

```text
name   = Taiko5DX_KR_V291_GRAMMAR125_HWTEST.zip
bytes  = 382,935,991
sha256 = c5a560a2fe4fdcec3c0ec5b6b2ac90efb2c3e57db211f65c2e6729ec38faba3d
```

Because the direct 383 MB Drive transfer route failed, the exact ZIP was split into eight ordered transport parts and uploaded to:

```text
/Google Drive/GPT/태합입지전/V291_HWTEST_PARTS
folder id = 1TZSn4_87QyQQhxf8CJ9beCAY9vQ5qCOq
```

Concatenating part00 through part07 reproduces the exact package SHA above. `V291_HWTEST_PACKAGE_MANIFEST.json` is stored in the same folder.

Canonical V291 detail document:

`docs/KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_VALIDATION_PACKAGE_V291.md`

## 3. Current boundary

Grammar125 status is now:

```text
V288 static-write authorization  CLOSED
V289 builder implementation      CLOSED
V290 integrated build validation CLOSED
V291 hardware package            READY
hardware execution               NOT YET PERFORMED
```

V291 adds no new WRITE_SAFE rows and does not validate runtime behavior by itself.

## 4. Next scope

Under a fresh explicit user execution signal, the next eligible single scope is:

`KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_EXECUTION_VALIDATION`

Use the V291 package unchanged. Record hardware/runtime observations only for this grammar125 cause family; do not mix new fixes or other cause families into the validation run.

## 5. Repository write boundary

Remote GitHub writes remain restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

A fresh explicit user execution signal is required before the next scope.
