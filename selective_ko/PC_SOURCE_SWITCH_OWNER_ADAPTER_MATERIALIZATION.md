# PC SOURCE / SWITCH OWNER ADAPTER MATERIALIZATION

Date: 2026-09-15 (KST)
Status: PRODUCTION REGISTRY SEED MATERIALIZED / REFERENCE-BACKED / NON-EXHAUSTIVE / NO CANDIDATE / NO BUILD
Scope: `PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION`

## 1. Purpose

This stage materializes the first persistent production identity/provenance records for the READY `PC_SOURCE_ADAPTER` and `SWITCH_OWNER_ADAPTER` layers. It consumes already-canonical evidence. It does not reopen `dinput8.dll`, F1 targeting, semantic-owner analysis, Switch write-safety analysis, TAI5MSG, or EVENT/TS5.

The first production cohort is intentionally bounded to the first canonical shard of the F1 static-write authorization manifest: 8 exact 1:1 PC-source / Switch-owner bindings. This is a production registry seed, not an exhaustive T5K or F1 population claim. Expansion is append-only.

## 2. Materialization basis and canonical inputs

Repository snapshot before this materialization:

```text
main commit = 2d78b64ab3a13c98e6faaf86f69ec35698be7682
main tree   = a56e71f5eeef7ceb3468c397d4a28f275ac8d363
```

The repository snapshot is run provenance, not a freshness dependency by itself. Adapter freshness is recomputed from immutable direct inputs and contract dependencies.

Direct input identities:

- F1 manifest index: `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST/INDEX.json`
  - Git blob `479b21c8bcbaa09aaf845906179411c3cec6dafb`
- F1 seed shard: `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST/part-01.jsonl`
  - Git blob `235ca401ca313369b90b76e710fcc0329312a716`
  - canonical semantic SHA-256 `0c57bf4da934b20fe93ccf39aed0fb0aba6d6d6b9c7ab82dbff778d84e33776b`
  - rows used: 8, lines 1-8
- identity/provenance contract:
  - `selective_ko/IDENTITY_PROVENANCE_CONTRACT.md`
  - Git blob `da67fff27e6845bb29e728c41ebb763553512bac`

Context-only policy identities, not output-driving freshness dependencies in this stage:

- applicability/realization taxonomy blob `9813ea91ff5bb8e331b5da721219e15713480fe8`
- fixed-particle policy blob `36d6a1530bc96b40a00b96d64dd6173aab834ef5`

No PC runtime/parser reverse engineering was rerun.

## 3. Materialized registry seed

Issued opaque IDs:

```text
entity_id         16
edge_id            8
artifact_id        2
candidate_id       0
manual_task_id     0
classification_id  0
```

Entity population:

```text
PC_SOURCE_INLINE         8
SWITCH_PHYSICAL_OWNER    8
```

Binding population:

```text
BINDS_TO                 8
cardinality in seed      1:1 x 8
```

The seed PC rows are:

```text
R36
R103
R128
R136
R137
R138
R139
R140
```

Their original/replacement bytes, PC RVA, Switch localization ID, target-object/write-window locators, storage class, language domain, terminator mode, and historical authorization action are copied only from the canonical F1 row-level manifest. No target discovery is rerun.

Persistent issued IDs:

```text
PC entities:     ENT-00000001 .. ENT-00000008
Switch owners:   ENT-00000009 .. ENT-00000016
binding edges:   EDG-00000001 .. EDG-00000008
artifacts:       ART-00000001 .. ART-00000002
```

## 4. Candidate and classification boundary

All eight source/owner records and binding edges retain:

```text
candidate_id = null
candidate_status = NOT_ISSUED
```

This stage emits zero:

- mechanism/usage classification rows;
- applicability rows;
- realization rows;
- release-scope decisions;
- derived dispositions;
- work-queue rows;
- fixed-particle classifications;
- manual tasks.

Historical full-port action labels are provenance only. `DIRECT_PORT` or static-write authorization is not imported as a selective realization value.

## 5. Field evidence and native-locator separation

Every production entity keeps its persistent opaque `entity_id` separate from native locators.

PC native locator evidence includes:

- canonical F1 record ID;
- source ID;
- PC RVA;
- source/replacement payload.

Switch owner native locator evidence includes:

