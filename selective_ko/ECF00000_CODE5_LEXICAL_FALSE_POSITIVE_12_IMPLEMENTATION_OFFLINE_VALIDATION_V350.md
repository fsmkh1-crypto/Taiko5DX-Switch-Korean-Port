# ECF00000 code-5 lexical false-positive 12 implementation / offline validation — V350

Date: 2026-09-20 (KST)

```text
validation_id   V350
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          4dca2a4165c31e4c6a56ab7f149a406bdb105a93 / V349
product_build   NONE
package/IPS     NONE
hardware        NOT RUN
```

V350 implements only the exact 12 V346 `LEXICAL_FALSE_POSITIVE_GAMUN` rows already admitted as
`INCLUDE_KO`. It does not process the 59 copula-derived rows, two mixed rows, three non-particle
suffix rows, build/package, create IPS, or run hardware.

## 1. Canonical source population

V346 exact row IDs:

```text
6383 6408 8526 8543 11056 11759 11788 12355 12370 13045 13048 13064
```

Every row has exactly one old-detector hit with:

```text
class      LEXICAL_FALSE_POSITIVE_GAMUN
surface    가문
product    INCLUDE_KO
```

The apparent `가` is not a post-value subject particle. It is the first syllable of lexical
`가문`. Therefore no particle normalization or runtime-josa policy is applied in V350.

V346 canonical membership provenance:

```text
INCLUDE_KO_12_ROWSET.bin
size    192
sha256  2e3b5b7981ee6b096a3dcc971fb5169cc8ff691c15f98132ef088e8cb07a4014
```

V350 exact implementation applicability:

`selective_ko/artifacts/ecf00000_v350_code5_lexical_false_positive_v1/APPLICABILITY.jsonl`

```text
rows    12
sha256  d0c6bf82792f1edbcc04363205c7b11f0ce11293ebb3c8dffa56761aa0b87edd
```

The V350 applicability reconstructs the V346 12-row rowset byte-exact and additionally binds per
row:

- partition;
- exact original and PC-KO offsets;
- opcode and command lengths;
- exact escape surface;
- exact stock command SHA-256;
- exact PC-KO command SHA-256;
- command growth.

## 2. PC patch source authority

V350 reuses the PC-KO EVENT source already byte-bound in V349 to the actual PC v1.02 patch
payload:

```text
PC-KO ECF00000.TS5
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
source  patch_payload.zip/data/EVENT/ECF00000.TS5
```

No translation text is guessed or reconstructed. Each of the 12 commands is sliced from the
canonical PC patch bytes using its exact V346 `ko_offset + ko_command_length` binding.

## 3. Implementation

New module:

`builder/selective_event_code5_lexical.py`

New tests:

`tests/test_selective_event_code5_lexical.py`

The implementation is deliberately separate from both particle paths:

```text
V345 FIXED_SURFACE_PARTICLE_V1        dual-literal transform
V349 DIRECT_ESCAPE_PARTICLE_V1        direct single-particle transform
V350 LEXICAL_FALSE_POSITIVE_GAMUN     exact raw PC-KO command overlay
```

For every V350 row:

```text
V350 exact applicability row
-> exact stock partition/original owner
-> current item must still equal exact stock command
-> verify stock command SHA-256
-> exact canonical PC-KO offset/length slice
-> verify opcode/length
-> verify PC-KO command SHA-256
-> copy the raw PC-KO command unchanged
```

There is no search/replace of `가`, no josa normalization, no fresh final-Korean grouping, and no
semantic widening beyond the exact 12-row authority.

## 4. Exact payload result

```text
rows                    12
opcode 0x11              4
opcode 0x13              8
stock command bytes     756
raw PC-KO bytes         956
payload growth         +200
```

The exact raw-overlay transformed-corpus SHA-256 is:

`fd3cdc3ee1d3dfff2d17db762598913979ce80605d51b2d90b3d1b201985bca2`

The 12-row canonical rowset SHA-256 remains:

`2e3b5b7981ee6b096a3dcc971fb5169cc8ff691c15f98132ef088e8cb07a4014`

## 5. Baseline and binding gates

All 12 rows remain exact stock owners after the V349 direct-particle layer and before inherited
structural relocation is applied.

The implementation rejects:

