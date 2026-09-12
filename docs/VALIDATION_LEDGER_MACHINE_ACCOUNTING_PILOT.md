# VALIDATION LEDGER — Machine-readable accounting pilot

Date: 2026-09-12
Scope: schema design and F1 278-row migration pilot only. No full-corpus migration, schema freeze, residual-family analysis, builder, IPS, or runtime work.

Detailed report: `docs/F1_MACHINE_ACCOUNTING_PILOT.md`

## V096 — machine-accounting schema v0.1 closes the identified accounting-model holes

**Status:** `VERIFIED AS PILOT DESIGN / NOT FROZEN`

The pilot schema explicitly provides:

- immutable claim-level IDs and partial supersession;
- append-only source-state revisions beginning at migration revision 1 rather than reconstructed history;
- independent action and source/action edge tables supporting 1:1, 1:N, N:1 and N:M;
- structured UNKNOWN debt with reason, resolution requirement and blocking gates;
- fixed total/applicable/excluded denominator semantics;
- `closure_state` independent from `terminal_disposition`;
- family-scoped write-authority responsibility plus `handoff_family`;
- invariant dependency/stale semantics where `STALE != FAIL`;
- descriptor leaf-obligation accounting (`14` subpatch obligations; `11` containers are grouping only);
- migration-manifest and source-anchor coverage gates;
- hard isolation of `FIXTURE-*` synthetic test IDs.

Historical `27,430` is retained only as a mixed-granularity inventory-record count. It is not used as one universal progress denominator.

Reuse rule: do not full-migrate the corpus or treat the schema as frozen solely because V096 exists. The pilot is allowed to reveal further schema changes.

## V097 — the F1 278-row source/action pilot preserves canonical membership and blocker semantics

**Status:** `VERIFIED / PILOT PASS`

Exact machine-state counts:

```text
sources                       278
target-resolved               262
analyzed-unresolved             16
closed DIRECT_PORT            158
open                           120
actions                       158
source/action edges           158
verified scope exclusions       0
```

Blocker split:

```text
PADDING_RECONSTRUCTION_REQUIRED  75
SHARED_OWNER_BINDING_REQUIRED    25
TERMINATOR_CAPACITY_FAIL          4
F1_RULE_REJECTED                 16
```

The 16 F1-rejected rows store only `candidate_target_identity`; `target_identity` remains null.

The 25 shared-owner rows hand off to `SHARED_OWNER_BINDING`, not I4, because V089 proves no simultaneous replacement conflict. Owner binding must first determine I3 agreement versus I4 conflict/redirection.

Write-authority responsibility is family-scoped:

```text
F1_LOCALIZATION_STATIC_DIRECT  158 / 158
F1_PADDING_RECONSTRUCTION        0 / 75
F1_STORAGE_RECONSTRUCTION        0 / 4
SHARED_OWNER_BINDING             0 / 25
```

The V094 ordered authorized-source hash remains `87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e`.

UNKNOWN debt is explicit: `target_identity=16`, `owner_binding=25`. No UNKNOWN that blocks write authorization is authorized.

## V098 — claim extraction, exact source round trip, coverage, and isolated cardinality fixture all pass

**Status:** `VERIFIED / PILOT PASS`

V088-V095 produced `42` atomic claims under the pilot extraction rules. Negative knowledge is represented explicitly as `EVIDENCE_GAP`; authorization limits are explicit `BOUNDARY` claims.

`docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md` source coverage:

```text
source blocks                 61
assertion-bearing / extracted 47
narrative-only                 2
metadata                      12
unexplained                    0
```

The coverage record reconstructs the exact canonical document with Git blob `ba9c660cf6f229ec2b19f024b9bc2cef94d26a44`; unexplained round-trip differences = `0`.

A synthetic fixture validates 1:N, N:1 and N:M edge capability under `tests/fixtures/` only. All fixture IDs use reserved `FIXTURE-*`; the validator rejects that prefix in project pilot state.

Seven-gate result:

```text
membership preservation                 PASS
provenance preservation                 PASS
blocker meaning preservation            PASS
source/action cardinality preservation  PASS
UNKNOWN silent-pass prevention          PASS
unexplained round-trip diff = 0         PASS
source-anchor unexplained blocks = 0    PASS
```

**Boundary:** V098 validates the pilot representation and validator behavior. It does not make generated pilot data authoritative over existing canonical Markdown, freeze the schema, or authorize wider migration.

## Stopping point

Schema design + F1 278 pilot are complete and pass. Schema remains unfrozen. Fresh user execution signal is required for schema-freeze review or any wider migration.
