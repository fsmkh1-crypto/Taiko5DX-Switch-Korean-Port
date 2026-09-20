# ECF00000 0x1E INCLUDE_KO_READY-23 IMPLEMENTATION / OFFLINE VALIDATION — V342

Date: 2026-09-20 (KST)

```text
validation_id   V342
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          3cfa2d0de033361897428e409b1434e424a4019e / V341
scope           ECF00000_1E_INCLUDE_KO_READY_23_IMPLEMENTATION_OFFLINE_VALIDATION
product_bytes   NOT PUBLISHED
build/package   NONE
hardware        NOT RUN
```

V342 implements only the exact 23 `INCLUDE_KO_READY` rows materialized by V341. It does not promote the 21 `INCLUDE_KO_RUNTIME_PENDING` rows and does not resume code-3 particle work or full S4.

## 1. Exact inputs

```text
stock ECF00000.TS5
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09

PC-KO ECF00000.TS5
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe

V341 1E compact ledger
records 461
sha256  4e84b8278e1fe6b13a7945c6ba13a5b2922cb686b79746a510c92fd2ce856b35

V341 INCLUDE_KO_READY rowset
rows    23
sha256  0011c816ae8519750c79b3a1917b830decce3b7f466fe6735212f433859fc38d
```

## 2. Implementation

New module:

`builder/selective_event_1e.py`

SHA-256:

`0e3e9c2b7b562301d69a444f83f886a222740dbde1f3e31da2a75b1620040320`

New tests:

`tests/test_selective_event_1e.py`

SHA-256:

`7a409d7cac003d9202c936f6c2692d5a342c85a5b1a35d3380c19b86f00bb40b`

The module:

- verifies the exact 461-row compact ledger identity and rowset hashes;
- verifies exact stock and PC-KO ECF identities when canonical mode is enabled;
- binds every `0x1E` row by original/KO partition-local ordinal, exact offset, exact length, and unchanged four-byte header;
- writes PC-KO bytes only for disposition `INCLUDE_KO_READY`;
- refuses any pre-existing mutation of `KEEP_JP_IDENTITY`, `PRESERVE_IDENTICAL`, or `INCLUDE_KO_RUNTIME_PENDING` rows;
- verifies the exact 23-row ready rowset, growth, and partition set as postconditions.

Final-Korean fresh grouping is not used as ownership authority.

## 3. Exact 1E application result

```text
ledger rows                         461
INCLUDE_KO_READY                     23
same-length ready                    21
+4-byte ready                         2
net growth                           +8 bytes
ready partitions                      0 / 11 / 72 / 161 / 681

KEEP_JP_IDENTITY untouched          344
PRESERVE_IDENTICAL untouched         73
RUNTIME_PENDING untouched            21
unauthorized 1E mutations             0
```

The two +4 rows remain the V341-proven `室町幕府` and `種子島` rows.

## 4. Regression / unit validation

Repository-level EVENT test families were executed together in the validation environment:

```text
V336/V337/V338 EVENT core tests      16 / 16 PASS
V342 1E tests                         5 / 5  PASS
V339 5A tests                         6 / 6  PASS
V340 residual-gate tests              7 / 7  PASS
------------------------------------------------
total                                34 / 34 PASS
```

The V342-specific five tests cover:

- canonical compact-ledger load;
- corrupted-ledger rejection;
- ready-row PC-KO payload replacement;
- non-ready row original preservation;
- rejection of a pre-existing non-ready mutation.

## 5. V339 baseline reproducibility

Before attributing any output delta to V342, the same integration harness was run without the V342 `0x1E` step.

Result:

```text
size    1,081,644
sha256  9d5821f0cc35356f68d1f243adc644c4be635e62ca4d9154bfe665cb612fd40c
```

This is byte-identical to the canonical V339 diagnostic output.

Therefore the V342 comparison has a clean baseline and does not depend on a different reconstruction path.

## 6. Exact-corpus V342 integration

Partial diagnostic context remains:

```text
V335 code 1 / 2 / 4 replacements
+ V339 5A composite
+ V342 1E ready-23
+ V337 generic relocation
+ V338 Switch special-span repair

V335 code 3 fixed-surface particle remains deferred.
```

