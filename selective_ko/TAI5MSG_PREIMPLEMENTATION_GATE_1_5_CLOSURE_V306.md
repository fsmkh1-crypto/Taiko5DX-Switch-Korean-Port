# TAI5MSG PREIMPLEMENTATION GATE 1-5 CLOSURE — V306

Date: 2026-09-18 (KST)
Status: CANONICAL PREIMPLEMENTATION CLOSURE / GATE-1..5 PASS / NO SERIALIZER / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V306`
Parent: `6f04d96eb21baddbe809a2fc7710b0582e116a00` / V305

## 1. Purpose

V306 materializes the bounded read-only results performed after V305 for the exact effective V303+V304 TAI5MSG release population.

It closes the five V305 preimplementation gates without implementing a serializer, emitting a Korean TAI5MSG release file, changing gameplay data, generating IPS/build/package output, or claiming physical-Switch/gameplay PASS.

Canonical population remains:

```text
TAI5MSG release rows       3,179
R1                         3,158
R2                            21
external-caller waits        191  EXCLUDED
inline/main release rows     139  SEPARATE CARRIER
global INCLUDE_KO          3,318
```

V304 remains the only authorized target-payload correction overlay.

## 2. Gate status

```text
GATE-1 DETERMINISTIC_PADDING_GATE           PASS
GATE-2 ZERO_REPLACEMENT_IDENTITY_REBUILD    PASS
GATE-3 CONTROL_AND_CODE_VALIDATION_GATE      PASS
GATE-4 STRONG_REPARSE_OFFSET_GATE            PASS
GATE-5 MAPPING_TO_GLYPH_CLOSURE_GATE         PASS_FOR_EFFECTIVE_TAI5MSG_3179
```

The last status is deliberately population-scoped. It does not claim that every Mapping 10,036 Korean-added entry has a visible font glyph.

## 3. GATE-1 — deterministic padding / physical extent

Canonical stock PC-JP / historically byte-identical Switch TAI5MSG identity:

```text
size    1,810,889 / 0x1BA1C9
sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f
blocks  33
messages 14,832
```

For stock B0..B31:

- physical block extent equals declared block size;
- bytes after logical used-data end are decrypted filler `0x5B`;
- corresponding encrypted/on-disk filler is `0x00`;
- stock declared sizes are `0x40` aligned.

Stock B32:

```text
offset             0x1AD780
declared size      0xCA80
physical size      0xCA49
declared-physical  0x37 / 55
physical filler    0
```

The final 55 bytes are absent from the file and are not writable capacity.

### Effective-release B32 correction

Zero-replacement identity alone could not distinguish “EOF always equals used-end” from “stock physical extent is preserved when selected payload shrinks.” Effective V303+V304 reconstruction resolves that ambiguity.

For this exact release:

```text
effective B32 used-end       0xB8D5
preserved physical extent    0xCA49
preserved declared size      0xCA80
physical filler              0x1174 / 4,468 bytes
omitted final tail           0x37 / 55 bytes
```

Therefore the binding effective-release contract is:

```text
B32 used data       0x0000..0xB8D4
B32 physical filler 0xB8D5..0xCA48
B32 physical EOF    0xCA49
B32 omitted tail    0xCA49..0xCA7F
B32 declared size   0xCA80
```

The physical filler uses the same canonical filler representation: decrypted `0x5B`, encrypted/on-disk `0x00`.

Do not generalize the stock zero-replacement relation into `B32 physical EOF = rebuilt used-end` for a shrinking release.

## 4. GATE-2 — zero-replacement identity rebuild

Canonical operations:

```text
parse 33 header pairs
-> decrypt block bytes by bytewise +0x5B
-> parse u16 count + u32 offsets[]
-> preserve all 14,832 message payloads
-> regenerate offsets
-> rebuild canonical physical filler
-> encrypt by bytewise -0x5B
-> regenerate header pairs
-> emit
```

Acceptance result:

```text
rebuilt size    1,810,889
rebuilt sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f
rebuilt == stock  TRUE
first divergence   NONE
```

All regenerated header pairs are identical to stock.

Reparse also reproduces all 33 block counts, all 14,832 logical messages, all block-local u32 offsets, physical extents, used-data ends and stock filler counts.

Canonical storage transform required for this identity is uniform bytewise `+0x5B` decrypt / `-0x5B` encrypt. No block-index, file-offset or block-size dependent state is required or observed in the canonical TAI5MSG path.

## 5. GATE-3 — effective payload control/code validation

Canonical PC-KO TAI5MSG source:

```text
size    2,134,366
sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
```

V303 raw payload validation fails exactly two rows:

```text
B19:M058  FB 05  -> invalid trail
B30:M058  FB 05  -> invalid trail
```

These are exactly the V304 correction rows.

After applying the exact V304 one-byte-delete overlays:

```text
effective rows             3,179
invalid lead/trail             0
unmapped two-byte codes        0
unknown tokens                 0
truncated controls             0
semantic 0x02 insertions       0
```

Every effective row has one terminal `05 05 05`.

The final `00` after `05 05 05` at `B32:M242` is accepted only as the canonical final-message structural terminator proven by JP/KO/SC/TW counterparts. This does not authorize arbitrary `00` tokens elsewhere.

Identity policy remains unchanged:

```text
dedicated identity fields        KEEP_JP
authored Korean prose literals   PRESERVE_AS_AUTHORED_KO
runtime-inserted identity        KEEP_JP
reverse substitution             FORBIDDEN
```

## 6. GATE-4 — strong reparse / offset closure

Effective V303+V304 analytical reconstruction produces:

```text
blocks                         33 / 33
messages                   14,832 / 14,832
per-block message counts       exact
offset entry counts            exact
u32 offsets ordered            PASS
message overlap                   0
message out-of-bounds             0
selected payload mismatch         0
unselected JP payload changes     0
```

Population relation:

```text
selected effective payloads   3,179
unchanged JP payloads        11,653
total                        14,832
```

Effective growth by block:

```text
B17  +0x0340
B19  +0x0A80
B20  +0x06C0
B21  +0x01C0
B22  +0x4340
B23  +0x0FC0
B24  +0x0E40
----------------
TOTAL +0x7780
```

Expected effective physical postcondition:

```text
growth       +0x7780 / 30,592
final size   1,841,481 / 0x1C1949
B32 offset   0x1B4F00
B32 declared 0xCA80
B32 physical 0xCA49
B32 omitted  0x37
```

V304 does not change the final growth because B19 remains inside declared `0xF600` and B30 remains inside declared `0xA540`.

`+0x7780` and `0x1C1949` are recomputed expected postconditions, not hard-coded serializer inputs.

The analytical effective reconstruction was deterministically reserialized twice with identical bytes. Its diagnostic-only SHA-256 was:

```text
dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9
```

This hash is a V306 analytical postcondition, not a materialized release artifact.

## 7. GATE-5 — Mapping to glyph closure for the effective release

Effective 3,179 payload:

```text
unique two-byte text codes             1,011
Korean-added unique codes                992
stock unique codes                        19
Korean-code occurrences              219,354
compact A1..DF Korean usage                0
PUA-mapped Korean usage                     0
```

The 992 Korean-added codes are all normal two-byte Hangul codes and are fully contained in Mapping 10,036.

```text
effective Korean codes       992
present in Mapping 10,036    992
missing                        0
```

They use lead pages `EB..F7`. The deployed Switch page-mapper realization covers the full `EB..F8 -> pages 49..62` domain.

Canonical Korean font:

```text
size    16,779,036
pages   64
sha256  c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
```

Canonical Switch original font:

```text
size    13,108,628
pages   50
sha256  9c886848c31c31d09aeeed0ac5c44b909d561220110ca04da0f7fa32d3a0083e
```

Korean font pages 0..48 preserve the Switch-original texture bytes, while page 49 onward supplies the Korean extension.

Direct Mapping/font-cell closure:

```text
Mapping Korean Hangul codes     2,350 / 2,350 non-empty font cells
effective TAI5MSG Hangul codes    992 / 992 non-empty font cells
effective missing glyph cells       0
```

The effective TAI5MSG release does not use Mapping's 192 PUA values, so V306 does not require or claim glyph closure for that PUA population.

Binding claim:

```text
effective emitted 992 Hangul codes
  subset of Mapping 10,036
  subset of EB..F8 page-mapper realization
  subset of non-empty Korean font Hangul cells
