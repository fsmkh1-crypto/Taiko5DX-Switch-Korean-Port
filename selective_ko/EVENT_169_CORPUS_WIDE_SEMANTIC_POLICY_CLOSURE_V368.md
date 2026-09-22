# EVENT 169 corpus-wide semantic policy closure — V368

Date: 2026-09-22 (KST)

```text
validation_id   V368
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_CORPUS_WIDE_SEMANTIC_POLICY_CLOSURE
parent          7f9822f27fe9b3696ffb914fc856d2f68d5109e7 / V367
implementation  NONE
product bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

## 1. Frozen authorities

```text
V366 source-owner universe          66,987
V366 direct/header-preserved        66,956
V366 overlap-composite                  31
V367 runtime event_len continuity      PASS
V367 direct runtime topology            PASS 66,956 / 66,956
V367 composite runtime continuity       PASS 31 / 31
```

V368 does not change V366 membership/binding and does not reopen V367 runtime closure.

Canonical V366 large artifact identity remains:

```text
archive bytes   2,211,822
archive sha256  430ab6394ade066c5314ac734819d68cd9f24554da2a5346bc23031019712b1c
DIRECT_HEADER_PRESERVED.jsonl bytes   34,971,518
DIRECT_HEADER_PRESERVED.jsonl sha256  6e7ca36d05a1a79e4e0918645f27a72b05c05505f66ac33a683e745b03da3d60
```

## 2. Raw semantic baseline and exact-policy overlay

V367 raw replay:

```text
INCLUDE_KO                   49,627
UNRESOLVED                    2,864
NON_KOREAN_TARGET            14,496
TOTAL                        66,987
```

Already-canonical exact-policy membership:

```text
V348/V349 direct particle     350
V350 lexical 가문              12
V351/V352 derived + mixed      61
V353/V360 suffix                3
--------------------------------
TOTAL                          426
```

Therefore the exact residual input is:

```text
2,864 - 426 = 2,438
```

## 3. Corpus-wide residual closure

The residual audit covered 2,438 exact source owners in 106 EVENT files and 2,671 detector-related occurrences.
Admission authority is V366 owner binding + actual PC-KO bytes + exact occurrence locator +
Switch runtime/control ownership, plus established TAI5MSG root authority where cross-carrier data is involved.
Class labels and fallback are not authority.

Final cause-family accounting:

```text
direct particle                                 1,334
copula / derived / composite particle surface    363
lexical 가문                                      702
lexical 가신                                        2
cross-carrier authored suffix                     14
direct + derived                                  12
direct + lexical 가문                               2
derived + lexical 가문                              4
direct + cross-carrier suffix                      5
-----------------------------------------------
TOTAL                                           2,438
UNRESOLVED                                          0
```

Cross-carrier roots used here remain tied to the existing V357 B0 authorities:

```text
\%05 -> B0:73
\%06 -> B0:82
\%07 -> B0:91
\%0B -> B0:139
\%23 -> B0:328
```

## 4. Final three-row occurrence-ownership closure

All three remaining rows are justified INCLUDE; no fallback is used.

```text
EFF27C00.TS5 source 0x3BA0 -> PC-KO 0x41F8   INCLUDE_KO
EFF27C00.TS5 source 0x3BA8 -> PC-KO 0x4200   INCLUDE_KO
EFF2D100.TS5 source 0x7A34 -> PC-KO 0x8AF0   INCLUDE_KO
```

`EFF27C00 0x3BA0` is an outer runtime span containing inner owner `0x3BA8`.
Source/target containment topology is preserved:

```text
source outer   0x3BA0..0x3BE0
source inner   0x3BA8..0x3BE0
PC-KO outer    0x41F8..0x4250
PC-KO inner    0x4200..0x4250
```

The outer detector sees exactly the same absolute occurrences as the inner owner:

```text
0x4211   \#0064 + ED61   (는)
0x4229   \#08AE + F2CB   (와)
```

Outer-exclusive particle occurrences: 0.

`EFF27C00 0x3BA8` preserves the runtime escapes and the following Korean particles are authored EVENT literals.
The previously noted leading-byte ambiguity does not overlap the exact escape/particle locators.

`EFF2D100 0x7A34` is the same nested-ownership cause family:

```text
source outer   0x7A34..0x7A78
source inner   0x7A38..0x7A78
PC-KO outer    0x8AF0..0x8B48
PC-KO inner    0x8AF4..0x8B48
0x8B0C         \#01FA + EF45   (를)
```

Outer-exclusive particle occurrences: 0.

Across the full V367 raw UNRESOLVED population, the multi-owner runtime-span UNRESOLVED rows are exactly these two outer owners.

Nested occurrence delegation requires all of:

```text
1. V366 exact owner binding
2. source/target runtime containment topology preserved
3. outer occurrence == inner occurrence at the exact absolute byte locator
4. outer-exclusive particle occurrence count == 0
5. inner owner independently admitted
```

## 5. Post-policy semantic accounting

```text
V367 raw INCLUDE_KO                    49,627
existing exact-policy promotion            426
V368 generalized-policy promotion        2,438
------------------------------------------------
post-policy INCLUDE_KO                  52,491
post-policy UNRESOLVED                       0
NON_KOREAN_TARGET                       14,496
TOTAL                                   66,987
```

Binding split:

```text
direct/header-preserved INCLUDE_KO      52,460
direct/header-preserved UNRESOLVED           0
direct/header-preserved NON_KOREAN      14,496
direct/header-preserved TOTAL           66,956

