# SELECTIVE KOREAN SOURCE CLASSIFICATION SCHEMA

Date: 2026-09-15
Status: DESIGN BASELINE

## 1. Purpose

This schema classifies existing PC Korean-patch source material for the selective Switch product. It intentionally does not preserve the old requirement that every PC source item must become a Switch action.

Event-related candidates must first pass the dedicated structural classification in `EVENT_EXTRACTION_SCHEMA.md`. `INCLUDE_EVENT_KO` is never assigned merely because a source belongs to an event container.

## 2. Terminal dispositions

Every candidate source receives exactly one terminal product disposition.

### `INCLUDE_DESCRIPTION_KO`

Use Korean for explanatory information needed to understand game entities or systems.

Typical content:

- person biography/description;
- region/location explanation;
- item/tool description;
- technique/skill description;
- help/system explanation.

Proper names inside the text may remain Japanese when separating or replacing them would require excluded identity logic.

### `INCLUDE_EVENT_KO`

Use Korean for event narration, objective/context text, choices, and structurally safe event sentences.

Event candidates must first receive an `event_structure_class` under `EVENT_EXTRACTION_SCHEMA.md`. Safe branch selection is permitted when every reachable translated leaf is a complete surface unit and shared callers are compatible. Dynamic grammar, cross-message composition, or unresolved caller topology is not `INCLUDE_EVENT_KO`.

### `INCLUDE_SAFE_DIALOGUE_KO`

Use Korean for dialogue only when the full surface sentence is structurally determined without unresolved dynamic grammar.

Examples:

- complete static sentence;
- simple variable insertion with stable control semantics and no unresolved particle allomorphy;
- name/place variable may remain Japanese;
- no unresolved nested grammar formatter;
- event dialogue whose event-structure classification is `EVENT_DIALOGUE_STATIC`, `EVENT_BRANCH_LOCAL_SAFE`, or `EVENT_VARIABLE_SAFE` and whose caller audit passes.

### `HOLD_DYNAMIC_DIALOGUE`

Dialogue whose Korean surface form depends on unresolved formatter composition, speech-style branching, relation state, shared grammar fragments, or script-level cross-message composition.

Examples include current C73/C188/C342-related families until a family-wide Korean grammar contract is proven.

This disposition is valid for R1-R3 and is not a release blocker.

### `KEEP_JP_IDENTITY`

Keep Switch original Japanese representation.

Default members:

- person names;
- place names;
- surname/given-name display fields;
- yomi/reading/sort keys;
- calendar/year/month/day text;
- name-entry/input-specific identity data.

### `OUT_OF_SCOPE`

PC Korean source has no required product role in the selective release.

Typical examples:

- Windows-only implementation mechanics;
- Koreanization supporting excluded name/yomi/date functionality;
- PC-only compatibility/installer behavior.

### `UNRESOLVED`

Insufficient evidence to decide product scope, event composition safety, caller compatibility, or semantic owner.

`UNRESOLVED` cannot be emitted by a release builder.

## 3. Required classification fields

Recommended base row model:

```text
source_id
source_family
pc_location_or_index
korean_payload
logical_role
product_disposition
formatter_dependency
identity_dependency
switch_owner_status
switch_owner_or_action
translation_review_status
provenance
notes
```

For event-related sources, the full metadata fields in `EVENT_EXTRACTION_SCHEMA.md` are additionally mandatory.

Initial translation review policy:

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

Translation quality is reviewed during runtime play rather than used as a pre-extraction release blocker.

## 4. Decision order

For each source:

1. identify the logical role from existing structural evidence;
2. if it is person/place/date/yomi/name-input identity, prefer `KEEP_JP_IDENTITY`;
3. if it is explanatory text, prefer `INCLUDE_DESCRIPTION_KO`;
4. if it is event-related, run `EVENT_EXTRACTION_SCHEMA.md` before assigning a product disposition;
5. if dialogue is surface-complete and structurally safe, use `INCLUDE_SAFE_DIALOGUE_KO`;
6. if dynamic formatter grammar or cross-message grammatical composition is required, use `HOLD_DYNAMIC_DIALOGUE`;
7. if the source exists only to support excluded PC mechanics, use `OUT_OF_SCOPE`;
8. if role/ownership/composition remains unclear, use `UNRESOLVED`.

## 5. Dynamic-dialogue test

A dialogue source is not `SAFE` merely because its Korean bytes fit.

It is `HOLD_DYNAMIC_DIALOGUE` when any of the following is true and not already closed:

- nested shared formatter call determines copula/verb/ending;
- speech-style predicate changes Korean morphology;
- relation/person predicate changes grammatical output;
- caller stem + formatter fragment + following suffix have overlapping grammatical responsibility;
- multiple callers of one formatter require different Korean surface composition;
- event script composes one sentence across multiple message fragments;
- shared message caller contexts disagree on Korean grammatical responsibility.

## 6. Event-first rule

Event membership is not itself a safety class.

Before an event source can become `INCLUDE_EVENT_KO` or `INCLUDE_SAFE_DIALOGUE_KO`, classify it under one of:

```text
EVENT_NARRATION_STATIC
EVENT_OBJECTIVE_STATIC
EVENT_CHOICE_STATIC
EVENT_BRANCH_LOCAL_SAFE
EVENT_VARIABLE_SAFE
EVENT_DIALOGUE_STATIC
EVENT_DYNAMIC_GRAMMAR
EVENT_SCRIPT_COMPOSED
EVENT_UNKNOWN
```

The exact definitions, branch completeness gates, particle-risk rules, shared-caller audit, and extraction metadata are authoritative in `EVENT_EXTRACTION_SCHEMA.md`.

## 7. Safety principles

- Do not classify by Korean text appearance alone.
- Do not convert a capacity problem into a translation rewrite.
- Do not translate excluded identity/yomi/date data because a source is easy to patch.
- Do not use raw-string uniqueness as sole owner proof.
- Existing VERIFIED Switch owner evidence may be reused without re-tracing.
- Excluded sources remain accounted for by product disposition; they are not silently dropped.
- A branch is not unsafe merely because it branches; complete independent leaves may be translated.
- A variable insertion is not safe merely because the token is understood; Korean particle allomorphy must be resolved or avoided.
- One safe caller does not prove a shared message safe for all callers.

## 8. Release-set definitions

R1 source set:

```text
INCLUDE_DESCRIPTION_KO
```

R2 adds:

```text
INCLUDE_EVENT_KO
```

R3 adds:

```text
INCLUDE_SAFE_DIALOGUE_KO
```

Never included in R1-R3:

```text
HOLD_DYNAMIC_DIALOGUE
KEEP_JP_IDENTITY
OUT_OF_SCOPE
UNRESOLVED
```

R4 may selectively promote `HOLD_DYNAMIC_DIALOGUE` families after explicit grammar-family closure.
