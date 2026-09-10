# PATCH_MAP

Canonical mapping of PC Korean-patch behavior to Nintendo Switch v1.1.3.

Status values:
- `CONFIRMED`: target and behavior are directly established
- `IMPLEMENTED`: present in current builder/mod path and not currently invalidated by runtime evidence
- `VALIDATE`: implementation/mapping exists or is understood, but must pass the normative validation policy before release use
- `NEXT`: known requirement, Switch implementation still pending
- `DEFER`: investigate only when required by behavior or later integration

| Area | PC patch behavior | Switch v1.1.3 target | Status | Notes |
|---|---|---|---|---|
| Runtime page mapper | `EB~F8` -> font pages 49~62 | `GetFontTexIndex` around `0x446420`; rewrite `0x44650C..0x446534` | IMPLEMENTED | NO-INLINE runtime baseline boots and renders Korean title with this active |
| Character segmentation | accepts game 2-byte ranges | `0x446310` | CONFIRMED | `EB~F8` is inside existing `E0~FC` lead range |
| Game-code -> UTF-16 lookup | search 10,036 mapping entries | `0x4305D0` | NEXT | Switch loop still uses 7,494 at `0x430624`; miss path has defined `U+25A0` fallback, so missing expansion is a functional gap but not yet proven as direct freeze cause |
| UTF-16 -> game-code lookup | search 10,036 mapping entries | `0x430350` | NEXT | Switch loop still uses 7,494 at `0x4303AC`; miss path has defined `0x81A1` fallback |
| Mapping table | 7,494 original + 2,542 Korean = 10,036 | original JP table around mapped `0x799E4E` | NEXT | expansion/relocation required; do not overwrite neighboring language data blindly |
| Runtime byte validation | broaden valid Korean code behavior | Switch counterpart not finalized | NEXT | Phase 0 prerequisite analysis priority after mapping lookup |
| Font page/threshold patch | PC runtime changes a byte threshold | Switch counterpart not finalized | NEXT | not a literal page-count patch; Phase 0 analysis target |
| Description font 1~2 | runtime font adjustments | Switch counterparts not finalized | NEXT | map by behavior/signature, not blind RVA conversion |
| UI width 1~4 | text/UI width adjustments | Switch counterparts not finalized | NEXT | locate homologous ARM64 routines; visual/layout priority unless evidence shows crash relevance |
| 17,103 inline records | same-length PC EXE replacements | Switch homologous text/data locations | VALIDATE | old 5,519 exact-unique-rodata selector is superseded as a safety rule; full corpus must follow Phase 0 then `docs/INLINE_VALIDATION_POLICY.md` |
| P0N diagnostic | 5,519 historical inline offsets rewritten with original bytes | Eden classic IPS loader/application path | VALIDATE | build generator verifies 5,519 true no-ops + page mapper, 5,520 records total; runtime result pending |
| 56 pointer records | pointer/reference patching | Switch pointer/data references | NEXT | T5K table parsed; Switch correspondence pending |
| 208 RomFS payload items | replacement data | same relative Switch RomFS paths | VALIDATE | 207 direct replacements work at least through Korean-title baseline; continue runtime coverage; PC `CWTDAT_JP.TR5` excluded |
| `FONT_JPN.G1T` | 64-page Korean font | `romfs/FONT/FONT_JPN.G1T` | IMPLEMENTED | NO-INLINE baseline confirms Korean title rendering; pages 0~48 unchanged, Korean 49~62 |
| `CWTDAT_JP.TR5` | small Korean changes on PC-sized structure | Switch-native `romfs/CMENU/CWTDAT_JP.TR5` | NEXT | never replace whole Switch file with PC file |

## Confirmed page mapper patch

Target offset: `0x44650C`

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

The builder extracts `RT_RCDATA/101` from the PC patch `dinput8.dll` and parses the resource directly.

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

Header fields:

```text
version              1
inline_count         17,103
pointer_count        56
runtime_count        11
prefix_size          0x9F2A
runtime_blob_size    0x9E
target PC EXE size   18,685,960
target PC EXE SHA256 10C69BAB50D29BAF6311360CAFBF7383716A126A6484D209F5E299E12AB565A2
```

The current Drive `PC_Original/Taiko5DX.exe` does **not** match this target identity and therefore cannot be used as PC-RVA context evidence. See `docs/VALIDATION_LEDGER.md` V012.

## Inline mapping: old selector and current rule

Historical selector result, reverified on the fixed inputs:

```text
PC records total                 17,103
unique original patterns          8,713
no Switch match                     186
multiple Switch matches            2,476
unique match outside rodata          528
candidate rodata patterns           5,523
overlap-skipped                         4
old selected unique patterns       5,519
PC records covered                  5,521
```

Runtime evidence invalidated the assumption that this rule is sufficient for safe inclusion:

- integrated set freezes;
- NO-INLINE baseline boots and renders Korean title;
- address-half A freezes;
- address-half B reaches title and then crashes on input.

Therefore the 5,519-set is a **reference/regression corpus only**, not a SAFE set.

Before implementing the full semantic validator, follow `docs/PHASE0_FAILURE_MODE_PLAN.md` to distinguish candidate-specific faults from IPS/build/runtime prerequisites. After Phase 0, all candidate classification follows `docs/INLINE_VALIDATION_POLICY.md`.

## Mapping counts

```text
Original JP mapping : 7,494 (0x1D46)
Korean additions    : 2,542
Total                : 10,036 (0x2734)
```

The newline mapping already belongs to the original mapping and must not be counted as an added Korean entry.
