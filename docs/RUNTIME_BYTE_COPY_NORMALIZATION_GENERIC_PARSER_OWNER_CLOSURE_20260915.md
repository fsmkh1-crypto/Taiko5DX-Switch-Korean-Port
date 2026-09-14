# Runtime byte copy / normalization route binding — generic parser owner closure

Date: 2026-09-15 (KST)
Scope: `RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_READ_ONLY`
Parent HEAD: `a5ba9b35f6c5c301bc6536763f15b05cf3aca2c8`

This checkpoint continues only the already-open compact-Korean byte-preservation cause family. It does not authorize implementation, WRITE_SAFE, a diagnostic build, pointer work, CWTDAT work, RomFS work, or unrelated descriptor/helper work.

## PC_PATCH_ORACLE_GATE

`PASS` — inherited from the canonical evidence for this exact family.

Applicable PC oracle remains the verified Korean-patch runtime/data evidence and its semantic obligation: compact Korean one-byte values must survive the text-consumer route without unintended Japanese halfwidth conversion. The Windows/x86 helper mechanism itself is not a Switch implementation prescription.

## Switch evidence source

The actual Switch `main` NSO from the project Google Drive was decompressed read-only and the relevant AArch64 control flow was inspected directly.

The immediately preceding checkpoint already established:

- ordinary halfwidth-kana mapper: `0x43497C`;
- unique mapper call site: `0x156F30`;
- ordinary mapped range: `0xA6..0xDD`;
- `0xDE/0xDF`: adjacent modifier/composition family;
- dominant `0x711DA0 / stride 0xC2` display fields have direct render/decode routes;
- the same C2 record's `+0x11` auxiliary field has a separate explicit conversion boundary at `0x43FD20`.

Those facts are inherited and not revalidated here.

## 1. The `0x156F30 -> 0x43497C` call belongs to one large parser body

The mapper call at `0x156F30` is inside the function beginning at `0x156D80`.

Observed behavior in that function includes:

- iteration over an input byte string;
- direct preservation of recognized two-byte lead sequences;
- control/escape parsing;
- decimal/hex-style token parsing;
- ordinary byte handling;
- the call at `0x156F30` to `0x43497C` for the native Japanese halfwidth mapping case;
- fallback copying of the original byte when the mapper returns no mapped value.

Therefore the low-level halfwidth mapper is not an isolated renderer helper. It is a branch inside a higher-level generic text parser/formatter.

## 2. External parser entry is `0x157C30`

The function at `0x157C30` is the externally called wrapper for the `0x156D80` parser body.

Its control flow is:

1. preserve `x0` and `x1` as parser object/input pointer;
2. call `0x157CA4` and conditionally update external state using the two integer arguments;
3. restore the preserved `x0/x1` pair;
4. tail-branch to `0x156D80`.

The actual text pointer is therefore forwarded unchanged from wrapper to parser.

Direct `BL` callers of `0x157C30` in Switch text are exactly nine:

```text
0x1603A8
0x1604F8
0x1605F0
0x1606EC
0x160838
0x160944
0x160994
0x1609AC
0x164610
```

This converts the previous broad generic-normalization uncertainty into a finite nine-entry high-level parser-entry census.

## 3. The wrapper integer arguments are not halfwidth conversion-enable flags

At several callers the two integer arguments are fixed to `0x519`; at others they are values resolved through the existing ID/object path. Inside `0x157C30`, those arguments are consumed before parser entry by calls through `0x25F664` when in range.

Immediately before the tail branch to `0x156D80`, the wrapper restores only the preserved parser object and text pointer into `x0/x1`.

No conversion-mode boolean is forwarded into the parser body through these integer arguments.

Disposition:

```text
CALLER_CONVERSION_ENABLE_FLAG hypothesis  REJECTED
```

The minimum preservation condition must therefore be sought in one of the following:

- parser-internal byte/context classification;
- a higher-level choice between this parser route and a direct-render route;
- a separate source-specific reconstruction boundary.

It must not be modeled as simply toggling the wrapper's `w2/w3` values.

## 4. `0x43FD20` auxiliary conversion is a separate conversion family

