# TAI5MSG 3179 SELECTIVE BUILDER / SERIALIZER DESIGN — V307

Date: 2026-09-18 (KST)
Status: CANONICAL DESIGN MATERIALIZED / NO IMPLEMENTATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V307`
Parent: `d7674950b0c5ca6e12638b3a2bbe2a25a0f86a0d` / V306

## 1. Purpose

V307 materializes the bounded read-only serializer design for the exact V303+V304 effective TAI5MSG release population after V306 closed GATE-1 through GATE-5.

V307 is design authority only. It does not create or modify serializer code, gameplay data, TAI5MSG release output, IPS, build/package output, or hardware state.

Canonical population remains:

```text
TAI5MSG release rows       3,179
R1                         3,158
R2                            21
external-caller waits        191  EXCLUDED
inline/main release rows     139  SEPARATE CARRIER
global INCLUDE_KO          3,318
```

## 2. Authoritative input stack

A future selective TAI5MSG serializer must consume exactly four authority layers:

```text
A. Switch stock TAI5MSG
   size    1,810,889
   sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f

B. PC Korean v1.02 TAI5MSG
   size    2,134,366
   sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090

C. V303 membership
   exactly 3,179 INCLUDE_KO rows
   SEL-CAND/SEL-CLS-000140..003318

D. V304 correction overlay
   exactly B19:M058 and B30:M058
```

The serializer must not discover new rows, infer product scope, translate content, promote the 191 waits, or consume the whole PC-Korean TAI5MSG as the product baseline.

## 3. Target-lattice construction

The full 14,832-message target lattice must begin from the stock JP lattice.

```text
stock JP 14,832 messages
 -> replace exactly V303 3,179 locators with canonical PC-KO payload
 -> apply exact V304 two-row corrections
 -> validate effective payload
 -> serialize all 14,832 messages
```

Postcondition:

```text
selected effective KO     3,179
unselected byte-exact JP 11,653
total                    14,832
```

The inverse architecture — begin with all PC-Korean messages and restore excluded rows to JP — is rejected.

## 4. V303 manifest integrity contract

Before source resolution, the serializer must fail-closed on V303 artifact integrity.

Required checks include:

```text
row count                  3,179
candidate IDs              contiguous 000140..003318
classification IDs         contiguous 000140..003318
unique locators            3,179
INCLUDE_KO                 3,179
STATIC_COMPLETE            3,179
RESOLVED                   3,179
R1                         3,158
R2                            21
intersection with wait set     0
```

Each V303 row shard must match the exact size and SHA-256 recorded in the V303 INDEX. Any shard, row, ID, locator, disposition, mechanism or count mismatch aborts.

## 5. V304 exact correction overlay

V304 is not a generalized repair algorithm.

For each of the two authorized rows, the implementation contract is:

```text
resolve exact V303 locator
 -> require canonical PC-KO file identity
 -> require exact V304 source message length/hash
 -> require FB at exact recorded offset
 -> require following 05 05 05
 -> delete exactly that one FB
 -> require exact corrected target length/hash
```

No other `FB05` occurrence may be automatically modified.

## 6. Block reconstruction policy

### 6.1 B0 through B31 — growth-only envelope

For every non-final block:

```text
used = 2 + 4 * message_count + sum(effective message lengths)

required = align_up(used, 0x40)

