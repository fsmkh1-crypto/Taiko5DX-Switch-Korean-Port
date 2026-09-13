# PORTABILITY MATRIX AND ACTION LEDGER DESIGN

Date: 2026-09-13 (KST)
Status: CANONICAL DESIGN CONTRACT / NO IMPLEMENTATION
Basis HEAD: `3994f5b5d3aa3b508b8d7941312b4199d47f6374`
Scope: `PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN`

## 1. Purpose and authority

This document materializes the current design for converting already established PC Korean semantic obligations and Switch counterpart/owner evidence into a Portability Matrix and final Switch Action Ledger.

It does not redesign FZ001, reclassify the forward 986 population, reopen TRACE closure, revalidate the F1 static-write authorization, modify builder/runtime/game files, generate IPS, or authorize a diagnostic build.

Authority order remains:

1. `PROJECT_STATE.md` sole resume authority;
2. frozen FZ001 identities inside their frozen schema domain;
3. later narrow canonical correction/overlay over older broader or unresolved state;
4. source canonical evidence documents;
5. this design contract as the current planning contract.

The external design synthesis `TAIKO5DX_PORTABILITY_ACTION_LEDGER_FINAL_DESIGN_20260913.md` is incorporated as design provenance. Repository canonical evidence remains authoritative where wording differs.

## 2. Fixed principles

The following are fixed:

- PC Korean patch result/behavior is the semantic Oracle when the patch directly provides the relevant obligation.
- Switch reproduces semantic effect, not Windows-specific mechanics.
- target/counterpart resolution, terminal disposition, portability, write authority, implementation, and release closure remain separate axes.
- capacity/storage failure is not translation failure.
- `NATIVE_EQUIVALENT_VERIFIED` receives no artificial portability class.
- `SUBSUMED` receives no independent portability class and must link directly to a final non-`SUBSUMED` action.
- builder is a semantic-free executor of an already resolved Action Ledger.
- existing INV-1 through INV-11 and Master Rule Registry rules are reused rather than duplicated.

## 3. FZ001 and current effective state

FZ001 remains immutable historical baseline. Its four frozen semantic identities are not changed by this design.

The current state used for new planning is an effective view produced by composing FZ001 with later canonical overlays. Composition is field-scoped, not whole-row replacement.

### 3.1 Effective-state composition rule

For each stable source identity:

1. start from the frozen FZ001 state where that source exists;
2. apply only later canonical overlays whose exact membership includes that source;
3. a later overlay may update only the axis/field that its evidence actually proves;
4. fields not addressed by that overlay are inherited unchanged;
5. a later narrow correction supersedes an older broader or unresolved claim only within its proven scope;
6. conflicting claims on the same axis without explicit precedence/supersession produce `CONFLICT`; automatic last-write-wins is forbidden;
7. historical rows/claims remain provenance and are never deleted or rewritten.

The current Oracle chain already follows this model: Oracle V1 -> Assisted follow-up -> Astra follow-up -> TRACE closure. Each later artifact refines only the effective disposition of its exact queue while preserving prior artifacts as provenance.

### 3.2 Effective F1 target-resolution state

FZ001 froze the historical F1 state as 262 target-resolved and 16 F1-rule-rejected/analyzed-unresolved rows. Those 16 were not proven false targets; the frozen materialization explicitly allowed resolution under another verified family.

Post-freeze evidence resolves all 16 on the target/counterpart axis:

- 14 are deterministically `ORACLE_RESOLVED` in Oracle V1;
- `R3181` and `R3182` are `TARGET_RESOLVED` in the Assisted follow-up.

Therefore the current effective F1 target-resolution view is:

```text
F1 source population                278
current effective target resolved   278
static-write authorized             158
write/action closure still open     120
```

This does not promote any new F1 write authorization. The 75 padding, 25 shared-owner, 4 capacity-fail, and the 16 later target-resolved rows remain outside the existing 158 static-write-authorized actions until their own action/write-safety requirements are closed.

## 4. Four-layer semantic model

Every source obligation is analyzed through four logical layers:

```text
PC source record
    -> PC Korean semantic obligation
    -> Switch semantic owner
    -> Switch action
```

### 4.1 PC source record

The stable canonical PC-side accounting identity. Source denominators never shrink because actions collapse or fan out.

### 4.2 PC Korean semantic obligation

The semantic result/effect carried by the PC patch, including as applicable:

- Korean text/label;
- formatter/control structure;
- pointer/reference effect;
- mapping behavior;
- runtime helper behavior;
- padding/storage-extension behavior.

One inline record is not assumed to equal one semantic object.

### 4.3 Switch semantic owner

The Switch object/family that actually owns the equivalent semantic responsibility, such as:

