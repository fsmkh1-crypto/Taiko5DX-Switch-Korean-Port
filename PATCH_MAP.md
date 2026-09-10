# PATCH_MAP

Canonical mapping of PC Korean-patch behavior to Nintendo Switch v1.1.3.

Status values:
- `CONFIRMED`: target and behavior are directly established
- `IMPLEMENTED`: present in current builder/mod path
- `NEXT`: known requirement, Switch implementation still pending
- `DEFER`: only investigate if runtime testing proves it necessary

| Area | PC patch behavior | Switch v1.1.3 target | Status | Notes |
|---|---|---|---|---|
| Runtime page mapper | `EB~F8` -> font pages 49~62 | `GetFontTexIndex` around `0x446420`; rewrite `0x44650C..0x446534` | IMPLEMENTED | 44-byte in-place ARM64 rewrite; no cave needed |
| Character segmentation | accepts game 2-byte ranges | `0x446310` | CONFIRMED | `EB~F8` already falls inside existing `E0~FC` lead range; no basic patch needed |
| Game-code -> UTF-16 lookup | search 10,036 mapping entries | `0x4305D0` | NEXT | Switch currently uses 7,494-entry JP table |
| UTF-16 -> game-code lookup | search 10,036 mapping entries | `0x430350` | NEXT | Switch currently uses 7,494-entry JP table |
| Mapping table | 7,494 original + 2,542 Korean = 10,036 | original JP table around mapped `0x799E4E` | NEXT | Expansion/relocation required; do not overwrite neighboring language data until xrefs are mapped |
| Runtime byte validation | broaden valid Korean code behavior | Switch counterpart not finalized | NEXT | Keep separate from segmentation function |
| Font page/threshold patch | PC runtime changes a byte threshold | Switch counterpart not finalized | NEXT | Earlier description as literal page count was inaccurate; treat as threshold logic |
| Description font 1 | runtime font adjustment | Switch counterpart not finalized | NEXT | Map by function/signature, not blind RVA conversion |
| Description font 2 | runtime font adjustment | Switch counterpart not finalized | NEXT | Same |
| UI width 1~4 | text/UI width adjustments | Switch counterparts not finalized | NEXT | Port after locating homologous ARM64 routines |
| 17,103 inline records | same-length EXE byte replacements | Switch `main` homologous locations | NEXT | Build automated context/signature matching; do not treat as one injected blob |
| 56 pointer records | pointer/reference patching | Switch pointer/data references | NEXT | Small set; port in same integrated build |
| 208 RomFS payload items | replacement data | same relative Switch RomFS paths | CONFIRMED | All 208 relative paths exist on Switch |
| `FONT_JPN.G1T` | 64-page Korean font | `romfs/FONT/FONT_JPN.G1T` | IMPLEMENTED | pages 0~48 unchanged; Korean 49~62 |
| `CWTDAT_JP.TR5` | small Korean changes on PC-sized structure | Switch-native `romfs/CMENU/CWTDAT_JP.TR5` | NEXT | Never drop whole PC file onto Switch; reconstruct changes onto Switch base |

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

## Mapping counts

```text
Original JP mapping : 7,494 (0x1D46)
Korean additions    : 2,542
Total                : 10,036 (0x2734)
```

The newline mapping already belongs to the original 7,494 and must not be counted as an added Korean entry.
