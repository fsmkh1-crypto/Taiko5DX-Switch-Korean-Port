# LEGACY EVIDENCE CLAIM-STRENGTH POLICY — V296

Date: 2026-09-17 (KST)
Status: CANONICAL CLAIM-STRENGTH / TRUST-BOUNDARY POLICY MATERIALIZED / DOCUMENTATION ONLY
Validation ID: `V296`
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `SELECTIVE_KO_LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296_MATERIALIZED`
Implementation authorization: NONE
Build authorization: NONE
New WRITE_SAFE authorization: 0
New INCLUDE_KO authorization: 0

## 1. Purpose

This policy records the trust boundary established by the post-failure audit of the historical full-port work.

The audit does **not** conclude that the historical binary analysis was broadly wrong. It concludes that several low-level facts were promoted too far into product-level/full-port conclusions.

Canonical distinction:

```text
low-level source/structure/runtime evidence may remain valid
!=
that evidence automatically authorizes selective Korean product inclusion
```

The failed full-port assembly therefore triggers **claim-strength correction**, not blanket revalidation of all prior VERIFIED facts.

## 2. Claim-strength classes

Historical evidence is interpreted under five classes.

### `TRUST_RETAIN_RAW_SOURCE`

Exact source facts remain reusable without revalidation unless contradictory evidence appears.

Examples:

- exact PC patch bytes, hashes, replacement bytes, Korean spellings and terminology;
- T5K population facts such as inline 17,103, Mapping 10,036 and Pointer 56;
- deterministic counts derived from exact source artifacts within their stated parser/scanner boundary.

### `TRUST_RETAIN_SCOPE_LIMITED`

A prior VERIFIED result remains valid only for the exact claim and route it proved. It may not be silently promoted to a broader claim.

Examples:

- TAI5MSG 33 blocks / 14,832 logical slots and 1:1 PC-original <-> PC-Korean locator lattice;
- Stage2 affine target resolution for 13,771 rows;
- F1 static-write authorization for the exact 158 rows;
- Mapping 10,036 forward/reverse round-trip on the tested Eden Android new-officer surname route;
- pointer companion `SUBSUMED` relations where the linked physical write remains unresolved;
- semantic-owner closures that explicitly did not grant WRITE_SAFE.

### `REAUDIT_ON_SELECTIVE_USE`

The historical fact may be reused as evidence, but any product-level interpretation must be re-audited when a selected R1/R2/R3 item actually depends on it.

Examples:

- whether a historical F1/Stage2/owner row belongs to the selective release corpus;
- whether a selected item requires a pointer redirect, runtime helper, formatter or other action family;
- whether a previously write-safe physical target should actually receive Korean in the selective product;
- whether historical grammar125 evidence is relevant to an optional R4 revisit.

### `SELECTIVE_PRODUCT_EXCLUDED`

The historical artifact remains provenance/diagnostic evidence but is not an implementation or release baseline for the selective product.

Examples:

- V289 historical integrated builder technique as a release baseline;
- V290 full-port integrated build as a selective baseline;
- V291 package as a selective baseline;
- bulk import of PC `data/` payload;
- whole-PC-Korean TAI5MSG reconstruction;
- historical heuristic/bulk inline selection as the release corpus.

### `WITHDRAWN_OR_REJECTED`

A claim contradicted by later evidence or built on wrong provenance must not be reused as proof.

Examples:

- exact PC v1.02 runtime parity claims derived from the wrong 18,479,304-byte PC executable;
- container/file name as usage/release class;
- long Korean text as automatic R1/UI description;
- F1 static 158 as R1 158;
- V290/V291 PASS as proof that gameplay/runtime was correct;
- symptom-local grammar patches such as global duplicate-syllable deletion or forced formatter predicate inversions.

## 3. Normative rules

### V296-R1 — Claim-strength ceiling

A downstream claim may never be stronger than the strongest evidence that directly supports it.

Examples:

```text
target resolved        != WRITE_SAFE
WRITE_SAFE             != INCLUDE_KO
source owner resolved  != release inclusion
build reproducible     != runtime correct
package byte-identical != hardware/gameplay validated
one-route runtime PASS != all-callers/all-platforms PASS
```

### V296-R2 — Product inclusion is an independent gate

Historical `WRITE_SAFE`, owner, counterpart, target or routing closure does not automatically create selective `INCLUDE_KO`.

Selective inclusion additionally requires the current product taxonomy, exact field/message/object role, applicable Switch structure/owner/caller evidence, risk/capacity/provenance closure and current product disposition.

### V296-R3 — Hardware/runtime evidence is route-scoped

A runtime observation applies only to the exact tested platform, route, payload and cause family.

The Mapping 10,036 Eden Android round-trip remains VERIFIED for the tested surname-input route. It does not by itself validate physical Switch execution, font/render behavior, every consumer, or every selected content route.

### V296-R4 — Build/package PASS semantics are non-gameplay by default

A build validation proves deterministic construction of its declared artifact. A package validation proves transport/identity of its declared payload.