- localization entry;
- raw/static object;
- shared object;
- language-table owner;
- relocation/reference owner;
- runtime-managed semantic family;
- native Switch UI/warning owner.

In the frozen accounting model, effective `target_identity` and its claims carry owner identity. Physical write/code sites remain action data and must not be conflated with semantic ownership.

### 4.4 Switch action

The final mutation or verified no-mutation outcome required to realize already decided semantics. Multiple sources may collapse into one action and one source may fan out to multiple actions.

## 5. Portability classes

Portability answers: how can the PC semantic obligation be realized on Switch?

### P1 — DATA_PORTABLE

The semantic result can be realized through Switch static/native data ownership without introducing a distinct runtime behavior family.

Typical realizations include direct write, complete object reconstruction, fixed/table reconstruction, padding/storage reconstruction, and static/reference redirection where the semantic owner model remains materially the same.

### P2 — RUNTIME_PORTABLE

The semantic behavior itself must be implemented as a Switch runtime behavior family.

### P3 — SEMANTIC_PORTABLE / MECHANIC_NOT_PORTABLE

The PC implementation mechanism is unsuitable or absent on Switch, but the same semantic result/effect can be reproduced through a different Switch-native owner or mechanism.

Examples include rerouting a PC-only object to a Switch-native localization owner or reproducing a PC helper effect through a structurally different Switch-native mechanism.

### P4 — PC_ONLY / NO_SWITCH_EQUIVALENT

Verified evidence proves no equivalent Switch semantic obligation remains.

P4 is valid only with explicit evidence, scope, and falsification condition. Absence of the exact PC object is not sufficient.

## 6. Portability and terminal disposition mapping

| Terminal disposition | Portability relation | Rule |
|---|---|---|
| `DIRECT_PORT` | normally P1 | simple static/native realization |
| `STRUCTURAL_PORT` | P1 or P3 | P1 for same-owner/model reconstruction; P3 for Switch-native semantic substitution |
| `REDIRECT_PORT` | P1 or P3 | P1 for static/reference relocation within the same model; P3 for semantic-owner/mechanism substitution |
| `RUNTIME_PORT` | P2 or P3 | P2 for direct runtime-semantic family implementation; P3 for different Switch-native mechanism |
| `NATIVE_EQUIVALENT_VERIFIED` | N/A | no new port action required |
| `SUBSUMED` | no independent class | reference the final non-`SUBSUMED` action |
| `PROVEN_IRRELEVANT` | P4 | verified exclusion only |
| `CONFLICT` | unresolved | portability must remain unknown |
| `UNRESOLVED` | unresolved | portability must remain unknown |

No P5 is created for native-equivalent state.

If one proposed action appears to require two incompatible portability mechanisms, first test whether the action identity is over-compressed. Split the action when its semantic/implementation responsibilities are independently executable and independently falsifiable.

## 7. Portability Matrix is a derived planning view

The Portability Matrix is not a new FZ001 semantic entity and does not mutate the frozen schema.

It is derived from existing/effective source state, source/action edges, proposed/final actions, and claims. Minimum planning columns are:

- stable source ID;
- effective target identity;
- effective terminal disposition;
- final action ID when applicable;
- source/action relation;
- derived portability class when applicable;
- current write authority;
- claim/evidence provenance.

`NATIVE_EQUIVALENT_VERIFIED`, `CONFLICT`, and `UNRESOLVED` may legitimately have no portability value. `SUBSUMED` inherits no independent value.

## 8. Existing schema is sufficient

No new mandatory semantic field is introduced by this design.

Use the existing frozen model:

Source state:
- `target_status` / `target_identity`;
- `terminal_disposition`;
- `write_authority` / `write_authority_family`;
- `closure_state`;
- `handoff_family`;
- `blocker`;
- `claim_refs[]` / `legacy_evidence_refs[]`.

Action:
- `action_id`;
- `action_family`;
- `storage_class`;
- `language_domain`;
- `switch_object_or_code_sites`;
- `input_source_ids[]`;
- `replacement_or_behavior`;
- `guards[]`;
- `apply_priority`;
- `capacity_requirement`;
- `conflict_state`;
- `runtime_test_family`;
- `runtime_validation_required`;
- `status`;
- provenance fields.

Edges:
- `PRIMARY`;
- `SHARED_OWNER`;
- `FRAGMENT`;
- `GUARD`;
- `SUBSUMED_BY`.

The Portability Matrix may expose a derived `portability_class` column, but it is not added to FZ001 source/action identities by this scope.

## 9. Source-to-action relation rules

- 1:1: one source obligation to one final action.
- 1:N: retain one source identity and link every required final action.
- N:1: multiple source obligations may collapse to one action only after replacement/semantic agreement or explicit conflict resolution.
- N:M: require an explicit structural family rule and complete linkage.
- `SUBSUMED`: source links directly to the final non-`SUBSUMED` action; chained subsumption is forbidden.
- no-edit outcomes do not receive placeholder/no-op actions.

