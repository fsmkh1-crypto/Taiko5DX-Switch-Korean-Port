# PATCH_MAP

Canonical mapping of PC Korean-patch behavior to Nintendo Switch v1.1.3.

## PC-side PHASE 1 framework reference

`docs/PC_RUNTIME_REVERSE_ENGINEERING.md` records the PC-only framework with DLL RVAs.
DllMain `0x8E10` stores module state; DirectInput8Create `0x8BD0` triggers patch once
`0x8710` → initializer `0x7870`. Resource parse and disk/memory identity gates precede
private storage preparation `0x6130`, staging `0x6490`, and commit `0x5980`.
Prefix/helper share one contiguous allocation. Commit uses preimage-guarded staged
writes and best-effort rollback; complete atomic restoration is not guaranteed.
No Switch counterpart was investigated or changed for this PHASE 1 record.

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
| Compact A1+ byte decode | accepts compact single-byte Korean codes | JP per-character decode around `0x445C60` | CONFIRMED | native path already accepts `A1..DF` as one-byte values; if `BD=쓰` reaches this layer it is not dropped at basic decode |
| Game-code -> UTF-16 lookup | search 10,036 mapping entries | `0x4305D0` | NEXT | loop still 7,494 at `0x430624`; miss -> `U+25A0` |
| UTF-16 -> game-code lookup | search 10,036 mapping entries | `0x430350` | NEXT | loop still 7,494 at `0x4303AC`; miss -> `0x81A1` |
| Mapping table | 7,494 original + 2,542 Korean | original JP table around `0x799E4E` | NEXT | safe expansion/relocation required for full conversion/input behavior |
| Runtime byte validation | broaden Korean code behavior | counterpart not finalized | NEXT | PC helper explicitly recognizes `A1..DF` single-byte; map by behavior |
| Font page/threshold | PC changes half/fullwidth threshold `0xFF -> 0xA0` for repurposed A1+ compact Korean glyphs | W0 six width/layout compares + W1 render-width compare `0x44D9D0` | VALIDATE | static counterparts exist; W1 runtime did not restore the tested Matsudaira `쓰`, so `0x44D9D0` is not established as the direct cause. Do not infer compact-name causality until active name-slot selection is established |
| Description font 1~2 | runtime font/layout adjustment | counterparts not finalized | NEXT | map by behavior/signature |
| UI width 1~4 | Korean width/layout adjustment | counterparts not finalized | NEXT | some behavior may overlap W0/W1 width cluster; remaining descriptors still need semantic mapping |
| Historical 5,519 inline | same-length PC EXE replacements | Switch homologous rodata objects | VALIDATE | D5519 with corrected offsets reaches early gameplay without freeze; unique-only selection misses duplicated objects including two `松平元康` fixed fields |
| Internal yomi fields | PC patch translates many halfwidth-kana readings | Switch name/yomi tables | VALIDATE | 2,099 D5519 records are halfwidth-kana/NUL fields; Switch policy is preserve original yomi internally |
| Visible yomi line | PC/UI shows auxiliary reading | actual Switch path not yet fully mapped | NEXT | eight direct callers of `0x45B0F8` were confirmed, but Y0 disabling those eight did not suppress observed rows; do not repeat narrow attempt |
| Repeated `はい` | `はい` -> `예` | standalone object `0x6A15A5` | NEXT | 7 raw matches but one true standalone object; pointer ref `0x58D0D0` |
| Repeated date suffixes | `年/月/日` -> `년/월/일` | `0x69785A / 0x68925A / 0x6A3CC6` | NEXT | pooled standalone objects; pointer table `0x59C730..0x59C768` references them consecutively |
| Repeated `城` | `城` -> `성` | standalone pooled object `0x6A15DC` | NEXT | multiple raw substring matches but one standalone object with multiple pointer refs |
| Repeated `清洲` | two padded `清洲` records -> `기요스` | fixed-field objects `0x6AE269`, `0x6AEFE9` | NEXT | exact two-to-two padded matches in place-name/yomi tables; replacements agree |
| Currency `貫/文` | unit translations | multiple standalone/embedded format-string objects | NEXT | do not globally replace raw kanji; map complete format/string objects structurally |
| 56 pointer records | pointer/reference patching | Switch pointer/data refs | NEXT | T5K parsed; correspondence pending |
| 208 RomFS payload items | replacement game data | same relative Switch RomFS paths | VALIDATE | 207 direct replacements used; PC `CWTDAT_JP.TR5` excluded |
| `FONT_JPN.G1T` | 64-page Korean font + compact page-63 glyph reuse | `romfs/FONT/FONT_JPN.G1T` | IMPLEMENTED | page 63 verified: `B2=마`, `BD=쓰`, `AA=다`; normal `케/자` cells also valid |
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

