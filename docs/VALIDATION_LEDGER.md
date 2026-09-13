# VALIDATION LEDGER — index

Canonical validation authority. Do not repeat a well-recorded validation solely because a new chat/model/agent is used.

Revalidation is allowed only when input identity changes, new evidence contradicts the record, provenance is insufficient for the decision, or the prior method is shown unsound.

## Canonical V-ledger parts

- V001–V039: `docs/VALIDATION_LEDGER_THROUGH_PHASE1.md`
- V040–V045: `docs/VALIDATION_LEDGER_PHASE2.md`
- V046–V051: `docs/VALIDATION_LEDGER_PHASE3.md`
- V052–V061: `docs/VALIDATION_LEDGER_PHASE4.md`
- V062: `docs/VALIDATION_LEDGER_PCREF1.md`
- V063–V069: `docs/VALIDATION_LEDGER_R0.md`
- V070–V073: `docs/VALIDATION_LEDGER_R1.md`
- V074–V075: `docs/VALIDATION_LEDGER_R1B.md`
- V076–V077: `docs/VALIDATION_LEDGER_R1C.md`
- V078–V081: `docs/VALIDATION_LEDGER_INVENTORY_STAGE1.md`
- V082–V086: `docs/VALIDATION_LEDGER_STAGE2.md`
- V087–V092: `docs/VALIDATION_LEDGER_F1.md`
- V093–V095: `docs/VALIDATION_LEDGER_F1_AUTH.md`
- V096–V098: `docs/VALIDATION_LEDGER_MACHINE_ACCOUNTING_PILOT.md`
- V099–V100, V102–V107: `docs/VALIDATION_LEDGER_SCHEMA_V1_AMENDMENT.md`
- V101: `docs/VALIDATION_LEDGER_DOCUMENT_GOVERNANCE.md`
- V108–V118: `docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_V1.txt`
- V119–V126: `docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_ASSISTED_297_FOLLOWUP.txt`
- V127–V133: `docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_ASTRA_10_FOLLOWUP.txt`
- V134–V143: `docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_TRACE_19_CLOSURE.txt`
- V144–V151: `docs/VALIDATION_LEDGER_MASTER_RULE_REGISTRY.txt`

## Post-freeze namespaced ledgers

- CF001–CF010: `docs/VALIDATION_LEDGER_CAP64_CORRECTION.txt`
- PF001–PF021: `docs/VALIDATION_LEDGER_POST_FREEZE_RESIDUAL.txt`
- FS251-001–FS251-012: `docs/VALIDATION_LEDGER_FORWARD_STRUCTURAL_CENSUS_251.txt`
- FS001–FS010: `docs/VALIDATION_LEDGER_FORWARD_986_STRUCTURAL.txt`

## Current precedence

- project resume authority: `PROJECT_STATE.md`
- master rule discovery/precedence overlay: `docs/MASTER_RULE_REGISTRY.md`
- document authority registry: `docs/DOCUMENT_AUTHORITY_INDEX.json`
- project operating rules: `AGENTS.md`
- artifact/machine provenance rules: `docs/ARTIFACT_AND_PROVENANCE_RULES.md`
- validation policy: `docs/VALIDATION_POLICY.md`
- GitHub/CI policy: `docs/GITHUB_AND_CI_POLICY.md`
- release inline policy: `docs/INLINE_VALIDATION_POLICY.md`
- full-port rules: `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`
- accounting/invariants: `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`
- PC runtime specification: `docs/PC_RUNTIME_DLL_SPEC.md`
- Stage 1: `docs/FULL_PORT_INVENTORY_STAGE1.md`
- Stage 2: `docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md`
- F1 audit/authorization: `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md`, `docs/F1_STATIC_WRITE_AUTHORIZATION.md`
- frozen machine-accounting schema/claims: `docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md`, `docs/CLAIM_EXTRACTION_RULES.md`
- schema freeze: `data/pilot/f1_v1_candidate/schema_freeze_declaration.json`
- post-freeze current forward routing closure: `docs/PC_PATCH_ORACLE_TRACE_19_CLOSURE.md`

Later narrower-scope corrections take precedence over older semantic overclaims. Historical plans and handoffs never override `PROJECT_STATE.md`. Counterpart/routing closure never implies `WRITE_SAFE`.
