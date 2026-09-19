# ECF00000 NESTED-AWARE REPRESENTATIVE RANGE VALIDATION — V329

Date: 2026-09-19 (KST)

```text
validation_id   V329
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_VALIDATION_CHECKPOINT
parent          66faa9a99dee99280188b2d5049a9bebaa0222a5 / V328
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint validates the V328 handler-grounded recursive-child traversal on a bounded representative range only. It does not perform the full 782-entrypoint replay.

## 1. Representative range

```text
entrypoints  253..290
count        38
```

The V327 outer-only baseline for exactly this owner range was cross-checked against the persisted chunk03 diagnostic artifact.

```text
outer path occurrences   300
outer unique targets     297
artifact match           PASS EXACT
```

The comparison baseline is therefore provenance-consistent with V327.

## 2. Nested-aware result

Applying the V328 recursive-child rules while preserving the parent outer continuation produced:

```text
                         outer-only   nested-aware   delta
target path occurrences       300           348       +48
unique physical targets       297           324       +27
0x11                          217           237       +20
0x12                            7             7         0
0x13                           71            77        +6
0x15                            2             3        +1
```

No previously visible outer target was lost.

```text
lost outer targets   0
nested errors        0
recursive edges     25
max recursion depth  2
```

## 3. Known missing-target recovery

The V328 proof targets were recovered automatically by the general recursive rule.

```text
parent 0x90150
entrypoint root 253

0x90158   absent outer / present nested-aware
0x901AC   absent outer / present nested-aware
```

No special-case insertion was used.

## 4. Large nested representative

Parent `0x9DAE0` is reached from entrypoints 289 and 290.

```text
child start            0x9DAE4
nested unique targets       21
outer-only membership        0 / 21
nested-aware membership     21 / 21
errors                       0
```

All 21 targets previously omitted by the outer-only ledger are recovered by the V328 rule.

## 5. Validation conclusion

The representative validation is PASS.

It proves, for this bounded range, that:

- the V328 handler-grounded recursive-child rule recovers real V327-missing target commands;
- the existing outer population is preserved;
- nested recursion deeper than one level is exercised successfully;
- recursive child traversal and parent outer continuation coexist correctly;
- physical-offset dedup does not explain the earlier deficit;
- special-casing the known missing offsets is unnecessary.

This checkpoint does not yet prove the full V324 4,444-target aggregate.

## 6. Rejected / do-not-repeat

Rejected for this range:

- nested traversal causes loss of outer targets;
- the V327 comparison baseline is parser-incompatible;
- `0x90158` / `0x901AC` require manual recovery;
- the 21 targets under `0x9DAE0` require one-off logic;
- recursion is only one level deep;
- the V327 deficit is caused by chunk partitioning or deduplication.

## 7. Artifact

Machine-readable validation artifact:

```text
Google Drive/GPT/태합입지전/ECF00000_V329_REPRESENTATIVE_VALIDATION/
ecf_v328_nested_aware_validation_ep253_290.json

folder id  12LRfTSSXJZcFC3wRdDRDkCIksPcyLmNv
file id    18tm8o5IGb30tY6aOSqDMM5mMMGzKR6rl
size       8.4 KiB
SHA-256    e68424c413dc10e04b3192a9234c559435a4b4d2a1775c481bc8e104b3964f4e
```

## 8. Impact boundary

Unchanged:

- V324 aggregate target counts;
- V325 Mapping/font/glyph closure;
- V326 admission aggregates;
- V327 diagnostic subset;
- V328 recursive-child rules;
- product bytes;
- serializer/build/package/IPS;
- TAI5MSG/B24;
- SNR.

The exact 4,444-row ledger and exact 4,123/115 row membership remain blocked until full nested-aware reconstruction is run.

## 9. Exact next scope

After a fresh explicit execution signal:

`ECF00000_NESTED_AWARE_FULL_LEDGER_RECONSTRUCTION_READ_ONLY`

Required gates:

```text
physical targets   4,444
messages           4,193
choices              251
Korean targets     4,238
INCLUDE_KO         4,123
UNRESOLVED           115
```

The full replay must use V328 handler-grounded recursion, active/self-cycle guards, parent outer continuation, and final physical-offset dedup.

Do not implement a serializer, rewrite EVENT payloads, build/package/IPS, or broaden to other EVENT files/SNR inside that replay.
