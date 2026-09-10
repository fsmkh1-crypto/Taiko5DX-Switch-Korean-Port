# PROJECT_STATE

Last updated: 2026-09-10 (KST)

This file is the canonical resume point for this project. Read this before new analysis or implementation work.

## 1. Goal

Port the existing PC Korean patch `Taiko5DX_Korean_Patcher_v1.02` to Nintendo Switch **TAIKO RISHHIDEN V DX v1.1.3**, with Eden Android as the primary development/test target.

Development policy: build an integrated mod first, then fix failures found in real execution. Do not keep splitting the project into long P0/P1/P2 validation phases unless a specific failure requires isolation.

## 2. Input assumption

Development assumes a **complete extracted Switch 1.1.3 dump is locally available**. The builder consumes the dump root directly.

Expected local source material:

- Switch 1.1.3 ExeFS, including `main`
- Switch 1.1.3 RomFS
- `Taiko5DX_Korean_Patcher_v1.02.zip`
- PC original files only when a comparison task specifically needs them

Large/binary source material stays outside this public repository.

## 3. Fixed target identity

- Title ID: `0100346017304000`
- Switch version: `1.1.3`
- `main` NSO Build ID: `D9120950C258610A746F4A31CE3A3B376DE393D9`
- Compressed `main` observed size: 5,287,359 bytes
- NSO mapped uncompressed end: `0xA20430`

NSO segments:

- text: mem `0x000000`, decompressed `0x58CE60`
- rodata: mem `0x58D000`, decompressed `0x432018`
- data: mem `0x9C0000`, decompressed `0x60430`

The builder now guards this exact segment layout in addition to the Build ID.

## 4. PC Korean patch structure already confirmed

The embedded `patch_payload.zip` contains 209 items total:

- 169 `EVENT/*.TS5`
- 28 `G1T`
- 10 `TR5`
- 1 `TAI5MSG_JP.DAT`
- 1 `dinput8.dll`

Therefore: 208 game-data replacement items + `dinput8.dll`.

All 208 target relative paths exist in the Switch 1.1.3 RomFS. Do not re-run path-existence validation unless the dump itself changes.

The integrated builder currently copies **207** of those game-data replacements directly and deliberately excludes only `CMENU/CWTDAT_JP.TR5`.

## 5. Known platform exception: CWTDAT

`CMENU/CWTDAT_JP.TR5` is structurally different between PC and Switch.

- Switch JP size: 480,382 bytes
- PC original JP size: 548,530 bytes
- PC Korean patched size: 548,530 bytes

The 68,148-byte size difference is a platform difference, not a Korean-patch expansion. Never replace the whole Switch CWTDAT with the PC file.

PC original vs PC Korean CWTDAT changes are small. A subset occurs at offsets shared with the Switch file and can be selectively reconstructed later from the Switch base.

## 6. Font and Korean byte encoding

The Switch original `FONT/FONT_JPN.G1T` and Steam original font are byte-identical.

- Original font size: 13,108,628 bytes
- Original texture pages: 50
- Original font SHA-256: `9c886848c31c31d09aeeed0ac5c44b909d561220110ca04da0f7fa32d3a0083e`
- PC Korean patched font size: 16,779,036 bytes
- PC Korean patched font SHA-256: `c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932`
- Patched texture pages: 64

Original pages 0~48 are unchanged. Korean pages 49~62 correspond to lead bytes `EB~F8`. Page 63 is the final single-byte/ASCII-ish page.

Korean text uses the game's custom two-byte code space, not UTF-8/UTF-16. Confirmed examples include `EBE0=기`, `ECE9=노`, `F5B6=타`.

## 7. Switch text/font functions already identified

- `0x430350`: UTF-16 -> game 1/2-byte code conversion
- `0x4305D0`: game code -> UTF-16 conversion
- `0x446310`: 1/2-byte character segmentation/count
- `0x446420`: `GetFontTexIndex`

Switch JP segmentation already treats `0x81~0x9F` and `0xE0~0xFC` as two-byte leads. Korean lead bytes `EB~F8` therefore already segment correctly.

