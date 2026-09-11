# PC -> Switch Accounting and Cross-Axis Invariants

Date: 2026-09-11
Status: CANONICAL DESIGN CONTRACT / NO IMPLEMENTATION

## 1. Purpose

This document defines the accounting structure and cross-axis invariants required to prove that the complete PC Korean patch has been represented on Nintendo Switch without silent omissions or mutually inconsistent subsystem decisions.

It complements `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`.

The framework answers:

> how should a PC semantic obligation be classified and ported?

This document answers:

> how do we prove that every obligation is represented, every Switch action is valid, and all independently resolved axes still agree when combined?

No builder edit, IPS generation, runtime build, or game-file modification is authorized by this document.

## 2. Three-ledger model

Release accounting consists of three linked ledgers.

```text
LEDGER-1  PC SOURCE ITEM LEDGER
            |
            | source_id -> switch_action_ids
            v
LEDGER-2  SWITCH ACTION LEDGER
            |
            | action/state -> invariant inputs
            v
LEDGER-3  CROSS-AXIS INVARIANT LEDGER
```

All three must close. `LEDGER-1` alone proves coverage, not consistency.

## 3. LEDGER-1 — PC source item ledger

### 3.1 Scope

Every canonical PC source obligation must have one stable row.

Current source denominators are inherited from the framework:

```text
inline records:       17,103
pointer records:          56
mapping entries:      10,036
descriptor containers:    11
descriptor subpatches:     14
helper semantic entries:    2
RomFS package items:      208
```

The overlapping accounting dimensions above remain separately visible where required. For example, descriptor containers and their 14 subpatches are both audited rather than collapsing the latter out of view.

### 3.2 Required fields

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

### 3.3 Source-row closure rule

A source row is closed only when:

- it has a permitted terminal disposition;
- all linked Switch actions exist;
- required evidence fields are present;
- no linked action is itself unresolved/conflicting;
- any `SUBSUMED` row links directly to a final non-`SUBSUMED` action.

A source row may link to multiple Switch actions. Multiple source rows may link to one action. Neither relation changes the source denominator.

## 4. LEDGER-2 — Switch action ledger

### 4.1 Scope

Every actual Switch mutation or explicitly verified no-mutation semantic outcome has one stable action identity.

Actions are object/family level, not raw-match level.

### 4.2 Required fields

```text
switch_action_id
action_family
storage_class
language_domain
switch_object_or_code_sites
input_source_ids
replacement_or_behavior
guards
apply_priority
capacity_requirement
conflict_state
runtime_test_family
status
evidence_ids
```

### 4.3 Referential integrity

Every action must link back to one or more source obligations unless it is an explicitly documented Switch-only infrastructure action required to realize already-linked semantic obligations. Such infrastructure actions still require an owning family and cannot exist as orphan writes.

Every source-linked action must preserve:

- object/field boundaries;
- storage ownership/mutability;
- language-domain rules;
- capacity/alignment constraints;
- required ordering/priority.

## 5. LEDGER-3 — cross-axis invariant ledger

Each invariant has:

```text
invariant_id
scope
inputs
method
expected_condition
status
evidence_or_output
falsification_condition
notes
```

Allowed final statuses:

```text
PASS
FAIL
NOT_APPLICABLE_WITH_EVIDENCE
NOT_RUN
UNKNOWN
```

Only `PASS` or properly evidenced `NOT_APPLICABLE_WITH_EVIDENCE` satisfy release closure.

## 6. INV-1 — final code-space / glyph closure

### Purpose

Prevent independently valid RomFS/main replacements, mapping design, page-mapper behavior and font content from disagreeing on the final Korean code space.

### Required condition

For every Korean code emitted by final patched main data and final RomFS payloads:

```text
emitted code
  -> represented by final semantic mapping
  -> accepted/routed by every required decode/page-selection path
  -> resolves to a valid page/glyph in final FONT_JPN.G1T
```

Equivalent set form:

```text
codes(final main replacements + final RomFS text payloads)
    subset_of codes(final mapping behavior)
    subset_of codes(accepted/routed by required runtime paths)
    subset_of codes(backed by final font glyphs)
```

The exact representation may differ from PC mechanics, but semantic closure must hold.

### Failure examples

- RomFS emits a Korean code absent from mapping;
- mapping contains a code routed to a non-existent font page;
- font has a glyph but one active decode path rejects/drops its encoded byte sequence.

