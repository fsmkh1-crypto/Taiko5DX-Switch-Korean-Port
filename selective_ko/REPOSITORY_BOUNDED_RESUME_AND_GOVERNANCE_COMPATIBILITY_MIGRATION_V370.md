# Repository bounded-resume and governance compatibility migration — V370

Date: 2026-09-22 (KST)

```text
validation_id   V370
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      REPOSITORY_ADMINISTRATIVE_MIGRATION
parent          5fb2499d6bbbd4ffd4d0c7a4122d0a510f9e5f77 / V369
product bytes   UNCHANGED
builder code    UNCHANGED
serializer      NOT IMPLEMENTED
build/package   NONE
hardware        NOT RUN
```

## 1. Purpose

V370 reduces resume/bootstrap cost and repairs governance-contract drift without changing any V366-V369 product finding.

The migration separates:

- active resume routing;
- exact-scope execution inputs;
- lazy historical provenance;
- failure discovery;
- current selective validation identity.

Historical Git evidence is preserved. No history rewrite, artifact deletion, ledger resharding, or product implementation is part of this scope.

## 2. Pre-migration baseline

Pinned V369 state:

```text
PROJECT_STATE.md                         175,202 bytes
selective_ko/SELECTIVE_PROJECT_STATE.md 101,708 bytes
selective_ko/KNOWN_FAILURES.md           56,220 bytes
```

The V369 root resume object carried 166 required-read paths.
The V369 selective state carried 165 numbered historical dependency paths.

The repository already had a bounded-read policy, but the active state still physically accumulated historical material.

## 3. Governance drift closed by this migration

The V369 push had a failing `Document governance` workflow.

The first observed CI failure was document-authority coverage drift: seven Markdown files under `docs/` were present in the repository but absent from `docs/DOCUMENT_AUTHORITY_INDEX.json`.

Static inspection also identified additional contract drift that would become blocking after the first failure was removed:

- V369 `scope_kind` used a descriptive checkpoint value while the validator accepts only operational `READ_ONLY` / `REPOSITORY_WRITE` modes.
- FZ001 remained declared, while the compact validator contract expected explicit declaration/basis fields not present in the accumulated V369 resume object.
- closure identity for the selective track was compared against the historical root `docs/VALIDATION_LEDGER.md`, whose latest full-port entry predates the selective V369 checkpoint.

V370 treats these as one governance-schema drift family rather than independent patches.

## 4. New bounded-resume architecture

Normal bootstrap becomes:

```text
AGENTS.md
-> PROJECT_STATE.md
-> active PROJECT_RESUME_V2.required_reads
-> current checkpoint / compact INDEX
-> exact-scope execution inputs on demand
-> historical provenance only when a concrete question requires it
```

`required_reads` is now an active bootstrap set, not a historical superset.

The full V369 pre-compaction state remains recoverable from pinned Git snapshots listed in:

`selective_ko/RESUME_HISTORY_INDEX.json`

Detailed rejected paths remain byte-preserved in:

`selective_ko/KNOWN_FAILURES.md`

Topic-level discovery is provided by:

`selective_ko/KNOWN_FAILURES_INDEX.json`

## 5. Validation identity routing

The selective track now uses:

`selective_ko/VALIDATION_INDEX.json`

for current validation/checkpoint identity.

The historical root `docs/VALIDATION_LEDGER.md` remains historical/full-port validation evidence and is no longer overloaded as the selective-track current validation counter.

The document-governance validator preserves the historical fallback for non-selective tracks while using the selective index when:

`active_product_track == SWITCH_SELECTIVE_KOREANIZATION`.

## 6. FZ001 compatibility

V370 restores the explicit FZ001 resume fields required by the existing schema-freeze validator:

```text
schema_freeze_declaration
schema_freeze_declaration_git_blob_sha
schema_freeze_basis_validation_id
schema_freeze_basis_ci_run_id
schema_freeze_basis_head
```

These values are taken from the existing canonical freeze declaration and do not change FZ001.

## 7. Document-authority coverage

The seven already-existing root/docs Markdown files omitted from the authority registry are registered as historical/canonical evidence with current-plan authority remaining with `PROJECT_STATE.md`.

No selective-subtree Markdown is silently added to the root document-authority registry; the validator's current Markdown coverage scope remains explicit.

## 8. Product facts preserved

V370 does not rederive or modify:

```text
source-owner universe                    66,987
direct/header-preserved                  66,956
overlap-composite                            31

post-policy INCLUDE_KO                    52,491
UNRESOLVED                                     0
NON_KOREAN_TARGET                         14,496

V369 overlap nodes                           210
relations                                    130
connected clusters                            87
final write-responsibility units              80
```

The V369 applicability large artifact, overlap ledgers, V366/V367/V368 authorities, and all existing product hashes remain unchanged.

## 9. Out of scope

V370 does not:

- implement or modify an EVENT serializer;
- modify any builder module;
- mutate EVENT or TAI5MSG bytes;
- reshard or relocate V369 ledgers;
- rewrite historical checkpoints;
- split the detailed KNOWN_FAILURES registry;
- make the V369 applicability materializer portable;
- build/package/IPS;
- perform hardware/runtime testing.

Materializer portability and broader storage optimization remain optional later administrative work and must not delay the serializer unless a concrete dependency requires them.

## 10. Exact next product scope

After a fresh explicit user execution signal:

`EVENT_169_RUNTIME_OVERLAP_CLUSTER_SERIALIZER_IMPLEMENTATION_OFFLINE_VALIDATION`

The next product stage must consume the V369 exact applicability authority and the 80 final write-responsibility units without reopening V366-V369 closed analysis.

STOP after V370 migration/validation closure.
