# EVENT 169 runtime event_len and semantic replay closure — V367

Date: 2026-09-22 (KST)

```text
validation_id   V367
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_RUNTIME_EVENT_LEN_AND_SEMANTIC_REPLAY_CLOSURE
parent          cf86983083279683c63a9f0208b92214fb23d80d / V366
implementation  NONE
product bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

## 1. Scope and frozen inputs

V367 closes the two claims intentionally left pending by V366:

```text
whole-family semantic admission replay
universal Switch runtime event_len / command-boundary continuity
```

The V366 source-owner universe and binding split are frozen and are not regenerated or reclassified:

```text
source-owner universe          66,987
direct/header-preserved        66,956
overlap-composite                  31
unaccounted source owners           0
ambiguous product bindings          0
```

The exact Switch v1.1.3 `main` used for handler evidence remains:

```text
bytes    5,287,359
sha256   b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b
```

The exact Switch EVENT source folder remains Drive folder
`1byPWJuG7dIn4KVS2GFLpXiMsDUHaZuHh` with 169 TS5 members. PC-KO EVENT payload authority remains
the V366 canonical embedded-patcher reconstruction; no installation-state EVENT folder is promoted.

## 2. Semantic classifier regression authority

No new semantic classifier was invented.

The V363 canonical archive preserves the actual V335 classifier as `V335_GENERATOR.py`, and its
SHA-256 is identical to the canonical V335 `GENERATOR.py`. Exact regression established:

```text
V335 legacy regression                PASS 2,858 / 2,858
V335 V334 source rows                 13,075
V335 INCLUDE_KO                       12,171
V335 UNRESOLVED                          426
V335 NON_KOREAN_TARGET                   478

V363 legacy V334 compatibility        PASS 13,075 / 13,075
V363 total ECF source rows            15,951
V363 canonical INCLUDE_KO             13,805
V363 canonical UNRESOLVED                470
V363 canonical NON_KOREAN_TARGET       1,671
V363 canonical BINDING_DEFER               5
```

Under the frozen V366 binding, V363's unchanged exact rows remain exact. One old V363 binding is
intentionally superseded by the V366 duplicate-KO correction at ECF00000 source `0x71AD0`, and
the five old binding-defer rows are now bound. This is not a classifier regression.

## 3. Whole-family semantic replay

Applying the canonical V335 classifier to the frozen 66,987-owner V366 universe gives:

```text
INCLUDE_KO                   49,627
UNRESOLVED                    2,864
NON_KOREAN_TARGET            14,496
TOTAL                        66,987
```

Semantic detail:

```text
INCLUDE_KO_NO_ESCAPE                 28,151
INCLUDE_KO_RUNTIME_EXPANSION         14,724
INCLUDE_KO_FIXED_SURFACE_PARTICLE     6,125
INCLUDE_KO_CHOICE                       627
UNRESOLVED_PARTICLE_RISK              2,864
NON_KOREAN_TARGET                    14,496
TOTAL                                66,987
```

Binding-family split:

```text
direct/header-preserved
  INCLUDE_KO              49,596
  UNRESOLVED               2,864
  NON_KOREAN_TARGET       14,496
  TOTAL                   66,956

overlap-composite
  INCLUDE_KO                  31
  UNRESOLVED                   0
  NON_KOREAN_TARGET            0
  TOTAL                       31
