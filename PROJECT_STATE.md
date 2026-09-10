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

## 3. Runtime evidence: what remains valid and what is superseded

Observed facts remain real:

- add-on OFF -> game boots/runs normally;
- v0.2b NO-INLINE -> boots and displays Korean title `태합입지전 V DX`;
- old integrated v0.2a -> freeze;
- v0.2c -> failure;
- old A -> freeze;
- old B -> title then crash after input;
- **P0N v0.2f -> freeze**.

However, v0.2a/v0.2b/v0.2c/A/B/P0N all used the wrong no-shift IPS convention. Therefore:

- they do **not** prove that the historical inline candidates themselves were unsafe;
- A/B do **not** prove multiple semantic faults;
- v0.2b does **not** prove that the intended page mapper at mapped `0x44650C` executed, because its IPS record targeted mapped `0x44640C`;
- P0N v0.2f was **not a true no-op in Eden** even though local flat-image round-trip checks said it was.

The old runtime interpretations are superseded, not erased. See the validation ledger and runtime-results document.

## 4. Immediate runtime control: P0N2 v0.2g

The next required test is **P0N2**:

- 207 RomFS replacements;
- Korean 64-page font;
- page-mapper record emitted at corrected IPS offset `0x44660C`;
- 5,519 historical inline locations written as true no-ops;
- every emitted IPS record uses mapped offset `+0x100`;
- total IPS records: 5,520.

Interpretation:

- **P0N2 boots** -> the corrected large classic-IPS path is viable; the old P0N freeze is explained by the coordinate bug. Then continue with corrected MVI tests and structural validation.
- **P0N2 fails** -> isolate corrected page mapper versus corrected 5,519 no-op-record application before semantic validator work.

Do not rerun old P0N v0.2f.

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

The page-mapper rewrite bytes for mapped `0x44650C..0x446534` are statically verified. Correct runtime application still needs P0N2-or-later confirmation because prior builds emitted the wrong IPS coordinate.

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

Run **P0N2 v0.2g only**, with all older diagnostic Korean mods disabled. Record whether it:

1. boots;
2. displays title;
3. accepts button input and reaches the next menu.

Only after that result decide whether to proceed to corrected MVI tests or isolate corrected page mapper/no-op application.

## 15. Final distribution target

Android APK remains the final frontend. It accepts the user's complete extracted Switch v1.1.3 dump and PC patch ZIP, reuses the same corrected core patch engine, and emits an Eden-ready mod through Android SAF/user-granted locations. It must not embed game binaries, patch payloads/fonts, keys, XCI/NSP/NCA, or full dumps.
