# INLINE VALIDATION POLICY

Normative policy for mapping the PC `T5K121R` inline replacement records to Nintendo Switch v1.1.3.

This document is a **project-level invariant**. Any agent working on inline text mapping, validation, IPS generation, or crash diagnosis must follow it unless new measured evidence requires an explicit revision of this policy.

## 1. Core premise

The previous rule, "an original byte pattern occurs exactly once in Switch `main` rodata, therefore it is safe to patch", is **not a safety proof**.

`unique exact match` may be used only to discover candidate locations. It must never, by itself, authorize a patch.

A distributable inline patch must be supported by all four evidence classes:

1. valid game encoding;
2. PC-to-Switch structural homology;
3. independently verified Switch-side field/boundary structure;
4. successful offline validation after simulated patch application.

Runtime success is a sanity check, not proof of safety.

## 2. Runtime evidence that motivated this policy

The following Eden Android observations are established:

- add-on disabled: game boots/runs normally;
- `v0.2b NO-INLINE` (207 RomFS replacements + Korean font + font page mapper, no inline patches): boots and displays the Korean title correctly;
- integrated inline set: freezes;
- address-ordered half A: freezes before normal progression;
- address-ordered half B: reaches the title, then exits after button input.

Therefore the inline set contains more than one unsafe or incorrectly mapped candidate, or contains multiple candidates whose effects occur on different execution paths. Binary splitting may locate a currently reproducible crash, but it cannot construct a safe release set.

## 3. Scope

The validator is designed for the complete PC inline corpus, not only the previously selected 5,519 patterns.

Canonical source counts:

- PC inline records: `17,103`;
- distinct original patterns: `8,713`;
- original game-code mapping entries: `7,494 (0x1D46)`;
- Korean additions: `2,542`;
- expanded mapping entries: `10,036 (0x2734)`.

Always report these units separately:

- record count;
- unique-pattern count;
- Switch candidate-location count.

Do not compare or combine counts with different units without labeling them.

## 4. Validation pipeline

### Stage 0 — Normalize records

Assign stable IDs to every PC inline record and preserve:

- record ID;
- pattern ID;
- PC RVA;
- record length;
- original bytes;
- replacement bytes.

### Stage 1 — Game-encoding validation

Do not use generic Shift-JIS assumptions as the authoritative decoder. Use the game's measured mapping tables and confirmed 1/2-byte rules.

Validate both original and replacement byte streams completely. Unknown or malformed code sequences cannot be SAFE.

Control codes must be derived from measured corpus behavior or otherwise confirmed. Preserve their sequence and semantics across original and replacement text.

### Stage 2 — Enumerate all Switch candidates

Search every original pattern across Switch `main`; do not force uniqueness.

Classify candidate locations by segment:

- `.text`: excluded from ordinary inline text mapping;
- `.rodata`: primary validation target;
- `.data`: never auto-SAFE; requires separate structural proof if later recovered.

Known mapping-table regions and other confirmed non-text tables are excluded from ordinary inline text mapping.

### Stage 3 — Piecewise collinearity / homology

Treat each candidate as a `(PC RVA, Switch offset)` relation.

Build **piecewise monotonic blocks**, not one global-LIS assumption. Large order-preserving runs are strong evidence that the two builds retain the same source-level string/data ordering within a block.

Use these blocks to:

- strengthen unique candidates;
- reject or downgrade out-of-block accidental matches;
- resolve some multi-match candidates between reliable anchors;
- recover candidates previously discarded solely because they matched more than once.

Collinearity is strong evidence, but block boundaries and port-specific reorderings must be allowed.

### Stage 4 — Establish anchors

ANCHOR candidates must have especially strong evidence: valid encoding, sufficient information content, reliable homology, clear field structure, no severe binary-risk flags, and successful boundary preservation.

Do not hard-code an arbitrary minimum byte length before measuring the corpus. Determine information-length thresholds from observed false-match/risk distributions.

### Stage 5 — Resolve multi-match candidates

For repeated strings, use anchor-bounded structural position rather than nearest-address guessing.

Evidence may include:

- order between surrounding anchors;
- relative distance to neighboring records;
- neighboring string/pattern order;
- membership in the same monotonic block;
- local record/stride structure.

If ambiguity remains, keep the candidate out of release builds.

### Stage 6 — Independently infer the Switch field structure

Never assume that the PC record length equals the Switch field width.

Classify the Switch location, where possible, as:

- NUL-terminated string;
- fixed-width text field;
- fixed-stride string array;
- string-pool entry;
- structure member;
- unknown.

Use neighboring boundaries, NUL positions, alignment, repeated strides, adjacent entries, and use-site evidence. A NUL byte by itself does not prove a C-style string boundary.

### Stage 7 — Boundary and terminator preservation

A replacement that consumes NUL/padding is not automatically invalid: it may be legal in a confirmed fixed-width field.

However, if the Switch field is NUL-terminated, the patched representation must preserve a valid terminator within the field. If field type is unknown and the replacement removes all apparent termination/padding, the candidate cannot be auto-SAFE.

Do **not** automatically shorten translations to make them fit. If the PC translation cannot be proven safe in the Switch field, downgrade it to HOLD. Any later shortening is a separate, explicit translation decision.

### Stage 8 — Binary-structure risk analysis

Track hard risk flags separately from confidence scores. Examples:

- integer-like;
- float-like;
- pointer/offset-like;
- high zero/padding density;
- table-like neighborhood;
- isolated short pattern;
- repeating binary pattern;
- non-text neighborhood.

