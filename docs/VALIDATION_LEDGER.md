# VALIDATION LEDGER — index

Canonical validation authority. Do not repeat a well-recorded validation solely because a new chat/model/agent is used.

Revalidation is allowed only when input identity changes, new evidence contradicts the record, provenance is insufficient for the decision, or the prior method is shown unsound.

## Canonical ledger parts

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
- V099–V100, V102: `docs/VALIDATION_LEDGER_SCHEMA_V1_AMENDMENT.md`
- V101: `docs/VALIDATION_LEDGER_DOCUMENT_GOVERNANCE.md`

## Current precedence

- project resume authority: `PROJECT_STATE.md`
- document authority registry: `docs/DOCUMENT_AUTHORITY_INDEX.json`
- project operating rules: `AGENTS.md`, `docs/PROJECT_OPERATING_RULES.md`
- artifact/machine provenance rules: `docs/ARTIFACT_AND_PROVENANCE_RULES.md`
- validation policy: `docs/VALIDATION_POLICY.md`
- GitHub/CI policy: `docs/GITHUB_AND_CI_POLICY.md`
- release inline policy: `docs/INLINE_VALIDATION_POLICY.md`
- full-port rules: `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`
- accounting/invariants: `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`
- PC runtime specification: `docs/PC_RUNTIME_DLL_SPEC.md`
- Stage 1: `docs/FULL_PORT_INVENTORY_STAGE1.md`
- Stage 2: `docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md`
- F1 audit: `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md`
- F1 authorization: `docs/F1_STATIC_WRITE_AUTHORIZATION.md`
- machine-accounting schema candidate: `docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md`
- claim extraction candidate: `docs/CLAIM_EXTRACTION_RULES.md`
- schema-v1 amendment report: `docs/SCHEMA_V1_AMENDMENT.md`

Later narrower-scope corrections take precedence over older semantic overclaims. Historical plans and handoffs never override `PROJECT_STATE.md`.

V094 historical authorization remains canonical semantic evidence. V100 records the original repository-artifact truncation. V101 classifies the later 12,071-byte upload as `FAILED_TRANSPORT_NOT_CANONICAL`. V102 closes the V094 transport blocker with deterministic plain JSONL shards while preserving the historical gzip identity; the candidate regression then advances to a separate `V089.C03` atomic-claim-policy blocker.

V096–V102 do not freeze schema v1. Documentation governance and V094 transport repair do not authorize wider migration, the 797 residual, builder, IPS, runtime, or game-file work.
