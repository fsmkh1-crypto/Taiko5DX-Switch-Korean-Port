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
| W0 v0.2m | D5519 + six A1+ fullwidth-threshold patches | **Observed stable; `케/자` render normally; tested Matsudaira name still lacks `쓰`** |
| W1 v0.2n | W0 + render-width gate change at mapped `0x44D9D0` | **NO FIX: tested Matsudaira name still lacks `쓰`; direct-cause hypothesis invalidated** |
| DCTRL7 | mapper + V019 R489 control + 5 repeated-object records | **PARTIAL PASS: scenario `1560年 -> 1560년`; tested `岡崎城` unchanged; in-game HUD date reported unchanged** |

## DCTRL7 — CURRENT DELIVERY CONTROL / REPEATED-OBJECT DISCRIMINATOR

Artifact:

- builder source commit `ccb13b3e85b8a72339b628f57bf12dda789fffe3`;
- IPS SHA-256 `2114f14ccc098103524b7cb4afaf416a8bc0185bc607dd198ce4f9511d2d6fab`;
- package `DCTRL7_Taiko5DX_KR_EDEN.zip`;
- package SHA-256 `c1092c6cb43da985a536c94dd01f132516540af35232f11d634e1afc0341fb33`;
- 7/7 guards PASS, no skips/extras, exact self-reparse and `mapped+0x100` round-trip PASS;
- Drive-retained package was redownloaded byte-identical before runtime use.

Runtime on Eden Android v0.2.1:

- scenario-selection display changed `1560年 日輪の章` to `1560년 日輪の章`;
- this establishes runtime delivery/consumption of DCTRL7's standalone `年` record at mapped `0x69785A` on that route and proves the Korean font/page-mapper can render the replacement;
- protagonist basic-information screen still showed `拠点 岡崎城` even though DCTRL7 includes standalone `城 @ 0x6A15DC -> 성`, so that standalone record is not sufficient for the tested screen;
- user reported the in-game HUD still showed `1560年 2月30日`; this HUD observation has narrower evidence because no DCTRL7 HUD screenshot was retained in the R0 documentation session;
- R489, standalone `月`, standalone `日`, and `はい` were not directly exposed on the supplied DCTRL7 route and must not be classified as failures.

Retained screenshots:

- scenario `1560년`: `DCTRL7_01_scenario_1560nyeon.jpg`, Drive ID `17XlqbJWd5aaEAUtsV0QRedPRNkKcPctR`, SHA-256 `5dc08060b4e0d18eecc962a7512347486b2253e20d2a1d9a5b361efa11e5f75f`;
- unchanged `岡崎城`: `DCTRL7_02_basic_info_okazaki_castle_jp.jpg`, Drive ID `1eY4pPcBP80HnDfkSfodPTX5oi_C7ppjj`, SHA-256 `76a450b0770ab155c85f0e4272bc51bbe80daac78e5b764975f834dcd8bf25bb`.

Canonical consequence: the current feedback loop is restored for the tested `年 @ 0x69785A` path. Global DCTRL7/ExeFS delivery failure is rejected. The remaining repeated-object work is now a source/consumer-coverage problem, not a reason to reopen the current artifact-delivery chain. Detailed record: `docs/diagnostics/DCTRL7_RUNTIME_RESULT.md`.

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
- the tested Matsudaira nameplate lacks `쓰`; later static evidence shows the historical unique-only selector did not patch the duplicated `松平元康` fixed fields, so this symptom is no longer established as compact-glyph loss inside the renderer.

## Y0 v0.2l — STABLE, TARGET SUPPRESSION FAILED

Artifact SHA-256 `ae67b2bdece0e261239a3a505ad018761904c25124f0857cf0a917f9a4a6c869`.

Y0 restores 2,099 halfwidth-kana yomi-like fields to original Switch bytes, retains 3,420 other historical inline replacements, and changes eight known direct `mov w6,#1` yomi-enable call sites to zero before shared routine `0x45B0F8`.

Runtime result on 2026-09-11:

- game remains stable on the tested route;
- Korean main names remain;
- **the garbled small reading rows visible in protagonist selection and dialogue nameplates remain present**.

Therefore the eight call sites are real static yomi-enable sites, but they do not control the observed two UI rows, or an additional wrapper/path re-enables/draws them. Do not repeat the same eight-site-only suppression attempt. Internal-yomi preservation remains the safer data policy while the actual visible-row path is traced later.

## W0 v0.2m — OBSERVATION RETAINED, CAUSALITY DOWNGRADED

Artifact SHA-256 `e453d5958793748ebf841f295ef4005a9a612fdbe643439fe9c2a2c0183ea2ad`.

W0 ports six Switch width/layout thresholds from `code < 0x100` to `code < 0xA1`, corresponding structurally to the PC `font_page_limit` behavior for repurposed page-63 compact Korean bytes.

Static compact-name evidence for the PC patch's `松平元康` replacement:

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
- `나야 스케자에몬` renders the previously odd `케/자` normally in W0;
- the tested Matsudaira nameplate still lacks `쓰` visually.

These are valid observations. The earlier causal interpretation is now downgraded: `케/자` are normal two-byte Korean codes rather than direct A1+ single-byte targets, and the Matsudaira observation did not establish that compact `BD=쓰` was actually present in the active source string reaching the renderer.

## W1 v0.2n — RUNTIME TESTED, DIRECT-CAUSE HYPOTHESIS INVALIDATED

W1 changed one additional text-render decision at mapped `0x44D9D0` on top of W0:

```text
and w8,w26,#0xffff
cmp w8,#0x100
b.hs alternate_width_path
mov w19,#8
...
bl 0x44E400
```

W1 edit:

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

Runtime result on 2026-09-11:

- the tested Matsudaira nameplate still appears without `쓰`;
- therefore changing `0x44D9D0` does not directly fix the symptom and the prior W1 causal hypothesis is invalidated.

The static gate itself remains real. However, subsequent static inspection found two corresponding Switch `松平元康` fixed fields at mapped `0x729D4D` and `0x729D5E`, and the historical D5519 unique-only selector patched neither because the original pattern occurs twice. Accordingly, the prior premise that a compact `BD=쓰` byte was reaching the tested renderer was not established.

Do not repeat W1 as a compact-`쓰` fix without first establishing the actual event/person -> current-name/alias-slot -> rendered-name path.

## Current interpretation

- The old freeze mechanism is dominated by the fixed `+0x100` IPS-coordinate defect.
- DCTRL7 restores the current feedback loop for standalone `年 @ 0x69785A` and proves repeated-object failures now need consumer/source analysis rather than a global delivery explanation.
- Y0 disproves only the narrow eight-site suppression hypothesis for the observed yomi rows; it does not disprove the internal-yomi classification or the policy of preserving yomi internally.
- W0 runtime observations remain valid, but direct causality between the A1+ threshold changes and the `케/자` correction is not established.
- W1 disproves the narrow claim that mapped `0x44D9D0` is the direct cause of the missing `쓰` symptom.
- The Matsudaira symptom must not be treated as proof of compact-glyph render loss until the active name slot/data selection path is established; duplicated `松平元康` fixed fields were skipped by the historical unique-only selector.
- Repeated short UI strings are now tracked through R0's RELA/registry/place-table structure rather than universal standalone-token assumptions.
