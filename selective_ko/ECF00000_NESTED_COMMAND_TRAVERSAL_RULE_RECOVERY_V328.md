# ECF00000 NESTED COMMAND TRAVERSAL RULE RECOVERY — V328

Date: 2026-09-19 (KST)

```text
validation_id   V328
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CHECKPOINT
parent          b14dcc1ec64af4da7d53935c61d2f5770592fc82 / V327
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint closes the root cause behind the V327 2,817-row outer-path subset and recovers the bounded nested EVENT traversal rule required to reconstruct the V324 4,444-target census.

## 1. Root cause

The simple V327 walker followed only the outer execution line:

```text
current command
-> handler returned length
-> p += length
-> next outer command
```

This is incomplete for ECF00000.

Selected EVENT opcode handlers recursively call the EVENT interpreter `0x15F2C0` on an address inside the current command payload. Those child streams can contain visible target commands `0x11/0x12/0x13/0x15`.

Therefore a complete structural census requires both:

```text
recursive child traversal
+
parent total-length outer continuation
```

The V327 outer walker performed only the second step and therefore skipped the nested target population.

## 2. Proven recursive-child opcode families

Bounded Switch handler analysis established the following recursive child starts and parent lengths.

| opcode | child stream start | parent total length |
|---|---|---|
| `0x01` | `p + 4` | `(word >> 6) & 0x3FFFFFC` |
| `0x02` | `p + 4` | `(word >> 6) & 0x3FFFFFC` |
| `0x05` | `p + 4` | `(word >> 17) & 0x7FFC` |
| `0x06` | `p + 8` | `(word >> 7) & 0x1FFFFFC` |
| `0x08` | `p + 4` | `(word >> 14) & 0x3FFFC` |
| `0x0C` | `p + ((word >> 10) & 0x3C)` | `(word >> 14) & 0x7FC` |
| `0x0D` | `p + ((word >> 10) & 0x3C)` | `(word >> 14) & 0x7FC` |
| `0x0E` | `p + 4` | `(word >> 6) & 0x3FFFFFC` |
| `0x0F` | `p + 4` | `(word >> 6) & 0x3FFFFFC` |

The decisive criterion is not command size. The criterion is whether the Switch handler actually invokes `0x15F2C0` on an internal pointer.

Do not generalize recursive traversal to every length-bearing opcode.

## 3. Newly closed length rules

The prior incomplete diagnostic walker used incorrect default 4-byte handling for two opcode families.

Closed:

```text
0x01 -> same parent-length family as 0x02 / 0x0E / 0x0F
0x0C -> same parent-length family as 0x0D
```

These corrections are structural parsing rules only. No product bytes are changed.

## 4. 0x06 child start

For opcode `0x06`, the handler processes the condition/expression beginning at `p+4` through helper `0x1704F4`, then adds the helper-consumed size plus four bytes before the recursive interpreter call.

For the bounded handler path, the helper returns four bytes on the relevant exits.

Therefore:

```text
0x06 child start = p + 8
```

This is closed for the recovered traversal rule and is not left as an unknown offset.

## 5. Direct missing-target reproduction

Representative parent:

```text
parent       0x90150
opcode       0x08
parent len   360
child start  0x90154
outer next   0x902B8
```

The child stream contains at least:

```text
0x90158  opcode 0x11
0x901AC  opcode 0x11
```

Both target offsets are absent from the V327 2,817-row outer-path ledger.

Their payloads are ordinary PC-Korean EVENT surfaces, including Korean dialogue/choice text. This directly proves that V327 skipped real product-relevant target commands rather than only opaque internal metadata.

A larger representative:

```text
parent             0x9DAE0
opcode             0x08
parent length      8,340
child start        0x9DAE4
child NUL          0x9E8A4
outer continuation 0x9FB74
nested targets     21
```

All 21 child target commands are absent from the V327 outer ledger.

This is sufficient to prove the missing-population mechanism without rerunning all 782 entrypoints.

## 6. Nested recursion depth

Nested traversal is not limited to one child level.

A representative `0x0E -> 0x0F -> internal stream` relation demonstrates that a child stream may itself encounter another recursive-container opcode.

Therefore the structural census requires recursive traversal with physical-address cycle guards and deduplication.

## 7. Cycle / self-edge guard

For `0x0C/0x0D`, the encoded child delta can resolve to zero.

A static census must not recurse indefinitely when:

```text
child_start == parent_start
```

Required guard:

- track active recursive physical starts;
- suppress self-edge or already-active recursion;
- preserve the parent command itself and continue using the parent total length;
- deduplicate final target commands by physical offset.

This is a census safety rule, not a gameplay rewrite.

## 8. Correct traversal model

The recovered structural traversal is:

```text
visit parent command
-> record parent physical command
-> if handler is a proven recursive-child family:
     compute child start by opcode-specific rule
     recursively walk child stream until its NUL
     allow nested recursive families inside the child
