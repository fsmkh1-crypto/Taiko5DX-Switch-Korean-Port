# SELECTIVE KOREAN SOURCE CLASSIFICATION SCHEMA

Date: 2026-09-17
Status: CROSS-CUTTING TAXONOMY LINKED / V293 ROUTING CLARIFICATION
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Purpose

This schema defines the selective-product classification boundary for PC Korean-patch source material.

The canonical common classification rules are defined in:

`SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`

That document is authoritative for:

- authority hierarchy;
- the three observed classification axes;
- mechanism decision inputs;
- risk flags;
- Switch physical-owner/shared-caller rules;
- evidence grades;
- automatic extraction vs manual judgment;
- derived disposition rules;
- safe-dialogue eligibility;
- release-phase gates.

This file remains the product-facing bridge between that common taxonomy and the selective Korean release scope.

Event-related candidates additionally use `EVENT_EXTRACTION_SCHEMA.md` for event-specific caller/branch metadata, but event classes do not replace the common taxonomy.

## 2. Classification model

New corpus rows are classified by three observed axes:

```text
mechanism_class
usage_class
investigation_status
```

`derived_disposition` is not a peer axis. It is computed from the three observed axes plus physical-owner, caller, risk, capacity, provenance, and evidence fields.

Manual disposition override is exceptional and requires:

```text
manual_override = true
manual_override_reason = non-empty
provenance = explicit evidence
```

Missing investigation may never be manually overridden into release inclusion.

## 3. Mechanism classes

Exactly one `mechanism_class` is assigned when investigation is sufficient:

```text
STATIC_COMPLETE
BRANCH_COMPLETE
VARIABLE_INSERT
PARTICLE_SENSITIVE_INSERT
NUMERIC_COUNTER_FORMAT
FRAGMENT_COMPOSED
GRAMMAR_FORMATTER
NAME_COMPOSED
MECHANISM_MIXED
```

`APPEND_AFTER` is not a risk flag. It is a mechanism-decision input used, with append-source responsibility, to distinguish complete branch output from fragment/formatter composition.

`CONTROL_GRAPH_DEPENDENT` is not used as a generic risk flag because branch-complete output is inherently control-graph dependent and the label does not discriminate release safety.

## 4. Usage classes

Exactly one `usage_class` is assigned:

```text
UI_DESCRIPTION
NARRATION_SYSTEM
DIALOGUE
IDENTITY
OTHER
```

Usage and generation mechanism are independent.

Examples:

- a person biography may be `UI_DESCRIPTION + STATIC_COMPLETE`;
- event narration may be `NARRATION_SYSTEM + VARIABLE_INSERT`;
- dialogue may be `DIALOGUE + BRANCH_COMPLETE` or `DIALOGUE + GRAMMAR_FORMATTER`;
- excluded person/yomi presentation may be `IDENTITY + NAME_COMPOSED`.

## 5. Investigation status

Exactly one `investigation_status` is assigned:

```text
RESOLVED
CALLER_UNKNOWN
NOT_INVESTIGATED
```

`CALLER_UNKNOWN` and `NOT_INVESTIGATED` derive `UNRESOLVED`; they are investigation states, not permanent mechanism classes.

## 6. Derived dispositions

Allowed terminal product dispositions are:

```text
INCLUDE_KO
DEFER_KO
KEEP_JP
BLOCKED
UNRESOLVED
```

### `INCLUDE_KO`

Eligible only when the current release phase permits the mechanism/usage combination and all required physical-owner/caller/risk/capacity/provenance gates are closed.

### `DEFER_KO`

Koreanization is desired but a later grammar/composition/structural closure is required.

A `DEFER_KO` row must carry `defer_revisit_condition`.

### `KEEP_JP`

Intentional Japanese retention under product scope.

Typical first-release members:

- person names;
- place names;
- yomi/reading/sort keys;
- surname/given-name composition;
- name-entry identity behavior;
- calendar/year/month/day identity presentation;
- other excluded identity fields.

A `KEEP_JP` row must carry `keep_jp_reason`.

### `BLOCKED`

Use only when evidence proves that the candidate cannot be realized under the currently authorized architecture and no approved escalation route remains.

Capacity failure alone is not `BLOCKED`.

### `UNRESOLVED`

Investigation or ownership/caller/mechanism evidence is incomplete for release classification.

