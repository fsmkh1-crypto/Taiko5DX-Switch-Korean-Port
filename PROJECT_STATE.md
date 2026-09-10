# PROJECT_STATE

Last updated: 2026-09-11 (KST)

This is the canonical resume point. Before inline/crash/UI work, read it with `docs/VALIDATION_LEDGER.md`, `PATCH_MAP.md`, `docs/INLINE_VALIDATION_POLICY.md`, `docs/PHASE0_FAILURE_MODE_PLAN.md`, `docs/RUNTIME_TEST_RESULTS.md`, and `docs/POST_D5519_ANALYSIS.md`.

## 1. Goal

Port `Taiko5DX_Korean_Patcher_v1.02` to Nintendo Switch **TAIKO RISHHIDEN V DX v1.1.3**, with Eden Android as the primary target. Final user-facing frontend remains an Android APK reusing the stabilized core builder.

## 2. Canonical Eden IPS coordinate rule

Eden/Yuzu NSO IPS patching operates on `0x100-byte NSOHeader + decompressed mapped NSO image`.

```text
emitted Eden IPS offset = mapped flat NSO offset + 0x100
```

Example: mapped page mapper `0x44650C` -> Eden IPS `0x44660C`.

All IPS-bearing builds through P0N v0.2f omitted this shift and patched `0x100` early. Their crashes remain historical observations but cannot establish candidate-level safety/failure.

## 3. Corrected runtime baseline

- **P0N2 v0.2g**: corrected mapper + 5,519 true no-op records -> PASS through title/input/main menu.
- **M1A v0.2h**: one corrected real inline `R489` -> PASS through scenario/protagonist flow.
- **D5519 v0.2k**: historical 5,519 real replacements with only the IPS coordinates corrected -> PASS through title, menu, scenario flow, protagonist selection, and normal early gameplay without freeze/forced exit.

D5519 strongly attributes the former immediate freezes to the missing `+0x100` build-layer defect. It does not certify every historical inline record for every late-game path.

## 4. Current visible issues

D5519/Y0 runtime screenshots establish several independent residual classes:

1. garbled auxiliary yomi/furigana rows on protagonist-selection and dialogue name UIs;
2. repeated short Japanese UI objects such as `はい`, date suffixes, `城`, and repeated `清洲` fields missed by unique-only matching;
3. compact/fixed-field Korean name rendering defects, especially `마츠다이라 모토야스` displaying without `츠` on a nameplate;
4. user-observed odd shapes around `케/자` in `나야 스케자에몬`;
5. currency format strings containing `貫/文`, which require format-object analysis rather than global replacement.

These are quality/coverage/runtime-behavior issues, not a recurrence of the old immediate freeze.

## 5. Yomi result: Y0 did not hide the observed rows

D5519 classification found 2,099 historical inline records whose original non-NUL bytes are entirely halfwidth kana `0xA1..0xDF`, leaving 3,420 non-yomi records.

Eight direct call sites set `mov w6,#1` before calls to shared name/yomi routine `0x45B0F8`:

```text
0x2A0ABC  0x2A565C  0x2A6F4C  0x2A7720
0x2A7FE4  0x2ADE5C  0x2BC1A0  0x2BD5C8
```

`Y0 v0.2l` restored the 2,099 internal yomi records to original Switch bytes and changed those eight enables to zero. Runtime remained stable, but the garbled small reading rows in protagonist selection and dialogue nameplates **still appeared**.

Therefore:

- the eight call-site mapping remains a valid static finding;
- the hypothesis that those eight sites alone control the observed two rows is disproved/incomplete;
- do not repeat the same eight-site-only suppression attempt;
- preserve internal Japanese yomi for sort/comparison compatibility while the actual visible-row path is traced later.

## 6. New critical font-width finding

The missing `츠` in `마츠다이라 모토야스` is not a translation omission and not corrupt source glyph art.

PC T5K records for `松平元康` use a 16-byte compact replacement:

```text
B2 BD AA F3 6B EE 93 20 EF 90 F5 E2 F2 7E F1 B8
```

Semantics:

```text
B2 = 마  (single-byte compact glyph on Korean font page 63)
BD = 츠  (single-byte compact glyph on Korean font page 63)
AA = 다  (single-byte compact glyph on Korean font page 63)
F36B = 이
EE93 = 라
20   = space
EF90 F5E2 F27E F1B8 = 모토야스
```

The exact Korean G1T atlas contains correct page-63 `마/츠/다` glyphs. The normal two-byte `케` (`F568`) and `자` (`F379`) glyph cells are also correct. Therefore the visible defects are runtime classification/layout/render behavior, not bad font artwork.

The PC runtime descriptor `font_page_limit` changes a threshold from `0xFF` to `0xA0`. Semantically, bytes above `0xA0` are moved from the single-byte halfwidth path to the alternate/full-width path. This explains why the compact A1+ Korean glyph system needs a runtime patch in addition to the font asset.

## 7. W0 diagnostic — current immediate test

Six Switch v1.1.3 width/layout sites implement or inline the corresponding `code < 0x100` halfwidth decision:

