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
- V099–V100: `docs/VALIDATION_LEDGER_SCHEMA_V1_AMENDMENT.md`

## Current precedence

- release inline policy: `docs/INLINE_VALIDATION_POLICY.md`
- full-port rules: `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`
- accounting/invariants: `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`
- Stage 1: `docs/FULL_PORT_INVENTORY_STAGE1.md`
- Stage 2: `docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md`
- F1 localization sequence audit: `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md`
- F1 row-level static authorization: `docs/F1_STATIC_WRITE_AUTHORIZATION.md`
- machine-accounting schema candidate: `docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md`
- claim extraction rules candidate: `docs/CLAIM_EXTRACTION_RULES.md`
- machine-accounting F1 pilot: `docs/F1_MACHINE_ACCOUNTING_PILOT.md`
- schema-v1 amendment report: `docs/SCHEMA_V1_AMENDMENT.md`
- current resume point: `PROJECT_STATE.md`

Later narrower-scope corrections take precedence over older semantic overclaims.
Historical PCREF1 remains provenance-insufficient under V062 and must not be used as negative evidence against verified object/fixed-field findings.

F1 V088/V092 supersede only the later provisional F1 promotion/accounting that treated all 278 F1 residual rows as accepted. They do not modify Stage-2 V082–V086.

F1 V093/V094 close the missing row-level provenance for the exact 158 V089 static-safe rows and authorize only those manifest actions as `DIRECT_PORT` static writes. V095 is metadata-only cleanup: it distinguishes the canonical 20-byte project Build ID from the padded 32-byte NSO header field and records that duplicate local replay outputs were not duplicate canonical repository artifacts.

V096–V098 validate a machine-readable schema pilot, not a schema freeze or full migration. V099 defines the v1 candidate amendment. V100 records that exact F1 source membership passes but the full v1 regression is blocked by a pre-existing truncated repository copy of the V094 action manifest. This artifact defect does not by itself erase the historical V094 authorization conclusion, but the committed manifest must not be consumed as a complete 158-action table until its canonical bytes are provenance-restored.

Existing canonical Markdown remains authoritative. Neither V099 nor V100 freezes schema v1 or authorizes wider migration, the 797 residual, builder, IPS, runtime, or game-file work.
