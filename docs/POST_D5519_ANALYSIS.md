# POST-D5519 ANALYSIS

Canonical analysis after the corrected-offset full-inline diagnostic build `D5519 v0.2k` was runtime-tested in Eden Android.

## 1. Runtime result that changes project direction

`D5519 v0.2k` re-ran the historical 5,519 exact-unique inline replacement set with the Eden NSO IPS coordinate corrected from `X` to `X + 0x100`.

Observed early-game route:

- boot: PASS;
- title: PASS;
- main menu: PASS;
- scenario selection/description: PASS;
- protagonist selection: PASS;
- entry into normal gameplay: PASS;
- no freeze or forced exit was observed on this route.

This is strong evidence that the pre-P0N2 freezes were dominated by the missing `+0x100` IPS coordinate shift. It does **not** certify all 5,519 historical candidates as release-safe for all game paths.

## 2. Visible anomalies in D5519

Screenshots show four different classes and they must not be conflated:

1. Korean main names/text render correctly in many places.
2. A small auxiliary reading/yomi line above or near names renders as garbled kana/Latin-like glyphs.
3. Short repeated UI tokens remain Japanese in some places, e.g. `はい`, `年/月/日`, `貫/文`, `城`.
4. Some location-name components such as `清洲` remain Japanese because the historical selector rejected non-unique matches.

## 3. Yomi policy for the Switch port

For the Korean Switch port, the visible Japanese reading/furigana line is not needed when the main name itself is already rendered directly in Korean.

Policy:

- keep Korean main-name display;
- preserve the original Japanese halfwidth-kana yomi bytes internally where possible, because yomi may participate in sort/comparison/input logic;
- do not translate internal yomi merely for display;
- suppress the visible auxiliary yomi line at the rendering call sites instead of deleting the field or zeroing the internal key.

This is intentionally Switch-port-specific behavior. It does not attempt to reproduce every PC runtime presentation choice when that choice is unnecessary for Korean readability.

## 4. Static evidence for the yomi diagnosis

Against the fixed Switch v1.1.3 mapped `main` and the corrected D5519 patch set:

- D5519 real inline records: 5,519;
- records whose original non-NUL bytes are entirely halfwidth-kana `0xA1..0xDF`: **2,099**;
- retained non-yomi historical inline records after excluding those: **3,420**.

The garbled small line therefore has a direct structural explanation: thousands of halfwidth-yomi fields were replaced with the custom Korean code space, while the Switch auxiliary-reading renderer is not yet equivalent to the PC runtime path.

A shared name/yomi drawing routine is called at mapped address `0x45B0F8`. Eight direct callers explicitly enable the auxiliary reading line with instruction bytes:

```text
26 00 80 52   ; mov w6, #1
```

Mapped call-site offsets:

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

At each site a nearby `BL` resolves to `0x45B0F8`. The diagnostic Y0 strategy changes only the enable argument to zero:

```text
E6 03 1F 2A   ; mov w6, wzr
```

while restoring the 2,099 internal halfwidth-yomi records to the original Switch bytes.

## 5. Repeated short strings: why the old selector misses them

The historical selector rejects a pattern whenever its raw byte sequence appears more than once anywhere in the flat image. This is too conservative for short Japanese strings because their bytes also occur as substrings inside longer prose or identifiers.

Examples from the fixed Switch `main`:

### `はい` -> `예`

- T5K has one intended record: `R2277`, `はい` -> `예`.
- raw `はい` byte sequence appears 7 times in Switch rodata;
- only **one** occurrence is a standalone NUL-delimited string object: mapped `0x6A15A5`;
- it is referenced by a pointer-table entry at `0x58D0D0`;
- the immediately adjacent pointer-table object is `いいえ` at `0x6A65B2`, which the historical unique selector already translates to `아니오`.

Therefore the 7 raw matches are not 7 equivalent UI objects; most are substring hits such as `とはいえ` or `にはいかなかった`. Object-boundary + pointer evidence isolates the intended `はい` safely.

### `年 / 月 / 日`

The Switch linker/compiler has pooled the standalone date suffix objects:

```text
年  mapped 0x69785A
月  mapped 0x68925A
日  mapped 0x6A3CC6
```

At pointer table `0x59C730..0x59C768`, the three objects are referenced consecutively as `年`, `月`, `日`. `年` is also referenced from another UI registration table at `0x597090` next to `名前を入力してください` and `生年を入力してください`.

Raw byte matching finds many occurrences because the same kanji occurs inside longer text, but there is exactly one standalone NUL-delimited pooled object for each suffix in rodata. Multiple PC T5K records for these suffixes all use the same Korean replacement (`년/월/일`), so a many-PC-to-one-Switch pooled mapping is semantically non-conflicting.

### `城`

- T5K has two `城` -> `성` records.
- raw `城` appears many times inside longer strings;
- Switch has one standalone NUL-delimited `城` object at mapped `0x6A15DC`;
- that object has multiple pointer-table references.

This is another safe-pooling candidate when all PC-side replacements agree.

### `清洲`

T5K has two padded records `清洲\0\0` -> `기요스`. Switch has exactly two corresponding padded occurrences:

```text
0x6AE269
0x6AEFE9
```

Both sit inside obvious fixed-stride place-name/yomi tables. Because both PC records share the same replacement and both Switch objects are structurally valid name fields, this is a strong two-to-two recovery candidate without arbitrary occurrence selection.

## 6. Currency/date unit policy

The PC T5K data does contain explicit translations such as:

- `年` -> `년`;
- `月` -> `월`;
- `日` -> `일`;
- `貫` -> `관`;
- `文` -> `문`;
- `はい` -> `예`;
- `いいえ` -> `아니오`.

Therefore Japanese unit suffixes seen in D5519 are not evidence that the PC patch intentionally leaves every such UI untouched. However the Switch port should not globally replace every raw `年/日/貫/文` byte sequence: many occurrences are substrings inside longer strings.

Recovery must operate on **string objects / pointer-table objects / confirmed fixed fields**, not raw global substring replacement.

## 7. New recovery rule

A repeated pattern may be promoted from historical MULTI/HOLD to a Switch candidate when all of the following are true:

1. all relevant PC records agree on the replacement bytes;
2. Switch candidate object boundaries are independently established (NUL object, fixed-width field, fixed-stride table, or pointer/relocation evidence);
3. substring occurrences inside longer strings are excluded;
4. any many-to-one pooling is replacement-consistent;
5. no patched range overlaps another incompatible object;
6. emitted IPS uses the canonical `mapped + 0x100` coordinate rule and round-trips back to the intended mapped object.

This rule is narrower and safer than either `unique exact match` or global short-string replacement.

## 8. Immediate implementation sequence

1. Runtime-test `Y0 v0.2l` to confirm that the auxiliary yomi line disappears while Korean main names and navigation remain stable.
2. Add a repeated-object recovery analyzer using pointer-table/boundary evidence.
3. First recovery diagnostic should target high-confidence visible cases only: `はい`, pooled `年/月/日`, pooled `城`, and both `清洲` objects.
4. Treat `貫/文` format-string cases separately because several visible currency strings embed the unit inside longer format strings; do not patch every raw occurrence globally.
5. Keep the full 17,103-record validator as the release-audit mechanism, but its role is now residual coverage/safety recovery rather than explaining the already-resolved pre-P0N2 freeze.