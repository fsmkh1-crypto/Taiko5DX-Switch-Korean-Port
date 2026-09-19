# ECF00000 NESTED INTERPRETER CONTEXT/DESCRIPTOR AUDIT — V330

Date: 2026-09-19 (KST)

```text
validation_id   V330
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CHECKPOINT
parent          75cad59d739703096dad7c8c616a2d3a7c28671f / V329
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint records the failed single-context full replay after V329 and closes its common root cause by auditing the interpreter context/descriptor family passed to `0x15F2C0`.

## 1. Failed full replay after V329

The V328/V329 recursive rule was applied to all 782 entrypoints using a single EVENT grammar for every recursive child.

Result:

```text
                         canonical   single-context replay
physical targets             4,444          2,858
messages                     4,193          2,609
choices                        251            249
choice strings                 504            500
Korean targets               4,238          2,651
INCLUDE_KO                   4,123          2,537
UNRESOLVED                     115            114
```

All six required reconstruction gates fail.

Relative to the V327 outer-only subset:

```text
outer-only physical targets  2,817
single-context replay        2,858
additional recovered            41
outer targets lost               0
```

The replay produced one structural error:

```text
entrypoint     762
root           0x1188E4
parent         0x118A4C
opcode         0x06
child start    0x118A54
misread at     0x118A58
false length   27,632
failure        file overrun
```

This failure is preserved as do-not-repeat evidence. The single-context full ledger artifact is diagnostic only and is not canonical row membership.

## 2. Common interpreter loop

Bounded Switch analysis shows that `0x15F2C0` is not one fixed EVENT parser.

It receives a context/descriptor and a byte address, dispatches the current record through a function pointer from that context, advances by the returned consumed length, and repeats until NUL.

The correct traversal identity is therefore:

```text
(context / descriptor, physical address)
```

not physical address alone.

## 3. Two direct descriptor families

For the bounded EVENT recursive-call census, two direct context families are established.

### EVENT context

```text
descriptor source   [0xA1C000 + 0x290] + 0x10
record handler      0x15F44C
role label          EVENT
```

### BRANCH context

```text
descriptor source   [0xA1C000 + 0x358] + 0x10
record handler      0x160BF8
role label          BRANCH
```

The label BRANCH is a project-local structural label only; it does not assert broader semantic meaning than the observed record-control behavior.

Direct `BL 0x15F2C0` call-site census in the bounded scope finds 11 direct call sites and no third direct descriptor family.

## 4. Corrected recursive context transitions

The V328 child address formulas remain useful, but the child context must be recorded separately.

| caller family | input context | child context | child start |
|---|---|---|---|
| EVENT 0x01 | EVENT | EVENT | p+4 |
| EVENT 0x02 | EVENT | EVENT | p+4 |
| EVENT 0x05 | EVENT | EVENT | p+4 |
| EVENT 0x06 | EVENT | BRANCH | p+8 |
| EVENT 0x08 | EVENT | BRANCH | p+4 |
| EVENT 0x0C | EVENT | EVENT | p+((word>>10)&0x3C) |
| EVENT 0x0D | EVENT | EVENT | p+((word>>10)&0x3C) |
| EVENT 0x0E/0x0F | EVENT | EVENT | p+4 |
| BRANCH 0x07 | BRANCH | EVENT | p+4 or p+8, as encoded by the handler path |
| BRANCH 0x09 | BRANCH | EVENT | p+4 |

Therefore the previously documented V328 statement that all listed child streams are directly EVENT grammar is superseded for `0x06` and `0x08`.

## 5. BRANCH record consumption

The bounded `0x160BF8` handler rules required for this cause family are:

```text
record byte 0x07 -> (word >> 9) << 2
record byte 0x09 -> (word >> 19) << 2
other nonzero     -> 4 bytes
NUL               -> stream termination
```

Records `0x07` and `0x09` can re-enter the EVENT context.

Thus the observed nesting topology includes:

```text
EVENT -> EVENT
EVENT -> BRANCH -> EVENT
```

and can nest further as the child EVENT stream itself encounters recursive records.

## 6. Entrypoint 762 closure

The prior full replay error is explained without a local exception.

For EVENT parent `0x118A4C / opcode 0x06`:

```text
child address   0x118A54
child context   BRANCH
```

Read under BRANCH grammar:

```text
0x118A54 byte 0x93 -> 4 bytes
0x118A58 byte 0x0A -> 4 bytes
0x118A5C byte 0xCD -> 4 bytes
...
NUL                     0x118BBC
errors                   0
```

The earlier 27,632-byte overrun came from incorrectly interpreting `0x118A58` as EVENT opcode `0x0A`.

No entrypoint-762 special case is permitted.

## 7. V329 representative result correction

The V329 numerical representative result remains valid:

```text
entrypoints 253..290
outer unique       297
nested-aware       324
new targets         27
lost outer           0
validation        PASS
```

However, its mechanism provenance is corrected.

Known recovery under EVENT parent `0x08` is:

```text
EVENT -> BRANCH -> EVENT
```

not direct EVENT -> EVENT traversal.

The targets `0x90158`, `0x901AC`, and all 21 nested targets beneath `0x9DAE0` remain valid recovered target evidence; only the intermediate context model is superseded.

## 8. Rejected / do-not-repeat

Rejected:

- every `0x15F2C0` recursive child uses the EVENT grammar;
- physical address alone is a sufficient recursion identity;
- EVENT `0x06` and `0x08` children should be parsed directly as EVENT;
- the entrypoint 762 overrun indicates corrupt PC-Korean data;
- a local `0x06` patch or entrypoint-specific exception is sufficient;
- V329 representative PASS proves the single-context model over the full corpus;
- rerunning all 782 entrypoints again before incorporating context/descriptor state.

The V327 outer-only subset remains diagnostic evidence. V324/V325/V326 aggregate claims are not superseded.

## 9. Artifact preservation

```text
Drive path
Google Drive/GPT/태합입지전/ECF00000_V330_CONTEXT_DESCRIPTOR_AUDIT/

