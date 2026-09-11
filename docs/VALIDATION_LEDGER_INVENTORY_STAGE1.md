# VALIDATION LEDGER — Full-port inventory Stage 1

Date: 2026-09-11  
Scope: read-only canonical inventory/accounting run. No builder transformation, IPS generation, game-file edit, or runtime diagnostic build.

Detailed report: `docs/FULL_PORT_INVENTORY_STAGE1.md`

## V078 — canonical package identity and source denominators close exactly

**Status:** `VERIFIED`

Canonical input identities all matched:

- Switch `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`;
- Switch Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`;
- PC patch ZIP SHA-256 `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`;
- embedded `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`;
- T5K121R SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`.

Source denominators reproduced exactly:

```text
inline                 17,103
pointer                    56
mapping                 10,036
descriptor containers      11
descriptor subpatches      14
helper semantic entries     2
RomFS data items           208
```

Additional package facts reproduced:

- pointer mode 0 = 5;
- pointer mode 1 = 51;
- 47 distinct mode-1 replacement targets;
- pointer pool = 602 bytes;
- runtime helper = 158 bytes.

**Reuse rule:** These are the canonical source-accounting denominators for the full-port framework. No future selector may silently shrink them.

## V079 — RELA and three localization source tables inventory completely

**Status:** `VERIFIED`

Canonical Switch mapped-flat image:

- size `0xA20430` (`10,617,904`).

RELA census:

- total `40,410`;
- type 1027 / `R_AARCH64_RELATIVE` = `40,023`;
- type 257 = `377`;
- type 1025 = `10`.

The three R1 localization source tables each contain exactly 3,803 slots and every slot has exactly one relative relocation:

```text
JP: 3,803 / unique source objects 3,431
CN: 3,803 / unique source objects 2,933
TW: 3,803 / unique source objects 2,935
```

Missing/non-relative slots = `0`.
Duplicate relative relocations for one source slot = `0`.

Distinct source-object language ownership census:

```text
JP only       3,428
CN only       2,914
TW only       2,916
CN + TW          16
JP + CN + TW      3
```

**Limit:** This ownership census does not establish which language-copy block is selected on a particular runtime route.

**Reuse rule:** Future language-domain gates may reuse this complete source-table inventory instead of re-enumerating the 3,803 × 3 slots.

## V080 — Stage-1 inline discovery census is deterministic and confirms raw matching is insufficient

**Status:** `VERIFIED AS MEASUREMENT`

The 17,103 inline records contain 8,713 distinct original-byte patterns.

Per-PC-record raw Switch candidate cardinality, candidate lists capped at 64:

- 0 candidates = `187`;
- exactly 1 candidate = `6,053`;
- more than 1 candidate = `10,863`;
- records reaching the 64-candidate cap = `386`.

Stage-1 inline exception queue:

```text
E_MULTI_CANDIDATE        10,747
E_OBJECT_UNKNOWN            187
E_REPLACEMENT_CONFLICT      116
TOTAL                     11,050
```

Candidate occurrence measurements across all inline rows:

```text
STATIC_RODATA             111,017
CODE                       10,954
STATIC_DATA_OR_RELA_SLOT      786

JP_ONLY                     4,885
CN_ONLY                        12
TW_ONLY                         2
UNKNOWN                   117,858

PLACE_TABLE_NAME              515
PLACE_TABLE_YOMI              433
```

These are candidate-occurrence counts, not distinct source-item or final action counts.

The report set was emitted twice from the same canonical inputs and every report hash matched exactly. No input was mutated and no IPS/game-file output was emitted.

Complete report bundle retained in Drive `Test_Results`:

- ID `1ezUGzY_eTnGBjs_YgUuTs19Sc0AeqPKT`
- `canonical_inventory_stage1_reports_20260911.zip`.

**Interpretation:** raw occurrence uniqueness cannot be the full-port safety rule. Structural/family classification is required for the majority of the inline corpus.

**Reuse rule:** Do not interpret 11,050 discovery exceptions as 11,050 independent manual fixes. Apply verified structural rules corpus-wide and recount the residual exception population.

## V081 — unauthenticated GitHub Actions download is not a canonical private-Drive transport

**Status:** `REJECTED OPERATIONAL WORKAROUND`

A one-off GitHub Actions run (`34604986859`) attempted to retrieve the canonical Drive inputs using `gdown`.

It failed at the first Drive download because the file is private and no public link could be retrieved. Validator execution did not begin.

**Meaning:** This rejects only unauthenticated public-link download from GitHub runners. It is not evidence against the canonical inputs or validator.

**Reuse rule:** Do not repeat the `gdown` public-link approach unless Drive sharing policy intentionally changes.