- localization ID;
- target object/write window;
- terminator offset/mode;
- runtime destination cell;
- storage class;
- language domain.

Each field claim points to one line-specific provenance record in `registry/provenance.jsonl`. The F1 manifest line is evidence for the locator/fact; it is not used to generate the opaque entity ID.

## 6. Artifact freshness

Production artifact IDs:

```text
ART-00000001  PC_SOURCE_ADAPTER
ART-00000002  SWITCH_OWNER_ADAPTER
```

Creation-time freshness is `FRESH`, recomputed from the F1 index/shard identities and the identity/provenance contract. Stored creation-time freshness is not authority; downstream consumers must recompute it.

Output SHA-256:

```text
registry/REGISTRY_STATE.json                         ce29f06b99f6de6a2fcfd8d560a28f1e2616c630316371e2aea3936048620496
registry/entities.jsonl                              90fd30dfe2b9d14e8caecc0f6f9b65c2281a91bca48db219f11e78221c73aab9
registry/edges.jsonl                                 0b792990e5cc0dc62c0daebeb63d9774729001ca747220042792ba72f5b055b6
registry/provenance.jsonl                            36ff55b27497618b632ec914d99fff9607cfcb903264dd84510f42b1403c14c2
artifacts/PC_SOURCE_SWITCH_OWNER_ADAPTER_MANIFEST.json b2cca41f1efed7399709e08dc953059660df123ccc1c6e9ccf3bdf4eadaf9844
```

## 7. Historical 24-edge recovery assessment

The identity/provenance contract carried a historical placeholder `NOT_YET_ASSESSED` for the known gap-internal 24 exact memberships pending adapter-materialization review.

Actual canonical provenance already contains:

- `docs/INLINE_GAP_INTERNAL_24_EDGE_PROVENANCE_RECOVERY.md`
  - blob `12fd5f8db9df8d96ad9599f619771fb711a1623a`
- `data/post_freeze/inline_gap_internal_24_edge_provenance_recovery_v1/MEMBERSHIP.json`
  - blob `5223f3eb6659a05d67230e5ce621d5a0beb0f025`
  - pair-list SHA-256 `133173ac874c64c9fda0fc40d020363e9fe2214ecba258e9602100f9432c3a5d`

Therefore the effective provenance status is:

```text
historical_artifact_edge_recovery = RECOVERABLE_FROM_SOURCE
exact membership recovered canonically = YES
selective registry import in this seed = NO
```

The canonical recovery contains 24 pair units. One recovered pair overlaps the already-materialized historical cross-boundary exact graph, so the recovery document records 23 additional reductions when composed with that graph. This stage does not recreate or import those relations.

This changes provenance status only. New Switch write authorization: **0**.

## 8. Coverage boundary

This seed does not claim:

- all 158 F1 static rows are registered;
- all 1,311 F1 accepted rows are registered;
- all 17,103 inline PC source records are registered;
- pointer/runtime T5K entities are registered;
- the full Switch owner graph is registered;
- 1:N or N:M corpus relations are newly observed;
- any selective candidate, applicability, realization, scope, or release decision exists.

The bounded seed exists to make the registry canonical before replay expansion. Future expansion must read the current registry and append IDs. It must never recompute, reuse, or renumber issued IDs.

## 9. Validation

Materialization validation:

```text
entity IDs unique                     PASS
edge IDs unique                       PASS
all edge endpoints exist              PASS
PC source entity count = 8            PASS
Switch owner entity count = 8         PASS
8 source -> 8 owner degree            PASS
candidate IDs issued = 0              PASS
candidate NOT_ISSUED preserved        PASS
registry next-sequence monotonic       PASS
field-level evidence retained          PASS
native locators separated from IDs     PASS
applicability/realization emitted = 0  PASS
release-scope decisions emitted = 0    PASS
particle-policy classifications = 0    PASS
TAI5MSG/EVENT adapter started = false PASS
builder/build started = false          PASS
```

## 10. Next boundary

Recommended next scope:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION
```

It should consume remaining READY canonical PC-source/Switch-owner evidence using this registry as input, append identities/edges without renumbering, and validate replay/freshness. It must remain separate from broad semantic/applicability/realization/release-scope classification and from TAI5MSG/EVENT/build implementation.

A fresh explicit user execution signal is required.
