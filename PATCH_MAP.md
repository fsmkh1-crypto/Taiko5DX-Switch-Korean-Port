# PATCH_MAP

Canonical mapping of PC Korean-patch behavior to Nintendo Switch v1.1.3.

Status values:
- `CONFIRMED`: target/behavior directly established
- `IMPLEMENTED`: present in the current corrected builder/mod path
- `VALIDATE`: mapped/implemented but still requires release validation or broader runtime coverage
- `NEXT`: known requirement, implementation pending
- `DEFER`: investigate when behavior requires it

| Area | PC patch behavior | Switch v1.1.3 target | Status | Notes |
|---|---|---|---|---|
| Eden IPS coordinate | Windows runtime writes process RVAs; not applicable directly | Eden NSO classic IPS image | CONFIRMED | emitted offset = mapped flat offset + `0x100`; pre-P0N2 builds were `0x100` early |
| Runtime page mapper | `EB~F8` -> font pages 49~62 | `GetFontTexIndex` around `0x446420`; rewrite `0x44650C..0x446534` | IMPLEMENTED | correct Eden emitted start `0x44660C`; P0N2/M1A/D5519 routes stable |
| Character segmentation | accepts game 2-byte ranges | `0x446310` | CONFIRMED | `EB~F8` already inside existing `E0~FC` lead range |
| Game-code -> UTF-16 lookup | search 10,036 mapping entries | `0x4305D0` | NEXT | loop still 7,494 at `0x430624`; miss -> `U+25A0` |
| UTF-16 -> game-code lookup | search 10,036 mapping entries | `0x430350` | NEXT | loop still 7,494 at `0x4303AC`; miss -> `0x81A1` |
| Mapping table | 7,494 original + 2,542 Korean | original JP table around `0x799E4E` | NEXT | safe expansion/relocation required for full conversion/input behavior |
| Runtime byte validation | broaden Korean code behavior | counterpart not finalized | NEXT | map by behavior/signature |
| Font page/threshold | PC changes half/fullwidth threshold `0xFF -> 0xA0` for repurposed A1+ compact Korean glyphs | six mapped compares `0x445EAC`, `0x445FC8`, `0x446198`, `0x4472E8`, `0x447344`, `0x447C44` | VALIDATE | W0 changes `cmp w8,#0x100` -> `cmp w8,#0xA1`; source G1T contains valid page-63 `마/츠/다`; runtime pending |
| Description font 1~2 | runtime font/layout adjustment | counterparts not finalized | NEXT | map by behavior/signature |
| UI width 1~4 | Korean width/layout adjustment | counterparts not finalized | NEXT | visual/layout follow-up; some behavior may overlap the width cluster now under W0 test |
| Historical 5,519 inline | same-length PC EXE replacements | Switch homologous rodata objects | VALIDATE | D5519 with corrected offsets reaches early gameplay without freeze; working diagnostic baseline, not release-certified |
| Internal yomi fields | PC patch translates many halfwidth-kana readings | Switch name/yomi tables | VALIDATE | 2,099 D5519 records are halfwidth-kana/NUL fields; Switch policy is preserve original yomi internally |
| Visible yomi line | PC runtime/UI shows translated reading | actual Switch path not yet fully mapped | NEXT | eight direct callers of `0x45B0F8` were confirmed, but Y0 disabling those eight did not suppress the observed protagonist/dialogue rows; do not repeat that narrow attempt |
| Repeated `はい` | `はい` -> `예` | standalone object `0x6A15A5` | NEXT | 7 raw matches but one true standalone object; pointer ref `0x58D0D0`, adjacent to `いいえ` object |
| Repeated date suffixes | `年/月/日` -> `년/월/일` | `0x69785A / 0x68925A / 0x6A3CC6` | NEXT | pooled standalone objects; pointer table `0x59C730..0x59C768` references them consecutively |
| Repeated `城` | `城` -> `성` | standalone pooled object `0x6A15DC` | NEXT | multiple raw substring matches but one standalone object with multiple pointer refs |
| Repeated `清洲` | two padded `清洲` records -> `기요스` | fixed-field objects `0x6AE269`, `0x6AEFE9` | NEXT | exact two-to-two padded matches in place-name/yomi tables; replacements agree |
| Currency `貫/文` | unit translations | multiple standalone/embedded format-string objects | NEXT | do not globally replace raw kanji; map complete format/string objects structurally |
| 56 pointer records | pointer/reference patching | Switch pointer/data refs | NEXT | T5K parsed; correspondence pending |
| 208 RomFS payload items | replacement game data | same relative Switch RomFS paths | VALIDATE | 207 direct replacements used; PC `CWTDAT_JP.TR5` excluded |
| `FONT_JPN.G1T` | 64-page Korean font + compact page-63 glyph reuse | `romfs/FONT/FONT_JPN.G1T` | IMPLEMENTED | original 50 pages; Korean 49~62 plus repurposed compact page-63 single-byte glyph cells |
| `CWTDAT_JP.TR5` | PC Korean changes on PC-sized structure | Switch-native `romfs/CMENU/CWTDAT_JP.TR5` | NEXT | never copy PC file wholesale; reconstruct only validated changes |

