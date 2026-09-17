# SWITCH SELECTIVE KOREANIZATION ARCHITECTURE

Date: 2026-09-17
Status: DESIGN BASELINE / V293 ROUTING CLARIFICATION / NO IMPLEMENTATION AUTHORITY

## 1. Design objective

Build a stable Korean-assisted Nintendo Switch version of Taiko Risshiden V DX by translating only the information needed to understand and play the game, while leaving high-risk identity and grammar systems in Japanese unless separately proven safe.

The architecture intentionally rejects the old assumption that every PC Korean-patch source item must become a Switch action.

## 2. Product layers

### Layer A — Korean content source

Preferred source:

- PC Korean translation corpus;
- PC Korean terminology;
- PC Korean explanatory text;
- PC Korean event text;
- PC Korean safe dialogue text.

This layer supplies content, not implementation mechanics.

### Layer B — source classifier

Every candidate source is classified before implementation.

Primary questions:

1. Is this explanatory/narrative text needed by the product scope?
2. Does it contain person/place/date/yomi identity content that may remain Japanese?
3. Does it require a dynamic formatter or relation/speech-style branch?
4. Is the complete logical object boundary known?
5. Is a safe Switch semantic owner already known?

No source reaches a builder without a terminal disposition.

Before broad classification, the project must know which containers/source families actually own the R1/R2/R3 content and which required classification fields are extractable for each family.

### Layer C — Korean code-space foundation

Reuse the verified Mapping 10,036 Switch-native family and Korean font assets where applicable.

Requirements:

- Unicode <-> game-code conversion must preserve the selected Korean corpus;
- Korean page mapping/font coverage must include every emitted Korean code;
- any selected mixed Japanese/Korean surface must preserve both scripts on its actual Switch transport/render route;
- no expansion is justified merely because the PC patch contains unused Korean assets.

### Layer D — text transport

Switch-native parsing/normalization behavior is preserved unless it corrupts selected Korean data.

Known structure to reuse:

- direct display/render routes;
- generic parser route;
- explicit auxiliary/yomi conversion route.

The selective project can reduce runtime-byte work by proving that excluded yomi/name fields never need Korean compact-byte preservation.

### Layer E — static/event content realization

Preferred order:

1. direct Switch-native static owner;
2. complete object reconstruction;
3. safe redirection to replacement storage;
4. minimal Switch-native runtime behavior only if the selected content cannot be represented safely as data.

Capacity failure never authorizes arbitrary shortening of the Korean source.

### Layer F — optional Korean dialogue grammar

Dynamic formatter dialogue is isolated from the base product.

It is included only after a formatter family obtains a corpus-wide Korean composition contract.

Examples of contract dimensions:

- caller owns the verb/copula stem;
- formatter owns the full verb/copula;
- formatter must emit suffix-only form;
- formatter is suppressed because the following ending already owns the grammatical function;
- context selects a distinct surface form.

A family rule must cover every in-scope caller or explicitly leave exceptions Japanese.

## 3. Content tiers

### Tier 1 — mandatory descriptions

- person descriptions;
- location/region descriptions;
- item/tool descriptions;
- technique/skill descriptions;
- explanatory menu/help text required to understand game systems.

Names embedded in these descriptions are a separate unresolved product-policy question when the PC Korean prose itself contains Korean-rendered identity literals. Identity fields remain Japanese by default, but prose-embedded identity handling must be explicitly decided before R1 release materialization depends on it.

### Tier 2 — mandatory events

- event narrative;
- quest/event explanations;
- decision context;
- static event sentences.

Dynamic speech-format fragments are excluded until safe.

### Tier 3 — optional safe dialogue

Include only lines whose Korean composition is structurally complete and does not depend on unresolved grammar families.

Typical eligible cases:

- complete static sentence;
- simple variable insertion with Japanese name/place token preserved;
- control tokens with known stable semantics;
- no nested grammar formatter dependency.

### Tier 4 — optional dynamic dialogue

Includes C73/C188/C342-like shared formatter families and similar nested composition.

This tier cannot block release.

## 4. Handling the prior malformed-dialogue family

Observed examples:

- `조금 과음한 모양이이오군`
- `오늘은 이만 실례하하겠습니다`
- `야규님입니다인가`

