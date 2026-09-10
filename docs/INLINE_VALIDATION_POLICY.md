# INLINE VALIDATION POLICY

Normative policy for mapping the PC `T5K121R` inline replacement records to Nintendo Switch v1.1.3.

This is a project-level invariant. Any agent working on inline text mapping, validation, IPS generation, or crash diagnosis must follow it unless new measured evidence causes an explicit recorded revision.

## 0. Mandatory prerequisite: Phase 0

Do **not** begin the full 17,103-record semantic validator solely because the historical inline set failed.

First follow `docs/PHASE0_FAILURE_MODE_PLAN.md` to distinguish candidate-specific failures from systemic IPS/build/runtime prerequisites. The first runtime control is P0N: the proven NO-INLINE baseline plus 5,519 true no-op inline IPS records.

Only after Phase 0 clears the architecture should the full validator become the main line of work.

## 1. Core premise

The previous rule, "an original byte pattern occurs exactly once in Switch `main` rodata, therefore it is safe to patch", is **not a safety proof**.

`unique exact match` may be used only to discover candidate locations. It must never, by itself, authorize a patch.

A distributable inline patch requires strong evidence across these axes:

1. valid game-specific encoding/control structure;
2. PC-to-Switch structural correspondence;
3. independently established Switch-side object/field/boundary structure;
4. no unresolved conflict, tail-merge, or binary-data risk;
5. successful simulated post-patch validation and emitted-IPS round trip.

Runtime success is a sanity check, not proof of safety.

## 2. Runtime evidence that motivated this policy

Established Eden Android observations:

- add-on disabled: normal boot/run;
- `v0.2b NO-INLINE` = 207 RomFS replacements + Korean font + page mapper + zero inline: boots and displays `태합입지전 V DX`;
- historical 5,519 inline set: freezes;
- v0.2c with one suspicious record removed: still fails;
- address-half A: freezes;
- address-half B: reaches title, then crashes/exits after button input.

Do not overstate these facts as "any inline set fails". Multiple candidate faults and systemic prerequisites remain distinguishable hypotheses until Phase 0 resolves them.

## 3. Scope and units

Long-term validator target: all `17,103` PC inline records, not only the old 5,519 selector output.

Canonical source counts:

- PC inline records: `17,103`;
- distinct original patterns: `8,713`;
- original mapping entries: `7,494 (0x1D46)`;
- Korean additions: `2,542`;
- expanded mapping entries: `10,036 (0x2734)`.

Always distinguish:

- record count;
- unique-pattern count;
- Switch candidate-location count.

For source identity and already-verified measurements, consult `docs/VALIDATION_LEDGER.md` before rerunning anything.

## 4. Input identity gate

PC-RVA neighborhood/homology evidence may use a PC executable only if its exact size and SHA-256 match the T5K target identity.

A matching file-version string is insufficient.

Current exact T5K target:

