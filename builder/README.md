# Builder

> **Governance note:** this document describes the existing development builder, including its historical exact-unique inline baseline. It is not the release-coverage authority and it does not define the current project resume step. Read `../AGENTS.md` and `../PROJECT_STATE.md` first.

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

The current legacy integrated output includes:

- the confirmed ARM64 Korean font-page mapper (`EB~F8 -> pages 49~62`);
- all directly reusable PC patch RomFS payload files except `CMENU/CWTDAT_JP.TR5` (207 files);
- the 64-page Korean `FONT_JPN.G1T`;
- a conservative exact-match subset of the 17,103 PC EXE inline translation records.

The legacy inline mapper uses the original byte sequences stored in `T5K121R`. It scans the decompressed Switch `main` and emits a patch only when the original bytes occur exactly once, the replacement is unambiguous, the match is inside Switch rodata, and it does not overlap a more specific selected patch. On the fixed 1.1.3 `main`, this historically selects 5,519 patterns covering 5,521 PC records.

That 5,519 subset is a development/diagnostic baseline only. `unique exact match` is not a release-safety or full-port coverage rule. Current release/accounting authority is defined by `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`, `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`, `docs/INLINE_VALIDATION_POLICY.md`, and the current `PROJECT_STATE.md`.

`BUILD_REPORT.json` records exact mapping statistics on every build so unresolved records can be improved without losing the working integrated subset.

The builder deliberately skips the PC `CMENU/CWTDAT_JP.TR5` because the Switch file has a different platform structure. That file must be reconstructed from the Switch-native base unless later structural evidence authorizes another path.

Still pending in the integrated builder are wider semantic/accounting layers including mapping relocation/count behavior, pointer records, runtime counterparts, Switch-native CWTDAT reconstruction, and full inline/object coverage. The authoritative current resume scope is always `PROJECT_STATE.md`.
