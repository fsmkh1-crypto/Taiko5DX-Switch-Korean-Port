# PC -> Switch Full-Port Rule Framework

Date: 2026-09-11
Status: DESIGN BASELINE / NO IMPLEMENTATION

## 1. Purpose

This document defines the rule system for porting the complete PC Korean patch semantics to Nintendo Switch v1.1.3 without silently losing records that do not fit a simple exact-match rule.

The objective is not to maximize automatic match rate. The objective is to make every PC patch input item auditable and force every item into an explicit Switch outcome.

The final release target is reached only when all source items are accounted for and no unresolved semantic obligation remains.

This design reuses canonical facts through R1C and does not itself add new Switch factual validation.

## 2. Canonical PC source denominators

The PC Korean patch must be treated as one integrated package with independent source axes:

- inline records: 17,103
- pointer records: 56
  - mode 0: 5
  - mode 1: 51
  - mode-1 replacement strings: 47 distinct strings in the PC pool
- mapping entries: 10,036
  - original mappings: 7,494
  - Korean additions: 2,542
- runtime descriptors: 11 containers / 14 subpatches
- runtime helper: 158 bytes, with two descriptor-used semantic entries
  - page mapper
  - byte-validation/copy path
- RomFS payload: 208 items in the PC patch package
  - current project path uses 207 direct replacements
  - `CWTDAT_JP.TR5` remains a separate Switch-native reconstruction problem

These are source-accounting denominators. Some source items may collapse into one Switch semantic action, but none may disappear from the accounting.

## 3. Core invariant: source accounting before implementation

Every source item receives a stable identity and exactly one terminal disposition.

Required terminal disposition values:

- `DIRECT_PORT` — same semantic object exists and can be patched directly
- `STRUCTURAL_PORT` — translated through a confirmed Switch table/array/fixed-field/formatter structure
- `REDIRECT_PORT` — Switch requires source/pointer/relocation redirection to a replacement object
- `RUNTIME_PORT` — semantic obligation requires code/runtime behavior rather than a data-only edit
- `NATIVE_EQUIVALENT` — concrete Switch evidence proves no edit is required for the stated semantic obligation
- `SUBSUMED` — this PC item is fully represented by another explicitly linked Switch family action
- `PROVEN_IRRELEVANT` — architecture or data model proves the PC mechanism itself is unnecessary and its semantic effect is already absent/not applicable; evidence is mandatory
- `CONFLICT` — candidate mappings exist but cannot yet be resolved safely
- `UNRESOLVED` — no sufficient Switch disposition yet exists

`SKIPPED`, `NO_MATCH`, `UNIQUE_ONLY_REJECT`, or silent omission are not terminal outcomes.

Release gate:

```text
UNRESOLVED = 0
CONFLICT   = 0
UNACCOUNTED = 0
```

`NATIVE_EQUIVALENT`, `SUBSUMED`, and `PROVEN_IRRELEVANT` require explicit evidence links. They cannot be used as convenience bins.

## 4. Two-layer accounting model

The validator must keep two independent ledgers.

### 4.1 Source-item ledger

Tracks every original PC package item.

Minimum fields:

```text
source_family
source_id
pc_location_or_index
original_bytes_or_semantics
replacement_bytes_or_semantics
semantic_family_id
terminal_disposition
switch_action_id
evidence_ids
runtime_validation_required
notes
```

### 4.2 Switch-action ledger

Tracks each actual Switch action once, even if many PC source items collapse into it.

Minimum fields:

```text
switch_action_id
storage_class
switch_object_or_code_sites
input_source_ids
replacement_or_behavior
guards
capacity_requirement
conflict_state
runtime_test_family
status
```

This prevents both failure modes:

- counting one Switch action many times because many PC records map to it;
- losing PC source records because several records collapse into one Switch object.

## 5. Inline 17,103 classification rules

Inline records are semantic translation inputs, not direct Switch addresses.

Every inline record must first be assigned to a Switch storage class.

### I1 — ordinary bounded string object

Conditions:

- Switch object boundary is independently established;
- replacement is semantically identical to PC replacement;
- replacement fits the Switch object without crossing a terminator/field boundary;
- no incompatible pooling/overlap exists.

Action: `DIRECT_PORT`.

Unique exact match may discover the object, but uniqueness alone is never the rule that authorizes the action.

### I2 — fixed-width / fixed-stride table field

Examples include name/place tables and duplicated fixed records.

Rule:

1. establish table base, stride, field offset and field width;
2. enumerate every structurally corresponding Switch slot;
3. group PC records by semantic object/value;
4. if PC replacements agree, apply the same source-grounded replacement to every corresponding Switch field that represents that semantic object;
5. preserve unrelated fields such as yomi unless separately required.

Action: `STRUCTURAL_PORT`.

