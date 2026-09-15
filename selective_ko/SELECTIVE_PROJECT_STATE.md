# SELECTIVE PROJECT STATE

Date: 2026-09-15 (KST)
Status: EVENT_EXTRACTION_SCHEMA_MATERIALIZED / NO CORPUS EXTRACTION / NO BUILD
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

The new product target is not a complete clone of the PC Korean patch.

Required Korean scope:

- character/person descriptions;
- region/location descriptions, while place names themselves may remain Japanese;
- tools/items descriptions;
- techniques/skills descriptions;
- event narrative/body text;
- static or otherwise proven-safe dialogue when practical.

Explicitly non-required for the first release:

- Korean person names;
- Korean place names;
- Korean calendar/year/month/day formatting;
- yomi/reading/sort-key conversion;
- Korean surname/given-name composition;
- Korean name-entry input;
- dynamic grammar formatter dialogue whose composition safety is not proven.

## 3. Inherited VERIFIED assets

The following are inherited without revalidation unless identity changes or contradictory evidence appears:

- Switch v1.1.3 `main` identity and Build ID;
- Stage1/Stage2/F1/FZ001 structural discoveries as provenance sources;
- Mapping 10,036 semantic obligation;
- the four-action Switch Mapping 10,036 realization;
- Mapping forward/reverse/round-trip PASS on the tested Eden Android route;
- Switch text decoder evidence that compact Korean bytes are accepted when they reach the decoder;
- Switch Japanese halfwidth normalization ownership/route findings;
- PC Korean translation corpus, names, terminology, mapping/font assets as source evidence;
- TAI5MSG container structure and message parser knowledge;
- known full-port failure/rejected-hypothesis history.

Existing full-port WRITE_SAFE does not automatically authorize selective-project output. The selective builder must consume only sources explicitly included by this project.

## 4. PC patch role in this project

Product-planning rule:

- PC Korean **text/content** = preferred translation/source reference;
- PC Korean **known-good visible result** = semantic reference where useful;
- PC Windows **implementation mechanics** = non-authoritative reference;
- PC workaround/known bug = never copied merely for parity.

The Switch implementation is selected from Switch-native data/code ownership after the required Korean semantic content is known.

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

The 170 MB PC patch ZIP remains at its existing canonical Drive location and is referenced rather than duplicated.

## 7. Source disposition states

Every candidate Korean source must end in exactly one of:

- `INCLUDE_DESCRIPTION_KO`
- `INCLUDE_EVENT_KO`
- `INCLUDE_SAFE_DIALOGUE_KO`
- `HOLD_DYNAMIC_DIALOGUE`
- `KEEP_JP_IDENTITY`
- `OUT_OF_SCOPE`
- `UNRESOLVED`

`UNRESOLVED` is not releasable.

Translation quality review is deferred to real-device/runtime QA and is not a pre-extraction blocker:

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

## 8. Event extraction boundary

Event-related text must follow `EVENT_EXTRACTION_SCHEMA.md` before receiving a product disposition.

Current event structural classes:

- `EVENT_NARRATION_STATIC`
- `EVENT_OBJECTIVE_STATIC`
- `EVENT_CHOICE_STATIC`
- `EVENT_BRANCH_LOCAL_SAFE`
- `EVENT_VARIABLE_SAFE`
- `EVENT_DIALOGUE_STATIC`
- `EVENT_DYNAMIC_GRAMMAR`
- `EVENT_SCRIPT_COMPOSED`
- `EVENT_UNKNOWN`

Key rules:

- branch presence alone does not make an event unsafe;
- every translated branch leaf must be a complete semantic surface unit;
- dynamic grammar and cross-message sentence composition are held out of R1-R3;
- variable insertion must account for Korean particle allomorphy;
- shared messages require all-caller compatibility, not one observed safe caller;
- EVENT/TS5 analysis is deepened only for dynamic/cross-message/mixed/unknown candidates rather than opened globally.

## 9. Release phases

R0 — infrastructure
- Mapping/font/text transport sufficient for selected Korean content.

R1 — descriptions
- character/region/item/skill explanatory text.

R2 — events
- event narrative, objectives/context, choices, branch-local complete text, and other structurally safe event content.

R3 — safe dialogue
- complete static lines and proven-safe variable insertion lines, including safe event dialogue.

R4 — optional dynamic grammar
- formatter-family reconstruction only if corpus-wide rules are proven.

R4 is optional and cannot block R1-R3 release.

## 10. Known grammar boundary

The prior full-port track observed malformed Korean such as:

- `모양이이오군`
- `실례하하겠습니다`
- `입니다인가`

Current policy: these are not repaired sentence-by-sentence and are not release blockers for R1-R3. Their formatter families remain `HOLD_DYNAMIC_DIALOGUE` until family-level Korean composition contracts are proven.

## 11. Materialized design documents

Current selective-project design baseline includes:

- `ARCHITECTURE.md`
- `CLASSIFICATION_SCHEMA.md`
- `EVENT_EXTRACTION_SCHEMA.md`
- `KNOWN_FAILURES.md`
- `MIGRATION_MANIFEST.json`

`EVENT_EXTRACTION_SCHEMA.md` is authoritative for event structural classes, branch completeness, variable/particle risk, shared-caller audit, event metadata fields, and minimal script-analysis depth.

## 12. Next scope

`SELECTIVE_KO_EVENT_CANDIDATE_INVENTORY_READ_ONLY`

Goals:

1. identify and count event-related candidate messages using existing PC/Switch provenance;
2. assign event structural classes where evidence already suffices;
3. extract control/formatter signatures and caller/branch metadata needed by the event schema;
4. separate safe narration/objective/choice/branch-local candidates from dynamic/cross-message/unknown queues;
5. preserve translation review as `DEFER_TO_RUNTIME_QA`;
6. perform no builder modification, no patch implementation, and no build.

After that report: STOP and require a fresh execution signal before any corpus materialization, Switch action implementation, or build.
