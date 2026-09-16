# KO Grammar Register Normalize 125 Static-Write Authorization — V288

Date: 2026-09-17 (KST)
Status: CANONICAL STATIC-WRITE AUTHORIZATION CLOSURE
Validation ID: `V288`
Scope: `KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_MATERIALIZATION`
Implementation authorization: NONE
Build authorization: NONE
New WRITE_SAFE authorization: 125 rows

## 1. Authority and inherited state

This closure inherits the canonical state at:

```text
base main HEAD = dcf52f08a0d52ba3aff604cf4bfc8d14aa4bdfcd
base tree      = 42b0ac78eab0c9ff3dd813e6b8586e8a6b2d87b1
last closed validation = V287
```

V272-V287, FZ001, prior WRITE_SAFE authority, rejected hypotheses, and unrelated
project queues remain valid unless explicitly superseded below.

`PC_PATCH_ORACLE_GATE=PASS`.

The canonical PC Korean v1.02 TAI5MSG input remains:

```text
size    = 2,134,366
sha256  = e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
blocks  = 33
messages= 14,832
```

The V285 exact 125-caller membership and responsibility classes, V286 target wording
authority, and V287 single-transaction reconstruction design are not re-censused or
re-adjudicated by V288.

## 2. Materialized exact authorization manifest

Canonical artifact set:

```text
index path      = selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json
index bytes     = 2,977
index sha256    = 587464c402538b31ffc10c4726e953f5c54b33cfd92f6fd9c14cd37de27c7a00
row shards      = 4
rows            = 125
manifest-set id = a17b5b493a4f529e6aa308954242434e13bede0dda14b075cc13a3a890bc254c
```

Ordered row shards:

```text
ROWS_00.json  rows  0..31   bytes 8,661  sha256 ecd3f1b4849257b4c2f38899578902c041d705f82eaad5f5274b1c8def4700a0
ROWS_01.json  rows 32..62   bytes 9,281  sha256 5bfdcea52fcbd17a13c1edffa410694598cb014b1f150ff9ae51ee51a83b6e2c
ROWS_02.json  rows 63..93   bytes 9,853  sha256 777fdf0264f3299d03fd9516278ab2ea27630807d78a5d15c19acc95601dc529
ROWS_03.json  rows 94..124  bytes 8,974  sha256 22016ac476a8e448993c8d1c10754a240bd7cca2b720edb6833ff11e4b864f9b
```

The index carries the canonical input identity, V285-V287 authority summary, row schema,
global closure checks, per-block final padding, the ordered shard list, and every shard
hash. The manifest-set identity is the SHA-256 of the four ordered shard SHA-256 strings
joined with newlines.

The row shards are a compact machine-action projection of the full analysis
serialization. They omit redundant full source/target message dumps and detailed rebuilt
offsets. Source identity remains exact through locator + source length + SHA-256. Each
row stores deterministic source-coordinate edit spans, exact replacement bytes for those
spans, target length/SHA-256, grammar removal accounting, preserved non-register call
sequence, and control fingerprint. Applying the edits to the guarded canonical source
deterministically reproduces the exact target bytes. Each row is promoted to `WRITE_SAFE`
by V288.

Pre-materialization analysis serialization provenance:

```text
bytes   = 221,602
sha256  = 4ec5e7ecde94fe502b01dc5f64ca60946347d8b477afe22f32cd7aa0106a92e2
```

## 3. Exact row-level closure

The manifest binds every row to:

- `(block_index, local_message_index)`;
- canonical source message locator, length, and SHA-256 guard;
- deterministic source-coordinate edit spans and exact replacement bytes;
- exact target message length and SHA-256 identity;
- grammar family and exact removal count;
- target grammar residual count;
- preserved non-register call sequence;
- control/branch fingerprint;
- fixed-block capacity result through the indexed per-block final-padding ledger;
- V288 authorization state.

Closed totals:

```text
manifest rows                         125
unique locators                       125
source unique hashes                  122
target unique hashes                  122

CALL_ERASURE_ONLY                      99
CALLER_ENDING_MATERIALIZE              17
CALLER_PHRASE_REWRITE                   6
BOUNDARY_JOIN_NORMALIZE                 3

grammar calls removed                 177
target grammar residual                 0
preserved non-register calls          125
non-register sequence mismatches        0
control/branch mismatches               0

grammar logical byte delta           -645

UNKNOWN                                 0
UNRESOLVED                              0
CONFLICT                                0
```

The three duplicated source-content pairs remain unambiguous because authorization
identity is locator + exact source guard, not hash alone:

```text
5:476  = 8:384
13:3   = 13:162
13:4   = 13:163
```

## 4. Capacity and deterministic whole-file replay

All 125 target messages reparse at their expected logical locators.

```text
grammar125 ∩ compact33                   0
combined changed messages              158
combined affected physical blocks       17
grown blocks                              0
block count after                        33
message count after                  14,832
file size after                   2,134,366
header block pairs identity            PASS
whole header bytes identity            PASS
minimum remaining affected padding  13 bytes

compact occurrences                     44
compact protected after                  44
compact unprotected after                 0
```

Three independent same-input replays were byte-identical.

Authorized deterministic reconstructed identity:

```text
sha256 = 993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06
```

This exactly reproduces the V287 analysis candidate identity.

## 5. Failed/rejected variant provenance

Do not normalize unrelated pre-existing punctuation while applying this grammar family.

A tested variant that normalized the existing `...` / `......` bytes in callers
`6:211` and `21:458` to the typography used in the human-readable V286 wording ledger
produced grammar delta `-101` instead of the required `-93` for the non-erasure tranche
and failed to reproduce the V287 deterministic whole-file identity.

Therefore those pre-existing punctuation bytes are outside this cause-family mutation
and remain preserved. V286 wording notation is semantic/readability authority, not a
license to change unrelated source punctuation.

All previously rejected global repeated-syllable cleanup, family-wide formatter
blanking, treating all 125 as erasure-only, SC/TW wording authority, global 0x6A
normalization, and two-pass intermediate serialization remain rejected.

## 6. WRITE_SAFE authorization

V288 grants exact static-write authorization to the 125 rows in the materialized
manifest and to no other population.

Explicit project WRITE_SAFE authority becomes:

```text
F1 DIRECT_PORT        158
Mapping                 4
grammar125            125
TOTAL                  287
```

This is an authorization/accounting closure only.

V288 does **not** authorize or perform:

- builder modification;
- TAI5MSG gameplay-data mutation;
- build or diagnostic build;
- IPS generation;
- hardware/runtime test;
- unrelated formatter/runtime/CWTDAT/name/yomi changes.

## 7. Required implementation architecture

Any later implementation must consume the canonical PC Korean input once:

```text
parse canonical input once
-> verify exact 125 source guards from the V288 manifest
-> apply exact 125 target messages
-> apply existing compact-byte preservation
-> rebuild affected message-offset tables once
-> preserve fixed physical block sizes
-> encrypt once
-> verify deterministic output SHA-256
```

The grammar-modified-intermediate -> current canonical-input serializer two-pass route
remains forbidden.

## 8. Next scope / STOP

The next eligible scope, under a fresh explicit execution signal, is:

`KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILDER_IMPLEMENTATION_NO_BUILD`

That scope may implement the already-authorized manifest into the builder, but must not
perform a build, IPS generation, or hardware validation. Those remain separate stages.

V288 ends here.