= PASS
```

Do not broaden this into “all 2,542 Korean-added Mapping entries have visible glyphs.”

Historical corrected-page-mapper builds provide representative Eden runtime evidence for normal two-byte Korean rendering. V306 does not claim exhaustive 992-glyph hardware visual QA or physical Nintendo Switch validation.

## 8. Rejected / narrowed hypotheses

Rejected:

- arbitrary per-block padding;
- B32 missing 55 bytes are writable padding;
- a shrinking B32 must move EOF to rebuilt used-end;
- a shrinking B32 must shrink declared size;
- V303 raw 3,179 payload is already fully control-safe without V304;
- malformed/unmapped effective rows remain after V304;
- effective TAI5MSG uses semantic `0x02` insertion controls;
- effective TAI5MSG requires compact page-63 Korean;
- W0/W1 compact-width family blocks this TAI5MSG population;
- effective TAI5MSG requires PUA glyphs;
- effective Korean Hangul code has a Mapping/page/glyph miss;
- V304 changes expected `+0x7780`;
- zero-replacement rebuild cannot reproduce exact stock bytes.

Narrowed:

- GATE-5 PASS is for the exact effective TAI5MSG 3,179 population, not all Mapping 10,036 entries.
- font asset identity and static glyph availability do not equal exhaustive runtime visual QA.
- analytical effective-output SHA-256 is not a release artifact identity.

All V305 rejected external hypotheses remain inherited.

## 9. Impact boundary

V306 changes no candidate/classification/disposition count.

```text
TAI5MSG release rows       3,179 unchanged
inline release rows          139 unchanged
global INCLUDE_KO          3,318 unchanged
191 external caller waits  EXCLUDED unchanged
```

V306 closes the five preimplementation gates only.

It does not close:

- layout/reflow QA;
- mistranslation/content-completeness/help QA;
- forced-minigame or 3+-choice event runtime QA;
- the 191 caller waits;
- physical Switch runtime validation;
- serializer implementation;
- package/build integration.

## 10. Next scope

After a fresh explicit user signal:

`TAI5MSG_3179_SELECTIVE_BUILDER_SERIALIZER_DESIGN_READ_ONLY`

The design must consume V303 membership, V304 exact payload overlays and V306 gate contracts. It must specify fail-closed source guards, deterministic reconstruction, B32 physical handling, Mapping/font package prerequisites and output postconditions.

It must not implement the serializer, emit a release TAI5MSG, change gameplay data, generate IPS/build/package output, or claim runtime PASS.

Stop after the required analysis report. A further explicit signal is required for implementation.

## 11. Repository write boundary

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
