# POST-D5519 ANALYSIS

Canonical analysis after the corrected-offset full-inline diagnostic build `D5519 v0.2k` was runtime-tested in Eden Android.

## 1. Runtime result that changes project direction

`D5519 v0.2k` re-ran the historical 5,519 exact-unique inline replacement set with the Eden NSO IPS coordinate corrected from `X` to `X + 0x100`.

Observed early-game route: boot, title, main menu, scenario selection/description, protagonist selection, and entry into normal gameplay all PASS; no freeze or forced exit was observed.

This strongly attributes the old immediate freezes to the missing `+0x100` IPS coordinate shift. It does not certify all 5,519 historical candidates for every late-game path.

## 2. Visible anomaly classes

Screenshots establish separate problems that must not be conflated:

1. Korean main names/text broadly work.
2. Small auxiliary reading/yomi rows render as garbled kana/Latin-like glyphs.
3. Repeated short UI tokens remain Japanese in some places (`はい`, date/currency suffixes, `城`).
4. Repeated location components such as `清洲` remain Japanese because the historical selector rejected non-unique matches.
5. Some fixed-field Korean names show glyph/spacing defects: `마츠다이라 모토야스` loses `츠` in a nameplate; `나야 스케자에몬` shows user-observed odd appearance around `케/자`.

## 3. Yomi policy and Y0 result

For the Switch Korean port, preserve original Japanese halfwidth-kana yomi internally where possible because it may participate in sorting/comparison/input. Do not translate internal yomi merely to show a redundant reading line when the main name is already Korean.

D5519 classification:

```text
real inline records                         5,519
halfwidth-kana/NUL yomi-like fields         2,099
non-yomi historical inline                  3,420
```

A shared name/yomi drawing routine exists at mapped `0x45B0F8`. Eight direct callers explicitly enable an auxiliary reading line with `mov w6,#1`:

```text
0x2A0ABC
0x2A565C
0x2A6F4C
0x2A7720
0x2A7FE4
0x2ADE5C
0x2BC1A0
0x2BD5C8
```

Y0 v0.2l restored the 2,099 internal yomi fields to original Switch bytes and changed those eight enables to zero. Runtime remained stable, but **the garbled small reading rows visible in protagonist selection and dialogue nameplates remained present**.

Therefore:

- the eight call sites are genuine static yomi-enable sites;
- they are not sufficient to control the two observed UI rows, or an additional wrapper/renderer draws those rows;
- the narrow Y0 suppression hypothesis is invalid/incomplete;
- do not repeat the same eight-site-only attempt;
- keep the internal-yomi preservation policy while actual visible-row tracing is deferred behind the higher-value compact-font test.

## 4. Compact Korean single-byte mechanism: root cause candidate for missing `츠`

The user-observed missing `츠` in `마츠다이라 모토야스` is not a transliteration choice and not a missing byte in the PC replacement.

T5K records R9751/R9752 replace padded `松平元康` with exactly 16 bytes:

```text
B2 BD AA F3 6B EE 93 20 EF 90 F5 E2 F2 7E F1 B8
```

The first three bytes are not normal two-byte Korean codes. The Korean G1T deliberately repurposes page-63 single-byte cells:

```text
B2 = 마
BD = 츠
AA = 다
```

The remainder is normal two-byte Korean:

```text
F36B = 이
EE93 = 라
20   = space
EF90 F5E2 F27E F1B8 = 모토야스
```

This compact form is necessary because the full normal two-byte spelling would not fit the 16-byte field.

Direct BC3 decoding of the exact Korean `FONT_JPN.G1T` shows that page-63 cells `B2`, `BD`, and `AA` contain correct `마/츠/다` glyph artwork. The normal two-byte cells for `케` (`F568`) and `자` (`F379`) are also correct. Therefore the source font atlas itself is not corrupt.

The runtime screenshot is especially diagnostic: `마` and `다` render while the middle compact `츠` is effectively missing. The remaining task is runtime classification/width/layout behavior.

## 5. PC `font_page_limit` semantics and Switch counterpart

The PC T5K runtime descriptor named `font_page_limit` is now decoded semantically. It modifies the comparison threshold from `0xFF` to `0xA0`, causing single-byte codes above `0xA0` to take the alternate/full-width path. It is not a literal font-page-count patch.

The Switch v1.1.3 font/width cluster contains a matching semantic decision: several routines compare a character code against `0x100` and select the halfwidth path for values below that threshold.

