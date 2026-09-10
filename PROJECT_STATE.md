# PROJECT_STATE

Last updated: 2026-09-11 (KST)

This is the canonical resume point. Before inline/crash/UI work, read it with `docs/VALIDATION_LEDGER.md`, `PATCH_MAP.md`, `docs/INLINE_VALIDATION_POLICY.md`, `docs/PHASE0_FAILURE_MODE_PLAN.md`, `docs/RUNTIME_TEST_RESULTS.md`, and `docs/POST_D5519_ANALYSIS.md`.

## 1. Goal

Port `Taiko5DX_Korean_Patcher_v1.02` to Nintendo Switch **TAIKO RISHHIDEN V DX v1.1.3**, with Eden Android as the primary target. Final user-facing frontend remains an Android APK reusing the stabilized core builder.

## 2. Canonical Eden IPS coordinate rule

Eden/Yuzu-style NSO IPS patching operates on:

```text
0x000000..0x0000FF  NSOHeader (0x100 bytes)
0x000100..          decompressed mapped NSO image
```

Therefore:

```text
emitted Eden IPS offset = mapped flat NSO offset + 0x100
```

Example: mapped page-mapper target `0x44650C` -> emitted IPS `0x44660C`.

Every IPS-bearing build through P0N v0.2f omitted this shift and patched `0x100` bytes early. Their runtime observations remain historical facts but cannot establish candidate-level safety/failure.

## 3. Corrected runtime evidence

### P0N2 v0.2g

5,519 true no-op inline records + corrected page mapper + RomFS/font baseline.

Result: **PASS** — boot, Korean title, input, and main menu.

### M1A v0.2h

Exactly one real inline (`R489`, `シナリオを選んでください` -> `시나리오를 선택하세요`).

Result: **PASS** through scenario/protagonist-selection flow.

### D5519 v0.2k

Historical 5,519 real replacements, unchanged payload bytes from old v0.2a, but every IPS address corrected by `+0x100`.

Result: **PASS on tested early-game route** — title, menu, scenario selection/description, protagonist selection, and entry into normal gameplay without freeze/forced exit.

This is strong evidence that the pre-P0N2 freeze diagnosis was dominated by the missing `+0x100` coordinate shift. It does not certify every historical inline candidate for every late-game path.

## 4. Post-D5519 UI diagnosis

The corrected full-inline build exposes residual quality/coverage issues rather than the former immediate freeze.

Observed classes:

- Korean main names/text: broadly working.
- Small auxiliary yomi/furigana line: garbled on name UIs.
- Repeated short UI tokens: some remain Japanese (`はい`, date/currency suffixes, `城`).
- Some repeated place names such as `清洲` remain Japanese because the historical unique-only selector rejected them.

Detailed evidence is in `docs/POST_D5519_ANALYSIS.md`.

## 5. Yomi policy and Y0 diagnostic

For the Korean Switch port, the visible reading line is unnecessary when the main name is already Korean.

Policy:

- keep Korean main-name display;
- preserve original Japanese halfwidth-kana yomi internally for sort/comparison/input compatibility;
- suppress only the visible auxiliary yomi line.

Static evidence against the fixed D5519 set:

- historical real inline records: 5,519;
- halfwidth-kana/NUL yomi-like fields: **2,099**;
- retained non-yomi inline records: **3,420**.

Shared name/yomi render routine: mapped `0x45B0F8`.

Eight callers explicitly enable the auxiliary line with `mov w6,#1` (`26 00 80 52`) and branch to that routine:

```text
0x2A0ABC
0x2A565C
0x2A6F4C
0x2A7720
0x2A7FE4
0x2ADE5C
0x2BC1A0
0x2BD5C8
```

Diagnostic Y0 changes those sites to `mov w6,wzr` (`E6 03 1F 2A`) and excludes the 2,099 yomi translations while retaining the original internal yomi bytes.

Prepared artifact:

- `Y0_Taiko5DX_KR_DBG_NOYOMI_v0.2l.zip`
- SHA-256 `ae67b2bdece0e261239a3a505ad018761904c25124f0857cf0a917f9a4a6c869`
- final IPS records: 3,429 = page mapper 1 + non-yomi historical inline 3,420 + yomi-callsite edits 8.

Reproducible builder: `builder/build_y0_noyomi.py`.

**Immediate runtime action:** test Y0 alone and confirm Korean main names remain, the garbled small yomi line disappears, and navigation remains stable.

## 6. Repeated short-string recovery: new evidence

The old selector rejects a pattern if the raw byte sequence occurs more than once anywhere, so short strings are falsely rejected when their bytes appear inside longer prose.

Strong object-level cases already identified:

