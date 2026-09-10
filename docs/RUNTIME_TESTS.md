# Eden Android Runtime Tests

Last updated: 2026-09-10 (KST)

## Environment

- Target: TAIKO RISHHIDEN V DX Switch v1.1.3
- Emulator: Eden Android
- Installation: extract mod ZIP to an ordinary Android-accessible folder, then import through the game's Add-ons -> + Install -> Mods and cheats flow.
- Do not assume direct normal-file-manager access to Eden's internal folder; it was not directly accessible on the real target device.

## Results

### Baseline / add-on disabled

- Result: PASS
- Game boots normally when the Korean-port add-on is disabled.

### v0.2a integrated

Contents:
- 207 reusable RomFS replacements
- 64-page Korean font
- ARM64 EB~F8 font page mapper
- 5,519 exact-unique inline Switch-main patches

Result: FAIL
- Freeze with add-on enabled.

### v0.2b NO-INLINE

Contents:
- 207 reusable RomFS replacements
- 64-page Korean font
- ARM64 EB~F8 font page mapper
- no inline patches

Result: PASS
- Boots to title screen.
- Korean title is visibly rendered correctly in the real Eden Android run.

Conclusion: the base RomFS/font/page-mapper combination is viable through title boot. The freeze is introduced by the inline patch set, not by the add-on mechanism itself.

### v0.2c remove-one-outlier

Contents:
- same as v0.2a except one suspicious non-text-looking inline record at Switch offset 0x5FBA41 removed
- 5,518 inline patches remain

Result: FAIL
- Still freezes.

Conclusion: 0x5FBA41 was not the sole failure source. There are one or more additional unsafe inline mappings, or a multi-patch interaction. Do not keep removing individual records by guesswork.

## Current isolation plan

Split the remaining 5,518 inline records by Switch offset into equal halves while keeping the known-good v0.2b base unchanged:

- v0.2d INLINE-A: 2,759 inline records, offsets 0x682AE5..0x72028D
- v0.2d INLINE-B: 2,759 inline records, offsets 0x72034F..0x783F9A

Test INLINE-A first. If it freezes, continue splitting A. If it boots, continue splitting B without requiring the user to retest the full set.
