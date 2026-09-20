# ECF00000 percent-macro ↔ TAI5MSG B0 46-root replacement preimplementation capacity / serializer admission — V356

Date: 2026-09-21 (KST)

```text
validation_id   V356
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_PREIMPLEMENTATION_CLOSURE
parent          2f2d995cb75dc03b13f05c716593be7eefb5be89 / V355 resume state synchronized
implementation  NONE
product bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

## 1. Scope and authorities

This scope admits only the exact 46 B0 roots frozen by V355 against the current V320-era selective TAI5MSG serializer. It does not add the roots to V303 membership, mutate the serializer, emit a TAI5MSG, build/package/IPS, or run hardware.

Canonical inputs:

```text
PC original TAI5MSG sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f
PC Korean TAI5MSG sha256    e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
V355 root rows Git blob     79ae7f379737527e805f88764c7eabd5162044d0
B0 length shard Git blob    b38fc8ef7fc9037992114519cc896947d50f596c
current serializer Git blob b5d7062e055503799803891ad24e5240d05b57bc
```

The V314 Drive cache was used directly; both TAI5MSG source hashes matched their canonical identities. Exact source/target message SHA-256 guards for all 46 locators are materialized in the V356 admission artifact.

## 2. Exact membership / collision result

```text
V355 roots                         46
unique B0 locators                 46
existing V303 B0 selected       10, 11
overlap with V303 B0               0
source != target                  46 / 46
source bytes total            13,916
target bytes total            14,494
raw payload delta               +578 / +0x242
```

V303's canonical 3,179-row membership remains unchanged. The new family is a separate exact B0 program-overlay population. If implemented, the effective replacement-locator set would be 3,179 + 46 disjoint locators, but this does not mint or rewrite V303 candidate/classification IDs.

## 3. B0 capacity and package projection

Current B0 state under the V320-era serializer is stock B0 plus existing V303 locals 10 and 11:

```text
B0 stock used_end               59,287 / 0xE797
B0 stock declared               59,328 / 0xE7C0
B0 current used_end             59,322 / 0xE7BA
B0 current filler                    6 / 0x0006
```

After exact 46-root PC-KO replacement:

```text
B0 projected used_end           59,900 / 0xE9FC
B0 projected declared           59,904 / 0xEA00
B0 projected filler                  4 / 0x0004
B0 declared growth                 576 / 0x0240
runtime block capacity         131,072 / 0x20000
B0 remaining capacity            71,168 / 0x11600
capacity verdict                 PASS
```

The payload itself grows by 578 bytes, but only 576 additional declared bytes are required because 6 bytes of the current B0 filler are consumed and the rebuilt block is aligned to 0x40.

Current V320 output projection baseline:

```text
current total growth             0x70C0
current final size             1,839,753 / 0x1C1289
current B32 offset               0x1B4840
```

V356 exact projected structure after implementing only this family:

```text
projected total growth           0x7300
projected final size           1,840,329 / 0x1C14C9
projected B32 offset              0x1B4A80
downstream B1..B32 offset shift   +0x0240
B32 internal used/declared        unchanged
largest declared block            remains 0x12B00
```

No projected output SHA is claimed because no output bytes were built in this READ ONLY scope.

## 4. Serializer admission contract

The 46-root family is admitted for a dedicated exact-message overlay path, not for V303 prose membership.

Implementation must fail closed unless all of the following hold:

1. whole-file PC original and PC-KO TAI5MSG identities match the canonical hashes;
2. the V356 46-row locator set is exact, unique, all in B0, and disjoint from V303/V304/V315/V320 mutation owners;
3. each stock B0 message length and SHA-256 matches the V356 source guard;
4. each same-locator PC-KO message length and SHA-256 matches the V356 target guard;
5. all 46 source and target payloads differ, including the two zero-length-delta roots;
6. target bytes are copied exactly from canonical PC-KO same-locator payloads; no hand translation or byte synthesis is allowed;
7. existing V303/V304/V315/V320 behavior remains byte-identical outside the new 46-root family plus serializer-owned block/header offset changes;
8. post-reparse confirms the 46 targets exactly and confirms no unrelated B0 payload mutation;
9. B0 declared size is exactly 0xEA00 and runtime capacity remains <=0x20000;
10. projected structural values above are reproduced before any package/hardware step.

## 5. Program-payload validation boundary

The 46 roots are B0 program payloads. The existing V303 prose validator `_validate_selected_message` is not semantically applicable to this family: it treats normal B0 program-control bytes, including 0x02-bearing program structure, as prose-control violations.

Therefore implementation must not force these 46 roots through the V303 prose validator merely to reuse an existing gate. The correct guard for this family is exact source/target message identity plus the already established B0 runtime ownership and same-locator PC-patch oracle.

If additional literal/code-domain validation is added later, it must be program-aware and must not scan raw B0 bytecode as if every byte were rendered text.

## 6. 확정된 사실

- exact 46-root membership is disjoint from current V303 B0 locals 10/11;
- all 46 source/target message pairs are hash-guardable from canonical V314 original/PC-KO sources;
- aggregate payload delta is +578, while aligned B0 declared growth is +576;
- projected B0 declared size 0xEA00 is far below runtime capacity 0x20000;
- only B0 physical/declaration growth and downstream absolute block offsets are structurally affected;
- the existing generic prose validator is the wrong semantic validator for this B0 program family.

## 7. 유력한 가설

A dedicated exact-message overlay using the V356 guards should reproduce the projected 0xEA00 B0 / 0x7300 total-growth structure without altering unrelated payloads.

This remains an implementation hypothesis until the exact overlay is implemented and replayed.

## 8. 미확정 사항

- final deterministic output SHA after the 46-root overlay;
- post-implementation program-aware validation details beyond exact-message identity;
- Eden / physical Switch behavior after packaging;
- whether any later cleanup should consolidate this overlay with generic correction infrastructure.

## 9. 기각된 가설 / do-not-repeat

- add +578 directly to final file size: REJECTED; alignment/filler makes declared growth +576;
- add the 46 roots into V303's 3,179 prose membership: REJECTED;
- reuse `_validate_selected_message` unchanged for B0 program roots: REJECTED;
- patch only V353's %15/%21/%2A witnesses: REJECTED;
- globally replace unrelated B0 messages: REJECTED;
- rescan all 14,832 TAI5MSG messages: NOT REQUIRED for this cause family.

## 10. 관련 영향 범위

Potential implementation impact is bounded to:

- exact 46 B0 message payloads;
- B0 used/declaration size;
- header/block absolute offsets for B1..B32;
- serializer postconditions and tests for the new overlay family.

Unchanged by this analysis:

- V303 membership 3,179;
- V304/V315/V320 correction populations;
- EVENT V349/V350/V352 results;
- Mapping/font assets;
- ExeFS IPS;
- product package;
- hardware runtime.

## 11. 수정 제안 / exact next scope

`ECF00000_PERCENT_MACRO_TAI5MSG_B0_46_ROOT_REPLACEMENT_IMPLEMENTATION_OFFLINE_VALIDATION`

Implement exactly the V356 46-row exact-message overlay, preserve V303 membership as-is, add family-specific source/target guards and postconditions, reproduce the V356 capacity projection, and run deterministic offline regression. Do not build/package/IPS or run hardware in that scope.

A fresh explicit user execution signal is required before implementation.
