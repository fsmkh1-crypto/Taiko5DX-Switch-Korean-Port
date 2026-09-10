# CHANGELOG

## 2026-09-10

### Critical Eden IPS offset correction

- Confirmed from Eden/Yuzu NSO loading code that ExeFS classic IPS is applied to an artificial image composed of `0x100-byte NSOHeader + decompressed mapped NSO image`.
- Canonical rule is now: `emitted IPS offset = mapped flat NSO offset + 0x100`.
- Corrected `builder/build.py` so internal `PatchPlan` addresses remain mapped offsets and `write_ips()` adds `+0x100` only at serialization time.
- Corrected `builder/build_p0n_noop.py` to generate `P0N2` under the same coordinate rule and to reparse the emitted IPS back to mapped coordinates for verification.
- Runtime result `P0N v0.2f = freeze` is real, but its original interpretation was invalidated: P0N was not a true no-op in Eden because every record was applied `0x100` too early.
- The same applies to all IPS-bearing builds through P0N v0.2f, including v0.2a/v0.2b/v0.2c/A/B. Their observations remain historical runtime facts, but they cannot be used as candidate-safety evidence.
- In particular, v0.2b reaching the Korean title does not prove that the intended page mapper at mapped `0x44650C` ran; the old emitted record targeted mapped `0x44640C`. The corrected emitted IPS offset is `0x44660C`.
- Generated corrected diagnostic `P0N2_Taiko5DX_KR_DBG_NOOP5519_PLUS100_v0.2g.zip`, SHA-256 `1ccb27e7f8836b8687ade7e147b0f549d49069dcecebaf808fa6eabd3277e8f6`.
- P0N2 contains 5,520 IPS records total: corrected page mapper plus 5,519 verified true no-op inline records. Static round-trip verification passes; Eden runtime result is pending.
- Updated `PROJECT_STATE.md`, `PATCH_MAP.md`, `docs/PHASE0_FAILURE_MODE_PLAN.md`, `docs/RUNTIME_TEST_RESULTS.md`, and `docs/VALIDATION_LEDGER.md` so later work cannot reuse the old no-shift interpretation.

### Phase 0 failure-mode diagnosis started

- Added `docs/PHASE0_FAILURE_MODE_PLAN.md` as the mandatory prerequisite before implementing the full 17,103-record inline validator.
- Added `builder/phase0_probe.py` for reproducible count/provenance measurements and `builder/build_p0n_noop.py` for the first runtime build-layer control.
- Reverified the historical selector counts on fixed inputs: 17,103 records, 8,713 unique original patterns, 5,523 unique-rodata candidates, 4 overlap skips, 5,519 historical selected patterns covering 5,521 PC records.
- Reproduced record-level collinearity statistics with explicit units: 6,053 unique-match record pairs, global LIS 3,524, 2,529 outside; top monotonic runs 1,844 / 1,074 / 978 / 78. Global LIS remains reference evidence only, not a safety hard gate.
- Reproduced NUL statistics: 12,347 records where the original contains NUL and replacement contains none; 4,747 originals contain no NUL. These are risk statistics, not automatic run-on verdicts.
- Did **not** reproduce the external `430` termination and `8,981 records / 1,242 patterns >=5-match` counts under the stated definitions. They remain non-canonical until the original scope/unit is identified.
- Confirmed both Switch conversion loops still use `0x1D46 = 7,494`. ARM64 disassembly also shows defined miss fallbacks (`0x81A1` for UTF-16->game code, `U+25A0` for game code->UTF-16), so mapping expansion is required functionally but is not yet proven as the direct freeze cause.
- Found a critical source-identity issue: the Drive `PC_Original/Taiko5DX.exe` is version-string `1.2.1.0` but does not match the T5K target. Supplied EXE is 18,479,304 bytes / SHA-256 `22e1cd1a...65ef6`; T5K target is 18,685,960 bytes / SHA-256 `10c69bab...65a2` (Steam build 9163702). The supplied EXE is barred from PC-RVA neighborhood/homology evidence.
- Updated `AGENTS.md`, `PROJECT_STATE.md`, `PATCH_MAP.md`, and `docs/VALIDATION_LEDGER.md` so later agents cannot skip Phase 0 or reuse the wrong PC EXE as context evidence.

