# SELECTIVE PROJECT STATE

Date: 2026-09-22 (KST)
Status: V370 BOUNDED RESUME / GOVERNANCE MIGRATION CLOSED / EVENT SERIALIZER IMPLEMENTATION AWAITS FRESH INSTRUCTION
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`  
Branch: `main`  
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

Repository-level resume authority: `../PROJECT_STATE.md`.

Current checkpoint:
`REPOSITORY_BOUNDED_RESUME_AND_GOVERNANCE_COMPATIBILITY_MIGRATION_V370.md`

Current product authority:
`EVENT_169_APPLICABILITY_AND_OVERLAP_CANONICALIZATION_V369.md`

Current validation index:
`VALIDATION_INDEX.json`

Historical dependency catalog:
`RESUME_HISTORY_INDEX.json`

Failure discovery index:
`KNOWN_FAILURES_INDEX.json`

Bounded resume policy:
`BOUNDED_RESUME_READ_POLICY.md`

The current bootstrap set is intentionally small. Historical dependencies are lazy provenance references, not mandatory resume reads.

## 2. Frozen V369 product state

```text
source-owner universe                    66,987
direct/header-preserved                  66,956
overlap-composite                            31

post-policy INCLUDE_KO                    52,491
post-policy UNRESOLVED                         0
NON_KOREAN_TARGET                         14,496

V368 generalized applicability rows        2,438
detector-related occurrences               2,671
fallback classifications                       0

overlap graph nodes                          210
relations                                    130
connected clusters                            87
final write-responsibility units              80

product-relevant multi-owner outer rows       91
direct-inner relations                       108
composite-inner relations                     22
```

V366 source membership/binding, V367 runtime continuity, V368 semantic-policy closure, and V369 exact ledgers remain VERIFIED/CLOSED and must not be regenerated merely to resume.

## 3. Current EVENT serializer design authority

Applicability INDEX:
`artifacts/event_169_v368_exact_applicability_v1/INDEX.json`

Overlap design INDEX:
`artifacts/event_169_overlap_cluster_design_v1/INDEX.json`

Important frozen design facts:

- 87 connected components are governed by 80 final write-responsibility units.
- Independent owner serialization is not approved for any of the 87 clusters.
- Seven cluster pairs share relocation responsibility through 12 fields.
- 17 fixed-surface-particle intersections are exact existing-policy intersections.
- 22 overlap-composite owners participate; all are direct outer -> composite inner relations.
- Five leading-control-recovery owners participate.
- Runtime-only inner owner `EKF00800:F60` must be addressable without assuming grouped-item ownership.
- Five connected `NON_KOREAN_TARGET` owners remain preservation boundaries.
- C31 ordering is fixed: V366 canonical composite reconstruction first, then the approved particle transform.
- Partial-overlap clusters must serialize the full union range rather than using one outer endpoint.

## 4. Execution inputs for the next product stage

These are execution/data inputs, not mandatory bootstrap prose reads.

Overlap graph/data:

- `artifacts/event_169_overlap_cluster_design_v1/NODES.jsonl`
- `artifacts/event_169_overlap_cluster_design_v1/EDGES.jsonl`
- `artifacts/event_169_overlap_cluster_design_v1/CLUSTERS.jsonl`
- `artifacts/event_169_overlap_cluster_design_v1/TRANSACTION_DOMAINS.jsonl`
- `artifacts/event_169_overlap_cluster_design_v1/RELOCATION_PLANS.jsonl`
- `artifacts/event_169_overlap_cluster_design_v1/STRUCTURAL_FIELD_VIEWS.jsonl`
- `artifacts/event_169_overlap_cluster_design_v1/SUPPORT_OWNERS.jsonl`
- `artifacts/event_169_overlap_cluster_design_v1/COMPOSITE_MEMBERSHIP_31.jsonl`

Applicability data:

- pinned V369 large artifact described by `artifacts/event_169_v368_exact_applicability_v1/INDEX.json`
- exact `APPLICABILITY.jsonl` row count: 2,438
- exact ledger SHA-256: `b9c421d18e7ce0a5d7603d7d3e764ad102bf791d965d7216edac85682a838c43`

Existing implementation surfaces that may be consumed or refactored by the authorized serializer stage:

- `../builder/selective_event.py`
- `../builder/selective_event_particle.py`
- `../builder/selective_event_direct_particle.py`
- `../builder/selective_event_code5_lexical.py`
- `../builder/selective_event_derived_surface.py`
- `../builder/selective_event_suffix3.py`
- `../builder/selective_event_5a.py`
- `../builder/selective_event_validation.py`

Do not treat existing ECF00000 wrappers as automatically valid corpus-wide writers. V369 owner/occurrence/transaction authority controls.

## 5. Other open product work

Unchanged separate work:

```text
non-B24 reflow candidates     584   not implemented
inline release corpus         139   classified, not implemented
SNR                                 separate track
final layout/translation QA         pending
```

These cause families must not be mixed into the EVENT overlap serializer implementation diagnostic stage.

## 6. Rejected paths and provenance

Use `KNOWN_FAILURES_INDEX.json` to locate the relevant section in `KNOWN_FAILURES.md`.

The following remain especially binding for the next EVENT implementation stage:

- no row-by-row treatment of the 130 overlap relations;
- no fallback semantic admission;
- no final-PC-KO fresh grouping as source-owner authority;
- no PC-KO structural-byte authority over Switch headers/control;
- no reuse of the rejected V334/Switch event-length mismatch hypothesis;
- no use of the superseded raw V367 89/128 overlap population;
- no independent final writer for shared relocation fields.

## 7. Exact next scope

A fresh explicit user execution signal may authorize:

`EVENT_169_RUNTIME_OVERLAP_CLUSTER_SERIALIZER_IMPLEMENTATION_OFFLINE_VALIDATION`

Until that signal, implementation, product mutation, build/package/IPS, and hardware execution remain unauthorized.

The next implementation stage must use the 80 final write-responsibility units as the final write-ownership authority and validate the complete 66,987-owner product accounting without reopening V366-V369 closed analysis.
