# Runtime byte copy / normalization route binding — dominant C2 table closure

Date: 2026-09-15 (KST)
Scope: `RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_READ_ONLY`
Parent HEAD: `00c83f1972f67eb05cd57515304ec563d8fc32c5`

This checkpoint advances only the already-open compact-Korean byte preservation family. It complements the immediately preceding low-level halfwidth-owner checkpoint and does not authorize implementation, WRITE_SAFE, a diagnostic build, pointer work, CWTDAT work, or unrelated descriptor/helper work.

## PC_PATCH_ORACLE_GATE

`PASS` — inherited from the canonical checkpoints for this exact family.

Applicable PC evidence remains the actual Korean patch runtime/data oracle already materialized canonically:

- `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- embedded T5K resource SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- exact inline source population 17,103
- susceptible `0xA6..0xDF` source-risk upper bound 2,057

Semantic obligation is unchanged: preserve compact Korean one-byte values through the Switch consumer route without unintended Japanese halfwidth conversion. The PC x86 helper mechanism itself is not a Switch implementation prescription.

## Relation to the preceding low-level owner checkpoint

The preceding canonical checkpoint behaviorally identified:

```text
ordinary halfwidth-kana primitive   0x43497C
single direct call site             0x156F30
ordinary mapped range               0xA6..0xDD
0xDE/0xDF                            adjacent modifier/composition family
```

This checkpoint does not reopen those facts. It binds the dominant fixed-stride Stage2 table to concrete higher-level consumer routes and determines which table fields do or do not traverse a separate explicit conversion boundary.

## Switch evidence source

The actual Switch `main` NSO from the project Google Drive was opened and decompressed for read-only analysis.

Observed NSO layout:

```text
text   mem 0x000000  size 0x58CE60
rodata mem 0x58D000  size 0x432018
data   mem 0x9C0000  size 0x060430
```

The analysis below follows actual AArch64 control flow in that image.

## Dominant Stage2 table owner

The dominant Stage2 risk family remains the fixed-stride table based at Japanese-side `0x711DA0`.

Six direct address constructions of the `0x711DA0` base were found in the native table-access family. The relevant record stride is `0xC2`.

Representative base selector/accessor:

```text
0x1D4790
  index guard
  language-state selection
  selected base + index * 0xC2
  return record pointer
```

The direct caller of `0x1D4790` is `0x2A0CC8`.

## Route A — eight display slots are direct text/render consumers

At `0x2A0CC8` the returned record pointer is retained and an eight-slot loop is formed:

```text
first field pointer  = record + 0x28
field stride         = 0x11
eight slots          = +0x28, +0x39, +0x4A, +0x5B,
                       +0x6C, +0x7D, +0x8E, +0x9F
```

The selected field pointer is used directly as text input. In the observed UI path it reaches:

```text
field pointer
 -> 0x4462B0   measurement/decode-side text consumer
 -> text-object setup
 -> 0x446FF0
 -> 0x44714C
 -> 0x445C60   canonical per-character decode family
```

`0x44714C` directly calls `0x445C60` while iterating the supplied field bytes.

No call to the explicit conversion-buffer routine `0x43FD20` occurs on this field-pointer path before `0x445C60`.

Therefore these eight fixed-stride display fields are proven members of a direct text/render-decode route and not members of the `0x43FD20` auxiliary-conversion route.

This does not assert that every possible caller context elsewhere is incapable of reaching the separately verified `0x156F30 -> 0x43497C` native halfwidth primitive; it closes the observed dominant display consumer path and rejects treating the table as one undifferentiated conversion route.

## Route B — record base / primary display text also has direct-renderer consumers

`0x1D5080` is a record-pointer accessor for the same `0xC2` family when its control path requests the direct record pointer.

Three direct callers were found:

```text
0x22DB70
0x232910
0x413784
```

Observed downstream uses include direct passage into `0x446FF0` and the `0x4462B0 -> 0x446FF0` display path. This independently confirms that the primary record/display string path is not forced through `0x43FD20`.

## Route C — +0x11 auxiliary field has an explicit conversion boundary

A separate accessor path computes:

```text
record + 0x11
```

and tail-branches to `0x43FD20` (observed at `0x1D52BC` / `0x1D530C`).

`0x43FD20` is not a renderer. It allocates/uses a rotating conversion buffer, iterates input bytes, treats `0xDE/0xDF` specially as halfwidth modifiers, invokes a conversion routine, and writes converted 16-bit output before returning the buffer.

This is a proven explicit Japanese auxiliary conversion route.

Accordingly, the same `0xC2` record family has at least two materially different text semantics:

```text
primary/display fields -> direct text/render decode route
+0x11 auxiliary field  -> explicit conversion-buffer route
```

A global normalization override across the whole table would therefore be incorrect.

## Impact on the open compact-Korean family

The dominant Stage2 `0x711DA0` family is no longer an undifferentiated consumer unknown.

Closed route facts:

1. the eight `+0x28..+0x9F` fixed-stride display fields reach the existing decoder on a path that does not use `0x43FD20`;
2. primary/display record-pointer uses likewise have direct-renderer consumers;
3. the `+0x11` auxiliary field is structurally separated by an explicit conversion boundary at `0x43FD20`;
4. the native low-level ordinary halfwidth mapper `0x43497C` remains a separately verified lower-level primitive with caller `0x156F30` and must not be globally patched;
5. therefore display preservation and legitimate auxiliary/yomi-style normalization require route/context separation.

This is consistent with the already-VERIFIED downstream fact that compact Korean bytes reaching `0x445C60` are accepted by that decoder family.

## Still open for this cause family

- exact source-risk cardinality assigned to each `0xC2` field route must be materialized from the canonical 2,057-row membership before changing the family denominator;
- whether any additional high-level consumer of the dominant table enters the `0x156F30 -> 0x43497C` generic halfwidth path remains to be bound; the direct display route proven here does not;
- the remaining Stage2 block families outside this dominant table still need grouped consumer binding;
- the 64 non-Stage2 risk rows still need canonical F1/forward/gap owner reuse and route binding;
- the high-level conversion-enable owner/context above `0x156F30` remains open;
- no minimum patch site or branch condition is yet authorized.

## Disposition

For the dominant `0x711DA0 / stride 0xC2` family:

```text
STRUCTURED_OWNER          VERIFIED
DISPLAY_ROUTE             VERIFIED_DIRECT_RENDER_DECODE
AUX_PLUS_0x11_ROUTE       VERIFIED_EXPLICIT_CONVERSION
LOWLEVEL_HALF_KANA        VERIFIED_ELSEWHERE_AT_0x43497C
GLOBAL_OVERRIDE           REJECTED
IMPLEMENTATION            NOT_AUTHORIZED
NEW_WRITE_SAFE            0
BUILD                     NOT_PERFORMED
```

Next work should stay in the same compact-Korean cause family and materialize exact field-route membership/cardinality, then test remaining consumers against the verified `0x156F30 -> 0x43497C` path before moving to the remaining Stage2 families.