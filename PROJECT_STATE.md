# PROJECT_STATE

Last updated: 2026-09-10 (KST)

This file is the canonical resume point for this project. Read this before new analysis or implementation work.

## 1. Goal

Port the existing PC Korean patch `Taiko5DX_Korean_Patcher_v1.02` to Nintendo Switch **TAIKO RISHHIDEN V DX v1.1.3**, with Eden Android as the primary development/test target.

Development policy: build an integrated mod first, then fix failures found in real execution. Do not keep splitting the project into long P0/P1/P2 validation phases unless a specific failure requires isolation.

## 2. Input assumption

From this point forward, development assumes a **complete extracted Switch 1.1.3 dump is locally available**. The working tool may consume the dump root directly.

Expected local source material:

- Switch 1.1.3 ExeFS, including `main`
- Switch 1.1.3 RomFS
- PC original files when comparison is needed
- `Taiko5DX_Korean_Patcher_v1.02.zip`

Large/binary source material stays outside this public repository.

## 3. Fixed target identity

- Title ID: `0100346017304000`
- Switch version: `1.1.3`
- `main` NSO Build ID: `D9120950C258610A746F4A31CE3A3B376DE393D9`
- Compressed `main` observed size: 5,287,359 bytes
- NSO mapped uncompressed end: `0xA20430`

NSO segments already parsed:

- text: mem `0x000000`, decompressed `0x58CE60`
- rodata: mem `0x58D000`, decompressed `0x432018`
- data: mem `0x9C0000`, decompressed `0x60430`

## 4. PC Korean patch structure already confirmed

The embedded `patch_payload.zip` contains 209 items total:

- 169 `EVENT/*.TS5`
- 28 `G1T`
- 10 `TR5`
- 1 `TAI5MSG_JP.DAT`
- 1 `dinput8.dll`

Therefore: 208 game-data replacement items + `dinput8.dll`.

All 208 target relative paths exist in the Switch 1.1.3 RomFS. Do not re-run path-existence validation unless the dump itself changes.

Representative files were already confirmed byte-identical between Switch original and PC original, including `TAI5MSG_JP.DAT`, original `FONT_JPN.G1T`, representative EVENT TS5 files, TITLE/UI G1T files, and SNR0~SNR8 TR5 files.

## 5. Known platform exception: CWTDAT

`CMENU/CWTDAT_JP.TR5` is structurally different between PC and Switch.

- Switch JP size: 480,382 bytes
- PC original JP size: 548,530 bytes
- PC Korean patched size: 548,530 bytes

The 68,148-byte size difference is a **platform difference**, not a Korean-patch expansion. Never replace the whole Switch CWTDAT with the PC file.

PC original vs PC Korean CWTDAT changes are small (about 201 changed bytes). A subset of changes occurs at offsets shared with the Switch file and can be selectively reconstructed later from the Switch base.

## 6. Font and Korean byte encoding

The Switch original `FONT/FONT_JPN.G1T` and Steam original font are byte-identical.

- Original font size: 13,108,628 bytes
- Original texture pages: 50
- Original font SHA-256: `9c886848c31c31d09aeeed0ac5c44b909d561220110ca04da0f7fa32d3a0083e`
- PC Korean patched font size: 16,779,036 bytes
- PC Korean patched font SHA-256: `c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932`
- Patched texture pages: 64

Original pages 0~48 are unchanged. Korean pages 49~62 correspond to lead bytes `EB~F8`. Page 63 is the single-byte/ASCII-ish final page. Do not repeat the old incorrect claim that original page 49 merely moved unchanged to page 63.

Korean text uses the game's custom two-byte code space, not UTF-8/UTF-16. Confirmed examples include `EBE0=기`, `ECE9=노`, `F5B6=타`.

## 7. Switch text/font functions already identified