```text
0x445EAC
0x445FC8
0x446198
0x4472E8
0x447344
0x447C44
```

At all six sites:

```text
old: 1F 01 04 71   cmp w8,#0x100
new: 1F 85 02 71   cmp w8,#0xA1
```

A separate `cmp #0x100` in conversion logic around `0x4304F8` is unrelated and must not be patched.

Prepared diagnostic:

- `W0_Taiko5DX_KR_DBG_FONTWIDTH_A1_v0.2m.zip`
- SHA-256 `e453d5958793748ebf841f295ef4005a9a612fdbe643439fe9c2a2c0183ea2ad`
- basis: D5519 v0.2k;
- D5519 5,520 IPS records retained;
- six threshold records added;
- final IPS record count 5,526;
- all six original-instruction guards and emitted-IPS round-trip checks pass.

Reproducible builder: `builder/build_w0_fontwidth.py`.

**Immediate action:** enable W0 alone, reach the Matsudaira Motoyasu nameplate and check whether `마츠다이라 모토야스` now includes `츠`. Also check `나야 스케자에몬` for `케/자` appearance and inspect general spacing/halfwidth regressions.

## 8. Repeated short-object recovery already established

Use actual Switch string objects, not every raw substring occurrence.

High-confidence targets:

- `はい` -> `예`: standalone object `0x6A15A5`, pointer ref `0x58D0D0`;
- `年/月/日` -> `년/월/일`: pooled objects `0x69785A / 0x68925A / 0x6A3CC6`, with consecutive pointer-table registration around `0x59C730..0x59C768`;
- `城` -> `성`: pooled standalone object `0x6A15DC`;
- `清洲` -> `기요스`: two fixed-field objects `0x6AE269`, `0x6AEFE9` with matching PC replacements.

Currency `貫/文` remains separate because many uses occur inside longer format strings.

Reproducible analyzer: `builder/repeated_token_probe.py`.

## 9. Fixed target identity

- Title ID `0100346017304000`
- Switch version `1.1.3`
- `main` Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed main size 5,287,359 bytes
- compressed main SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- mapped flat size `10,617,904 / 0xA20430`
- text `0x000000 + 0x58CE60`
- rodata `0x58D000 + 0x432018`
- data `0x9C0000 + 0x60430`

## 10. PC patch source facts

PC patch ZIP SHA-256 `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`.

T5K121R:

- mapping entries 10,036;
- original mapping entries 7,494 (`0x1D46`);
- Korean additions 2,542;
- inline records 17,103;
- pointer records 56;
- runtime descriptors 11.

`dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`.

The Drive `PC_Original/Taiko5DX.exe` is not the exact T5K target and must not be used for PC binary-context evidence. Exact target is Steam build 9163702, size 18,685,960, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`.

## 11. Encoding/font/conversion status

- Switch original font == Steam original: 13,108,628 bytes / 50 pages / SHA-256 `9c886848...a0083e`.
- Korean font: 16,779,036 bytes / 64 pages / SHA-256 `c82d80da...66932`.
- Normal Korean uses the custom two-byte game code; lead bytes `EB~F8` map to pages 49~62.
- PC patch additionally repurposes page-63 single-byte codes above `0xA0` for compact Korean glyphs in tight fixed fields.

Switch functions:

- `0x430350`: UTF-16 -> game code;
- `0x4305D0`: game code -> UTF-16;
- `0x446310`: segmentation/count;
- `0x446420`: GetFontTexIndex.

Both conversion loops still search 7,494 entries; misses are defined (`0x81A1`, `U+25A0`). Expansion to 10,036 remains needed for full input/conversion behavior but D5519 proves it is not required merely for survival of the tested rendered-text route.

## 12. Validator role after D5519

The full 17,103-record validator remains a release-audit/recovery mechanism, not the primary explanation for the old freeze. It must recover missed repeated/string-pool/fixed-field mappings safely and audit late-game structural risk. `unique exact match` remains discovery evidence only; runtime pass remains route evidence only.

## 13. Priority after W0 result

1. evaluate W0 compact-font result and regressions;
2. if W0 fixes compact glyphs, promote the six-site threshold patch into the integrated builder;
3. trace the actual auxiliary-yomi draw path later; do not repeat Y0's eight-site-only attempt;
4. recover high-confidence repeated UI objects (`はい`, date suffixes, `城`, both `清洲` fields);
5. structurally map currency format strings (`貫/文`);
6. expand 7,494 -> 10,036 conversion mapping;
7. map remaining runtime descriptors / 56 pointer records / Switch-native CWTDAT changes;
8. full release validator and broad runtime route.

## 14. Eden Android / final distribution

Development builds must be installed through Eden's per-game Add-ons importer; direct normal file-manager access to Eden internal storage is not assumed.

Final frontend remains an Android APK using SAF. It accepts the user's complete extracted Switch v1.1.3 dump and PC patch ZIP and emits an Eden-ready mod without embedding copyrighted game binaries, patch payloads/fonts, keys, or dumps.