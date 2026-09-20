# ECF00000 DIRECT_ESCAPE_PARTICLE_V1 implementation / offline validation — V349

Date: 2026-09-20 (KST)

```text
validation_id   V349
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          14270ba7ff6e32abd63e033a995c1f97780760f2 / V348
product_build   NONE
package/IPS     NONE
hardware        NOT RUN
```

V349 implements only the exact V348 `DIRECT_ESCAPE_PARTICLE_V1` applicability population.
It does not implement the 12 lexical false-positive code-5 rows, process copula-derived or
non-particle suffix morphology, promote the two mixed rows, build/package, create IPS, or run
hardware.

## 1. Canonical inputs and PC-patch provenance

```text
stock ECF00000.TS5
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09

PC-KO ECF00000.TS5
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe

V345 offline baseline
size    1,102,600
sha256  658d21cecbd038f39f89cf65e063d68861a481e96e73f530387c7133d46f3295
```

The PC-KO EVENT bytes were re-bound to the actual v1.02 PC patch payload before implementation:

```text
Taiko5DX_Korean_Patcher_v1.02.zip
sha256  df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec

embedded patcher executable
sha256  109dc729e66df8cd0a47c5f6c24719260eb03a89890a0c69d3ba739145dcfb23

embedded patch_payload.zip
sha256  eebc7aa18ff5811959ea02a4f5c45ed312a3327d00a6c1c99bf2565c788b11a2

patch_payload.zip/data/EVENT/ECF00000.TS5
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
```

Therefore the Korean EVENT source consumed by V349 is the actual PC-patch payload byte-for-byte,
not a reconstructed translation or guessed text source.

V348 exact authorities:

```text
APPLICABILITY.jsonl
sha256  7f2d632d3ccdcf9244c40b82f8b82714d048203bce7e88d0de9a1df532257097
rows    350

OCCURRENCES.jsonl
sha256  76593511a4886ad00f2bb57758e4fb86ef6378664163b8a700dda5f40b2d0575
rows    386
```

## 2. Implementation

New module:

`builder/selective_event_direct_particle.py`

New tests:

`tests/test_selective_event_direct_particle.py`

The implementation does not extend or mutate V345's exact 1,251-row dual-literal ledger.
It consumes the V348 JSONL authorities through a separate `DIRECT_ESCAPE_PARTICLE_V1` path.

Per row, the binding contract is:

```text
V348 row_id / partition / original_offset
-> exact stock original grouped item
-> current item must still equal that stock owner
-> V348 ko_offset + ko_command_length
-> raw exact slice from canonical PC-KO EVENT
-> exact message field
-> exact escape + exact source-particle bytes
-> expected raw-needle multiplicity must equal ledger multiplicity
-> ordered occurrence binding
-> 2-byte particle replacement only
```

Global standalone-particle replacement is not used.
Fresh reparsing of final Korean bytes is not owner authority.
`(row_id, escape)` alone is not treated as occurrence identity.

## 3. Exact transform result

```text
rows                          350
occurrences                   386
normalization candidate rows  108
substitutions                 117
raw PC-KO command bytes    24,068
transformed command bytes  24,068
particle-specific delta          0
```

Exact substitutions:

```text
은 -> 는    50
이 -> 가    45
을 -> 를    13
과 -> 와     9
------------
total      117
```

Canonical rowset SHA-256:

`295ba0bbed34d36bcca584646a08df42b3e61b38af0ea4c6f89880fecc2aad70`

Transformed-corpus SHA-256:

`01157230d52e5ae23ede0c03fc3eda5cc090540254b354e73d720fe5189980ee`

Although each particle transform is `2 bytes -> 2 bytes`, replacing the original JP commands
with their Korean commands changes the 350 command payloads by an aggregate `+5,584` bytes.
This is why EVENT relocation and structural validation remain mandatory.

## 4. Baseline-state and raw-locator gates

All 350 V348 target items were still exact stock bytes in the V345 diagnostic baseline:

```text
V345 target baseline mismatch   0 / 350
```

Every V348 occurrence was rebound from the raw canonical PC-KO row slice:

```text
raw locator failures            0 / 386
unexpected raw-needle count     0
source-byte mismatches          0
edit collisions                 0
```

Repeated identical escapes are accepted only when the exact field-local source-needle
multiplicity equals the V348 ledger and the ordered occurrences bind one-for-one.

## 5. Unit validation

```text
canonical V348 ledger SHA/counts             PASS
corrupted applicability SHA rejection        PASS
repeated identical escape binding            PASS
unexpected extra same needle rejection       PASS
synthetic exact application                   PASS
unauthorized pre-existing mutation rejection PASS
--------------------------------------------------
unit                                           PASS_6_OF_6
```

