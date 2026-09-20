# ECF00000 FIXED_SURFACE_PARTICLE_V1 preimplementation closure — V344

Date: 2026-09-20 (KST)

```text
validation_id   V344
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      PREIMPLEMENTATION_LEDGER_AND_VALIDATOR_GATE
parent          7386d4168aad0ac85f27ecf16b97d1af5a6bf9cd / V343
product_bytes   UNCHANGED
particle_impl   NOT IMPLEMENTED
build/package   NONE
hardware        NOT RUN
```

V344 closes two prerequisites for future EVENT fixed-particle implementation:

1. materialize the exact `FIXED_SURFACE_PARTICLE_V1` applicability axis independently from the V335 single semantic-detail code;
2. replace the V340 one-baseline-residual-only gate with an exact source-proven embedded-alias gate that can distinguish layout-exposed command-looking bytes from genuinely novel runtime residuals.

No particle serializer or product TS5 is produced by V344.

## 1. Exact particle mapping

Canonical surface mapping remains:

```text
은(는) -> 는
이(가) -> 가
을(를) -> 를
과(와) -> 와
와(과) -> 와
(으)로 -> 로
```

Every approved literal is six encoded payload bytes and every fixed surface is two bytes:

```text
6 bytes -> 2 bytes
-4 bytes per occurrence
```

The actual PC-KO bytes reproduce this relation exactly. Reverse-orientation literals `는(은) / 가(이) / 를(을) / 로(으)` are absent from this ECF corpus.

## 2. V335 particle-count correction

V335 correctly classified product admission, but its single semantic-detail axis loses particle applicability on rows classified first as `INCLUDE_KO_CHOICE`.

Exact current V334/V335-bound population:

```text
semantic code 3 / INCLUDE_KO_FIXED_SURFACE_PARTICLE
  rows          1,226
  occurrences   1,364

semantic code 2 / INCLUDE_KO_CHOICE with explicit dual literal
  rows             25
  occurrences      25

FIXED_SURFACE_PARTICLE_V1 exact applicability
  rows          1,251
  occurrences   1,389
```

Therefore the old combined interpretation `1,226 rows / 1,389 occurrences` is rejected for implementation routing. The total 1,389 occurrence census remains correct, but 25 occurrences live on 25 choice rows.

Exact occurrence breakdown:

```text
은(는)   521
이(가)   395
을(를)   358
과(와)    41
와(과)    51
(으)로    23
----------------
total   1,389
```

Rows by occurrence count:

```text
1 occurrence   1,125 rows
2 occurrences    115 rows
3 occurrences     10 rows
4 occurrences      1 row
```

Aggregate fixed-surface shrink relative to raw PC-KO payload:

```text
1,389 * -4 = -5,556 bytes
```

## 3. Applicability ledger

Canonical artifact:

`selective_ko/artifacts/ecf00000_v344_particle_preimplementation_v1/PARTICLE_APPLICABILITY_COMPACT.bin`

```text
records       1,251
record size      23 bytes
serialization   <IHIIBBBBxHH
sha256          b6d228b6b1e8e23285763b88d5d5eda6064153433123283217c4ea955d550a4d
rowset sha256   8282d175c6666f8fa4700a28f4917ea32abe3d315d0b7a98ebdee53650831aa7
```

The ledger binds V334 row ID, partition, original/KO offsets, opcode, V335 semantic code, occurrence count, choice-overlap flag, raw KO command length and transformed command length.

The deterministic transformed-corpus membership hash is:

`f86a4f49f18c741445dcf9fc69390b818be5feba7f256973a9a69cdbd33368c5`

Applicability is now explicitly independent of `semantic_detail`.

## 4. Byte-level transform validation

Across all 1,251 rows:

```text
literal overlap                     0
escape-token internal replacement   0
command header mutation             0
choice string-count mutation        0
4-byte alignment violation          0
remaining approved dual literal     0
```

Each replacement changes length by exactly four bytes, preserving mod-4 alignment of the affected string field.

## 5. Read-only whole-context simulation

Diagnostic-only simulation context:

```text
V335 codes 1 / 2 / 4
+ exact fixed-particle applicability 1,251 rows
+ V342 1E ready-23
+ V339 5A
+ V337 generic relocation
+ V338 special spans
```

Output:

```text
size             1,102,600
sha256           658d21cecbd038f39f89cf65e063d68861a481e96e73f530387c7133d46f3295
delta vs V342    +20,948
```

This output is diagnostic only and is not a product artifact.

Structural gates:

```text
baseline walker errors       0
V337 generic relocation      PASS
V338 special spans           PASS_3_OF_3
V338 false-02                PASS_2_OF_2
V339 5A violations           0
```