`UNRESOLVED` cannot be emitted by a release builder.

## 7. PC occurrence conflict rule

PC occurrence-specific replacements are a hazard map, not a Switch implementation template.

For logical conflict classification only:

1. remove the already-defined trailing NUL padding from logical comparison;
2. classify source-grounded whitespace-only differences separately;
3. preserve all non-whitespace byte ordering/content for semantic comparison.

Then:

```text
normalized logical replacements differ -> PC_OCCURRENCE_CONFLICT
only whitespace differs                -> PC_SPACING_VARIANT
```

`PC_OCCURRENCE_CONFLICT` blocks automatic `INCLUDE_KO` until caller/owner context is resolved.

`PC_SPACING_VARIANT` does not by itself block inclusion.

This distinction preserves known spacing-only occurrence variants without misclassifying them as semantic caller conflicts.

## 8. Physical-owner/shared-caller rule

Classification follows the Switch physical owner, reusing existing L1/L2/L3 or other canonical owner provenance when applicable.

Rules:

1. enumerate all known callers of one physical owner;
2. if caller-specific separation is not already available, the most restrictive proven caller governs that owner;
3. separate physical owners may be classified independently even when source text is identical;
4. raw string equality or uniqueness is not owner proof;
5. incomplete caller topology gives `investigation_status=CALLER_UNKNOWN` and derives `UNRESOLVED`;
6. caller-specific restructuring/redirection is a separate escalation, not an automatic classification shortcut.

Source/mechanism inventory may still proceed before full owner closure where the evidence supports it. Missing owner/caller evidence blocks final release inclusion; it does not automatically erase otherwise valid source-side structural observations.

## 9. Safe dialogue product definition

A dialogue row is R3-safe only when it satisfies the full safe-dialogue definition in `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`.

At minimum:

- `usage_class=DIALOGUE`;
- `investigation_status=RESOLVED`;
- mechanism is `STATIC_COMPLETE`, `BRANCH_COMPLETE`, or proven-safe `VARIABLE_INSERT`;
- all callers of the same Switch physical owner are compatible;
- no unresolved particle/grammar risk exists;
- no cross-message composition exists;
- the row is not consumed as a formatter/message fragment by another deferred or unsafe composition family;
- capacity has a proven safe realization.

A Korean line that merely looks complete or renders correctly in one caller is not sufficient proof.

## 10. Particle and numeric screening

Japanese particle adjacency is an automatic risk detector only.

```text
JP_PARTICLE_ADJACENCY -> may raise PARTICLE_RISK
```

It does not by itself prove `PARTICLE_SENSITIVE_INSERT`.

Likewise, numeric insertion becomes `NUMERIC_COUNTER_FORMAT` only when runtime behavior dynamically selects counter/unit/morphology/format. A fixed literal unit with a numeric slot remains ordinary `VARIABLE_INSERT` when no dynamic counter decision exists.

## 11. Event overlay

Event membership is not a safety class.

`EVENT_EXTRACTION_SCHEMA.md` remains an auxiliary event overlay for:

- event-specific caller/reference metadata;
- branch topology;
- leaf completeness;
- event control/formatter signatures;
- event-local variable metadata.

Its legacy event structural classes map into the common taxonomy and are not terminal release dispositions.

Examples:

```text
EVENT_NARRATION_STATIC / EVENT_OBJECTIVE_STATIC
  -> usually STATIC_COMPLETE + NARRATION_SYSTEM

EVENT_BRANCH_LOCAL_SAFE
  -> candidate BRANCH_COMPLETE only after append_after=NO and all-caller closure

EVENT_VARIABLE_SAFE
  -> candidate VARIABLE_INSERT only after particle/counter screening

EVENT_DIALOGUE_STATIC
  -> candidate STATIC_COMPLETE + DIALOGUE

EVENT_DYNAMIC_GRAMMAR
  -> GRAMMAR_FORMATTER or MECHANISM_MIXED

EVENT_SCRIPT_COMPOSED
  -> FRAGMENT_COMPOSED / GRAMMAR_FORMATTER / MECHANISM_MIXED

EVENT_UNKNOWN
  -> non-resolved investigation status
```

New rows do not use legacy dispositions such as `INCLUDE_EVENT_KO` or `HOLD_DYNAMIC_DIALOGUE` as terminal state.

## 12. Required common metadata

