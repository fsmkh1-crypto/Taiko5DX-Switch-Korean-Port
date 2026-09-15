# EVENT EXTRACTION SCHEMA

Date: 2026-09-15
Status: DESIGN MATERIALIZED / NO CORPUS EXTRACTION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `EVENT_EXTRACTION_SCHEMA_MATERIALIZATION`

## 1. Purpose

This document defines how event-related text is classified before any source is promoted into the selective Korean release set.

An event container is not automatically safe to translate. Event text can contain narration, choices, static dialogue, variable insertion, branch-local complete sentences, shared message reuse, cross-message composition, and unresolved dynamic grammar. The classification unit is therefore the event message plus its caller/context metadata, not merely the file or message bytes.

Translation quality review is deferred to runtime QA. This schema determines structural/product safety only.

## 2. Product rule

The decisive question is not whether an event has branches.

The decisive question is whether each emitted surface sentence is structurally complete and has no unresolved grammatical responsibility shared with another formatter, message fragment, branch-dependent morphology rule, or context-dependent particle rule.

Safe branching is allowed. Dynamic grammatical composition is not included in R1-R3.

## 3. Event structural classes

Every event candidate receives exactly one `event_structure_class`.

### `EVENT_NARRATION_STATIC`

Complete narrative or descriptive event text.

Typical examples:
- event narration;
- historical/context explanation;
- result narration;
- scene-setting text.

Default product disposition: `INCLUDE_EVENT_KO` when the Switch owner/action is otherwise safe.

### `EVENT_OBJECTIVE_STATIC`

Complete objective, task, instruction, or event-context explanation.

Default product disposition: `INCLUDE_EVENT_KO`.

### `EVENT_CHOICE_STATIC`

A complete selectable choice string whose meaning does not depend on unresolved grammar composition.

Default product disposition: `INCLUDE_EVENT_KO`.

### `EVENT_BRANCH_LOCAL_SAFE`

The event contains conditional branching, but every reachable leaf selected by the branch is an independently complete surface sentence or complete UI string.

Requirements:
- each branch leaf has an explicit message target;
- each translated leaf is complete on its own;
- no branch leaf depends on a shared unresolved grammar formatter;
- no hidden cross-message prefix/suffix composition is required;
- shared message reuse passes caller-context audit.

Default product disposition: `INCLUDE_EVENT_KO` or `INCLUDE_SAFE_DIALOGUE_KO` according to logical role.

### `EVENT_VARIABLE_SAFE`

A structurally complete sentence with variable insertion where the variable does not determine unresolved Korean morphology.

Potential safe variables:
- person identifier rendered as original Japanese text;
- place identifier rendered as original Japanese text;
- item/technique identifier when the surrounding Korean grammar is invariant;
- fixed numeric value.

The insertion is unsafe if variable pronunciation or semantic class controls Korean particles/endings that are not resolved independently.

Default product disposition: `INCLUDE_EVENT_KO` for narration/system/event text, or `INCLUDE_SAFE_DIALOGUE_KO` for dialogue.

### `EVENT_DIALOGUE_STATIC`

Complete event dialogue whose surface sentence is fully represented by one structurally known message and stable controls.

Requirements:
- no unresolved shared grammar formatter;
- no cross-message sentence completion;
- no speech-style/relation predicate that changes Korean morphology;
- any variable insertion passes the particle-risk rule.

Default product disposition: `INCLUDE_SAFE_DIALOGUE_KO`.

### `EVENT_DYNAMIC_GRAMMAR`

The emitted Korean surface form depends on unresolved runtime grammar composition.

Triggers include:
- nested formatter controlling copula, verb stem, ending, honorific, interrogative, or speech style;
- relation/person predicate changing Korean morphology;
- caller stem plus formatter fragment plus following suffix sharing grammatical responsibility;
- multiple callers of one formatter requiring different Korean surface responsibilities;
- known C73/C188/C342-like composition families until family-wide closure.

Default product disposition: `HOLD_DYNAMIC_DIALOGUE`.

### `EVENT_SCRIPT_COMPOSED`

The final sentence is assembled from multiple messages/fragments or from a script-level composition relation not reducible to a complete leaf message.

Examples:
- prefix message + conditional fragment + suffix message;
- one message supplies a stem and another supplies an inflectional ending;
- branch selects only a grammatical fragment rather than a full sentence.

Default product disposition: `HOLD_DYNAMIC_DIALOGUE` until the complete composition contract is proven.

### `EVENT_UNKNOWN`

The message is event-related, but caller topology, composition responsibility, or semantic role is insufficiently known.

Default product disposition: `UNRESOLVED`.

## 4. Required extraction metadata

Every extracted event candidate must carry the following fields.

```text
source_id
source_family
source_file
source_block
source_message_id
pc_original_payload
pc_korean_payload
logical_role
event_structure_class
script_linkage
branch_id
branch_leaf_count
branch_targets
control_opcode_signature
nested_formatter_ids
variable_kinds
particle_risk
composition_mode
caller_count
caller_context_ids
shared_caller_safety
identity_dependency
switch_owner_status
switch_owner_or_action
product_disposition
translation_review_status
provenance
notes
```

### Field constraints

`logical_role`:

```text
NARRATION
OBJECTIVE
CHOICE
DIALOGUE
SYSTEM
UNKNOWN
```

`script_linkage`:

```text
DIRECT
BRANCH_SELECTED
DYNAMIC
CROSS_MESSAGE
UNKNOWN
```

