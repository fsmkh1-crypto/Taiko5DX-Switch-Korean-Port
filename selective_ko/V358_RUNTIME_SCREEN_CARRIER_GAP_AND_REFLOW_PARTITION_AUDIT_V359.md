# V358 runtime screenshot carrier-gap / reflow partition audit — V359

Date: 2026-09-21 (KST)

```text
validation_id   V359
track           SWITCH_SELECTIVE_KOREANIZATION
parent          6223b67ef58b160ca2391e8ea668cd0c49cff382 / V358
scope_kind      READ_ONLY_RUNTIME_EVIDENCE_AND_CAUSE_PARTITION
product bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
hardware        USER EDEN SCREENSHOTS ONLY
```

## 1. Scope

V359 records the user-supplied Eden screenshots observed immediately after the V358 diagnostic
package handoff and partitions the visible symptoms by carrier/cause family.

The screenshots do not independently attest the installed ZIP hash on the device, so V359 records
them as user runtime evidence tied by conversation context, not as a device-side cryptographic
package-identity proof.

No implementation, TAI5MSG mutation, EVENT mutation, SNR mutation, IPS, package rebuild, or hardware
write occurs in V359.

## 2. Observed runtime pattern

Five screenshots show a consistent mixed-language pattern:

```text
screen 1  1554 scenario/chapter synopsis body                    JP
screen 2  person detail: dedicated name/UI JP, biography body   KO
screen 3  ordinary dialogue body                                JP
screen 4  landmark: dedicated place name JP, description body   KO
screen 5  ordinary dialogue body                                JP
```

The Korean description routes prove that Korean font/page/TAI5MSG rendering remains active on the
observed routes. The Japanese dialogue routes do not establish a V357 TAI5MSG failure because V358
explicitly excluded EVENT/TS5.

The dedicated Japanese person/place fields remain consistent with the binding identity policy.

## 3. V358 package omission boundary

V358 contains exactly:

```text
SELECTIVE_PACKAGE_INFO.json
exefs/D9120950C258610A746F4A31CE3A3B376DE393D9.ips
romfs/FONT/FONT_JPN.G1T
romfs/TAI5MSG_JP.DAT
```

It explicitly excludes EVENT, inline 139, SNR, ordinary non-B24 584 reflow, and unrelated carriers.

Therefore the observed mixed language is expected from the V358 isolation boundary and must not be
treated as proof that the Korean font, Mapping/page mapper, or V357 TAI5MSG is globally inactive.

## 4. EVENT implementation state

Switch/PC parity authority already proves:

```text
Switch v1.1.3 / PC-original ECF00000.TS5
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09
```

Current direct-path mapping authority records:

```text
PC data/EVENT/*.TS5
-> Switch romfs/EVENT/*.TS5
status PATH COMPATIBLE
```

The latest implemented EVENT diagnostic before the cross-carrier discovery is V352:

```text
V352 ECF00000.TS5
bytes   1,109,356
sha256  e61569508ffc9995f78df51f01b42be5402b79d5e26a8c8f3e71c0448d8eaaeb
Drive   1mIkFwodiotxI6gV0iGGeuW33vC5vEq46
status  DIAGNOSTIC ONLY / NOT PACKAGED
```

V352 includes the implemented EVENT semantic population through its 423/426 code-5 state, but the
following exact three rows remained deferred:

```text
row 4743    partition 208   original 0x60248   %21 -> TAI5MSG B0:M349
row 5059    partition 215   original 0x64898   %15 -> TAI5MSG B0:M209
row 11440   partition 604   original 0xC3988   %2A -> TAI5MSG B0:M395
```

V353 explicitly rejected raw-copying those three PC-KO EVENT commands while the corresponding
language-bearing TAI5MSG B0 roots were still Japanese.

V357 has since implemented the full exact 46-root B0 percent-macro family, including these three
roots. Therefore the original cross-carrier blocker is now closed on the TAI5MSG side, but the three
EVENT rows themselves have still not been implemented into a post-V352 EVENT output.

Conclusion:

```text
package V352 EVENT as "current final EVENT"    REJECTED
next prerequisite before EVENT integration    implement exact suffix-three EVENT rows
```

## 5. Inline 139 state

The selective inline population is:

```text
V298 ending-help    39 INCLUDE_KO
V299 numeric        53 INCLUDE_KO
V300 static         47 INCLUDE_KO
--------------------------------
total              139 INCLUDE_KO
```

However V298/V299/V300 are candidate/classification materializations only and explicitly record no
builder/build/IPS realization.

Therefore inline 139 must not be silently merged into an EVENT integration package. It remains a
separate implementation carrier.

## 6. Line-break / reflow evidence

The user additionally reported visibly poor Korean line breaking. The supplied landmark screenshot
contains an especially clear token split around the phrase rendered visually as:

```text
... 함께 조
모
3산이라 ...
```

This is not an EVENT-carrier symptom.

V313 already closed the selected TAI5MSG overflow census:

```text
selected hard-overflow rows           697
ordinary non-B24 safe reflow          584
  B17..B20 HELP_RENDERER              156
  B22_DESCRIPTION                     308
  B23_DESCRIPTION                     120
B24 hard-overflow                     109
B0/B21 caller-specific waits            4
```

