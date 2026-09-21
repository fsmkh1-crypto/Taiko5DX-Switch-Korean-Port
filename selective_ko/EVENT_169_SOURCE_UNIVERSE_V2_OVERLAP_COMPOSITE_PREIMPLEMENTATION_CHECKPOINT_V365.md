# EVENT 169 source-universe v2 / overlap-composite preimplementation checkpoint — V365

Date: 2026-09-21 (KST)

```text
validation_id   V365
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_SOURCE_UNIVERSE_AND_COUNTERPART_MAPPING_CHECKPOINT
parent          589ce489cc9ff1fc2c58e3630803c5bbfe5fce95
implementation  NONE
product bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
ledger status   NOT MATERIALIZED
```

## 1. Scope and claim boundary

This checkpoint records the whole-family read-only findings obtained after V364 and closes the
specific direct-target collision observed while preparing the next exact ledger replay.

It does not claim that the EVENT-169 source-universe v2 ledger, the 31 overlap-composite recipes,
or the full semantic replay have been materialized. Global counts below remain provisional until
that replay closes with zero unaccounted owners and zero ambiguous product bindings.

The exact Nintendo Switch EVENT input is the Drive folder:

```text
project path  태합입지전 프로젝트/Switch/EVENT
folder id     1byPWJuG7dIn4KVS2GFLpXiMsDUHaZuHh
TS5 files     169
TE5 files     169
```

## 2. Inherited whole-family read-only results

```text
Switch TS5 vs PC original SHA-256       169 / 169 byte-identical
parser noop serialization               169 / 169 byte-identical
PC-original editor owners                     66,977
runtime-only valid owners                         10
provisional source-owner universe              66,987
provisional direct/header-preserved            66,956
provisional overlap-composite                       31
```

The ten runtime-only valid owners are bounded to:

```text
EFF0C300   2
EFF2D200   1
EKF00400   2
EKF00800   2
EP124B00   3
TOTAL     10
```

The 31 overlap-composite rows remain a distinct preimplementation family. Their PC-authored Korean
surface must be recovered while preserving Switch-original headers, control bytes, branch ownership,
and the identity policy:

```text
identity presentation fields       KEEP_JP
authored Korean prose literals     PRESERVE_AS_AUTHORED_KO
runtime-inserted identity          KEEP_JP
reverse identity substitution      FORBIDDEN
```

Two duplicate-KO counterpart overrides remain required:

```text
ECF00000 source 0x71AD0
EP111700 source 0x1364
```

The direct EVENT percent-root support set remains provisionally closed at 48:

```text
V357 roots                  46
%12 -> TAI5MSG B0:181       +1
%33 -> TAI5MSG B0:307       +1
TOTAL                       48
```

## 3. Collision input identity

```text
file                         EP124B00.TS5
Switch / PC-original bytes   150,508
Switch / PC-original SHA-256 8ff94b34fb1db16cbd4f15ca63df3a786ca3100787278d2c9fab7d2a1d70061c
PC-KO bytes                  184,056
PC-KO SHA-256                e0d54ba7777350a8f3601269b4e15ed1256a2aa4ad42ca51f4a96ddf66b15299
partition index              111
original bounds              0x22590..0x22CB4
PC-KO bounds                 0x2A050..0x2A928
source target owners         34
fresh-grouped KO targets     31
```

## 4. Root cause

Source owner `0x22624` contains the literal escape-bearing text `\\<1F3`.

```text
original '<' offset   0x2263B
original modulo 4     3
PC-KO '<' offset      0x2A0FC
PC-KO modulo 4        0
byte                   0x3C
```

The translated byte layout moved the ordinary ASCII `<` onto a four-byte boundary. The PC editor
v0.30 grouping heuristic therefore treated `0x2A0FC` as a structural `0x3C` command even though it
is inside the text payload of the real `0x11` owner beginning at `0x2A0E4`.

That false group swallowed three subsequent, runtime-valid raw `0x11` headers:

