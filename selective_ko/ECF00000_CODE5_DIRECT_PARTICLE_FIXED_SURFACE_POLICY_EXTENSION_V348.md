# ECF00000 code-5 direct-particle fixed-surface policy extension — V348

Date: 2026-09-20 (KST)

```text
validation_id   V348
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_POLICY_EXTENSION_AND_APPLICABILITY_MATERIALIZATION
parent          aa0c89ff54f112761dbd5308dc1f7609c00a9f66 / V347 canonical + bounded-resume maintenance
product_bytes   UNCHANGED
implementation  NONE
build/package   NONE
hardware        NOT RUN
```

## 1. Scope

V348 closes only the product-policy applicability question left by V347 for the exact V346
`DIRECT_PARTICLE_ONLY` population.

```text
pure direct rows                    350
pure direct occurrences             386
mixed rows excluded                   2
mixed direct occurrences excluded     3
```

The exact 350-row membership is inherited from the V346 direct rowset
`c590ce16cf7d230e0a63914b2e5a2dff92bd0ecad35aa7d8b765b74563944ae6`.
V348 does not regenerate or broaden that semantic class.

The two `MIXED_DIRECT_AND_DERIVED_RISK` rows remain excluded because their direct-particle
portion is not sufficient to close their independently unresolved derived morphology.

## 2. Binding policy decision

The canonical first-release `FIXED_SURFACE_PARTICLE_V1` philosophy is extended through a
separate, ECF00000-specific applicability authority:

```text
extension id        DIRECT_ESCAPE_PARTICLE_V1
base policy         FIXED_SURFACE_PARTICLE_V1
eligible class      exact V346 DIRECT_PARTICLE_ONLY 350 only
V345 membership     unchanged
global substitution forbidden
```

V347 already closed the runtime-responsibility boundary:

```text
runtime escape owner               value/control expansion
following particle surface owner   EVENT authored literal
Switch runtime josa selector       NONE
PC patch runtime josa selector     NONE_ESTABLISHED
```

Therefore, for these exact pure-direct rows, the remaining first-release particle-specific
decision is only which member of the already canonical allomorphic pair to emit. No
pronunciation/final-consonant inference is required for the first release.

## 3. Fixed surfaces

The existing preferred surfaces remain unchanged:

```text
은 -> 는
이 -> 가
을 -> 를
과 -> 와
는 -> 는
가 -> 가
를 -> 를
와 -> 와
로 -> 로
```

This is not authorization to rewrite ordinary standalone particles elsewhere. Applicability is
limited to the exact V348 occurrence ledger.

## 4. Exact applicability

Across the 350 pure-direct rows:

```text
direct occurrences                 386
already preferred                  269
opposite-side                      117
normalization candidate rows       108
already-preferred-only rows        242
opposite-only rows                 104
both-side rows                       4
```

Source occurrence counts:

```text
가 104
는  81
를  47
와  27
로  10
이  45
은  50
을  13
과   9
----
386
```

Exact substitutions:

```text
은 -> 는    50
이 -> 가    45
을 -> 를    13
과 -> 와     9
------------
total      117
```

Post-policy target counts:

```text
가 149
는 131
를  60
와  36
로  10
----
386
```

## 5. Exact occurrence authority

Canonical artifacts:

`selective_ko/artifacts/ecf00000_v348_direct_escape_particle_policy_v1/APPLICABILITY.jsonl`

- 350 rows;
- exact V346 row/partition/original-offset/KO-offset/opcode bindings;
- per-row direct and normalization occurrence counts.

`selective_ko/artifacts/ecf00000_v348_direct_escape_particle_policy_v1/OCCURRENCES.jsonl`

- 386 occurrences;
- row ID;
- message-field index;
- decoded character offset;
- exact escape surface;
- source particle;
- approved target particle;
- compact Korean source/target bytes;
- substitution flag.

The V348 decoded locator is an applicability/provenance locator, not a raw-byte address.
A future implementation must rebind each row through the canonical V346/V334 `ko_offset +
ko_command_length` raw PC-KO slice, parse the actual message field, and verify the exact
escape + source-particle sequence before mutation.

```text
(row_id, escape) alone                    NOT SUFFICIENT
surface text search without row binding   FORBIDDEN
final Korean fresh grouping               NOT OWNER AUTHORITY
```

