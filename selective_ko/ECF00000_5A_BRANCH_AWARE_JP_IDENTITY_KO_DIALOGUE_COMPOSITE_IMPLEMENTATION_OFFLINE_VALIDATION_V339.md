# ECF00000 5A BRANCH-AWARE JP IDENTITY / KO DIALOGUE COMPOSITE IMPLEMENTATION — V339

Date: 2026-09-20 (KST)

```text
validation_id   V339
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          c93474d6021a734a1fdf0d460a59fe43b2863b1f / V338
scope           ECF00000_5A_BRANCH_AWARE_JP_IDENTITY_KO_DIALOGUE_COMPOSITE_IMPLEMENTATION_OFFLINE_VALIDATION
product_bytes   NOT PUBLISHED
build/package   NONE
hardware        NOT RUN
```

V339 implements only the `0x5A` composite family discovered after the aborted S4 replacement attempt. Dedicated identity remains Japanese. Korean dialogue comes from the exact PC Korean patch. The implementation is branch-aware and resolves dependencies from later `0x5A` objects toward earlier ones inside each original edit partition.

## 1. Why this stage exists

V334/V335 exactly cover the `11/12/13/15` runtime target universe, but the full PC patch also mutates editor-owned `1E/5A/3C` objects. `0x5A` is structurally special because Switch runtime length depends on NUL positions in the two name fields and dialogue and can inspect bytes following the PC-editor-owned `0x5A` object.

A first `JP name + KO dialogue` prototype therefore could not be treated as an ordinary payload copy. The exact affected outer runtime-relevant `0x5A` mapping was frozen before implementation.

## 2. Exact compact mapping

Repository artifact:

`selective_ko/artifacts/ecf00000_v339_5a_composite_v1/MAPPING_ORIGINAL_KO_5A_COMPACT.bin`

```text
records        1,088
record size       16 bytes
serialization  <HHIIHH

partition       uint16_le
ordinal         uint16_le   # 0x5A ordinal inside partition
original_offset uint32_le
ko_offset       uint32_le
original_length uint16_le
ko_length       uint16_le

artifact size   17,408 bytes
sha256          6aafe3b284e3ec65a7f2928334bffa9a81b15b54d47c85928484a3b59058c97e
rowset sha256   255a1b40ad776ac55f3d034f64075782c4e51f51227747180237df134694a774
partitions      63
```

The mapping is bound to exact stock and PC-KO identities:

```text
stock ECF00000.TS5
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09

PC-KO ECF00000.TS5
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
```

## 3. Implementation

New module:

`builder/selective_event_5a.py`

Local validated SHA-256 before Git materialization:

`16eb972dfd099ddc2faf183ce5616fdf343ab9b1ba05e323e77275ed0ca9fab9`

The implementation provides:

- compact mapping loader with count/SHA/rowset/collision gates;
- exact three-field `0x5A` parser;
- JP-name / KO-dialogue composite builder;
- Switch `0x5A` runtime-length formula;
- exact original target-anchor discovery;
- per-partition reverse dependency solve;
- branch/special-span-aware candidate evaluation;
- final all-row runtime-target verification;
- exact canonical count and rowset-hash gates.

The solver does not fresh-reparse final Korean bytes to rediscover ownership.

## 4. Binding 5A policy

Exact mapping population:

```text
outer runtime-relevant 5A     1,088
name-only PC-KO changes          14
KO-dialogue rows               1,074
```

The 14 name-only rows preserve the complete original `0x5A` object.

The 1,074 dialogue rows preserve the original JP name fields and use the PC-KO dialogue field. Resolution is determined from the current layout, not hard-coded row offsets.

Final canonical solve:

```text
ORIGINAL_TARGET               1,058
CHOICE_NEXT_START                15
ZERO_NEXT_TERMINATOR              1
-----------------------------------
translated rows                1,074
```

Padding realization:

```text
no extra padding                 992
dialogue +1 ASCII space           40
dialogue +2 ASCII spaces          15
dialogue +3 ASCII spaces          11
name2 +2 ASCII spaces             16
-----------------------------------
modified by alignment policy       82
```

The 16 name2-padding rows are the 15 choice-coupled rows plus the single branch-interaction zero-terminator row.

## 5. Branch-aware dependency rule

`0x5A` evaluation must not be performed once and then followed by branch repair.

A later `0x5A` mutation can change bytes inspected by an earlier `0x5A`, and a relocated branch header can likewise introduce a new NUL byte into an earlier `0x5A` runtime scan.

Binding algorithm:

```text
base current layout
-> partition-local translated 5A rows initialized as JP name + KO dialogue
-> process each partition's 5A rows from later item to earlier item
-> for every candidate, recalculate current V337 generic branches + V338 special spans
-> try ORIGINAL_TARGET with dialogue padding 0,1,2,3
-> if exact original target cannot be preserved:
     allow CHOICE_NEXT_START only for the proven immediate 0x15 coupled subtype
     allow ZERO_NEXT_TERMINATOR only for the proven immediate 0x00 subtype
     both use name2 +2 ASCII spaces
-> apply final branch/special repair
-> verify all 1,074 runtime outcomes again
```