### Validation ledger promoted to mandatory workflow

- Promoted `docs/VALIDATION_LEDGER.md` into the mandatory pre-read path in `AGENTS.md`.
- Any agent must consult the ledger before repeating a prior validation. A new chat/model/agent is never by itself a reason to revalidate.
- Revalidation is allowed only for changed inputs/version/hash, contradictory new evidence, inadequate provenance for a current high-risk decision, or proof that the original method was unsound.
- When a prior result is too poorly documented to reuse safely, it may be revalidated once, but the revalidation must record exact claim, input identity/hash/version, method/script/parameters, offsets/ranges/count units, observed result, status, and reproducible artifact/report/commit path.
- Future meaningful sessions must update the ledger whenever facts are newly verified, reverified, invalidated, or superseded, so repeated analysis is avoided.

### Canonical inline-validation redesign

- Added `docs/INLINE_VALIDATION_POLICY.md` as the normative project-level policy for all future T5K inline mapping.
- Added `docs/RUNTIME_TEST_RESULTS.md` to preserve the actual Eden Android observations separately from safety conclusions.
- Promoted the key rule to `AGENTS.md`: `unique exact match` is candidate-discovery evidence only and can never by itself authorize a release patch.
- Changed the validator target from the old 5,519 exact-unique rodata subset to the full 17,103-record T5K inline corpus.
- Defined mandatory safety axes: game-code validity, PC↔Switch structural homology, independently established Switch field/boundary structure, conflict/binary-risk rejection, and simulated post-patch offline re-validation.
- Adopted piecewise collinearity/anchor analysis as the preferred global homology model; do not assume one global LIS or perfect ordering across the whole binary.
- Prohibited automatic translation shortening merely to fit an unproven Switch field width. Uncertain candidates are HOLD until field structure is established.
- Defined ANCHOR / SAFE-A / SAFE-B / PROBABLE / HOLD / REJECT classes and made hard gates primary over weighted confidence scoring.
- Restricted binary split / delta debugging to isolating currently reproducible failures. A passing split is never evidence that all members are safe.
- Added the explicit user-start gate to `AGENTS.md`: design/review discussion does not authorize implementation/build/commit work unless the user explicitly starts it; documentation-only requests authorize only the requested documentation edits.
- Updated `PROJECT_STATE.md` and `PATCH_MAP.md` so the old 5,519 selector is no longer presented as a safe implemented subset.

### Eden runtime evidence refinement

- Add-on disabled: baseline game boots/runs normally.
- `v0.2b NO-INLINE` boots and renders the Korean title `태합입지전 V DX`; later IPS-coordinate analysis showed its intended page-mapper rewrite was not actually applied at the intended mapped offset.
- `v0.2c` with one suspicious inline removed still fails.
- Address-ordered half A freezes.
- Address-ordered half B reaches the Korean title, then forced-exits/crashes after button input.
- These observations are retained as history, but the old inference of candidate-level/multi-fault behavior is superseded because all those IPS records were emitted `0x100` too early.

### First Eden Android runtime result

- Integrated v0.2a freezes when the add-on is enabled.
- With the same game and Eden environment, disabling the add-on restores normal boot/execution.
- This confirms only that the enabled mod package affected execution; later analysis found the IPS coordinate bug, so v0.2a cannot be used as clean semantic-inline evidence.
- Do not attribute the freeze to Eden's Global/Custom per-game setting at this stage; the add-on enable/disable state is the confirmed differentiator.

### Eden Android test packaging