Severe structural evidence can veto an otherwise high textual score.

### Stage 9 — XREF / use-site analysis

Where feasible, inspect how the Switch location is referenced.

A path into string lookup/rendering is strong positive evidence. A path into arithmetic, indexing, pointer/offset interpretation, or another non-text use is strong negative evidence.

Lack of a direct XREF is not an automatic rejection because indirect tables and relative references may be used.

### Stage 10 — Overlap and inclusion audit

Check both:

- actual Switch address-range overlap;
- pattern inclusion/subsequence relationships that can create competing assignments.

Resolve conflicts before any release build is generated.

### Stage 11 — Simulated patch + offline re-validation

Before generating the release IPS, apply the proposed SAFE set to an in-memory copy of the flat Switch image and re-run structural checks.

For every patched field, verify at minimum:

- replacement decodes completely;
- field boundary remains valid;
- no unintended next-field run-on occurs;
- control-code structure remains valid;
- fixed stride remains intact where applicable;
- font-page mapping is valid for emitted Korean lead bytes;
- no patch touches executable code or an excluded binary region.

This stage is mandatory. A runtime test cannot replace it.

## 5. Confidence classes

Use hard gates first; use numerical scoring only to prioritize candidates that already passed mandatory gates.

### ANCHOR

Structural correspondence is strong enough to help determine neighboring mappings. ANCHOR is the strongest evidence class.

### SAFE-A

Encoding, homology, Switch field structure, boundary preservation, conflict checks, and offline post-patch validation all pass with strong structural evidence. XREF/use-site evidence is preferred where available.

### SAFE-B

All mandatory safety gates pass, but one non-mandatory evidence source such as direct XREF is weaker or unavailable. May be included in an integrated development/release candidate after ANCHOR/SAFE-A validation.

### PROBABLE

Likely text, but field structure, homology, or short-pattern confidence is not strong enough for release inclusion. Diagnostic/test only.

### HOLD

Unresolved candidate. Never included automatically.

### REJECT

Confirmed invalid encoding, non-text use, unsafe boundary behavior, unresolved destructive conflict, or other hard failure. Never patched.

## 6. Length policy

Use `info_len` — effective textual information after removing NUL/padding and recognized control structure — rather than raw record length.

Do not freeze arbitrary cutoffs such as 4, 6, 8, 10, or 16 bytes before measuring the actual corpus. First produce distributions by `info_len` for:

- unique vs multi-match behavior;
- collinearity membership;
- field-structure success;
- binary-risk incidence;
- false-positive/manual-review rate.

Then choose thresholds from measured evidence. Short strings should normally lose confidence or require anchor/use-site support rather than being rejected merely because they are short.

## 7. Audit output

Every candidate must remain auditable. Minimum fields:

- record ID / pattern ID;
- PC RVA / PC length;
- original/replacement bytes;
- decoded original/replacement text;
- Switch match count and selected offset;
- PC/Switch block IDs and collinearity status;
- field type and estimated width/stride;
- NUL/boundary state before and after;
- `info_len`;
- control-code sequences;
- binary-risk flags;
- overlap/inclusion flags;
- XREF/use-site status;
- offline post-patch validation result;
- final grade and reason.

Prefer machine-readable CSV/JSON plus a human-reviewable summary.

## 8. Runtime validation policy

Canonical baseline is the proven NO-INLINE build: RomFS replacements + Korean font + page mapper.

Runtime progression should be staged by confidence, not by arbitrary address halves:

1. ANCHOR-only;
2. SAFE-A;
3. SAFE-A + SAFE-B;
4. PROBABLE only in isolated diagnostic builds when needed.

Coverage should exercise text families, not only early-game progression: title/menu/settings, scenario and officer selection, officer/family/castle/location lists, items/treasures, skills/jobs, dialogue/events, map, battles/duels/minigames, save list, save/load, and other screens that render large name/location tables.

Runtime success means only that the tested path did not expose a failure. It does not promote an unsafe or unproven candidate to SAFE.

## 9. Delta-debugging policy

Binary split / `ddmin` is allowed only to isolate the cause of a **currently reproducible failure** after a statically validated candidate set has been built.

It must not be used to construct the safe set, and a passing half must never be treated as proof that every member of that half is safe.

When practical, diagnostic subdivision should preserve meaningful groups such as homology block, field type, text family, or risk class instead of arbitrary address halves.

## 10. Unresolved policy values

The following must be determined from measured analysis rather than guessed in advance:

- minimum ANCHOR `info_len`;
- minimum SAFE `info_len`;
- exact handling of candidates that consume NUL/padding when Switch field type is not yet proven;
- whether and how selected `.data` candidates can ever be recovered.

Until measured evidence resolves these values, conservative behavior is mandatory: uncertain candidates stay out of release builds.

## 11. Release gate

An individual inline patch may enter a distributable build only if all mandatory gates pass:

- original encoding valid;
- replacement encoding valid;
- control structure valid;
- allowed Switch region;
- structural homology established;
- Switch field structure established strongly enough for safe replacement;
- boundary/stride preserved;
- no unresolved overlap or competing mapping;
- simulated post-patch offline validation passes;
- no severe binary-structure risk remains unresolved.

`unique match` and `runtime did not crash` are explicitly **not** release gates.

## 12. Implementation target

The long-term validator target is the full `17,103`-record corpus. The old `5,519` subset is a regression/reference set, not the target architecture.

The purpose of the validator is both to remove false-positive mappings and to recover valid repeated/ambiguous strings through structural evidence.