folder id
13i_20vwtbiJEc0EhrxfnWj71brv6LbOW
```

Failed single-context full replay:

```text
file   ecf_v329_nested_aware_full_ledger.json
id     1U8wpmCtJrPmw63cuW7izi6r-vKsQoSkm
SHA-256
d00f6ce0a1762dbab69274ff88dc02864330ef0bbcc2bc66321facec27937c17
```

Context/descriptor audit:

```text
file   ecf_nested_interpreter_context_descriptor_audit.json
id     1PFFEuWO4MkunCTjN7XXZrHXmeNCYf0vy
SHA-256
bb8f15cb7a62c033089f4f01a2b28ec7b3c9ccd4a19e4c36c912b8f095ace9e3
```

## 10. Impact boundary

Unchanged:

- V324 aggregate 4,444 / 4,193 / 251;
- V325 code/glyph/font closure;
- V326 4,238 Korean / 4,123 INCLUDE / 115 UNRESOLVED aggregates;
- identity and fixed-particle policy;
- TAI5MSG/B24;
- SNR;
- product bytes.

Corrected:

- V328 recursive-child mechanism for EVENT `0x06` and `0x08`;
- V329 representative traversal provenance.

Still blocked:

- exact 4,444 physical-row ledger;
- exact 4,123/115 row membership;
- EVENT serializer implementation.

## 11. Exact next scope

After a fresh explicit execution signal:

`ECF00000_TWO_CONTEXT_FULL_LEDGER_RECONSTRUCTION_READ_ONLY`

Required traversal state:

```text
(context, physical address)
EVENT handler  = 0x15F44C
BRANCH handler = 0x160BF8
```

Required final gates:

```text
physical targets   4,444
messages           4,193
choices              251
Korean targets     4,238
INCLUDE_KO         4,123
UNRESOLVED           115
```

Do not implement a serializer, rewrite EVENT payloads, build/package/IPS, or broaden to other EVENT files/SNR in the next replay.