The large positive delta vs V342 is expected because V342 still preserves all code-3 rows as original JP; V344 simulation both admits their Korean payload and then applies the -5,556-byte particle normalization.

## 6. State-aware residual cause-family expansion

The particle simulation exposes three raw state-aware observations:

```text
0xBDD78   inherited stock residual              1 observation
0xC3740   same logical residual under S/F states 2 observations
```

Unique logical residuals: 2.

`0xC3740` is not a new product command. It is:

```text
EVENT 0x0B @ 0xC373C
  +4 -> apparent 0x0E @ 0xC3740
```

The apparent child is inside the original parent 0x0B runtime extent.

## 7. Exact 0x0B+4 -> 0x0E alias family

The stock corpus contains 52 exact structural candidates where:

```text
parent opcode        0x0B
alias inner offset   +4
alias byte           0x0E
alias lies inside parent runtime extent
```

Parent-length distribution:

```text
8 bytes    33
12 bytes   19
------------
total      52
```

No alias original offset is a TS5 entrypoint or a V334 canonical text/choice target.

Source-proven dispositions:

```text
INHERITED_STOCK_RESIDUAL    1
NOVEL_ALIAS_ELIGIBLE       48
NOT_GATE_ELIGIBLE           3
-----------------------------
total                       52
```

The three non-eligible rows are retained as structural evidence and are not whitelisted. They consist of one parent not reached by the stock state-aware model and two aliases whose decoded child length is zero.

Compact alias ledger:

```text
records       52
record size   26 bytes
serialization <HIIIHIIBB
sha256        62e2d01d5aab9b8bc9a156e04acf3842cdef8ca58bbc29c8629228aec651518c
rowset sha256 857b880f7380447928fc46abad4d1d66e012859ad00eeaaaaa54f73f17f27c97
```

## 8. V344 validator gate

`builder/selective_event_validation.py` is upgraded from the V340 absolute stock-residual differential gate.

New rule for a residual not present in the stock baseline:

```text
candidate original anchor/opcode/decoded length
must match exact NOVEL_ALIAS_ELIGIBLE ledger row
AND current bytes must prove:
  same 0x0B parent header
  same parent decoded length
  alias exactly at parent +4
  same 0x0E header
  same alias decoded length
  same partition containment
otherwise BLOCK
```

This is not a blanket `0x0B+4` whitelist.

State observation handling is also corrected:

```text
same logical key + same current offset
  -> collapse as multiple state observations

same logical key + different current offset
  -> BLOCK as ambiguous
```

Validator module SHA-256:

`d08fb0eca0ef1f9e82cd14aa5b96e626d693add2f2088cb84014dd2b453c4d66`

Validator test SHA-256:

`b14cf3b34f5d4c90e5b9b5259df9a446459f68bfe7636fa6ff2c6ed18e1f1520`

Repository EVENT regression:

`PASS_35_OF_35`

The full particle diagnostic passed the new gate as:

```text
candidate observations       3
unique logical residuals     2
inherited stock              1
source-proven alias          1
novel                        0
blocking                     false
```

## 9. Rejected / do-not-repeat

Reject:

- use `semantic_detail == code 3` as the sole particle applicability gate;
- treat `1,226 rows / 1,389 occurrences` as an exact implementation population;
- omit the 25 choice-overlap rows;
- globally replace ordinary particles outside exact dual literals;
- normalize raw bytes outside parsed message/choice string fields;
- add only `0xC3740` as a one-off validator exception;
- blanket-whitelist all command-looking bytes inside 0x0B;
- require every conservative S/F observation to have a distinct logical residual;
- interpret a new MAY-model alias as proof that the transformed product VM is corrupt without source provenance.

## 10. Current disposition / next scope

```text
V343 3C KEEP_JP ledger                    CLOSED
V344 particle applicability ledger         MATERIALIZED
V344 V335 particle-count correction        CLOSED
V344 source-aware alias ledger             MATERIALIZED
V344 source-aware residual validator       IMPLEMENTED / OFFLINE PASS
particle serializer                        NOT IMPLEMENTED
product/build/package/IPS                  NONE
```

Exact next scope after a fresh explicit user signal:

`ECF00000_FIXED_SURFACE_PARTICLE_V1_IMPLEMENTATION_OFFLINE_VALIDATION`

That next scope may implement only the exact 1,251-row applicability ledger and canonical six-to-two-byte mapping, then rerun V337/V338/V339/V340/V344 gates. It must not promote the 21 pending 0x1E rows, resume unrelated S4 families, build/package/IPS, or run hardware without another explicit authorization.
