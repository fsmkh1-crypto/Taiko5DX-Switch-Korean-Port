# PROJECT_STATE

Last updated: 2026-09-10 (KST)

This file is the canonical resume point for the project. Before inline/crash work, read it together with `docs/VALIDATION_LEDGER.md`, `PATCH_MAP.md`, `docs/INLINE_VALIDATION_POLICY.md`, `docs/PHASE0_FAILURE_MODE_PLAN.md`, and `docs/RUNTIME_TEST_RESULTS.md`.

## 1. Goal

Port `Taiko5DX_Korean_Patcher_v1.02` to Nintendo Switch **TAIKO RISHHIDEN V DX v1.1.3**, with Eden Android as the primary test target. Final user-facing frontend remains an Android APK that reuses the stabilized core builder.

## 2. Critical current finding: Eden IPS offsets require +0x100

This is now a canonical build-layer fact.

Eden/Yuzu-style NSO patching applies classic IPS to an artificial image consisting of:

```text
0x000000..0x0000FF  NSOHeader (0x100 bytes)
0x000100..          decompressed mapped NSO image
```

Therefore:

```text
emitted IPS offset = mapped flat NSO offset + 0x100
```

Example:

- mapped page-mapper target: `0x44650C`
- correct Eden IPS offset: `0x44660C`

All development IPS builds through **P0N v0.2f** emitted mapped offsets directly without the required shift. The core builder has now been corrected so `PatchPlan` keeps mapped offsets while `write_ips()` adds `+0x100` only during serialization.

This discovery changes interpretation of every earlier IPS-bearing runtime test.

## 3. Runtime evidence: corrected controls are working

Observed historical facts remain real:

- add-on OFF -> game boots/runs normally;
- v0.2b NO-INLINE -> boots and displays Korean title `태합입지전 V DX`;
- old integrated v0.2a -> freeze;
- v0.2c -> failure;
- old A -> freeze;
- old B -> title then crash after input;
- P0N v0.2f -> freeze.

However, v0.2a/v0.2b/v0.2c/A/B/P0N all used the wrong no-shift IPS convention. Therefore they cannot establish candidate-level safety/failure.

The corrected control **P0N2 v0.2g** uses `mapped+0x100` for every IPS record and contains 5,519 true no-op inline records plus the corrected page mapper. Runtime result:

- boots successfully;
- reaches Korean title;
- accepts button input;
- reaches the next main menu.

The first real-inline MVI build **M1A v0.2h** also passes:

- exactly one real inline replacement, T5K `R489`;
- `シナリオを選んでください` -> `시나리오를 선택하세요`;
- mapped `0x69B6A1` -> Eden IPS `0x69B7A1`;
- user progressed through scenario selection/description and protagonist selection without freeze or forced exit.

Therefore the corrected classic-IPS path is viable and **at least one real corrected inline record can coexist with the baseline** on a substantial early-game route. This does not make the historical 5,519 replacement set SAFE.

## 4. Current Phase-0 step: independent one-record MVI controls

Phase 0 remains in Minimal Viable Inline testing. The purpose is to distinguish candidate-specific failures from a blanket runtime prerequisite failure before scaling up.

Completed:

- `P0N2 v0.2g`: corrected 5,519-no-op large-IPS control — PASS.
- `M1A v0.2h`: corrected single real inline `R489` — PASS.

Prepared next:

- **M1B v0.2i** — T5K `R674`, `主人公選択` -> `주인공선택`, mapped `0x682DA4`, Eden IPS `0x682EA4`.
- **M1C v0.2j** — T5K `R726`, `はじめから` -> `처음부터`, mapped `0x684140`, Eden IPS `0x684240`.

Each build contains only the corrected page mapper plus one real inline record, with the 207 RomFS replacements and Korean 64-page font baseline. Test them independently with every other Korean diagnostic mod disabled.

If M1B and M1C both pass, proceed to a corrected 10-record MVI aggregation. If one fails while the other passes, investigate the failing record/field rather than declaring a systemic failure.

## 5. Fixed Switch target

- Title ID: `0100346017304000`
- Switch version: `1.1.3`
- `main` Build ID: `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed `main` size: 5,287,359 bytes
- compressed `main` SHA-256: `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- mapped flat size/end: `10,617,904 / 0xA20430`

Segments:

- text: `0x000000 + 0x58CE60`
- rodata: `0x58D000 + 0x432018`
- data: `0x9C0000 + 0x60430`

## 6. PC patch source facts

PC patch ZIP SHA-256:
`df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`

Embedded payload: 209 items = 208 game-data replacements + `dinput8.dll`.

T5K121R canonical counts:

- mappings: 10,036
- original mappings: 7,494 (`0x1D46`)
- Korean additions: 2,542
- inline records: 17,103
- pointer records: 56
- runtime descriptors: 11

`dinput8.dll` SHA-256:
`ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`

`RT_RCDATA/101` SHA-256:
`5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`

## 7. PC EXE availability

The currently supplied Drive `PC_Original/Taiko5DX.exe` is not the exact T5K target and must not be used for PC binary-context evidence.