A repeated original byte pattern is not grounds for rejection once table structure disambiguates the slots.

### I3 — pooled/shared rodata object with replacement agreement

R1/R1B establish that one rodata byte object can feed multiple localization IDs.

Rule:

- enumerate logical users of the pooled object where structurally recoverable;
- map all relevant PC contexts that correspond to the object;
- if all PC replacements that semantically map to those logical uses agree, one shared source-object patch is allowed subject to boundary/capacity checks.

Action: normally `STRUCTURAL_PORT` through one shared object.

Consumer-by-consumer tracing is not required merely because the object is pooled when replacement agreement and object structure remove semantic ambiguity.

### I4 — pooled/shared rodata object with replacement conflict

If logical uses of one Switch storage object require different PC replacements, the shared source must not be globally overwritten.

Preferred resolution order:

1. reuse an existing Switch replacement object if one already exists;
2. redirect specific localization/source entries or pointer owners to distinct existing objects;
3. otherwise allocate/construct replacement storage and redirect only the conflicting logical owners.

For RELA-materialized localization source slots, implementation must respect loader relocation semantics. A runtime-populated BSS destination cell is not an offline patch target. Per-entry redirection must operate on the static owning pointer/relocation representation or another proven equivalent layer.

Action: `REDIRECT_PORT`.

### I5 — formatter/composite object

Examples: `%s城`, date composites, currency formats.

Rule:

- patch the complete formatter object, never raw suffix substrings;
- preserve format/control tokens and their order/types unless PC evidence proves a semantic change;
- identify formatter families structurally, not by one occurrence;
- PC family correspondence may collapse multiple suffix records into fewer Switch composite objects;
- if the translated formatter cannot fit its current storage, move to `REDIRECT_PORT` rather than truncating or overwriting adjacent data.

Action: `STRUCTURAL_PORT` or `REDIRECT_PORT`.

### I6 — localization logical entry

The 3,803-entry source/destination architecture means rodata identity and logical localization identity are separate dimensions.

Rules:

- do not treat runtime destination buffers as patch storage;
- source-side object patching is allowed when replacement agreement makes all relevant logical uses equivalent;
- logical-entry redirection is required only when uses conflict or when source ownership differs;
- R1C shows the R1B secondary pointer-to-cell selector pattern is sparse, not a universal registry. It must not become a general prerequisite for ordinary localization entries.

Consumer tracing becomes an exception tool, used when structural correspondence/replacement agreement cannot determine the correct action.

### I7 — internal yomi / reading / key fields

Internal reading data is a special semantic class and must not be silently treated as ordinary visible text.

Rules:

- account for every PC source record in this class;
- preserve the PC replacement as source evidence;
- determine whether the Switch field is visible display data, internal sort/input key, or both;
- do not zero or suppress the field as a substitute for a data-port decision;
- if preserving Japanese internal yomi is chosen for Switch safety/behavior, that must be an explicit, evidence-backed disposition for those source records rather than an untracked omission.

Action may be `STRUCTURAL_PORT`, `NATIVE_EQUIVALENT`, or an explicitly documented platform divergence only after evidence supports it.

### I8 — unresolved/unknown storage

Any inline record that cannot be assigned to I1-I7 remains `UNRESOLVED` and enters the exception queue. It is never dropped because it lacks a unique match.

## 6. Inline family compression rule

The analysis unit should be a structural/semantic family whenever possible, not one record at a time.

Family keys may include:

- same PC replacement semantics;
- same Switch table/field class;
- same formatter schema;
- same pooled object ownership;
- same localization logical family;
- same name/alias structure;
- same control-code schema.

A family may be promoted to an automatic rule only after:

1. object structure is established;
2. replacement conflict audit passes;
3. boundary/capacity rule is known;
4. representative positive examples and boundary/duplicate examples are checked;
5. no known counterexample violates the rule.

After promotion, the rule is applied corpus-wide and only exceptions are manually investigated.

## 7. Pointer 56 rules

Pointer records remain first-class source items. They are not automatically absorbed into inline text.

For every pointer record derive:

- PC original semantic target;
- replacement semantic target;
- ownership/sharing relation;
- whether the equivalent Switch object already exists;
- whether Switch uses a direct pointer, RELA entry, table member, localization source slot, or another reference model.

### P1 — pointer target already represented by a patched Switch object

If the Switch reference already points to the correct object and the object itself is ported by an inline/structural action, the PC pointer record becomes `SUBSUMED` with an explicit link to that Switch action.

This is particularly relevant to PC mode-0 records converging on module-resident targets also translated by the inline layer.

### P2 — existing Switch reference requires redirection to existing object

Action: `REDIRECT_PORT`; patch the owning static pointer/relocation representation.

### P3 — replacement string does not exist in Switch

Create/allocate one canonical replacement object per distinct replacement string where sharing is semantically valid, then redirect all owning references.

