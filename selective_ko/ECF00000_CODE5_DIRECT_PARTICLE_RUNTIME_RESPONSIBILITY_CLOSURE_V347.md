# ECF00000 code-5 direct-particle runtime-responsibility closure — V347

Date: 2026-09-20 (KST)

```text
validation_id   V347
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CLOSURE
parent          b6731468936c0f993da7afb65b790ed079578c42 / V346
product_bytes   UNCHANGED
implementation  NONE
build/package   NONE
hardware        NOT RUN
```

## 1. Scope

V347 closes only the runtime-responsibility question left open by V346 for:

```text
DIRECT_PARTICLE_ONLY                  350 rows
MIXED_DIRECT_AND_DERIVED_RISK           2 rows
direct-particle occurrences           389
```

Exact membership is inherited from the canonical V346 ledger. V347 does not regenerate,
broaden, or reorder that membership.

This scope does not process the 59 copula-derived-only rows, the three non-particle-suffix rows,
or the derived-morphology portion of the two mixed rows.

## 2. Switch EVENT escape responsibility

Bounded Switch v1.1.3 runtime analysis establishes the message-string expansion path at
`0x156D80`.

```text
message string
-> recognize 0x5C ('\\')
-> decode escape kind / argument
-> obtain or format runtime value/control state
-> append expanded value into scratch output
-> resume ordinary string scan
-> following Korean particle bytes are emitted as ordinary literal text
```

Relevant bounded anchors:

```text
0x156E28   backslash / escape recognition
0x1578F0   expanded runtime value append path
0x157908   resume message-string processing
```

No generic Korean final-consonant / particle-allomorph selection responsibility is present in
this bounded EVENT escape path.

Binding responsibility:

```text
escape token      runtime value/control expansion
following 조사    authored EVENT literal data
```

## 3. Original-PC -> PC-KO escape preservation

For the V346 direct-particle cause-family:

```text
target rows                              352 / 352
row escape sequence preserved            352 / 352
direct escape occurrences preserved      389 / 389
escape mismatches                          0
unique direct escape surface forms       107
```

The Korean patch therefore does not replace these EVENT escape tokens with Korean-specific
particle selectors. It translates/restructures the literal grammar around the same runtime
expansion tokens.

## 4. Original Japanese adjacency evidence

At the corresponding direct occurrences, the same runtime escape is immediately followed in
the PC original by a Japanese grammatical particle in 382 of 389 cases:

```text
は   133
が   121
を    50
と    37
の    24
に    11
へ     4
で     2
--------
total 382
```

The remaining seven occurrences are Korean word-order / phrase-restructuring cases rather than
evidence that the escape itself owns Korean particle selection.

This independently supports the ownership boundary:

```text
runtime value production != post-value grammatical-particle selection
```

## 5. PC Korean runtime-patch code layer

The canonical PC Korean runtime package contains 17,103 inline records.

Bounded target-range census against the target PC EXE executable `.text` region:

```text
target .text RVA range               0x1000 .. 0xB000B0
inline target minimum                0xB1EA08
inline target maximum                0x1061CD7
inline records targeting .text       0 / 17,103
```

Therefore the 17,103 inline layer does not inject an executable Korean-particle selector into
the PC EXE.

The separately closed executable patch layer is the 11 runtime descriptors plus 158-byte helper.
Its established responsibilities are mapping lookup/limits, byte validation/copy, runtime page
mapping, font/page threshold, UI width, and description-font related changes. No descriptor or
helper responsibility for Hangul final-consonant testing or Korean particle selection is present.

Binding conclusion:

```text
PC Korean runtime josa selector      NONE ESTABLISHED
Switch EVENT runtime josa selector   NONE
particle surface owner               EVENT authored literal
```

## 6. Same escape surface does not imply one particle allomorph

The same escape token is observed with opposite members of a Korean allomorphic pair in the
PC-Korean corpus. Nine exact direct escape surfaces show this property:

```text
\%00
\%01
\%03
\#07F0
\#07FE
\%20320
\#0218
\#01E3
\E079
```

Representative `\%00` census includes both sides of multiple pairs:

```text
subject   가 19 / 이 10
topic     는 33 / 은 10
and       와  1 / 과  2
```

Thus an escape family cannot be assigned a fixed Korean particle by escape identity alone.

## 7. Current fixed-surface-policy comparison

Using the already canonical first-release preferred surfaces:

```text
은/는 -> 는
이/가 -> 가
을/를 -> 를
과/와 -> 와
(으)로 -> 로
```

the 389 direct occurrences divide as:

```text
preferred-side occurrences    269
opposite-side occurrences     120
total                         389
```

Across the 350 pure-direct rows only:

```text
already preferred only        242 rows
opposite only                 104 rows
both preferred + opposite       4 rows
normalization-candidate rows   108
opposite occurrences          117
```

Exact pure-direct substitutions implied by a future policy extension would be:

```text
은 -> 는    50
이 -> 가    45
을 -> 를    13
과 -> 와     9
-------------
total       117
```

The two mixed rows contain three additional opposite-side direct occurrences:

```text
row 12476   이 -> 가     1
row 13029   을 -> 를     2
```

Those two rows remain DEFER because their derived-morphology responsibility is independently
unresolved.

## 8. Product disposition

V347 closes runtime responsibility only. It does not authorize a new fixed-surface
applicability class and does not change product admission.

```text
V346 lexical false-positive INCLUDE_KO    12 / unchanged
DIRECT_PARTICLE_ONLY                     350 / DEFER unchanged
MIXED                                      2 / DEFER unchanged
COPULA_DERIVED_ONLY                       59 / DEFER unchanged
NON_PARTICLE_SUFFIX                        3 / DEFER unchanged
code-5 DEFER total                       414 / unchanged
```

No product TS5 bytes are changed by V347.

## 9. Rejected / do-not-repeat

Reject:

- Switch EVENT escapes dynamically select Korean particle allomorphs;
- the PC Korean patch adds a hidden final-consonant/josa selector through the 17,103 inline layer;
- the PC runtime helper/descriptors contain a Korean josa-selection hook;
- one escape surface implies one fixed Korean particle;
- the direct-particle rows require semantic reverse engineering of all 107 escape forms before
  ownership can be decided;
- the existing V345 1,251-row ledger may be silently expanded to absorb these rows;
- the two mixed rows can be promoted merely by closing their direct-particle portion.

## 10. Current disposition / next scope

```text
V345 fixed-surface serializer                 CLOSED / IMPLEMENTED
V346 code-5 semantic ledger                   CLOSED
V347 direct-particle runtime responsibility   CLOSED
pure direct rows                              350 / DEFER
mixed rows                                      2 / DEFER
product/build/package/IPS                     NONE
```

Exact next scope after a fresh explicit user signal:

`ECF00000_CODE5_DIRECT_PARTICLE_FIXED_SURFACE_POLICY_EXTENSION_READ_ONLY`

READ ONLY only. Decide whether the existing FIXED_SURFACE_PARTICLE_V1 release policy may be
extended to the exact V346 DIRECT_PARTICLE_ONLY cause-family through a separate applicability
authority. If designed, preserve V345 membership unchanged and create a separate
DIRECT_ESCAPE_PARTICLE applicability overlay. Do not implement, mutate product bytes, promote
the mixed rows, process copula-derived morphology, build/package/IPS, or run hardware without
another fresh authorization.