-> independently advance outer pointer by parent total handler length
-> continue outer stream until NUL
-> globally deduplicate target commands by physical offset
```

Both the child recursion and the outer continuation are required.

Runtime branch predicates may determine which path executes in one play session. The product census must not discard structurally present child text merely by choosing one runtime predicate outcome.

## 9. Rejected / do-not-repeat

Rejected:

- a pure `p += handler_length` walker is sufficient for V324 census reconstruction;
- all length-bearing commands should be recursively decoded;
- raw scanning inside every large command is an acceptable substitute for handler-grounded traversal;
- `0x0A/0x0B` being length-bearing proves that they are recursive child containers;
- V327's missing 1,627 targets are caused by chunk splitting;
- V324's 4,444 aggregate should be discarded before nested-aware replay;
- `0x06` child start remains unknown;
- `0x01` and `0x0C` should retain the old default 4-byte diagnostic length.

The recursive-child family must remain grounded in actual Switch handler behavior.

## 10. Relationship to V327

V327 remains valid diagnostic evidence:

```text
OUTER_PATH_SUBSET        2,817 physical targets
canonical V324 aggregate 4,444 physical targets
deficit                  1,627
```

V328 explains why V327 is a strict subset.

V328 does not yet claim that a full nested-aware replay reproduces 4,444. That whole-corpus validation has not been run in this checkpoint.

## 11. Related impact boundary

Unchanged:

- V324 Switch/PC-original carrier parity;
- V325 Mapping 10,036 and 907/907 glyph closure;
- V326 4,123 INCLUDE / 115 UNRESOLVED aggregate claims;
- fixed-particle and identity policies;
- Korean font / page mapper;
- TAI5MSG/B24;
- SNR.

Still blocked:

- exact 4,444 physical-command ledger materialization;
- exact 4,123 serializer-input row membership;
- exact 115-row semantic-adjacency closure;
- EVENT selective serializer implementation.

No gameplay bytes, builder, package, IPS, or runtime artifact is changed by V328.

## 12. Exact next scope

After a fresh explicit execution signal:

`ECF00000_NESTED_AWARE_REPRESENTATIVE_RANGE_VALIDATION_READ_ONLY`

Bounded representative range:

```text
entrypoints 253..290
```

Required checks:

1. use the V328 recursive-child rules;
2. retain the ordinary outer continuation;
3. apply physical-address cycle guards;
4. collect target commands by exact physical offset;
5. confirm automatic recovery of known V327-missing targets including `0x90158`, `0x901AC`, and the nested target population under `0x9DAE0`;
6. compare nested-aware vs V327 outer-only counts for this representative range;
7. stop after the representative proof.

Do not:

- rerun all 782 entrypoints;
- implement a production parser/serializer;
- rewrite EVENT payloads;
- build/package/IPS;
- broaden to other EVENT files or SNR.
