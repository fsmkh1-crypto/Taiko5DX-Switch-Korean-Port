# SCRIPT TAXONOMY AND CROSS-CUTTING RULES

Date: 2026-09-15 (KST)
Status: CANONICAL SELECTIVE-KO DESIGN RULE
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES_MATERIALIZATION`

## 1. Purpose

This document defines the common classification and decision rules for Koreanizing text across different game containers and runtime paths.

The classification unit is not a file type. `TAI5MSG`, `EVENT/TS5`, UI/description tables, CWTDAT, SNR-backed state, and other containers may each contain outputs produced by different mechanisms. A container name therefore never determines safety by itself.

The product target is selective Koreanization. The first release prioritizes explanatory text, structurally safe event text, and proven-safe dialogue. Person/place identity, yomi, date formatting, name composition, and unresolved dynamic Korean grammar may remain Japanese.

Translation quality review is deferred to real-device/runtime QA:

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

This document governs structural classification and release disposition, not translation-style editing.

## 2. Authority hierarchy

Different questions have different authorities. They must not be collapsed into one generic "PC reference" category.

### 2.1 Translation/content authority

For Korean translations, terminology, established Korean spellings, and source-grounded content already present in the PC Korean patch:

```text
PC_KOREAN_PATCH_DATA = SOURCE_AUTHORITY
```

Do not guess names, terms, glyph codes, or translations that are available from canonical PC patch data.

### 2.2 Glyph/mapping authority

PC mapping/font assets define the Korean source obligation. Switch release behavior must use the separately validated Switch-native realization where one exists.

```text
PC_MAPPING_FONT_DATA          = SOURCE_AUTHORITY
VERIFIED_SWITCH_REALIZATION   = SWITCH_RUNTIME_AUTHORITY
```

### 2.3 Script/control authority

For script graph, control flow, opcode semantics, physical owner topology, and runtime structure:

```text
SWITCH_ORIGINAL = STRUCTURAL_AUTHORITY
```

The PC patch may reveal semantic intent but does not override Switch-native structure.

### 2.4 Visible semantic result

A known-good PC Korean visible result is a semantic oracle only for the context in which it was actually observed.

```text
PC_KNOWN_GOOD_VISIBLE_RESULT = SEMANTIC_ORACLE
```

Do not generalize one observed caller to all callers of a shared message/formatter.

### 2.5 PC runtime mechanism

PC runtime helpers, pointer redirects, suppression logic, descriptors, and Windows-specific code are implementation references, not Switch implementation authority.

Until the exact PC target executable identity/runtime context is proven for a runtime observation, that observation cannot exceed `HINT` evidence grade.

```text
PC_RUNTIME_MECHANISM = REFERENCE_OR_HINT
```

### 2.6 PC workaround/bug

Known workarounds and defects are non-authoritative implementation evidence.

```text
PC_WORKAROUND_OR_BUG = NON_AUTHORITATIVE_EVIDENCE
```

They may still identify a real semantic hazard. In particular, occurrence-specific PC replacement behavior can be used as a risk map even when the Windows mechanism itself is not ported.

### 2.7 Conflict rule

When PC content and Switch structure differ:

```text
structure = Switch
content/semantic obligation = PC source/oracle
implementation = Switch-native design
```

Do not rewrite Korean source text merely to make a Switch structural mismatch disappear.

## 3. Top-level cross-cutting principles

1. Preserve Switch-native script/control/runtime structure by default and selectively transfer Korean content/semantic effect.
2. Do not mechanically clone Windows/x86 patch mechanisms.
3. Do not automatically change string count, slot count, object cardinality, branch graph, or control graph.
4. A structural change required for correct Korean is an explicit escalation item and needs its own design/authorization.
5. A classification that is not resolved is never an inclusion reason.
6. Classification is based on all callers of the same Switch physical owner, not on one screenshot, one caller, or raw-string uniqueness.
7. When one physical owner is shared by multiple callers and caller-specific separation is not already available, the most restrictive proven caller governs that physical owner.
8. Separate physical owners may be classified independently even when their source text is identical.
9. Dynamic Korean grammar is never repaired by generic syllable deduplication, suffix deletion, branch forcing, or per-sentence patches.
10. Capacity failure is not a translation defect and does not authorize truncation or rewriting.
11. PC occurrence-specific replacements are evidence about context sensitivity; they are not instructions to reproduce PC occurrence mechanics.
12. Translation QA is deferred to runtime play unless a translation issue blocks structural interpretation.

### 3.1 Capacity escalation order

When Korean payload capacity fails, use this order:

```text
current storage
-> alternate existing storage
-> object/data reconstruction
-> redirect/relocation realization
-> Switch-native runtime semantic equivalent
-> only after technical routes are exhausted: human translation adjustment review
```

Automatic truncation or "shorten until it fits" is forbidden.

## 4. Classification model: three observed axes plus one derived result

`mechanism_class`, `usage_class`, and `investigation_status` are observed/classified properties.

`disposition` is not a fourth peer axis. It is derived from those three properties plus risk/evidence fields. Manual disposition overrides require an explicit reason and provenance.

## 5. Axis A — generation mechanism

Every candidate receives exactly one `mechanism_class`.

### `STATIC_COMPLETE`

The complete visible semantic unit is contained in one output object/message. No runtime fragment composition or morphology-producing formatter contributes to the sentence.

### `BRANCH_COMPLETE`

Runtime control chooses among alternatives, but every reachable selected output is independently complete and no same-sentence append completes the selected leaf.

Required condition:

```text
append_after = NO
```

for grammatical/sentence completion on the classified output path.

Branch count alone is irrelevant. A branch that selects only an ending or fragment is not `BRANCH_COMPLETE`.

### `VARIABLE_INSERT`

The base sentence is complete apart from inserted runtime data such as a person, place, item, technique, or fixed numeric value. The inserted value does not itself choose Korean morphology.

The decisive discriminator from `FRAGMENT_COMPOSED` is source provenance:

```text
runtime data value -> VARIABLE_INSERT
message/string-table fragment -> FRAGMENT_COMPOSED
```

### `PARTICLE_SENSITIVE_INSERT`

A runtime inserted value can change the required Korean particle or other adjacent morphology based on pronunciation/ending/semantic class, and that morphology is not already resolved independently.

Japanese particle adjacency is a risk detector, not a final classifier. `は/が/を/に/と/へ` or analogous adjacency may raise `PARTICLE_RISK`, but the final mechanism classification requires Korean composition context.

Do not guess the Korean reading of a Japanese-retained name solely to choose a particle.

### `NUMERIC_COUNTER_FORMAT`

A numeric runtime value participates in dynamic counter/unit/morphology selection or number-format behavior rather than merely filling a fixed numeric slot.

A number followed by a fixed literal unit remains `VARIABLE_INSERT` when no dynamic counter decision exists.

### `FRAGMENT_COMPOSED`

The final visible sentence/semantic unit is formed by joining two or more message/string-table fragments, but no grammar-producing formatter has yet been proven to own Korean morphology.

This class is deferred by default because cross-fragment Korean responsibility must be established over the complete composition graph.

### `GRAMMAR_FORMATTER`

Runtime logic contributes Korean grammatical form: particle, copula, verb stem/`하다` realization, ending, honorific/register, interrogative form, speech-style morphology, relation-dependent morphology, or equivalent inflectional responsibility.

Known malformed families such as C73/C188/C342-like composition remain here until family-wide contracts are proven.

### `NAME_COMPOSED`

Visible identity is assembled from surname/given-name/yomi/title/alias or equivalent identity fields.

First-release default is Japanese retention unless a separate scope explicitly promotes the family.

### `MECHANISM_MIXED`

Two or more different generation mechanisms are proven to coexist in one indivisible physical owner/output responsibility and cannot yet be represented by a single preceding class.

This is a resolved structural finding, not a synonym for unknown.

## 6. Axis B — usage

Every candidate receives exactly one `usage_class`.

```text
UI_DESCRIPTION
NARRATION_SYSTEM
DIALOGUE
IDENTITY
OTHER
```

Definitions:

- `UI_DESCRIPTION`: person/region/item/technique descriptions, help, explanatory UI text, and comparable information text.
- `NARRATION_SYSTEM`: event narration, result messages, system/event context, objectives, and non-dialogue event information.
- `DIALOGUE`: spoken/internal dialogue and conversation output.
- `IDENTITY`: person/place/yomi/name/date-identity presentation excluded from the first-release Korean requirement.
- `OTHER`: valid content that does not fit the four primary product roles.

Usage does not imply mechanism. A narration can be `VARIABLE_INSERT`; a UI description can be `STATIC_COMPLETE`; dialogue can be any mechanism class.

## 7. Axis C — investigation status

Every candidate receives exactly one `investigation_status`.

```text
RESOLVED
CALLER_UNKNOWN
NOT_INVESTIGATED
```

- `RESOLVED`: evidence is sufficient to apply the mechanism/owner/disposition rules for the current release decision.
- `CALLER_UNKNOWN`: candidate is known but all relevant callers/owner relationships are not closed.
- `NOT_INVESTIGATED`: structural classification has not been performed.

`CALLER_UNKNOWN` and `NOT_INVESTIGATED` derive `UNRESOLVED`; they are not permanent mechanism classes.

## 8. Mechanism decision inputs

The following are classification inputs, not risk flags.

### `append_after`

```text
YES
NO
UNKNOWN
```

Records whether the classified output is followed, on the same semantic output path, by another append that contributes to the same surface unit.

This field is central to `BRANCH_COMPLETE` versus formatter/fragment classification. `append_after=YES` does not by itself prove grammar formatting; the appended source and responsibility must also be identified.

### `append_after_targets`

List the known post-output append targets/fragments/formatter IDs.

### `variable_source_kind`

```text
RUNTIME_DATA
MESSAGE_FRAGMENT
FIXED_LITERAL
NONE
UNKNOWN
```

This separates runtime insertion from message-fragment composition.

### `insert_followed_by`

Record the source token/character/control immediately following each insertion point when recoverable.

### `jp_particle_adjacency`

```text
YES
NO
UNKNOWN
```

This is an automatically extractable detector that may raise `PARTICLE_RISK`; it is not sufficient by itself to classify `PARTICLE_SENSITIVE_INSERT`.

### `dynamic_counter_decision`

```text
YES
NO
UNKNOWN
```

Only `YES` supports `NUMERIC_COUNTER_FORMAT` rather than ordinary fixed-unit variable insertion.

## 9. Risk and evidence flags

Risk flags are orthogonal to mechanism and usage.

Recommended flags:

```text
PARTICLE_RISK
SHARED_OWNER_RISK
PC_OCCURRENCE_CONFLICT
PC_SPACING_VARIANT
CROSS_MESSAGE_COMPOSITION
BUFFER_CAPACITY_RISK
```

`APPEND_AFTER` is intentionally not a risk flag; it is a mechanism-decision input.

No generic `CONTROL_GRAPH_DEPENDENT` flag is used. Branch-complete output is inherently control-graph dependent, so that flag would not discriminate safety.

### 9.1 `PARTICLE_RISK`

Raised when insertion context may require Korean allomorphy or other morphology that depends on runtime value properties.

### 9.2 `SHARED_OWNER_RISK`

Raised when one Switch physical owner is used by multiple callers with potentially incompatible Korean surface responsibility.

Raw source-text equality does not establish shared ownership. Existing L1/L2/L3 owner provenance should be reused where applicable.

### 9.3 PC occurrence conflict classifier

PC occurrence-specific replacements are normalized only for risk classification; build payload bytes remain untouched.

Normalization for this classifier:

1. remove already-defined trailing NUL padding for logical comparison;
2. classify differences that are solely source-grounded whitespace insertion/removal as spacing variants;
3. preserve all non-whitespace byte ordering and content.

Then:

```text
normalized logical replacements differ -> PC_OCCURRENCE_CONFLICT
only whitespace differs                -> PC_SPACING_VARIANT
```

`PC_OCCURRENCE_CONFLICT` blocks automatic `INCLUDE_KO` until caller/owner context is resolved.

`PC_SPACING_VARIANT` is evidence to inspect layout/caller context but does not itself block `INCLUDE_KO`.

This distinction prevents known spacing-only occurrence variants from being misclassified as semantic conflicts.

### 9.4 `CROSS_MESSAGE_COMPOSITION`

Raised when the candidate is consumed as part of another message/formatter composition or relies on another message to complete its semantic surface.

This flag is required for safe-dialogue gating.

### 9.5 `BUFFER_CAPACITY_RISK`

Raised when selected Korean content does not fit the current proven storage/capacity. It triggers the capacity escalation order; it never authorizes silent translation shortening.

## 10. Physical-owner and shared-caller rule

Classification follows the Switch physical owner.

1. Resolve the physical owner using existing owner provenance where available.
2. Enumerate all known callers of that physical owner.
3. If the physical owner cannot be caller-separated under the existing structure, the most restrictive proven caller governs the owner.
4. If separate physical owners exist, classify them independently even if source bytes/text are identical.
5. If caller topology is incomplete, set `investigation_status=CALLER_UNKNOWN` and derive `UNRESOLVED`.
6. Caller-specific restructuring/redirection is a separate structural escalation, not an automatic classification shortcut.

PC RVA/occurrence splitting is useful as a hazard map but does not prove equivalent Switch ownership.

## 11. Safe dialogue definition

A candidate is `SAFE_DIALOGUE` for R3 only when all of the following are true:

1. `usage_class = DIALOGUE`;
2. `investigation_status = RESOLVED`;
3. `mechanism_class` is one of:
   - `STATIC_COMPLETE`;
   - `BRANCH_COMPLETE`;
   - proven-safe `VARIABLE_INSERT`;
4. all callers of the same Switch physical owner are compatible with the same Korean surface responsibility;
5. no unresolved `PARTICLE_RISK` exists;
6. no unresolved grammar/formatter responsibility exists;
7. `CROSS_MESSAGE_COMPOSITION` is absent;
8. the candidate is not consumed as a formatter/message fragment by another deferred/unsafe composition family;
9. any capacity risk has a separately proven realization.

A line is not safe merely because it looks complete in Korean text data or rendered correctly in one caller.

## 12. Type-specific first-release policy

| Mechanism | R1-R3 default | Required gate |
|---|---|---|
| `STATIC_COMPLETE` | eligible | owner + capacity + evidence resolved |
| `BRANCH_COMPLETE` | eligible | complete leaves, `append_after=NO`, all callers compatible |
| `VARIABLE_INSERT` | conditional | slot semantics fixed, no unresolved particle/morphology risk |
| `PARTICLE_SENSITIVE_INSERT` | defer | Korean grammar/rewriting strategy requires separate closure |
| `NUMERIC_COUNTER_FORMAT` | conditional/defer | dynamic counter semantics proven and Korean result stable |
| `FRAGMENT_COMPOSED` | defer | complete composition graph and Korean responsibility proven |
| `GRAMMAR_FORMATTER` | defer | family-wide Korean grammar contract proven |
| `NAME_COMPOSED` | keep Japanese | first-release identity exclusion |
| `MECHANISM_MIXED` | defer | components and ownership separately closed |

`DEFER_KO` rows must carry a concrete `revisit_condition`. Deferred work must not silently become permanent merely because the current build is playable.

## 13. Required metadata schema

Base row fields:

```text
source_id
source_family
source_container
source_file
source_block
source_message_id
pc_original_payload
pc_korean_payload
switch_physical_owner_id
switch_owner_class
mechanism_class
usage_class
investigation_status
caller_count
caller_list
branch_targets
branch_leaf_completeness
append_after
append_after_targets
variable_kinds
variable_source_kind
insert_followed_by
jp_particle_adjacency
dynamic_counter_decision
nested_formatter_ids
cross_message_consumers
risk_flags
pc_occurrence_count
pc_replacement_variant_count
pc_conflict_class
pc_mechanism
buffer_capacity
ko_payload_length_bytes
evidence_grade
provenance
translation_review_status
derived_disposition
keep_jp_reason
defer_revisit_condition
manual_override
manual_override_reason
notes
```

Container-specific schemas may add fields but must not redefine the meaning of the common fields.

### `pc_conflict_class`

```text
NONE
SPACING_VARIANT
LOGICAL_CONFLICT
UNKNOWN
```

### `evidence_grade`

```text
VERIFIED
OBSERVED
INFERRED
HINT
REJECTED
```

- `VERIFIED`: established with adequate provenance/method for the claim.
- `OBSERVED`: directly observed output/state but not generalized beyond the observed context.
- `INFERRED`: reasoned conclusion supported by evidence but not directly verified.
- `HINT`: useful weak evidence, including runtime observations whose exact target identity is not proven.
- `REJECTED`: a hypothesis/route was tested or contradicted sufficiently that it must not be reused as active support.

Rejected hypotheses remain recorded so later agents do not repeat them.

## 14. Automatic extraction vs manual judgment

This distinction is mandatory before corpus-scale classification.

### 14.1 Automatable or primarily machine-extractable

Where container structure permits, extract automatically:

- source/container/block/message identity;
- control/opcode signature;
- caller/reference edges;
- caller count/list;
- branch targets;
- `append_after` and appended target identity;
- runtime-data vs message-fragment source provenance;
- `insert_followed_by`;
- `jp_particle_adjacency` detector;
- dynamic-counter opcode/path evidence;
- nested formatter IDs;
- cross-message consumer references;
- physical-owner binding when existing canonical owner maps cover the source;
- PC occurrence count;
- PC replacement variants;
- spacing-only vs logical occurrence conflict classification when byte rules suffice;
- byte length and known storage capacity;
- direct provenance identities/hashes.

### 14.2 Manual/semantic judgment

Human or explicit semantic review remains necessary for:

- `usage_class` where role is not structurally encoded;
- whether a branch leaf is semantically complete in Korean;
- whether an insertion truly requires pronunciation-dependent Korean morphology;
- grammatical responsibility across fragments;
- whether dynamic counter behavior produces a stable Korean form;
- semantic equivalence of PC source content to the selected Switch context;
- interpretation of mixed mechanisms;
- manual disposition override;
- translation-quality review during runtime QA.

Do not design a taxonomy that requires thousands of rows to be manually populated with data that can be deterministically extracted.

## 15. Derived disposition

Disposition is computed from classification/evidence. It is not a free-form manual label.

Allowed values:

```text
INCLUDE_KO
DEFER_KO
KEEP_JP
BLOCKED
UNRESOLVED
```

### 15.1 `UNRESOLVED`

Derive when:

- `investigation_status != RESOLVED`;
- physical owner/caller topology required for the decision is unknown;
- a required mechanism input is `UNKNOWN` and affects safety.

`UNRESOLVED` is never releasable.

### 15.2 `KEEP_JP`

Derive when the product intentionally retains original Japanese, especially `IDENTITY` / `NAME_COMPOSED` first-release scope.

`keep_jp_reason` is required.

### 15.3 `DEFER_KO`

Derive when Koreanization is desired but requires a later grammar/composition/structural closure, including unresolved-safe `PARTICLE_SENSITIVE_INSERT`, `FRAGMENT_COMPOSED`, `GRAMMAR_FORMATTER`, or `MECHANISM_MIXED` families.

`defer_revisit_condition` is required.

### 15.4 `BLOCKED`

Use only when evidence proves that the candidate cannot be realized under the currently authorized product architecture and no approved escalation route remains. Capacity failure alone is not `BLOCKED` until the escalation order is exhausted.

### 15.5 `INCLUDE_KO`

Eligible only when:

- investigation is resolved;
- physical owner/callers are sufficiently known;
- mechanism is allowed for the target release phase;
- no blocking grammar/particle/cross-message/shared-owner/logical PC occurrence conflict remains;
- capacity has a proven safe realization;
- source provenance is sufficient.

### 15.6 Manual override

A manual override is exceptional and requires all of:

```text
manual_override = true
manual_override_reason = non-empty
provenance = explicit evidence
```

An override cannot turn missing investigation into proof. `CALLER_UNKNOWN`/`NOT_INVESTIGATED` may not be manually overridden to `INCLUDE_KO`.

## 16. Release phases under the common taxonomy

### R0 — infrastructure

Mapping/font/text transport sufficient for selected Korean content.

### R1 — descriptions

`INCLUDE_KO` rows with `usage_class=UI_DESCRIPTION`.

### R2 — narration/events/system

Add structurally safe `INCLUDE_KO` rows with `usage_class=NARRATION_SYSTEM`, plus event-local non-dialogue rows otherwise mapped to `OTHER` only when their event role is explicitly resolved.

### R3 — safe dialogue

Add only rows satisfying the Safe Dialogue Definition in section 11.

### R4 — optional deferred grammar/composition

Selectively revisit `DEFER_KO` families after their recorded `defer_revisit_condition` is met.

R4 remains optional and cannot block R1-R3.

## 17. Event-schema compatibility

`EVENT_EXTRACTION_SCHEMA.md` remains a source-specific auxiliary schema for event caller/branch metadata. Its `event_structure_class` is not a replacement for the common taxonomy.

New corpus rows must always materialize the common fields in this document.

Legacy event classes map conceptually as follows:

- `EVENT_NARRATION_STATIC` / `EVENT_OBJECTIVE_STATIC` / `EVENT_CHOICE_STATIC` -> usually `STATIC_COMPLETE` plus the appropriate usage;
- `EVENT_BRANCH_LOCAL_SAFE` -> candidate `BRANCH_COMPLETE` only after `append_after=NO` and all-caller closure;
- `EVENT_VARIABLE_SAFE` -> candidate `VARIABLE_INSERT` only after particle/dynamic-counter screening;
- `EVENT_DIALOGUE_STATIC` -> candidate `STATIC_COMPLETE + DIALOGUE`;
- `EVENT_DYNAMIC_GRAMMAR` -> `GRAMMAR_FORMATTER` or `MECHANISM_MIXED` according to actual graph;
- `EVENT_SCRIPT_COMPOSED` -> `FRAGMENT_COMPOSED`, `GRAMMAR_FORMATTER`, or `MECHANISM_MIXED` according to actual responsibility;
- `EVENT_UNKNOWN` -> non-resolved investigation status.

Any legacy `INCLUDE_EVENT_KO`, `INCLUDE_SAFE_DIALOGUE_KO`, `HOLD_DYNAMIC_DIALOGUE`, `KEEP_JP_IDENTITY`, `OUT_OF_SCOPE`, or similar event disposition text is superseded for new rows by the derived disposition model in this document.

## 18. PC occurrence conflict as a hazard map

Do not discard occurrence-level PC patch evidence merely because its implementation is Windows-specific.

Use it to answer:

- did identical/related original content receive context-specific Korean replacements?;
- are differences only spacing/layout?;
- is a Switch physical owner shared across contexts that PC separated by RVA occurrence?;
- does the PC patch reveal a semantic split that the Switch owner model must account for?

Logical conflicts trigger investigation; spacing-only variants do not automatically block release.

## 19. Known rejected approaches

The following are not valid cross-cutting solutions:

- file/container-wide "translate all" classification;
- branch presence alone as unsafe/safe criterion;
- Korean byte-fit alone as safety proof;
- one safe caller as proof for a shared owner;
- raw string uniqueness as owner proof;
- generic `하하 -> 하`, `이이 -> 이`, longest-overlap, or suffix-deletion heuristics;
- global Japanese halfwidth disable;
- mechanical PC runtime-helper transplant;
- capacity failure -> automatic translation shortening;
- treating PC implementation parity as the final product target.

## 20. Recommended classification workflow

```text
source inventory
-> bind Switch physical owner
-> extract caller graph
-> extract mechanism-decision inputs (`append_after`, variable source, insertion adjacency, counter behavior)
-> assign mechanism_class
-> assign usage_class
-> assign investigation_status
-> compute PC occurrence conflict/spacing evidence
-> compute risk flags
-> derive disposition
-> runtime QA for included rows
```

For corpus-scale feasibility, extraction of `append_after`, `insert_followed_by`, caller lists, cross-message consumers, and PC occurrence conflict data should be automated before broad manual classification.

## 21. Current boundary

This design rule creates no patch action, builder change, corpus mutation, IPS, or runtime artifact.

The next recommended read-only scope is:

`SELECTIVE_KO_CROSSCUTTING_AUTOMATABLE_FIELD_INVENTORY_READ_ONLY`

Its goal is to determine, per source family/container, how the common machine-extractable fields can be produced and which existing canonical parsers/owner ledgers can be reused, beginning with `append_after`, caller lists, `insert_followed_by`, cross-message consumer links, and PC occurrence conflict classification.