- Steam 1.2.1.0 build 9163702;
- size `18,685,960`;
- SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`.

The currently supplied Drive PC EXE does not match and is barred from PC-binary-context evidence.

## 5. Validation pipeline

### Stage 0 — Normalize records

Assign stable record/pattern IDs and preserve:

- record ID;
- pattern ID;
- PC RVA;
- record length;
- original bytes;
- replacement bytes.

### Stage 1 — Encoding/control validation

Use the game's measured mapping/code rules, not generic Shift-JIS as the authoritative decoder.

Validate original and replacement byte streams completely. Encoding validity is necessary but never sufficient for proving text identity.

Control-code policy:

- derive the whitelist from an independent trusted corpus such as confirmed event text or strongly established text objects;
- freeze the whitelist before candidate classification;
- do not automatically expand the whitelist from the same uncertain inline corpus being classified;
- preserve code type/order/count and any confirmed parameter bytes/semantics.

Unknown/malformed code sequences cannot be SAFE.

### Stage 2 — Enumerate all Switch candidates

Search every original pattern across Switch `main`; do not force uniqueness.

Segment treatment:

- `.text`: excluded from ordinary inline text patching;
- `.rodata`: primary target;
- `.data`: excluded from auto-patching, but **retained as an analysis/evidence source** for pointers/relocations/arrays.

Known mapping tables and confirmed non-text regions are excluded from ordinary inline patching.

Where language-specific rodata regions can be established reliably, prefer JP-region candidates and reject/hold CN/TW-only candidates. Do not invent language boundaries from weak heuristics; record unknown/shared regions explicitly.

### Stage 3 — Build structural evidence sources

Use independent evidence with explicit strength levels. Strong sources may include:

- NSO relocation/reference data that demonstrates an object start or pointer target;
- pointer/offset arrays in `.data`/`.rodata`;
- repeated fixed-stride arrays;
- clear NUL/string-boundary patterns;
- direct/indirect XREF or use-site behavior;
- neighboring confirmed text objects.

Relocation/XREF evidence is strong positive/negative evidence, not a universal requirement. Lack of direct XREF does not reject an indirectly referenced string.

### Stage 4 — Tail-merge / string-pooling / many-to-one audit

Perform this against the **rodata-wide string/object inventory**, not only the candidate set.

Detect at minimum:

- candidate beginning inside a larger known string/object;
- true suffix/tail sharing;
- prefix/subsequence relationships;
- multiple PC records resolving to one Switch object;
- one Switch range receiving incompatible replacements.

A many-to-one mapping with conflicting PC replacements is HOLD unless the semantic equivalence is independently proven. Never pick a replacement by arbitrary longest/first rule.

Candidate-start-not-after-NUL is a risk signal, not an unconditional rejection because fixed-width/pool structures exist; use object-start evidence and inventory context.

### Stage 5 — Independently infer Switch field/object structure

Never assume PC record length equals Switch field width.

Classify where possible as:

- NUL-terminated string;
- fixed-width text field;
- fixed-stride array entry;
- string-pool entry;
- structure member;
- shared/tail-merged object;
- unknown.

Evidence ordering should favor stronger structural proof over text density. Inspect neighboring entries as a group rather than inferring field type from one candidate.

Important ambiguity:

- `text + NUL + alignment padding` can resemble a fixed-width field;
- a single sample cannot reliably distinguish them.

If the array/object model cannot be established, keep the candidate out of auto-SAFE.

### Stage 6 — Piecewise/local PC↔Switch homology

Use `(PC RVA, Switch offset)` relations to identify local monotonic blocks.

Do **not** use one global LIS as a release gate. Global LIS is only a diagnostic/reference statistic.

Block evidence should consider both:

- relative order; and
- distance/spacing consistency.

Allow block reordering between PC and Switch. Collinearity is one strong path to confidence, not the only path: strong independent structural evidence can support a candidate in a reordered region.

Track anchor coverage by region so anchor-poor UI/name tables become explicit blind spots rather than silently disappearing from coverage.

### Stage 7 — Establish anchors

ANCHOR records require the strongest available independent evidence. Length alone is not enough.

Prefer anchors with:

- confirmed object start/field structure;
- relocation/pointer/reference evidence when available;
- high information content;
- unambiguous candidate location;
- no tail-merge/conflict risk;
- coherent local block context.

An anchor may support neighboring candidates but must never bootstrap its own correctness circularly from those candidates.

### Stage 8 — Resolve multi-match candidates

For a repeated pattern, a candidate may be recovered inside a confirmed local block only when ambiguity is actually removed.

Recommended hard gates:

1. candidate in the bounded local block is uniquely determined after exclusions;
2. surrounding anchors are independently strong;
3. local PC/Switch order is coherent;
4. relative spacing is consistent with the block;
5. selected location independently passes field/object structure checks;
6. selected range has no competing assignment/conflict.

If two plausible positions remain, HOLD. Do not choose the nearest or first candidate merely to increase coverage.

A recovered multi-match candidate cannot become ANCHOR on the basis of the same block that resolved it.

### Stage 9 — Boundary / terminator / stride preservation

A replacement consuming PC NUL/padding is not automatically invalid.

Switch-side semantics control the decision:

- confirmed fixed-width field: full-width replacement may be valid;
- confirmed NUL-terminated field: a valid terminator must remain within the field;
- unknown structure: no automatic SAFE if replacement removes apparent termination/padding.

Do not automatically shorten translations. If the existing translation cannot be proven safe, HOLD it for explicit later translation work.

### Stage 10 — Binary-structure risk analysis

Track hard risk flags separately from confidence scores:

- integer-like;
- float-like;
- pointer/offset-like;
- high zero/fill density;
- table-like neighborhood;
- alignment/fill bytes that may belong to another object;
- isolated short pattern;
- repeating binary pattern;
- non-text neighborhood.

Same-length replacement does not move later objects, so do not describe this as changing ARM64 address alignment. The real risk is overwriting bytes that belong to an adjacent/embedded object or later treating the modified bytes as non-text data.

### Stage 11 — XREF/use-site negative filtering

A path into text rendering/lookup is useful positive evidence. A path into arithmetic, indexing, pointer interpretation, asset-key comparison, sort-key generation, or other non-text semantics is strong negative evidence.

XREF presence is not an "absolute king" and is not required for all SAFE objects.

### Stage 12 — `info_len` threshold calibration with a null model

Use `info_len` = effective textual information after removing established NUL/padding/control structure.

Do not choose arbitrary cutoffs from the real-candidate distribution alone.

Construct a length/code-shape-preserving shuffled/negative control corpus and measure accidental Switch-match behavior by `info_len`.

Choose thresholds only after comparing real versus null distributions. Record the method and resulting threshold in the validation ledger.

### Stage 13 — Simulated patch and object-level offline validation

Apply the proposed set to an in-memory copy of the flat Switch image.

For each patched object, verify:

- complete replacement decoding;
- field/object boundary preservation;
- no next-object run-on or adjacent-field corruption;
- control-code preservation;
- fixed stride unchanged where applicable;
- Korean font-page mapping valid;
- no executable/excluded region touched.

Check nearby patches jointly, not only independently, when their ranges are close enough to interact structurally.

### Stage 14 — Set-level invariants

Do not rely on one universal "all NUL-string start offsets must remain identical" rule because fixed-width/tail-shared structures exist.

Instead build field-type-specific set invariants, including as applicable:

- object-start/boundary inventory preservation;
- unchanged neighboring non-target bytes;
- unchanged fixed-stride layout;
- no new unresolved overlap/tail-sharing conflict;
- suspicious patch density in anchor-free regions triggers HOLD/review;
- code segment remains untouched except separately authorized runtime patches.

### Stage 15 — Emitted IPS round-trip

After generating the IPS:

- reparse the exact emitted artifact;
- reconstruct its effect on the flat image;
- compare it against the intended patch plan/simulated image;
- verify classic IPS offset/length limits and `EOF` marker collision handling.

A correct in-memory plan is not enough if the serialized artifact differs.

## 6. Confidence classes

Hard gates precede numerical scoring.

### ANCHOR

Independent structural evidence strong enough to help locate neighboring objects. It cannot depend circularly on those neighbors for its own proof.

### SAFE-A

Strong direct structural evidence such as relocation/pointer/object-start/use-site evidence plus valid field semantics, conflict checks, and offline/IPS validation. Collinearity may strengthen but is not mandatory.

### SAFE-B

Field/object structure and local homology are strong enough for safe use, but direct structural evidence is weaker or a repeated candidate was recovered through independent anchors. All mandatory safety gates still pass.

### PROBABLE

Likely text/correspondence but one structural axis remains insufficient. Diagnostic only; not release inclusion.

### HOLD

Unresolved or ambiguous. Never included automatically.

### REJECT

Confirmed encoding failure, non-text use, destructive boundary behavior, unresolved incompatible mapping, forbidden segment, or other hard failure.

## 7. Known residual risks not completely solvable by offline re-decode

Static string integrity cannot fully prove runtime semantics for:

- identifiers/asset keys compared against hard-coded literals;
- precomputed kana/sort/search indexes;
- save/load identity or compatibility paths;
- conditional late-game content;
- layout/rendering limits whose runtime buffer behavior is not statically established;
- shared JP/CN/TW runtime semantics.

These residual risks justify staged runtime sanity testing and a conservative partial-translation release rather than weakening static gates.

## 8. Runtime validation policy

After Phase 0 and offline gates:

1. ANCHOR-only;
2. SAFE-A;
3. SAFE-A + SAFE-B;
4. PROBABLE only in isolated diagnostics when needed.

Runtime coverage must exercise text families, not just early-game progression: title/menu/settings, scenario/officer selection, officer/family/castle/location lists, items/treasures, skills/jobs, dialogue/events, map, battles/duels/minigames, save list, save/load, and other large name/location tables.

Runtime success means only that the tested path did not expose a failure.

## 9. Delta-debugging policy

Binary split/ddmin is allowed only to isolate a **currently reproducible failure**.

It must not construct the safe set. A passing half is never proof that all members are safe.

Prefer meaningful subdivisions by local block, field type, text family, or risk class over arbitrary address halves when possible.

## 10. Audit output

Every candidate must remain auditable. Minimum fields:

- record/pattern IDs;
- PC RVA/length;
- original/replacement bytes and decoded forms;
- candidate count/offsets;
- segment/language-region status;
- structural evidence level/source;
- local block ID, order/spacing consistency;
- field/object type, width/stride, NUL state;
- tail-merge/subsequence/many-to-one/conflict flags;
- `info_len` and null-model class;
- control-code sequence;
- binary-risk flags;
- XREF/use-site status;
- simulated post-patch result;
- set-level invariant result;
- emitted-IPS round-trip result;
- final grade and reason.

Prefer machine-readable JSON/CSV plus a human-readable summary.

## 11. Release target

The first stable inline release should prefer **ANCHOR + SAFE-A**, accepting remaining Japanese text rather than weakening gates to chase coverage. SAFE-B can be added after separate offline/runtime confidence is established.

The long-term validator target remains all 17,103 records so repeated/ambiguous strings can be recovered safely rather than permanently discarded.

`unique match` and `runtime did not crash` are explicitly **not** release gates.