overlap-composite INCLUDE_KO                31
overlap-composite UNRESOLVED                 0
overlap-composite TOTAL                     31
```

All ten V366 runtime-only valid owners are admitted after policy overlay.

## 6. Serializer-design constraint update

V367 runtime topology remains valid. Only the semantic subset changes:

```text
multi-owner runtime-span rows                  2,240   unchanged
NON_KOREAN_TARGET                              2,149
INCLUDE_KO                                        91   supersedes raw V367 89
UNRESOLVED                                         0   supersedes raw V367 2

INCLUDE -> INCLUDE inner relations               130   supersedes 128
direct-inner relations                            108   supersedes 106
composite-inner relations                          22   unchanged
```

## 7. Rejected / do not repeat

- residual/unknown -> DIRECT_PARTICLE fallback;
- Work class output as ground truth;
- class-name-only promotion;
- ECF exact membership treated as corpus-wide proof without row provenance;
- every percent escape treated as a simple value substitution;
- lexical `가신` folded into 조사 or `가문`;
- nested outer detector hits counted as separate grammar hazards when they are exact inner occurrences;
- EFF27C00 0x3BA8 leading-byte ambiguity treated as an occurrence blocker;
- changing V366 membership or V367 runtime continuity to force semantic closure;
- post-policy serializer census using 89 outer / 128 relations.

The earlier fallback-based Work result happened to produce the same aggregate `52,491 / 0`;
that derivation remains rejected. V368 reaches the result through exact provenance.

## 8. Claim boundary

```text
V366 source membership/binding             CLOSED / unchanged
V367 runtime event_len/topology             CLOSED PASS / unchanged
V368 post-policy semantic admission         CLOSED
EVENT UNRESOLVED                            0
product EVENT serializer                    NONE
EVENT/TAI5MSG mutation                      NONE
build/package/IPS                           NONE
hardware                                    NOT RUN
```

## 9. Exact next scope

`EVENT_169_RUNTIME_OVERLAP_CLUSTER_SERIALIZER_DESIGN_READ_ONLY`

READ ONLY. Freeze V366 membership/binding, V367 runtime continuity, and V368 semantic closure.
Use 91 product-relevant INCLUDE_KO multi-owner outer spans and 130 INCLUDE-to-INCLUDE relations.
Intersect those clusters with existing ECF overlay modules before proposing implementation.
No builder/product mutation, build, package, IPS, or hardware.
