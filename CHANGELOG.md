# CHANGELOG

## 2026-09-10

### M1A corrected real-inline test passed

- User runtime-tested `M1A v0.2h` in Eden Android and progressed successfully through the early scenario/protagonist-selection flow without freeze or forced exit.
- M1A contains exactly one real T5K inline replacement: `R489`, `シナリオを選んでください` -> `시나리오를 선택하세요`, mapped `0x69B6A1`, Eden IPS `0x69B7A1`.
- This proves at least one corrected real inline record can coexist with the corrected RomFS/font/page-mapper baseline. It does not certify the historical 5,519-set.
- Screenshot-visible Korean names/descriptions elsewhere are primarily baseline RomFS/font output and are not being misattributed to R489.
- Prepared two more independent one-record controls before scaling to 10 records: `M1B v0.2i` (`R674`, `主人公選択` -> `주인공선택`, mapped `0x682DA4`) and `M1C v0.2j` (`R726`, `はじめから` -> `처음부터`, mapped `0x684140`).
- Updated `PROJECT_STATE.md`, `docs/RUNTIME_TEST_RESULTS.md`, and `docs/VALIDATION_LEDGER.md` so M1A PASS is canonical and the next action is M1B/M1C.

### P0N2 passed; corrected MVI testing started

- User runtime-tested `P0N2_Taiko5DX_KR_DBG_NOOP5519_PLUS100_v0.2g.zip` in Eden Android.
- P0N2 boots, reaches the Korean title, accepts input, and reaches the next main menu.
- This verifies that the corrected `mapped + 0x100` classic-IPS coordinate path works through the tested menu path and that 5,520 IPS records are not intrinsically the old freeze mechanism.
- The old P0N/v0.2a/v0.2b/v0.2c/A/B semantic interpretations remain superseded because those builds wrote IPS records `0x100` early.
- Added `builder/build_mvi.py`, a reusable diagnostic builder that accepts explicit 1-based T5K record IDs, requires one exact Switch-rodata occurrence, and emits corrected-offset MVI builds. MVI inclusion is diagnostic only, not release-SAFE promotion.
- Prepared `M1A v0.2h` with exactly one real inline replacement: T5K record 489, `シナリオを選んでください` -> `시나리오를 선택하세요`, mapped `0x69B6A1`, Eden IPS `0x69B7A1`.
- M1A test route is title -> main menu -> new game -> scenario selection; confirm Korean prompt and continued responsiveness.
- Updated `PROJECT_STATE.md`, `docs/RUNTIME_TEST_RESULTS.md`, and `docs/VALIDATION_LEDGER.md` to make P0N2 PASS canonical and move Phase 0 to corrected MVI content testing.

### Critical Eden IPS offset correction

- Confirmed from Eden/Yuzu NSO loading code that ExeFS classic IPS is applied to an artificial image composed of `0x100-byte NSOHeader + decompressed mapped NSO image`.
- Canonical rule is now: `emitted IPS offset = mapped flat NSO offset + 0x100`.
- Corrected `builder/build.py` so internal `PatchPlan` addresses remain mapped offsets and `write_ips()` adds `+0x100` only at serialization time.
- Corrected `builder/build_p0n_noop.py` to generate `P0N2` under the same coordinate rule and to reparse the emitted IPS back to mapped coordinates for verification.
- Runtime result `P0N v0.2f = freeze` is real, but its original interpretation was invalidated: P0N was not a true no-op in Eden because every record was applied `0x100` too early.
- The same applies to all IPS-bearing builds through P0N v0.2f, including v0.2a/v0.2b/v0.2c/A/B. Their observations remain historical runtime facts, but they cannot be used as candidate-safety evidence.
- In particular, v0.2b reaching the Korean title does not prove that the intended page mapper at mapped `0x44650C` ran; the old emitted record targeted mapped `0x44640C`. The corrected emitted IPS offset is `0x44660C`.
- Generated corrected diagnostic `P0N2_Taiko5DX_KR_DBG_NOOP5519_PLUS100_v0.2g.zip`, SHA-256 `1ccb27e7f8836b8687ade7e147b0f549d49069dcecebaf808fa6eabd3277e8f6`.
- P0N2 contains 5,520 IPS records total: corrected page mapper plus 5,519 verified true no-op inline records. Static round-trip verification passes.

### Phase 0 failure-mode diagnosis started