Six confirmed equivalent/inlined sites are:

```text
0x445EAC
0x445FC8
0x446198
0x4472E8
0x447344
0x447C44
```

Each original instruction is:

```text
1F 01 04 71   cmp w8,#0x100
```

The PC-equivalent Switch threshold is:

```text
1F 85 02 71   cmp w8,#0xA1
```

so `0x00..0xA0` remains on the halfwidth side and `0xA1+` takes the alternate/full-width side.

A different `cmp #0x100` around mapped `0x4304F8` belongs to conversion logic and must not be included in this patch family.

## 6. W0 diagnostic

`W0 v0.2m` uses D5519 as the baseline and adds only the six threshold edits above.

Artifact:

- `W0_Taiko5DX_KR_DBG_FONTWIDTH_A1_v0.2m.zip`
- SHA-256 `e453d5958793748ebf841f295ef4005a9a612fdbe643439fe9c2a2c0183ea2ad`
- D5519 base records: 5,520
- added width/layout records: 6
- final IPS records: 5,526
- all original-instruction guards PASS;
- no D5519 record collision;
- emitted classic IPS exact round-trip PASS.

Reproducible builder: `builder/build_w0_fontwidth.py`.

Runtime test must answer three narrow questions:

1. does `마츠다이라 모토야스` regain the missing `츠`?
2. does `나야 스케자에몬` improve or change around `케/자`?
3. are there regressions in general spacing or halfwidth Japanese UI text?

W0 is diagnostic until those runtime observations are recorded.

## 7. Repeated short strings: why the old selector misses them

The historical selector rejects a pattern whenever its raw byte sequence appears more than once anywhere in the flat image. This is too conservative for short Japanese strings because their bytes also occur as substrings inside longer prose.

### `はい` -> `예`

- one intended T5K record;
- 7 raw rodata byte matches;
- exactly one standalone NUL-delimited string object at mapped `0x6A15A5`;
- pointer reference at `0x58D0D0`;
- adjacent pointer-table object is `いいえ`, already translated to `아니오` by the historical selector.

### `年 / 月 / 日`

Standalone pooled objects:

```text
年  0x69785A
月  0x68925A
日  0x6A3CC6
```

Pointer table `0x59C730..0x59C768` references them consecutively. Multiple PC records agree on `년/월/일`, so the many-PC-to-one-Switch pooling is non-conflicting.

### `城`

T5K has two `城` -> `성` records. Switch has one standalone pooled `城` object at mapped `0x6A15DC` with multiple references. PC replacements agree.

### `清洲`

T5K has two padded `清洲\0\0` records with identical replacement `기요스`. Switch has exactly two corresponding padded fixed-field occurrences:

```text
0x6AE269
0x6AEFE9
```

Both lie in fixed-stride place-name/yomi tables.

## 8. Currency/date unit policy

The PC T5K contains explicit translations `年->년`, `月->월`, `日->일`, `貫->관`, `文->문`, `はい->예`, `いいえ->아니오`.

Do not globally replace raw one/two-character byte sequences. Currency units in particular occur inside multiple longer format strings such as `%d貫` and combined 貫/文 layouts. Recover complete string objects or structurally confirmed fields only.

## 9. Repeated-object recovery rule

A repeated pattern may be recovered only when:

1. relevant PC replacements agree;
2. Switch object boundaries/field structure are independently established;
3. substring hits inside longer strings are excluded;
4. pointer/relocation/stride evidence supports the selected object;
5. pooling creates no replacement conflict;
6. no incompatible overlap remains;
7. emitted IPS uses `mapped+0x100` and round-trips back to the intended mapped object.

## 10. Immediate implementation sequence

1. Runtime-test W0 before adding repeated short-string recovery so the font-width variable stays isolated.
2. If W0 fixes the compact `츠` path without regressions, promote the six-site threshold behavior into the integrated builder.
3. If `케/자` remain visually wrong, investigate their two-byte UI-specific advance/scaling path separately; the G1T glyph cells are already verified correct.
4. Recover high-confidence repeated objects (`はい`, pooled `年/月/日`, pooled `城`, both `清洲` fields).
5. Map `貫/文` complete format objects separately.
6. Return to the actual visible yomi-row draw path after higher-impact name/font issues are stable.
7. Keep the full 17,103 validator as release audit/recovery, not as the explanation for the resolved pre-P0N2 freeze.