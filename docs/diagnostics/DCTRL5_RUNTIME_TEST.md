# DCTRL5 Eden Runtime Test

## Purpose

Verify the Eden delivery path, not translation coverage. DCTRL5 contains exactly one already-verified prerequisite record (`V006` runtime page mapper) plus five `V024` diagnostic text-object records.

## Artifact identity

- Package: `DCTRL5_Taiko5DX_KR_EDEN.zip`
- SHA-256: `49a314996f2305a952250f23853f483d0f435494167eec87b8c5077bf10f53f5`
- Drive: `태합입지전 포팅/Eden_Builds/DCTRL5_Taiko5DX_KR_EDEN.zip`
- Builder source commit: `bc3db0fd42ebecfd0a6ebc7d61651ea18f738fbf`
- Build report + emit log first coexist at commit: `e5c223231bf0dec69dbd45581002a235e5fbd07e`
- Pre-runtime provenance freeze: `docs/diagnostics/DCTRL5_PROVENANCE_FREEZE.json`

## Package structure

After extracting the ZIP, select this directory itself in Eden:

`Taiko5DX_KR_DBG_DCTRL5/`

It contains:

- `exefs/D9120950C258610A746F4A31CE3A3B376DE393D9.ips`
- `romfs/FONT/FONT_JPN.G1T`
- `DCTRL5_BUILD_INFO.json`

The IPS is Eden classic IPS and uses the canonical mapped-to-emitted `+0x100` NSOHeader shift.

## Baseline control

1. Disable DCTRL5 and any other Korean-port diagnostic/mod add-ons for this game.
2. Use game update 1.1.3.
3. Reach a screen that visibly contains the normal Japanese date objects (`年`, `月`, and/or `日`).
4. Capture that baseline screen before enabling DCTRL5.

Do not infer failure from an object that is not actually visible on the chosen baseline route.

## Install in Eden

1. Extract `DCTRL5_Taiko5DX_KR_EDEN.zip` to normal Android-accessible storage.
2. Open the target game's per-game settings in Eden.
3. Open Add-ons.
4. Choose `+ Install` -> `Mods and cheats`.
5. Select the extracted `Taiko5DX_KR_DBG_DCTRL5` directory itself, not its parent and not only `romfs` or `exefs`.
6. Ensure DCTRL5 is enabled.
7. Disable/remove overlapping Taiko5DX Korean diagnostic mods for this test.
8. Launch with update 1.1.3 active.

## Primary observation

Return to the same date screen used for the baseline.

Expected diagnostic replacements are source-grounded from the PC T5K:

- `年` -> Korean `년`
- `月` -> Korean `월`
- `日` -> Korean `일`

`はい` -> `예` and `城` -> `성` are secondary observations if those objects appear naturally on the tested route.

## Interpretation

### DELIVERY PASS

If at least one date object that was visibly Japanese in the baseline (`年`, `月`, or `日`) now displays its Korean replacement, the current build/package/install/runtime delivery path is proven active on that route.

If delivery passes while `はい` or `城` remains Japanese on a screen that definitely consumes the verified object, classify that as a per-object consumer/data-selection issue, not a global delivery failure.

### DELIVERY PASS + RENDERING-PREREQUISITE FAILURE

If the date object's bytes visibly change but the Korean glyph is broken, missing, or wrong, classify text-record delivery as active. Investigate the rendering prerequisite family (page-mapper runtime semantics / actual mapper path / Korean font selection) rather than treating the IPS as absent.

### DELIVERY FAIL

If the same baseline date objects remain unchanged Japanese with DCTRL5 enabled, classify the feedback-loop delivery control as failed. Do not proceed to causal interpretation of new counterpart diagnostics. Investigate the D5519-to-current delivery delta in this order:

1. builder/emitted IPS output;
2. exact package identity;
3. Eden version/loader behavior;
4. install method;
5. overlapping/old add-ons;
6. game update/Build ID;
7. RomFS font prerequisite.

## Result capture

Record:

- exact tested ZIP SHA-256;
- Eden version/build if visible;
- game update 1.1.3 / Build ID;
- whether other add-ons were disabled;
- baseline screenshot;
- DCTRL5 screenshot of the same route;
- exact observed forms of `年/月/日` and, if encountered, `はい/城`;
- PASS / PASS+rendering-failure / FAIL classification.
