# SELECTIVE PROJECT STATE

Date: 2026-09-17 (KST)
Status: V294 IDENTITY_IN_PROSE POLICY MATERIALIZED / V293 NEXT_SCOPE AUTHORITY RECONCILED / TAI5MSG STRUCTURE MATERIALIZED / F1 STATIC 158 COMPLETE / NO CORPUS CLASSIFICATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the sole executable next-scope authority for the `SWITCH_SELECTIVE_KOREANIZATION` product track.

The repository-root `PROJECT_STATE.md` is the repository-level resume authority and routes selective work here. Historical/design/reference documents may describe sequences or old next stages, but they do not override this file.

The prior selective canonical state at commit `a954885f7f59c64b18cd969e3178397604e02d58` is inherited without revalidation except where explicitly superseded below.

Required reads for the next selective scope:

1. `../docs/SELECTIVE_KO_NEXT_SCOPE_AUTHORITY_RECONCILIATION_V293.md`
2. `IDENTITY_IN_PROSE_POLICY.md`
3. `KNOWN_FAILURES.md`
4. `ARCHITECTURE.md`
5. `CLASSIFICATION_SCHEMA.md`
6. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
7. `IDENTITY_PROVENANCE_CONTRACT.md`
8. `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`
9. `FIXED_PARTICLE_POLICY.md`
10. `PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION.md`
11. `registry/provenance_shards/INDEX.json`
12. `TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION.md`
13. `artifacts/TAI5MSG_STRUCTURE_INDEX_MANIFEST.json`
14. `artifacts/tai5msg_structure_index_v1/INDEX.json`
15. this file

## 2. Product / authority boundary

The selective project is not a full clone of the PC Korean patch.

Priority Korean scope remains descriptions, event/system/context text, and structurally safe dialogue. Person/place identity, yomi/readings, calendar/name composition/input, and unresolved dynamic grammar remain Japanese or deferred unless separately promoted.

Authority remains:

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

Canonical policy:

`IDENTITY_IN_PROSE_POLICY.md`

Current status:

```text
identity_in_prose_policy = RESOLVED_IDENTITY_IN_PROSE_V1
```

First-release behavior:

```text
identity presentation fields            -> KEEP_JP
PC Korean prose identity literals        -> PRESERVE_AS_AUTHORED_KO
runtime-inserted person/place identity   -> KEEP_JP
prose-literal reverse substitution       -> FORBIDDEN
```

Meaning:

- dedicated person/place identity fields remain Japanese;
- yomi/readings/sort keys remain Japanese;
- surname/given-name composition remains Japanese;
- Korean name entry remains excluded;
- a Korean person/place spelling already authored as ordinary PC Korean prose remains Korean as part of that sentence;
- runtime-inserted person/place identity remains Japanese;
- the project intentionally tolerates the resulting visual naming mismatch;
- no Korean-prose -> Japanese-name normalization transform is created for first release.

This is an intentional low-cost product tradeoff and must not be reopened merely because the same identity appears in Japanese in one field and Korean in prose.

## 4. Particle / grammar interaction

`IDENTITY_IN_PROSE_V1` does not solve dynamic morphology by itself.

`FIXED_SURFACE_PARTICLE_V1` may be used only under its existing exact applicability gate.

The following remain separate unresolved causes when present:

- unknown physical owner/caller topology;
- shared-owner conflict;
- cross-message composition;
- copula/verb/speech-style/interrogative formatter responsibility;
- numeric-counter morphology;
- unknown Switch counterpart;
- storage/capacity/terminator safety.

No pronunciation inference is introduced for Japanese runtime identity tokens.

## 5. Classification metadata rule

Future corpus materialization should record identity handling explicitly when relevant.

Recommended metadata field:

```text
identity_token_policy
```

Allowed first-release values:

```text
KEEP_JP_IDENTITY_FIELD
PRESERVE_AUTHORED_KO_PROSE_LITERAL
KEEP_JP_RUNTIME_INSERT
NOT_APPLICABLE
```

This product metadata does not itself change:

```text
mechanism_class
usage_class
investigation_status
switch_applicability
switch_realization
derived_disposition
```

Release inclusion still requires normal owner/caller/risk/capacity/provenance gates.

## 6. Product-route exclusions and retained evidence

The following historical full-port artifacts remain excluded from the selective product baseline:

```text
V290 integrated full-port builder/build = EXCLUDE_FROM_SELECTIVE_PRODUCT
V291 package                            = EXCLUDE_FROM_SELECTIVE_PRODUCT
```

V291 remains historical failure / narrow diagnostic evidence only.

Separately retained:

```text
V285-V288 grammar125 analysis/manifest = OPTIONAL_R4_GRAMMAR_EVIDENCE
V289 implementation technique          = REFERENCE_ONLY
```

Do not incrementally subtract problems from V291 to create a selective product.

## 7. Persistent registry state

Current totals remain inherited from V293:

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

No candidate/classification IDs are created by V294.

## 8. TAI5MSG and owner boundaries remain unchanged

`ART-00000005` remains a PC-original <-> PC-Korean locator/length structure lattice only.

It does not by itself prove payload semantics, opcode/call structure, Switch physical-owner mapping, Switch caller topology, or release disposition.

Current proven selective Switch owner coverage remains the inherited F1 static 158 bindings where applicable.

Insufficient owner coverage blocks unsupported `INCLUDE_KO`; it does not prohibit source/container/mechanism inventory where evidence exists.

## 9. Mixed-script route safety

The product policy permits Japanese identity tokens and Korean prose to coexist.

Historical evidence shows at least one route can render both scripts, but route-wide safety is not globally assumed.

For each selected mixed-script family, mapping/font/transport behavior must preserve both Japanese and Korean on the actual Switch route.

## 10. Executable next scope — sole authority

The exact next selective scope remains:

```text
SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY
```

Purpose:

1. identify the source families/containers that actually own R1 descriptions/UI, R2 event/system context, and R3 dialogue candidates;
2. record per family/container which common classification fields are machine-extractable, manually decidable, or currently unavailable;
3. record current Switch owner/caller coverage per family;
4. bind reusable parsers, structure indices, and owner ledgers;
5. measure identity-in-prose exposure for coverage/QA planning under the already-fixed `IDENTITY_IN_PROSE_V1` policy;
6. identify whether TAI5MSG, EVENT/TS5, UI/description tables, or other containers are required for each release phase.

This scope is READ ONLY inventory/availability analysis.

It must not:

- create broad corpus classification rows;
- issue candidate/classification IDs;
- assign corpus dispositions;
- reopen or redesign `IDENTITY_IN_PROSE_V1`;
- mutate gameplay data;
- implement serializers/builders;
- create IPS/build/runtime artifacts.

A fresh explicit user execution signal is required before this scope begins.

## 11. Current non-materialized work

Still not materialized:

- cross-container R1/R2/R3 content-owner inventory;
- broader source-owner coverage outside F1-static-158;
- TAI5MSG selective corpus classifications;
- EVENT/TS5 production adapter;
- R1 description/UI adapters where needed;
- rewritten TAI5MSG/EVENT/UI payloads;
- selective serializers/builders;
- IPS/build;
- translation QA.

## 12. Repository write boundary

Repository writes remain restricted to:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API writes, branch creation, or force update are permitted.