## Confirmed page mapper

Mapped target `0x44650C`; Eden emitted start `0x44660C`.

Original:

```text
690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b3f01007108b1891a087d0813007d0011
```

Replacement:

```text
693e08532a8103515f610071680100545f29007168000054407d00110400001440990011020000141f2003d5
```

Logical result: `E0~EA -> 31~41`, `EB~F8 -> 49~62`, `F9 -> fallback`, `FA~FC -> existing 46~48 logic`.

## Font page/threshold mapping

The PC T5K `font_page_limit` descriptor is now understood semantically. It changes a comparison threshold from `0xFF` to `0xA0`, so single-byte values above `0xA0` take the alternate/full-width route. The Korean font's page 63 intentionally repurposes such values for compact Korean glyphs in fixed-length fields.

Concrete example: `松平元康` is replaced in 16 bytes as:

```text
B2 BD AA F3 6B EE 93 20 EF 90 F5 E2 F2 7E F1 B8
```

where page-63 single-byte `B2/BD/AA` are `마/츠/다` and the remainder is normal two-byte Korean `이라 모토야스`.

Six Switch width/layout compare sites use:

```text
1F 01 04 71   cmp w8,#0x100
```

W0 diagnostic changes them to:

```text
1F 85 02 71   cmp w8,#0xA1
```

Mapped sites:

```text
0x445EAC
0x445FC8
0x446198
0x4472E8
0x447344
0x447C44
```

A separate compare around `0x4304F8` belongs to conversion logic and is explicitly excluded.

## T5K121R resource layout

```text
resource size                  613,685 (0x95D35)
header                         0x0000..0x0047
mapping table                  0x0048..0x9D17   (10,036 x 4)
pointer replacement strings    0x9D18..0x9F71   (602 bytes)
runtime helper blob            0x9F72..0xA00F   (158 bytes)
inline patch records            0xA010..0x951BF  (17,103)
pointer patch records           0x951C0..0x9553F (56 x 16)
runtime descriptors             0x95540..end      (11)
```

Target PC EXE: size `18,685,960`, SHA-256 `10C69BAB50D29BAF6311360CAFBF7383716A126A6484D209F5E299E12AB565A2`. The supplied Drive PC EXE does not match and cannot support PC binary-context evidence.

## Historical inline selector and corrected interpretation

Reverified counts:

```text
PC records total                 17,103
unique original patterns          8,713
no Switch match                     186
multiple Switch matches            2,476
unique match outside rodata          528
candidate rodata patterns           5,523
overlap-skipped                         4
historical selected patterns       5,519
PC records covered                  5,521
```

Corrected evidence: P0N2 5,519 true no-ops passes; M1A one real inline passes; D5519 all historical 5,519 real replacements passes into normal early gameplay. The set is a useful diagnostic baseline, but `unique exact match` remains insufficient as release-safety proof.

## Yomi mapping policy and Y0 result

D5519 contains 2,099 halfwidth-kana/NUL yomi-like historical inline fields and 3,420 other inline records. Policy remains to preserve original internal Japanese yomi and avoid translating it solely for display.

Eight real direct yomi-enable call sites to shared routine `0x45B0F8` were identified, but Y0 runtime testing showed that zeroing those eight sites did **not** remove the garbled reading rows observed in protagonist selection and dialogue nameplates. Their static mapping remains valid, but the observed rows use another/indirect path. Actual visible-row suppression is still NEXT.

## Repeated-object recovery rule

Recover a repeated pattern only when PC replacements agree, Switch object boundary/field is independently established, substring hits inside longer strings are excluded, pointer/relocation/stride evidence supports the object, pooling has no replacement conflict, no incompatible overlap remains, and the emitted IPS round-trips under `mapped+0x100`.

Current high-confidence objects are documented in `docs/POST_D5519_ANALYSIS.md` and reproduced by `builder/repeated_token_probe.py`.

## Mapping counts

```text
Original JP mapping : 7,494 (0x1D46)
Korean additions    : 2,542
Total                : 10,036 (0x2734)
```

The newline mapping belongs to the original mapping and is not a Korean-added entry.