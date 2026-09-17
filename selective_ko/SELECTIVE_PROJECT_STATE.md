# SELECTIVE PROJECT STATE

Date: 2026-09-17 (KST)
Status: V295 CONTAINER-ANALYSIS CORRECTION MATERIALIZED / CONTENT INVENTORY REMAINS OPEN / V294 IDENTITY POLICY CLOSED / NO CORPUS CLASSIFICATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the sole executable next-scope authority for the selective product track.

The repository-root `PROJECT_STATE.md` is the sole repository-level resume authority and routes selective work here.

Inherited base before V295 correction:

```text
commit = b1bd4972c7d8793150ecf7d2648ae0be1c774b43
scope  = SELECTIVE_KO_IDENTITY_IN_PROSE_V1_MATERIALIZED / V294
```

All prior VERIFIED/closed facts are inherited without revalidation except where `CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md` explicitly corrects claim strength or stale routing.

Required reads for the current selective scope, in authority order:

1. `CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`
2. `SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`
3. `../docs/SELECTIVE_KO_NEXT_SCOPE_AUTHORITY_RECONCILIATION_V293.md`
4. `IDENTITY_IN_PROSE_POLICY.md`
5. `KNOWN_FAILURES.md`
6. `ARCHITECTURE.md`
7. `CLASSIFICATION_SCHEMA.md`
8. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
9. `EVENT_EXTRACTION_SCHEMA.md`
10. `IDENTITY_PROVENANCE_CONTRACT.md`
11. `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`
12. `FIXED_PARTICLE_POLICY.md`
13. `PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION.md`
14. `registry/provenance_shards/INDEX.json`
15. `TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION.md`
16. `artifacts/TAI5MSG_STRUCTURE_INDEX_MANIFEST.json`
17. `artifacts/tai5msg_structure_index_v1/INDEX.json`
18. this file

If any lower document conflicts with V295 correction or this file, V295 correction + this file govern.

## 2. Product / authority boundary

The selective project is not a full clone of the PC Korean patch.

Priority Korean scope remains:

- descriptions/help/UI explanatory text;
- event/system/context text;
- structurally safe dialogue.

First-release Japanese/deferred scope remains:

- dedicated person/place identity fields;
- yomi/readings/sort keys;
- surname/given-name composition;
- date/calendar identity presentation;
- Korean name entry;
- unresolved dynamic grammar/formatter dialogue.

Authority:

```text
PC Korean content/terminology              -> SOURCE_AUTHORITY
PC mapping/font source obligation          -> SOURCE_AUTHORITY
verified Switch mapping realization        -> SWITCH_RUNTIME_AUTHORITY
Switch script/control/owner/runtime        -> STRUCTURAL_AUTHORITY
known-good PC visible Korean               -> SEMANTIC_ORACLE
PC runtime mechanics                       -> REFERENCE_OR_HINT
PC workaround/defect                       -> NON_AUTHORITATIVE_EVIDENCE
```

Conflict rule:

```text
structure = Switch
content/semantic obligation = PC source/oracle
implementation = Switch-native design
```

## 3. V294 identity-in-prose policy — CLOSED

Current policy remains:

```text
identity presentation fields            -> KEEP_JP
PC Korean prose identity literals        -> PRESERVE_AS_AUTHORED_KO
runtime-inserted person/place identity   -> KEEP_JP
prose-literal reverse substitution       -> FORBIDDEN
```

This decision is not reopened by cross-container inventory.

The project intentionally accepts Japanese identity presentation alongside Korean-authored prose spellings where they differ.

## 4. V295 correction overlay — CLOSED

Canonical correction:

`CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`

V295 does not close the inventory. It corrects the following points:

```text
TAI5MSG Korean-bearing-message census = 13,590
prior 13,591 count                    = WITHDRAWN
inline >=10/20/40 Korean-char counts  = 203 / 98 / 69
those inline counts                   = LENGTH CENSUS ONLY, NOT USAGE CLASS
PC patch EVENT file denominator       = 169
EVENT 169/169 structural text-bearing = NOT ESTABLISHED
F1 static 158                         = SOURCE/OWNER PROVENANCE, NOT R1 COUNT
exact exploratory identity-exposure totals = NOT CANONICALIZED
```

Verified container-role conclusions currently safe to retain:

- TAI5MSG is not dialogue-only;
- verified EVENT/TS5 samples directly contain event narration/dialogue payloads, so EVENT is not control-only;
- SNR is a mixed container containing scenario/narrative and identity-related data, so it requires field/record-selective treatment;
- a container/file name never determines R1/R2/R3 safety by itself.

## 5. Superseded stale wording

The following lower-document clauses are non-authoritative where they conflict with V294/V295:

### `ARCHITECTURE.md`

- identity-in-prose is **not** unresolved; V294 closed it;
- the old sequence step scheduling an identity-in-prose decision is complete, not future work;
- content tier must not be inferred from container name.

### `CLASSIFICATION_SCHEMA.md`

- translation-QA deferral does not reopen identity-in-prose; V294 already resolved that product-policy question.