## 8. `dinput8.dll` / T5K121R is now parsed directly

`dinput8.dll` SHA-256: `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`.

The builder now extracts `RT_RCDATA/101` from `dinput8.dll` and parses the `T5K121R` resource itself. No raw DLL file-offset assumption is needed.

Directly parsed resource layout:

```text
resource size                  613,685 (0x95D35)
header                         0x0000..0x0047
mapping table                  0x0048..0x9D17  (10,036 x 4 bytes)
pointer replacement strings    0x9D18..0x9F71  (602 bytes)
runtime helper blob            0x9F72..0xA00F  (158 bytes)
inline patch records            0xA010..0x951BF  (17,103 variable records)
pointer patch records           0x951C0..0x9553F (56 x 16 bytes)
runtime descriptors             0x95540..end     (11 descriptors)
```

Header values agree with the known patch:

- version 1
- inline records 17,103
- pointer records 56
- runtime descriptors 11
- target PC EXE size 18,685,960

Runtime descriptor names include `ui_width_1~4`, `description_font_1~2`, `mapping_lookup_1A/2A`, `runtime_byte_validation`, `font_page_limit`, and `runtime_page_mapper`.

## 9. Confirmed and implemented Switch page mapper

An in-place ARM64 rewrite at `0x44650C..0x446534` preserves the existing JP mapping and adds:

- `EB~F8` -> pages 49~62

No code cave is required.

Original 44 bytes at `0x44650C`:

`690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b3f01007108b1891a087d0813007d0011`

Replacement 44 bytes:

`693e08532a8103515f610071680100545f29007168000054407d00110400001440990011020000141f2003d5`

## 10. Unicode/game-code mapping expansion

The T5K resource contains exactly **10,036** mapping entries.

- original mapping: 7,494
- Korean additions: 2,542
- total: 10,036

The PC DLL changes the lookup count from `0x1D46` (7,494) to `0x2734` (10,036).

Switch functions at `0x430350` and `0x4305D0` still use the 7,494-entry JP mapping. Full Unicode/input conversion support still requires relocating/expanding the table and changing lookup references/counts.

Do not overwrite neighboring language mapping data blindly. This remains a real pending implementation item.

## 11. 17,103 inline records: meaningful subset now integrated

The builder now parses all 17,103 same-length PC replacement records and maps a conservative subset automatically into Switch `main`.

For the fixed Switch 1.1.3 `main`:

```text
PC records total                 17,103
unique original patterns          8,713
no Switch match                     186
multiple Switch matches            2,476
unique match outside rodata          528
candidate rodata patterns           5,523
overlap-skipped                         4
selected unique patterns            5,519
PC records covered                  5,521
```

Selection rule is intentionally simple and reproducible:

- exact original bytes occur exactly once in the whole Switch `main`;
- duplicate PC records with the same original bytes must agree on replacement bytes;
- match must lie inside Switch rodata (`0x58D000..0x9BF018`), not ARM64 text;
- overlapping candidates are resolved longest-first.

This is now part of the integrated Eden build. The remaining records are not discarded; they remain pending for context-aware matching instead of being guessed.

## 12. 56 pointer records

The exact 56-record T5K pointer table is now parsed and retained by the builder/reporting layer. Switch correspondence is not yet emitted because the PC slots/RVAs cannot be copied directly into the NSO.

This is the next major hardcoded-text expansion after the exact-unique inline subset.

## 13. Current integrated Eden development build

The unified builder emits one `Taiko5DX_KR_DEV` mod containing:

- Build-ID IPS
- ARM64 page mapper
- 5,519 exact-unique inline translation patches (5,521 PC records covered)
- 207 directly reusable PC Korean RomFS payload files
- the 64-page Korean font
- `BUILD_REPORT.json` with T5K parse and mapping statistics

Local builder execution against the fixed 1.1.3 `main` completed successfully and produced **5,520 IPS records total** (5,519 inline + 1 page mapper).

### First real Eden Android runtime result

The first integrated v0.2a test produced a **freeze with the add-on enabled**. With the same game/environment and the add-on disabled, the game boots/runs normally. Therefore the failure is inside the current mod package, not a baseline Eden/game launch failure.

