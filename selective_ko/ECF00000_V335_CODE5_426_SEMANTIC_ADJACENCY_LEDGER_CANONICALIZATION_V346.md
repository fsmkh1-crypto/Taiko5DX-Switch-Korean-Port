# ECF00000 V335 code-5 426 semantic-adjacency ledger canonicalization — V346

Date: 2026-09-20 (KST)

```text
validation_id   V346
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      LEDGER_MATERIALIZATION_AND_REPLAY_VALIDATION
parent          1354bd3a09656fc38be366214e261127d79e987e / V345
product_bytes   UNCHANGED
implementation  NONE
build/package   NONE
hardware        NOT RUN
```

## 1. Scope

V346 materializes the immediately preceding READ ONLY classification of the exact V335
`UNRESOLVED_PARTICLE_RISK` / code-5 population. It does not implement any code-5 row.

Exact source population:

```text
rows             426
detector hits     466
opcode 0x11       299
opcode 0x12         7
opcode 0x13       120
```

The 426 rows are exact members of the V334 source universe and V335 semantic-admission
artifact. V346 does not reclassify any CLOSED V344/V345 fixed-surface row.

## 2. Exact semantic partition

```text
DIRECT_PARTICLE_ONLY              350
COPULA_DERIVED_ONLY                59
MIXED_DIRECT_AND_DERIVED_RISK       2
LEXICAL_FALSE_POSITIVE_GAMUN       12
NON_PARTICLE_SUFFIX_ADJACENCY       3
--------------------------------------
total                              426
```

The hit-level cause-family census is:

```text
DIRECT_PARTICLE                    389
COPULA_DERIVED_MORPHOLOGY           62
LEXICAL_FALSE_POSITIVE_GAMUN         12
NON_PARTICLE_SUFFIX_ADJACENCY         3
--------------------------------------
total detector hits                466
```

## 3. Product disposition

Binding V346 product disposition:

```text
INCLUDE_KO
  LEXICAL_FALSE_POSITIVE_GAMUN      12

DEFER
  DIRECT_PARTICLE_ONLY             350
  COPULA_DERIVED_ONLY               59
  MIXED_DIRECT_AND_DERIVED_RISK      2
  NON_PARTICLE_SUFFIX_ADJACENCY      3
--------------------------------------
DEFER total                         414
```

The 12 INCLUDE_KO rows are false positives of the old detector: the apparent `가` is
the first syllable of lexical `가문`, not a post-value Korean subject particle. This is a
semantic-admission correction only. V346 does not materialize those 12 rows into a product TS5.

Exact row IDs:

```text
6383 6408 8526 8543 11056 11759 11788 12355 12370 13045 13048 13064
```

## 4. Direct-particle cause family

Across the 350 pure-direct rows plus the two mixed rows, exact direct-particle occurrences:

```text
가   104
는    81
은    50
를    47
이    46
와    27
을    15
로    10
과     9
--------
total 389
```

This corrects a minor transcription error in the prior conversational summary. The prior total
`389` was correct; V346 binds the exact row-level counts above.

These occurrences remain DEFERRED because V345's fixed-surface implementation is limited to
the exact V344 dual-literal ledger. A direct literal immediately after a runtime escape requires
a separate runtime-responsibility/admission proof.

## 5. Copula / derived morphology cause family

The 59 pure rows plus two mixed rows contain 62 derived-morphology occurrences.

Observed surfaces include:

```text
이었다        10
이었으나       8
이라는        7
이라면        5
이다         3
이라         3
이니         3
이야말로       2
이네         2
이지         2
이오         2
와의         2
이었지만       2
이여         2
이야         1
이라고        1
이신가        1
로군         1
이셨군요       1
이란         1
이시옵니다      1
이군         1
이었나        1
```

Examples include forms such as `이었다`, `이었으나`, `이라는`, `이라면`, `이니`,
`이야말로`, and `와의`.

These are not V344 fixed dual-particle literals and must not be routed through
`FIXED_SURFACE_PARTICLE_V1`.

## 6. Non-particle suffix adjacency

Three exact rows are detector false positives of a different type:

```text
row 4743   \%21 + 는 것도 ...
row 5059   없\%15 + 는데 ...
row 11440  보\%2A + 는 건 ...
```

The detected `는` belongs to verbal/ending morphology, not a noun particle attached to a
runtime-inserted identity/value. They remain DEFERRED to an ending/formatter-responsibility
cause family.

## 7. Canonical ledger

Compact ledger:

`selective_ko/artifacts/ecf00000_v346_code5_semantic_adjacency_v1/LEDGER_COMPACT.bin`

```text
records        426
record size     24 bytes
serialization  <IHIIBBBBHHH
sha256         9ca57b03d70d3fc031e9c7d955dd4a90cdea292b2e1fe6e2069373b5c9975ffd
```

Fields:

```text
row_id
partition
original_offset
ko_offset
opcode
class_code
product_code
hit_count
original_command_length
ko_command_length
reserved
```

Class codes:

```text
1 DIRECT_PARTICLE_ONLY
2 COPULA_DERIVED_ONLY
3 MIXED_DIRECT_AND_DERIVED_RISK
4 LEXICAL_FALSE_POSITIVE_GAMUN
5 NON_PARTICLE_SUFFIX_ADJACENCY
```

Product codes:

```text
1 INCLUDE_KO
2 DEFER
```

Human-readable exact ledger:

`LEDGER.jsonl`

SHA-256:

`52b5533e8db3221d9ee8ace6c0e9b3151a80a4b35cb1500a44171a6092281b49`

## 8. READ ONLY diagnostic membership provenance

The source READ ONLY diagnostic is preserved byte-exact in the artifact directory.

SHA-256:

`c6463acefa960cf61892ef631ce6759bdb35af387a8fe65411f299af5d82b6e8`

Its previously reported membership hashes are preserved in `INDEX.json`; they are diagnostic
membership provenance, while the V346 compact ledger and rowset binaries are the canonical
serialized representation.

## 9. Rejected / do-not-repeat

Reject:

- treat all 426 code-5 rows as one fixed-particle family;
- treat every escape-adjacent `가` as a subject particle;
- keep the 12 `가문` rows unresolved;
- send copula/derived forms through V345 fixed-surface logic;
- treat rows 4743 / 5059 / 11440 as noun-particle adjacency;
- promote any of the remaining 414 rows merely because V345 fixed-particle output passed;
- modify V345's exact 1,251-row ledger to absorb code-5 rows without a new policy authority.

## 10. Current disposition / next scope

```text
V345 fixed-surface particle                CLOSED / IMPLEMENTED
V346 code-5 exact semantic ledger          MATERIALIZED
code-5 INCLUDE_KO                          12 / NOT IMPLEMENTED
code-5 DEFER                              414
  direct-particle-only                    350
  copula-derived-only                      59
  mixed                                     2
  non-particle suffix                       3
product/build/package/IPS                  NONE
```

Exact next scope after a fresh explicit user signal:

`ECF00000_CODE5_DIRECT_PARTICLE_RUNTIME_RESPONSIBILITY_READ_ONLY`

READ ONLY only. Investigate the direct-particle cause family (350 pure rows plus direct
occurrences in the 2 mixed rows) against actual runtime escape responsibility and PC-patch
behavior. Do not implement those rows, process copula-derived morphology, promote the mixed
rows, build/package/IPS, or run hardware without a fresh authorization.
