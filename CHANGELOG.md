# CHANGELOG

## 2026-09-10

### First Eden Android runtime result

- Integrated v0.2a freezes when the add-on is enabled.
- With the same game and Eden environment, disabling the add-on restores normal boot/execution.
- This confirms the immediate failure is inside the current mod package rather than a baseline Eden/game launch problem.
- Do not attribute the freeze to Eden's Global/Custom per-game setting at this stage; the add-on enable/disable state is the confirmed differentiator.
- Prepared `v0.2b NO-INLINE` as the next diagnostic build: 207 RomFS replacements + Korean font + page mapper remain, while all 5,519 inline IPS translation patches are removed.
- Next interpretation: if v0.2b boots, narrow the inline set by binary splitting; if it still freezes, isolate page mapper vs RomFS/font.

### Eden Android test packaging

- Added `docs/EDEN_ANDROID_TEST_GUIDE.md`.
- Recorded a real target-environment constraint: the user could not directly access Eden's internal Android folder with the normal file manager.
- Current development ZIP instructions now use Eden's own per-game Add-ons importer: extract to an ordinary Android folder, then `+ Install` -> `Mods and cheats`, selecting the mod root containing `exefs/` and `romfs/`.
- Added a first-run checklist focused on boot success, Korean glyph rendering, clipping/width problems, event dialogue behavior, and crash/log capture.
- Repacked the current integrated build as Android-oriented v0.2a with the guide embedded; patch payload itself is unchanged from integrated v0.2.

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
- Added conservative automatic Switch mapping: exact unique original bytes, Switch rodata only, no conflicting replacement, no overlap guessing.
- On the fixed Switch 1.1.3 `main`, selected 5,519 unique inline patterns covering 5,521 PC records.
- Reworked IPS generation to support thousands of patch records in one integrated Eden build.
- Integrated 207 directly reusable PC Korean RomFS payload files; `CMENU/CWTDAT_JP.TR5` remains intentionally excluded.
- Added fixed NSO segment-layout guards and original Switch font hash guard.
- Local build-generation test completed with 5,520 IPS records total: 5,519 inline translations + the ARM64 page mapper.
- Updated `PROJECT_STATE.md`, `PATCH_MAP.md`, and builder documentation to make this the new canonical resume point.

### Still pending

- 7,494 -> 10,036 Switch mapping table relocation/reference/count patches.
- Switch correspondence for the 56 pointer records.
- Context-aware mapping for ambiguous/missing inline records.
- `ui_width_1~4` / `description_font_1~2` Switch runtime counterparts.
- Switch-native `CWTDAT_JP.TR5` reconstruction.

### Repository initialization

- Established Nintendo Switch v1.1.3 / Title ID / NSO Build ID as the fixed development target.
- Adopted full extracted Switch 1.1.3 dump as the standard local development input.
- Documented the existing PC Korean patch as the source implementation to port rather than rebuilding translation assets from scratch.
- Recorded confirmed PC payload composition: 208 game-data replacements plus `dinput8.dll`.
- Recorded the Switch CWTDAT structural exception.
- Recorded the confirmed 64-page Korean font layout and custom Korean byte-code range.
- Recorded Switch text/font functions at `0x430350`, `0x4305D0`, `0x446310`, and `0x446420`.
- Recorded and implemented the first ARM64 page-mapper rewrite adding `EB~F8 -> pages 49~62`.
- Recorded exact mapping counts: 7,494 original + 2,542 Korean = 10,036.
- Corrected previous misunderstanding of 17,103 PC EXE records: they are primarily same-length in-place replacement records, not a monolithic injected text blob.
- Established integrated-build-first workflow and Eden Android as the primary test target.

### Existing local proof-of-concept

A local P0 Eden mod was produced containing:

- Build-ID IPS with the page-mapper patch
- PC Korean-patched `FONT_JPN.G1T`
- one translated EVENT TS5 smoke-test file

This P0 is superseded by the integrated development build path and is not stored in this public repository.
