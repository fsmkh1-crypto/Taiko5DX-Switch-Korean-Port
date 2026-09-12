# PROJECT_STATE

Last updated: 2026-09-12 (KST)

## Current status

Repo: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`  
Branch: `main`

Stage 1 canonical inventory: COMPLETE.  
Stage 2 affine structural targeting: COMPLETE.  
F1 unique-anchor bounded localization sequence audit: COMPLETE.  
F1 158-row static write authorization/provenance closure: COMPLETE as historical V094 evidence.  
Machine-readable accounting v0.1 F1 pilot: COMPLETE / PASS.  
Schema-v1 amendment: IMPLEMENTED AS CANDIDATE / REGRESSION BLOCKED / NOT FROZEN.

The v1 candidate does not reauthorize or invalidate the prior F1 byte-analysis result. It normalizes accounting semantics and exposes a pre-existing provenance/transport defect in the committed V094 action-manifest file.

Canonical target:
- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

## Accounting snapshot

```text
historical mixed-granularity inventory records  27,430
leaf-obligation records after descriptor groups 27,419
inline rows                                      17,103
Stage-1 raw exceptions                           11,050
Stage-2 residual                                  1,248
conservative later target-resolved                  451
conservative target-unresolved residual              797
```

`27,430` and `27,419` are not universal progress percentages. Progress is tracked by family/axis with fixed denominators.

## F1 canonical population

```text
DIRECT_PORT authorized                    158
PADDING_RECONSTRUCTION_REQUIRED            75
SHARED_OWNER_BINDING_REQUIRED              25
TERMINATOR_CAPACITY_FAIL                    4
F1_RULE_REJECTED                           16
TOTAL                                     278
```

Machine axes remain:

```text
analysis RESOLVED                 262
analysis ANALYZED_UNRESOLVED       16
target RESOLVED                   262
closure CLOSED                    158
closure OPEN                      120
verified exclusions                0
```

The 25 shared-owner rows hand off to `SHARED_OWNER_BINDING`. Replacement conflict is not proven. Do not preclassify them as I4; owner binding must first determine I3 agreement vs I4 conflict/redirection.

## Machine-accounting v1 candidate

Current candidate artifacts:

- schema: `docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md`
- claim rules: `docs/CLAIM_EXTRACTION_RULES.md`
- amendment report: `docs/SCHEMA_V1_AMENDMENT.md`
- amendment ledger: `docs/VALIDATION_LEDGER_SCHEMA_V1_AMENDMENT.md`
- candidate overlay: `data/pilot/f1_v1_candidate/`
- validator library: `tools/machine_accounting_v1_candidate_lib.py`
- validator: `tools/validate_machine_accounting_schema_v1_candidate.py`
- V094 transport diagnostic: `tools/diagnose_f1_manifest_transport.py`
- fixtures: `tests/fixtures/machine_accounting_schema_v1.json`

Candidate design:

- semantic schema and transport format are independently versioned;
- source/action state is append-only revisioned;
- descriptor `GROUP` vs `OBLIGATION` is explicit;
- V094 remains the intended sole action-payload authority; no duplicate action truth source is created;
- compact source/edge data are deterministic seeds governed by a versioned materialization contract;
- claim IDs remain immutable; composite v0.1 claims are superseded rather than renumbered;
- 42 historical claim rows + 52 appended atomic claims -> 94 effective / 85 ACTIVE candidate claims;
- atomic claim refs and legacy evidence refs are separate;
- UNKNOWN remains a hard authorization blocker;
- invariant dependency fingerprints support `PASS -> STALE`, with STALE distinct from FAIL;
- target-resolution progress explicitly reports resolved/applicable, resolved/total and excluded/total.

## V094 manifest repository-artifact blocker

Canonical V094 provenance records:

```text
expected gzip SHA-256       8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
expected content SHA-256    c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
expected action rows        158
```

GitHub Actions run `34663770280` measured the current committed file:

```text
repository file bytes       21,288
repository SHA-256          826c73a0f80ae645420a189a4dd7b1e3637afd0e514fbc4f00d84189595daf37
gzip end-of-stream          false
recoverable payload bytes   314,998
recovered payload SHA-256   772ed05a0d3af9856eca3cf93165663b005d5ef9bbd06b228886c7f18ca51fc0
complete JSON actions       55 / 158
first malformed line        56
```

The repository payload is therefore semantically truncated, not merely missing a gzip footer.

Git history shows the same artifact blob from its introduction at commit `c6c7800177c46d320f3281ddd9fd9bf03b137726`; the schema-v1 amendment did not introduce this defect.

Interpretation:

- historical V094 authorization remains canonical evidence unless separately contradicted;
- the currently committed gzip cannot be consumed as a complete action table;
- missing 103 action payload rows must not be inferred/synthesized;
- candidate action/edge semantic hashes cannot be pinned from partial data;
- v1 regression cannot complete;
- schema remains NOT FROZEN.

## Authority boundary

Existing canonical Markdown remains authoritative.

No full V001–V100 machine migration has occurred. No full 27,430/27,419 source migration, no new 797 residual-family analysis, no builder/IPS/runtime implementation and no game-file modification were performed by the schema-v1 amendment.

R0/R1/R1B/R1C, Stage 1, Stage 2, F1 audit, F1 authorization, V095 cleanup, and V096–V098 pilot facts remain canonical. V099 records the candidate schema amendment. V100 records the manifest-artifact blocker; do not reinterpret it as technical disproof of V094.

## Mandatory boundaries

- PC patch is semantic authority.
- raw uniqueness is not a safety rule.
- target resolution is not write authorization.
- preserve internal Japanese yomi until its separate consumer/semantic gate is resolved.
- consumer tracing is an exception/family tool, not the default for structurally resolved rows.
- one diagnostic build = one root-cause family.
- no force-push and no silent source omission.
- no silent UNKNOWN authorization.
- no denominator exclusion without a verified exclusion claim.
- machine claim IDs are immutable after issuance.
- do not synthesize missing V094 action payloads from IDs/counts.

## Next stage

Fresh execution signal required.

Recommended next step: **V094 manifest provenance/transport repair only**.

Preferred order:

1. find an exact canonical manifest copy with gzip SHA-256 `8bbb...`;
2. if no exact artifact exists, reproduce it from the already-defined V093/V094 deterministic replay using the same canonical inputs, as artifact restoration rather than new F1 analysis;
3. prove content SHA `c612...`, gzip SHA `8bbb...`, 158 rows and existing stable IDs/source hash;
4. replace only the corrupted repository artifact;
5. rerun schema-v1 candidate regression and pin materialized semantic hashes;
6. report and STOP again before any schema-freeze declaration.

Do not combine the repair with full migration, the 797 residual, builder, IPS, runtime, mapping, or game-file work.
