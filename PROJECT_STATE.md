# PROJECT_STATE

Last updated: 2026-09-10 (KST)

This file is the canonical resume point for the project. Before inline/crash work, read it together with `docs/VALIDATION_LEDGER.md`, `PATCH_MAP.md`, `docs/INLINE_VALIDATION_POLICY.md`, `docs/PHASE0_FAILURE_MODE_PLAN.md`, and `docs/RUNTIME_TEST_RESULTS.md`.

## 1. Goal

Port the existing PC Korean patch `Taiko5DX_Korean_Patcher_v1.02` to Nintendo Switch **TAIKO RISHHIDEN V DX v1.1.3**, with Eden Android as the primary development/test target.

Primary output remains one integrated Eden mod. Final end-user frontend remains Android APK using the same stabilized core patch logic.

## 2. Current decision point: Phase 0 before full validator

The old `5,519 exact-unique rodata` inline selector is invalid as a safety rule, but the observed failures do not yet prove that every failure is candidate-specific.

Before building the full 17,103-record semantic validator, follow `docs/PHASE0_FAILURE_MODE_PLAN.md` to distinguish:

- bad/wrong inline candidates and field-structure violations; from
- IPS/build-loader/runtime prerequisites that can fail even for semantically correct candidates.

Current first runtime control is **P0N**:

- same known-good NO-INLINE baseline: 207 RomFS replacements + Korean font + page mapper;
- plus 5,519 historical inline IPS records that are true **no-ops** (each writes the original Switch bytes back to itself);
- 5,520 IPS records total including page mapper;
- generator reparses the emitted IPS and verifies every no-op record against the flat image.

Interpretation:

- P0N boots like v0.2b -> large classic-IPS record count/packaging/application is not the current cause; proceed to MVI content tests;
- P0N fails -> stop semantic-validator implementation and investigate the IPS/build-loader/application layer first.

## 3. Fixed Switch target

- Title ID: `0100346017304000`
- Switch version: `1.1.3`
- `main` Build ID: `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed `main` observed size: 5,287,359 bytes
- compressed `main` SHA-256 used by Phase 0: `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- mapped flat end: `0xA20430` (10,617,904 bytes)

NSO segments:

- text: `0x000000 + 0x58CE60`
- rodata: `0x58D000 + 0x432018`
- data: `0x9C0000 + 0x60430`

## 4. Current source material and identity warning

Available Phase-0 inputs were located in the project Drive:

- Switch `main`;
- Switch original `FONT_JPN.G1T`;
- Switch `CWTDAT_JP/CN/TW.TR5`;
- `Taiko5DX_Korean_Patcher_v1.02.zip`;
- a `PC_Original/Taiko5DX.exe`.

The supplied PC EXE is **not the exact executable targeted by T5K121R** and must not be used for PC-RVA neighborhood/homology evidence.

Supplied Drive EXE:

- version resource: `1.2.1.0`
- size: `18,479,304`
- SHA-256: `22e1cd1afbd7d87a58b3560e7549f7e0fb462c723b4db9e1b1e747babb765ef6`

Exact PC patch target from README/T5K:

- Steam `1.2.1.0`, build `9163702`
- size: `18,685,960`
- SHA-256: `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`

Obtain that exact EXE before any validation that requires real PC binary context. T5K record RVAs/order and embedded original/replacement bytes remain usable without it.

## 5. PC Korean patch structure

PC patch ZIP SHA-256 used by Phase 0:
`df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`

Embedded `patch_payload.zip`: 209 items = 208 game replacements + `dinput8.dll`.

- 169 `EVENT/*.TS5`
- 28 G1T
- 10 TR5
- 1 `TAI5MSG_JP.DAT`
- 1 `dinput8.dll`

`dinput8.dll` SHA-256:
`ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`

`RT_RCDATA/101` SHA-256:
`5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`

T5K121R:

- mappings: 10,036
- original mappings: 7,494 (`0x1D46`)
- Korean additions: 2,542
- inline records: 17,103
- pointer records: 56
- runtime descriptors: 11

## 6. Font / encoding / page mapper

Switch original `FONT/FONT_JPN.G1T` and Steam original font are byte-identical.

- original: 13,108,628 bytes / 50 pages / SHA-256 `9c886848c31c31d09aeeed0ac5c44b909d561220110ca04da0f7fa32d3a0083e`
- Korean patched: 16,779,036 bytes / 64 pages / SHA-256 `c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932`

Korean uses the game custom 1/2-byte code space. Korean lead bytes `EB~F8` map to font pages 49~62.

Switch functions:

- `0x430350`: UTF-16 -> game code
- `0x4305D0`: game code -> UTF-16
- `0x446310`: character segmentation/count
- `0x446420`: `GetFontTexIndex`

Implemented page mapper rewrite at `0x44650C..0x446534` adds `EB~F8 -> pages 49~62` and is proven through Korean-title rendering in NO-INLINE runtime testing.

## 7. Mapping-loop Phase-0 result

Both Switch conversion routines still use the original 7,494-entry limit:

- `0x4303AC` in `0x430350` path: `0x1D46`
- `0x430624` in `0x4305D0` path: `0x1D46`

