# PC AUTHORED DERIVED SURFACE POLICY

Date: 2026-09-20 (KST)
Status: CANONICAL SELECTIVE-KO PRODUCT POLICY / V351 / NO IMPLEMENTATION
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Policy ID: `PC_AUTHORED_DERIVED_SURFACE_V1`

## 1. Purpose

This policy closes first-release handling for the exact V346 code-5 copula/derived-morphology cause family. Runtime escapes continue to produce values/controls; Korean derived morphology is preserved from the PC-authored EVENT literal. No pronunciation/final-consonant inference is introduced.

## 2. Authority boundary

```text
PC Korean EVENT prose / derived surface   SOURCE AUTHORITY
Switch escape/value expansion             STRUCTURAL AUTHORITY
runtime-inserted identity presentation    KEEP_JP under IDENTITY_IN_PROSE_V1
derived Korean morphology                 PRESERVE PC-AUTHORED EVENT LITERAL
```

No general Korean copula/ending/honorific selector is established in the Switch EVENT escape path or in the already-audited PC executable patch layer.

## 3. Canonical release decision

```text
runtime escape token            preserve
runtime-produced value          preserve Switch behavior
PC-authored derived surface     preserve exactly as authored
pronunciation inference         forbidden
escape-identity morphology      forbidden
global allomorph rewrite        forbidden
```

Opposite allomorph candidates are provenance only and never authorize rewriting.

## 4. Exact applicability

```text
COPULA_DERIVED_ONLY             59 rows
MIXED_DIRECT_AND_DERIVED_RISK    2 rows
derived occurrences             62
unique escape tokens            27
PC-authored surface forms       23
```

No `NON_PARTICLE_SUFFIX_ADJACENCY` row is eligible. Future implementation must rebind each V351 row to V334 original/PC-KO command hashes before mutation.

## 5. Cardinality rule

```text
FIXED_LOGICAL_REFERENCE_PRONUNCIATION_NOT_SINGLETON_SAFE   10 tokens / 11 occurrences
DYNAMIC_OR_LIMITED_DYNAMIC                                 17 tokens / 51 occurrences
pronunciation-singleton-safe tokens                         0 / 27
```

A logical fixed reference is not immutable pronunciation proof. No morphology may be selected from escape identity.

## 6. Surface-family rule

All 23 PC-authored surfaces are preserved per occurrence. Counterpart candidates in the artifact are linguistic provenance only:

`counterpart_candidate != authorized normalization`

This explicitly includes non-simple surfaces such as `와의` and `로군`.

## 7. Mixed composite

The exact two mixed rows use `V351_MIXED_COMPOSITE_V1`:

```text
raw PC-KO command
-> preserve derived surface
-> normalize only exact V351 direct occurrences
-> inherited EVENT structural validation
```

Exact direct edits:

```text
row 12476   \%00    이 -> 가
row 13029   \#07F0  을 -> 를
row 13029   \E079   을 -> 를
```

This does not expand V348's 350-row membership.

## 8. Product effect

```text
V351 rows admitted / not implemented   61
code-5 admitted total                  423
code-5 remaining DEFER                   3
V334 INCLUDE_KO                     12,594
V334 DEFER                               3
NON_KOREAN_TARGET                      478
TOTAL                                13,075
```

The remaining three DEFER rows are exactly the V346 non-particle-suffix family.

## 9. Forbidden shortcuts

Reject pronunciation inference, escape-identity allomorph selection, global copula rewriting, V345/V349 misuse, raw-copying mixed rows without their three direct fixes, V348 membership expansion, V346 regeneration, and any V351 widening to suffix-three.

## 10. Boundary

```text
implementation        NONE
product TS5 bytes     UNCHANGED
build/package/IPS     NONE
hardware              NOT RUN
```