declared = max(stock_declared, required)
physical = declared
```

This is a growth-only envelope policy: a block may grow when required but must not shrink below its stock declared extent merely because selected Korean payload becomes shorter.

Canonical growth blocks and effective declared growth:

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

Representative shrink-risk blocks:

```text
B18 stock 0xB1C0 / effective used 0xAED0 / naive align 0xAF00 / keep 0xB1C0
B28 stock 0xA080 / effective used 0x9A23 / naive align 0x9A40 / keep 0xA080
B29 stock 0xA480 / effective used 0x9D6C / naive align 0x9D80 / keep 0xA480
B30 stock 0xA540 / effective used 0x9E09 / naive align 0x9E40 / keep 0xA540
B31 stock 0xA5C0 / effective used 0x9DD1 / naive align 0x9E00 / keep 0xA5C0
```

A serializer that applies `declared = align_up(used,0x40)` to every block produces the wrong aggregate growth `+0x58C0` instead of the canonical effective `+0x7780`. That shrink strategy is rejected.

### 6.2 B32 — preserved physical envelope plus omitted tail

B32 is special and must not use the B0..B31 physical rule.

Binding current corpus state:

```text
effective used-end       0xB8D5
physical extent          0xCA49
declared size            0xCA80
physical filler          0x1174 / 4,468 bytes
omitted tail             0x37 / 55 bytes
```

Serializer contract:

- preserve declared `0xCA80` for this corpus;
- preserve physical extent `0xCA49`;
- require effective used-end <= physical extent;
- fill the physical slack deterministically;
- do not emit the final 55-byte declared-minus-physical tail.

Canonical filler is decrypted `0x5B`, encrypted/on-disk `0x00`.

Do not generalize stock zero-replacement `physical EOF == used-end` into the shrinking effective release.

## 7. Header reconstruction policy

The first block offset remains `0x140`.

For block i > 0:

```text
block[i].offset =
block[i-1].offset + block[i-1].declared_size
```

A future serializer should copy the canonical stock `0x000..0x13F` header region, rewrite only the 33 `<u32 offset,u32 declared_size>` pairs required by the rebuilt layout, and preserve stock spare/header bytes `0x108..0x13F` unchanged.

Expected current-corpus B32 offset is `0x1B4F00`, but this is a postcondition, not an input constant.

## 8. Message-table reconstruction

For each block plaintext:

```text
u16 message_count
u32 offsets[message_count]
message payloads
canonical filler
```

Offset algorithm:

```text
cursor = 2 + 4 * message_count

for message in logical order:
    offsets.append(cursor)
    cursor += len(message)
```

Fail-closed checks:

- message count unchanged for every block;
- first offset equals table end;
- offsets strictly increase;
- no overlap;
- all message ends fit the applicable physical contract;
- every offset fits u32;
- every declared block size <= runtime `0x20000` buffer.

Current largest rebuilt block is B22 `0x12B00`.

## 9. Storage transform

Reuse the verified TAI5MSG primitive only:

```text
decrypt byte = (raw + 0x5B) & 0xFF
encrypt byte = (plain - 0x5B) & 0xFF
```

No block-index, file-offset, block-size or rolling state is part of the canonical transform.

The zero-replacement identity test remains a mandatory implementation regression gate:

```text
canonical stock
 -> parse/decrypt
 -> zero replacements
 -> rebuild/encrypt
 -> exact byte-identical canonical stock
```

Any failure aborts before Korean payload realization.

## 10. Effective payload validation order

Required processing order:

```text
validate V303 authority
 -> resolve canonical PC-KO source payloads
 -> apply exact V304 overlay
 -> run GATE-3 tokenizer/code validation
 -> construct target lattice
 -> serialize