Direct ARM64 disassembly of the fixed flat image shows defined table-miss fallbacks:

- UTF-16 -> game-code miss -> fallback `0x81A1` bytes;
- game-code -> UTF-16 miss -> `U+25A0`.

Therefore 7,494 -> 10,036 expansion is a real functional requirement but **not yet proven as the direct freeze cause**. It may still break search/sort/compare/save/conversion semantics and remains a priority runtime prerequisite.

## 8. CWTDAT platform exception

Never replace Switch `CMENU/CWTDAT_JP.TR5` wholesale with the PC file.

- Switch JP: 480,382 bytes
- PC original/patched: 548,530 bytes

Reconstruct only validated Korean changes onto the Switch-native structure later.

## 9. Inline corpus and reverified historical selector

Reverified fixed-input counts:

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

The 5,519 set is historical/regression data only, never a SAFE set.

## 10. Reverified structural statistics

The earlier external collinearity observation was reproduced with explicit units:

Record-level unique-match pairs:

- 6,053 record pairs
- global LIS length 3,524
- 2,529 record pairs outside that LIS
- top adjacent monotonic runs: 1,844 / 1,074 / 978 / 78

Pattern-level equivalent:

- 6,051 unique pattern pairs
- LIS length 3,522

This confirms strong large-block order preservation exists, but global LIS is reference evidence only. Final homology uses piecewise/local blocks plus structural evidence.

NUL statistics reverified:

- original contains NUL and replacement contains none: 12,347 records
- original contains no NUL: 4,747 records

Do not interpret those counts as automatic run-on failures; Switch field type/width remains authoritative.

External `430` termination and `8,981/1,242 >=5-match` counts were **not reproduced under the stated definitions** and remain non-canonical. See ledger V011C/V011D.

## 11. Runtime evidence already established

Recorded in `docs/RUNTIME_TEST_RESULTS.md`:

- add-on OFF -> normal boot/run;
- v0.2b NO-INLINE -> boots and renders `태합입지전 V DX`;
- integrated 5,519 inline set -> freeze;
- v0.2c one-record removal -> still fails;
- address-half A -> freeze;
- address-half B -> title, then button input -> forced exit/crash.

Do not overstate this as "any inline set fails".

## 12. Full validator architecture after Phase 0

If Phase 0 clears the architecture, build the validator for all 17,103 records, not just the old 5,519.

Mandatory principles:

- game-specific encoding validity;
- all Switch candidate positions, not unique-only;
- `.text` ordinary-inline exclusion;
- `.data` excluded from auto-patching but retained as an analysis/evidence source;
- relocation/reference evidence as strong evidence, not a universal requirement;
- rodata-wide tail-merge/subsequence/conflict checks;
- piecewise/local PC-RVA <-> Switch-offset blocks using order and distance consistency;
- collinearity is not the sole mandatory route to SAFE;
- independent Switch field classification and boundary/stride semantics;
- control-code whitelist derived independently and frozen before classification;
- shuffled/negative controls when choosing `info_len` thresholds;
- simulated patching, field-type-specific set invariants, adjacent-patch interaction checks;
- final IPS reparse and diff against the intended patch plan/image;
- ANCHOR / SAFE-A / SAFE-B / PROBABLE / HOLD / REJECT hard-gate classification;
- no automatic translation shortening.

Runtime success remains sanity evidence only.

## 13. Pointer/runtime work remaining

- safe 7,494 -> 10,036 mapping relocation/reference/count patches;
- `runtime_byte_validation` counterpart;
- `font_page_limit` counterpart;
- 56 pointer-record Switch mappings;
- `description_font_1~2`;
- `ui_width_1~4`;
- Switch-native CWTDAT reconstruction.

Runtime descriptors should be investigated by actual semantics/reachability; do not assume all are prerequisites for the validator.

## 14. Eden Android constraint

Do not assume normal file-manager access to Eden internal Android storage.

Development mod installation:

1. extract to accessible Android storage;
2. Eden per-game Add-ons;
3. `+ Install` -> `Mods and cheats`;
4. select the mod root containing `exefs/` and/or `romfs/`;
5. enable only the intended diagnostic build.

## 15. Immediate next actions

1. Run **P0N** in Eden Android and record the result.
2. If P0N passes, prepare independently selected MVI real-inline tests rather than arbitrary address splits.
3. Obtain the exact Steam build-9163702 PC EXE before PC binary-context homology work.
4. Continue Phase-0 runtime-descriptor/reachability analysis while avoiding claims not supported by evidence.
5. Only after Phase 0 clears the architecture, implement the full 17,103-record validator.
6. Update `docs/VALIDATION_LEDGER.md` with every new/reverified/invalidated fact so later agents do not repeat checks.

## 16. Final distribution target

Primary end-user frontend remains Android APK. It will accept the user's complete extracted Switch v1.1.3 dump and PC patch ZIP, reuse the same core patch engine, and emit an Eden-ready mod via Android SAF/user-granted locations. It must not embed game binaries, patch payloads/fonts, keys, XCI/NSP/NCA, or full dumps.
