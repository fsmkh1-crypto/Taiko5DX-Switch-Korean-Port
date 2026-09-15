# SELECTIVE PROJECT STATE

Date: 2026-09-15 (KST)
Status: CROSSCUTTING_TAXONOMY_MATERIALIZED / EVENT_INVENTORY_READ_ONLY_COMPLETE / NO CORPUS MATERIALIZATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Base identity

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Umbrella branch: `main`
Initialization base HEAD: `f652333af41271b32bafb2054a1a1c3c853f1105`
Selective-project initialization commit: `2fb74c1e53030750012bcf7f13cf2ad8ebe43b2d`
Nintendo Switch title ID: `0100346017304000`
Target game version: `1.1.3`

This file is the resume authority for the `selective_ko/` subtree only. The repository-root `PROJECT_STATE.md` remains authoritative for the historical full-port track.

## 2. Product target

The selective product target is not a complete clone of the PC Korean patch.

Required/priority Korean scope:

- character/person descriptions;
- region/location descriptions, while place names themselves may remain Japanese;
- tools/items descriptions;
- techniques/skills descriptions;
- event narration/body/system/context text;
- static or otherwise proven-safe dialogue when practical.

Explicitly non-required for the first release:

- Korean person names;
- Korean place names;
- Korean calendar/year/month/day formatting;
- yomi/reading/sort-key conversion;
- Korean surname/given-name composition;
- Korean name-entry input;
- dynamic grammar formatter dialogue whose composition safety is not proven.

Translation quality review is deferred to real-device/runtime QA rather than pre-extraction review.

## 3. Inherited VERIFIED assets

The following are inherited without revalidation unless identity changes or contradictory evidence appears:

- Switch v1.1.3 `main` identity and Build ID;
- Stage1/Stage2/F1/FZ001 structural discoveries as provenance sources;
- L1/L2/L3 physical/semantic owner findings where applicable;
- Mapping 10,036 semantic obligation;
- the four-action Switch Mapping 10,036 realization;
- Mapping forward/reverse/round-trip PASS on the tested Eden Android route;
- Switch text decoder evidence that compact Korean bytes are accepted when they reach the decoder;
- Switch Japanese halfwidth normalization ownership/route findings;
- PC Korean translation corpus, terminology, mapping/font assets as source evidence;
- TAI5MSG container/message parser knowledge;
- existing event/TS5 structural observations;
- known full-port failure and rejected-hypothesis history.

Existing full-port WRITE_SAFE does not automatically authorize selective-project output. The selective builder must consume only sources explicitly included by this project.

## 4. PC patch authority model

The selective project no longer uses one undifferentiated "PC reference" category.

Authority is separated as follows:

```text
PC Korean translation/content/terminology     -> SOURCE_AUTHORITY
PC mapping/font source obligation             -> SOURCE_AUTHORITY
verified Switch mapping/font realization      -> SWITCH_RUNTIME_AUTHORITY
Switch script/control/owner/runtime structure -> STRUCTURAL_AUTHORITY
known-good PC Korean visible result           -> SEMANTIC_ORACLE (observed context only)
PC runtime mechanism                          -> REFERENCE_OR_HINT
PC workaround/known defect                    -> NON_AUTHORITATIVE_EVIDENCE
```

Conflict rule:

```text
structure = Switch
content/semantic obligation = PC source/oracle
implementation = Switch-native design
```

PC occurrence-level differences remain useful as a hazard map even when their Windows-specific implementation is not ported.

## 5. Current migrated repository assets

Direct-reuse family:

- `reuse/mapping10036/build_mapping10036_diag.py`
- `reuse/mapping10036/mapping10036_helper_v2.s`
- `reuse/mapping10036/mapping10036_helper_v2.ld`

Reference-only family:

- `reference/tai5msg_legacy_reconstruction.py`
- `reference/t5k_pc_patch_parser.py`

Reference-only code must not become release behavior without a separate review against this project's scope.

