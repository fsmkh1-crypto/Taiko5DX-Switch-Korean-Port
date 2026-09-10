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
5. The tested Matsudaira nameplate lacks `쓰`; this is no longer established as compact/fixed-field glyph loss because later static evidence shows the historical selector did not patch the duplicated `松平元康` fixed fields. The earlier `케/자` appearance change in `나야 스케자에몬` under W0 remains an observation, not a settled causal proof for the A1+ single-byte threshold family.

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

Therefore the eight call sites are genuine static yomi-enable sites but the narrow suppression hypothesis is incomplete. Do not repeat the same eight-site-only attempt. Keep internal yomi preserved while the actual visible-row path is traced later.

## 4. Compact Korean single-byte mechanism — corrected mapping

T5K R9751/R9752 replace padded `松平元康` with exactly 16 bytes:

```text
B2 BD AA F3 6B EE 93 20 EF 90 F5 E2 F2 7E F1 B8
```

Correct compact mapping:

```text
B2 = 마
BD = 쓰
AA = 다
F36B = 이
EE93 = 라
20   = space
EF90 F5E2 F27E F1B8 = 모토야스
```

Thus the intended Korean display is **`마쓰다이라 모토야스`**. Earlier project text that called the second compact glyph `츠` was a transcription error, not a change in source data.

Direct BC3 decoding of the exact Korean `FONT_JPN.G1T` shows valid page-63 glyph art for `마/쓰/다`. Normal two-byte `케` (`F568`) and `자` (`F379`) glyphs are also correct. Source font art is not the defect.

## 5. PC `font_page_limit` and W0

The PC T5K runtime descriptor `font_page_limit` changes comparison threshold `0xFF -> 0xA0`, making single-byte codes above `0xA0` use the alternate/full-width path.

W0 v0.2m ports six Switch width/layout decisions:

```text
0x445EAC
0x445FC8
0x446198
0x4472E8
0x447344
0x447C44
```

Each changes:

```text
cmp w8,#0x100 -> cmp w8,#0xA1
```

Runtime result:

- stable on the tested route;
- `나야 스케자에몬` renders `케/자` correctly in W0;
- the tested Matsudaira nameplate still lacks `쓰` visually.

These observations remain valid. The former causal interpretation is downgraded: `케/자` are normal two-byte Korean codes rather than direct A1+ single-byte targets, and the Matsudaira observation did not establish that compact `BD=쓰` was present in the active name string reaching the renderer.

Artifact:

- `W0_Taiko5DX_KR_DBG_FONTWIDTH_A1_v0.2m.zip`
- SHA-256 `e453d5958793748ebf841f295ef4005a9a612fdbe643439fe9c2a2c0183ea2ad`
- final IPS records 5,526.

## 6. Why basic byte decoding is not dropping `BD`

Switch function around mapped `0x445C60` performs per-character decoding in the JP path. It recognizes `0x81..0x9F` and `0xE0..0xFC` as two-byte leads, while `0xA1..0xDF` falls through as a valid one-byte code.

Therefore, if compact `BD=쓰` reaches this decode layer, it is not simply rejected or consumed as an invalid byte. This static fact remains valid, but the later W1 result shows that the tested Matsudaira symptom cannot be used to prove such a byte was actually entering this renderer.

## 7. W1: render-width gate exists, direct-cause hypothesis invalidated

Further disassembly found a text-render decision at mapped `0x44D9D0` that W0 did not include:

```text
0x44D9C4  and w8,w26,#0xffff
0x44D9D0  cmp w8,#0x100
0x44D9D4  b.hs 0x44D9E0
0x44D9D8  mov w19,#8
0x44D9E0  ... alternate/table width path ...
0x44DA30  bl 0x44E400
```

The static control flow is real: codes below `0x100` take the width-8 path before glyph construction/draw.

W1 v0.2n is W0 plus only:

```text
mapped 0x44D9D0 : cmp w8,#0x100 -> cmp w8,#0xA1
Eden IPS 0x44DAD0
bytes: 1F 01 04 71 -> 1F 85 02 71
```

Artifact:

- `W1_Taiko5DX_KR_DBG_FONTWIDTH_RENDER_v0.2n.zip`
- SHA-256 `26fcd1434561b2e02d797079d6d996e5becfe66808e763d0b309ee1db10d44d1`
- W0 base records 5,526 -> W1 5,527
- original-byte guard and emitted-IPS round-trip PASS.

Runtime result on 2026-09-11: the tested Matsudaira nameplate still appears without `쓰`. Therefore the prior hypothesis that `0x44D9D0` was the direct cause of the missing compact `쓰` symptom is invalidated.

Subsequent static inspection found two corresponding Switch `松平元康` fixed fields at mapped `0x729D4D` and `0x729D5E`. The historical D5519 unique-only selector patched neither because the same original pattern occurs twice. By contrast, the preceding `松平竹千代` occurrence was unique and therefore selected.

Accordingly, the prior premise that an active compact `BD=쓰` byte was reaching the tested nameplate renderer was not established. Do not repeat W1 as a compact-`쓰` fix until the actual event/person ID -> current name/alias slot -> rendered name path is established.

## 8. Repeated short strings

Historical unique-only matching is too conservative for short objects because raw bytes also occur inside longer prose. Recover actual Switch string objects, not every raw substring.

High-confidence objects:

- `はい -> 예`: standalone object `0x6A15A5`, pointer ref `0x58D0D0`;
- `年/月/日 -> 년/월/일`: pooled objects `0x69785A / 0x68925A / 0x6A3CC6`, consecutive pointer-table registration around `0x59C730..0x59C768`;
- `城 -> 성`: pooled standalone object `0x6A15DC`;
- `清洲 -> 기요스`: fixed-field objects `0x6AE269`, `0x6AEFE9`.

PC replacements agree for each recovered object. Currency `貫/文` remains separate because many uses are embedded in longer format strings.

## 9. Repeated-object recovery rule

A repeated pattern may be recovered only when:

1. relevant PC replacements agree;
2. Switch object boundaries/field structure are independently established;
3. substring hits inside longer strings are excluded;
4. pointer/relocation/stride evidence supports the selected object;
5. pooling creates no replacement conflict;
6. no incompatible overlap remains;
7. emitted IPS uses `mapped+0x100` and round-trips back to the intended mapped object.

## 10. Immediate next analysis sequence

1. Establish the actual protagonist/nameplate data path: event/person ID -> current name/alias slot -> rendered name object.
2. Survey duplicated person-name/renaming/alias fixed slots skipped by historical unique-only matching, grounded in the PC patch's actual replacement bytes.
3. Report the full affected root-cause family before proposing any new patch or diagnostic build.
4. Separately continue the visible-yomi-row path, repeated-object recovery, currency format objects, conversion-table expansion, remaining runtime descriptors/pointers, and Switch-native CWTDAT work according to project priority.

No new patch/build is authorized by this analysis update.