- `はい` -> `예`: raw 7 rodata matches, but exactly one standalone NUL-delimited object at mapped `0x6A15A5`, referenced from pointer table `0x58D0D0`; adjacent object is `いいえ` at `0x6A65B2`, already translated to `아니오`.
- pooled date suffix objects: `年` `0x69785A`, `月` `0x68925A`, `日` `0x6A3CC6`; pointer table `0x59C730..0x59C768` references them consecutively. Multiple PC records agree on `년/월/일`.
- pooled `城`: standalone object mapped `0x6A15DC`, multiple pointer references; both PC `城` records agree on `성`.
- `清洲`: two T5K padded records with identical replacement `기요스`; exactly two corresponding Switch padded name fields at `0x6AE269` and `0x6AEFE9`, both in fixed-stride place-name/yomi tables.

Reproducible analyzer: `builder/repeated_token_probe.py`.

New rule: recover **Switch string objects**, not every raw substring occurrence. Require replacement agreement plus independent object-boundary/pointer/stride evidence.

Currency `貫/文` needs a separate pass because several visible strings embed units inside longer format strings; no global raw replacement.

## 7. Fixed target identity

- Title ID: `0100346017304000`
- Switch version: `1.1.3`
- `main` Build ID: `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed `main`: 5,287,359 bytes
- compressed `main` SHA-256: `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- mapped flat size: `10,617,904 / 0xA20430`

Segments:

- text `0x000000 + 0x58CE60`
- rodata `0x58D000 + 0x432018`
- data `0x9C0000 + 0x60430`

## 8. PC patch source facts

PC patch ZIP SHA-256:
`df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`

T5K121R:

- mappings 10,036;
- original mappings 7,494 (`0x1D46`);
- Korean additions 2,542;
- inline records 17,103;
- pointer records 56;
- runtime descriptors 11.

`dinput8.dll` SHA-256:
`ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`

`RT_RCDATA/101` SHA-256:
`5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`

The currently supplied Drive `PC_Original/Taiko5DX.exe` is not the exact T5K target and is barred from PC-RVA neighborhood/XREF evidence. Exact target: Steam build 9163702, 18,685,960 bytes, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`.

## 9. Font / encoding / conversion status

- Switch original font == Steam original: 13,108,628 bytes / 50 pages / SHA-256 `9c886848...a0083e`.
- Korean patched font: 16,779,036 bytes / 64 pages / SHA-256 `c82d80da...66932`.
- Korean uses custom game 1/2-byte code space; lead bytes `EB~F8` map to pages 49~62.

Switch functions:

- `0x430350`: UTF-16 -> game code;
- `0x4305D0`: game code -> UTF-16;
- `0x446310`: segmentation/count;
- `0x446420`: GetFontTexIndex.

Both conversion loops still use 7,494 entries. Miss fallbacks are defined (`0x81A1` and `U+25A0`). Expansion to 10,036 remains functionally required for full input/conversion compatibility, but D5519 proves it is not required merely to survive the tested early-game rendered-text route.

## 10. Historical inline statistics

```text
PC records total                 17,103
unique original patterns          8,713
no Switch match                     186
multiple Switch matches            2,476
unique match outside rodata          528
candidate rodata patterns           5,523
overlap-skipped                         4
historical selected patterns       5,519
PC records covered                  5,521
```

These are reference counts, not release-safety certification.

Reproduced structural stats:

- record-level unique pairs 6,053;
- global LIS 3,524;
- outside LIS 2,529;
- top adjacent monotonic runs 1,844 / 1,074 / 978 / 78;
- original contains NUL and replacement none: 12,347 records;
- original has no NUL: 4,747 records.

External `430` and `8,981/1,242` figures remain non-canonical pending exact-definition reproduction.

## 11. Validator role after D5519

The full 17,103-record validator remains required for release audit/recovery, but its role changed:

- no longer the primary explanation for the old immediate freeze;
- now used to recover missed repeated/string-pool/fixed-field mappings safely and audit late-game structural risk;
- unique exact match remains candidate-discovery evidence only;
- runtime pass remains route-sanity evidence only.

Required principles still include game encoding validation, all candidate locations, Switch-side field/object structure, relocation/XREF/pointer/stride evidence, tail-merge/conflict checks, local homology, simulated patching, offline revalidation, and emitted-IPS round-trip.

## 12. Remaining port work

Priority order:

1. runtime-test Y0;
2. recover high-confidence repeated UI objects (`はい`, pooled date suffixes, pooled `城`, both `清洲` fields);
3. map currency format strings (`貫/文`) structurally rather than globally;
4. expand 7,494 -> 10,036 conversion mapping safely;
5. map remaining PC runtime descriptors / 56 pointer records as evidence requires;
6. reconstruct Switch-native `CWTDAT_JP.TR5` changes;
7. full 17,103 release validator and broad runtime route.

## 13. Eden Android installation constraint

Do not assume normal file-manager access to Eden internal storage. Use Eden's per-game Add-ons importer with an extracted mod root containing `exefs/` and/or `romfs/`.

## 14. Final distribution target

Android APK remains the final frontend. It accepts the user's complete extracted Switch v1.1.3 dump and PC patch ZIP, reuses the corrected core patch engine, and emits an Eden-ready mod through Android SAF/user-granted locations. It must not embed copyrighted game files, patch payloads/fonts, keys, XCI/NSP/NCA, or full dumps.