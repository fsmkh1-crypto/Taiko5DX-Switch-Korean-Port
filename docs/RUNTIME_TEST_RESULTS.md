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
| W0 v0.2m | D5519 + six A1+ fullwidth-threshold patches | **PARTIAL PASS: stable; `케/자` fixed; compact `쓰` still absent** |
| W1 v0.2n | W0 + missed render-width gate at mapped `0x44D9D0` | **Prepared; runtime pending** |

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
- compact/fixed-field Korean name rendering defects, most clearly `마쓰다이라 모토야스` losing the compact `쓰` glyph on a nameplate, and earlier odd appearance around `케/자` in `나야 스케자에몬`.

## Y0 v0.2l — STABLE, TARGET SUPPRESSION FAILED

Artifact SHA-256 `ae67b2bdece0e261239a3a505ad018761904c25124f0857cf0a917f9a4a6c869`.

Y0 restores 2,099 halfwidth-kana yomi-like fields to original Switch bytes, retains 3,420 other historical inline replacements, and changes eight known direct `mov w6,#1` yomi-enable call sites to zero before shared routine `0x45B0F8`.

Runtime result on 2026-09-11:

- game remains stable on the tested route;
- Korean main names remain;
- **the garbled small reading rows visible in protagonist selection and dialogue nameplates remain present**.

Therefore the eight call sites are real static yomi-enable sites, but they do not control the observed two UI rows, or an additional wrapper/path re-enables/draws them. Do not repeat the same eight-site-only suppression attempt. Internal-yomi preservation remains the safer data policy while the actual visible-row path is traced later.

## W0 v0.2m — PARTIAL PASS

Artifact SHA-256 `e453d5958793748ebf841f295ef4005a9a612fdbe643439fe9c2a2c0183ea2ad`.

W0 ports six Switch width/layout thresholds from `code < 0x100` to `code < 0xA1`, corresponding to the PC `font_page_limit` behavior for repurposed page-63 compact Korean bytes.

Static compact-name evidence for `松平元康`:

```text
B2 = 마
BD = 쓰
AA = 다
F36B EE93 = 이라
... = 모토야스
```

The intended Korean name is **`마쓰다이라 모토야스`**. The earlier project transcription `마츠다이라` / `BD=츠` was wrong and is corrected in the canonical ledger.

Runtime result on 2026-09-11:

- game remained stable on the tested route;
- `나야 스케자에몬` now renders the previously odd `케/자` correctly;
- `마쓰다이라 모토야스` still lacks the compact `BD=쓰` visually, appearing effectively as `마 다이라모토야스` in the nameplate;
- therefore the six W0 sites are real/useful width-path counterparts but do not cover the final compact-glyph render decision.

## W1 v0.2n — PREPARED, RUNTIME PENDING

After W0, a missed text-render decision was found at mapped `0x44D9D0`:

```text
and w8,w26,#0xffff
cmp w8,#0x100
b.hs alternate_width_path
mov w19,#8
...
bl 0x44E400
```

For every code below `0x100`, the old path forces width 8 immediately before glyph construction/draw. This is a high-confidence semantic counterpart that W0 did not patch.

W1 is W0 plus exactly one new edit:

```text
mapped 0x44D9D0  : cmp w8,#0x100 -> cmp w8,#0xA1
Eden IPS 0x44DAD0
bytes             : 1F 01 04 71 -> 1F 85 02 71
```

Artifact:

- `W1_Taiko5DX_KR_DBG_FONTWIDTH_RENDER_v0.2n.zip`
- SHA-256 `26fcd1434561b2e02d797079d6d996e5becfe66808e763d0b309ee1db10d44d1`
- W0 records 5,526 -> W1 records 5,527
- original-byte guard and classic-IPS round-trip PASS.

Runtime check: enable W1 alone; verify whether `마쓰다이라 모토야스` regains the compact `쓰`, confirm `나야 스케자에몬` remains correct, and note any spacing/clipping or stability regression.

## Current interpretation

- The old freeze mechanism is dominated by the fixed `+0x100` IPS-coordinate defect.
- Y0 disproves only the narrow eight-site suppression hypothesis for the observed yomi rows; it does not disprove the internal-yomi classification or the policy of preserving yomi internally.
- W0 confirms that the PC A1+ half/fullwidth behavior matters on Switch: it corrected the visible normal two-byte `케/자` issue without destabilizing the tested route.
- W0 not restoring compact `BD=쓰` proves there is at least one additional render/layout decision. Static tracing identifies `0x44D9D0` as the next isolated target, tested by W1.
- Repeated short UI strings remain a separate object-recovery task after the compact-font path is stable.