## 6. Drive workspace

Project folder:

`GPT / 태합입지전 프로젝트 / Switch_선택형_한글화_프로젝트`

Subfolders:

- `00_설계_문서`
- `10_원본_참조`
- `20_재사용_자산`
- `30_대사_이벤트_분류`
- `90_보류_제외`

Copied into `10_원본_참조` during initialization:

- Switch v1.1.3 `main`
- Switch v1.1.3 original `FONT_JPN.G1T`
- PC original `TAI5MSG_JP.DAT`

The canonical PC v1.02 Korean patch ZIP remains at its existing Drive location and is referenced rather than duplicated.

## 7. Canonical common taxonomy

The project-wide script/text classification authority for the selective subtree is now:

`SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`

New corpus rows use three observed axes:

```text
mechanism_class
usage_class
investigation_status
```

`derived_disposition` is computed from those axes plus physical-owner/caller/risk/capacity/provenance/evidence fields. It is not a fourth peer axis.

### 7.1 Mechanism classes

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

### 7.2 Usage classes

```text
UI_DESCRIPTION
NARRATION_SYSTEM
DIALOGUE
IDENTITY
OTHER
```

### 7.3 Investigation status

```text
RESOLVED
CALLER_UNKNOWN
NOT_INVESTIGATED
```

### 7.4 Derived dispositions

```text
INCLUDE_KO
DEFER_KO
KEEP_JP
BLOCKED
UNRESOLVED
```

`UNRESOLVED` is not releasable.

Manual disposition override requires an explicit reason and provenance and cannot convert missing investigation into proof.

## 8. Cross-cutting decision inputs and risks

Key mechanism-decision inputs include:

```text
append_after
append_after_targets
variable_source_kind
insert_followed_by
jp_particle_adjacency
dynamic_counter_decision
```

`APPEND_AFTER` is not a risk flag. It is a mechanism-decision input used to distinguish complete branch output from fragment/formatter composition.

No generic `CONTROL_GRAPH_DEPENDENT` risk flag is used because branch-complete output is inherently control-graph dependent.

Current common risk flags include:

```text
PARTICLE_RISK
SHARED_OWNER_RISK
PC_OCCURRENCE_CONFLICT
PC_SPACING_VARIANT
CROSS_MESSAGE_COMPOSITION
BUFFER_CAPACITY_RISK
```

PC occurrence handling:

- trailing NUL padding is removed for logical conflict comparison under the existing rule;
- spacing-only logical differences -> `PC_SPACING_VARIANT` and do not automatically block inclusion;
- non-spacing logical replacement differences -> `PC_OCCURRENCE_CONFLICT` and block automatic inclusion until caller/owner context is resolved.

## 9. Physical-owner/shared-caller rule

Classification follows the Switch physical owner, not raw text identity.

- reuse existing L1/L2/L3 and other canonical owner provenance where applicable;
- enumerate all known callers of a shared physical owner;
- if caller-specific separation is not already present, the most restrictive proven caller governs that owner;
- separate physical owners may be classified independently even when source text is identical;
- incomplete caller topology gives `CALLER_UNKNOWN` and derives `UNRESOLVED`;
- caller-specific redirection/restructuring is a separate escalation.

PC RVA/occurrence splitting is a hazard map, not proof of equivalent Switch ownership.

## 10. Safe dialogue boundary

A dialogue row is eligible for R3 only if all common safe-dialogue gates pass.

In particular, it must:

- be `usage_class=DIALOGUE`;
- have `investigation_status=RESOLVED`;
- be `STATIC_COMPLETE`, `BRANCH_COMPLETE`, or proven-safe `VARIABLE_INSERT`;
- have all callers of the same physical owner compatible;
- have no unresolved particle/grammar responsibility;
- have no cross-message composition;
- not be consumed as a formatter/message fragment by another deferred or unsafe composition family;
- have a proven safe capacity realization.

One rendered line or one safe caller is not global proof.

