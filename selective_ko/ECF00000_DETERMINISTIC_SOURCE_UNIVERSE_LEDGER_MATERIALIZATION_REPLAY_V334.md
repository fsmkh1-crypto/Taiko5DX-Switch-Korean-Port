# ECF00000 DETERMINISTIC SOURCE-UNIVERSE LEDGER MATERIALIZATION / CLEAN REPLAY — V334

Date: 2026-09-20 (KST)

```text
validation_id   V334
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      ARTIFACT_MATERIALIZATION_AND_REPLAY_VALIDATION
parent          cf43820aee6677d5db7ae4c3dfa95e608e12ab61 / V333
product_bytes   UNCHANGED
serializer      NOT IMPLEMENTED
build/package   NONE
repository      DOCUMENTATION_AND_PROVENANCE_ARTIFACTS_ONLY
```

V334 materializes the exact V333 deterministic MAY-reachable EVENT source universe and closes the aggregate-without-membership provenance gap that existed for historical V324.

## 1. Canonical result

```text
source universe                   13,075
PC-KO replacement candidates      12,599
preserve-original candidates         476
Korean-bearing                    12,597

opcode 0x11                       10,320
opcode 0x12                        1,075
opcode 0x13                        1,322
opcode 0x15                          358
```

Exact compact rowset identity:

```text
serialization  sorted rows; struct <IB
               uint32_le KO physical offset + uint8 opcode
sha256         1f927558cf5c16f636d8c3c15323c4bd498e279332ce9ebe9595fa27307c5631
```

The canonical construction remains:

```text
V330 exact baseline                         2,863
local parser baseline                       2,866
local-only target-validity difference           3
  0x364FC
  0xE9AF0
  0xE9AFC

state-aware raw                            13,078

canonical =
  V330 exact baseline
  UNION
  (state-aware raw - local parser baseline)

canonical                                  13,075
```

The three local-only offsets are not removed to numerically fit any historical count. They remain excluded because V333/V334 preserve the exact V330 target-validity baseline and add only the independently established state-machine cause-family delta.

## 2. Exact original -> Korean binding

The materialized ledger closes:

```text
mapping rows                  13,075
distinct original rows        13,075
mapping collisions                 0
opcode mismatches                  0
partition mismatches               0
target-target runtime overlaps     0
```

Mapping provenance:

```text
EDITOR_TARGET_ORDINAL             12,713
EDITOR_TARGET_ALIGNMENT              360
V333 0x5A drift special binding        2
                                  ------
                                  13,075
```

Special bindings:

```text
KO 0x16828 -> original 0x12C40
KO 0x168E0 -> original 0x12C90
```

The exact verbose mapping is preserved in Drive. The compact mapping inside the canonical ZIP is sorted by KO offset and uses:

```text
struct <IIBBBx
original_offset uint32_le
ko_offset       uint32_le
opcode          uint8
disposition     uint8  0=PRESERVE_ORIGINAL / 1=REPLACE_FROM_PC_KO
mapping_method  uint8  0=ORDINAL / 1=ALIGNMENT / 2=V333_5A_DRIFT_BINDING
pad             uint8
record size     12
record count    13,075
sha256          d510f2965483b3b5a22dbef06a9bfe059bb82fa96c1f36b05423e7fb0438cccc
```

## 3. Artifact identities

Canonical verbose artifacts:

```text
GENERATOR.py
a0677b9bee1f50a191606a2eada3f391dfdf57851ccb913d2b8c54acb6e33eec

ROWS.jsonl
aef17d206559ec548a5fb3c2414d8a1f17832f7e4c2df03b8468240926c11b65

MAPPING.jsonl
5c9f8a96f985b5cf691b5303b90cff23a8e54b541b5151790a0e93f09045f600

ROWSET_OFFSET_OPCODE.bin
1f927558cf5c16f636d8c3c15323c4bd498e279332ce9ebe9595fa27307c5631

MAPPING_ORIGINAL_KO_COMPACT.bin
d510f2965483b3b5a22dbef06a9bfe059bb82fa96c1f36b05423e7fb0438cccc

INDEX.json
4d0b68dfffef91ee94f44d8a30a11228d347fad8319e9dd555239294849bf2e5

REPLAY_VALIDATION.json
2ee8479817d466657650223804fb0187b4bb1afffdaf3b7646ba0e0423442da2

MANIFEST.sha256
9daecac032f50b160e945594404c8f5386284d764fec798fbb65d65411a6a274
```

Repository stores the small metadata/provenance files under:

