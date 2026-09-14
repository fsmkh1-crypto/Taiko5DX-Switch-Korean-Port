# PROJECT_STATE

Last updated: 2026-09-14 (KST)

This file is the sole project-resume authority.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION_MATERIALIZED","scope_kind":"REPOSITORY_WRITE","status":"STOPPED_AWAITING_USER_SIGNAL","last_closed_validation_id":"V260","last_closed_stage_commit":"559fc548afda7034568e81ec1d6af0f69ab2a2c2","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","mapping_10036_helper_v2_authorization":"docs/MAPPING_10036_HELPER_TEXT_V2_STATIC_WRITE_SAFETY_AUTHORIZATION.txt","mapping_10036_helper_v2_manifest":"data/post_freeze/mapping_10036_helper_text_v2_static_write_safety_authorization_v1/MANIFEST.json","mapping_10036_diagnostic_build":"docs/MAPPING_10036_DELIVERY_CONTROLLED_DIAGNOSTIC_BUILD.txt","mapping_10036_diagnostic_manifest":"data/post_freeze/mapping_10036_delivery_controlled_diagnostic_build_v1/MANIFEST.json","mapping_10036_runtime_validation":"docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","mapping_10036_runtime_manifest":"data/post_freeze/mapping_10036_runtime_forward_reverse_hardware_validation_v1/MANIFEST.json","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md","docs/MAPPING_10036_SWITCH_COUNTERPART_SURVEY.txt","docs/MAPPING_10036_REALIZATION_DESIGN.txt","docs/MAPPING_10036_ALIGNMENT_PADDING_RUNTIME_VALIDITY.txt","docs/MAPPING_10036_HELPER_HOOK_CONTRACT.txt","docs/MAPPING_10036_STATIC_WRITE_SAFETY_AUTHORIZATION.txt","docs/MAPPING_10036_HELPER_TEXT_V2_STATIC_WRITE_SAFETY_AUTHORIZATION.txt","data/post_freeze/mapping_10036_helper_text_v2_static_write_safety_authorization_v1/MANIFEST.json","docs/MAPPING_10036_DELIVERY_CONTROLLED_DIAGNOSTIC_BUILD.txt","data/post_freeze/mapping_10036_delivery_controlled_diagnostic_build_v1/MANIFEST.json","docs/MAPPING_10036_RUNTIME_FORWARD_REVERSE_HARDWARE_VALIDATION.txt","data/post_freeze/mapping_10036_runtime_forward_reverse_hardware_validation_v1/MANIFEST.json","docs/GITHUB_AND_CI_POLICY.md","docs/F1_STATIC_WRITE_AUTHORIZATION.md"]}
PROJECT_RESUME_V2 -->

## Current canonical state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Inherited without revalidation: Stage1, Stage2, F1, FZ001, forward-986, Oracle/Assisted/Astra/TRACE closure, full-corpus coverage/semantic-owner/action-collapse overlays, pointer-56 closure, and Mapping 10,036 survey/design/storage/helper-hook/static-write closure.

Canonical inline source accounting remains 17,103: Stage2 13,771 + F1 1,311 + forward 986 + gap 1,035.

Existing F1 static WRITE_SAFE authority remains 158. Effective Mapping 10,036 WRITE_SAFE authority remains four. Explicit independently authorized static actions remain 162; this is not final full-port Action Ledger cardinality.

## Mapping 10,036 helper V2 — V246–V251

Historical `MAP10036_HELPER_TEXT_V1` remains preserved as VERIFIED evidence but is not the implementation target because its exact payload was not materialized with recoverable source/generator provenance.

Effective helper action:

```text
MAP10036_HELPER_TEXT_V2    WRITE_SAFE / DIAGNOSTIC_IMPLEMENTED / EDEN_RUNTIME_VALIDATED
```

V2 retains the validated 308-byte TEXT_ALIGNMENT_RX interval, structural-zero preimage guard, entry/re-entry contract and ABI constraints. Exact payload SHA-256 is `f472326cab461ac8258282d5795031c33bcc52c9d2f1cd821b8eb6c94352f493` and deterministic source/linker/toolchain provenance is materialized.

Helper coordinate provenance is closed: `0x58CE60` equals decimal `5820000`. Builder source, embedded diagnostic build-info and emitted IPS agree on that coordinate. Earlier handoff decimal `5811808` is an arithmetic transcription error and must not be reused.

The other three Mapping actions remain unchanged:

