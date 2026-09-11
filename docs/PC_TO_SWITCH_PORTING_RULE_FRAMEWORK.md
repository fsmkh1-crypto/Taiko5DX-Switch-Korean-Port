# PC -> Switch Full-Port Rule Framework

Date: 2026-09-11
Status: DESIGN BASELINE / NO IMPLEMENTATION

## 1. Purpose

This document defines the rule system for porting the complete PC Korean patch semantics to Nintendo Switch v1.1.3 without silently losing records that do not fit a simple exact-match rule.

The objective is not to maximize automatic match rate. The objective is to make every PC patch input item auditable, force every item into an explicit Switch outcome, and then prove that the outcomes are mutually consistent across text, pointers, mapping, runtime code, font, and RomFS.

The final release target is reached only when:

1. every PC source obligation is accounted for;
2. every required Switch action is resolved;
3. cross-axis invariants all pass;
4. evidence-backed runtime validation required by each rule family passes.

This design reuses canonical facts through R1C. It does not convert external-review measurements or unverified counts into project facts.

Detailed three-ledger schema and release invariants are defined in `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`.

## 2. Canonical PC source denominators

The PC Korean patch is one integrated package with independent source axes:

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
- RomFS payload: 208 package items
  - current project model: 207 direct-replacement-path items
  - `CWTDAT_JP.TR5` is the remaining separate Switch-native reconstruction item

These are source-accounting denominators. Some source items may collapse into one Switch semantic action, while one PC byte window may require multiple Switch actions. Neither case permits a source item to disappear from accounting.

If any denominator is later changed, that change requires its own provenance-backed inventory result. A review-only number is never allowed to silently replace a canonical denominator.

## 3. Terminal dispositions and release meaning

Every source item receives a stable identity and exactly one terminal disposition.

Allowed terminal dispositions:

- `DIRECT_PORT` — one confirmed Switch object can receive the same semantic replacement directly
- `STRUCTURAL_PORT` — replacement is applied through a confirmed Switch table/array/field/formatter structure
- `REDIRECT_PORT` — the Switch owner/reference/relocation must point to another replacement object
- `RUNTIME_PORT` — the semantic obligation requires code/runtime behavior rather than a data-only edit
- `NATIVE_EQUIVALENT_VERIFIED` — concrete Switch evidence proves equivalent semantics within an explicit scope and no edit is required
- `SUBSUMED` — the source item is fully represented by another explicitly linked non-`SUBSUMED` terminal Switch action
- `PROVEN_IRRELEVANT` — architecture/data-model evidence proves the PC mechanism is not applicable and no equivalent semantic obligation remains on Switch
- `CONFLICT` — multiple candidate outcomes remain and cannot yet be safely selected
- `UNRESOLVED` — no sufficient Switch disposition exists yet

Non-terminal evidence states may include `NATIVE_EQUIVALENT_CANDIDATE`, but a candidate never satisfies release accounting.

`SKIPPED`, `NO_MATCH`, `UNIQUE_ONLY_REJECT`, silent omission, and evidence-free `NATIVE_EQUIVALENT` are forbidden terminal outcomes.

Coverage alone is not the release gate. Final closure requires:

```text
UNACCOUNTED = 0
UNRESOLVED  = 0
CONFLICT    = 0
ALL REQUIRED CROSS-AXIS INVARIANTS = PASS
ALL REQUIRED GUARDS = PRESENT AND PASS
ALL REQUIRED RUNTIME FAMILY TESTS = PASS
```

## 4. Three-layer accounting model

