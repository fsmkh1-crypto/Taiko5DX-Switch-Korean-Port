# ECF00000 SELECTIVE COMMAND ADMISSION CLASSIFICATION — V326

Date: 2026-09-19 (KST)

```text
validation_id   V326
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CHECKPOINT
parent          5bd285eb32c119a8795f768d64b219f0dc2b5275 / V325
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint classifies the bounded ECF00000 Korean command population admitted by V325 infrastructure closure. It does not implement an EVENT serializer or alter gameplay bytes.

## 1. Population

V325 Korean-bearing command population:

```text
Hangul no-escape message commands      2,891
Hangul choice commands                   251
Hangul escape/control message commands 1,096
---------------------------------------------
total Korean target commands           4,238
```

The 144 control/binary-style message records from V325 remain outside this Korean target population and must be preserved structurally, not decoded as ordinary text.

## 2. Switch runtime escape/control responsibility

The backslash-prefixed EVENT forms are runtime syntax, not ordinary literal decoration.

Bounded Switch runtime evidence:

```text
message string
-> 0x156D80
-> recognize 0x5C ('\\')
-> decode escape kind / argument
-> obtain or format runtime value/control state
-> append into scratch output string
-> normal message rendering path
```

Observed escape surface families include `\#`, `\%`, `\A`, `\B`, `\C`, `\D`, `\E`, `\G`, `\M`, numeric forms, `\&`, `\>`, and `\=`.

Within this bounded path, the escape layer is a runtime value/control expansion layer. No general Korean particle, copula, ending, honorific, speech-style, or interrogative selection responsibility was established in this path.

Do not generalize this into semantic names for all 278 unique escape surface forms. Full per-form game-world semantics are not required merely to decide Korean morphology responsibility.

## 3. Command disposition

### 3.1 No-escape Korean messages

```text
population       2,891
disposition      INCLUDE_KO
```

These messages directly contain the Korean surface payload and have no backslash expansion population from V325. Mapping/font/container structure is already closed by V324/V325.

They are treated as static-complete candidates for this bounded admission decision. Exact 0x11/0x12/0x13 UI-role naming remains separate and does not reopen text-carrier admission.

### 3.2 Choice commands

```text
choice commands   251
choice strings    504
2-choice          249
3-choice            2
escape strings      0
disposition       INCLUDE_KO
```

Branch presence alone is not an unsafe condition. These choice surfaces are complete selectable strings and contain no unresolved runtime escape/control population.

### 3.3 Escape/control Korean messages

Starting population:

```text
1,096
```

Subdivision:

```text
explicit dual-particle messages          243
particle-risk detector hits              118
overlap: dual-particle + detector           3
detector-only unresolved                 115
remaining grammar-invariant expansion    738
---------------------------------------------
total                                   1,096
```

#### Explicit dual-particle messages

```text
population    243 messages
occurrences   287
disposition   INCLUDE_KO
surface rule  FIXED_SURFACE_PARTICLE_V1
```

The mechanism/risk provenance is retained. Applying the canonical fixed-particle release surface does not relabel the structural mechanism as ordinary VARIABLE_INSERT.

#### Grammar-invariant runtime expansion/control

```text
population    738
disposition   INCLUDE_KO
```

For this bounded set, the runtime escape/control layer contributes values/control expansion, while the Korean sentence surface responsibility is already present in the PC-Korean payload and no remaining V325 particle-risk detector is present.

Runtime person/place identity remains Japanese under `IDENTITY_IN_PROSE_V1`. That token policy does not force the surrounding Korean command to KEEP_JP.

#### Detector-only particle-risk set

```text
population    115
disposition   UNRESOLVED
```

The current detector only proves escape/control adjacency to a particle-family Korean surface. It does not distinguish a true grammatical particle from a Korean lexical prefix/word continuation.

Known false-positive shape:

```text
\#0276가문
```

Here `가` can be the first syllable of the lexical word `가문`, not a particle.