## 6. Previously hidden branch interaction

The preimplementation cross-check found one row that invalidated the earlier independent-5A assumption:

```text
partition        118
original 5A      0x3FE34
PC-KO counterpart 0x504B8
```

A later generic branch owner at original `0x3FE58` changes from:

```text
04 01 B0 05
```

to a layout-dependent header containing a new NUL byte. That changes the preceding `0x5A` runtime scan.

This row cannot preserve the old physical target using dialogue padding 0..3. The source-proven PC-KO behavior makes the `0x5A` self-contained; with original JP name fields, adding two ASCII spaces to the second name reproduces the self-contained geometry without translating the name.

Policy:

`ZERO_NEXT_TERMINATOR / name2 +2 spaces`

This cause is recorded in `KNOWN_FAILURES.md` so a future implementation does not reintroduce the invalid `solve 5A first -> repair branches later` ordering.

## 7. Exact rowset gates

```text
modified 82
sha256  26bc49d7a19cafa2e75aed11be2fa2f3874442b07cb55db92f1e7f7dd2b3d016

dialogue-padding 66
sha256  00bef7fff43008f41014f358611d890c6ac4e7857502c026f2afc6bc6c47eead

choice-coupled 15
sha256  0579d61f80c791e041c056e9a83fce785e5af8b1edf101a91a910b63dd8d0446

zero-terminator 1
sha256  538065cd4a3886366d236e574bd9010306867409e4bd7b698ae9b40d5a7ae9eb
```

The implementation treats these hashes as validation postconditions, not as a hard-coded list of offsets.

## 8. Unit validation

New test module:

`tests/test_selective_event_5a.py`

Local validated SHA-256 before Git materialization:

`285bf186962ccd1a342e2044c5566ae8cf53fefeff410b7d7b41303e17e46717`

Tests:

```text
compact mapping identity                PASS
mapping corruption rejection            PASS
JP names + KO dialogue composition      PASS
name2/dialogue padding placement        PASS
real-stock 5A runtime-length fixture    PASS
name-only row original preservation     PASS
--------------------------------------------
unit tests                              PASS_6_OF_6
```

## 9. Exact-corpus offline validation

The solver was run against the exact stock and PC-KO ECF files in the same partial S4 context used to expose the `0x5A` problem: V335 codes 1/2/4 applied, code 3 deferred, codes 0/5 original.

Result:

```text
mapping rows                  1,088
translated                    1,074
name-only original               14
verification violations            0
```

After final V337 generic relocation and V338 special-span repair:

```text
diagnostic output size       1,081,644
diagnostic output sha256     9d5821f0cc35356f68d1f243adc644c4be635e62ca4d9154bfe665cb612fd40c
baseline walker errors                0
5A runtime violations                 0
```

The state-aware diagnostic walker still reports exactly one previously separated residual overrun:

```text
partition       593
source original 0xBDD78
opcode          0x0E
```

That residual is outside the `0x5A` cause-family and is not modified by V339.

## 10. Scope boundary

V339 does not implement or authorize:

- `1E` semantic admission;
- `3C` mutation (`KEEP_JP` remains current direction);
- the partition-593 `0x0E` residual fix;
- V335 code-3 `FIXED_SURFACE_PARTICLE_V1` transformation;
- completion of S4;
- final ECF product output;
- package/build/IPS;
- hardware execution;
- other EVENT files or SNR.

The `9d5821...` TS5 is diagnostic only and is not a product artifact.

## 11. Rejected / do-not-repeat

Reject:

- translate 5A names to Korean merely to inherit PC-KO geometry;
- hard-code 82 special offsets as the implementation policy;
- solve every 5A independently;
- solve all 5A first and only then repair branch headers;
- preserve the old inside-choice target for the 15 coupled rows after replacing the choice payload;
- treat the partition-118 zero-terminator case as ordinary dialogue padding;
- reopen V336/V337/V338 merely because this later payload family was incomplete.

## 12. Current disposition and next scope

```text
S1 no-op serializer core                 CLOSED_V336
S2 generic relocation                    CLOSED_V337
S3 Switch special spans                  CLOSED_V338
5A JP-identity / KO-dialogue composite    IMPLEMENTED_V339
5A exact mapping                         1,088
5A verification violations               0
1E semantic admission                    NOT IMPLEMENTED
3C                                       KEEP_JP DIRECTION / NOT MATERIALIZED
0x0E partition-593 residual              OPEN
full S4                                  BLOCKED
product/build/package/IPS                NONE
```

Exact next scope after a fresh explicit user execution signal:

`ECF00000_PARTITION593_0E_RESIDUAL_RUNTIME_OVERRUN_ROOT_CAUSE_READ_ONLY`

Bounded READ ONLY only. Determine why the partial selective layout still reaches/decodes the `0x0E` path incorrectly and whether the cause belongs to `1E`, another omitted payload mutation, or independent runtime structure. Do not implement a fix, resume S4, or build/package/IPS in that scope.
