# ECF00000 FIXED_SURFACE_PARTICLE_V1 implementation / offline validation — V345

Date: 2026-09-20 (KST)

```text
validation_id   V345
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          9b47c02b9edcc7d83c4b3f3d9160806258ead60d / V344
product_build   NONE
package/IPS     NONE
hardware        NOT RUN
```

V345 implements only the exact V344 `FIXED_SURFACE_PARTICLE_V1` applicability ledger. It does not promote the 21 pending `0x1E` rows, resolve V335 code-5 rows, resume unrelated S4 families, build/package, create IPS, or run hardware.

## 1. Canonical inputs

```text
stock ECF00000.TS5
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09

PC-KO ECF00000.TS5
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe

V344 particle ledger
rows    1,251
sha256  b6d228b6b1e8e23285763b88d5d5eda6064153433123283217c4ea955d550a4d
```

## 2. Implementation

New module:

`builder/selective_event_particle.py`

New tests:

`tests/test_selective_event_particle.py`

The module consumes the exact V344 23-byte compact ledger and applies only the approved exact dual-form literals:

```text
은(는) -> 는
이(가) -> 가
을(를) -> 를
과(와) -> 와
와(과) -> 와
(으)로 -> 로
```

Every replacement is `6 bytes -> 2 bytes`, therefore `-4 bytes` per occurrence.

Canonical totals:

```text
rows                         1,251
occurrences                  1,389
code-3 rows                  1,226
choice-overlap rows             25
raw PC-KO command bytes      94,092
transformed command bytes    88,536
aggregate shrink              5,556
```

Exact literal counts:

```text
은(는)   521
이(가)   395
을(를)   358
과(와)    41
와(과)    51
(으)로    23
```

Transformed-corpus SHA-256:

`f86a4f49f18c741445dcf9fc69390b818be5feba7f256973a9a69cdbd33368c5`

## 3. Baseline-state gate

The particle layer does not silently overwrite arbitrary current bytes.

```text
semantic code 3
  current item must still equal original JP owner

semantic code 2 / choice overlap
  current item must already equal exact raw PC-KO choice owner
```

Any other pre-existing mutation fails.

This preserves the current S4 ordering contract while keeping particle applicability independent from the V335 single semantic-detail axis.

## 4. PC-KO ownership correction discovered during implementation

The first implementation attempt attempted to resolve each `ko_offset` through a fresh parse/grouping of the final PC-KO file.

That failed at canonical V334 special binding `ko_offset 0x16828`.

Root cause:

- V334 already fixes exact original -> KO offsets/lengths, including fresh-reparse drift bindings;
- final-Korean fresh grouping is explicitly not ownership authority;
- a V345 particle implementation must consume `ko_offset + ko_length` as raw exact PC-KO bytes from the canonical ledger, not rediscover the owner by reparsing final Korean bytes.

Binding implementation:

```text
ledger ko_offset / ko_length
-> raw slice from exact canonical PC-KO blob
-> verify opcode / length
-> transform only parsed message/choice string ranges
```

The rejected fresh-PC-KO-grouping approach is recorded in `KNOWN_FAILURES.md`.

## 5. Unit regression

Repository EVENT tests after adding the particle module:

```text
V336/V337/V338 core tests     16
V342 1E tests                  5
V339 5A tests                  6
V345 particle tests            6
V344 validator tests           8
--------------------------------
total                         41 / 41 PASS
```

Particle tests cover:

- canonical ledger SHA/counts;
- corrupted-ledger rejection;
- all six approved surface forms;
- multi-choice field preservation;
- code-3 JP baseline + choice raw-KO baseline routing;
- unauthorized pre-existing mutation rejection.

## 6. Exact whole-context implementation replay

Integration context:

```text
V335 code 1 / 2 / 4 base application
+ V345 exact particle 1,251
+ V342 1E ready-23
+ V339 5A
+ V337 generic relocation
+ V338 special spans
+ V344 source-aware residual validator
```

Output:

```text
size    1,102,600
sha256  658d21cecbd038f39f89cf65e063d68861a481e96e73f530387c7133d46f3295
```

This is byte-for-byte identical to the V344 READ ONLY particle simulation.

```text
V344 simulation equivalence      PASS_BYTE_EXACT
deterministic second replay      PASS_BYTE_IDENTICAL
```

## 7. Structural gates

```text
V337 generic plans               7,579 / PASS
V338 special spans                   3 / PASS
V338 false EVENT-02                  2 / PASS
V339 5A mapping                  1,088
V339 translated 5A              1,074
V339 5A violations                  0
baseline walker errors               0
```

V342 `0x1E` remains:

```text
ready rows                         23
ready growth                       +8
unauthorized pre-existing mutation  0
```

## 8. V344 state-aware alias gate

Raw conservative observations:

```text
0xBDD78    1 observation
0xC3740    2 S/F observations
```

Gate result:

```text
candidate observations             3
unique logical residuals           2
inherited stock                     1
source-proven alias                 1
novel                               0
blocking                         false
```

The `0xC3740` residual remains accepted only through the exact V344 source-aware alias proof. No blanket alias whitelist is introduced.

## 9. Canonical output boundary

The V345 TS5 is an offline diagnostic implementation output only. It is preserved in Drive for exact replay evidence but is not a packaged product/build/IPS artifact.

```text
product package     NONE
IPS                 NONE
hardware            NOT RUN
```

## 10. Rejected / do-not-repeat

Reject:

- final-PC-KO fresh grouping as owner authority;
- resolving `ko_offset` by reparsing Korean bytes instead of exact ledger slicing;
- applying particle policy only to semantic code 3;
- omitting 25 choice-overlap rows;
- accepting arbitrary pre-existing mutations on particle rows;
- global standalone-particle substitution;
- bypassing V344 source-aware residual proof after layout changes.

## 11. Current disposition / next scope

```text
V344 particle applicability / validator     CLOSED
V345 particle serializer                    IMPLEMENTED / OFFLINE PASS
V345 exact output equivalence               PASS_BYTE_EXACT
V345 EVENT regression                       PASS_41_OF_41
1E runtime pending                          21
V335 code-5 unresolved particle-risk       426
full S4                                      NOT CLOSED
build/package/IPS                            NONE
```

Exact next scope after a fresh explicit user signal:

`ECF00000_V335_CODE5_426_SEMANTIC_ADJACENCY_CLOSURE_READ_ONLY`

READ ONLY only. Classify the exact V335 code-5 / 426-row unresolved particle-risk population against actual PC-KO text/escape adjacency and runtime responsibility. Do not implement those rows, promote the 21 pending `0x1E` rows, build/package/IPS, or run hardware in that scope.
