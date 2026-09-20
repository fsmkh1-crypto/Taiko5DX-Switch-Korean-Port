# ECF00000 code-5 PC-authored derived-surface policy and applicability — V351

Date: 2026-09-20 (KST)

```text
validation_id   V351
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      POLICY_AND_EXACT_APPLICABILITY_MATERIALIZATION
parent          6b71216089cf6cf852c56a5b2944d76c474b250a / V350
product_bytes   UNCHANGED
implementation  NONE
build/package   NONE
hardware        NOT RUN
```

## 1. Exact scope

```text
pure derived rows       59
mixed rows               2
total rows              61
derived occurrences     62
unique escapes          27
authored surfaces       23
mixed direct edits       3
```

Membership is inherited from V346 and is not rediscovered from final Korean.

## 2. Runtime responsibility

At all 62 derived occurrences the PC Korean payload preserves the runtime escape and authors the following Korean morphology literally. Switch escape handling owns value/control expansion, not Korean copula selection. The audited PC runtime patch layer establishes no Korean copula selector.

## 3. Policy

Canonical policy: `selective_ko/PC_AUTHORED_DERIVED_SURFACE_POLICY.md`

Policy ID: `PC_AUTHORED_DERIVED_SURFACE_V1`

Release action: preserve each exact PC-authored derived surface; do not infer pronunciation or choose morphology from escape identity.

## 4. Cardinality

```text
fixed logical reference / pronunciation not singleton-safe   10 tokens / 11 occurrences
dynamic or limited-dynamic                                   17 tokens / 51 occurrences
pronunciation-singleton-safe                                  0 tokens
```

Artifact: `selective_ko/artifacts/ecf00000_v351_pc_authored_derived_surface_policy_v1/ESCAPE_CARDINALITY.json`

## 5. Surfaces

23 exact surface forms / 62 occurrences are materialized in:

`selective_ko/artifacts/ecf00000_v351_pc_authored_derived_surface_policy_v1/SURFACE_FAMILIES.json`

Every record has `normalization_authorized=false`. Counterpart candidates are provenance only.

## 6. Exact rows and byte impact

`selective_ko/artifacts/ecf00000_v351_pc_authored_derived_surface_policy_v1/ROWS.jsonl`

```text
pure 59 raw growth     +944
mixed 2 raw growth      +28
combined               +972
```

V334 ROWS.jsonl remains the exact command-hash authority by row ID.

## 7. Occurrences

`selective_ko/artifacts/ecf00000_v351_pc_authored_derived_surface_policy_v1/OCCURRENCES.jsonl`

contains 62 exact row/hit/escape/surface bindings.

## 8. Mixed composite

`selective_ko/artifacts/ecf00000_v351_pc_authored_derived_surface_policy_v1/MIXED_COMPOSITE.jsonl`

```text
row 12476   \%00    이 -> 가
row 13029   \#07F0  을 -> 를
row 13029   \E079   을 -> 를
```

Transform order is raw PC-KO overlay -> preserve derived morphology -> exact direct normalization -> inherited EVENT gates.

## 9. Product admission

```text
V349 direct-only implemented              350
V350 lexical false-positive implemented    12
V351 pure derived admitted                  59 / NOT IMPLEMENTED
V351 mixed composite admitted                2 / NOT IMPLEMENTED
code-5 admitted total                      423
remaining DEFER                              3

V334 INCLUDE_KO                          12,594
V334 DEFER                                    3
NON_KOREAN_TARGET                           478
TOTAL                                    13,075
```

Only the three V346 `NON_PARTICLE_SUFFIX_ADJACENCY` rows remain DEFER.

## 10. Rejected / do-not-repeat

Reject hidden Korean copula selectors, escape-ID morphology, pronunciation inference, global allomorph rewriting, fixed-ID pronunciation assumptions, universalizing `와의`/`로군`, raw-copying mixed rows without direct fixes, V348 expansion, V346 regeneration, or suffix-three inclusion.

## 11. Next scope

`ECF00000_CODE5_PC_AUTHORED_DERIVED_SURFACE_IMPLEMENTATION_OFFLINE_VALIDATION`

Implement exact V351 61 only: pure 59 raw PC-KO overlays; mixed 2 via `V351_MIXED_COMPOSITE_V1`; bind V334 command hashes; run inherited EVENT gates. No suffix-three, build/package/IPS, or hardware without fresh authorization.
