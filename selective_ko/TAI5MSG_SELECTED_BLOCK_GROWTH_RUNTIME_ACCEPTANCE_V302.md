# TAI5MSG SELECTED BLOCK GROWTH RUNTIME ACCEPTANCE — V302

Date: 2026-09-18 (KST)
Status: CANONICAL READ-ONLY RUNTIME-STRUCTURE ACCEPTANCE CLOSURE / NO CANDIDATE / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V302`
Parent: `7940685f56d51ad1cc260d66e5c7d01a69ae861d` / V301 state

## 1. Purpose

This checkpoint closes only the V301 cause-family:

`TAI5MSG_SELECTED_BLOCK_GROWTH_RUNTIME_ACCEPTANCE_READ_ONLY`

Scope is limited to selected-message block growth in:

`B17 B19 B20 B21 B22 B23 B24`

It does not analyze the 191 external-caller evidence waits, R2884/R2885, EVENT/TS5, SNR, builder implementation, IPS generation, translation changes, or hardware gameplay execution.

## 2. Direct Switch runtime authority

Actual Nintendo Switch v1.1.3 `main` used for this analysis:

```text
size    5,287,359
SHA256  b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b
NSO     NSO0
```

The canonical TAI5MSG loader is the Switch AArch64 function at `0x43F518`.

Relevant verified behavior:

```text
0x43F560  destination = object + 0x8
0x43F564  copy length = 0x108
0x43F56C  copy 0x108 bytes from loaded resource
```

`0x108 = 33 * 8`, therefore the runtime copies the complete 33-entry `<block_offset, block_size>` pair table.

The loader then loops exactly 33 times:

```text
0x43F580  block_index++
0x43F584  compare block_index with 0x21
0x43F588  exit after 33 blocks
```

Per block:

```text
0x43F594  read block_size from copied header pair
0x43F598  compare block_size with 0x20000
0x43F5B0  read block_offset from copied header pair
0x43F5B4  source = file_base + block_offset
0x43F5B8  copy block_size bytes to that block's runtime buffer
0x43F5E4..0x43F634
          decrypt copied bytes by adding 0x5B
```

Therefore the Switch TAI5MSG load path uses regenerated header offsets and sizes directly. It does not calculate later block positions from original JP physical locations.

## 3. Runtime block capacity

Allocator `0x43F354` allocates one `0x20000`-byte buffer for each of the 33 blocks.

Observed allocation span:

```text
object + 0x748
...
object + 0x848