## 6. V346 human-ledger surface metadata correction

The V346 human-readable `LEDGER.jsonl` contains exactly two direct-hit records where the
diagnostic `surface` field disagrees with the actual occurrence and with `detector_head`:

```text
row 4094   escape \%00   detector_head 를   surface 는
row 7233   escape \%01   detector_head 를   surface 가
```

Both rows contain the same escape more than once with different following particles. The
observed shape is consistent with an occurrence-binding mistake in the auxiliary `surface`
metadata, but the generating-code root cause has not been proven and is therefore recorded only
as an inferred explanation.

Binding consequence:

```text
V346 compact ledger membership     unchanged
V346 350-row direct rowset         unchanged
direct occurrence total            unchanged
preferred/opposite counts          unchanged
V347 runtime conclusion            unchanged
V348 policy result                 unchanged
```

For V348 occurrence authority, `surface` is non-authoritative. The exact decoded source
adjacency and `detector_head` are used, and all 386 occurrences resolve with zero locator
failures.

## 7. Byte-impact boundary

The direct particle characters use the already established compact Korean two-byte surfaces.

Every V348 particle normalization is therefore:

```text
2 bytes -> 2 bytes
particle-specific payload delta = 0
```

This does not mean whole-row Korean replacement is length-neutral. The Korean command payload
can differ in total length from the original Japanese command, so the existing EVENT
reconstruction, relocation, special-span and validator responsibilities remain mandatory.

V345 is different and remains untouched:

```text
V345 explicit dual literal   6 bytes -> 2 bytes
V348 direct escape particle  2 bytes -> 2 bytes
```

The two policies share the preferred release surfaces, not the same transform implementation.

## 8. Product disposition

V348 closes the pure-direct particle policy gate and changes semantic product admission for only
the exact 350 pure-direct rows:

```text
code-5 population
  LEXICAL_FALSE_POSITIVE_GAMUN       12   INCLUDE_KO
  DIRECT_PARTICLE_ONLY              350   INCLUDE_KO / NOT IMPLEMENTED
  COPULA_DERIVED_ONLY                59   DEFER
  MIXED_DIRECT_AND_DERIVED_RISK       2   DEFER
  NON_PARTICLE_SUFFIX_ADJACENCY       3   DEFER
```

Effective V334-universe product overlay:

```text
INCLUDE_KO             12,533
DEFER                       64
NON_KOREAN_TARGET          478
------------------------------
TOTAL                    13,075
```

The original V335 semantic-detail vector is preserved as historical/source classification
provenance; V348 is a later product-policy overlay and does not rewrite that vector.

## 9. Rejected / do-not-repeat

Reject:

- append these 350 rows into the V344/V345 1,251-row ledger;
- modify the V345 particle serializer to pretend direct single particles are six-byte dual forms;
- use `(row_id, escape)` as a unique occurrence identity;
- use V346 human-ledger `surface` as authoritative occurrence content;
- globally replace standalone `은/는/이/가/을/를/과/와/로`;
- assign a fixed particle by escape identity;
- promote either mixed row because its direct portion is now policy-resolved;
- send copula-derived or verbal-suffix morphology through this policy;
- infer that zero particle-byte delta removes EVENT relocation/rebuild obligations.

## 10. Current disposition / next scope

```text
V347 runtime responsibility             CLOSED
V348 direct-escape policy extension     CLOSED
V348 exact applicability                350 rows / 386 occurrences
V348 product admission                  350 INCLUDE_KO / NOT IMPLEMENTED
V345 membership                         UNCHANGED
mixed / copula / suffix                 DEFER 2 / 59 / 3
implementation                          NONE
product bytes                           UNCHANGED
build/package/IPS/hardware              NONE
```

Exact next scope after a fresh explicit user signal:

`ECF00000_DIRECT_ESCAPE_PARTICLE_V1_IMPLEMENTATION_OFFLINE_VALIDATION`

Implement only the exact V348 350-row applicability population through a separate direct-escape
path. Rebind every row from canonical raw PC-KO offset/length slices, verify occurrence
provenance before mutation, preserve V345 membership unchanged, and rerun the inherited EVENT
relocation/special-owner/5A/residual-validator gates. Do not promote the mixed rows, process
copula-derived morphology, build/package/IPS, or run hardware without another fresh
authorization.