## 7. INV-2 — language-domain isolation

### Purpose

Prevent accidental mutation of CN/TW-only objects or unsafe shared-language objects caused by raw-byte coincidence.

### Required condition

- JP-owned targets may be modified under normal port rules.
- CN/TW-only objects receive zero unauthorized mutations.
- `SHARED_LANGUAGE` objects may change only when the source ledger proves replacement agreement or explicit owner-specific redirection.
- unknown language ownership cannot be silently treated as JP.

The invariant does not assert that all three language copy paths execute at runtime. It checks static ownership and authorized mutation boundaries.

## 8. INV-3 — storage ownership / relocation integrity

### Purpose

Ensure file-time edits target persistent owners rather than loader/runtime products.

### Required condition

- no offline action writes a `RUNTIME_POPULATED` destination as though it were persistent storage;
- RELA-owned references are changed through the correct static owner/addend/reference representation;
- every final relocated/static reference points to a valid object with required alignment/range;
- no action invalidates known object/segment boundaries.

For localization, destination BSS buffers remain runtime products; source-side or proven owner-side representation is authoritative for offline edits.

## 9. INV-4 — source/action cardinality integrity

### Purpose

Prevent PC byte windows and Switch object structures from being silently treated as one-to-one when they are not.

### Required condition

For each source row:

- the declared `1:1 / 1:N / N:1 / N:M` relation is represented explicitly;
- every required split object action exists for `1:N`;
- every collapsed `N:1`/`N:M` action has replacement-agreement or conflict evidence;
- no bytes outside the proven Switch field/object boundary are modified by an action justified only by a narrower PC window.

## 10. INV-5 — overlap and application-order consistency

### Purpose

Prevent individually correct writes from corrupting one another when combined.

### Required condition

- unintended Switch write overlaps = 0;
- every intended overlap has explicit ownership and `apply_priority`;
- source-level PC overlap/order semantics that matter to the final effect are represented even when Switch physical writes differ;
- `SUBSUMED` does not erase a later overriding semantic obligation.

PC `inline=0 / pointer=1 / code=2` is reference ordering evidence, not a requirement to copy Windows mechanics literally.

## 11. INV-6 — mapping consumer algorithm consistency

### Purpose

Ensure the final 10,036-entry mapping representation is valid for every Switch consumer, not merely large enough.

### Required condition

For every semantic mapping consumer:

- table/base source is the intended final representation;
- count/limit covers the intended semantic set;
- lookup algorithm is known sufficiently to prove compatibility;
- ordering/sortedness/index invariants required by that algorithm hold;
- duplicated tables/caches, if any, remain synchronized or are explicitly redirected/subsumed.

A count change alone never satisfies this invariant.

## 12. INV-7 — code-site authorization and containment

### Purpose

Prevent accidental executable-code mutations outside reviewed runtime families.

### Required condition

- every code-byte mutation belongs to a declared `RUNTIME_PORT` action;
- every site is in the enumerated same-semantic counterpart family;
- code segment bytes outside authorized sites remain unchanged;
- guards match canonical input bytes before mutation;
- emitted patch records match the action plan exactly.

## 13. INV-8 — guard / target-identity closure

### Purpose

Preserve the safety obligation of the PC target-identity/fail-closed design in an offline Switch patch workflow.

### Required condition

- output is bound to canonical Title ID/version/Build ID and expected input identity;
- every guard-required action has a guard or stronger format-aware precondition;
- final canonical build has `GUARD_FAIL = 0`;
- `SILENT_GUARD_SKIP = 0`;
- no action is omitted because its preimage failed without the release becoming failed/unresolved.

## 14. INV-9 — final semantic decode / round-trip consistency

### Purpose

Check that final encoded replacement bytes decode back to the intended source-grounded Korean semantics under the final mapping/runtime model.

### Required condition

For every action family for which deterministic decoding is defined:

```text
final encoded bytes
-> final mapping/decode semantics
-> intended PC Korean replacement/control structure
```

Formatter/control tokens are compared structurally, not flattened as display-only text.

This invariant is especially important when storage reconstruction or code-space relocation changes physical bytes while preserving semantic text.

## 15. INV-10 — deterministic build and emitted-patch reproducibility

### Purpose

Ensure accounting results correspond exactly to the artifact later tested/released.

### Required condition

Given identical canonical inputs and source commit:

- inventory/accounting output is deterministic;
- action plan is deterministic;
- built outputs are byte-identical where the build stage is deterministic by design;
- emitted IPS reparses into the exact planned record set;
- artifact hashes and source commit are retained;
- unexpected emitted records = 0.

This invariant becomes executable only after implementation is separately authorized.

## 16. INV-11 — evidence closure for no-edit dispositions

### Purpose

Prevent `NATIVE_EQUIVALENT_VERIFIED`, `SUBSUMED`, or `PROVEN_IRRELEVANT` from becoming escape bins.

### Required condition

Every such source item has:

```text
evidence_ids
scope = STATIC_ONLY | RUNTIME_OBSERVED | BOTH
falsification_condition
final linked action/family where applicable
```

Additional rules:

- `SUBSUMED -> SUBSUMED` chains = 0;
- candidate native-equivalence states are nonterminal;
- evidence fan-out is reported so unusually broad reuse of one evidence item is reviewed rather than silently accepted.

No universal numeric fan-out threshold is fixed here; the validator must expose the distribution and allow the project to set/escalate thresholds based on observed corpus structure.

## 17. Runtime validation matrix

Runtime evidence is attached to rule families, not individual records by default.

For each runtime-required family record:

```text
runtime_test_family
parameter_dimensions
ordinary_case
boundary_case
duplicate_or_shared_case
language_domain_case
storage_class_case
prior_anomaly_case
positive_delivery_control
route_reachability_evidence
regression_case
result
artifact_provenance
```

Only dimensions applicable to that family are required.

### 17.1 Positive control

A positive control proves the currently tested artifact is delivered/applied on the tested route.

### 17.2 Reachability / negative-control requirement

A no-change observation is not causal evidence unless the relevant path is known to have been reached.

Reachability may be proven by:

- prior canonical runtime evidence on that exact path; or
- a dedicated safe sentinel diagnostic whose sole purpose is to prove route consumption.

Do not intentionally mix a route-reachability sentinel with a different root-cause hypothesis in the same diagnostic build unless the sentinel is already established infrastructure and does not alter the semantic hypothesis being tested.

### 17.3 Final integration test

Single-family diagnostics validate causality. A later integration build validates coexistence across previously closed families and is required before release.

## 18. Release closure formula

The project reaches release-accounting closure only when all of the following are true:

```text
SOURCE:
  UNACCOUNTED = 0
  UNRESOLVED  = 0
  CONFLICT    = 0

ACTION:
  orphan actions = 0
  unresolved/conflicting actions = 0
  unintended overlaps = 0
  all guard-required actions guarded

INVARIANTS:
  every required INV-* = PASS
  or explicitly NOT_APPLICABLE_WITH_EVIDENCE

EVIDENCE:
  all high-risk no-edit dispositions have evidence + scope + falsification condition
  SUBSUMED chains = 0

RUNTIME:
  every required family test = PASS
  final integration test = PASS

ARTIFACT:
  guard failures = 0
  silent guard skips = 0
  unexpected emitted records = 0
  provenance complete
```

`100% source coverage` without invariant closure is not release closure.

## 19. Read-only validator output contract

The first authorized implementation of this design should be read-only and produce no IPS/game modifications.

Minimum outputs:

1. canonical source manifest and denominator summary;
2. Switch structural/ownership inventory;
3. source-item ledger;
4. Switch-action proposal ledger;
5. cross-axis invariant ledger;
6. exception queue;
7. evidence fan-out report;
8. coverage/resolution/guard summaries;
9. machine-readable unresolved/conflict list.

The validator must fail closed if input identities do not match canonical project inputs.

## 20. External review provenance rule

Independent reviews are valuable for finding rule-system holes, but measurements first appearing in an external review are not canonical facts until reproduced or otherwise provenance-bound in this repository.

Therefore numeric claims such as counts by PC section, NUL occupancy statistics, or newly measured object populations must be recorded as `REVIEW_CLAIM_UNVERIFIED` until independently reproduced. The logical rule motivated by such a claim may still be adopted when it is valid without depending on the unverified number.

## 21. Current boundary

This document completes the design of the three-ledger accounting and cross-axis consistency gate.

It does not execute the inventories, validate the new invariants against binaries, edit the builder, produce IPS/ZIP artifacts, or authorize a runtime build.

The next stage requires a fresh user execution signal.