33 pointers * 8 bytes
each allocation size = 0x20000 = 131,072 bytes
```

The loader compares every declared block size against `0x20000` before copying. The path emits its diagnostic/assert path when the declared size exceeds this value; the physical buffers are also exactly `0x20000`.

For the seven V301 growth blocks:

```text
block  JP size  V301 growth  selected rebuilt size  runtime buffer
B17    0xDAC0   +0x0340      0xDE00                 0x20000
B19    0xEB80   +0x0A80      0xF600                 0x20000
B20    0xD6C0   +0x06C0      0xDD80                 0x20000
B21    0xC500   +0x0400      0xC900                 0x20000
B22    0xE7C0   +0x4340      0x12B00                0x20000
B23    0x10F00  +0x1280      0x12180                0x20000
B24    0xE400   +0x0E40      0xF240                 0x20000
```

All seven fit.

Largest rebuilt block:

```text
B22 selected size = 0x12B00 = 76,544
buffer             = 0x20000 = 131,072
remaining          = 0x0D500 = 54,528
```

Thus the V301 growth requirement is not close to the runtime block-buffer ceiling.

## 4. Following-block relocation

Because `0x43F5B0/0x43F5B4` reads each block's current header offset and forms `file_base + offset`, growth of an earlier block does not require preserving any original later-block file offset.

Required cumulative relocation for a selective rebuild is deterministic:

```text
B18/B19 offset shift  +0x0340
B20 offset shift      +0x0DC0
B21 offset shift      +0x1480
B22 offset shift      +0x1880
B23 offset shift      +0x5BC0
B24 offset shift      +0x6E40
B25..B32 shift        +0x7C80
```

Total selected growth remains:

`+0x7C80 = 31,872 bytes`

No absolute JP physical-file offset dependency was found on the canonical TAI5MSG load/get path.

## 5. Message offset table regeneration

The canonical top-level message getter at `0x43F2A4` derives block/local message coordinates from the numeric message ID.

It loads the selected block runtime-buffer pointer, reads the block's `u16` message count, then reads the selected `u32` message offset from:

`block_buffer + 0x02 + local_message_index * 4`

Relevant instructions include:

```text
0x43F2DC  load selected block buffer
0x43F2EC  copy/read 2-byte message_count
0x43F304  reload selected block buffer
0x43F308  local_index * 4
0x43F310  + 0x02 table base
0x43F318  copy/read 4-byte message_offset
```

Therefore message starts are data-driven by the block-local offset table at runtime. Original JP message physical positions are not embedded in this getter.

Disposition:

```text
regenerated message offset table  ACCEPTED BY RUNTIME STRUCTURE
variable message byte lengths     ACCEPTED WITHIN BLOCK CAPACITY
original per-message position     NOT REQUIRED
```

## 6. Alignment

All canonical PC original JP/SC/TW block offsets and declared sizes inspected in this analysis are `0x40` aligned. The canonical PC Korean TAI5MSG format already demonstrates the same format family.

However the Switch TAI5MSG loader at `0x43F518` does not perform a modulo/`0x40` alignment test before consuming a pair. Its direct runtime checks relevant here are pair-driven offset/size access and the `0x20000` size ceiling.

Therefore:

```text
0x40 alignment = canonical format invariant to preserve
0x40 alignment = not proven to be a loader-enforced runtime condition
additional alignment requirement = not found on canonical loader/getter path
```

A future serializer should preserve `0x40` alignment because all canonical source files use it and there is no reason to weaken the format invariant.

## 7. Final block / EOF

The inherited ART-00000005 structure evidence remains binding:

```text
JP B32 declared minus physical = 55 bytes
PC Korean B32 declared minus physical = 34 bytes
```

Read-only PC-original cross-language corroboration performed during V302 also showed:

```text
SC size    1,918,773
SC SHA256  04ff8afe290b12f2f7b93e174952f5c7550acff1ef0fe17b96d889170e0a706e
SC B32 declared minus physical = 11 bytes