- Added `docs/EDEN_ANDROID_TEST_GUIDE.md`.
- Recorded a real target-environment constraint: the user could not directly access Eden's internal Android folder with the normal file manager.
- Current development ZIP instructions use Eden's own per-game Add-ons importer: extract to an ordinary Android folder, then `+ Install` -> `Mods and cheats`, selecting the mod root containing `exefs/` and `romfs/`.
- Added a first-run checklist focused on boot success, Korean glyph rendering, clipping/width problems, event dialogue behavior, and crash/log capture.

### Distribution strategy

- Fixed the primary final user-facing patcher target as an **Android APK**, matching Eden Android as the main usage environment.
- The APK will be a separate patch-generation app, not an Eden plugin or executable installed inside Eden.
- Standard inputs remain a complete extracted Switch v1.1.3 dump plus `Taiko5DX_Korean_Patcher_v1.02.zip`.
- Standard output will be an Eden-ready mod directory containing `exefs/` and `romfs/`.
- Android Storage Access Framework / user-granted folder access will be used for source selection and output placement.
- The APK will not embed copyrighted game files, the PC patch archive, translated payloads, fonts, keys, XCI/NSP/NCA, or full dumps.
- Development order is fixed as core builder first, Android APK frontend second. The APK must reuse the same patch engine rather than fork the logic.
- A Windows CLI/EXE frontend may be added later only as a secondary convenience layer.

### Integrated port expansion

- Added direct PE resource extraction for `dinput8.dll` `RT_RCDATA/101`.
- Added exact parser for the `T5K121R` container.
- Confirmed and encoded the resource layout: 10,036 mappings, 602-byte pointer string pool, 158-byte helper blob, 17,103 inline records, 56 pointer records, and 11 runtime descriptors.
- Added a single-pass Aho-Corasick matcher for the 17,103 PC inline replacement records.
- Added the former exact-unique Switch mapping selector: exact unique original bytes, Switch rodata only, no conflicting replacement, no overlap guessing.
- On the fixed Switch 1.1.3 `main`, that former selector chose 5,519 unique inline patterns covering 5,521 PC records. It is retained only as a reference/regression set; release safety still requires the full validation policy.
- Reworked IPS generation to support thousands of patch records in one integrated Eden build.
- Integrated 207 directly reusable PC Korean RomFS payload files; `CMENU/CWTDAT_JP.TR5` remains intentionally excluded.
- Added fixed NSO segment-layout guards and original Switch font hash guard.

### Still pending

- **P0N2 Eden runtime result**; then corrected MVI 1/10/100 content tests if P0N2 passes.
- Exact Steam build-9163702 PC EXE for optional PC-binary context/homology work.
- Full 17,103-record inline correspondence/validation pipeline after Phase 0.
- 7,494 -> 10,036 Switch mapping table relocation/reference/count patches.
- Switch correspondence for the 56 pointer records.
- `runtime_byte_validation`, font threshold, `ui_width_1~4`, `description_font_1~2` counterparts as evidence requires.
- Switch-native `CWTDAT_JP.TR5` reconstruction.

### Repository initialization

- Established Nintendo Switch v1.1.3 / Title ID / NSO Build ID as the fixed development target.
- Adopted full extracted Switch 1.1.3 dump as the standard local development input.
- Documented the existing PC Korean patch as the source implementation to port rather than rebuilding translation assets from scratch.
- Recorded confirmed PC payload composition: 208 game-data replacements plus `dinput8.dll`.
- Recorded the Switch CWTDAT structural exception.
- Recorded the confirmed 64-page Korean font layout and custom Korean byte-code range.
- Recorded Switch text/font functions at `0x430350`, `0x4305D0`, `0x446310`, and `0x446420`.
- Recorded and implemented the ARM64 page-mapper rewrite adding `EB~F8 -> pages 49~62`.
- Recorded exact mapping counts: 7,494 original + 2,542 Korean = 10,036.
- Corrected the old misunderstanding of 17,103 PC EXE records: they are primarily same-length in-place replacement records, not a monolithic injected text blob.
- Established integrated-build-first workflow and Eden Android as the primary test target.