This result does **not yet identify which mod component is responsible**. The immediate diagnostic build is `v0.2b NO-INLINE`, which keeps the 207 RomFS replacements, Korean font, and page-mapper patch but removes all 5,519 inline IPS translations.

Interpretation of the next test:

- v0.2b boots: the 5,519 inline patch set is the primary freeze suspect and must be narrowed/fixed.
- v0.2b still freezes: isolate page-mapper versus RomFS/font next.

Do not attribute the freeze to Eden's Global/Custom per-game setting merely because Custom was selected; add-on disable restoring normal execution makes the mod itself the current variable of interest.

`CWTDAT_JP.TR5`, the 10,036-entry mapping relocation, the 56 pointer mappings, and remaining UI/runtime counterparts are still pending.

### Eden Android installation constraint

Do **not** assume normal Android file-manager access to Eden's internal folder. In the actual target phone environment, Eden's internal folder was not directly accessible.

For current development ZIPs, the supported install flow is:

1. extract the ZIP into an ordinary accessible location such as Android `Download`;
2. open the target game's Eden per-game Add-ons screen;
3. choose `+ Install` -> `Mods and cheats`;
4. select the extracted mod root directory itself, which must contain `exefs/` and/or `romfs/` directly beneath it;
5. confirm the mod is listed/enabled, then run with update 1.1.3 active.

Do not tell the user to manually browse into or copy files directly to Eden's hidden/internal Android storage as the default procedure. See `docs/EDEN_ANDROID_TEST_GUIDE.md`.

## 14. Development output strategy

Primary dev output remains one Eden mod directory continuously replaced during testing:

```text
Taiko5DX_KR_DEV/
├─ exefs/
│  └─ <BuildID>.ips
└─ romfs/
   └─ ...
```

Internal feature isolation is for debugging only. Do not return to serial P0/P1/P2 packaging unless a concrete runtime failure requires it.

## 15. Final distribution target

The final user-facing patcher target is **Android APK first**, because Eden Android is the primary usage environment.

The APK is a separate patch-generation app; it is not installed into Eden itself. Its job is to:

1. let the user select a complete extracted Switch 1.1.3 dump root;
2. let the user select `Taiko5DX_Korean_Patcher_v1.02.zip`;
3. validate the expected Build ID / source layout;
4. run the same patch-generation logic as the development builder;
5. emit an Eden-ready `Taiko5DX_KR` mod directory containing `exefs/` and `romfs/`;
6. use Android Storage Access Framework / user-granted folder access for output so the user can place the result where Eden can import or manage it.

The APK must **not embed or redistribute** copyrighted game binaries, the PC patch archive, translated game-data payloads, fonts, keys, XCI/NSP/NCA files, or full game dumps. Those remain user-supplied inputs.

Development order is fixed: **finish and validate the core builder first, then wrap the same logic in the Android APK UI.** Do not fork the patch logic into a separate implementation that would require maintaining two independent patch engines.

A Windows CLI/EXE frontend may be added later as a convenience, but it is secondary and must reuse the same core patch logic.

## 16. Work priority from here

1. Run `v0.2b NO-INLINE` in Eden Android and record whether it boots.
2. If v0.2b boots, binary-split the 5,519 inline set until the offending patch cluster is identified; if it still freezes, isolate page mapper vs RomFS/font instead.
3. In parallel, implement Switch-side 10,036 mapping relocation/count patches.
4. Map the 56 pointer records and then the ambiguous/missing inline records with context-aware matching.
5. Locate/port `ui_width_1~4` and `description_font_1~2` counterparts where runtime behavior shows they matter.
6. Reconstruct Switch-native `CWTDAT_JP.TR5` selectively.
7. Keep replacing one integrated dev mod and use failures to drive deeper work.
8. After the core builder is functionally stable, add the Android APK frontend using SAF-based file/folder selection and Eden-oriented output.

## 17. Anti-loop rule

Do not spend an entire work session re-validating one already-established point. If a fact is marked confirmed here, reuse it unless a new implementation result contradicts it. Prefer integrated forward progress and real test feedback.