Output:

```text
size           1,081,652
growth stock    +149,716
delta vs V339         +8
sha256         e1f251cb6614fd79bd0e5add752b23460d4e70af5ad52325abbfd4421195569b
```

Deterministic rerun is byte-identical.

## 7. Delta containment vs V339

Only five partitions differ from V339:

```text
0 / 11 / 72 / 161 / 681
```

Using the original grouped-item topology as authority, exactly 32 item payloads/headers differ:

```text
1E ready payloads               23
relocation headers               9
other item changes               0
----------------------------------
total                            32
```

The nine relocation-header differences are expected consequences of the two +4 payload growths and exact branch-span preservation. They are not new translation payloads.

## 8. V337 generic relocation gate

```text
generic source plans        7,579
all final encoded spans     PASS
```

Every final generic owner decodes to the current source-item-count span frozen from the original topology.

No generic plan is promoted or removed by V342.

## 9. V338 special-owner gate

All three Switch-only special spans pass after V342:

```text
original owner  final span   final header
0xCBBB0         620          04 01 D8 04
0x65F40         128          04 01 00 01
0x7E1B0         3512         09 F0 77 1B
```

False EVENT-02 expression operands remain nonowners:

```text
0xAC470 / 0x980C0   PASS_2_OF_2
```

## 10. V339 5A gate

V342 does not alter the V339 `0x5A` solution population or hashes:

```text
mapping                         1,088
translated                      1,074
name-only original                 14
ORIGINAL_TARGET                 1,058
CHOICE_NEXT_START                  15
ZERO_NEXT_TERMINATOR                1
modified rows                       82
verification violations              0
```

The modified/dialogue-padding/choice/zero rowset hashes remain exactly V339 canonical.

## 11. V340 differential residual gate

Baseline walker errors remain zero.

The conservative state-aware replay still exposes exactly the one V340 stock-preexisting logical residual:

```text
partition        593
original anchor  0xBDD78
current offset   0xDDD8C
opcode           0x0E
decoded length   0x7F5408
```

`current_offset` moved by the legitimate +8 bytes before partition 593. The V340 logical key excludes current offset, so this remains the same inherited stock residual.

```text
inherited residuals   1
novel residuals       0
blocking              false
```

## 12. Scope boundary

V342 does not authorize or implement:

- the 21 `INCLUDE_KO_RUNTIME_PENDING` `0x1E` rows;
- any `0x3C` PC-KO mutation;
- V335 code-3 `FIXED_SURFACE_PARTICLE_V1`;
- full S4 completion;
- final product ECF output;
- build/package/IPS;
- hardware execution;
- unrelated EVENT files or SNR.

The `e1f251...` TS5 is diagnostic only.

## 13. Rejected / do-not-repeat

Reject:

- implement all 44 semantic `0x1E` candidates merely because the 23 ready rows passed;
- promote the 21 runtime-pending rows without new provenance;
- mutate the 344 identity rows to inherit PC-KO names;
- treat the nine changed branch headers as unauthorized payload expansion;
- use final-Korean fresh grouping to rediscover `0x1E` ownership;
- interpret the moved V340 residual offset as a novel residual;
- claim V342 completes S4.

## 14. Current disposition / next scope

```text
V336 S1 serializer core               CLOSED
V337 generic relocation               CLOSED
V338 special spans                    CLOSED
V339 5A composite                     CLOSED
V340 state-aware residual gate        CLOSED
V341 1E semantic ledger               CLOSED
V342 1E ready-23 implementation        IMPLEMENTED / OFFLINE PASS

1E runtime pending                    21
3C                                     KEEP_JP / not materialized
code-3 fixed particle                  OPEN
full S4                                NOT RESUMED
product/build/package/IPS              NONE
```

Exact next scope after a fresh explicit user signal:

`ECF00000_3C_KEEP_JP_EXACT_LEDGER_MATERIALIZATION_READ_ONLY`

READ ONLY only. Materialize the exact `0x3C` family and prove the KEEP_JP disposition against original/PC-KO mapping. Do not mutate `0x3C`, promote the 21 pending `0x1E` rows, implement code-3 particles, resume full S4, build/package/IPS, or run hardware in that scope.