## 6. Exact whole-context implementation replay

Integration baseline:

```text
V345 offline diagnostic
+ V349 exact direct-escape 350
+ V337 generic relocation
+ V338 special spans
+ V339 5A runtime target gate
+ V344/V345 state-aware residual gate
```

Output:

```text
size                 1,108,184
sha256               a175e64b2f52e1735b25e2b3e8c4453c36913416b893e4ebd569d8110de69d5e
delta vs V345        +5,584
simulation replay    PASS_BYTE_EXACT
deterministic rerun  PASS_BYTE_IDENTICAL
```

The implementation-generated output is byte-for-byte identical to the independent V348
pre-implementation diagnostic harness result.

## 7. Mutation accounting and structural gates

Compared with V345:

```text
changed grouped items            632
target payload items             350
non-target changed items         282
  generic relocation owners      281
  Switch special-span owners       1
unexpected non-target changes      0
```

Inherited gates:

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

Only the first V338 special owner changes relative to V345 because the V349 growth falls within
that source-proven span. The other two remain byte-identical to V345.

## 8. State-aware residual gate

Raw conservative observations:

```text
original 0xBDD78  -> current 0xE306C   1 observation   decoded 0x7F5408
original 0xC3740  -> current 0xE99E0   2 S/F observations   decoded 0x1A7400
```

Gate result:

```text
candidate observations       3
unique logical residuals     2
inherited stock              1
source-proven alias           1
novel                         0
blocking                   false
```

`0xBDD78` remains the V340 inherited stock MAY-model artifact.
`0xC3740` remains the exact V344 `NOVEL_ALIAS_ELIGIBLE` `0x0B + 4 -> 0x0E` source-proven alias.
Current candidate bytes still match the canonical parent/alias headers exactly.
No blanket residual whitelist is introduced.

## 9. Drive archival mirror

Git remains canonical authority. Drive is an archival mirror.

```text
folder
1lHZrAJnnlmtvpXN4vLJXO-GacmfRIq1L

diagnostic TS5
19LtkSfFjd9MLNXh9DDQ8cdADuoqHRCtm

validation JSON
1fiKZoiUkVZYn3ish0yELUJ7KZToOEj4T

implementation module
1c6glNM04ATtVLZvtLNbi7crJQMzMe-d5

test module
1QzkIxvPxV1CdI0n9SYvfLWHge-des3hX
```

## 10. Rejected / do-not-repeat

Reject:

- append the 350 rows to V345's 1,251-row dual-literal ledger;
- route direct single particles through the V345 `6 -> 2` transform;
- treat V348 decoded character offsets as raw byte offsets;
- bind repeated escapes by `(row_id, escape)` alone;
- accept fewer or more raw source-needle occurrences than the ledger expects;
- globally replace standalone Korean particles;
- skip generic/special relocation because the particle bytes themselves are length-neutral;
- interpret the `+5,584` whole-row growth as particle-replacement growth;
- treat `0xC3740` as a novel blocker without the V344 alias provenance check;
- promote either mixed row or any copula/suffix row through this implementation.

## 11. Current disposition / next scope

```text
V345 fixed-surface dual-literal         IMPLEMENTED / OFFLINE PASS
V348 direct-escape policy               CLOSED
V349 direct-escape implementation       IMPLEMENTED / OFFLINE PASS
code-5 direct-particle-only             350 IMPLEMENTED
code-5 lexical false-positive            12 INCLUDE_KO / NOT IMPLEMENTED
code-5 copula-derived-only               59 DEFER
code-5 mixed                              2 DEFER
code-5 non-particle suffix                3 DEFER
product build/package/IPS/hardware      NONE
```

Effective V334 product-admission overlay remains:

```text
INCLUDE_KO             12,533
DEFER                       64
NON_KOREAN_TARGET          478
TOTAL                    13,075
```

The admission count is unchanged by implementation; V349 changes implementation coverage only.

Exact next scope after a fresh explicit user signal:

`ECF00000_CODE5_LEXICAL_FALSE_POSITIVE_12_IMPLEMENTATION_OFFLINE_VALIDATION`

Implement only the exact 12 V346 `LEXICAL_FALSE_POSITIVE_GAMUN` rows already admitted as
`INCLUDE_KO`. Reuse their exact original/PC-KO row bindings and inherited EVENT structural gates.
Do not process the 59 copula rows, two mixed rows, three suffix rows, build/package/IPS, or run
hardware without another fresh authorization.