New corpus rows must include the common fields defined in `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`, including at least:

```text
mechanism_class
usage_class
investigation_status
switch_physical_owner_id
caller_list
append_after
append_after_targets
variable_source_kind
insert_followed_by
jp_particle_adjacency
dynamic_counter_decision
cross_message_consumers
risk_flags
pc_occurrence_count
pc_conflict_class
buffer_capacity
ko_payload_length_bytes
evidence_grade
provenance
derived_disposition
keep_jp_reason
defer_revisit_condition
manual_override
manual_override_reason
translation_review_status
```

Container-specific schemas may add fields but may not redefine common-field semantics.

Initial translation review policy remains:

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

Translation quality is reviewed during runtime play rather than used as a pre-extraction release blocker.

This translation-QA deferral does not resolve product-policy questions such as how Japanese-retained identity should appear when the PC Korean prose contains Korean person/place names as literals.

## 13. Automatic extraction vs manual judgment

Corpus-scale classification must distinguish deterministic extraction from semantic judgment.

Machine extraction should be used where possible for:

- source/container/message identity;
- caller/reference graph;
- branch targets;
- `append_after` and append target identity;
- variable-source provenance;
- `insert_followed_by`;
- Japanese particle adjacency detector;
- dynamic counter path/opcode evidence;
- nested formatter IDs;
- cross-message consumers;
- physical-owner reuse from canonical ledgers;
- PC occurrence/variant data;
- spacing-only versus logical conflict where byte rules suffice;
- byte lengths/capacity;
- direct provenance identities/hashes.

Manual/semantic judgment remains for:

- usage when not encoded structurally;
- semantic branch completeness;
- whether Korean morphology truly depends on inserted value pronunciation/class;
- grammatical responsibility across fragments;
- semantic equivalence of PC source to selected Switch context;
- mixed mechanism interpretation;
- exceptional manual override;
- runtime translation-quality QA.

Do not turn machine-extractable fields into thousands of manual checklist entries.

## 14. Evidence grades

Use:

```text
VERIFIED
OBSERVED
INFERRED
HINT
REJECTED
```

`REJECTED` is retained so later agents do not repeat failed or contradicted hypotheses.

PC runtime behavior whose exact target executable/runtime identity is not proven cannot exceed `HINT` for mechanism claims.

## 15. Capacity rule

Do not convert capacity failure into a translation rewrite.

Use the canonical escalation order:

```text
current storage
-> alternate existing storage
-> object/data reconstruction
-> redirect/relocation realization
-> Switch-native runtime semantic equivalent
-> only after technical routes are exhausted: human translation adjustment review
```

Automatic truncation/shortening is forbidden.

## 16. Release-set definitions

R1:

```text
INCLUDE_KO + usage_class=UI_DESCRIPTION
```

R2 adds structurally safe:

```text
INCLUDE_KO + usage_class=NARRATION_SYSTEM
```

and explicitly resolved event-local non-dialogue rows where appropriate.

R3 adds only rows satisfying the Safe Dialogue product definition.

R4 may selectively revisit `DEFER_KO` grammar/composition families after their recorded revisit conditions are met.

R4 remains optional and cannot block R1-R3.

## 17. Superseded legacy disposition labels

The following labels remain readable as historical provenance but are superseded for new corpus rows:

```text
INCLUDE_DESCRIPTION_KO
INCLUDE_EVENT_KO
INCLUDE_SAFE_DIALOGUE_KO
HOLD_DYNAMIC_DIALOGUE
KEEP_JP_IDENTITY
OUT_OF_SCOPE
UNRESOLVED   # legacy direct label; new rows derive it
```

Historical rows/documents are not silently rewritten. When materialized into the new corpus model they must be re-expressed as common axes plus `derived_disposition` with provenance retained.

## 18. Current boundary and routing

This schema creates no corpus rows, Switch actions, builder changes, IPS, or runtime artifact.

This file does **not** declare the executable next scope.

The sole executable next-scope authority is:

`selective_ko/SELECTIVE_PROJECT_STATE.md`

Before broad corpus classification, the architecture requires a cross-container inventory that establishes, per source family/container, which common fields are machine-extractable, manually decidable, or currently unavailable, and which existing parsers/owner ledgers can be reused.

That inventory requirement is a design prerequisite, not an independent routing declaration from this schema.