## 11. Event overlay status

`EVENT_EXTRACTION_SCHEMA.md` remains an auxiliary event-source schema for event-specific caller/branch metadata.

Its event structural classes are not terminal product classes and are mapped into the common taxonomy.

Important consequences:

- event membership alone never implies inclusion;
- branch presence alone never implies risk;
- `EVENT_BRANCH_LOCAL_SAFE` becomes candidate `BRANCH_COMPLETE` only after `append_after=NO` and all-caller closure;
- `EVENT_VARIABLE_SAFE` becomes candidate `VARIABLE_INSERT` only after particle/dynamic-counter screening;
- dynamic grammar/cross-message event classes map into deferred common mechanism classes;
- unknown event topology maps into non-resolved investigation status.

The previous read-only event inventory established that EVENT/TS5 contains both structurally simple event output and dynamic grammar/composition candidates. That inventory is evidence for the common taxonomy, not authorization to implement event content first.

## 12. Translation review policy

Initial extraction/classification uses:

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

Translation quality is reviewed while playing on the actual runtime path. Structural classification is not delayed for stylistic translation review unless semantic ambiguity prevents mechanism/usage classification.

## 13. Capacity rule

Capacity failure is not a translation defect.

Canonical escalation order:

```text
current storage
-> alternate existing storage
-> object/data reconstruction
-> redirect/relocation realization
-> Switch-native runtime semantic equivalent
-> only after technical routes are exhausted: human translation adjustment review
```

Automatic truncation or translation shortening is forbidden.

## 14. Release phases

R0 — infrastructure
- Mapping/font/text transport sufficient for selected Korean content.

R1 — descriptions
- `INCLUDE_KO` rows with `usage_class=UI_DESCRIPTION`.

R2 — narration/events/system
- add structurally safe `INCLUDE_KO` rows with `usage_class=NARRATION_SYSTEM` and explicitly resolved event-local non-dialogue rows where applicable.

R3 — safe dialogue
- add only rows satisfying the common Safe Dialogue definition.

R4 — optional deferred grammar/composition
- selectively revisit `DEFER_KO` families after recorded revisit conditions are met.

R4 remains optional and cannot block R1-R3.

## 15. Materialized design documents

Current selective-project design baseline includes:

- `ARCHITECTURE.md`
- `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
- `CLASSIFICATION_SCHEMA.md`
- `EVENT_EXTRACTION_SCHEMA.md`
- `KNOWN_FAILURES.md`
- `MIGRATION_MANIFEST.json`

Authority order for new classification work:

1. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md` for common taxonomy/authority/risk/disposition rules;
2. `CLASSIFICATION_SCHEMA.md` for selective-product mapping and release-set bridge;
3. container-specific auxiliary schemas such as `EVENT_EXTRACTION_SCHEMA.md` for additional metadata only.

Legacy disposition names remain historical provenance but are superseded for new corpus rows.

## 16. Current implementation boundary

No selective corpus rows have been materialized under the new common taxonomy.

No selective builder change, Switch action, IPS, or runtime artifact is authorized by the taxonomy documents themselves.

Translation QA remains deferred.

## 17. Next scope

`SELECTIVE_KO_CROSSCUTTING_AUTOMATABLE_FIELD_INVENTORY_READ_ONLY`

Goals:

1. inventory each relevant source/container family before content-specific implementation begins;
2. determine which common metadata fields can be extracted automatically per family;
3. identify reusable canonical parsers, caller graphs, physical-owner ledgers, and PC patch provenance;
4. prioritize automatic extraction of `append_after`, caller lists, `insert_followed_by`, cross-message consumers, variable-source provenance, and PC occurrence conflict/spacing classification;
5. separate machine-extractable fields from manual semantic judgment before broad classification;
6. do not implement descriptions/events/dialogue yet;
7. perform no builder modification and no build.

After that read-only report: STOP and require a fresh execution signal before corpus materialization, implementation, or build.
