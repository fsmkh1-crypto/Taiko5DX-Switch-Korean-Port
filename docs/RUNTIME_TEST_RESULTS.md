# RUNTIME TEST RESULTS

Observed Eden Android behavior for the Taiko5DX Switch Korean-port development builds. Runtime success is route evidence, not by itself release-SAFE certification.

## 2026-09-10 / 2026-09-11

| Variant | Key configuration | Result |
|---|---|---|
| Add-on disabled | no mod | Game boots/runs normally |
| v0.2a | historical 5,519 real inline + old no-shift IPS convention | Freeze |
| v0.2b NO-INLINE | RomFS/font + old no-shift page-mapper record | Boots; Korean title visible |
| v0.2c | 5,518 real inline + old no-shift convention | Fails/freezes |
| A | 2,759 old-offset real inline | Freeze |
| B | 2,759 old-offset real inline | Title then crash after input |
| P0N v0.2f | 5,519 intended no-op records but old no-shift convention | Freeze |
| P0N2 v0.2g | corrected page mapper + 5,519 true no-ops, all `mapped+0x100` | **PASS: title -> input -> main menu** |
| M1A v0.2h | corrected page mapper + one real inline `R489` | **PASS through scenario/protagonist flow** |
| D5519 v0.2k | corrected page mapper + historical 5,519 real replacements, all `mapped+0x100` | **PASS through early gameplay; no freeze/forced exit observed** |
| Y0 v0.2l | D5519-derived non-yomi inline + internal yomi restored + visible yomi call sites disabled | **Prepared; runtime pending** |

## Critical build-layer correction

Eden/Yuzu applies classic IPS to an artificial image consisting of:

```text
0x000000..0x0000FF  NSOHeader (0x100 bytes)
0x000100..          decompressed mapped NSO image
```

Canonical rule:

```text
emitted IPS offset = mapped flat NSO offset + 0x100
```

All IPS-bearing builds through P0N v0.2f omitted this shift. Therefore their observed crashes are historical runtime facts but cannot be used as candidate-level safety evidence: each intended mapped target `X` was actually patched at mapped `X-0x100`.

P0N2 is the first true large no-op control under the correct coordinate convention and passed.

## P0N2 v0.2g — PASS

Artifact:

- `P0N2_Taiko5DX_KR_DBG_NOOP5519_PLUS100_v0.2g.zip`
- SHA-256 `1ccb27e7f8836b8687ade7e147b0f549d49069dcecebaf808fa6eabd3277e8f6`
- 5,520 IPS records = corrected page mapper + 5,519 verified true no-op records.

Observed: boot, Korean title, button input, next main menu all succeeded.

Narrow conclusions:

1. corrected `+0x100` classic-IPS coordinate path works on the tested route;
2. 5,520 classic-IPS records are not intrinsically causing the old freeze;
3. old P0N freeze is explained by wrong-address writes, not by true no-op count.

## M1A v0.2h — PASS

Exactly one real inline replacement:

- T5K `R489`;
- `シナリオを選んでください` -> `시나리오를 선택하세요`;
- mapped `0x69B6A1` -> emitted `0x69B7A1`.

Observed progression through scenario selection/description and protagonist selection without freeze/forced exit.

## D5519 v0.2k — PASS WITH RESIDUAL UI ISSUES

D5519 is the historical v0.2a 5,519-real-inline payload with only the IPS coordinate convention corrected by `+0x100`.

Artifact SHA-256:
`46017206ed2679a645b1e0121aff6b7742fcbec94f41197e5f5681f517c9fae2`

User runtime screenshots show successful progression through:

- title;
- main menu;
- scenario selection;
- scenario explanation;
- protagonist selection;
- entry into normal gameplay.

No freeze or forced exit was observed on this route.

Visible residual issues:

- Korean main text/names broadly render;
- small auxiliary yomi/furigana line is garbled on name UIs;
- some short repeated UI tokens remain Japanese (`はい`, date/currency suffixes, `城`);
- some repeated place-name components such as `清洲` remain Japanese.

This strongly supports the corrected interpretation that the earlier immediate freezes were dominated by the missing `+0x100` build-layer bug. It does **not** prove all 5,519 records are safe for every late-game path.

## Y0 v0.2l — PREPARED, RUNTIME PENDING

Purpose: preserve original Japanese halfwidth-kana yomi internally while removing the unnecessary visible reading line from Korean name UIs.

Artifact:

- `Y0_Taiko5DX_KR_DBG_NOYOMI_v0.2l.zip`
- SHA-256 `ae67b2bdece0e261239a3a505ad018761904c25124f0857cf0a917f9a4a6c869`

Static composition:

- page mapper: 1;
- retained non-yomi historical inline records: 3,420;
- removed/restored-to-original halfwidth-yomi translations: 2,099;
- yomi-render enable call-site edits: 8;
- final IPS records: 3,429.

Eight mapped call sites change:

```text
26 00 80 52   mov w6,#1
```

to:

```text
E6 03 1F 2A   mov w6,wzr
```

before calls to shared mapped routine `0x45B0F8`.

Next runtime check: run Y0 alone and verify that Korean main names remain, the garbled small yomi line disappears, and navigation/sorting remain stable.

## Current interpretation

- `+0x100` omission is the dominant confirmed defect behind pre-P0N2 IPS builds.
- D5519 changes the next priority from crash-halving to residual UI/data-layer recovery.
- Yomi and repeated short strings are separate problems: yomi should be preserved internally but hidden visually; repeated short UI strings should be recovered at confirmed Switch object locations rather than by global raw substring replacement.
- See `docs/POST_D5519_ANALYSIS.md` for static evidence and the recovery rule.