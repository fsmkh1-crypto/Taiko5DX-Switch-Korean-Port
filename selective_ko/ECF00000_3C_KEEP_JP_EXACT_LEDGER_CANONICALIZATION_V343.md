# ECF00000 0x3C KEEP_JP exact ledger canonicalization — V343

Date: 2026-09-20 (KST)

```text
validation_id   V343
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      LEDGER_MATERIALIZATION_AND_REPLAY_VALIDATION
parent          e275f8ff457f14aee12fc9df31acdd2fee085eca / V342
scope           ECF00000_3C_KEEP_JP_EXACT_LEDGER_CANONICALIZATION
product_bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

V343 materializes the exact `0x3C` family disposition established by the preceding READ ONLY audit. It does not apply any PC-KO `0x3C` mutation and does not resume S4.

## 1. Exact inputs

```text
stock ECF00000.TS5
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09

PC-KO ECF00000.TS5
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe

V342 diagnostic
size    1,081,652
sha256  e1f251cb6614fd79bd0e5add752b23460d4e70af5ad52325abbfd4421195569b
```

## 2. Exact mapping

Original and PC-KO editor-grouped `0x3C` objects map partition-locally by `0x3C` ordinal:

```text
original 3C rows           101
PC-KO 3C rows              101
partitions containing 3C    73
partition count mismatch     0
header mismatch              0
changed                    100
byte-identical               1
```

Exact original/KO offsets, lengths, payload hashes, runtime-length observations and dispositions are persisted in the V343 ledger.

## 3. Runtime/semantic disposition

The family is not homogeneous.

```text
KEEP_JP_IDENTITY             100
PRESERVE_STRUCTURAL_ALIAS      1
--------------------------------
TOTAL                         101
mutation allowed                0
```

### 3.1 Normal rename objects — 100

The 100 normal rows are four-field rename/identity records:

```text
surname / family-name field
personal-name field
surname reading
personal-name reading
```

For all 100 rows:

```text
Switch runtime consumed length == editor grouped-object length   original PASS
Switch runtime consumed length == editor grouped-object length   PC-KO PASS
```

PC-KO changes these identity fields. Current selective policy keeps dedicated identity presentation in Japanese, therefore all 100 rows are `KEEP_JP_IDENTITY`.

### 3.2 Embedded structural alias — 1

The exceptional row is:

```text
partition          283
ordinal            0
original offset    0x7BFEC
PC-KO offset       0x9B038
editor length      36
runtime 3C length  20
PC-KO changed      NO
MAY-reachable      NO
```

Its original offset is `EVENT 0x38 @ 0x7BFE8 + 4`. The byte value `0x3C` is therefore inside another runtime command rather than a normal standalone rename command. PC-editor grouping over-groups this region as a `0x3C` text object.

Disposition:

`PRESERVE_STRUCTURAL_ALIAS`

This row is a direct counterexample to treating PC-editor text grouping as runtime ownership authority.

## 4. MAY-reachable cross-check

```text
all editor-grouped 3C         101
MAY-reachable                   87
non-MAY                         14
```

The 87 MAY-reachable rows are all within the 100 normal rename rows. The 14 non-MAY rows consist of 13 normal identity rows plus the single embedded structural alias.

Reachability does not alter product disposition because all 101 rows remain original.

## 5. V342 current-state check

Replaying all 101 rows against the V342 diagnostic by partition-local `0x3C` ordinal confirms:

```text
mapping rows checked            101 / 101
original binding mismatch         0
PC-KO binding mismatch            0
payload SHA mismatch              0
V342 current 3C mutation          0
current editor-grouped 3C count 101
```

Therefore V342 already satisfies the final V343 `0x3C` policy without a serializer mutation step.

If all 100 changed PC-KO rename objects were copied, aggregate `0x3C` growth would be `+1,012` bytes. V343 authorizes none of that growth.

## 6. Canonical artifact

Repository artifact directory:

`selective_ko/artifacts/ecf00000_v343_3c_keep_jp_v1/`

Compact ledger:

```text
file         LEDGER_COMPACT.bin
records      101
record size   18 bytes
size        1,818 bytes
serialization
<HHIIHHBB
  partition:u16
  ordinal:u16
  original_offset:u32
  ko_offset:u32
  original_length:u16
  ko_length:u16
  disposition:u8
  subtype:u8
