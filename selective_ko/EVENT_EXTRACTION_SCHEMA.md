# EVENT EXTRACTION SCHEMA

Date: 2026-09-17
Status: DESIGN MATERIALIZED / COMMON-TAXONOMY ALIGNED / V295 ROUTING CORRECTED / NO CORPUS EXTRACTION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `EVENT_EXTRACTION_SCHEMA_MATERIALIZATION`

## 1. Purpose

This document defines how event-related text is structurally described before any source is promoted into the selective Korean release set.

An event container is not automatically safe to translate. Event text can contain narration, choices, static dialogue, variable insertion, branch-local complete sentences, shared message reuse, cross-message composition, and unresolved dynamic grammar. The classification unit is therefore the event message plus its caller/context metadata, not merely the file or message bytes.

Translation quality review is deferred to runtime QA. This schema determines event-specific structural metadata only.

Common classification authority remains:

- `CLASSIFICATION_SCHEMA.md`;
- `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`.

This event schema is an overlay and may not redefine common `mechanism_class`, `usage_class`, `investigation_status`, or terminal `derived_disposition` semantics.

V295 correction authority:

`CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`

## 2. Product rule

The decisive question is not whether an event has branches.

The decisive question is whether each emitted surface sentence is structurally complete and has no unresolved grammatical responsibility shared with another formatter, message fragment, branch-dependent morphology rule, or context-dependent particle rule.

Safe branching is allowed. Dynamic grammatical composition is not included in R1-R3.

Container membership alone never decides product inclusion.

## 3. Event structural classes

Every event candidate may receive one event-specific `event_structure_class` in addition to the common taxonomy fields.

### `EVENT_NARRATION_STATIC`

Complete narrative or descriptive event text.

Typical examples:
- event narration;
- historical/context explanation;
- result narration;
- scene-setting text.

Common-taxonomy expectation: usually `STATIC_COMPLETE + NARRATION_SYSTEM`.

Potential derived disposition: `INCLUDE_KO` only after Switch owner/action, caller/risk/capacity/provenance gates close.

### `EVENT_OBJECTIVE_STATIC`

Complete objective, task, instruction, or event-context explanation.

Common-taxonomy expectation: usually `STATIC_COMPLETE + NARRATION_SYSTEM`.

Potential derived disposition: `INCLUDE_KO` only after common release gates close.

### `EVENT_CHOICE_STATIC`

A complete selectable choice string whose meaning does not depend on unresolved grammar composition.

Common-taxonomy expectation: typically `STATIC_COMPLETE` or `BRANCH_COMPLETE`, with usage determined from actual context.

Potential derived disposition: `INCLUDE_KO` only after common release gates close.

### `EVENT_BRANCH_LOCAL_SAFE`

The event contains conditional branching, but every reachable leaf selected by the branch is an independently complete surface sentence or complete UI string.

Requirements:
- each branch leaf has an explicit message target;
- each translated leaf is complete on its own;
- no branch leaf depends on a shared unresolved grammar formatter;
- no hidden cross-message prefix/suffix composition is required;
- shared message reuse passes caller-context audit;
- `append_after=NO` for same-surface grammatical completion.

Common-taxonomy expectation: candidate `BRANCH_COMPLETE`.

Potential derived disposition: `INCLUDE_KO` only when the usage/release phase and all common gates permit it.

### `EVENT_VARIABLE_SAFE`

A structurally complete sentence with variable insertion where the variable does not determine unresolved Korean morphology.

Potential safe variables:
- person identifier rendered as original Japanese text;
- place identifier rendered as original Japanese text;
- item/technique identifier when the surrounding Korean grammar is invariant;
- fixed numeric value.

The insertion is unsafe if variable pronunciation or semantic class controls Korean particles/endings that are not resolved independently.

Common-taxonomy expectation: candidate `VARIABLE_INSERT`.

Potential derived disposition: `INCLUDE_KO` only after particle/counter/owner/caller/capacity gates close.

### `EVENT_DIALOGUE_STATIC`