V320 implemented only the B24 body-layout family:

```text
B24 native-wrap rows implemented      108
ordinary non-B24 584                  DEFERRED / NOT IMPLEMENTED
```

The V313 proposed ordinary non-B24 mutation contract is byte-conservative:

```text
SPACE 0x20 <-> NEWLINE 0x0A only
preserve all game-code glyph bytes
preserve control sequences
preserve token order
wrap at <=40 half-width units
never split a Korean whitespace-delimited token when a prior legal boundary exists
```

The current screenshots are consistent with that known unresolved family. Exact screenshot-to-locator
binding was not established in V359, so no individual B22/B23 message is newly claimed here.

## 7. Scenario synopsis / SNR boundary

The scenario/chapter synopsis in screen 1 remains Japanese.

Its presentation is consistent with a scenario-data carrier, but V359 does not claim an exact SNR
locator without a direct source binding.

V358 excludes SNR, and no current SNR implementation authority is promoted by V359.

Therefore:

```text
screen-1 Japanese synopsis != EVENT integration failure proof
screen-1 exact carrier       UNCONFIRMED in this scope
SNR remains separate
```

## 8. 확정된 사실

1. V358 is an isolated TAI5MSG/IPS/font package and excludes EVENT, inline, SNR and non-B24 reflow.
2. User runtime screenshots show Korean TAI5MSG-style description bodies while ordinary dialogue remains Japanese.
3. V352 exact EVENT output exists and passed offline structural validation but was never packaged.
4. V352 is not the final cross-carrier EVENT state because rows 4743/5059/11440 remained deferred.
5. V357 now supplies the exact B0 roots required by those three EVENT rows.
6. The three EVENT rows still require an explicit post-V357 implementation/replay before packaging.
7. Inline 139 is classified INCLUDE_KO but not implemented.
8. Ordinary non-B24 584 reflow remains unimplemented.
9. B24 108-row native-wrap correction is already implemented and must not be reopened merely because non-B24 wrapping remains poor.

## 9. 유력한 가설

- The Japanese ordinary-dialogue screens are primarily explained by the absence of EVENT/TS5 from V358.
- The visible Korean description word-splitting is consistent with the already-known non-B24 584 reflow family.
- A post-V357 three-row EVENT completion followed by a dedicated EVENT+V357 package should expose the
  intended EVENT Korean route without requiring font/Mapping changes.

These remain runtime hypotheses until the corresponding isolated implementation/package tests run.

## 10. 미확정 사항

- exact locator/carrier of each supplied screenshot;
- exact SNR ownership of screen 1;
- exact B22/B23 locator of the visible landmark-description wrap defect;
- runtime behavior of a post-V357 completed EVENT payload;
- inline-139 implementation;
- ordinary non-B24 584 reflow implementation.

## 11. 기각된 가설 / do-not-repeat

- V358 proves EVENT Koreanization failed — REJECTED; EVENT is absent from V358.
- V358 Korean font or TAI5MSG is globally inactive — REJECTED by visible Korean descriptions.
- package raw V352 as the final current EVENT payload — REJECTED; suffix-three remains absent.
- fix EVENT omission and 584 reflow in one diagnostic build — REJECTED; separate cause families.
- add inline 139 merely because it is INCLUDE_KO — REJECTED; implementation is absent.
- treat the scenario synopsis as proven EVENT content — REJECTED.
- reopen B24 native-wrap 108 solely because non-B24 descriptions wrap poorly — REJECTED.

## 12. 관련 영향 범위

Carrier / state matrix:

```text
TAI5MSG V357                  IMPLEMENTED / PACKAGED V358
TAI5MSG B24 108 reflow        IMPLEMENTED
TAI5MSG ordinary non-B24 584  NOT IMPLEMENTED
EVENT V352                    IMPLEMENTED DIAGNOSTIC / NOT PACKAGED
EVENT suffix-three            TAI5MSG DEPENDENCY CLOSED / EVENT ROWS NOT IMPLEMENTED
inline 139                    CLASSIFIED / NOT IMPLEMENTED
SNR                           OUTSIDE CURRENT IMPLEMENTED PACKAGE
identity presentation         KEEP_JP
```

## 13. 수정 제안 / exact next scope

Next executable cause-family:

`ECF00000_SUFFIX3_POST_V357_EVENT_IMPLEMENTATION_OFFLINE_VALIDATION`

Required work:

1. start from exact V352 EVENT output authority;
2. consume the three exact V353 row bindings only;
3. use the canonical PC-KO EVENT command bytes;
4. admit them only because the required V357 B0 roots are now exact product payloads;
5. rerun V337 generic relocation, V338 special-span, V339 5A, and V340/V344 residual gates;
6. require deterministic byte-identical rerun and exact mutation accounting;
7. produce a new EVENT diagnostic identity;
8. do not package it yet;
9. do not modify TAI5MSG, non-B24 584 reflow, inline 139, SNR, IPS or font.

Only after that cause-family closes should a separate package-integration scope combine:

```text
new post-V357 EVENT ECF00000.TS5
+ V357 TAI5MSG
+ existing verified IPS
+ existing Korean font
```

The ordinary non-B24 584 reflow remains a later independent cause-family and must not be mixed into
that EVENT diagnostic build.