- a non-canonical applicability artifact;
- a current item already mutated away from its stock owner;
- original command hash mismatch;
- PC-KO command hash mismatch;
- wrong opcode or command length;
- wrong V346 exact rowset;
- any row outside the exact 12-row applicability.

## 6. Unit validation

```text
canonical exact applicability          PASS
corrupted applicability SHA reject     PASS
synthetic raw PC-KO replacement        PASS
unauthorized baseline mutation reject  PASS
PC-KO command hash mismatch reject     PASS
-------------------------------------------
unit                                   PASS_5_OF_5
```

## 7. Whole-context offline replay

Integration order:

```text
V345 offline baseline
+ V349 exact direct-escape 350
+ V350 exact lexical false-positive 12
+ V337 generic relocation
+ V338 Switch special spans
+ V339 5A runtime target gate
+ V344/V345 state-aware residual gate
```

V349 baseline:

```text
size    1,108,184
sha256  a175e64b2f52e1735b25e2b3e8c4453c36913416b893e4ebd569d8110de69d5e
```

V350 output:

```text
size    1,108,384
sha256  bedd0cd3b367e3caed4f7d06adc6b3ecfb607d0152d8329f830eb6de98411ff2
delta   +200
```

A deterministic second replay is byte-identical.

## 8. Mutation accounting

Relative to V349:

```text
changed grouped items             25
target payload items              12
non-target changed items          13
  generic relocation owners       13
  Switch special-span owners       0
unexpected non-target changes      0
```

Thus every non-target byte change is owned by the already-established generic relocation family.
No unrelated command is changed.

## 9. Inherited structural gates

```text
V337 generic plans             7,579 / PASS
V338 special spans                 3 / PASS
V338 false EVENT-02                2 / PASS
V339 5A mapping                1,088
V339 translated 5A            1,074
V339 original-target          1,058
V339 choice-next-start           15
V339 zero-next-terminator          1
V339 5A violations                0
baseline walker errors             0
```

The two false EVENT-02 expression headers remain byte-identical to the V349 baseline.

## 10. State-aware residual gate

```text
candidate observations       3
unique logical residuals     2
inherited stock              1
source-proven alias           1
novel                         0
blocking                   false
```

The logical identities remain unchanged:

- partition 593 / original `0xBDD78` / opcode `0x0E` / decoded `0x7F5408`: V340 inherited stock
  MAY-model artifact;
- partition 604 / original `0xC3740` / opcode `0x0E` / decoded `0x1A7400`: V344 exact source-proven
  alias.

V350 only relocates their current addresses as expected from the additional +200 bytes. It does
not create a new logical residual.

## 11. Rejected / do-not-repeat

Reject:

- interpret the `가` in these 12 rows as a Korean subject particle;
- route these rows through V345 fixed-surface dual-literal logic;
- route these rows through V349 direct-escape particle normalization;
- modify `가문` to satisfy a particle detector;
- discover the 12 rows again from a fresh final-Korean grouping;
- broaden the raw-KO overlay to other V346 code-5 classes;
- process the 59 copula rows, two mixed rows, or three suffix rows in V350;
- skip EVENT relocation because the semantic issue is only a lexical false positive;
- build/package/IPS or run hardware in this scope.

## 12. Current disposition / next scope

```text
V349 direct-particle-only             350 IMPLEMENTED / OFFLINE PASS
V350 lexical false-positive            12 IMPLEMENTED / OFFLINE PASS
code-5 currently admitted total       362 IMPLEMENTED / OFFLINE PASS
code-5 copula-derived-only             59 DEFER
code-5 mixed                            2 DEFER
code-5 non-particle suffix              3 DEFER
remaining code-5 DEFER                 64
product build/package/IPS/hardware   NONE
```

Effective V334 product-admission counts do not change:

```text
INCLUDE_KO             12,533
DEFER                       64
NON_KOREAN_TARGET          478
TOTAL                    13,075
```

Exact next scope after a fresh explicit user signal:

`ECF00000_CODE5_COPULA_DERIVED_RUNTIME_RESPONSIBILITY_READ_ONLY`

READ ONLY only. Investigate the 59 pure `COPULA_DERIVED_ONLY` rows plus the derived-morphology
occurrences in the two mixed rows as one cause family, using actual PC-patch bytes and Switch
runtime responsibility. Do not implement them, process the three non-particle suffix rows,
build/package/IPS, or run hardware without another fresh authorization.
