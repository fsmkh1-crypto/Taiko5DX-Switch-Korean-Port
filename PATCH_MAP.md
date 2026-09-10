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
| Font page/threshold | PC runtime threshold change | counterpart not finalized | NEXT | not a literal page-count constant |
| Description font 1~2 | runtime font/layout adjustment | counterparts not finalized | NEXT | map by behavior/signature |
| UI width 1~4 | Korean width/layout adjustment | counterparts not finalized | NEXT | visual/layout follow-up |
| Historical 5,519 inline | same-length PC EXE replacements | Switch homologous rodata objects | VALIDATE | D5519 with corrected offsets reaches early gameplay without freeze; set is now a working diagnostic baseline, not release-certified |
| Internal yomi fields | PC patch translates many halfwidth-kana readings | Switch name/yomi tables | VALIDATE | 2,099 D5519 records are halfwidth-kana/NUL fields; Switch policy is preserve original yomi internally, do not translate for display |
| Visible yomi line | PC runtime/UI shows translated reading | shared Switch name/yomi renderer `0x45B0F8` and 8 callers | VALIDATE | Y0 changes eight `mov w6,#1` enables to zero; runtime pending |
| Repeated `はい` | `はい` -> `예` | standalone object `0x6A15A5` | NEXT | 7 raw matches but one true standalone object; pointer ref `0x58D0D0`, adjacent to `いいえ` object |
| Repeated date suffixes | `年/月/日` -> `년/월/일` | `0x69785A / 0x68925A / 0x6A3CC6` | NEXT | pooled standalone objects; pointer table `0x59C730..0x59C768` references them consecutively |
| Repeated `城` | `城` -> `성` | standalone pooled object `0x6A15DC` | NEXT | multiple raw substring matches but one standalone object with multiple pointer refs |
| Repeated `清洲` | two padded `清洲` records -> `기요스` | fixed-field objects `0x6AE269`, `0x6AEFE9` | NEXT | exact two-to-two padded matches in place-name/yomi tables; replacements agree |
| Currency `貫/文` | unit translations | multiple standalone/embedded format-string objects | NEXT | do not globally replace raw kanji; map complete format/string objects structurally |
| 56 pointer records | pointer/reference patching | Switch pointer/data refs | NEXT | T5K parsed; correspondence pending |
| 208 RomFS payload items | replacement game data | same relative Switch RomFS paths | VALIDATE | 207 direct replacements used; PC `CWTDAT_JP.TR5` excluded |
| `FONT_JPN.G1T` | 64-page Korean font | `romfs/FONT/FONT_JPN.G1T` | IMPLEMENTED | original 50 pages; Korean pages 49~62 added |
| `CWTDAT_JP.TR5` | PC Korean changes on PC-sized structure | Switch-native `romfs/CMENU/CWTDAT_JP.TR5` | NEXT | never copy PC file wholesale; reconstruct only validated changes |

## Confirmed page mapper

Mapped target: `0x44650C`; Eden emitted start: `0x44660C`.

Original:

```text
690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b3f01007108b1891a087d0813007d0011
```

Replacement:

```text
693e08532a8103515f610071680100545f29007168000054407d00110400001440990011020000141f2003d5
```

Logical result:

```text
E0~EA -> 31~41
EB~F8 -> 49~62
F9    -> reject/fallback path
FA~FC -> existing 46~48 logic
```

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

Target PC EXE identity:

```text
size    18,685,960
SHA-256 10C69BAB50D29BAF6311360CAFBF7383716A126A6484D209F5E299E12AB565A2
```

The current Drive `PC_Original/Taiko5DX.exe` does not match this identity and cannot be used for PC binary-context evidence.

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

The earlier conclusion that the 5,519 set itself caused immediate freeze was superseded after the Eden coordinate defect was found.

Corrected evidence:

- P0N2: 5,519 true no-ops + corrected mapper -> PASS through main menu.
- M1A: one real corrected inline -> PASS through scenario/protagonist flow.
- D5519: all historical 5,519 real replacements + corrected mapper -> PASS into normal early gameplay without freeze/forced exit on tested route.

Therefore the 5,519 set is a useful working diagnostic baseline, but `unique exact match` remains insufficient as a release-safety proof.

## Yomi mapping policy

D5519 classification:

```text
historical real inline                  5,519
halfwidth-kana/NUL yomi-like fields     2,099
non-yomi historical inline              3,420
```

Switch policy:

1. preserve original internal Japanese yomi;
2. keep Korean main names;
3. suppress the unnecessary visible reading line.

Eight mapped yomi-enable call sites:

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

Each has original `26 00 80 52` (`mov w6,#1`) before a nearby BL to shared routine `0x45B0F8`. Y0 diagnostic replaces with `E6 03 1F 2A` (`mov w6,wzr`).

## Repeated-object recovery rule

Raw short-string match count is not object count. Recover a repeated pattern only when:

- PC replacements agree;
- Switch object boundary/field is independently established;
- substring hits inside longer strings are excluded;
- pointer/relocation/stride evidence supports the selected object;
- many-PC-to-one-Switch pooling has no replacement conflict;
- no overlap/conflict remains;
- IPS output round-trips through the `+0x100` coordinate conversion.

Current high-confidence objects are documented in `docs/POST_D5519_ANALYSIS.md` and reproducible with `builder/repeated_token_probe.py`.

## Mapping counts

```text
Original JP mapping : 7,494 (0x1D46)
Korean additions    : 2,542
Total                : 10,036 (0x2734)
```

The newline mapping belongs to the original mapping and is not a Korean-added entry.