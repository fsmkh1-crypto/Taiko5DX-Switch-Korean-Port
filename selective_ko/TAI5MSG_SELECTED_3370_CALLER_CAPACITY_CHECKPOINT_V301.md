# TAI5MSG SELECTED 3370 CALLER / CAPACITY CHECKPOINT — V301

Date: 2026-09-18 (KST)
Status: CANONICAL READ-ONLY ANALYSIS CHECKPOINT / NO CANDIDATE / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V301`
Parent: `bec39bce36e5b267bee8018d5ee89f2ef93c45fe` / V300

## 1. Purpose

This checkpoint canonicalizes the read-only TAI5MSG work performed after V300.

It records:
- PC-JP / PC-KO / Switch TAI5MSG source identities and locator binding;
- the conservative selected source floor;
- Switch owner binding;
- TAI5MSG internal caller/composition closure;
- external caller-family closure;
- block-envelope / growth partition;
- unresolved evidence waits;
- the next read-only cause-family.

It issues no candidate IDs, classification IDs, builder change, game-byte write, IPS, build, or runtime artifact.

## 2. TAI5MSG source and structure authority

Inherited verified structure:

```text
blocks                  33
logical message slots   14,832
slot cardinality        1:1
insert/delete/reorder   0
locator determinism     PASS
```

PC original TAI5MSG:

```text
size     1,810,889
SHA-256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f
```

PC Korean TAI5MSG extracted directly from the patch payload without executing the patcher:

```text
size     2,134,366
SHA-256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
```

Switch v1.1.3 TAI5MSG had already been historically VERIFIED as byte-identical to the PC original TAI5MSG. This checkpoint reuses that established fact; it does not reopen it merely because the work resumed in another session.

Therefore `(block_index, local_message_index)` is the exact PC-JP -> Switch owner binding coordinate for this source family.

The global Switch RomFS bundle is still not treated as fully supplied. Only the TAI5MSG original identity is separately recorded as historically verified.

## 3. Conservative selected source floor

```text
R1 UI_DESCRIPTION        3,347
R2 NARRATION_SYSTEM         23
-----------------------------
selected total           3,370
```

These 3,370 rows are a conservative selected floor, not a claim that every other TAI5MSG message is permanently excluded.

Every selected row has:

```text
valid TAI5MSG locator          3,370 / 3,370
unique Switch logical owner    3,370 / 3,370
owner collisions               0
Korean-bearing PC payload      3,370 / 3,370
```

## 4. TAI5MSG internal composition closure

The full TAI5MSG C/J control-edge graph was audited.

```text
all TAI5MSG C/J edges                       11,845
selected rows with outgoing C/J edge             0
selected rows with incoming C/J edge             0
selected rows with semantic 0x02 insertion       0
```

The Switch top-level TAI5MSG interpreter/getter resets the output cursor/buffer on each top-level call. Consecutive top-level message fetches therefore do not implicitly append to one another.

For all 3,370 selected rows:

```text
mechanism_class            STATIC_COMPLETE
append_after               NO
cross_message_consumers    []
CROSS_MESSAGE_COMPOSITION  absent
```

subject to external caller-family closure below.

## 5. External caller-family closure

```text
R1 caller-resolved   3,158 / 3,347
R2 caller-resolved      21 /    23
----------------------------------
total                 3,179 / 3,370
```

Resolved large families include B22 item/place/trade descriptions, major biography helpers, B17-B20 minigame/help consumers, B24 help consumers, substantial B23 description ranges, B21 direct system/progression consumers, and B0 selected system messages.

Observed consumption is standalone message display or splitting one physical message by its own newline into separate UI fields. That is not cross-message composition.

## 6. External caller evidence waits

Exactly 191 selected rows remain external-caller evidence waits.

```text
R1 caller wait  189
R2 caller wait    2
-------------------
total            191
```

Exact wait composition:

```text
B23:0..93       94
B23:616          1
B21:44..58      15
B32 extras       79
B21:39..40       2
------------------
total           191
```

These rows are not rejected. They already have exact Switch owner, no incoming/outgoing C/J, no semantic 0x02 insert, no TAI5MSG-internal append, and complete source-side messages. Their remaining blocker is external all-caller provenance only.

Do not promote them by adjacency, table proximity, or similarity to neighboring resolved rows.

## 7. Block reconstruction / capacity state

TAI5MSG uses variable-length messages inside blocks with an offset table. Per-message original byte length is not fixed in-place capacity.

```text
current Switch block envelope fit   1,254
block growth required               2,116
-----------------------------------------
selected total                      3,370
```

Usage partition:

```text
current-envelope fit
  R1  1,252
  R2      2

growth-required
  R1  2,095
  R2     21
```

Growth blocks:

```text
B17  +0x0340     832
B19  +0x0A80   2,688
B20  +0x06C0   1,728
B21  +0x0400   1,024
B22  +0x4340  17,216
B23  +0x1280   4,736
B24  +0x0E40   3,648
--------------------
TOTAL +0x7C80  31,872 bytes
```

The selected reconstructed size of each growth-required block does not exceed the corresponding block size already demonstrated by the PC Korean TAI5MSG format. That proves data-format feasibility, not Switch runtime acceptance.

## 8. Combined caller / capacity partition

```text
caller RESOLVED + current block envelope fit    1,175
caller RESOLVED + block-growth gate             2,004
external caller evidence wait                     191
-----------------------------------------------------
selected total                                   3,370
```

The 2,004 rows share one dominant remaining structural cause-family: Switch runtime acceptance of rebuilt/grown TAI5MSG blocks.

The 191 caller waits remain a separate cause-family.

## 9. Claim boundary

```text
source selected                 != INCLUDE_KO
exact owner                     != all-callers resolved
all-callers resolved            != block-growth runtime PASS
PC Korean block format feasible != Switch runtime acceptance
checkpoint                      != builder/build/gameplay PASS
```

Current release corpus remains:

```text
candidate IDs         139
classification IDs    139
INCLUDE_KO rows       139
```

V301 TAI5MSG candidate IDs issued: 0.

## 10. Other evidence waits unchanged

Inline waits remain `R2884` and `R2885`. They are outside the TAI5MSG selected population.

V288 grammar125 remains a separate grammar/formatter cause-family.

## 11. Rejected shortcuts

Do not:
1. treat TAI5MSG as dialogue-only;
2. treat all 13,590 Korean-bearing messages as release candidates;
3. infer usage from length/Korean density;
4. use per-message original length as fixed TAI5MSG capacity;
5. treat top-level getter calls as implicit append;
6. treat newline splitting of one message as cross-message composition;
7. promote the 191 caller waits by neighboring-range similarity;
8. import the full PC Korean TAI5MSG wholesale;
9. treat PC block-format feasibility as Switch runtime growth acceptance.

## 12. Next scope

After a fresh explicit user signal:

`TAI5MSG_SELECTED_BLOCK_GROWTH_RUNTIME_ACCEPTANCE_READ_ONLY`

Scope is limited to:

```text
B17 B19 B20 B21 B22 B23 B24
```

Questions:
- loader/parser use of changed block offsets/sizes;
- relocation of following blocks after regenerated offsets;
- absolute physical-offset dependencies;
- 0x40 alignment and any additional invariant;
- EOF/final-block assumptions;
- whether the 2,004 caller-resolved growth rows receive a safe structural realization.

Do not mix the 191 caller waits into that cause-family.

After reporting that read-only analysis, require a new explicit signal before materialization or implementation.

## 13. Repository write boundary

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
