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

Both files are part of the canonical ledger. Later phases must append a new phase ledger part and update this index, rather than revalidating established entries.

## Current precedence

- release inline safety policy: `docs/INLINE_VALIDATION_POLICY.md`
- validated fact/revalidation authority: this index and its ledger parts
- corrected-runtime observations: `docs/RUNTIME_TEST_RESULTS.md`
- D5519/yomi/repeated-object/font-width analysis: `docs/POST_D5519_ANALYSIS.md`
- PC runtime reverse engineering index: `docs/PC_RUNTIME_REVERSE_ENGINEERING.md`
- current resume point: `PROJECT_STATE.md`

When a new result changes a canonical fact, update the relevant ledger part/index in the same authorized work session as state/changelog documentation.