```text
MAP10036_FWD_MISS_HOOK_V1
MAP10036_REV_MISS_HOOK_V1
MAP10036_DELTA_RODATA_V1
```

## Mapping 10,036 diagnostic delivery — V252–V257

Builder source commit: `27d851713c5ee21f6b34a67c503b9195b15cf712`.

Effective diagnostic action set is exactly four:

```text
MAP10036_FWD_MISS_HOOK_V1
MAP10036_REV_MISS_HOOK_V1
MAP10036_HELPER_TEXT_V2
MAP10036_DELTA_RODATA_V1
```

Delivery validation remains:
- exact input identity: PASS;
- Build ID: PASS;
- preimage guards: 4/4 PASS;
- intended actions = 4; emitted actions = 4; extra = 0;
- mapped-to-IPS shift = +0x100;
- IPS self-reparse = PASS;
- independent reserialization = PASS;
- RLE records = 0;
- IPS SHA-256 = `6ff4b07db9b83b22197009206e21b5023ad02e62458e8597bac219a3c0faa120`;
- package SHA-256 = `e4810b8186bab484fc076419c1a882b7deb9031b09560d47a8eace00b5f49cca`.

Diagnostic package:
`Google Drive / 태합입지전 프로젝트 / Eden_Builds / MAPPING10036_Taiko5DX_KR_EDEN.zip`
Drive file ID: `1HYtLZOmONs82AXeD_NQAF4jKP-_37rej`.

No font, yomi, pointer, descriptor, translation or unrelated runtime action is present in this diagnostic artifact.

## Mapping 10,036 Eden runtime closure — V258–V260

Runtime environment: Eden Android v0.2.1.

Test route: new-officer surname software keyboard. The test value `가사힝` was entered and committed. The game-field display then showed non-Korean/garbled glyphs, which is outside Mapping adjudication because the Mapping-only diagnostic intentionally contains no Korean font/render family. The same surname input field was reopened and the software keyboard initial text was exactly `가사힝`; the user explicitly confirmed the second retained screenshot is the post-commit reopen.

Tested route verdict:

```text
forward mapping      PASS
reverse mapping      PASS
runtime round-trip   PASS
renderer/font        NOT VALIDATED BY THIS BUILD
physical Switch      NOT TESTED
```

Retained runtime evidence in Google Drive `Test_Results`:
- `MAPPING10036_01_committed_game_field_garbled.jpg`, Drive ID `1lPIAfVsVrNUed12dbQEhR1jPzKB-tQbh`, SHA-256 `fcc34d2c31d2264769eab9962c5b2c886402cc1eaac9800cb95b38e82bc72e5c`;
- `MAPPING10036_02_reopen_keyboard_gasahing_restored.jpg`, Drive ID `1DNwL_hAUzJ5BEZJEFO6pPIyFCk_jQCyK`, SHA-256 `dbbbdc24c0a035fd2ecb448405404509d787dc9548bd1be359c3261b809edaec`.

The card-possession cheat used only to expose the new-officer menu is a separate diagnostic aid and is not part of the Mapping artifact or Mapping conversion evidence.

Runtime observation sampled `가사힝`; exhaustive 2,542-entry correctness remains grounded in the prior deterministic/static verification rather than exhaustive runtime entry of every character.

## Current interpretation

Mapping 10,036 is no longer an Eden-runtime blocker for the tested forward/reverse route. Do not reopen this family merely because Korean glyphs render incorrectly when the deliberately Mapping-only artifact is used. Font/page/renderer integration, physical-Switch execution and unrelated descriptor families remain separate validation scopes.

No Astra escalation is indicated for this closure.

## Write boundary

Remote GitHub writes remain restricted to `create_blob -> create_tree -> create_commit -> update_ref(force=false)`. `create_file`, `update_file`, `delete_file`, `create_branch` and all other write actions remain excluded.

## STOP boundary

Status: `STOPPED_AWAITING_USER_SIGNAL`.

Next recommended scope: **`PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION_READ_ONLY`**.

Use the Mapping 10,036 Eden runtime closure as inherited VERIFIED evidence. Do not revalidate FZ001, Stage1, Stage2, F1, forward-986, Oracle/Assisted/Astra/TRACE, pointer-56, or the closed Mapping 10,036 route merely because the chat/model changes. Physical-Switch and renderer/font validation remain separate and are not prerequisites for beginning the read-only Action Ledger population scope.