TW size    1,944,333
TW SHA256  bf165a3f30b72045ea5f92e5acca45a950be4d94294cc10e82576f3fffcb0294
TW B32 declared minus physical = 51 bytes
```

SC/TW are corroborative PC-original format evidence only; they are not promoted to Switch RomFS identity authority.

For the selective JP rebuild, only blocks before B32 grow. If B32 payload/declared size are preserved and the file grows by the same cumulative `0x7C80`, the JP relation remains:

```text
new B32 offset              = old B32 offset + 0x7C80
new file size               = old file size + 0x7C80
B32 physical bytes          = unchanged
B32 declared-minus-physical = unchanged 55 bytes
```

Thus the existing JP final-block EOF relation is preservable without inventing new EOF padding.

The internal generic-resource allocation behavior that tolerates the canonical final declared/physical gap was not separately reverse-engineered in this scope because the selective realization can preserve the already-working JP relation exactly.

## 8. 확정된 사실

1. Switch loader copies and consumes all 33 header `<offset,size>` pairs.
2. Every block is loaded using the current header offset and current header size.
3. Following blocks may move when preceding blocks grow; the canonical loader does not require original JP physical offsets.
4. Each block has a dedicated `0x20000` runtime buffer.
5. All seven selected rebuilt block sizes remain below `0x20000`.
6. The runtime message getter reads block-local `u32` message offsets from the data table, so regenerated message-offset tables are structurally accepted.
7. The seven-block selected growth total is `0x7C80`.
8. The JP B32 final-block declared/physical relation can be preserved exactly after that relocation.
9. No runtime patch is required merely to make the seven block growths addressable by the canonical TAI5MSG loader/getter.

## 9. 유력한 가설

The lower generic resource loader likely provides allocation/alignment behavior sufficient for the canonical B32 declared/physical EOF gap. This is strongly implied by the stock JP runtime behavior but its exact lower-level allocation implementation is not needed for the selective growth realization because the stock JP 55-byte relation can be preserved exactly.

## 10. 미확정 사항

- selective rebuilt TAI5MSG has not yet been executed on hardware;
- this V302 closure does not validate rendering/layout/translation quality;
- the exact lower generic-resource implementation behind final EOF padding tolerance was not separately closed;
- the 191 external-caller evidence waits remain untouched;
- R2884/R2885 remain untouched.

None of these items reopens the seven-block structural runtime-acceptance result.

## 11. 기각된 가설

Rejected for this cause-family:

- TAI5MSG blocks must retain original JP physical file offsets;
- following blocks cannot move after an earlier block grows;
- messages are addressed by original JP physical message positions;
- each message is limited to its original in-place byte envelope;
- selected growth requires a Switch runtime hook/patch;
- V290/V291 build/package evidence may be used as hardware-execution proof.

V291 remains package/transport evidence only. It did not perform hardware execution.

A transient numerical lead involving an unrelated `0x140` allocation was also rejected during analysis after its owner path was shown to belong to another resource/object family. It is not TAI5MSG evidence.

## 12. 관련 영향 범위

V301 partition remains:

```text
caller RESOLVED + current envelope fit  1,175
caller RESOLVED + block-growth gate     2,004
external caller evidence wait             191
--------------------------------------------
selected total                           3,370
```

V302 closes the structural block-growth gate for the 2,004 caller-resolved rows.

This does not automatically issue `INCLUDE_KO`, `WRITE_SAFE`, candidate IDs, or classification IDs.

Therefore the caller-resolved population eligible for the next release-admission audit becomes:

```text
1,175 current-fit
2,004 growth-gate structurally cleared
--------------------------------------
3,179 caller-resolved rows
```

The 191 caller waits remain a separate cause-family.

## 13. 수정 제안

When implementation is separately authorized later, use a Switch-structure-first selective serializer:

```text
Switch-original TAI5MSG structure
-> replace only selected Korean payloads
-> regenerate affected block message-offset tables
-> grow B17/B19/B20/B21/B22/B23/B24 by required 0x40 units
-> regenerate all 33 header offset/size pairs
-> relocate following blocks by cumulative growth
-> preserve canonical per-block encryption/storage form
-> preserve B32 EOF omission relationship
```

Do not import the complete PC Korean TAI5MSG wholesale.

No serializer/builder implementation is authorized by V302 itself.

## 14. Next scope / STOP

After a fresh explicit user signal:

`TAI5MSG_CALLER_RESOLVED_3179_RELEASE_ADMISSION_READ_ONLY`

Scope population:

```text
R1 caller-resolved  3,158
R2 caller-resolved     21
total                3,179
```

Purpose:

- reuse V301 source-role/mechanism/caller closure without re-tracing it;
- reuse V302 capacity/growth structural acceptance;
- audit remaining common release gates: provenance, PC occurrence conflict, risk flags, transport requirements, identity policy applicability, and derived disposition;
- identify terminal `INCLUDE_KO`/defer/keep/unresolved results without issuing IDs;
- keep the 191 caller waits outside this scope;
- do not implement builder/serializer/build/IPS.

After that read-only report, require another explicit user signal before candidate/classification materialization or implementation.

## 15. Repository write boundary

Repository mutation for V302 materialization is restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No Contents-API write, branch creation, force update, gameplay-data write, build, or IPS is permitted.