Action: `REDIRECT_PORT` with explicit capacity accounting.

The PC 602-byte contiguous pool is an implementation detail. Switch may use another representation, but all 47 distinct mode-1 replacement strings must be accounted for.

### P4 — Switch native reference model already provides equivalent semantics

Only classify as `NATIVE_EQUIVALENT` when concrete data/control-flow evidence proves the same target selection behavior. Absence of a visible symptom is insufficient.

## 8. Mapping 10,036 rules

Mapping is one indivisible semantic family for completeness purposes.

Target semantic result:

```text
mapping contents = exact PC semantic 10,036-entry mapping
all relevant lookup/conversion paths reference that complete mapping
all relevant counts/limits cover 10,036 entries
```

Required pre-implementation facts:

1. exact Switch original mapping storage and footprint;
2. all semantic table-base consumers;
3. all semantic count/limit consumers;
4. available capacity or relocation requirement;
5. conversion directions and any duplicated tables/caches.

Implementation rule:

- if original Switch storage cannot hold 10,036 entries, create a safe expanded representation;
- redirect every proven semantic base reference to it;
- change every proven semantic count/limit consistently;
- never edit only the two currently known count literals and assume completeness.

PC descriptor subpatches `mapping_lookup_1/2` are source-accounted as `SUBSUMED` by this mapping-family action once their semantic obligations are fully represented.

## 9. Runtime helper and descriptor rules

The 11 PC descriptors / 14 subpatches are mapped by semantic family, not x86 byte identity.

Required Switch families:

- mapping address/count behavior — subsumed by mapping family when complete
- runtime page mapper
- runtime byte-validation/copy behavior
- raw font-page/byte threshold behavior
- four width-related semantics
- two description-font argument semantics

For every family the final state must be one of:

- all Switch counterpart sites enumerated and patched;
- `NATIVE_EQUIVALENT` with concrete evidence;
- explicitly `PROVEN_IRRELEVANT` by architecture/semantic analysis.

PC one-site cardinality does not imply one Switch site. One PC semantic change may fan out to many ARM64 sites.

### H1 — page mapper

Existing confirmed Switch mapper behavior is input evidence. Release completion requires a family-level check that all relevant page-selection paths used by the Korean font are covered.

### H2 — byte-validation/copy helper

The known per-character decoder accepting `A1..DF` is not enough by itself.

The rule is to establish whether all source paths capable of carrying compact Korean bytes preserve/copy them equivalently. If an existing ARM64 flow already does so, classify it as native-equivalent. Otherwise patch the full same-cause family.

### H3 — width/font/threshold descriptor families

Use the raw PC behavior as the semantic requirement. Do not infer screen names from stale labels. Enumerate every Switch site serving that same role before deciding the family is complete.

## 10. RomFS 208 rules

Every payload item gets a disposition.

Allowed classes:

- `DIRECT_FILE_REPLACEMENT`
- `SWITCH_NATIVE_RECONSTRUCTION`
- `NATIVE_EQUIVALENT`
- `UNRESOLVED`

Direct replacement requires at minimum:

- same intended relative resource role/path;
- no known format/version incompatibility;
- package/runtime path acceptance where tested;
- retained source/output identity.

Current special rule:

- `CWTDAT_JP.TR5` must not be blindly copied for release. Reconstruct PC semantic changes onto the Switch-native structure unless later structural proof establishes whole-file compatibility.

The Korean font remains part of the same total accounting even though its current path is already implemented/tested.

## 11. Exception queue

Any automatic rule failure creates a persistent exception record with a stable reason code.

Suggested reason codes:

```text
E_OBJECT_UNKNOWN
E_MULTI_CANDIDATE
E_POOL_CONFLICT
E_REPLACEMENT_CONFLICT
E_FIELD_WIDTH
E_FORMAT_SCHEMA
E_CONTROL_SCHEMA
E_POINTER_OWNER_UNKNOWN
E_NEEDS_STORAGE
E_RUNTIME_COUNTERPART_UNKNOWN
E_NATIVE_EQUIVALENCE_UNPROVEN
E_ROMFS_STRUCTURE_MISMATCH
```

An exception may leave the queue only by being assigned a terminal disposition with evidence.

The queue is the main worklist after bulk rules are applied. The project should not return to scanning the entire corpus manually after each discovery.

## 12. Runtime validation policy

Runtime testing is a rule-family validator, not a substitute for corpus accounting.

Runtime testing is required when any of the following is true:

- new storage or pointer/RELA redirection is introduced;
- a pooled/shared object has multiple logical users;
- static evidence cannot distinguish competing consumer/source choices;
- a formatter/composite family has been reconstructed;
- a runtime code family (mapping/helper/descriptor) changes;
- native-equivalence is materially dependent on observed behavior;
- a previous runtime anomaly is being claimed resolved.