The old full-port route attempted to preserve PC Korean TAI5MSG composition and diagnose runtime predicates. Later evidence showed that the PC Korean data itself can contain caller/formatter boundaries that look duplicative when naively appended.

Selective-project policy:

1. do not alter C8:87, 0x6A, relation state, or individual fragments merely to hide these examples;
2. mark affected formatter-dependent lines as deferred for R1-R3;
3. when R4 is intentionally opened, enumerate the complete caller set for each formatter family;
4. derive Korean responsibility boundaries from the original Japanese grammar role + PC Korean intended text + caller/suffix context;
5. implement one family rule only after all affected callers are classified;
6. any unresolved caller remains Japanese rather than receiving a heuristic deduplication patch.

This converts the old issue from a release blocker into an optional grammar subsystem.

## 5. Reuse policy for previous work

### Reuse directly

- Mapping 10,036 Switch-native implementation/evidence;
- Switch binary identities and layout;
- structural target/owner evidence where the same selected source is reused;
- TAI5MSG parser/container knowledge;
- TAI5MSG 14,832-slot structure lattice for deterministic locator/length structure only;
- font/code-space inventory, subject to exact asset identity and actual selected-route coverage;
- deterministic build/guard principles.

### Reuse as reference only

- PC runtime descriptors/helpers;
- pointer pool layout;
- full 17,103 source-accounting obligation;
- full-port Action Ledger cardinalities;
- PC-specific runtime allocation/signature machinery;
- TAI5MSG legacy reconstruction that assumes the entire PC Korean file is the product payload;
- V289 grammar125 implementation technique.

### Optional later evidence

- V285-V288 grammar125 analysis/manifest as `OPTIONAL_R4_GRAMMAR_EVIDENCE`.

### Exclude from selective product baseline

- V290 integrated full-port builder/build;
- V291 package;
- bulk PC patch `data/` import;
- whole-PC-Korean-TAI5MSG release payload assumptions.

V291 screenshots/runtime observations may be retained as historical failure/narrow diagnostic evidence, not as release payload or builder input.

### Exclude from initial product scope

- CWTDAT Koreanization;
- yomi conversion;
- Korean person/place-name replacement;
- date/calendar Koreanization;
- Korean name entry;
- unresolved dynamic dialogue grammar.

## 6. New builder shape

A future selective builder should consume an explicit manifest, not discover scope heuristically.

Conceptual inputs:

- canonical Switch v1.1.3 dump;
- approved Korean font/code-space assets;
- approved selected-source manifest;
- explicit per-source Switch action/guard;
- optional R4 grammar manifest.

Builder responsibilities:

- validate exact input identities;
- apply only approved actions;
- reject unknown/unresolved rows;
- preserve excluded Japanese objects;
- emit deterministic artifacts and reports.

Builder must not:

- decide which sentence should be Korean;
- infer that a repeated string is safe to overwrite;
- auto-deduplicate Korean syllables;
- import all PC patch files merely because they exist;
- translate names/yomi/date fields implicitly.

## 7. Validation gates

For R1-R3 release:

- every included source has a known logical object;
- every included source has an explicit Switch owner/action;
- every emitted Korean code has mapping/font coverage;
- every selected mixed-script surface preserves Japanese and Korean on its actual route;
- excluded identity/yomi/date objects remain byte-identical to the Switch baseline unless separately approved;
- unresolved product-policy questions such as identity-in-prose are closed before affected payload materialization;
- no deferred dynamic-grammar source is emitted;
- build is deterministic;
- representative runtime tests pass for each included content family.

## 8. Architectural sequence — non-authoritative guidance

This section is architectural guidance only. It does **not** declare the executable next scope.

The sole executable next-scope authority is:

`selective_ko/SELECTIVE_PROJECT_STATE.md`

Recommended sequence after V293:

1. cross-container content-owner / classification-field availability inventory for R1/R2/R3;
2. identity-in-prose product-policy decision;
3. R1 description/UI owner and structure closure;
4. R1 classification/materialization and diagnostic build;
5. R2 event/system container/owner closure and diagnostic build;
6. R3 safe-dialogue payload/caller/owner classification and diagnostic build;
7. optional R4 grammar work only if still desired.

The inventory stage may prove that some phases share or reorder containers. If so, change the roadmap explicitly instead of treating this sequence as a hidden execution authority.

Each stage remains separately authorized.