Complete event dialogue whose surface sentence is fully represented by one structurally known message and stable controls.

Requirements:
- no unresolved shared grammar formatter;
- no cross-message sentence completion;
- no speech-style/relation predicate that changes Korean morphology;
- any variable insertion passes the particle-risk rule.

Common-taxonomy expectation: candidate `STATIC_COMPLETE + DIALOGUE`.

Potential derived disposition: `INCLUDE_KO` only when it satisfies the full R3 Safe Dialogue definition.

### `EVENT_DYNAMIC_GRAMMAR`

The emitted Korean surface form depends on unresolved runtime grammar composition.

Triggers include:
- nested formatter controlling copula, verb stem, ending, honorific, interrogative, or speech style;
- relation/person predicate changing Korean morphology;
- caller stem plus formatter fragment plus following suffix sharing grammatical responsibility;
- multiple callers of one formatter requiring different Korean surface responsibilities;
- known C73/C188/C342-like composition families until family-wide closure.

Common-taxonomy expectation: `GRAMMAR_FORMATTER` or `MECHANISM_MIXED`.

Default current result: `DEFER_KO` when Koreanization is desired and a concrete R4 revisit condition is known; otherwise unresolved structural evidence remains `UNRESOLVED`.

### `EVENT_SCRIPT_COMPOSED`

The final sentence is assembled from multiple messages/fragments or from a script-level composition relation not reducible to a complete leaf message.

Examples:
- prefix message + conditional fragment + suffix message;
- one message supplies a stem and another supplies an inflectional ending;
- branch selects only a grammatical fragment rather than a full sentence.

Common-taxonomy expectation: `FRAGMENT_COMPOSED`, `GRAMMAR_FORMATTER`, or `MECHANISM_MIXED` according to proven responsibility.

Default current result: usually `DEFER_KO` after the composition graph is known; otherwise `UNRESOLVED`.

### `EVENT_UNKNOWN`

The message is event-related, but caller topology, composition responsibility, or semantic role is insufficiently known.

Common result: non-resolved investigation state and derived `UNRESOLVED`.

## 4. Required extraction metadata

Every extracted event candidate carries event overlay fields plus the common fields required by `CLASSIFICATION_SCHEMA.md`.

Event-specific overlay fields:

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
provenance
notes
```

Common fields still required where materialized include at least:

```text
mechanism_class
usage_class
investigation_status
append_after
append_after_targets
variable_source_kind
insert_followed_by
jp_particle_adjacency
dynamic_counter_decision
cross_message_consumers
risk_flags
buffer_capacity
ko_payload_length_bytes
evidence_grade
derived_disposition
keep_jp_reason
defer_revisit_condition
manual_override
manual_override_reason
translation_review_status
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

1. use source-grounded wording whose grammar is already invariant;
2. apply the separately authorized fixed-particle policy only under its exact applicability gate;
3. leave the row Japanese where product scope permits;
4. use `DEFER_KO` when a later morphology/formatter closure is the explicit revisit condition;
5. use `UNRESOLVED` when ownership/mechanism evidence is incomplete.

The extractor must not guess Korean pronunciation of Japanese names merely to choose a particle.

## 6. Branch-safety decision

A branch is safe when all of the following are true:

1. all reachable leaf message targets are known;
2. every translated leaf is a complete semantic surface unit;
3. control/variable semantics for every leaf are known;
4. no leaf delegates unresolved grammar to a shared formatter;
5. no leaf depends on a preceding/following message fragment to complete Korean morphology;
6. every shared leaf message has compatible caller semantics across all in-scope callers;
7. same-surface completion does not require an unaccounted `append_after` target.

If any one condition fails, do not promote the branch family merely because one observed path looks correct.

## 7. Shared-message caller audit

The same physical/logical message may be referenced from multiple event or dialogue contexts.

Rules:

