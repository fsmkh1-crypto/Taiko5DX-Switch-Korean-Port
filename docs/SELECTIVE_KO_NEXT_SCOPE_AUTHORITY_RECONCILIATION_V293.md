# Selective-KO Next-Scope Authority Reconciliation — V293

Date: 2026-09-17 (KST)
Status: CANONICAL ROUTING / PRODUCT-GOVERNANCE CORRECTION
Validation ID: `V293`
Scope: `SELECTIVE_KO_NEXT_SCOPE_AUTHORITY_RECONCILIATION`
Implementation authorization: NONE
Build authorization: NONE
New WRITE_SAFE authorization: 0

## 1. Authority and inherited state

Base canonical state:

```text
main HEAD = 405b866d31997bd0b277be11507e8441ba62f08d
tree      = 78eb095a1857e51f16b8f049c70b8163cda4cf98
last closed validation = V292
```

All previously VERIFIED/CLOSED technical evidence remains inherited without revalidation, including FZ001, Stage1/Stage2/F1 provenance, Mapping 10,036, Pointer-56 analysis, TAI5MSG 33 blocks / 14,832 logical slots, V272-V291, the V288 grammar125 manifest, and the V292 product-route reconciliation.

V293 changes project routing and audit-derived product-governance constraints only. It does not mutate gameplay data, create classification rows, implement a builder, or create a build.

## 2. External design-audit result consumed

An independent architecture review of the V292 selective design returned `SOUND_WITH_CORRECTIONS`.

The following findings are accepted:

- executable `next_scope` declarations had drifted across multiple documents;
- `ART-00000005` is a deterministic locator/length structure lattice and must not be promoted into payload/opcode/caller/owner classification evidence;
- current proven Switch physical-owner coverage is 158 F1 rows, which is insufficient to authorize release inclusion for the broader selective corpus;
- the current product has an unresolved `identity-in-prose` policy question for Korean explanatory text that contains person/place names while identity fields themselves remain Japanese;
- broad TAI5MSG classification should not be the immediate product step before the project knows which containers/source families actually own R1/R2/R3 content and which classification fields are available there;
- V290/V291 must remain excluded from the selective product baseline.

The following audit statements are qualified rather than adopted literally:

- lack of owner coverage does not make all source/mechanism analysis impossible; it blocks final release inclusion until the owner/caller gates are closed;
- TAI5MSG is not assumed to be dialogue-only; its product-role distribution remains to be inventoried;
- mixed Japanese/Korean rendering has been observed on at least one historical V291 runtime route, but that observation does not prove all selective routes safe.

## 3. Single executable next-scope authority

Effective after V293:

```text
selective executable next-scope authority
  = selective_ko/SELECTIVE_PROJECT_STATE.md
```

The repository-root `PROJECT_STATE.md` routes into that authority but does not duplicate the exact executable next scope.

The following documents are design/history/reference documents and must not independently route execution:

- `selective_ko/README.md`
- `selective_ko/ARCHITECTURE.md`
- `selective_ko/CLASSIFICATION_SCHEMA.md`
- `selective_ko/FIXED_PARTICLE_POLICY.md`
- `selective_ko/MIGRATION_MANIFEST.json`
- historical validation documents including V292

Any historical `next_scope`/`next stage` statement retained for provenance is non-authoritative once superseded by the selective state file.

## 4. Corrected immediate next scope

The immediate next selective scope becomes:

```text
SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY
```

Purpose:

1. identify which source families/containers actually own R1 descriptions/UI, R2 event/system context, and R3 dialogue candidates;
2. record, per container/source family, which common classification fields are:
   - machine-extractable now;
   - manually decidable now;
   - unavailable without a new parser/adapter/owner expansion;
3. record the current Switch physical-owner/caller coverage available for each family;
4. identify which existing parsers, structure indices, and owner ledgers can be reused;
5. sample/measure `identity-in-prose` exposure sufficiently to support the later product-policy decision;
6. identify whether TAI5MSG, EVENT/TS5, UI/description tables, or other containers are required for each release phase.