## 10. Korean Oracle and capacity/storage handling

Default rule: preserve the PC Korean semantic result.

Capacity/storage blockers do not authorize automatic shortening, translation change, terminator removal, control-token removal, or formatter simplification.

Resolution order is:

1. identify another valid storage/owner within the proven semantic model;
2. complete-object/storage reconstruction;
3. `REDIRECT_PORT` to valid replacement storage/owner;
4. Switch-native runtime equivalent when required;
5. only after all evidence-backed realization paths fail, leave unresolved for explicit human semantic review.

Semantic deviation is an exception path, not a normal portability class. No mandatory `korean_payload_origin` or semantic-deviation field is created now. If a real approved deviation later exists, the PC Oracle and final approved semantic result must both retain provenance.

## 11. Action-family planning taxonomy

Preserve already-issued action identities/families such as `F1_LOCALIZATION_STATIC_DIRECT`.

For new proposal work, the following conceptual families may be used where the evidence actually requires them:

- `DIRECT_STATIC_WRITE`;
- `COMPLETE_OBJECT_RECONSTRUCTION`;
- `PADDING_RECONSTRUCTION`;
- `SHARED_OWNER_ACTION`;
- `LANGUAGE_OWNER_REROUTE`;
- `SWITCH_NATIVE_SEMANTIC_REROUTE`;
- `RUNTIME_SEMANTIC_ACTION`.

These are planning labels, not permission to rewrite the frozen action schema or silently rename existing action IDs/families. Additional families require an independently meaningful execution/validation boundary; existing INV-* coverage is not duplicated as action taxonomy.

## 12. Builder semantic-free executor contract

A future builder may only validate and execute an already resolved Action Ledger.

Allowed builder responsibilities:

- verify canonical input identity;
- verify ledger-defined guards;
- execute ledger-defined transformations;
- deterministic serialization;
- exact planned-vs-emitted action comparison;
- overlap/application-order checks;
- hashes/reports;
- fail-closed validation.

The builder must not:

- discover/select semantic targets;
- decide Korean wording;
- truncate or shorten on capacity failure;
- add/remove terminators or control tokens by heuristic;
- deduplicate merely because text matches;
- merge/split source/action relations by heuristic;
- decide reroute/native-equivalent/subsumed status;
- choose P1/P2/P3/P4;
- silently skip failed guards;
- create an unplanned fallback action;
- emit a partial-success release artifact after failure.

Any such unresolved decision means the Action Ledger is not ready for builder consumption.

## 13. Existing invariant reuse

Do not create duplicate gates for already-canonical invariants:

- INV-1 code-space/font/RomFS closure;
- INV-2 language-domain isolation;
- INV-3 storage/relocation integrity;
- INV-4 source/action cardinality;
- INV-5 overlap/order consistency;
- INV-6 mapping consumer consistency;
- INV-7 code-site authorization;
- INV-8 guards/target identity;
- INV-9 semantic round-trip;
- INV-10 deterministic build/reproducibility;
- INV-11 evidence closure for no-edit dispositions.

Portability and actions attach to these invariants; they do not replace them.

## 14. Decision procedure for future population

For each obligation/family:

1. compose current effective source state from frozen baseline plus exact canonical overlays;
2. preserve the PC Korean semantic Oracle and control/formatter semantics;
3. resolve the current Switch semantic owner from existing evidence;
4. establish 1:1 / 1:N / N:1 / N:M relation;
5. determine no-edit or `SUBSUMED` cases first;
6. define the final action and terminal disposition;
7. derive P1/P2/P3/P4 only where applicable;
8. evaluate language/storage/capacity/terminator/shared-owner/overlap/guard requirements;
9. grant or deny write authority independently;
10. bind required INV-1..INV-11 and runtime-family validation.

A failed write-safety gate does not automatically alter portability or the Korean semantic Oracle.

## 15. Current boundaries and next scope

This design creates no new Switch write authorization and performs no implementation.

Unchanged:

- FZ001 frozen identities;
- F1 existing 158 static-write authorizations;
- forward 986 membership;
- Oracle/Assisted/Astra/TRACE provenance and closure;
- builder/runtime/game files;
- INV-1..INV-11 definitions.

The next recommended scope is `PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION_READ_ONLY`:

- materialize the current effective source-state input view;
- generate a read-only Portability Matrix proposal;
- generate a read-only Action Ledger proposal;
- report unresolved/conflict/write-safety queues;
- do not modify builder/runtime/game files or emit IPS.

A fresh explicit user signal is required for that scope.