- `caller_count` and `caller_context_ids` are mandatory when linkage is known;
- all callers must agree on the proposed Korean surface responsibility before one shared source is included;
- safe callers plus one unsafe caller produce `shared_caller_safety=MIXED`;
- `MIXED` cannot be emitted as one unconditional Korean replacement;
- resolve through owner separation/redirection if structurally possible, otherwise defer, keep Japanese, or remain unresolved according to the common taxonomy.

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

Known malformed families such as the prior `모양이이오군`, `실례하하겠습니다`, and `입니다인가` cases remain deferred for R1-R3. They are not repaired with deduplication or branch forcing.

## 9. Minimal script analysis policy

Do not reverse-engineer every EVENT/TS5 script upfront.

Use the minimum evidence required for classification:

1. collect event candidate message references;
2. record control/formatter signature from the message;
3. recover caller/reference and branch topology sufficient to identify reachable leaves;
4. deepen script analysis only for rows whose linkage/composition/caller state remains dynamic, cross-message, mixed, or unknown;
5. preserve unresolved rows rather than expanding the analysis scope blindly.

This keeps script work proportional to actual selected content.

## 10. Mapping event classes to the common taxonomy

Event classes do not directly assign legacy terminal labels.

Use this mapping only as a classification aid:

```text
EVENT_NARRATION_STATIC  -> usually STATIC_COMPLETE + NARRATION_SYSTEM
EVENT_OBJECTIVE_STATIC  -> usually STATIC_COMPLETE + NARRATION_SYSTEM
EVENT_CHOICE_STATIC     -> STATIC_COMPLETE or BRANCH_COMPLETE; usage from context
EVENT_BRANCH_LOCAL_SAFE -> candidate BRANCH_COMPLETE after append/caller closure
EVENT_VARIABLE_SAFE     -> candidate VARIABLE_INSERT after particle/counter screening
EVENT_DIALOGUE_STATIC   -> candidate STATIC_COMPLETE + DIALOGUE
EVENT_DYNAMIC_GRAMMAR   -> GRAMMAR_FORMATTER or MECHANISM_MIXED
EVENT_SCRIPT_COMPOSED   -> FRAGMENT_COMPOSED / GRAMMAR_FORMATTER / MECHANISM_MIXED
EVENT_UNKNOWN           -> CALLER_UNKNOWN or NOT_INVESTIGATED as evidence dictates
```

Then derive only one of the common terminal results:

```text
INCLUDE_KO
DEFER_KO
KEEP_JP
BLOCKED
UNRESOLVED
```

Legacy labels such as `INCLUDE_EVENT_KO`, `INCLUDE_SAFE_DIALOGUE_KO`, and `HOLD_DYNAMIC_DIALOGUE` remain historical provenance only.

## 11. Current EVENT-family claim-strength boundary

Current source-side facts from V295:

```text
PC Korean patch EVENT/*.TS5 file denominator = 169
verified samples directly contain Korean narration/dialogue payloads
```

Not established yet:

```text
169/169 structurally verified text-bearing status
production whole-family text-field parser
whole-family caller/branch extraction
Switch-original EVENT correspondence
production Switch owner/action bindings
```

Raw byte scans may be used for discovery only. They cannot be promoted into structural text-field counts without parser/boundary proof.

## 12. Extraction order

Future event candidate materialization uses this order:

```text
event candidate message collection
-> control/formatter signature extraction
-> event-script caller/reference binding
-> branch-leaf completeness check
-> variable/particle-risk classification
-> shared-caller audit
-> event_structure_class overlay
-> common mechanism/usage/investigation axes
-> common derived_disposition
```

No step may infer the next step from Korean text appearance alone.

## 13. Current boundary and routing

This schema creates no corpus rows, Switch actions, write authorization, builder changes, IPS, or runtime artifact.

This file does **not** declare the executable next scope.

The sole executable next-scope authority is:

`SELECTIVE_PROJECT_STATE.md`

Current EVENT work remains inside the broader open container/field-availability inventory until that state file explicitly advances the route.

If Switch-original EVENT data becomes necessary later and is not yet supplied, use `SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md` and record the counterpart as `NOT_YET_SUPPLIED`; do not infer Switch structure from the PC file.
