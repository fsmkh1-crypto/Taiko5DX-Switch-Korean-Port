# Eden Android test guide

## Important storage rule

Do **not** assume that Android users can directly browse or write Eden's internal data directory with a normal file manager. The tested user environment could not access the Eden folder directly.

For development builds, installation must therefore be documented around Eden's own per-game add-on importer rather than manual copying into an internal Eden path.

## Install flow

1. Extract the distributed ZIP into an ordinary Android-accessible folder such as `Download`.
2. Confirm the extracted mod directory has `exefs/` and `romfs/` directly beneath it.
3. Open Eden and enter the target game's per-game settings / Add-ons screen.
4. Choose `+ Install` and then `Mods and cheats` (`모드 및 치트` in the Korean resources).
5. In Android's folder picker, select the extracted `Taiko5DX_KR_DEV` directory itself.
6. Confirm the mod appears in the game's Add-ons list and is enabled.
7. Run with game update 1.1.3 active.

Eden validates mod folders by expecting at least one of `cheats/`, `romfs/`, or `exefs/` under the selected directory, so the user must select the mod root, not its parent and not the `romfs` subfolder alone.

## First-run checks

- Does the game boot normally?
- Does any Korean text render correctly?
- Are there squares, question marks, wrong kana/kanji, or missing glyphs?
- Do title/menu strings clip or overlap?
- Can a new game reach scenario / officer selection?
- Do event dialogue lines render and wrap correctly?
- Does any specific translated screen crash?
- Do long descriptions or choices overflow their UI boxes?
- If possible, can a save be created and loaded?

## Failure report

Record the first failing screen and classify it as one of:

- crash
- freeze
- Korean glyph corruption
- Japanese text remaining
- clipping / overlap / width issue
- other

Attach a screenshot when possible. For crashes, collect the Eden log as well.

## Current known incomplete areas

- Switch-native `CWTDAT_JP.TR5` reconstruction
- 7,494 -> 10,036 character-mapping expansion
- 56 pointer-record mappings
- remaining UI width / description-font runtime behavior
- ambiguous / missing inline records beyond the exact-unique subset

For the first integrated build, the two highest-value observations are therefore **whether it boots** and **whether actual Korean glyphs render correctly**.