A direct scan of the `0x43FD20` auxiliary conversion routine found no call to `0x43497C`.

Conversely, inside the `0x156D80` generic parser body, the verified `0x43497C` call remains at `0x156F30`.

Thus the following two conversion paths are distinct and must not be collapsed:

```text
generic parser/formatter
  0x157C30 -> 0x156D80 -> 0x156F30 -> 0x43497C

C2 +0x11 auxiliary conversion
  accessor -> 0x43FD20 -> separate conversion implementation
```

This strengthens the prior rejection of a table-wide or global normalization override.

## 5. Relation to dominant C2 table routes

The previous canonical C2 checkpoint proved that the dominant display fields from the `0x711DA0 / stride 0xC2` family reach `0x445C60` through direct measurement/text-object/render-decode consumers without passing through `0x43FD20` on the observed route.

This checkpoint further shows that the generic halfwidth parser is a separately owned nine-entry family at `0x157C30`.

No evidence in this checkpoint links the already-proven dominant direct-display C2 route to `0x157C30`. Therefore the dominant display route must remain classified as direct-render/decode unless a separate concrete call-chain is found.

The C2 `+0x11` auxiliary route remains separately classified at `0x43FD20`.

## 6. Confirmed facts

- `0x156D80` owns the generic parser body containing the unique `0x156F30 -> 0x43497C` ordinary-halfwidth call.
- `0x157C30` is the external wrapper that tail-branches to `0x156D80`.
- `0x157C30` has exactly nine direct call sites.
- wrapper `w2/w3` values are not a halfwidth conversion-enable flag forwarded to the parser.
- `0x43FD20` does not call `0x43497C`; the auxiliary conversion path is separate from the generic parser halfwidth path.
- the already-proven dominant C2 display route remains direct-render/decode; no new link to the generic parser was established here.

## 7. Strong working hypotheses

- compact-Korean corruption attributable to this family can only occur for source routes that actually enter the `0x157C30 -> 0x156D80` parser path and present overlapping compact bytes to the ordinary-byte branch;
- a minimum Switch-native fix, if required after route membership is materialized, is likely to distinguish Korean compact-byte context inside or immediately before this parser rather than globally disabling Japanese halfwidth conversion.

These remain hypotheses until source-family membership and a safe discriminant are bound.

## 8. Open items

- map the nine `0x157C30` caller contexts back to canonical source/storage owner families;
- materialize exact 2,057-risk-row membership/cardinality by C2 display, C2 auxiliary, generic-parser, remaining Stage2, and non-Stage2 routes;
- reuse existing F1/forward/gap provenance for the 64 non-Stage2 rows;
- bind remaining Stage2 block families outside the dominant C2 table;
- identify a safe source/context discriminant before proposing any parser patch site;
- do not authorize a diagnostic build until the whole same-cause affected range is enumerated.

## 9. Rejected hypotheses retained

- the low-level mapper is a renderer-only function;
- the wrapper's two integer arguments are a simple halfwidth conversion ON/OFF control;
- the C2 `+0x11` conversion and generic parser halfwidth mapping are the same routine;
- global halfwidth disable is safe;
- the dominant C2 display route should be patched merely because the table also contains an auxiliary conversion field.

## 10. Disposition

```text
PC_PATCH_ORACLE_GATE          PASS
GENERIC_PARSER_BODY           VERIFIED at 0x156D80
GENERIC_PARSER_WRAPPER        VERIFIED at 0x157C30
WRAPPER_DIRECT_CALLERS        VERIFIED = 9
LOWLEVEL_HALF_KANA_CALL       VERIFIED at 0x156F30 -> 0x43497C
WRAPPER_FLAG_HYPOTHESIS       REJECTED
AUX_0x43FD20_SAME_PATH        REJECTED
IMPLEMENTATION                NOT_AUTHORIZED
NEW_WRITE_SAFE                0
DIAGNOSTIC_BUILD              NOT_PERFORMED
```

Next canonical work remains read-only route membership: classify the nine parser callers by source owner, materialize exact risk-row cardinalities, then continue remaining Stage2 and 64 non-Stage2 provenance binding before any implementation design.