Supplied EXE:

- version resource `1.2.1.0`
- size `18,479,304`
- SHA-256 `22e1cd1afbd7d87a58b3560e7549f7e0fb462c723b4db9e1b1e747babb765ef6`

Exact T5K target:

- Steam build `9163702`
- size `18,685,960`
- SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`

The project can continue without it using T5K RVAs/order plus Switch-side evidence. Exact PC EXE is only required before claims that depend on real PC binary neighborhood/XREF context.

## 8. Font / encoding / page mapper

Switch original font and Steam original font are byte-identical.

- original: 13,108,628 bytes / 50 pages / SHA-256 `9c886848c31c31d09aeeed0ac5c44b909d561220110ca04da0f7fa32d3a0083e`
- Korean patched: 16,779,036 bytes / 64 pages / SHA-256 `c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932`

Korean uses the game's custom 1/2-byte code space. Korean lead bytes `EB~F8` map to pages 49~62.

Switch functions:

- `0x430350`: UTF-16 -> game code
- `0x4305D0`: game code -> UTF-16
- `0x446310`: segmentation/count
- `0x446420`: `GetFontTexIndex`

The page-mapper rewrite bytes for mapped `0x44650C..0x446534` are statically verified. P0N2/M1A confirm that the corrected mapper record coexists with the baseline through the tested early-game route; later coverage is still required for exhaustive behavior.

## 9. Mapping-loop result

Both conversion routines still use 7,494 entries:

- `0x4303AC` in UTF-16 -> game-code path;
- `0x430624` in game-code -> UTF-16 path.

Defined misses were observed:

- UTF-16 -> game code: fallback `0x81A1`;
- game code -> UTF-16: fallback `U+25A0`.

Thus 7,494 -> 10,036 expansion is functionally required but is not yet proven as the freeze cause.

## 10. Inline corpus and reproduced structural statistics

Historical selector counts are reproducible:

```text
PC records total                 17,103
unique original patterns          8,713
no Switch match                     186
multiple Switch matches            2,476
unique match outside rodata          528
candidate rodata patterns           5,523
overlap-skipped                         4
old selected unique patterns       5,519
PC records covered                  5,521
```

These counts are regression/reference facts only. `unique exact match` is not a release-safety proof.

Reproduced collinearity facts:

- record-level unique pairs: 6,053
- global LIS: 3,524
- outside LIS: 2,529
- top adjacent monotonic runs: 1,844 / 1,074 / 978 / 78
- pattern-level unique pairs: 6,051; LIS 3,522

Reproduced NUL statistic:

- original has NUL and replacement has none: 12,347 records
- original has no NUL: 4,747 records

External `430` and `8,981/1,242` figures remain non-canonical pending exact-definition reproduction.

## 11. Validator architecture after Phase 0

The final validator still targets all 17,103 records and retains these invariants:

- game-specific encoding validation;
- all Switch candidate locations, not unique-only;
- `.text` ordinary-inline exclusion;
- `.data` excluded from auto-patching but usable as an evidence source;
- Switch field structure determined independently of PC record length;
- relocation/XREF/pointer/stride evidence;
- rodata-wide tail-merge/subsequence/conflict detection;
- local/piecewise homology using order and distance consistency;
- collinearity as evidence, not the only route to SAFE;
- independent frozen control-code whitelist;
- shuffled negative controls for `info_len` thresholds;
- simulated patching and field-type-specific boundary/set invariants;
- emitted IPS reparse with `-0x100` coordinate conversion back to mapped image;
- ANCHOR / SAFE-A / SAFE-B / PROBABLE / HOLD / REJECT;
- no automatic translation shortening;
- runtime success is sanity evidence only.

## 12. Remaining runtime/port work

- run M1B/M1C independently, then 10/100-record MVI aggregation if they pass;
- safe 7,494 -> 10,036 mapping relocation/reference/count patches;
- `runtime_byte_validation` counterpart;
- `font_page_limit` counterpart;
- 56 pointer-record Switch mappings;
- `description_font_1~2`;
- `ui_width_1~4`;
- Switch-native `CWTDAT_JP.TR5` reconstruction.

## 13. Eden Android install constraint

Do not assume direct normal-file-manager access to Eden's internal Android folder. Use Eden's per-game Add-ons importer with an extracted mod root containing `exefs/` and/or `romfs/`.

## 14. Immediate next action

Run **M1B v0.2i** and **M1C v0.2j** separately, never simultaneously.

For M1B, reach protagonist selection and check that `主人公選択` becomes `주인공선택` while input remains normal.

For M1C, reach the screen that previously displayed `はじめから` and check that it becomes `처음부터` while navigation remains normal.

If both pass, build the corrected 10-record MVI set next.

## 15. Final distribution target

Android APK remains the final frontend. It accepts the user's complete extracted Switch v1.1.3 dump and PC patch ZIP, reuses the same corrected core patch engine, and emits an Eden-ready mod through Android SAF/user-granted locations. It must not embed game binaries, patch payloads/fonts, keys, XCI/NSP/NCA, or full dumps.