```

Before serialization, require:

```text
invalid lead/trail        0
unknown tokens            0
unmapped game codes       0
semantic 0x02 insertions  0
```

Only B32:M242 may carry the canonical final-message `...05 05 05 00` structural terminator. Do not generalize arbitrary `00` as a valid token.

## 11. Independent post-emit reparse

After emission, parse the emitted bytes again from the beginning rather than trusting writer state.

Required postconditions:

```text
blocks                         33
messages                   14,832
selected target matches      3,179
unselected JP exact matches 11,653
overlaps                         0
out-of-bounds                    0
```

Recompute from the emitted layout and then require the current-corpus expected postconditions:

```text
growth       +0x7780
file size    0x1C1949 / 1,841,481
B32 offset   0x1B4F00
B32 declared 0xCA80
B32 physical 0xCA49
B32 omitted  0x37
```

These values must never be used to drive the layout calculation.

V306 analytical SHA-256
`dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9`
may be used only as a development regression oracle until an actual implementation/output is separately validated and materialized. It is not yet a release artifact identity.

## 12. Mapping/font responsibility boundary

The pure TAI5MSG serializer must not patch Switch `main`, Mapping, page-mapper code or font assets.

The serializer should emit an effective-code-usage report sufficient for package integration.

Package integration separately requires:

- deployed Mapping 10,036 realization;
- deployed `EB..F8 -> pages 49..62` page mapper;
- Korean font SHA-256 `c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932`;
- proof that the serializer's effective 992 Hangul game codes are a subset of deployed capability.

W0/W1 compact A1..DF width changes are not required by this TAI5MSG population.

## 13. Legacy builder separation

Existing `builder/tai5msg.py` remains legacy/reference code for the historical V288/V289/V290 full-port/grammar125 path.

Potentially reusable primitives:

- `+0x5B/-0x5B` storage transform;
- 33-pair header parsing concept;
- u16 count + u32 offset parsing;
- basic block/message decomposition.

Do not carry forward:

- V288 grammar125 manifest dependency;
- whole-PC-Korean-TAI5MSG product baseline;
- fixed-size-only block reconstruction;
- compact-Korean mutation;
- historical V288/V289 output-hash assumptions.

The selective serializer should be a separate module rather than an in-place semantic expansion of the legacy routine.

Suggested implementation path: `builder/selective_tai5msg.py`.

## 14. Fail-closed error classes

A future implementation should distinguish at least:

```text
STOCK_IDENTITY_MISMATCH
PC_KO_IDENTITY_MISMATCH
V303_INDEX_OR_SHARD_INTEGRITY_FAIL
V303_MEMBERSHIP_FAIL
V303_DUPLICATE_LOCATOR
V304_INDEX_OR_ROWS_INTEGRITY_FAIL
V304_SOURCE_GUARD_FAIL
V304_TARGET_GUARD_FAIL
LOCATOR_OUT_OF_RANGE
CONTROL_TOKEN_VALIDATION_FAIL
MAPPING_DOMAIN_MISS
BLOCK_RUNTIME_CAPACITY_FAIL
B32_PHYSICAL_CONTRACT_FAIL
POST_REPARSE_COUNT_FAIL
POST_OFFSET_FAIL
POST_SELECTED_PAYLOAD_FAIL
POST_UNSELECTED_JP_MUTATION
OUTPUT_GROWTH_POSTCONDITION_FAIL
OUTPUT_SIZE_POSTCONDITION_FAIL
```

Failure must be transactional: construct in memory or temporary storage, complete all validation, and publish a final artifact only after every guard passes. A partially validated release file must not be published.

## 15. Rejected implementation shortcuts

Rejected:

- shrink every block to `align_up(used,0x40)`;
- shrink B32 EOF to effective used-end;
- begin from full PC-Korean lattice and restore exclusions;
- extend legacy V288 `builder/tai5msg.py` as the selective product policy engine;
- let the serializer choose translations or new membership;
- auto-repair malformed source beyond exact V304 authority;
- silently skip a row after a validation failure;
- couple pure TAI5MSG serialization to all ExeFS/font writes;
- use V306 output size/growth/hash as layout-driving constants.

## 16. Implementation boundary and next scope

V307 creates no implementation authority by itself.

After a fresh explicit user signal, the next bounded scope is:

`TAI5MSG_3179_SELECTIVE_SERIALIZER_IMPLEMENTATION_OFFLINE_VALIDATION`

That scope may create the independent selective serializer and offline regression tests for V303+V304+V306+V307 contracts.

It must still exclude:

- package integration;
- full selective builder integration beyond the TAI5MSG module;
- IPS generation;
- Eden/Switch runtime package;
- hardware execution;
- unrelated EVENT/SNR/name/yomi/reflow/translation work.

After implementation/offline-validation reporting, a further explicit user signal is required before build/package or repository materialization beyond that authorized implementation scope.

## 17. Repository write boundary

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
