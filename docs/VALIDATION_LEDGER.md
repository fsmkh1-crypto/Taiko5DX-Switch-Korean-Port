# VALIDATION_LEDGER — index

Canonical validation authority for the project.

## Operating rule

Do not repeat a well-recorded validation. Revalidation is allowed only when:

1. input file/version/hash changes;
2. new static/runtime evidence directly contradicts the record;
3. provenance is insufficient for the current high-risk decision;
4. the prior validation method is shown to be unsound.

A new chat/model/agent is never by itself a revalidation trigger.

Status values remain `VERIFIED`, `VERIFIED-RUNTIME`, `VERIFIED-LEGACY`, `NEEDS-REVERIFY`, `INVALIDATED`, `SUPERSEDED`.

## Canonical ledger parts

- V001–V039, including all pre-PC-DLL findings and PC DLL PHASE 1: `docs/VALIDATION_LEDGER_THROUGH_PHASE1.md`
- V040–V045, PC DLL PHASE 2 parser grammar: `docs/VALIDATION_LEDGER_PHASE2.md`
- V046–V051, PC DLL PHASE 3 mapping/pointer runtime semantics: `docs/VALIDATION_LEDGER_PHASE3.md`
- V052–V061, PC DLL PHASE 4 helper/descriptor runtime semantics: `docs/VALIDATION_LEDGER_PHASE4.md`
- V062, PCREF1 emitted-delivery provenance gap: `docs/VALIDATION_LEDGER_PCREF1.md`

All files are part of the canonical ledger. Later factual phases must append a new ledger part and update this index rather than revalidating established entries.

## PC Runtime Canonical Closure accounting

The 2026-09-11 PC Runtime Canonical Closure is an integration/audit stage, not a new factual validation stage. It therefore added no V062+ IDs at closure time. V062 was created later by the separately authorized PCREF1 delivery-verification stage.

Closure products:

- `docs/PC_RUNTIME_CANONICAL_CLOSURE.md`
- closed `docs/PC_RUNTIME_DLL_SPEC.md`
- `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md`
- `docs/SWITCH_COUNTERPART_SURVEY_RULES.md`

These documents must trace factual PC claims to V001–V061. The closure corrected stale aggregate wording; it did not reopen established phase facts.

## PCREF1 delivery-verification accounting

V062 records that historical PCREF1 emitted-IPS integrity is **not established** because the actual ZIP/IPS, SHA-256, final record count, guard report, manifest, round-trip report and reproducible builder were not retained in the canonical sources available to the verification session.

Consequences:

- the historical PCREF1 screen-no-change observation is retained only as an observation;
- it must not be used as negative evidence against V024/V025/V033 object/fixed-field findings;
- a later fresh reproducible delivery-control diagnostic is required before a new runtime no-change result can be interpreted causally;
- a new artifact can validate the current delivery pipeline but cannot retroactively prove what the lost PCREF1 artifact contained.

Detailed report: `docs/PCREF1_DELIVERY_VERIFICATION.md`.

### Narrow precedence correction for V029

V029's directly established byte fact remains valid: the PC descriptor changes a compare immediate `0xFF -> 0xA0`.

However, the stronger wording in V029 that assigns that compare a fully established `halfwidth/full-width path` meaning is **superseded for semantic use by PHASE 4 V060 and the closure**. PHASE 4 establishes the raw threshold change while leaving broader display meaning only partially confirmed. Future work must cite the raw threshold unless later Switch/PC context independently proves the stronger semantic role.

This is a scope/wording precedence correction; it does not create a new validation ID.

Key closure corrections that must not be reintroduced:

- pointer wire grammar is `u8 mode + reserved[3] + u32 arg`, not `<IIII>`;
- prefix/helper use one contiguous private allocation, not two mandatory independent allocations;
- mapping alone is 40,144 bytes; 40,746 bytes is mapping + 602-byte pointer pool;
- helper `+0x20` fallback resumes original processing rather than immediate invalid rejection;
- raw `font_page_limit` behavior is compare threshold `0xFF -> 0xA0`, not a literal page-count fact or a fully named display-path fact;
- the PC descriptor unique+anchor rule is target-version application machinery, not a Switch counterpart-discovery gate.

## Current precedence

- release inline safety policy: `docs/INLINE_VALIDATION_POLICY.md`
- validated fact/revalidation authority: this index and its ledger parts, with later narrower-scope corrections taking precedence over older semantic overclaims
- PCREF1 delivery-verification record: `docs/PCREF1_DELIVERY_VERIFICATION.md`
- closed PC runtime aggregate specification: `docs/PC_RUNTIME_DLL_SPEC.md`
- PC runtime closure/audit: `docs/PC_RUNTIME_CANONICAL_CLOSURE.md`
- corrected-runtime observations: `docs/RUNTIME_TEST_RESULTS.md`
- D5519/yomi/repeated-object/font-width analysis: `docs/POST_D5519_ANALYSIS.md`
- PC runtime reverse engineering index: `docs/PC_RUNTIME_REVERSE_ENGINEERING.md`
- next Switch survey baseline: `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md`
- next Switch survey operating rules: `docs/SWITCH_COUNTERPART_SURVEY_RULES.md`
- current resume point: `PROJECT_STATE.md`

When a new result changes a canonical fact, update the relevant ledger part/index in the same authorized work session as state/changelog documentation.