## Compact font-width mapping

PC T5K `松平元康` replacement:

```text
B2 BD AA F3 6B EE 93 20 EF 90 F5 E2 F2 7E F1 B8
```

Correct semantics: `B2/BD/AA = 마/쓰/다`, then normal two-byte `이라 모토야스`. The intended display is `마쓰다이라 모토야스`.

The PC `font_page_limit` descriptor changes threshold `0xFF -> 0xA0`; Switch W0/W1 experiments changed selected `code < 0x100` decisions to `code < 0xA1`.

W0 changes six mapped compares:

```text
0x445EAC  0x445FC8  0x446198
0x4472E8  0x447344  0x447C44
```

`cmp w8,#0x100 -> cmp w8,#0xA1`.

W0 runtime observation: stable; `케/자` in `나야 스케자에몬` render normally; the tested Matsudaira name still lacks `쓰`. Do not treat the `케/자` observation as direct proof of the A1+ single-byte mechanism because those glyphs are normal two-byte Korean codes.

W1 adds one additional text-render decision:

```text
mapped 0x44D9D0 -> Eden IPS 0x44DAD0
cmp w8,#0x100 -> cmp w8,#0xA1
```

W1 runtime on 2026-09-11 did not restore `쓰`. The static gate exists, but the hypothesis that it directly caused the missing `쓰` symptom is invalidated.

Static inspection also established two corresponding Switch `松平元康` fixed fields at mapped `0x729D4D` and `0x729D5E`; historical D5519 unique-only matching selected neither because the original pattern is duplicated. Therefore the earlier assumption that an active compact `BD=쓰` byte was reaching the tested renderer was not established.

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

Reverified counts: 17,103 PC records; 8,713 unique originals; 5,523 unique-rodata candidates; 4 overlap skips; 5,519 historical selected patterns covering 5,521 PC records.

Corrected evidence: P0N2 5,519 true no-ops passes; M1A one real inline passes; D5519 all historical 5,519 real replacements passes into normal early gameplay. The set is a useful diagnostic baseline, but `unique exact match` remains insufficient as release-safety proof and can omit duplicated fixed objects.

## Yomi mapping policy and Y0 result

D5519 contains 2,099 halfwidth-kana/NUL yomi-like historical inline fields and 3,420 other inline records. Policy remains to preserve original internal Japanese yomi and avoid translating it solely for display.

Eight real direct yomi-enable call sites to shared routine `0x45B0F8` were identified, but Y0 runtime testing showed that zeroing those eight sites did not remove the garbled reading rows observed in protagonist selection and dialogue nameplates. Actual visible-row suppression remains NEXT.

## Repeated-object recovery rule

Recover a repeated pattern only when PC replacements agree, Switch object boundary/field is independently established, substring hits inside longer strings are excluded, pointer/relocation/stride evidence supports the object, pooling has no replacement conflict, no incompatible overlap remains, and the emitted IPS round-trips under `mapped+0x100`.

## Mapping counts

```text
Original JP mapping : 7,494 (0x1D46)
Korean additions    : 2,542
Total                : 10,036 (0x2734)
```

The newline mapping belongs to the original mapping and is not a Korean-added entry.