`variable_kinds` is a set drawn from:

```text
PERSON
PLACE
ITEM
TECHNIQUE
NUMBER
DATE
OTHER
NONE
```

`particle_risk`:

```text
NONE
FIXED
ALLOMORPHIC
UNKNOWN
```

`composition_mode`:

```text
COMPLETE
VARIABLE_COMPLETE
FORMATTER_DEPENDENT
CROSS_MESSAGE
UNKNOWN
```

`shared_caller_safety`:

```text
NOT_SHARED
ALL_SAFE
MIXED
UNKNOWN
```

`translation_review_status` for initial extraction is fixed to:

```text
DEFER_TO_RUNTIME_QA
```

No automatic translation-quality score is required for initial classification.

## 5. Particle-risk rule

A variable insertion is not safe merely because the control token is understood.

Potentially unsafe Korean allomorphy includes:

- 은/는
- 이/가
- 을/를
- 과/와
- 으로/로

When an inserted person/place/item name remains Japanese and the runtime does not provide a proven Korean particle selector, the row is not automatically `EVENT_VARIABLE_SAFE` if the Korean sentence requires pronunciation-dependent allomorphy.

Allowed resolutions are:

1. use wording with invariant grammar;
2. use a source-grounded fixed particle only when the context semantically permits it;
3. leave the row Japanese;
4. classify unresolved morphology as `HOLD_DYNAMIC_DIALOGUE` or `UNRESOLVED` according to ownership evidence.

The extractor must not guess Korean pronunciation of Japanese names merely to choose a particle.

## 6. Branch-safety decision

A branch is safe when all of the following are true:

1. all reachable leaf message targets are known;
2. every translated leaf is a complete semantic surface unit;
3. control/variable semantics for every leaf are known;
4. no leaf delegates unresolved grammar to a shared formatter;
5. no leaf depends on a preceding/following message fragment to complete Korean morphology;
6. every shared leaf message has compatible caller semantics across all in-scope callers.

If any one condition fails, do not promote the branch family merely because one observed path looks correct.

## 7. Shared-message caller audit

The same physical/logical message may be referenced from multiple event or dialogue contexts.

Rules:

- `caller_count` and `caller_context_ids` are mandatory when linkage is known;
- all callers must agree on the proposed Korean surface responsibility before one shared source is included;
- safe callers plus one unsafe caller produce `shared_caller_safety=MIXED`;
- `MIXED` cannot be emitted as one unconditional Korean replacement;
- resolve through owner separation/redirection if structurally possible, otherwise hold or leave Japanese.

One safe screenshot/caller does not prove a shared message globally safe.

## 8. Formatter dependency test

An event candidate is formatter-dependent when any reachable path contains a nested/shared formatter that contributes Korean grammar rather than a purely semantic value.

High-risk responsibilities include:

- copula;
- verb stem or `하다` realization;
- sentence ending;
- honorific register;
- interrogative form;
- speech-style variant;
- relation-dependent morphology.

Known malformed families such as the prior `모양이이오군`, `실례하하겠습니다`, and `입니다인가` cases remain held. They are not repaired with deduplication or branch forcing.

## 9. Minimal script analysis policy

Do not reverse-engineer every EVENT/TS5 script upfront.

Use the minimum evidence required for classification:

1. collect event candidate message references;
2. record control/formatter signature from the message;
3. recover caller/reference and branch topology sufficient to identify reachable leaves;
4. deepen script analysis only for rows classified `DYNAMIC`, `CROSS_MESSAGE`, `MIXED`, or `UNKNOWN`;
5. preserve unresolved rows rather than expanding the analysis scope blindly.

This keeps script work proportional to actual selected content.

## 10. Mapping to product dispositions

```text
EVENT_NARRATION_STATIC    -> INCLUDE_EVENT_KO
EVENT_OBJECTIVE_STATIC    -> INCLUDE_EVENT_KO
EVENT_CHOICE_STATIC       -> INCLUDE_EVENT_KO
EVENT_BRANCH_LOCAL_SAFE   -> INCLUDE_EVENT_KO or INCLUDE_SAFE_DIALOGUE_KO
EVENT_VARIABLE_SAFE       -> INCLUDE_EVENT_KO or INCLUDE_SAFE_DIALOGUE_KO
EVENT_DIALOGUE_STATIC     -> INCLUDE_SAFE_DIALOGUE_KO
EVENT_DYNAMIC_GRAMMAR     -> HOLD_DYNAMIC_DIALOGUE
EVENT_SCRIPT_COMPOSED     -> HOLD_DYNAMIC_DIALOGUE
EVENT_UNKNOWN             -> UNRESOLVED
```

This mapping is provisional with respect to Switch owner/write safety. A structurally safe event still requires a proven Switch owner/action before build inclusion.

## 11. Extraction order

Future event candidate materialization must use this order:

```text
event candidate message collection
-> control/formatter signature extraction
-> event-script caller/reference binding
-> branch-leaf completeness check
-> variable/particle-risk classification
-> shared-caller audit
-> event_structure_class
-> final product disposition
```

No step may infer the next step from Korean text appearance alone.

## 12. Current boundary

This schema creates no corpus rows, Switch actions, write authorization, builder changes, IPS, or runtime artifact.

Next recommended scope:

`SELECTIVE_KO_EVENT_CANDIDATE_INVENTORY_READ_ONLY`

That scope should count and classify candidate event/message populations using this schema, without implementation or build.
