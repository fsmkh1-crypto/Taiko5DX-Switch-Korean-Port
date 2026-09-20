# ECF00000 DETERMINISTIC SOURCE UNIVERSE AND SERIALIZER CONTRACT CONSOLIDATION — V333

Date: 2026-09-20 (KST)

```text
validation_id   V333
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      DOCUMENTATION_CONSOLIDATION_CHECKPOINT
parent          c32dde9857c49b1a833aa1cd3d67fcb455453d52 / V332
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint consolidates the post-V332 READ ONLY EVENT analysis into one implementation-preparation contract. It does not implement a parser or serializer and does not promote historical V324 aggregate counts to exact membership.

## 1. Authority split

The implementation contract uses the following authority boundary.

```text
Switch runtime
  -> command boundary and execution semantics
  -> EVENT/BRANCH context transitions
  -> runtime state semantics
  -> runtime branch-length interpretation

PC editor v0.30
  -> edit-partition ownership
  -> source-proven branch arithmetic
  -> false-positive/disguised-command guards
  -> branch-distance repair behavior
  -> partition-size / TS5 offset-table rebuild behavior

PC Korean payload
  -> visible Korean replacement bytes and authored Korean text oracle

Historical V324 4,444
  -> claim-level aggregate evidence only
  -> never a numeric fitting target
```

Final-PC-KO fresh reparsing is not serializer ownership authority. Original-PC editor ownership plus exact original-to-Korean logical binding is the preservation authority.

## 2. Deterministic MAY-reachable source universe

The state-aware full replay uses the already closed EVENT/BRANCH runtime model and the EVENT branch-state model.

Traversal identity is at least:

```text
(context, physical_address, S, F)
```

where:

- EVENT descriptor/handler = `[0xA1C000+0x290]+0x10 / 0x15F44C`;
- BRANCH descriptor/handler = `[0xA1C000+0x358]+0x10 / 0x160BF8`;
- EVENT `0x06/0x08` enter BRANCH;
- BRANCH `0x07/0x09` can re-enter EVENT;
- `0x04/0x05` depend on EVENT state `S/F`;
- choice `0x15` contributes the exact normal selection domain `0..N-1`;
- boolean/result writers use their source-proven branch-relevant domains.

The deterministic structural result is:

```text
MAY_REACHABLE physical targets   13,075
messages                         12,717
choices                             358
choice strings                      728
Korean-bearing targets           12,597
INCLUDE_KO under inherited rules 12,171
UNRESOLVED                           426
non-Korean                           478
```

The sorted `physical_offset + opcode` rowset diagnostic SHA-256 observed in the READ ONLY replay is:

```text
1f927558cf5c16f636d8c3c15323c4bd498e279332ce9ebe9595fa27307c5631
```

Disposition:

```text
13,075 = DETERMINISTIC MAY-REACHABLE STRUCTURAL SOURCE UNIVERSE
13,075 != proven exact gameplay-feasible corpus
13,075 != historical V324 4,444 rowset
```

The MAY-reachable corpus intentionally unions structurally valid runtime outcomes. Predicate correlation across concrete game-state variables is not modeled and is not required merely to establish a conservative localization source universe.

## 3. Exact original counterpart binding

Switch v1.1.3 original `ECF00000.TS5` remains byte-identical to PC original:

```text
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09
```

PC Korean `ECF00000.TS5` remains:

```text
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
```

The READ ONLY binding audit found:

```text
MAY candidate rows                  13,075
exact original counterparts         13,075
distinct original targets           13,075
mapping collisions                       0
opcode mismatches                        0
partition mismatches                     0

original != PC Korean rows          12,599
byte-identical preserve rows           476
```

Therefore the source-universe population splits into:

```text
12,599  actual PC-Korean replacement candidates
   476  preserve-original candidates
