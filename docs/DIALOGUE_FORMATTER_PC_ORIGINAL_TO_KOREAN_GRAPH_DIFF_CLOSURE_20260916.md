# Dialogue Formatter PC Original -> Korean Graph Diff Closure

Date: 2026-09-16 (KST)
Scope: `DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_READ_ONLY`
Status: CANONICAL READ-ONLY ANALYSIS CLOSURE
Implementation authorization: NONE
Build authorization: NONE
New WRITE_SAFE authorization: 0
New validation ID: NONE

## 1. Purpose

This document materializes the completed issue-C comparison between the PC original
`TAI5MSG_JP.DAT` formatter graph and the canonical PC Korean-patched v1.02
`TAI5MSG_JP.DAT`.

The comparison answers the exact closure question recorded in `PROJECT_STATE.md`:

1. whether condition/predicate expressions changed;
2. whether lower-message call IDs / graph edges changed;
3. whether branch/default/empty-output topology changed;
4. whether only output fragments changed.

This is an analysis artifact only. It does not authorize a Switch patch, diagnostic
build, runtime-state modification, or sentence-level translation edit.

## 2. PC_PATCH_ORACLE_GATE

`PC_PATCH_ORACLE_GATE=PASS`

Actual PC evidence used:

- PC original `TAI5MSG_JP.DAT`
  - size: `1,810,889` bytes
  - SHA-256: `aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f`
- canonical PC Korean-patched v1.02 `TAI5MSG_JP.DAT`
  - size: `2,134,366` bytes
  - SHA-256: `e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090`
- canonical patcher reconstruction guard in `builder/tai5msg.py` uses the same patched
  input SHA-256 `e3b4522a...` and the established `33 blocks / 14,832 messages` identity.

The PC original file was sourced from the project Google Drive `PC_Original` corpus.
The Korean-patched file was extracted from the canonical v1.02 patch package payload.

## 3. File / structure identity

Observed structural population:

```text
PC original:
  blocks                 33
  total messages     14,832
  block 0 messages      471

PC Korean v1.02:
  blocks                 33
  total messages     14,832
  block 0 messages      471
```

Block 0 is the centralized speech-style / address / copula / verb / interrogative
formatter family already identified by canonical issue-C evidence.

## 4. Block-0 graph comparison result

All `471` block-0 messages were compared at the control/graph layer separately from
literal output text.

Observed block-0 content-level change:

```text
messages with byte/content changes    366
messages byte-identical               105
TOTAL                                 471
```

Observed graph/control comparison:

```text
message graph/control skeleton identical    471 / 471
message graph/control skeleton changed        0 / 471
```

The closure analysis observed `14,590` control/graph events across block 0 and found
the corresponding event sequence/value structure preserved between PC original and
PC Korean v1.02.

Observed event-family counts used by the comparison:

```text
condition / branch markers       5,611
runtime/state references         5,121
comparators                      2,199
boolean operators                  452
lower-message calls              1,182
  0x4A family                      965
  0x43 family                      217
```

The corresponding lower-message call IDs / edges were preserved.

The control-event interval topology was also preserved: regions that were empty
outputs versus literal-output regions remained in the same graph positions. The
Korean patch changes output fragments inside the preserved graph rather than
redesigning the graph itself.

## 5. Exact closure matrix

| Comparison axis | Result |
|---|---|
| condition / predicate expressions | PRESERVED |
| lower-message call IDs / graph edges | PRESERVED |
| branch/default topology | PRESERVED |
| empty-output topology | PRESERVED |
| literal/output fragments | CHANGED where translation requires |

Therefore the PC Korean patch does **not** introduce a Korean-specific formatter
graph redesign for this family.

## 6. Confirmed facts

- The malformed-ending issue C is not explained by a missing PC-original -> PC-Korean
  formatter graph transformation.
- The Korean patch relies on the original formatter control graph and substitutes
  Korean output fragments within that graph.
- The current Switch `TAI5MSG` reconstruction does not intentionally rewrite block-0
  formatter semantics; canonical compact-byte reconstruction targets other affected
  blocks and preserves unaffected raw blocks.
- Sentence-by-sentence Korean rewriting is not a valid root-cause repair for this
  family.
- Font/glyph and Mapping 10,036 remain outside the primary cause family.

## 7. Rejected / superseded hypotheses

The following remain rejected and must not be repeated absent contradictory evidence:

- `0x01 prefix unsupported` as a proven C root cause;
- local sentence-by-sentence translation correction;
- global runtime-state normalization;
- font/mapping as the primary cause;
- Stage1 `storage_mutability=CODE` count as formatter-code-patch count.

Newly rejected by this closure:

- **PC Korean formatter graph redesign missing on Switch**.

Reason: the PC original and PC Korean block-0 graph/control structure is preserved
across all 471 messages while output fragments change.

## 8. Root-cause consequence

The decision rule from the prior canonical state selects its first branch:

```text
PC original -> PC Korean preserves graph/conditions
AND changes output fragments
=> next root-cause layer:
   PC-vs-Switch runtime state / predicate semantic parity
```

This does not yet prove which state field, producer, evaluator, domain, or call-time
value is wrong on Switch.

## 9. Next read-only question

Next scope:

`DIALOGUE_FORMATTER_PC_SWITCH_PREDICATE_STATE_PARITY_READ_ONLY`

The next analysis must remain PC-patch-first and should bind the representative
malformed paths back to the exact block-0 predicate/state references, then compare:

1. predicate expression identity/semantics;
2. state/reference field semantic ownership;
3. value domain and producer;
4. evaluation timing / call context;
5. PC behavior versus Switch-native counterpart.

No field inversion, forced state value, global normalization, code patch, diagnostic
build, or translation change is authorized by this document.

## 10. Impact boundary

The result applies to the shared block-0 formatter family, not only the two currently
observed malformed strings. Any analogous malformed honorific/copula/verb/interrogative
composition using the same graph family must be investigated through the shared
predicate/state path before local patching.

## 11. STOP boundary

This materialization closes only
`DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_READ_ONLY`.

The next predicate/state parity analysis requires a fresh explicit user execution
signal after this canonical materialization is reported.