sha256      4375510e70d24ed008c80db5fc8efcae6582069b69cad88ba6d42e6ab67df1cf
```

Disposition codes:

```text
1 KEEP_JP_IDENTITY
2 PRESERVE_STRUCTURAL_ALIAS
```

Subtype codes:

```text
1 RENAME_FOUR_FIELD
2 EMBEDDED_EVENT38_PLUS4_EDITOR_OVERGROUP
```

A human-readable `LEDGER.jsonl`, MAY-reachable rowset, replay validation, INDEX, and manifest are stored beside the compact ledger.

## 7. Exact rowset gates

Rows serialize for rowset hashing as:

`<HHII = partition:u16 + ordinal:u16 + original_offset:u32 + ko_offset:u32>`

```text
all 101
b360b83de11125d8449bb273cfc13bd018a4ac9b47f07e500b6f3ff2520ab0e2

KEEP_JP_IDENTITY 100
dd95d3aea68e8bcd6587d3b8172c1e61e7b8b347678a44aa621d9db4cdfdf331

PRESERVE_STRUCTURAL_ALIAS 1
9ce0e1d59937059ed600ff957b2c2df96e6b262375a72863977f25ec3664121e

MAY-reachable 87
1af9788706429afd406c7c8b955a7b53749fd571efd345cbd7b3b8951489bea4

non-MAY 14
fa8e913baeccb838b018094fae935038343aabdbf4365d5a37ebfd71e34cd0bd
```

## 8. Replay validation

```text
input identity                         PASS
mapping rows                           101 / 101
partition count mismatch               0
header mismatch                        0
normal runtime/editor length match     100 / 100 original
normal runtime/editor length match     100 / 100 PC-KO
structural alias exact                 PASS
all rowset hashes                      PASS
compact ledger deterministic           PASS
V342 current 3C mutations              0
product bytes changed                  NO
```

## 9. Rejected / do-not-repeat

Reject:

- copy all 101 PC-KO `0x3C` editor objects;
- treat all 101 editor-grouped `0x3C` objects as equivalent standalone runtime rename commands;
- translate only the 87 MAY-reachable rows while changing non-MAY identity rows;
- treat `0x7BFEC` as a normal rename command;
- use final-Korean fresh grouping as runtime ownership authority;
- introduce a dedicated `0x3C` mutation serializer merely because PC-KO changed 100 rows;
- reopen V342 1E/5A/branch results because V343 adds no product mutation.

## 10. Current disposition / next scope

```text
V336 S1 serializer core               CLOSED
V337 generic relocation               CLOSED
V338 special spans                    CLOSED
V339 5A composite                     CLOSED
V340 state-aware residual gate        CLOSED
V341 1E semantic ledger               CLOSED
V342 1E ready-23 implementation        CLOSED
V343 3C KEEP_JP ledger                MATERIALIZED

1E runtime pending                    21
3C product mutation                    0
code-3 fixed particle                  OPEN
full S4                                NOT RESUMED
product/build/package/IPS              NONE
```

Exact next scope after a fresh explicit user signal:

`ECF00000_FIXED_SURFACE_PARTICLE_V1_EXACT_TRANSFORM_RECOVERY_READ_ONLY`

READ ONLY only. Recover the exact PC-patch transformation semantics for the V335 code-3 / 1,226-row `FIXED_SURFACE_PARTICLE_V1` population from real PC-KO/original payloads and runtime/layout evidence. Do not invent a transform, promote the 21 pending `0x1E` rows, resume full S4, build/package/IPS, or run hardware in that scope.