`selective_ko/artifacts/ecf00000_v334_source_universe_ledger_v1/`

The complete verbose ledger, generator, and compact binaries are preserved as one canonical Drive ZIP rather than duplicating ~12 MB of verbose JSON in Git.

## 4. Google Drive preservation

```text
path
Google Drive/GPT/태합입지전/ECF00000_V334_SOURCE_UNIVERSE_LEDGER/

folder id
18TFmrFV8fpyaMpKLOPpa2hmAp6rNfLMW

file
ECF00000_V334_SOURCE_UNIVERSE_LEDGER_CANONICAL.zip

file id
1zunx5DYMOWUtkIPOBUxVCCeDeE27eU1q

size
1,530,925 bytes

sha256
fc47e81842f299f04c272b6076637ec163cdca2ed469b17105bc36182dc765e0

upload/download roundtrip
PASS_BYTE_IDENTICAL
```

Drive was read back after upload and the returned bytes reproduce the exact ZIP SHA above.

## 5. Clean replay

The final generator was executed independently in two fresh output directories with the same exact input identities.

Result:

```text
source-universe rows     13,075 / 13,075
replacement              12,599 / 12,599
preserve                     476 / 476
Korean-bearing            12,597 / 12,597
state-aware errors             0
baseline errors                 0
target overlaps                 0

ROWS.jsonl                    BYTE_IDENTICAL
MAPPING.jsonl                 BYTE_IDENTICAL
ROWSET_OFFSET_OPCODE.bin      BYTE_IDENTICAL
MAPPING_ORIGINAL_KO_COMPACT   BYTE_IDENTICAL
INDEX.json                    BYTE_IDENTICAL
REPLAY_VALIDATION.json        BYTE_IDENTICAL
```

Disposition:

`PASS_BYTE_IDENTICAL`

The exact V333 source-universe membership is therefore no longer count-only evidence.

## 6. Runtime/editor boundary and special-owner carry-forward

The exact ledger revalidates:

```text
runtime/editor boundary mismatch rows          113
mismatch rows that are actual replacement       0
```

All 113 are preserve-original and do not block replacement rows.

Special serializer annotations remain:

```text
SWITCH_DYNAMIC_SPAN
  0xFDC04  EVENT 0x04
  0x7F7A8  EVENT 0x04
  0x9DAE4  BRANCH 0x09

NOT_EVENT_OWNER / EVENT_0x0A_EXPRESSION_DATA
  0xD7008
  0xBDC58
```

Full-PC-KO diagnostic branch headers/spans remain diagnostic only and MUST NOT be hardcoded into a selective build.

## 7. Historical 4,444 disposition

Historical V324 aggregate counts remain claim-level evidence only.

V334 does not fit, prune, or tune 13,075 to 4,444.

Do not repeat:

- count-only reconstruction without exact membership;
- state-aware raw 13,078 as canonical membership;
- numeric fitting to 4,444;
- final-Korean fresh reparse as ownership authority;
- treating 0xD7008/0xBDC58 as EVENT 0x02 owners;
- reclassifying the 113 boundary mismatches as replacement blockers.

## 8. Remaining semantic-admission gap

V333 carried aggregate semantic results:

```text
INCLUDE_KO     12,171
UNRESOLVED        426
```

Those aggregate counts are not yet persisted as exact row-level admission membership on the V334 13,075 ledger.

Therefore serializer implementation remains blocked until the semantic-admission layer is materialized against the exact V334 row IDs/offsets.

## 9. Current disposition

```text
exact source-universe membership     MATERIALIZED
exact original->KO mapping           MATERIALIZED
clean replay                         PASS_BYTE_IDENTICAL
Drive roundtrip                      PASS_BYTE_IDENTICAL
Git provenance metadata              MATERIALIZED
semantic admission exact rowset      NOT_YET_MATERIALIZED
serializer implementation            NOT AUTHORIZED BY V334
product bytes / build / package      NONE
```

## 10. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_V334_SOURCE_UNIVERSE_SEMANTIC_ADMISSION_LAYER_MATERIALIZATION_READ_ONLY`

Authorized next:

- bind inherited semantic-admission rules to exact V334 row IDs;
- materialize exact INCLUDE_KO / UNRESOLVED / other disposition membership;
- prove aggregate totals against the V333 12,171 / 426 evidence;
- preserve exact row provenance and rejected hypotheses;
- stop before serializer implementation.

Not authorized next:

- EVENT serializer implementation;
- EVENT payload rewrite;
- build/package/IPS;
- unrelated EVENT files;
- SNR;
- numeric fitting to historical 4,444.