The validator must keep three independent but linked ledgers.

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
language_domain
storage_mutability
window_object_cardinality
terminal_disposition
switch_action_ids
evidence_ids
evidence_scope
falsification_condition
runtime_validation_required
notes
```

### 4.2 Switch-action ledger

Tracks every actual Switch action exactly once, even if many PC source items collapse into it or one source item fans out to multiple actions.

Minimum fields:

```text
switch_action_id
action_family
storage_class
switch_object_or_code_sites
input_source_ids
replacement_or_behavior
guards
apply_priority
capacity_requirement
conflict_state
runtime_test_family
status
```

### 4.3 Cross-axis invariant ledger

Tracks conditions that cannot be proven from either source coverage or action coverage alone.

Examples include:

- emitted code/glyph closure across main/RomFS -> mapping -> page mapper -> font;
- language-domain isolation;
- relocation/reference validity;
- overlap/priority consistency;
- approved-code-site containment;
- mapping algorithm/order assumptions;
- deterministic output and emitted IPS round-trip.

The canonical invariant definitions live in `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`.

This three-ledger model prevents three different failures:

- one Switch action counted many times because many PC records map to it;
- PC source records lost because several collapse into one Switch object;
- individually plausible actions combined into an internally inconsistent final patch.

## 5. Universal preclassification gates

These gates run before I1-I8 or any automatic inline classification. They are not special cases of pooled strings.

### G1 — language-domain ownership

For localization-backed objects, use the three verified 3,803-entry source tables and their RELA ownership to label source-object use.

Allowed labels:

```text
JP
CN
TW
SHARED_LANGUAGE
NON_LOCALIZATION
UNKNOWN
```

Rules:

- `JP`: eligible for Korean-port analysis.
- `CN`/`TW`: never modify merely because bytes match a PC record.
- `SHARED_LANGUAGE`: requires an explicit replacement-agreement and active-path/ownership audit before a shared object can be modified.
- `NON_LOCALIZATION`: allowed only when independent object structure proves that the object is outside the localization-language ownership model.
- `UNKNOWN`: cannot receive an automatic safe disposition.

The existence of the JP/CN/TW copy blocks is VERIFIED. Which language path is active in a given runtime context must not be inferred solely from their existence.

Language-domain labeling must extend beyond the localization tables by independent structure when possible; absence from the 3-table registry alone does not automatically mean either `NON_LOCALIZATION` or `UNKNOWN` without supporting evidence.

### G2 — storage mutability / ownership

Every Switch target is classified before patch authorization:

```text
STATIC_RODATA
STATIC_DATA
RELA_OWNED_REFERENCE
RUNTIME_POPULATED
CODE
UNKNOWN
```

Rules:

- `STATIC_RODATA` / proven static field data may be patchable subject to boundary/capacity rules.
- `RELA_OWNED_REFERENCE`: patch the owning static object/RELA addend/reference representation, not a loader-populated cell as if it were persistent file storage.
- `RUNTIME_POPULATED`: never an offline data target; trace upward to its static source/owner or use a proven runtime action.
- `CODE`: editable only through an explicitly authorized runtime/descriptor action family.
- `UNKNOWN`: remains unresolved.

This gate applies to I1-I8, pointer records, localization source entries, and any data object reached from them.

### G3 — PC-window -> Switch-object cardinality

A PC inline record is a byte window, not automatically a semantic object boundary.

Before applying a rule, establish the relation between that PC window and Switch objects:

```text
1:1
1:N
N:1
N:M
0:?
```

Rules:

- `1:1`: normal I1-I8 classification may proceed.
- `1:N`: split the PC obligation into object-level Switch actions while retaining one source record linked to all resulting actions.
- `N:1`: multiple PC source items may collapse into one Switch action only after replacement-agreement/conflict auditing.
- `N:M`: requires a structural family rule; no independent raw-byte patching.
- no established target set: `UNRESOLVED`.

If a Switch object is larger than the PC window, direct partial overwrite is forbidden unless an exact subfield boundary is independently established. Otherwise promote to `STRUCTURAL_PORT`, `REDIRECT_PORT`, or `UNRESOLVED`.

## 6. Inline 17,103 classification rules

Inline records are semantic translation inputs, not direct Switch addresses.

`DIRECT_PORT` and `STRUCTURAL_PORT` have the same evidence standard: independent object/field boundaries, semantic correspondence, capacity safety, and conflict audit. `DIRECT_PORT` means structurally simple, not evidentially weaker.

### I1 — ordinary bounded string object

Conditions:

- G1-G3 are resolved;
- object boundary is independently established;
- replacement is semantically identical to the PC replacement;
- replacement fits without crossing a terminator/field boundary;
- no incompatible pooling/overlap exists.

Action: `DIRECT_PORT`.

Unique exact match may discover the object, but uniqueness alone never authorizes the action.

### I2 — fixed-width / fixed-stride table field

Rule:

1. establish table base, stride, field offset and field width;
2. enumerate every structurally corresponding Switch slot;
3. group PC records by semantic object/value;
4. audit 1:N/N:1/N:M cardinality explicitly;
5. if PC replacements agree, apply the source-grounded replacement to every corresponding Switch field for that semantic object;
6. preserve unrelated fields such as yomi unless separately required.

Action: `STRUCTURAL_PORT`.

Repeated raw bytes are not grounds for rejection once table structure disambiguates the slots.

### I3 — pooled/shared object with replacement agreement

Rule:

- enumerate structurally recoverable logical users;
- map all relevant PC contexts to the object;
- confirm language-domain compatibility;
- if all corresponding PC replacements agree, one shared source-object action is permitted subject to mutability, boundary and capacity checks.

Action: normally `STRUCTURAL_PORT` through one shared object.

Consumer-by-consumer tracing is not required merely because the object is pooled when structure and replacement agreement remove ambiguity.

### I4 — pooled/shared object with replacement conflict

A shared source must not be globally overwritten when logical uses require different PC replacements.

Preferred resolution order:

1. reuse an existing safe replacement object;
2. redirect specific source entries/pointer owners/relocations to distinct existing objects;
3. otherwise create replacement storage and redirect only conflicting owners.

Runtime-populated destination buffers are not offline patch targets. Static owning pointer/relocation representations or another proven equivalent layer must be used.

Action: `REDIRECT_PORT`.

### I5 — formatter/composite object

Examples: `%s城`, date composites, currency formats.

Rule:

- patch/reconstruct the complete formatter object, never global suffix substrings;
- preserve format/control tokens and token ordering/types unless PC evidence proves a semantic change;
- identify formatter families structurally;
- allow N:1 or N:M family collapse only with explicit source-to-action links;
- if translated form cannot fit current storage, use `REDIRECT_PORT` rather than truncating or overwriting adjacent data.

Action: `STRUCTURAL_PORT` or `REDIRECT_PORT`.

### I6 — localization logical entry

The verified 3,803-entry architecture means rodata identity and logical localization identity are separate dimensions.

Rules:

- runtime destination buffers are not patch storage;
- source-side object patching is allowed when G1/G2 pass and replacement agreement makes relevant logical uses equivalent;
- logical-entry redirection is required only when uses conflict or ownership differs;
- R1C proves the R1B secondary pointer-to-cell selector pattern is sparse and must not become a universal prerequisite.

Consumer tracing is an exception tool when structure/replacement agreement cannot determine the correct action.

### I7 — internal yomi / reading / key fields

Rules:

- account for every PC source record in this class;
- preserve PC replacement as source evidence;
- determine whether the Switch field is visible display data, internal sort/input key, or both;
- do not zero/suppress the field as a substitute for a porting decision;
- a deliberate Japanese-internal-yomi divergence requires an explicit evidence-backed disposition and scope.

### I8 — unresolved/unknown storage

Any inline record that cannot pass G1-G3 and be assigned safely to I1-I7 remains `UNRESOLVED`. It is never dropped because it lacks a unique match.

## 7. Inline family compression rule

The normal analysis unit is a structural/semantic family, not one record at a time.

A family may be promoted to an automatic rule only after:

1. object structure and G1-G3 classification are established;
2. replacement conflict audit passes;
3. boundary/capacity rule is known;
4. family parameter dimensions are listed;
5. representative ordinary, boundary, duplicate/shared and storage-class cases are checked as applicable;
6. no known counterexample violates the rule.

After promotion, apply the rule corpus-wide and investigate only exceptions. A new reusable rule discovered from one exception must be rerun over the whole corpus.

## 8. Pointer 56 rules

Pointer records remain first-class source items and are never silently absorbed into inline text.

For every pointer record derive:

- PC original semantic target;
- replacement semantic target;
- ownership/sharing relation;
- whether the Switch object already exists;
- Switch reference model: direct pointer, RELA entry, table member, localization source slot, or other proven owner.

### P1 — target already represented by a ported Switch object

If the Switch reference already points to the correct object and that object is ported by another action, the pointer record may become `SUBSUMED` only with an explicit link to the final non-`SUBSUMED` action.

`SUBSUMED -> SUBSUMED` chains are forbidden.

### P2 — reference requires redirection to existing object

Action: `REDIRECT_PORT`; patch the owning static reference/relocation representation.

### P3 — replacement string does not exist in Switch

Create one canonical replacement object per distinct replacement string where sharing is semantically valid, then redirect all owners.

Action: `REDIRECT_PORT` with explicit capacity accounting.

The PC 602-byte pool is an implementation detail; the 47 distinct mode-1 replacement strings remain source obligations.

### P4 — native equivalent

Use `NATIVE_EQUIVALENT_VERIFIED` only when concrete Switch evidence proves equivalent target-selection semantics within a recorded scope and falsification condition.

## 9. Mapping 10,036 rules

Mapping is one indivisible semantic family for completeness purposes.

Target result:

```text
mapping contents = exact PC semantic 10,036-entry mapping
all relevant lookup/conversion paths reference that complete mapping
all relevant counts/limits cover 10,036 entries
all algorithmic/order assumptions required by those consumers remain valid
```

Required pre-implementation facts:

1. exact Switch original mapping storage and footprint;
2. every semantic table-base consumer;
3. every semantic count/limit consumer;
4. available capacity or relocation requirement;
5. conversion directions and duplicated tables/caches;
6. lookup algorithm used by each consumer (linear/binary/direct/other);
7. any ordering/sortedness/index invariants required by those consumers.

Implementation rule:

- if original Switch storage cannot hold 10,036 entries, create a safe expanded representation;
- redirect every proven semantic base reference to it;
- change every proven semantic count/limit consistently;
- preserve consumer-required ordering/index properties;
- never edit only currently known count literals and assume completeness.

PC descriptor mapping subpatches become `SUBSUMED` only after the mapping-family action fully represents their semantic obligations.

## 10. Runtime helper and descriptor rules

The 11 descriptors / 14 subpatches are mapped by semantic family, not x86 byte identity.

Required Switch families:

- mapping address/count behavior;
- runtime page mapper;
- runtime byte-validation/copy behavior;
- raw font-page/byte threshold behavior;
- four width-related semantics;
- two description-font argument semantics.

For every family, final state must be:

- all required Switch counterpart sites enumerated and represented by `RUNTIME_PORT`; or
- `NATIVE_EQUIVALENT_VERIFIED`; or
- `PROVEN_IRRELEVANT` with architecture/semantic proof.

PC one-site cardinality does not imply one Switch site.

### H1 — page mapper

Existing confirmed Switch mapper behavior is input evidence. Completion requires a family-level check that every relevant page-selection path used by the final Korean code space is covered.

### H2 — byte-validation/copy helper

A known decoder accepting one relevant byte range is not enough by itself. Establish whether all source paths capable of carrying compact Korean bytes preserve/copy them equivalently.

### H3 — width/font/threshold families

Use raw PC behavior as the semantic requirement. Do not infer screen names from stale labels. Enumerate every Switch site serving the same role before closure.

## 11. RomFS 208 rules

The canonical package denominator remains 208 items unless a separately validated inventory changes it.

Current project accounting model:

```text
207 direct-replacement-path items
+ 1 CWTDAT_JP.TR5 Switch-native reconstruction item
= 208 package items
```

Every item receives a disposition:

- `DIRECT_FILE_REPLACEMENT`
- `SWITCH_NATIVE_RECONSTRUCTION`
- `NATIVE_EQUIVALENT_VERIFIED`
- `UNRESOLVED`

Direct replacement requires at minimum:

- same intended resource role/path;
- no known format/version incompatibility;
- package/runtime path acceptance where tested;
- retained source/output identity.

`CWTDAT_JP.TR5` must not be blindly copied for release unless later structural proof establishes whole-file compatibility. The Korean font remains inside total accounting even when its current path is already implemented/tested.

## 12. Evidence-strength rules

`NATIVE_EQUIVALENT_VERIFIED`, `SUBSUMED`, and `PROVEN_IRRELEVANT` are high-risk closure dispositions and require:

```text
evidence_ids
scope = STATIC_ONLY | RUNTIME_OBSERVED | BOTH
falsification_condition
linked final switch_action_id where applicable
```

Rules:

- absence of a visible symptom is not evidence of native equivalence;
- a candidate state does not satisfy release closure;
- `SUBSUMED` chains are forbidden;
- one weak evidence item must not silently justify a large source family. The validator must report evidence fan-out so unusually broad reuse is manually reviewed;
- external-review measurements remain proposals until reproduced with provenance in this repository.

## 13. Guard / transaction safety axis

PC target-identity and guarded-commit mechanics are not literal Switch patch content, but their safety obligation must survive in the offline port.

Required release safety behavior:

- bind output to canonical Switch Title ID/version/Build ID and expected input identity;
- every action that edits bytes must have an original/preimage guard unless a documented format-aware transformation provides an equivalent stronger guard;
- no silent guard skip is allowed;
- intended overlapping actions must declare ordering/priority;
- unintended overlaps are release-blocking conflicts;
- source-level PC overlap relations that encode semantic ordering must be retained as provenance even if Switch implementation does not use the same physical overlap.

`apply_priority` belongs in the Switch-action ledger. PC `inline=0 / pointer=1 / code=2` is reference semantics, not a command to reproduce Windows write mechanics literally.

## 14. Exception queue

Any automatic-rule failure creates a persistent exception record with a stable reason code. Existing reason codes may be retained; the exact taxonomy is operational rather than a release invariant.

An exception leaves the queue only by receiving a terminal disposition with evidence. The project must not return to full-corpus manual scanning after each discovery.

## 15. Runtime validation policy

Runtime testing validates rule families; it never substitutes for corpus accounting.

Runtime testing is required when, among other cases:

- new storage or pointer/RELA redirection is introduced;
- a pooled/shared object has multiple logical users;
- static evidence cannot distinguish competing source/consumer choices;
- a formatter/composite family is reconstructed;
- a runtime code family changes;
- native equivalence materially depends on runtime behavior;
- a previous runtime anomaly is claimed resolved.

Per diagnostic build:

- one root-cause/rule family only;
- include all proven same-cause sites;
- preserve guards;
- reparse emitted IPS and verify the exact plan;
- bind source commit, artifact hashes and runtime observation.

Family validation must define its parameter space. Representative cases should cover the meaningful extremes for that family, such as duplicate slots, boundary lengths, language domain, storage class, pooled ownership, and prior anomaly routes.

A no-change runtime result may be used as evidence only when route reachability is independently demonstrated. Reachability may be established by prior verified observation or by a dedicated safe sentinel/negative-control diagnostic. Do not interpret an unproven-unreached route as successful native equivalence.

Integration testing across previously validated families is a final release requirement and is distinct from single-family diagnostic builds.

## 16. Coverage metrics

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

Report counts by disposition, with `NATIVE_EQUIVALENT_CANDIDATE` shown separately as nonterminal.

### Guard coverage

Report:

```text
GUARD_REQUIRED_ACTIONS
GUARDED_ACTIONS
GUARD_PASS
GUARD_FAIL
SILENT_GUARD_SKIP
```

Release requires every guard-required action to be guarded, `GUARD_FAIL=0`, and `SILENT_GUARD_SKIP=0` for the final canonical input.

### Invariant coverage

Every required invariant in `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md` must report `PASS`. `NOT_RUN`, `UNKNOWN`, or `WAIVED` do not satisfy release closure unless the invariant definition itself marks the condition non-applicable with evidence.

## 17. Conflict rules

Never resolve a conflict by:

- first match;
- nearest address;
- longest match;
- arbitrary language-table assumption;
- replacement popularity;
- raw localization numeric-index hits;
- one successful screen observation.

Resolution requires independent structure, semantic correspondence, or targeted runtime discrimination.

## 18. Consumer-tracing policy after R1C

Consumer tracing is not the default workflow for every text object.

Use it only when:

- multiple logical owners require different replacements;
- active slot/alias selection changes displayed storage;
- runtime symptoms contradict structural mapping;
- pointer ownership cannot be established statically;
- two valid storage candidates remain after general rules.

R1C established that the R1B secondary pointer-to-cell table pattern is sparse, so that exact structure is not a universal porting prerequisite.

## 19. Recommended execution sequence

### Stage A — freeze full PC source inventory

Generate stable IDs and normalized manifests for every source axis. No source item enters implementation without inventory membership.

### Stage B0 — build prerequisite Switch ownership indices

Before bulk mapping, establish reusable indices for:

- language-domain ownership;
- storage mutability/relocation ownership;
- object/field boundaries;
- PC-window -> Switch-object cardinality;
- bounded strings and fixed-stride arrays;
- localization source entries/logical IDs;
- formatter/control schemas;
- pointer/reference owners;
- mapping consumers/algorithms/order assumptions;
- runtime counterpart families;
- RomFS identity/layout.

### Stage B1 — run static cross-axis invariants available before implementation

At minimum run all invariants that can be evaluated from canonical existing inputs, especially code-space/font closure where the necessary mapping/font/RomFS inputs already exist.

A failure here changes the design before bulk classification rather than after implementation.

### Stage C — apply general rules corpus-wide

Apply G1-G3, I1-I8, P1-P4 and mapping/runtime/RomFS rules in bulk.

Output:

- source ledger;
- Switch-action ledger;
- invariant ledger;
- exception queue;
- exact accounting totals.

### Stage D — investigate exceptions only

Prioritize high-impact conflicts and common structural families before isolated residuals. When one exception yields a reusable rule, promote it and rerun the whole corpus.

### Stage E — implementation plan

Only after rule/accounting coverage and prerequisite invariants are stable, convert resolved actions into guarded builder transformations. This requires a fresh user execution signal.

### Stage F — family runtime validation

Validate implemented rule families under section 15.

### Stage G — integration and final closure audit

Release candidate requires:

```text
UNACCOUNTED = 0
UNRESOLVED  = 0
CONFLICT    = 0
all required invariants = PASS
all required guards = PASS
silent guard skips = 0
unexpected emitted records = 0
required family runtime tests = PASS
integration runtime test = PASS
```

Every high-risk closure disposition must have evidence, scope and falsification condition.

## 20. Practical project direction

The normal unit of progress is now:

```text
PC semantic family
-> Switch ownership/storage class
-> general porting rule
-> corpus-wide application
-> cross-axis consistency check
-> exception queue
```

Individual visible strings, consumer tracing and runtime discrimination are escalation tools for unresolved exceptions, not the normal unit of progress.

This preserves both project requirements:

1. move toward applying the whole PC patch instead of endlessly deepening one hypothesis;
2. prevent holes by proving total accounting and cross-axis consistency rather than assuming unmatched or independently plausible records are harmless.

## 21. Current implementation boundary

This document authorizes no builder edit, IPS generation, runtime build, or game-file modification.

The next implementation-oriented stage should first create the read-only inventory/accounting/invariant validator against canonical inputs. Patch generation remains a later, separately authorized stage.