- `0x430350`: UTF-16 -> game 1/2-byte code conversion
- `0x4305D0`: game code -> UTF-16 conversion
- `0x446310`: 1/2-byte character segmentation/count
- `0x446420`: `GetFontTexIndex`

Switch JP segmentation already treats `0x81~0x9F` and `0xE0~0xFC` as two-byte leads. Therefore Korean lead bytes `EB~F8` already segment correctly; basic static rendering does not need a separate segmentation patch.

## 8. `dinput8.dll` findings

`dinput8.dll` SHA-256: `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`.

Observed runtime descriptor names include:

- `runtime_byte_validation`
- `font_page_limit`
- `runtime_page_mapper`
- `description_font_1`, `description_font_2`
- `ui_width_1` ~ `ui_width_4`
- mapping lookup patches

The PC runtime page mapper is confirmed to map Korean lead bytes `EB~F8` to font pages 49~62 and otherwise fall back to original behavior.

## 9. Confirmed Switch page-mapper patch

Switch original `GetFontTexIndex` behavior:

- `81~9F` -> pages 0~30
- `E0~EA` -> pages 31~41
- `FA~FC` -> pages 46~48
- one-byte code -> `texture_count - 1`

An in-place ARM64 rewrite at `0x44650C..0x446534` is already assembled and locally verified. It preserves existing JP mapping and adds:

- `EB~F8` -> pages 49~62

No code cave is required for this patch.

Original 44 bytes at `0x44650C`:

`690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b3f01007108b1891a087d0813007d0011`

Replacement 44 bytes:

`693e08532a8103515f610071680100545f29007168000054407d00110400001440990011020000141f2003d5`

## 10. Unicode/game-code mapping expansion

Original mapping table contains exactly **7,494** entries and matches the PC original table byte-for-byte.

The Korean patch adds exactly **2,542** entries:

- 2,350 KS X 1001 completed Hangul mappings
- 192 PUA mappings

Total: **10,036** entries.

The PC DLL changes the lookup count from `0x1D46` (7494) to `0x2734` (10036).

Switch functions at `0x430350` and `0x4305D0` each use the 7,494-entry JP mapping. Full Unicode/input conversion support requires relocating/expanding the table and changing lookup references/counts.

A physically large enough neighboring table area exists, but cross-reference safety has not yet been proven. Do not overwrite another language table blindly.

## 11. PC EXE patch records

The patch resource contains **17,103** fixed-width same-length in-place replacement records of the form conceptually:

`[PC RVA][length][original bytes][Korean bytes]`

These are not a single 571 KB string blob that must be inserted into Switch `main`.

There are also **56** separate pointer-patch records.

The next task is to map these PC targets to corresponding Switch locations using binary/context signatures and then apply the safe mappings through the unified builder.

## 12. Development output strategy

Primary dev output is one Eden mod directory continuously replaced during testing:

```text
Taiko5DX_KR_DEV/
├─ exefs/
│  └─ <BuildID>.ips
└─ romfs/
   └─ ...
```

Internal builder feature switches are only for debugging/isolation. They are not intended as separate public patch editions.

Final public distribution target: a builder/patcher that uses the user's locally available source material and produces the mod. Do not publish copyrighted game/translation payload files in this repository.

## 13. Work priority from here

1. Convert the current proof-of-concept builder to accept the full Switch 1.1.3 dump root.
2. Port remaining `dinput8.dll` behavior into Switch ARM64/data patches, prioritizing mapping lookup + table expansion and width/font runtime fixes.
3. Build automated correspondence for 17,103 inline records and 56 pointer records.
4. Integrate the 208 PC payload files while reconstructing Switch-native CWTDAT selectively.
5. Produce one integrated Eden development mod and test it.
6. Use failures from real execution to decide what needs deeper analysis.

## 14. Anti-loop rule

Do not spend an entire work session re-validating one already-established point. If a fact is marked confirmed here, reuse it unless a new implementation result contradicts it. Prefer integrated forward progress and real test feedback.