Unless an explicit hardware execution result exists, neither may be cited as proof that the game displayed or composed the content correctly.

Therefore:

```text
V290 = historical build-reproducibility evidence
V291 = historical package/transport evidence
V290/V291 = NOT selective gameplay-success evidence
```

### V296-R5 — Exact PC runtime provenance is required for exact-runtime parity claims

PC runtime mechanics remain `REFERENCE_OR_HINT` unless the exact target executable/version and exact-family provenance are established.

The wrong-build PC disassembly may remain structural background only. It cannot prove exact v1.02 runtime parity.

### V296-R6 — No blanket revalidation

The failure of the historical product assembly is not a reason to redo every VERIFIED low-level fact.

Revalidation is required only when:

- later evidence directly contradicts the prior claim;
- the current selective use asks the evidence to support a stronger claim than it originally proved;
- the exact source/runtime identity required by the claim was never established;
- a new selected item crosses an owner/caller/storage boundary that the old proof did not cover.

### V296-R7 — Full-port assembly order is non-authoritative

Rejected historical sequence:

```text
bulk PC payload import
-> whole-container / broad inline realization
-> hardware breakage
-> symptom-by-symptom repair
```

Required selective sequence remains:

```text
exact field/message/object selection
-> source role/mechanism classification
-> Switch owner/caller/structure binding where required
-> capacity/risk/provenance closure
-> selective INCLUDE_KO authorization
-> implementation/build
-> cause-family runtime validation
```

## 4. Audited historical evidence disposition

### Retained without reopening original proof

- PC patch exact raw/source evidence and Korean content authority;
- Mapping 10,036 source obligation;
- TAI5MSG 33-block / 14,832-slot locator structure;
- Stage2 13,771 affine target-resolution facts, with no write/release escalation;
- F1 158 static-write provenance, with no R1/release escalation;
- Mapping 10,036 tested Eden round-trip, limited to the tested route;
- pointer/source/action structural relations within their original authorization boundary;
- prior rejected hypotheses and failure records.

### Re-audit only when a selected item depends on them

- semantic-owner overlays as product-role evidence;
- historical WRITE_SAFE 287 as a source of possible implementation actions;
- pointer replacement-pool realization;
- runtime helper/descriptor counterpart needs;
- grammar125/R4 formatter evidence;
- any historical full-port action whose current selected field/message/object and caller set have not been independently established.

### Excluded as selective baselines

- V289/V290/V291 product assembly path;
- PC data bulk-copy policy;
- whole-PC-Korean TAI5MSG product payload;
- historical broad inline-selection product policy;
- incremental subtraction/repair from V291.

## 5. Confirmed facts from the audit

- V290 explicitly validated an integrated build artifact and explicitly did **not** perform hardware validation.
- V291 explicitly validated package/transport identity and explicitly recorded hardware execution as not yet performed.
- V292 already excluded V290/V291 from the selective product baseline.
- V295 already recorded the bulk/file-level assembly-order failure and corrected container/usage overreach.
- Stage2 documentation itself states that structural target identity does not authorize every semantic write.
- F1 static-158 documentation proves physical write safety for the exact 158 rows but does not prove R1/product inclusion.
- Mapping 10,036 has a separate route-scoped runtime round-trip proof and therefore is not reopened merely because the historical full-port product failed.

## 6. Rejected hypotheses / do-not-repeat

Do not repeat:

- `full-port failed -> Mapping 10,036 must be redesigned`;
- `full-port failed -> F1 158 physical targets were necessarily wrong`;
- `full-port failed -> TAI5MSG 33/14,832 structure was necessarily wrong`;
- `WRITE_SAFE -> must translate`;
- `owner resolved -> must translate`;
- `build PASS -> gameplay PASS`;
- `package PASS -> hardware PASS`;
- `PC runtime helper exists -> same Switch helper/count/mechanism is required`;
- `V291 minus known bad pieces -> selective release`.

## 7. Impact range

V296 changes evidence interpretation and precedence only.

Unchanged:

- FZ001 frozen identities;
- all exact hashes and raw source artifacts;
- existing Mapping 10,036 route-scoped verification;
- F1 158 physical write-safety provenance;
- TAI5MSG structure artifact identities;
- V294 identity-in-prose policy;
- V295 source/container corrections;
- current candidate/classification/INCLUDE_KO counts;
- current executable inventory scope.

V296 creates:

```text
new candidate IDs      = 0
new classification IDs = 0
new WRITE_SAFE         = 0
new INCLUDE_KO         = 0
builder changes        = 0
gameplay-data changes  = 0
build/IPS artifacts    = 0
```

## 8. Next scope / STOP

The active selective inventory remains open and unchanged:

`SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY`

V296 is a trust-boundary policy overlay. It does not authorize implementation and does not itself resume the inventory after this materialization report.

A fresh explicit user execution signal is required for the next analysis stage.

## 9. Repository write boundary

Repository mutation for this materialization is restricted to:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API write, branch creation, force update, build, or gameplay mutation is authorized.