### `EVENT_EXTRACTION_SCHEMA.md`

- event structural classes remain useful overlay metadata;
- legacy terminal labels `INCLUDE_EVENT_KO`, `INCLUDE_SAFE_DIALOGUE_KO`, `HOLD_DYNAMIC_DIALOGUE` are historical/provisional only;
- new rows use common axes and terminal dispositions `INCLUDE_KO / DEFER_KO / KEEP_JP / BLOCKED / UNRESOLVED`;
- its file-local next-scope recommendation is not execution authority.

### `TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION.md`

- its final direct-next-step recommendation to broad TAI5MSG classification is historical and superseded;
- ART-00000005 remains locator/length structure only.

No historical document needs to be silently rewritten to erase what was previously believed; V295 preserves the correction provenance explicitly.

## 6. Persistent registry / owner state

Current totals remain:

```text
PC_SOURCE_INLINE        = 158
SWITCH_PHYSICAL_OWNER   = 158
entity IDs              = 316
BINDS_TO edges          = 158
edge IDs                = 158
artifact IDs            = 5
candidate IDs           = 0
manual task IDs         = 0
classification IDs      = 0
```

F1 static 158 is a verified source-owner population only. It does not imply 158 R1 descriptions or automatic `INCLUDE_KO`.

## 7. TAI5MSG boundary

`ART-00000005` remains a PC-original <-> PC-Korean locator/length structure lattice.

It does not prove:

- payload semantics;
- opcode/call structure;
- Switch-original correspondence;
- Switch physical owner;
- Switch caller topology;
- mechanism class;
- release disposition.

Corrected source-side Korean-bearing-message census is `13,590`, but this count alone authorizes nothing downstream.

## 8. EVENT/TS5 boundary

Current source-side facts:

```text
PC Korean patch EVENT/*.TS5 denominator = 169 files
verified samples show direct Korean narration/dialogue payloads in EVENT family
```

Not yet established:

- 169/169 structurally verified text-bearing status;
- production text-field parser over the whole family;
- Switch-original script/caller correspondence;
- production owner/action bindings.

Do not broad-classify EVENT rows merely from raw byte scans.

## 9. SNR boundary

SNR must be treated as a mixed container.

Do not assign one file-level product disposition across scenario prose and identity data.

The current first-release identity policy remains Japanese retention for dedicated identity fields. Selected authored Korean narrative/prose may be considered separately after structural closure.

## 10. Switch-original source supply

The user will provide XCI-derived Switch originals when a later structural scope requires them.

Canonical input contract:

`SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`

Planned Drive-relative destination:

```text
태합입지전 프로젝트/Switch/Original_v1.1.3/
├─ exefs/main
└─ romfs/<exact extracted relative tree>
```

Current source status:

```text
Switch original RomFS bundle = NOT_YET_SUPPLIED
current blocker              = false
```

Do not repeatedly request the extraction now.

When needed, provide the extraction method then. Until supplied, mark a required Switch counterpart unavailable/not-yet-supplied instead of guessing.

## 11. Mixed-script route safety

V294 permits Japanese runtime identity tokens and Korean prose to coexist.

Route-wide safety is still not globally assumed. Each selected mixed-script family must preserve Japanese and Korean mapping/font/transport behavior on its actual Switch route.

## 12. Executable next scope — sole authority

The exact next selective scope remains:

```text
SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY
```

The scope remains open because the prior analysis was corrected before closure.

Remaining purpose:

1. produce an actual R1 `UI_DESCRIPTION` source census without using string length as a proxy;
2. record per container/family which common fields are machine-extractable, manually decidable, or unavailable;
3. record EVENT/TS5 parser/text-field/caller-field availability without broad corpus classification;
4. record SNR field/record parser availability without assigning one file-level disposition;
5. keep source-side TAI5MSG payload availability separate from Switch owner/caller availability;
6. either establish a reproducible identity-in-prose exposure method or leave exact totals unmaterialized;
7. record Switch-original counterpart state as `NOT_YET_SUPPLIED` where required, without making source absence a blocker until the relevant later structural scope.

This scope is READ ONLY inventory/availability analysis.

It must not:

- create broad corpus classification rows;
- issue candidate/classification IDs;
- assign release dispositions to a broad corpus;
- implement serializers/builders;
- mutate gameplay data;
- create IPS/build/runtime artifacts;
- reopen V294 identity policy;
- reopen closed Mapping/F1/other VERIFIED work without new contradictory evidence.

## 13. Current non-materialized work

Still not materialized:

- completed cross-container R1/R2/R3 field-availability inventory;
- actual R1 source-role census;
- broader source-owner coverage outside F1-static-158;
- TAI5MSG selective corpus classifications;
- EVENT/TS5 production adapter;
- SNR selective field adapter;
- selected Korean payloads;
- selective serializers/builders;
- IPS/build;
- translation QA.

## 14. Repository write boundary

Repository writes remain restricted to:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API write, branch creation, issue/PR write, or force update is permitted for repository materialization.

After V295 materialization is reported, a fresh explicit user execution signal is required before resuming the read-only inventory or beginning any later stage.