13,075  total
```

The exact 13,075 membership/mapping ledger is not yet persisted in the repository. Counts and the observed diagnostic rowset hash are canonicalized by V333, but exact membership MUST be materialized and replay-verified before serializer implementation. This requirement exists specifically to avoid repeating the V324 aggregate-without-rowset provenance failure.

## 4. Target ownership and boundary compatibility

Against the original-PC editor graph:

```text
normal editor target owners   13,074
disguised 0x15 owner               1
missing editor owner                0
target-target runtime overlaps      0
```

Additional provenance properties:

```text
targets reached from multiple roots       147
targets reached under multiple S/F states 2,705
```

Physical replacement ownership is deduplicated by physical target. Multiple roots/states remain provenance only and do not cause duplicate writes.

A total of 113 rows show runtime/editor boundary disagreement:

```text
0x11  100
0x13   12
0x15    1 disguised
```

All 113 are byte-identical between original and PC Korean and therefore are preserve-original rows, not selective replacement rows. No changed replacement row remains blocked by this boundary mismatch.

## 5. Final-Korean fresh reparse is forbidden as ownership authority

Freshly reparsing the final PC-Korean payload with the PC editor heuristics can change grouping because translated payload bytes alter edit-time heuristic boundaries.

Two confirmed examples are Korean `0x13` targets:

```text
KO 0x16828 -> original 0x12C40
KO 0x168E0 -> original 0x12C90
```

They are valid original target owners but become swallowed by a Korean-side `0x5A` grouped item during fresh reparse.

Required serializer rule:

```text
ownership authority =
  original-PC editor graph
  + exact original->Korean target mapping

NOT =
  fresh parse of final Korean payload
```

## 6. EVENT 0x04 / 0x05 state contract

`0x04` and `0x05` are not unconditional recursive containers.

Project-local runtime state:

```text
S = current result / selection state
F = branch-chain state
initial fresh EVENT context: S=1, F=1
```

For the 11-bit label `L`:

```text
0x04:
  always evaluate L

0x05:
  evaluate only when F == 1
  if F == 0, skip the test/child path

match:
  L == 0x3FF OR L == S
    -> F = 0
    -> execute child EVENT at p+4 using a fresh EVENT context

mismatch:
    -> F = 1
    -> child not executed
```

Normal choice-state values are `0..N-1`; branch-relevant message/UI boolean results are `0/1`. Special/cancel UI values do not create additional ordinary 11-bit label matches.

The historical V330 unconditional `0x05` treatment is not exact runtime semantics.

## 7. Dynamic branch-span exceptions required by Switch

Most branch preservation is governed by original-PC ownership plus source-proven PC editor arithmetic. Three runtime owners require Switch-specific dynamic span calculation in the final selective layout.

### 7.1 EVENT 0x04 at PC-Korean 0xFDC04

Original owner counterpart:

```text
original  0xCBBB0
KO full   0xFDC04
```

This is a real Switch EVENT `0x04`, although the PC editor false-`04` guard groups the preceding `0x17 + 0x04` pattern as edit-time payload.

The apparent preceding `0x17` is part of a `0x0A` expression operand stream, not an owning EVENT command. The actual `0x04` span field occupies the latter two header bytes, so recalculating the span does not corrupt the preceding operand interpretation.

Full-PC-KO diagnostic span only:

```text
original span       456
full-KO span        628
diagnostic header   04 01 E8 04
```

Do not hardcode that diagnostic header. Final selective output MUST calculate the span from the actual rebuilt layout.

### 7.2 EVENT 0x04 at PC-Korean 0x7F7A8

Original owner counterpart:

```text
original  0x65F40
KO full   0x7F7A8
```

This is likewise a real Switch EVENT `0x04`, not a false runtime command.

Full-PC-KO diagnostic span only:

```text
original span       92
full-KO span        128
diagnostic header   04 01 00 01
```

Final selective output MUST dynamically calculate the actual span.

### 7.3 BRANCH 0x09 at PC-Korean 0x9DAE4

Original counterpart:

```text
original  0x7E1B0
KO full   0x9DAE4
```

For bytes `09 F0 6F 14`:

```text
PC editor preservation interpretation  2614
Switch runtime interpretation           2612
```

Switch runtime's `(word >> 19) << 2` points exactly to the next BRANCH `0x09` boundary in the original layout.

Full-PC-KO diagnostic span:

```text
3524
diagnostic full-KO header  09 F0 8F 1B
```

Do not hardcode that diagnostic header. Final selective output MUST compute the Switch-runtime span from the actual rebuilt next physical `0x09` position.

## 8. Two false EVENT-0x02 owners are expression data

The following Korean-side physical positions MUST NOT be treated as EVENT `0x02` branch owners:

```text
0xD7008
0xBDC58
```

They are operands consumed by the preceding EVENT `0x0A` expression structure.

Representative structure:

```text
0xD7000  0A ...
0xD7004  expression operand #1
0xD7008  02 ...  expression operand #2
0xD700C  next actual EVENT command

