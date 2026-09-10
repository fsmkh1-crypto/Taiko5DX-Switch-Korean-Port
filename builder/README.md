# Builder

Current development input policy: use a complete extracted Nintendo Switch v1.1.3 dump rather than manually passing individual Switch files.

Example:

```bash
pip install -r requirements.txt

python builder/build.py \
  --switch-dump "/path/to/Taiko5DX_Switch_1.1.3_dump" \
  --pc-patcher "/path/to/Taiko5DX_Korean_Patcher_v1.02.zip" \
  --output "/path/to/output"
```

The builder locates ExeFS `main` and the RomFS root, validates the fixed NSO Build ID/segment layout, validates the original Switch font, extracts the embedded PC patch payload, parses `dinput8.dll`'s `T5K121R` resource, and emits one Eden development mod folder.

Current integrated output includes:

- the confirmed ARM64 Korean font-page mapper (`EB~F8 -> pages 49~62`);
- all directly reusable PC patch RomFS payload files except `CMENU/CWTDAT_JP.TR5` (207 files);
- the 64-page Korean `FONT_JPN.G1T`;
- a conservative exact-match subset of the 17,103 PC EXE inline translation records.

The inline mapper uses the original byte sequences stored in `T5K121R`. It scans the decompressed Switch `main` and emits a patch only when the original bytes occur exactly once, the replacement is unambiguous, the match is inside Switch rodata, and it does not overlap a more specific selected patch. On the fixed 1.1.3 `main`, this currently selects 5,519 patterns covering 5,521 PC records.

`BUILD_REPORT.json` records exact mapping statistics on every build so unresolved records can be improved without losing the working integrated subset.

The builder deliberately skips the PC `CMENU/CWTDAT_JP.TR5` because the Switch file has a different platform structure. That file must be reconstructed from the Switch-native base rather than copied wholesale.

Still pending in the integrated port are the 10,036-entry mapping relocation/count patches, the 56 pointer records, UI/description-font runtime counterparts, and Switch-native CWTDAT reconstruction. These are tracked in `PROJECT_STATE.md` and `PATCH_MAP.md`.
