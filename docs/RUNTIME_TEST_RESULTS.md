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
| Y0 v0.2l | remove 2,099 translated halfwidth-yomi records + disable eight known yomi-enable callers | **Stable, but target garbled yomi rows still appear; suppression hypothesis incomplete** |
| W0 v0.2m | D5519 + six A1+ fullwidth-threshold patches | **Prepared; runtime pending** |

## Critical build-layer correction

Eden/Yuzu applies classic IPS to an artificial image consisting of `0x100-byte NSOHeader + decompressed mapped NSO image`. Canonical rule is:

```text
emitted IPS offset = mapped flat NSO offset + 0x100
```

All IPS-bearing builds through P0N v0.2f omitted this shift. Their crashes are historical observations only and cannot establish candidate-level safety because every intended mapped target `X` was patched at `X-0x100`.

## P0N2 v0.2g — PASS

Artifact SHA-256 `1ccb27e7f8836b8687ade7e147b0f549d49069dcecebaf808fa6eabd3277e8f6`.

5,520 IPS records = corrected page mapper + 5,519 verified true no-op records. Boot, Korean title, input, and next main menu all succeeded. This proves corrected large classic-IPS application works on the tested route and that record count itself was not the old freeze mechanism.

## M1A v0.2h — PASS

Exactly one real inline replacement: T5K `R489`, `シナリオを選んでください` -> `시나리오를 선택하세요`, mapped `0x69B6A1` -> emitted `0x69B7A1`. Scenario/protagonist-selection flow remained responsive.

## D5519 v0.2k — PASS WITH RESIDUAL UI ISSUES

D5519 reuses the historical 5,519-real-inline payload and fixes only the IPS coordinate convention. Artifact SHA-256 `46017206ed2679a645b1e0121aff6b7742fcbec94f41197e5f5681f517c9fae2`.

User runtime screenshots show successful progression through title, main menu, scenario selection/explanation, protagonist selection, and normal early gameplay with no freeze or forced exit.

Residual issues observed:

- garbled auxiliary yomi/furigana rows on name UIs;
- repeated short Japanese UI tokens such as `はい`, date/currency suffixes and `城`;
- repeated place-name components such as `清洲`;
- compact/fixed-field Korean name rendering defects, most clearly `마츠다이라 모토야스` losing the `츠` glyph on a nameplate, and user-observed odd appearance around `케/자` in `나야 스케자에몬`.

## Y0 v0.2l — STABLE, TARGET SUPPRESSION FAILED

Artifact SHA-256 `ae67b2bdece0e261239a3a505ad018761904c25124f0857cf0a917f9a4a6c869`.

Y0 restores 2,099 halfwidth-kana yomi-like fields to original Switch bytes, retains 3,420 other historical inline replacements, and changes eight known direct `mov w6,#1` yomi-enable call sites to zero before shared routine `0x45B0F8`.

Runtime result on 2026-09-11:

- game remains stable on the tested route;
- Korean main names remain;
- **the garbled small reading rows visible in protagonist selection and dialogue nameplates remain present**.

Therefore the eight call sites are real static yomi-enable sites, but they do not control the observed two UI rows, or an additional wrapper/path re-enables/draws them. Do not repeat the same eight-site-only suppression attempt. Internal-yomi preservation remains the safer data policy while the actual visible-row path is traced later.

## W0 v0.2m — PREPARED, RUNTIME PENDING

Purpose: test the PC `font_page_limit` behavior that reclassifies repurposed single-byte codes `A1+` as full-width glyphs.

Important static evidence:

- PC T5K `松平元康` replacement fits a 16-byte fixed field by using compact single-byte codes `B2 BD AA` for `마 츠 다`, followed by normal two-byte Korean for `이라 모토야스`.
- The exact Korean G1T page-63 cells contain valid `마/츠/다` artwork, so the missing `츠` is not a corrupt source-font glyph.
- PC `font_page_limit` changes threshold `0xFF -> 0xA0`; semantically, values above `0xA0` move to the alternate/full-width path.
- Six Switch width/layout compare sites use `cmp w8,#0x100` and have been changed to `cmp w8,#0xA1` in W0:

```text
mapped      Eden IPS
0x445EAC -> 0x445FAC
0x445FC8 -> 0x4460C8
0x446198 -> 0x446298
0x4472E8 -> 0x4473E8
0x447344 -> 0x447444
0x447C44 -> 0x447D44
```

Artifact:

- `W0_Taiko5DX_KR_DBG_FONTWIDTH_A1_v0.2m.zip`
- SHA-256 `e453d5958793748ebf841f295ef4005a9a612fdbe643439fe9c2a2c0183ea2ad`
- basis: D5519 v0.2k
- final IPS records: 5,526 = D5519 5,520 + six threshold edits.

Runtime check: enable W0 alone, reach the Matsudaira Motoyasu nameplate, verify whether `마츠다이라 모토야스` now contains `츠`, then inspect `나야 스케자에몬` for `케/자` appearance and note any spacing/halfwidth regressions.

## Current interpretation

- The old freeze mechanism is dominated by the fixed `+0x100` IPS-coordinate defect.
- Y0 disproves only the narrow eight-site suppression hypothesis for the observed yomi rows; it does not disprove the internal-yomi classification or the policy of preserving yomi internally.
- The missing `츠` is now tied to a concrete PC runtime mechanism: compact A1+ Korean glyphs plus the `font_page_limit` half/fullwidth threshold. W0 is the first direct Switch diagnostic of that behavior.
- `케/자` source glyphs are correct in the G1T. If W0 does not fix their runtime appearance, investigate their UI-specific advance/scaling/render path separately.
- Repeated short UI strings remain a separate object-recovery task after the font-width diagnostic.