This scope is an inventory/availability analysis only.

It must not:

- create broad corpus classification rows;
- issue candidate/classification IDs;
- assign `INCLUDE_KO`/`KEEP_JP`/`DEFER_KO` to the corpus;
- decide the final identity-in-prose policy;
- mutate TAI5MSG/EVENT/UI data;
- implement a serializer/builder;
- create IPS/build/runtime artifacts.

## 5. Identity-in-prose boundary

The first-release identity policy remains:

```text
person names / place names / yomi / name composition / calendar identity = KEEP_JP by default
```

However, Korean explanatory/narrative source text may contain Korean-rendered person/place names as literals inside prose.

V293 does not decide whether those embedded identity tokens should:

- remain as the PC Korean prose source supplies them;
- be transformed back to Japanese identity spelling;
- follow a context-dependent policy.

This remains an explicit product-policy decision that must be closed before R1 release materialization can rely on such prose.

`translation_review_status = DEFER_TO_RUNTIME_QA` must not be used to defer this product-policy decision as if it were ordinary translation polish.

## 6. TAI5MSG structure-lattice boundary

`ART-00000005` remains directly reusable for deterministic logical location only:

```text
33 blocks
14,832 messages
1:1 PC-original <-> PC-Korean logical slots
locator_determinism = PASS
```

It does not, by itself, authorize claims about:

- decoded payload semantics;
- opcode/call structure;
- append/formatter responsibility;
- Switch physical owner;
- Switch caller topology;
- release disposition.

Also, the 14,832-slot lattice is a PC-original <-> PC-Korean structural correspondence artifact; it must not be read as proof of a complete Switch counterpart mapping.

## 7. Owner / release-inclusion boundary

Current selective registry evidence remains:

```text
F1 PC source entities      = 158
Switch physical owners     = 158
BINDS_TO edges             = 158
```

These 158 owner bindings remain reusable where the same selected source is consumed.

For the broader corpus:

- source/mechanism inventory may proceed where evidence exists;
- release inclusion must remain unresolved until required Switch owner/caller/applicability/capacity gates close;
- raw source uniqueness or a TAI5MSG locator does not substitute for Switch ownership.

## 8. V290 / V291 product disposition correction

Selective product disposition is now explicit:

```text
V290 integrated full-port builder/build = EXCLUDE_FROM_SELECTIVE_PRODUCT
V291 package                            = EXCLUDE_FROM_SELECTIVE_PRODUCT
V291 role                               = HISTORICAL_FAILURE_EVIDENCE / narrow historical diagnostic evidence only
```

Do not:

- use V290/V291 as a selective builder baseline;
- subtract problems from V291 until it looks selective;
- import V291 payloads into the selective release.

The following remain separately reusable:

```text
V285-V288 grammar125 analysis/manifest = OPTIONAL_R4_GRAMMAR_EVIDENCE
V289 implementation technique          = REFERENCE_ONLY
V291 screenshots/runtime observations  = HISTORICAL_FAILURE_EVIDENCE
```

## 9. Architectural sequence after V293

This is guidance, not an executable routing declaration outside the selective state file:

1. content-container / field-availability inventory;
2. identity-in-prose product-policy decision;
3. R1 owner/structure closure for selected description/UI families;
4. R1 classification/materialization and diagnostic build;
5. R2 event/system structure/owner closure and diagnostic build;
6. R3 safe-dialogue payload/caller/owner classification and diagnostic build;
7. optional R4 grammar work using grammar125 and other family evidence where applicable.

If the inventory proves that a different container ordering is required, change the roadmap explicitly rather than silently reinterpreting an old `next_scope` statement.

## 10. STOP boundary

V293 ends after documentation/state routing materialization.

No content-container inventory is performed in V293.

The next analysis requires a fresh explicit user execution signal and must use the exact current scope from `selective_ko/SELECTIVE_PROJECT_STATE.md`.

## 11. Repository write boundary

Repository mutation for V293 is permitted only through:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API write action, branch creation, or force update is permitted.
