# CONTENT CONTAINER / FIELD AVAILABILITY CORRECTION — V295

Date: 2026-09-17 (KST)
Status: CANONICAL CORRECTION MATERIALIZED / INVENTORY SCOPE REMAINS OPEN / NO CORPUS CLASSIFICATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `SELECTIVE_KO_CONTAINER_ANALYSIS_CORRECTION_V295_MATERIALIZED`

## 1. Purpose

This document corrects overstatements and stale routing discovered while executing:

`SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY`

It does **not** close that inventory scope.

It does not create candidate IDs, classification IDs, dispositions, gameplay-data rewrites, serializers, builders, IPS, builds, or runtime artifacts.

Materialization parent:

```text
commit = b1bd4972c7d8793150ecf7d2648ae0be1c774b43
scope  = SELECTIVE_KO_IDENTITY_IN_PROSE_V1_MATERIALIZED / V294
```

All V294 facts remain inherited unless explicitly corrected below.

## 2. Corrected TAI5MSG Korean-bearing-message census

Canonical TAI5MSG structural facts remain unchanged:

```text
blocks      = 33
messages    = 14,832
PC original <-> PC Korean logical slots = 1:1
```

A prior exploratory count reported `13,591` Korean-bearing messages. That count was one too high because a naive two-byte scanner treated a byte inside a control sequence as text.

Corrected control-aware census:

```text
Korean-bearing TAI5MSG messages = 13,590
```

Known false-positive witness:

```text
block_index         = 15
local_message_index = 280
bytes               = 01 4D 02 74 02 33 69 02 74 EC D5 05 05 05
```

The `02 74 EC` sequence is consumed as one three-byte control sequence. `EC` is therefore not a text lead byte in that position.

This corrected count is a source-side census only. It does not prove usage class, mechanism class, Switch owner, caller topology, applicability, realization, or release inclusion.

## 3. Inline long-Korean census — preserved but reinterpreted

The previously measured PC inline replacement counts remain valid as byte/text-length census values:

```text
Korean characters >= 10 : 203 source records
Korean characters >= 20 :  98 source records
Korean characters >= 40 :  69 source records
```

These values must **not** be interpreted as R1 `UI_DESCRIPTION` counts.

Long Korean inline text includes multiple semantic roles, including narration/ending-style prose. Therefore:

```text
long Korean inline text != UI_DESCRIPTION
```

`usage_class` still requires source-grounded structural or semantic classification.

The F1 static 158 source/owner bindings likewise do not equal 158 R1 rows. They remain source/owner provenance only; candidate/classification/disposition totals remain zero.

## 4. EVENT/TS5 denominator and claim-strength correction

The canonical PC Korean patch payload contains:

```text
RomFS data files total = 208
EVENT/*.TS5 files      = 169
```

Verified samples establish that the EVENT/TS5 family directly contains Korean event narration and dialogue payloads. Therefore the prior model that EVENT/TS5 is merely control script with all visible text owned elsewhere is rejected.

However, the stronger statement that all `169/169` EVENT files have structurally verified Korean text fields is **withdrawn**.

Reason:

- a raw byte scan of binary TS5 files can misidentify non-text bytes as game-code text;
- no production TS5 text-field parser/caller adapter has yet enumerated all 169 files;
- current `EVENT_EXTRACTION_SCHEMA.md` remains a design schema, not a completed corpus extraction.

Canonical safe statement:

```text
169 EVENT/TS5 files exist in the PC patch payload.
Verified samples prove direct Korean narration/dialogue payloads exist in the EVENT family.
169/169 structural text-bearing status is not yet established.
```

## 5. SNR mixed-container correction

SNR is not an identity-only container.

PC original/Korean SNR evidence establishes coexistence of at least:

- scenario title / introductory narrative text;
- person display-name / identity-related data.

Therefore one file-level product disposition is invalid for SNR.

Required principle:

```text
SNR classification must be field/record selective.
container membership alone does not determine usage_class or disposition.
```

Existing product policy remains unchanged:

- authored Korean prose may remain Korean when selected;
- dedicated person/place/yomi/reading identity fields remain Japanese for the first release.

## 6. Container is not release phase

The following simplifications are explicitly rejected:

```text
TAI5MSG == dialogue-only
EVENT/TS5 == script/control-only
SNR == identity-only
one container == one release phase
long Korean string == R1 UI_DESCRIPTION
F1 static 158 == R1 158
PC-original <-> PC-Korean correspondence == Switch correspondence
Drive search miss == proof that a source file does not exist
```

R1/R2/R3 assignment remains message/field/object based, not filename based.

## 7. Identity-in-prose exploratory-count correction

