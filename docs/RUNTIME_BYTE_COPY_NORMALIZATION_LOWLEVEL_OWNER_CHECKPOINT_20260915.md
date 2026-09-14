# Runtime byte copy / normalization route binding — low-level halfwidth owner checkpoint

Date: 2026-09-15 (KST)
Scope: `RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_READ_ONLY`
Parent HEAD: `d448be60739c5e3b81ddaf4f1d4b4652bc2669a9`

This is a read-only analysis checkpoint. It does not authorize implementation, diagnostic build generation, write safety, or release integration.

## PC_PATCH_ORACLE_GATE

`PASS`.

The existing canonical PC runtime-byte helper evidence is reused without reopening VERIFIED work. The semantic obligation remains: compact Korean one-byte values and ordinary two-byte values accepted by the PC Korean patch must survive copy/normalization and reach the existing Switch consumer without unintended Japanese halfwidth conversion. The PC x86 helper mechanism is not mechanically transplanted.

## Newly confirmed Switch fact

The actual low-level Japanese halfwidth-kana conversion primitive is now behaviorally identified at Switch text address `0x43497C`.

Evidence is semantic, not caller-count based:

- the function compares the input against `0xA6`;
- it forms an index from `input - 0xA6`;
- the indexed span covers the ordinary halfwidth-kana body through `0xDD`;
- it performs a 16-bit lookup from Switch RODATA table `0x6A856A`;
- the table entries are fullwidth Shift-JIS equivalents (for example the first entry resolves to bytes `82 F0`, followed by the expected Japanese fullwidth-kana sequence);
- `0xDE` / `0xDF` are handled outside this ordinary table path by the adjacent voiced/semi-voiced-mark composition family.

Therefore the previously open statement that Japanese halfwidth handling can mutate Korean compact bytes in the overlapping range is now tied to a concrete native conversion primitive rather than only to a broad parser symptom.

## Direct caller binding

`0x43497C` has one direct call site in the Switch text image: `0x156F30`.

That call lies inside the larger parser/conversion routine containing the character-class dispatch around the `0x156Bxx..0x157xxx` region. This establishes a deterministic next trace direction:

`source/storage consumer -> parser/conversion routine -> 0x156F30 -> 0x43497C halfwidth table mapper`

The exact high-level entry owner(s) feeding this parser routine are not yet closed in this checkpoint.

## Rejected / corrected prior lead

`0x263C5C` remains rejected. Its 1,078 direct-caller count was only a numerical coincidence and its actual body belongs to an unrelated calculation/copy routine. It must not be used as the halfwidth normalizer owner.

The canonical 1,078-call-site broad-family statement is therefore not sufficient by itself to identify a patch site. Route binding must proceed from the now-confirmed semantic primitive and its real caller chain.

## Impact interpretation

No change to the 2,057 susceptible-source upper bound or the previous structural split:

- Stage2 affine target-resolved risk rows: 1,993;
- non-Stage2 risk rows: 64;
- dominant fixed-stride structured RODATA family inside Stage2: 1,686;
- place-table risk rows: 32 = 17 display-name starts + 15 yomi starts;
- Stage2 DATA risk rows: 40.

These remain source/route analysis counts, not Action Ledger cardinality.

## Confirmed facts / strong hypothesis / unresolved / rejected / impact / proposed correction

### Confirmed facts

- PC_PATCH_ORACLE_GATE = PASS.
- downstream Switch character decode remains compatible when compact Korean bytes reach it.
- `0x43497C` is the native ordinary halfwidth-kana conversion primitive for `0xA6..0xDD`, backed by RODATA lookup table `0x6A856A`.
- `0xDE/0xDF` are separated into the adjacent voiced/semi-voiced composition family rather than the ordinary table body.
- `0x43497C` has a single direct caller at `0x156F30`.

### Strong hypothesis

One or more of the affected text consumer families reach `0x43497C` through the parser/conversion routine containing `0x156F30`; the minimum Korean-preservation repair owner is likely a context/route decision above this low-level mapper rather than modification of the mapper itself.

### Unresolved

- exact high-level entry owner(s) that activate this conversion path;
- family-by-family binding of the 1,993 Stage2 risk rows and 64 non-Stage2 risk rows to this path versus direct-renderer or explicit-yomi paths;
- active conversion-control flag/context for the dominant `0x711DA0` fixed-stride table consumer;
- exact high-level owner of the legitimate yomi conversion path.

### Rejected

- use of `0x263C5C` as the normalizer because its caller count equals 1,078;
- patching the downstream renderer/decode layer;
- globally disabling Japanese halfwidth conversion;
- mechanically transplanting the PC x86 helper.

### Related impact range

Potentially any source family whose runtime route enables the native halfwidth conversion before renderer entry. The 2,057-row source census remains only the maximum susceptible denominator until route binding is complete.

### Proposed correction direction

Do not patch `0x43497C` globally. Continue upward from `0x156F30` to identify the conversion-enable context and bind each storage/consumer family. The intended realization remains conditional raw preservation for Korean compact data while preserving legitimate Japanese auxiliary/yomi normalization.

## Next deterministic work

1. recover the parser routine entry containing `0x156F30` and enumerate its real high-level callers;
2. bind the dominant `0x711DA0` fixed-stride table access family into that caller graph or prove it uses a different route;
3. bind place display-name and place-yomi routes separately;
4. reuse existing F1/forward/gap provenance to classify the 64 non-Stage2 rows;
5. after complete route coverage, design a single-cause diagnostic realization; implementation and WRITE_SAFE remain blocked until then.

New WRITE_SAFE authority: 0.
Existing total remains 162.