```text
0x2A120
0x2A154
0x2A194
```

The old alignment left three source owners unmatched and incorrectly assigned the first visible KO
target to a later source owner:

```text
source 0x22624   unmatched
source 0x22654   unmatched
source 0x2267C   unmatched
source 0x226B0 -> KO 0x2A0E4   WRONG
```

Adding only `0x22624 -> 0x2A0E4` therefore produced a direct-target collision. The collision assertion
was correct and must not be weakened.

## 5. Partition-atomic reconstruction

```text
source       correct KO   KO length   KO end
0x22624  ->  0x2A0E4         60       0x2A120
0x22654  ->  0x2A120         52       0x2A154
0x2267C  ->  0x2A154         64       0x2A194
0x226B0  ->  0x2A194         56       0x2A1CC
0x226DC  ->  0x2A1CC         12       0x2A1D8
```

Reconstructing the complete partition target sequence gives:

```text
source owners                    34
corrected KO owners              34
opcode-sequence equality         PASS
four-byte header equality        PASS 34 / 34
unique KO targets                PASS 34 / 34
direct-target collisions         0
```

Exactly four mappings change relative to the old fresh-group alignment:

```text
0x22624   NONE      -> 0x2A0E4
0x22654   NONE      -> 0x2A120
0x2267C   NONE      -> 0x2A154
0x226B0   0x2A0E4  -> 0x2A194
```

The remaining 30 mappings in partition 111 are unchanged.

## 6. Global impact

This correction adds neither a source owner nor an overlap-composite row. All four changed mappings
belong to the direct/header-preserved family. The provisional top-level accounting remains:

```text
source-owner universe          66,987
direct/header-preserved        66,956
overlap-composite                  31
```

However, `0x226B0 -> 0x2A0E4` is one newly proven wrong-existing mapping outside the previously
enumerated minimum 22. The confirmed lower bound is now at least 23. The exact global number must
not be frozen until every direct-drift partition is rebuilt atomically.

## 7. Rejected / do not repeat

- weakening or removing the direct-target uniqueness assertion;
- treating the collision as a legitimate shared KO-target alias;
- rejecting the otherwise correct `0x22624 -> 0x2A0E4` counterpart;
- adding only the three formerly unmatched rows without reassigning `0x226B0`;
- treating payload byte `0x2A0FC = 0x3C` as a real structural owner;
- using final PC-KO fresh grouping as source-ownership authority;
- adding these four direct/header-preserved rows to the 31 overlap-composite family;
- assuming the remainder of partition 111 shifted after the local recovered chain.

## 8. Mandatory ledger gates

Each remaining direct-drift partition must be rebuilt as a complete partition mapping, not as
independent row overrides. Admission requires all of:

```text
source owner count == reconstructed KO owner count
opcode sequence equality
four-byte header equality
runtime event_len continuity
partition-bound containment
unique KO target count == mapping row count
direct-target collisions == 0
unaccounted source owners == 0
```

The 31 overlap-composite rows must remain separate and receive exact per-row recipes containing
source owner, PC-KO containing parent, Korean surface byte slice, surrounding control bytes,
Switch-original header/owner, identity policy, transform order, and final selective payload contract.

## 9. Exact next scope

`EVENT_169_SOURCE_UNIVERSE_V2_OVERLAP_COMPOSITE_31_PREIMPLEMENTATION_EXACT_LEDGER_MATERIALIZATION_REPLAY`

Materialize only the exact source-universe v2, direct binding, duplicate override,
overlap-composite, semantic replay, and 48-root cross-carrier ledgers. First apply the
partition-atomic rule to every remaining direct-drift partition.

```text
source owners                    66,987 exact
unaccounted source owners             0
ambiguous product bindings            0
direct-target collisions              0
overlap-composite recipes            31 exact
semantic replay                 complete
```

No product serializer implementation, EVENT/TAI5MSG mutation, build, package, IPS, or hardware is
authorized by this checkpoint.