Previously reported exact exposure totals such as TAI5MSG person-name occurrence counts, EVENT person-name occurrence counts, and SNR person-name occurrence counts are **not canonicalized by V295**.

The qualitative finding remains:

```text
identity-in-prose exposure is non-trivial, especially in TAI5MSG.
```

Exact totals require a reproducible, provenance-bearing identity-set extraction rule before materialization.

Do not cite the exploratory exact totals as canonical counts until such an artifact exists.

V294 product policy remains closed and unchanged:

```text
identity presentation fields          -> KEEP_JP
PC Korean prose identity literals      -> PRESERVE_AS_AUTHORED_KO
runtime-inserted person/place identity -> KEEP_JP
reverse substitution                   -> FORBIDDEN
```

## 8. Switch-original source boundary

Missing or not-yet-located Switch original RomFS sources are not treated as a project failure and do not block documentation correction.

When a later scope actually needs Switch-original TAI5MSG/EVENT/SNR structure authority, the user will provide an XCI extraction.

Canonical external-input layout is defined in:

`SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`

Until those sources are supplied, record the relevant Switch counterpart as unavailable/not-yet-supplied. Do not infer absence from Drive search behavior and do not substitute PC structure as Switch authority.

## 9. Supersession map for stale wording

This V295 correction supersedes only the conflicting statements listed below. Other non-conflicting evidence in those documents remains valid.

### `ARCHITECTURE.md`

Superseded:

- Tier-1 wording that identity-in-prose remains an unresolved product-policy question;
- architectural sequence step that still schedules an identity-in-prose decision after V293.

Replacement:

- V294 already closed `IDENTITY_IN_PROSE_V1`;
- cross-container inventory remains open;
- container membership never determines tier by itself.

### `CLASSIFICATION_SCHEMA.md`

Superseded:

- wording that translation-QA deferral leaves identity-in-prose as an unresolved product-policy question.

Replacement:

- identity-in-prose is closed by V294;
- translation QA remains deferred independently.

### `EVENT_EXTRACTION_SCHEMA.md`

Superseded for new rows:

- legacy terminal labels such as `INCLUDE_EVENT_KO`, `INCLUDE_SAFE_DIALOGUE_KO`, and `HOLD_DYNAMIC_DIALOGUE`;
- the file-local `SELECTIVE_KO_EVENT_CANDIDATE_INVENTORY_READ_ONLY` next-scope recommendation as execution authority.

Replacement:

- event structural classes remain an overlay;
- new rows use common axes and common terminal dispositions `INCLUDE_KO / DEFER_KO / KEEP_JP / BLOCKED / UNRESOLVED`;
- executable next scope is declared only by `SELECTIVE_PROJECT_STATE.md`.

### `TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION.md`

Superseded:

- final recommendation to proceed directly to `TAI5MSG_SELECTIVE_MESSAGE_CLASSIFICATION_READ_ONLY`.

Replacement:

- ART-00000005 remains locator/length structure only;
- current cross-container inventory must close first;
- no broad TAI5MSG classification is authorized by the structure artifact alone.

## 10. Full-port design failure recorded by this correction

The old full-port track produced useful low-level evidence, but its product assembly order was too coarse.

Rejected sequence:

```text
bulk/file-level PC payload import
-> observe breakage
-> diagnose individual symptoms
```

Current selective sequence remains:

```text
identify container and exact field/message/object
-> determine usage/mechanism evidence
-> bind Switch owner/caller/structure
-> close capacity/risk/provenance
-> only then authorize Korean realization
```

Do not revive bulk `data/` import or whole-container inclusion as the selective baseline.

## 11. Current inventory scope remains open

The exact executable next scope remains:

`SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY`

Remaining work inside that same scope includes:

1. obtain an actual R1 `UI_DESCRIPTION` census rather than using string length as a proxy;
2. record EVENT/TS5 parser/text-field/caller-field availability without broad corpus classification;
3. record SNR field/record parser availability without assigning file-level dispositions;
4. preserve the control-aware TAI5MSG census rule and distinguish source-side payload availability from Switch-owner/caller availability;
5. either create a reproducible identity-in-prose exposure method or leave exact exposure counts unmaterialized;
6. record Switch-original counterpart availability as `NOT_YET_SUPPLIED` until the XCI-derived source bundle is provided.

No implementation follows automatically from completion of this read-only inventory.

## 12. Repository and build boundary

V295 creates documentation/authority correction only.

```text
candidate IDs                 = 0
classification IDs            = 0
selective INCLUDE_KO rows      = 0
TAI5MSG payload rewrites       = 0
EVENT/SNR payload rewrites     = 0
builder changes                = 0
IPS/build/runtime artifacts    = 0
```

Repository write policy remains:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