- Added `docs/PHASE0_FAILURE_MODE_PLAN.md` as the mandatory prerequisite before implementing the full 17,103-record inline validator.
- Added `builder/phase0_probe.py` for reproducible count/provenance measurements and `builder/build_p0n_noop.py` for the first runtime build-layer control.
- Reverified the historical selector counts on fixed inputs: 17,103 records, 8,713 unique original patterns, 5,523 unique-rodata candidates, 4 overlap skips, 5,519 historical selected patterns covering 5,521 PC records.
- Reproduced record-level collinearity statistics with explicit units: 6,053 unique-match record pairs, global LIS 3,524, 2,529 outside; top monotonic runs 1,844 / 1,074 / 978 / 78. Global LIS remains reference evidence only, not a safety hard gate.
- Reproduced NUL statistics: 12,347 records where the original contains NUL and replacement contains none; 4,747 originals contain no NUL. These are risk statistics, not automatic run-on verdicts.
- Did **not** reproduce the external `430` termination and `8,981 records / 1,242 patterns >=5-match` counts under the stated definitions. They remain non-canonical until the original scope/unit is identified.
- Confirmed both Switch conversion loops still use `0x1D46 = 7,494`. ARM64 disassembly also shows defined miss fallbacks (`0x81A1` for UTF-16->game code, `U+25A0` for game code->UTF-16), so mapping expansion is required functionally but is not yet proven as the direct freeze cause.
- Found a critical source-identity issue: the Drive `PC_Original/Taiko5DX.exe` is version-string `1.2.1.0` but does not match the T5K target. Supplied EXE is 18,479,304 bytes / SHA-256 `22e1cd1a...65ef6`; T5K target is 18,685,960 bytes / SHA-256 `10c69bab...65a2` (Steam build 9163702). The supplied EXE is barred from PC-RVA neighborhood/homology evidence.

### Validation ledger promoted to mandatory workflow

- Promoted `docs/VALIDATION_LEDGER.md` into the mandatory pre-read path in `AGENTS.md`.
- Any agent must consult the ledger before repeating a prior validation. A new chat/model/agent is never by itself a reason to revalidate.
- Revalidation is allowed only for changed inputs/version/hash, contradictory new evidence, inadequate provenance for a current high-risk decision, or proof that the original method was unsound.
- When a prior result is too poorly documented to reuse safely, it may be revalidated once, but the revalidation must record exact claim, input identity/hash/version, method/script/parameters, offsets/ranges/count units, observed result, status, and reproducible artifact/report/commit path.

### Canonical inline-validation redesign

- Added `docs/INLINE_VALIDATION_POLICY.md` as the normative project-level policy for all future T5K inline mapping.
- Added `docs/RUNTIME_TEST_RESULTS.md` to preserve the actual Eden Android observations separately from safety conclusions.
- Promoted the key rule to `AGENTS.md`: `unique exact match` is candidate-discovery evidence only and can never by itself authorize a release patch.
- Changed the validator target from the old 5,519 exact-unique rodata subset to the full 17,103-record T5K inline corpus.
- Defined mandatory safety axes: game-code validity, PC↔Switch structural homology, independently established Switch field/boundary structure, conflict/binary-risk rejection, and simulated post-patch offline re-validation.
- Adopted piecewise collinearity/anchor analysis as the preferred global homology model; do not assume one global LIS or perfect ordering across the whole binary.
- Prohibited automatic translation shortening merely to fit an unproven Switch field width. Uncertain candidates are HOLD until field structure is established.
- Defined ANCHOR / SAFE-A / SAFE-B / PROBABLE / HOLD / REJECT classes and made hard gates primary over weighted confidence scoring.
- Restricted binary split / delta debugging to isolating reproducible failures. A passing split is never evidence that every member is safe.

### Eden Android test packaging

- Added `docs/EDEN_ANDROID_TEST_GUIDE.md`.
- Recorded that normal Android file-manager access to Eden's internal folder cannot be assumed.
- Development ZIP instructions use Eden's per-game Add-ons importer with an extracted mod root containing `exefs/` and `romfs/`.

### Distribution strategy

- Final user-facing patcher target is an Android APK for Eden Android.
- Standard inputs remain a complete extracted Switch v1.1.3 dump plus `Taiko5DX_Korean_Patcher_v1.02.zip`.
- The APK must reuse the same core patch engine and use Android SAF/user-granted locations.
- It must not embed copyrighted game files, patch payloads/fonts, keys, XCI/NSP/NCA, or full dumps.

### Integrated port expansion

- Added direct PE resource extraction for `dinput8.dll` `RT_RCDATA/101` and exact T5K parser.
- Canonical counts: 10,036 mappings, 17,103 inline records, 56 pointer records, 11 runtime descriptors.
- Historical exact-unique selector gives 5,519 rodata patterns covering 5,521 PC records; it remains regression/reference only.
- Integrated 207 directly reusable PC Korean RomFS payload files; `CMENU/CWTDAT_JP.TR5` is intentionally excluded.

### Still pending

- Run M1B and M1C independently, then 10/100-record MVI aggregation if they pass.
- Exact Steam build-9163702 PC EXE for optional PC-binary context/homology work.
- Full 17,103-record inline correspondence/validation pipeline after Phase 0.
- 7,494 -> 10,036 Switch mapping table relocation/reference/count patches.
- Switch correspondence for the 56 pointer records.
- `runtime_byte_validation`, font threshold, `ui_width_1~4`, `description_font_1~2` counterparts as evidence requires.
- Switch-native `CWTDAT_JP.TR5` reconstruction.
