# ECF00000 SELECTIVE EVENT NO-OP SERIALIZER CORE IMPLEMENTATION / OFFLINE VALIDATION — V336

Date: 2026-09-20 (KST)

```text
validation_id   V336
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          d0f22893001b9a42981afb83dd529d05b76427b2 / V335
product_bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

V336 implements only S1 of the staged EVENT serializer plan: a no-op `ECF00000.TS5` serializer core that reproduces the PC editor v0.30 edit-partition/grouping model, rebuilds the count/offset table from unchanged partitions, and proves a zero-replacement byte-exact round trip. It does not implement generic branch relocation, Switch dynamic-span exceptions, V334/V335 Korean replacement, particle rewriting, build/package, or runtime execution.

## 1. Input authority

Switch v1.1.3 / PC-original `ECF00000.TS5`:

```text
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09
count   782
offsets 783
first   0xC44
last    0xE3860 = EOF
```

PC editor authority remains V331 plus the preserved v0.30 source provenance. V334 `GENERATOR.py` remains a read-only grouping oracle for this validation; V334/V335 exact source membership and semantic admission are not consumed for any replacement in S1.

## 2. Implemented module

```text
builder/selective_event.py
```

Implemented in S1:

- guarded TS5 count/offset-table parsing;
- `offset[i]..offset[i+1]` edit-partition materialization;
- exact PC editor `CombineDialogueBytes` grouping behavior needed by V331/V334;
- textish `11/12/13/1E` grouping traps;
- ordinary/disguised `15` handling;
- false-`04` guards:
  - `16/17/18 + 04`;
  - `0B xx 17 00 + 04 00`;
  - `04 00 xx 0E + 04 00 yy 0E`;
- `5A` and `3C` grouped-string handling;
- byte-preservation and grouped-item contiguity assertions;
- deterministic count/offset-table reconstruction from partition payloads;
- no-op serializer/report CLI.

Not implemented in V336:

- `02/04/06/07/08/09` branch-field relocation;
- `0xFDC04 / 0x7F7A8 / 0x9DAE4` Switch dynamic-span handling;
- `0xD7008 / 0xBDC58` special-owner logic beyond inherited design authority;
- V334/V335 replacement application;
- `FIXED_SURFACE_PARTICLE_V1` transformation;
- EVENT layout/reflow;
- package/build/IPS.

## 3. Unit validation

Repository tests:

```text
tests/test_selective_event.py
```

Fresh Python execution:

```text
tests run   8
passed      8
failed      0
status      PASS_8_OF_8
```

Covered unit families:

- synthetic parse/rebuild identity;
- textish grouping and branch trap;
- disguised `15`;
- ordinary choice merge and forced-break form;
- all three false-`04` guard families;
- `5A` / `3C` grouped-string handling;
- misaligned partition rejection;
- stock header geometry.

Python compile check also passed for the new module and test.

## 4. V334 grouping-oracle cross-check

The V334 canonical ZIP's exact `GENERATOR.py` was used only as an independent read-only oracle after implementation.

For every stock partition:

```text
partitions compared       782 / 782
item-count mismatches       0
item-start mismatches       0
item-byte mismatches        0
disguised-15 mismatches     0
guard-merge mismatches      0
status                      PASS_EXACT_782_OF_782
```

This establishes that the new core reproduces the already-canonical V334 editor-grouping implementation for the complete original file rather than only passing synthetic fixtures.

Observed stock grouping diagnostics from the new core:

```text
grouped items          69,285
target-looking items   15,951
disguised 0x15             65
16/17/18 + 04 guards       837
0B17 + 0400 guards          32
04000E pair guards          38
```

These stock counts are V336 diagnostics. They do not replace V331's separate PC-Korean editor-grouping census.

## 5. Zero-replacement identity gate

The exact stock file was parsed, all 782 edit partitions materialized/grouped, and the TS5 header/count/offset table/payloads rebuilt without replacements.

Result:

```text
input size    931,936
output size   931,936
input sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09
output sha256 bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09
byte compare  IDENTICAL
status        PASS_BYTE_EXACT
```

Therefore S1 closes the container/grouping/no-op reconstruction cause-family.

## 6. Scope boundary

V336 proves only:

```text
stock TS5
-> exact editor edit partitions
-> exact grouping replay
-> unchanged partition serialization
-> rebuilt global offset table
-> stock bytes exactly reproduced
```

It does not prove that any length-changing replacement is safe. In particular, no branch field has yet been recalculated after a payload-size change.

## 7. Rejected / do-not-repeat

Do not:

- treat V336 no-op PASS as proof of generic relocation;
- add Korean replacement rows before the relocation engine is independently closed;
- infer runtime ownership from the edit partitions;
- replace original-PC grouping authority with final-Korean fresh parsing;
- mix the three Switch dynamic-span exceptions into the generic relocation validation stage;
- build/package/IPS from this S1 core.

## 8. Current disposition

```text
S1 no-op serializer core             IMPLEMENTED
S1 unit validation                   PASS_8_OF_8
S1 V334 grouping oracle              PASS_EXACT_782_OF_782
S1 zero-replacement identity rebuild PASS_BYTE_EXACT
branch relocation engine             NOT IMPLEMENTED
Switch dynamic-span exceptions       NOT IMPLEMENTED
V334/V335 selective replacement      NOT IMPLEMENTED
product bytes / build / package      NONE
```

## 9. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_SELECTIVE_EVENT_GENERIC_RELOCATION_ENGINE_IMPLEMENTATION_OFFLINE_VALIDATION`

S2 only:

- implement ordinary PC-editor `02/04/06/07/08/09` relocation arithmetic from original edit ownership;
- use synthetic/controlled length-change fixtures and deterministic offline validation;
- keep the three Switch-specific dynamic-span owners out of the generic pass;
- do not apply V334/V335 Korean replacements;
- no build/package/IPS/hardware.
