# PATCH_MAP

Canonical mapping of PC Korean-patch behavior to Nintendo Switch v1.1.3.

Status values:
- `CONFIRMED`: target and behavior are directly established
- `IMPLEMENTED`: present in current builder/mod path
- `PARTIAL`: meaningful safe subset is implemented; remaining cases are tracked
- `NEXT`: known requirement, Switch implementation still pending
- `DEFER`: only investigate if runtime testing proves it necessary

| Area | PC patch behavior | Switch v1.1.3 target | Status | Notes |
|---|---|---|---|---|
| Runtime page mapper | `EB~F8` -> font pages 49~62 | `GetFontTexIndex` around `0x446420`; rewrite `0x44650C..0x446534` | IMPLEMENTED | 44-byte in-place ARM64 rewrite; no cave needed |
| Character segmentation | accepts game 2-byte ranges | `0x446310` | CONFIRMED | `EB~F8` already falls inside existing `E0~FC` lead range; no basic patch needed |
| Game-code -> UTF-16 lookup | search 10,036 mapping entries | `0x4305D0` | NEXT | Switch currently uses 7,494-entry JP table |
| UTF-16 -> game-code lookup | search 10,036 mapping entries | `0x430350` | NEXT | Switch currently uses 7,494-entry JP table |
| Mapping table | 7,494 original + 2,542 Korean = 10,036 | original JP table around mapped `0x799E4E` | NEXT | Expansion/relocation required; do not overwrite neighboring language data blindly |
| Runtime byte validation | broaden valid Korean code behavior | Switch counterpart not finalized | NEXT | Keep separate from segmentation; only force-port after counterpart is identified or runtime symptom requires it |
| Font page/threshold patch | PC runtime changes a byte threshold | Switch counterpart not finalized | NEXT | Earlier description as literal page count was inaccurate; treat as threshold logic |
| Description font 1 | runtime font adjustment | Switch counterpart not finalized | NEXT | Map by function/signature, not blind RVA conversion |
| Description font 2 | runtime font adjustment | Switch counterpart not finalized | NEXT | Same |
| UI width 1~4 | text/UI width adjustments | Switch counterparts not finalized | NEXT | Port after locating homologous ARM64 routines |
| 17,103 inline records | same-length EXE byte replacements | exact unique original bytes in Switch `main` rodata | PARTIAL | current builder maps 5,519 unique patterns, covering 5,521 PC records, using exact-match/no-guess rule |
| 56 pointer records | pointer/reference patching | Switch pointer/data references | NEXT | T5K table is now parsed exactly; Switch correspondence still required |
| 208 RomFS payload items | replacement data | same relative Switch RomFS paths | PARTIAL | builder emits 207 directly; PC `CWTDAT_JP.TR5` is the one deliberate exception |
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

## T5K121R resource layout now parsed directly

The builder extracts `RT_RCDATA/101` from the PC patch `dinput8.dll` and parses the resource without hard-coding a raw DLL file offset.

```text
resource size                  613,685 (0x95D35)
header                         0x0000..0x0047
mapping table                  0x0048..0x9D17  (10,036 x 4 bytes)
pointer replacement strings    0x9D18..0x9F71  (602 bytes)
runtime helper blob            0x9F72..0xA00F  (158 bytes)
inline patch records            0xA010..0x951BF  (17,103 variable records)
pointer patch records           0x951C0..0x9553F (56 x 16 bytes)
runtime descriptors             0x95540..end     (11 descriptors)
```

Header fields independently agree with the known patch:

```text
version              1
inline_count         17,103
pointer_count        56
runtime_count        11
prefix_size          0x9F2A
runtime_blob_size    0x9E
target PC EXE size   18,685,960
```

## Inline mapping currently implemented

For the fixed Switch 1.1.3 `main`, the 17,103 PC records contain 8,713 distinct original byte patterns. The integrated builder scans the whole decompressed Switch `main` once with an Aho-Corasick matcher, then only emits a translation patch when all of the following are true:

1. the PC original bytes occur exactly once in the whole Switch `main`;
2. records sharing those original bytes agree on the replacement bytes;
3. the match lies inside Switch rodata (`0x58D000..0x9BF018`), not ARM64 text;
4. the patch does not overlap a more specific selected record.

Observed result on the fixed 1.1.3 `main`:

```text
PC records total                 17,103
unique original patterns          8,713
no Switch match                     186
multiple Switch matches            2,476
unique match outside rodata          528
candidate rodata patterns           5,523
overlap-skipped                         4
selected unique patterns            5,519
PC records covered                  5,521
```

This is intentionally a forward-progress integrated subset, not a claim that the remaining 11,582 records are unportable. Ambiguous cases are left for context/pointer mapping instead of guessed.

## Mapping counts

```text
Original JP mapping : 7,494 (0x1D46)
Korean additions    : 2,542
Total                : 10,036 (0x2734)
```

The newline mapping already belongs to the original 7,494 and must not be counted as an added Korean entry.