Therefore these 115 must not be bulk-classified as PARTICLE_SENSITIVE_INSERT or DEFER_KO without semantic adjacency closure.

## 4. Aggregate disposition

```text
INCLUDE_KO    4,123
UNRESOLVED      115
DEFER_KO          0
KEEP_JP           0
BLOCKED           0
---------------------
TOTAL          4,238
```

INCLUDE_KO decomposition:

```text
2,891  no-escape messages
  251  choice commands
  243  explicit dual-particle messages
  738  grammar-invariant runtime expansion/control messages
----------------------------------------------------------
4,123
```

Current admission closure:

```text
4,123 / 4,238 = 97.28% admitted
115 / 4,238   = 2.71% unresolved
```

Percentages are descriptive only; exact command counts remain authoritative.

## 5. Shared physical target commands

V324/V325 facts remain:

```text
shared physical target commands   20
Hangul-bearing                    20
escape/control-bearing             2
explicit dual-particle-bearing     1
```

Path-vs-physical census shows:

```text
0x11 shared revisits  14
0x12 shared revisits   3
0x13 shared revisits   2
0x15 shared revisit    1
-------------------------
total                 20
```

Shared physical ownership does not create an additional blanket unresolved population here. Static literal and complete-choice commands have the same physical surface responsibility wherever reached. Dynamic members remain governed by the escape/control and particle-risk classification above.

If a shared command belongs to the 115 detector-only unresolved set, it is already counted there and must not be double-counted.

## 6. Product consequence

The ECF00000 content-admission blocker is now narrowed to one cause-family:

```text
escape-adjacent particle semantic ambiguity   115 commands
```

Not current blockers:

- Mapping 10,036;
- Korean font glyph availability;
- page mapper;
- PUA;
- EVENT file growth/carrier;
- the 1,096 escape/control population as a whole;
- Japanese runtime identity by itself;
- shared physical target commands by themselves.

Whole-file exact PC-KO replacement remains not authorized because the product is selective and 115 commands remain unresolved. The selected route remains reconstruction from the Switch structure with admitted PC-Korean payloads.

## 7. Rejected / do-not-repeat

Rejected:

- all backslash escapes are unresolved grammar formatters;
- all 1,096 escape/control Korean messages must be deferred;
- every one of the 118 particle detector hits is a real grammatical particle;
- shared physical target status alone requires all 20 commands to be deferred;
- Japanese runtime identity means the entire surrounding Korean message must remain Japanese;
- all 278 unique escape forms require full semantic reverse engineering before command admission;
- absence of backslash syntax alone proves all possible caller semantics globally, beyond this bounded ECF00000 admission decision.

## 8. Remaining layout / implementation boundary

This checkpoint closes content admission only for the classified population.

Still separate:

- EVENT layout/reflow QA under the 714 px / three-visual-line renderer behavior;
- production EVENT serializer design;
- fixed-particle byte rewriting and offset/length regeneration;
- deterministic reconstruction;
- diagnostic package/build/runtime validation;
- unrelated EVENT files;
- SNR.

No implementation is authorized by V326.

## 9. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_PARTICLE_RISK_115_SEMANTIC_ADJACENCY_CLOSURE_READ_ONLY`

Inspect exactly the 115 detector-only rows and classify each as one of:

```text
LEXICAL_FALSE_POSITIVE
TRUE_PARTICLE_RISK
EXPLICITLY_RESOLVABLE
```

Then derive the canonical product disposition:

- lexical false positive -> `INCLUDE_KO`;
- true unresolved particle responsibility -> `DEFER_KO` with a concrete revisit condition;
- explicitly resolvable -> apply only an already-authorized canonical policy whose exact applicability gate is proven.

Do not:

- implement a serializer;
- rewrite EVENT bytes;
- build/package;
- broaden to the other 981 escape/control Korean messages;
- expand to other EVENT files or SNR.