```

The ten V366 runtime-only owners classify as:

```text
INCLUDE_KO   9
UNRESOLVED   1
TOTAL       10
```

No owner is unclassified and no new source membership is introduced.

## 4. Switch runtime event_len formula

Direct ARM64 handler evidence establishes:

```text
0x11 handler   0x160334
0x12 handler   0x16049C
0x13 handler   0x1605AC
0x15 handler   0x16068C
```

For `0x11/0x12/0x13`, Switch runtime consumption is:

```text
(strlen(payload) + 8) & ~3
```

The V334 helper expression is:

```text
4 + align4(strlen(payload) + 1)
```

These are algebraically identical:

```text
4 + ((strlen + 1 + 3) & ~3)
= 4 + ((strlen + 4) & ~3)
= (strlen + 8) & ~3
```

For `0x15`, the handler uses the header choice count and consumes each NUL-terminated choice with
the same four-byte alignment rule:

```text
4 + sum(align4(strlen(choice) + 1))
```

This is also the V334 `event_len()` contract. The earlier intermediate hypothesis that the V334
formula and Switch formula differ is false and must not be reused.

## 5. Universal runtime replay

Independent binary-formula replay over the frozen V366 universe gives:

```text
direct source formula checks            66,956 / 66,956 PASS
direct KO target formula checks         66,956 / 66,956 PASS
composite source formula checks             31 / 31 PASS
composite final-owner formula checks        31 / 31 PASS
formula mismatches                              0
```

Direct opcode population:

```text
0x11   54,363
0x12    2,916
0x13    8,902
0x15      775
TOTAL   66,956
```

Source-to-KO runtime owner-span topology:

```text
direct rows                           66,956
topology preserved                    66,956
topology mismatches                        0
new one-sided containment violations       0
```

Partition-contained rows are `66,954 / 66,956` on both source and KO sides. The two inherited
stock exceptions are editor-recognized disguised `0x15` tails:

```text
ECF00000  source 0xDAB1C -> target 0x10FA8C
EPF11700  source 0x12BC  -> target 0x179C
```

Both preserve the same source/KO runtime-span state and both are `NON_KOREAN_TARGET`; they are not
new Koreanization defects.

For the 31 overlap-composites:

```text
source event_len == source owner length                  31 / 31
final selective event_len == final selective owner len   31 / 31
runtime continuity                                        PASS
```

Therefore the V366 universal runtime event_len / command-boundary continuity claim is CLOSED PASS.

## 6. Editor-owner versus runtime-span topology

Runtime continuity PASS does not imply a one-to-one relation between PC-editor grouped items and
Switch runtime spans. The independent replay records:

```text
direct editor-item len == runtime len        60,180
direct editor-item len != runtime len         6,776
TOTAL                                        66,956

multi-owner runtime-span rows                  2,240
  NON_KOREAN_TARGET                            2,149
  INCLUDE_KO                                      89
  UNRESOLVED                                       2
```

The 89 product-relevant INCLUDE_KO outer spans contain other frozen owners. INCLUDE_KO outer to
INCLUDE_KO inner relations total 128:

```text
direct-inner relations       106
composite-inner relations     22
TOTAL                         128
```

Direct disguised-`0x15` rows total 127:

```text
NON_KOREAN_TARGET   99
INCLUDE_KO          28
```

Twenty-seven of the 28 INCLUDE_KO disguised-`0x15` rows are multi-owner runtime spans.

These counts are a serializer-design constraint, not a runtime-continuity failure. Source membership
continues to use the V366 PC-editor/source-owner authority, while future write-conflict analysis must
add the Switch runtime-span topology as a separate layer.

## 7. Rejected / do not repeat

The following intermediate claims were produced by an incorrect comparison of two algebraically
equivalent event-length formulas and are explicitly rejected:

```text
"V334 event_len differs from the Switch handler"
"52,290 rows have a V334-vs-Switch length conflict"
"12 sampled files contain 8,512 source/KO runtime phase mismatches"
"13 of 31 composites have runtime phase mismatch"
"runtime event_len closure is FAIL"
```

Do not reuse those counts or conclusions.

Also rejected:

- every editor owner is a one-to-one Switch runtime command span;
- every text-like runtime span must terminate inside the same editor partition;
- the two inherited disguised-`0x15` tails are Koreanization-created defects;
- semantic classification must be redesigned to close the full 169-file family.

## 8. Closed claims and remaining boundary

V367 closes:

```text
V366 source membership/binding          inherited CLOSED
whole-family semantic admission replay  CLOSED PASS
universal runtime event_len continuity  CLOSED PASS
direct source/KO runtime topology        CLOSED PASS
31 composite runtime continuity          CLOSED PASS
```

Not implemented or changed:

```text
product EVENT serializer             NONE
EVENT/TAI5MSG mutation               NONE
build/package/IPS                    NONE
hardware                             NOT RUN
```

The remaining implementation-design risk is the product-relevant multi-owner runtime-span family,
not event_len correctness.

## 9. Exact next scope

`EVENT_169_RUNTIME_OVERLAP_CLUSTER_SERIALIZER_DESIGN_READ_ONLY`

READ ONLY. Treat V366 membership/binding and V367 semantic/runtime closure as frozen. Census and
cluster the 89 INCLUDE_KO multi-owner outer spans and all 128 INCLUDE_KO-to-INCLUDE_KO inner
relations, then intersect those clusters with the existing ECF overlay modules before proposing a
serializer implementation. Do not modify product bytes, builder code, package, IPS, or hardware in
that scope.
