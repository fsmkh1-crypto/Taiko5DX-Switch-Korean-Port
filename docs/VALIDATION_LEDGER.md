# VALIDATION_LEDGER

Canonical record of what has actually been validated, what still needs revalidation, and what has been invalidated or superseded.

## Operating rule

The project must not repeatedly re-check an already well-recorded fact. However, a prior conclusion whose evidence/provenance is incomplete may be revalidated **once when the result materially matters to current work**. After that revalidation, the result must be recorded here with enough detail that another agent can reproduce or trust it without starting over.

A validation may be repeated only when at least one of the following is true:

1. an input file/version/hash changed;
2. a new runtime or static-analysis result directly contradicts the recorded conclusion;
3. the original record lacks enough provenance to support a current implementation decision;
4. the validation method itself is later shown to be unsound.

Do not revalidate merely because a new chat, agent, or model is starting.

## Required evidence for new validations

Every meaningful validation entry should record, where applicable:

- validation ID and date;
- exact claim being tested;
- input identity: filename/role, version, size, hash, Build ID as available;
- method/tool/script and relevant parameters;
- exact offsets/ranges/count units when relevant;
- observed result;
- final status;
- artifact/report/script path or commit that can reproduce the result;
- reason for any later revalidation, invalidation, or supersession.

Counts must state their unit explicitly, e.g. `records`, `unique patterns`, or `candidate locations`.

## Status values

- `VERIFIED`: direct evidence is sufficiently recorded for reuse.
- `VERIFIED-RUNTIME`: directly observed in the target runtime; keep static-safety claims separate.
- `VERIFIED-LEGACY`: likely valid prior result, but provenance is not yet sufficient for a high-risk implementation decision. Revalidate once if that decision depends on it.
- `NEEDS-REVERIFY`: conflicting, incomplete, or externally reported result that must be reproduced before becoming canonical.
- `INVALIDATED`: a previous conclusion was disproved.
- `SUPERSEDED`: still historically true, but replaced by a stronger/newer rule or result.

## Current ledger

| ID | Claim | Status | Recorded evidence / reuse rule |
|---|---|---|---|
| V001 | Fixed Switch target is v1.1.3, Title ID `0100346017304000`, `main` Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`. | VERIFIED | Recorded in `PROJECT_STATE.md`; builder hard-guards the Build ID. Recheck only if target version/dump changes. |
| V002 | Switch NSO mapped layout is text `0x000000+0x58CE60`, rodata `0x58D000+0x432018`, data `0x9C0000+0x60430`. | VERIFIED | Recorded in `PROJECT_STATE.md`; builder hard-guards the exact segment layout. Recheck only if `main` changes. |
| V003 | Switch original `FONT_JPN.G1T` matches Steam original; original SHA-256 `9c886848...a0083e`; PC Korean font SHA-256 `c82d80da...66932`; 50 -> 64 pages. | VERIFIED | Recorded in `PROJECT_STATE.md`; original/patched font hash guards exist in builder. Recheck only if source patch/dump changes. |
| V004 | T5K121R contains 10,036 mappings, 17,103 inline records, 56 pointer records, 11 runtime descriptors. | VERIFIED | Parsed directly from `RT_RCDATA/101`; layout and counts recorded in `PROJECT_STATE.md`/`PATCH_MAP.md` and parser path. Do not recount unless PC patch archive changes. |
| V005 | Original mapping count is 7,494 (`0x1D46`), Korean additions 2,542, total 10,036 (`0x2734`). | VERIFIED | Recorded consistently in `PROJECT_STATE.md` and `PATCH_MAP.md`. Any conflicting `7,334` claim is non-canonical until reproduced and explained. |
| V006 | Page mapper patch at `0x44650C` adds `EB~F8 -> pages 49~62` while preserving existing ranges. | VERIFIED | Original/replacement 44-byte sequences recorded in `PROJECT_STATE.md` and `PATCH_MAP.md`; implemented with original-byte guard. Runtime Korean title rendering is additional evidence, not proof of every page-mapper edge case. |
| V007 | Historical exact-unique scan: 17,103 records -> 8,713 unique original patterns; 5,523 candidate rodata patterns; 4 overlap-skipped; 5,519 selected patterns covering 5,521 PC records. | VERIFIED-LEGACY | Counts are reproducible from the existing matcher/builder, but **selection safety is INVALIDATED as a release criterion**. Use only as historical/regression statistics. If a future decision depends on any sub-count, rerun once and record report artifact. |
| V008 | `unique exact match in rodata` is sufficient to classify an inline patch as safe. | INVALIDATED | Runtime: integrated v0.2a failed, while NO-INLINE v0.2b booted and rendered Korean title. `docs/INLINE_VALIDATION_POLICY.md` supersedes the old rule. |
| V009 | NO-INLINE baseline (207 RomFS payloads + Korean font + page mapper, no inline set) boots and reaches Korean title in Eden Android. | VERIFIED-RUNTIME | User-observed runtime result, recorded in `docs/RUNTIME_TEST_RESULTS.md`. This proves the baseline path reaches title; it does not prove late-game safety of every baseline component. |
| V010 | A half of old inline set freezes; B half reaches title then exits after button input. | VERIFIED-RUNTIME | User-observed runtime result, recorded in `docs/RUNTIME_TEST_RESULTS.md`. This disproves the single-localized-fault assumption and does not make either passing prefix/screen globally safe. |
| V011 | External review measurements: large PC-RVA/Switch-offset monotonic runs/LIS, 12,347 NUL-covering records, 430 high-risk termination cases, and `8,981` multi-match-related count. | NEEDS-REVERIFY | Useful design hypotheses, but provenance/unit definitions are not yet canonical in this repo and one accompanying mapping count conflicted with verified `7,494`. Reproduce once before using these numbers as hard gates; record exact script, inputs, units, and report. |

## Inline-validation precedence

For inline mapping, `docs/INLINE_VALIDATION_POLICY.md` is the normative safety policy. This ledger answers a different question: **which underlying measurements and facts are already sufficiently proven, and which must be revalidated before use?**

When a new validation changes a canonical fact, update this ledger first or in the same commit as `PROJECT_STATE.md` / `PATCH_MAP.md` / `CHANGELOG.md`.