0xBDC50  0A ...
0xBDC54  expression operand #1
0xBDC58  02 ...  expression operand #2
0xBDC5C  next actual EVENT command
```

They are not TS5 entrypoints, not proven EVENT child starts, and have no valid EVENT predecessor establishing them as runtime EVENT `0x02` owners.

Rejected serializer behavior:

- calculating a branch span from either position;
- treating their large apparent ranges as target ownership;
- blocking translations inside those apparent ranges merely because the first operand byte is `0x02`.

These bytes remain expression data and are preserved according to their enclosing command.

## 9. Historical 4,444 disposition

The historical V324 aggregate remains:

```text
physical 4,444
messages 4,193
choices 251
Korean 4,238
INCLUDE 4,123
UNRESOLVED 115
```

V332 closed recovery of the original exact membership as unsuccessful with preserved accessible evidence.

V333 does not numerically fit the deterministic corpus to those counts.

Rejected/do-not-repeat:

- filtering 13,075 until it equals 4,444;
- treating V330 2,863 as complete EVENT membership;
- adding `0x04` unconditionally;
- treating `0x05` as unconditional recursion;
- using PC editor 15,945 target-looking items as runtime membership;
- fresh-reparsing final Korean bytes as ownership authority;
- treating `0xD7008/0xBDC58` as EVENT `0x02` branch owners;
- preserving all branch fields merely because the PC patched file left them unchanged;
- hardcoding full-PC-KO diagnostic branch headers into a selective build.

## 10. Preimplementation acceptance gates

Before serializer implementation is authorized, the exact source-universe ledger must be materialized and replay-verified.

Required artifact-level gates:

1. exact 13,075 physical target membership persisted;
2. exact original counterpart for 13,075/13,075 persisted;
3. replacement/preserve split exactly 12,599/476;
4. zero mapping collisions;
5. zero opcode mismatches;
6. zero partition mismatches;
7. zero target-target runtime overlaps;
8. exact rowset replay hash stable across clean rerun;
9. `0xD7008/0xBDC58` explicitly marked expression-data / non-owner;
10. dynamic Switch-span owner policy persisted for `0xFDC04/0x7F7A8/0x9DAE4`;
11. final-KO fresh reparse explicitly forbidden as ownership authority;
12. historical 4,444 retained only as historical aggregate evidence.

## 11. Current disposition

```text
deterministic source-universe contract     CLOSED_V333
MAY-reachable target count                 13,075
actual replacement candidates              12,599
preserve-original candidates                  476
exact original counterpart count           13,075 / 13,075
exact rowset/mapping artifact               NOT_YET_MATERIALIZED
serializer implementation                  NOT_AUTHORIZED_BY_V333
payload/build/package/IPS                   NONE
```

## 12. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_DETERMINISTIC_SOURCE_UNIVERSE_LEDGER_MATERIALIZATION_AND_REPLAY_VALIDATION`

Authorized next:

- deterministically regenerate the exact 13,075 source-universe rows from the V333 contract;
- materialize exact physical membership and original->Korean counterpart mapping;
- persist replacement/preserve disposition;
- persist dynamic-span / false-owner annotations;
- clean rerun and verify exact rowset identity/hash;
- update canonical documentation only after artifact verification.

Not authorized next:

- serializer implementation;
- EVENT payload rewrite;
- build/package/IPS;
- numeric fitting to 4,444;
- unrelated EVENT files;
- SNR;
- reopening already closed Switch/PC-editor semantics without genuinely contradictory evidence.