Runtime testing is not automatically required for every individual record after a structural rule has been established.

Per diagnostic build:

- one root-cause/rule family only;
- include all proven sites of that family;
- preserve original-byte guards;
- reparse emitted IPS and verify exact planned records;
- bind source commit, IPS/package hashes and runtime observation per provenance policy.

Representative runtime coverage should include:

- a positive-control path proving current artifact delivery;
- one ordinary family member;
- one duplicate/repeated boundary member where applicable;
- one previously failing/anomalous route when the family is intended to fix it;
- a regression route proving no nearby behavior was broken.

## 13. Coverage metrics

The builder/validator should emit two coverage summaries.

### Source coverage

```text
INLINE:     17,103 / 17,103 dispositions
POINTER:        56 / 56 dispositions
MAPPING:    10,036 / 10,036 semantic entries represented
DESCRIPTOR:     11 / 11 containers and 14 / 14 subpatches represented
HELPER:          2 / 2 semantic entries represented
ROMFS:         208 / 208 items represented
```

### Resolution coverage

For every axis show counts by disposition:

```text
DIRECT_PORT
STRUCTURAL_PORT
REDIRECT_PORT
RUNTIME_PORT
NATIVE_EQUIVALENT
SUBSUMED
PROVEN_IRRELEVANT
CONFLICT
UNRESOLVED
```

A high automatic percentage is useful but is not a release gate. The release gate is zero conflict/unresolved/unaccounted.

## 14. Conflict rules

Never resolve a conflict by:

- first match;
- nearest address;
- longest match;
- arbitrary language-table assumption;
- replacement popularity;
- a raw localization numeric index hit;
- one successful screen observation.

Resolution requires independent structure, semantic correspondence, or targeted runtime discrimination.

## 15. Consumer-tracing policy after R1C

Consumer tracing is not the default workflow for every text object.

Use it only when one of these conditions holds:

- multiple Switch logical owners require different replacements;
- active slot/alias selection changes which stored object is displayed;
- a runtime symptom contradicts the structural mapping;
- pointer ownership cannot be established statically;
- two valid storage candidates remain after structural rules.

R1C established that the R1B secondary pointer-to-cell table pattern is sparse, so searching for that exact pattern across ordinary localization entries is not a universal porting rule.

## 16. Recommended execution sequence

### Stage A — freeze full PC source inventory

Generate stable IDs and normalized source manifests for every source axis.

No source item may enter implementation without being present in this inventory.

### Stage B — build Switch structural inventory

Create reusable indices for:

- bounded strings;
- fixed fields / fixed-stride arrays;
- rodata pools and RELA owners;
- localization source entries/logical IDs;
- formatter/control schemas;
- pointer/reference owners;
- mapping tables/consumers;
- descriptor/helper counterpart families;
- RomFS resource identity/layout.

### Stage C — apply general rules corpus-wide

Apply I1-I8, P1-P4, mapping/runtime/RomFS rules in bulk.

Output:

- resolved action set;
- exception queue;
- exact accounting totals.

### Stage D — investigate exceptions only

Prioritize by impact:

1. conflicts that block many source items;
2. common structural family gaps;
3. runtime/code families;
4. isolated residuals.

When one exception reveals a new reusable structural rule, promote the rule and rerun the whole corpus rather than patching that one item locally.

### Stage E — implementation plan

Only after rule/accounting coverage is stable, convert resolved Switch actions into guarded builder transformations.

This requires a fresh user execution signal.

### Stage F — family runtime validation

Validate newly implemented rule families with provenance-bound diagnostic builds as required by section 12.

### Stage G — final closure audit

Release candidate requires:

```text
UNACCOUNTED = 0
UNRESOLVED  = 0
CONFLICT    = 0
silent guard skips = 0
unexpected emitted records = 0
```

Every `NATIVE_EQUIVALENT`, `SUBSUMED`, or `PROVEN_IRRELEVANT` source item must link to its evidence/action.

## 17. Practical consequence for current project direction

The project should stop treating individual visible strings as the normal unit of progress.

The normal unit becomes:

```text
PC semantic family
-> Switch storage/behavior class
-> general porting rule
-> corpus-wide application
-> exception queue
```

Individual consumer tracing and runtime discrimination are escalation tools for exceptions, not prerequisites for porting all 17,103 inline records.

This preserves the user's two requirements simultaneously:

1. move toward applying the whole PC patch rather than endlessly deepening one hypothesis;
2. prevent holes by proving total source accounting instead of assuming unmatched records are harmless.

## 18. Current implementation boundary

This document authorizes no builder edit, IPS generation, runtime build, or game-file modification by itself.

The next implementation-oriented stage should first create the inventory/accounting validator and run it read-only against the existing canonical inputs. Any patch generation remains a later, separately authorized stage.
