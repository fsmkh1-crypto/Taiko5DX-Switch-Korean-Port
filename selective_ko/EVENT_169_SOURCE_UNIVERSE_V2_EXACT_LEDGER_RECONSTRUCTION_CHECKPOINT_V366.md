# EVENT 169 source-universe v2 exact-ledger reconstruction checkpoint — V366

Date: 2026-09-21 (KST)

```text
validation_id   V366
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_EXACT_LEDGER_RECONSTRUCTION_CHECKPOINT
parent          b1826ba4c34c2354257cbd19165548dce4868ad9 / V365
implementation  NONE
product bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

## 1. Scope and claim boundary

V366 independently reconstructs the lost EVENT-169 exact-ledger state from V365 without using the
old Codex V366 counts as generation inputs. The old numbers were cross-check references only after
independent materialization.

This checkpoint closes exact source-owner membership, direct/header-preserved binding,
overlap-composite recipes, leading-control recovery, duplicate-KO overrides, whole accounting,
and the 48 independent percent-root census.

Two claims are intentionally **not** promoted by this reconstruction:

```text
runtime event_len continuity      NOT independently generalized for all 66,987 owners
full semantic admission replay    NOT independently rederived as a whole-family classification
```

Those are the next bounded READ ONLY closure scope. No product serializer implementation,
EVENT/TAI5MSG mutation, build, package, IPS, or hardware is authorized here.

## 2. Canonical inputs

```text
canonical Git base                b1826ba4c34c2354257cbd19165548dce4868ad9
Switch EVENT TS5                  169
Switch vs PC-original parity      inherited VERIFIED 169/169 byte-identical
PC-KO source                      exact v1.02 embedded EVENT payloads
PC-KO EVENT files                 169
PC-KO aggregate patched bytes     4,085,204
```

The v1.02 PC-KO EVENT working set was recovered directly from the patcher's embedded payload.
All 169 extracted files matched the patcher's per-file PatchedSize and PatchedSha256 metadata.
Representative anchors remained exact:

```text
ECF00000.TS5  1,156,480  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
EP124B00.TS5    184,056  e0d54ba7777350a8f3601269b4e15ed1256a2aa4ad42ca51f4a96ddf66b15299
```

A different Drive `Taiko5DX/data/EVENT` installation-state folder was rejected as source authority
because its ECF00000 and EP124B00 sizes did not match the canonical embedded payloads.

## 3. Independent source universe

Replaying the actual PC editor v0.30 grouping rule over all 169 Switch-original TS5 files gives:

```text
editor source owners        66,977
runtime-only valid              10
source-owner universe       66,987
```

The ten runtime-only owners are bounded to:

```text
EFF0C300   2
EFF2D200   1
EKF00400   2
EKF00800   2
EP124B00   3
TOTAL     10
```

Thirteen aligned raw target-like candidates existed outside editor grouping; ten are valid
runtime owners and three are false payload hits.

## 4. Direct/header-preserved ledger

Independent reconstruction gives:

```text
direct editor rows          66,946
direct runtime-only rows        10
direct/header-preserved     66,956
unique direct targets       66,956
direct-target collisions         0
header equality             PASS 66,956 / 66,956
partition containment       PASS 66,956 / 66,956
per-partition target order  PASS
```

Nine direct-only drift partitions were rebuilt atomically rather than patched row-by-row:

```text
ECF00000   partitions 11, 89, 247, 283
EFF0C300   partition 30
EP111700   partition 1
EP124B00   partitions 111, 112, 113
```

Eight repeated-header LCS boundaries were ambiguous under header-only alignment and were resolved
by preserved surrounding-anchor order rather than arbitrary tie-breaking.

Two duplicate-KO counterpart overrides remain exact and necessary:

```text
ECF00000 source 0x71AD0 -> chosen 0x8E010; duplicate-looking 0x8E040 equals source
EP111700 source 0x1364  -> chosen 0x1794;  duplicate-looking 0x17B0 equals source
```

Three old Codex reference rows were reproduced independently after generation:

```text
ECF00000 0x96E6C -> 0xBC498
ECF00000 0x96E7C -> 0xBC4A8
EKF00800 0xF60   -> 0x1308
```

## 5. Overlap-composite 31

The exact remainder is a disjoint 31-row reconstruction family:

```text
source-owner universe          66,987
direct/header-preserved        66,956
overlap-composite                  31
```

Distribution:

```text
ECF00000 11   EF51FA00 1   EFF01700 2   EFF03600 1
EFF06E00  4   EFF07700 1   EFF0A500 1   EFF0C300 6
EFF21800  1   EPF20500 2   EPF32000 1
```

Opcode distribution:

```text
0x11  30
0x12   1
```

Each recipe records source owner, Switch-original header/control ownership, the containing PC-KO
window, Korean surface slice and SHA-256, trailing control boundary, identity policy, transform
order, final selective owner, and final-owner SHA-256.

Validation:

```text
membership uniqueness             PASS 31/31
disjoint from direct              PASS
surface slice/terminator          PASS 31/31
source header preservation        PASS 31/31
final owner alignment             PASS 31/31
direct-target internal overlap    0
composite pair overlap            0
```

## 6. Leading-control recovery family

Five composite rows form one common control-recovery cause family:

```text
ECF00000  p527  source 0xB0E44
ECF00000  p527  source 0xB122C
ECF00000  p664  source 0xD752C
EFF01700  p3    source 0x19D0
EFF0C300  p31   source 0xBFF4
```

All five preserve a Switch-owned leading 0x04 control and a 16-byte trailing control block. In the
PC-KO counterpart the first 12 trailing bytes remain byte-exact and only the final 4-byte branch
span changes. Therefore the product contract is:

```text
preserve Switch control ownership
+ recover PC-authored Korean surface
+ recompute relocation/branch span after layout
```

One additional composite row, `ECF00000 source 0xC22BC`, requires restoration of a Switch-side
leading literal byte `0x5C` before the PC-KO Korean surface. This is not an extra source owner.

## 7. Whole accounting replay

Exact set replay closes the top-level accounting:

```text
covered source owners                66,987
unaccounted source owners                 0
extraneous ledger owners                  0
direct/composite source overlap            0
ambiguous product bindings                 0
direct-target collisions                   0
composite/direct surface collisions        0
composite pair overlaps                    0
whole source-set equality                PASS
```

The V365 provisional top-level counts are therefore independently reproduced exactly.

## 8. Percent-root cross-carrier accounting

The EVENT corpus contains 50 syntactic percent-token types. `%04` and `%20` are previously closed
argument-bearing EVENT references rather than independent TAI5MSG roots. `%0C` and `%1F` are absent.
The independent runtime-root set is therefore exactly 48:

```text
syntactic token types              50
argument-reference non-roots       2   (%04, %20)
independent percent roots          48
uncovered independent-root owners   0
```

New V363-era roots are accounted as:

```text
%12  owners 1 / occurrences 1 / DIRECT / uncovered 0
%33  owners 4 / occurrences 4 / DIRECT / uncovered 0
```

Three independent-root owners (`%03` x2, `%05` x1) are composite rows; their final selective owner
recipes preserve the macro references.

## 9. Artifacts and storage policy

Git-resident compact artifact authority:

`artifacts/event_169_source_universe_v2_exact_ledger_reconstruction_v1/INDEX.json`

Large row ledgers are not intended for Git. They are bundled into the Drive archive named in the
INDEX with byte size and SHA-256 provenance. The archive contains ledgers and validation metadata,
not raw PC-KO EVENT payload files.

## 10. Rejected / do not repeat

- use the non-canonical `Taiko5DX/data/EVENT` installation-state folder as PC-KO source authority;
- download/rebuild the full 177 MB patcher when EVENT 169 is wholly recoverable from part00;
- use final PC-KO fresh grouping as source-owner authority;
- weaken direct-target uniqueness to accept an apparent collision;
- repair direct drift with isolated row overrides instead of partition-atomic reconstruction;
- treat PC-KO structural/control bytes as product authority for the 31 composites;
- treat the five leading-control rows as five unrelated one-off patches;
- count `%04/%20` as independent percent roots and inflate the root count to 50;
- claim full semantic replay or a universal runtime event_len gate without independent evidence.

## 11. Exact next scope

`EVENT_169_V366_RUNTIME_EVENT_LEN_AND_SEMANTIC_REPLAY_CLOSURE_READ_ONLY`

READ ONLY only. Use the exact V366 66,987-row accounting as frozen membership. Close only the
remaining universal runtime-length/command-boundary continuity gate and whole-family semantic
admission replay. Do not change source membership, direct/composite binding, product serializer,
EVENT/TAI5MSG bytes, build/package/IPS, or hardware unless a contradiction is proven and reported.
