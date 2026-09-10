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

The builder locates ExeFS `main` and the RomFS root, validates the expected NSO Build ID and the known `GetFontTexIndex` bytes, extracts the embedded PC patch payload, and emits an Eden development mod folder.

Current implementation deliberately skips the PC `CMENU/CWTDAT_JP.TR5` because the Switch file has a different platform structure. That file will be reconstructed from the Switch-native base once the selective patch module is added.

The current code patch implements only the confirmed Korean font page mapper. Remaining runtime/inline/pointer mapping work is tracked in `PROJECT_STATE.md` and `PATCH_MAP.md`.
