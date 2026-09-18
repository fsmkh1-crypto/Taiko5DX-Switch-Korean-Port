# TAI5MSG 3179 SELECTIVE SERIALIZER IMPLEMENTATION / OFFLINE VALIDATION — V308

Date: 2026-09-18 (KST)
Status: IMPLEMENTATION MATERIALIZED / REPO-METADATA OFFLINE VALIDATION PASS / BYTE-EXACT EXECUTION PENDING
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V308`
Parent: `07ffd6561e087c81145f4ef7b026b0b56d631db7` / V307

## 1. Scope

Authorized scope: `TAI5MSG_3179_SELECTIVE_SERIALIZER_IMPLEMENTATION_OFFLINE_VALIDATION`.

Implemented:

- independent selective serializer module `builder/selective_tai5msg.py`;
- V303 index/shard guards and exact membership checks;
- V304 exact two-row correction guards;
- stock/PC-KO identity guards;
- canonical TAI5MSG parse/decrypt/encrypt primitives;
- zero-replacement byte-identity gate;
- effective selected-payload control/mapping validator;
- V307 growth-only B0..B31 reconstruction;
- V307 B32 preserved-physical-envelope reconstruction;
- independent post-emit reparse and selected/unselected byte comparison;
- current-corpus postcondition checks;
- repository-only metadata preflight;
- unit/regression test source `tests/test_selective_tai5msg.py`.

Not included:

- package integration;
- Mapping/font/ExeFS mutation;
- IPS/build/package;
- Eden/Switch runtime package;
- hardware execution;
- EVENT/SNR/name/yomi/reflow/translation work.

## 2. 확정된 사실

### PC_PATCH_ORACLE_GATE

`PASS`.

Used PC evidence:

- canonical PC Korean TAI5MSG size/SHA: 2,134,366 / `e3b4522a...`;
- V303 exact locator membership;
- V304 exact PC payload defects and replacement bytes;
- V306 effective code/control census;
- V306/V307 storage/block/B32 contracts.

### V303 independent repository replay

All eight V303 JSONL shards were read from canonical GitHub and independently checked against INDEX metadata.

```text
8/8 shard byte sizes     PASS
8/8 shard SHA-256        PASS
8/8 shard row counts     PASS
rows                     3,179
unique locators          3,179
unique candidate IDs     3,179
unique classification    3,179
ID continuity            PASS
row ordering             PASS
INCLUDE_KO/STATIC/RESOLVED PASS
R1                       3,158
R2                          21
191-wait intersection       0
```

### V304 independent repository replay

```text
ROWS.jsonl byte size      PASS
ROWS.jsonl SHA-256        PASS
row count                 2
B19:M058 source/target lengths PASS
B30:M058 source/target lengths PASS
exact FB byte             PASS
following 05 05 05        PASS
exact one-byte deletion   PASS
```

### Structure-length offline replay

Using the canonical ART-00000005 per-message original/Korean length lattice, exact V303 membership and V304 deltas:

```text
B0 selected               2
B17..B32 selected         3,177
total selected            3,179

growth:
B17 +0x0340
B19 +0x0A80
B20 +0x06C0
B21 +0x01C0
B22 +0x4340
B23 +0x0FC0
B24 +0x0E40
TOTAL +0x7780

B32 used-end              0xB8D5
B32 offset                0x1B4F00
B32 declared              0xCA80
B32 physical              0xCA49
B32 filler                0x1174
B32 omitted               0x37

final physical size       0x1C1949 / 1,841,481
largest declared block    0x12B00
```

This independently reproduces V306/V307 arithmetic without using the expected growth/final-size values to drive layout.

## 3. 유력한 가설

The implemented algorithm should reproduce the V306 analytical diagnostic SHA
`dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9`
when executed against the exact canonical stock/PC-KO binary inputs and Mapping 10,036 code set.

This remains a hypothesis until the new Python module itself is executed byte-for-byte against those binaries.

## 4. 미확정 사항

The current session could not execute Python/container-backed byte replay after the 170,498,865-byte PC patch ZIP was mounted into the conversation runtime: container/Python startup repeatedly failed with transport timeout before user code executed.

Therefore the following are NOT claimed:

```text
new module Python syntax/runtime execution    NOT PERFORMED
zero-replacement test through new module      NOT PERFORMED
actual 3,179 binary serialization             NOT PERFORMED
new module output SHA == V306 diagnostic SHA  NOT PERFORMED
unit-test runner result                       NOT PERFORMED
release artifact                              NOT CREATED
```

The limitation is execution-environment transport, not a discovered TAI5MSG format failure.

## 5. 기각된 가설

Still rejected by implementation:

- shrink every block to `align_up(used,0x40)`;
- shrink B32 physical EOF to effective used-end;
- start from all-PC-KO and restore exclusions;
- silently skip invalid rows;
- generalized FB05 repair;
- use expected `+0x7780`/`0x1C1949` as layout inputs;
- make legacy V288 `builder/tai5msg.py` the selective policy engine;
- couple pure TAI5MSG serialization to package/ExeFS/font mutation.

No new binary hypothesis was introduced to bypass the blocked execution.

## 6. 관련 영향 범위

Repository implementation surface is intentionally isolated:

```text
builder/selective_tai5msg.py
tests/test_selective_tai5msg.py
```

Historical `builder/tai5msg.py` is unchanged.

V303/V304/V306/V307 artifacts are unchanged.

No gameplay binary/output is committed.

## 7. 수정 제안 / next scope

Do not advance to package integration yet.

Next bounded scope after a fresh explicit signal:

`TAI5MSG_3179_SELECTIVE_SERIALIZER_BYTE_EXACT_OFFLINE_REPLAY`

Goal:

1. run the new module against exact canonical stock TAI5MSG and extracted PC-KO TAI5MSG;
2. supply the canonical Mapping 10,036 code set;
3. run zero-replacement identity;
4. run the 3,179 effective reconstruction;
5. run unit/regression tests;
6. require exact V306 postconditions and diagnostic SHA;
7. report and STOP.

Only after that replay passes may package/build integration be proposed.

## 8. Repository write boundary

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
