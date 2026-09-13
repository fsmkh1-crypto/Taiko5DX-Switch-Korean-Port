# PROJECT_STATE

Last updated: 2026-09-14 (KST)

This file is the sole project-resume authority.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"MAPPING_10036_HELPER_HOOK_CONTRACT_MATERIALIZED","scope_kind":"READ_ONLY","status":"STOPPED_AWAITING_USER_SIGNAL","last_closed_validation_id":"V239","last_closed_stage_commit":"15795a7952d703c17fac294e90a9a8124c330b04","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"schema_freeze_status":"FROZEN_FZ001","mapping_10036_survey":"docs/MAPPING_10036_SWITCH_COUNTERPART_SURVEY.txt","mapping_10036_realization_design":"docs/MAPPING_10036_REALIZATION_DESIGN.txt","mapping_10036_alignment_padding_validity":"docs/MAPPING_10036_ALIGNMENT_PADDING_RUNTIME_VALIDITY.txt","mapping_10036_helper_hook_contract":"docs/MAPPING_10036_HELPER_HOOK_CONTRACT.txt","mapping_10036_helper_hook_index":"data/post_freeze/mapping_10036_helper_hook_contract_v1/INDEX.json","required_reads":["docs/MASTER_RULE_REGISTRY.md","docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md","docs/MAPPING_10036_SWITCH_COUNTERPART_SURVEY.txt","docs/MAPPING_10036_REALIZATION_DESIGN.txt","docs/MAPPING_10036_ALIGNMENT_PADDING_RUNTIME_VALIDITY.txt","docs/MAPPING_10036_HELPER_HOOK_CONTRACT.txt","data/post_freeze/mapping_10036_helper_hook_contract_v1/MEMBERSHIP.json","docs/VALIDATION_LEDGER_MAPPING_10036_HELPER_HOOK_CONTRACT.txt","docs/WRITE_TRANSPORT_INCIDENT_20260914.txt","docs/F1_STATIC_WRITE_AUTHORIZATION.md","docs/PC_PATCH_ORACLE_TRACE_19_CLOSURE.md"]}
PROJECT_RESUME_V2 -->

## Current canonical state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Inherited without revalidation: Stage1, Stage2, F1, FZ001, forward-986, Oracle/Assisted/Astra/TRACE closure, full-corpus coverage/semantic-owner/action-collapse overlays, pointer-56 closure, and mapping-10,036 survey/design/storage-class closure through V233.

Canonical inline source accounting remains 17,103: Stage2 13,771 + F1 1,311 + forward 986 + gap 1,035. Existing F1 static WRITE_SAFE authority remains 158. No new WRITE_SAFE is granted here.

## Mapping 10,036 realization state

Preferred family remains `MAPPING_KOREAN_MISS_FALLBACK_COMPACT_V1`.

Closed before this scope:
- preserve original 7,494-entry table, four table references, two count literals and both six-entry loops;
- Korean addition = exact 2,542-pair semantic suffix;
- TEXT alignment storage 0x58CE60..0x58D000 is runtime/delivery-valid RX storage;
- RODATA alignment storage 0x9BF018..0x9C0000 is runtime/delivery-valid read-only storage.

## Helper / hook contract — V234–V239

Canonical evidence:
- `docs/MAPPING_10036_HELPER_HOOK_CONTRACT.txt`
- `data/post_freeze/mapping_10036_helper_hook_contract_v1/MEMBERSHIP.json`
- `data/post_freeze/mapping_10036_helper_hook_contract_v1/INDEX.json`
- `docs/VALIDATION_LEDGER_MAPPING_10036_HELPER_HOOK_CONTRACT.txt`

Closed facts:
- forward miss hook owner: 0x4304E0 -> helper 0x58CE60;
- reverse miss hook owner: 0x430798 -> helper 0x58CF00;
- each hook is one direct 4-byte AArch64 branch and is within direct branch range;
- forward hit re-entry: 0x430568; forward fallback re-entry: 0x43056C;
- reverse re-entry: 0x430820;
- helper scratch is caller-saved x8-x15 only; x19-x28/x30 remain preserved;
- exact helper text size = 308 bytes / 77 instructions; TEXT slack = 108 bytes;
- helper payload SHA-256 = 60b1fd4b8231dca9f11e5e46007bddef97f55434f1e46df1445be2fb361e6cad;
- delta payload = 2,349 bytes; SHA-256 = ddedc507fa892a5b5be6f35ab24f0a0e5fac0d71e633134712b33bd4c6a2088f;
- exhaustive forward/reverse 16-bit-domain verification: exactly 2,542 hits in each direction, zero extra hits, exact 2,542/2,542 round-trip;
- original-byte/zero-preimage guards are fixed for all four physical write sites;
- proposed physical Action Ledger IDs: `MAP10036_FWD_MISS_HOOK_V1`, `MAP10036_REV_MISS_HOOK_V1`, `MAP10036_HELPER_TEXT_V1`, `MAP10036_DELTA_RODATA_V1`;
- new WRITE_SAFE = 0.

No Astra escalation was required because no semantic/context ambiguity remained after deterministic control-flow, ABI and exhaustive mapping verification.

## Remaining mapping open items

- static WRITE_SAFE authorization for the four independently guardable physical writes;
- delivery-controlled diagnostic build only after a fresh execution signal authorizes an implementation/build scope;
- runtime Korean forward/reverse round-trip observation.

## Write boundary

Remote GitHub writes are restricted to `create_blob -> create_tree -> create_commit -> update_ref(force=false)`. All file add/modify/delete/recovery operations use Git object writes only. `create_file`, `update_file`, `delete_file`, `create_branch` and every other write action remain excluded even if surfaced by tools.

## STOP boundary

Status: `STOPPED_AWAITING_USER_SIGNAL`.

Next recommended scope: **`MAPPING_10036_STATIC_WRITE_SAFETY_AUTHORIZATION_READ_ONLY`**.

That scope may adjudicate WRITE_SAFE for the exact four mapping physical actions using the now-closed owner, storage, helper, hook, guard and delivery evidence. It must not emit IPS/build/runtime/game-file changes or combine unrelated descriptor families.
