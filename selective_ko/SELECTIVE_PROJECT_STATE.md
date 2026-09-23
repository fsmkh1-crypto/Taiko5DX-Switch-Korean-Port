# SELECTIVE PROJECT STATE

Date: 2026-09-23 (KST)
Status: V371 ACTIVE REQUEST PARTIAL / 54 OF 169 FILE REPLAY PASS / 80 OF 80 FINAL-RESPONSIBILITY UNITS OBSERVED / CANDIDATE NOT EMITTED
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`, branch `main`.
Repository-level authority: `../PROJECT_STATE.md`.
Current checkpoint: `EVENT_169_ACTIVE_REQUEST_PARTIAL_54_FILES_80_UNITS_CHECKPOINT_V371.md`.
Current artifact index: `artifacts/event_169_active_request_partial_54_v1/INDEX.json`.
Current failures: `artifacts/event_169_active_request_partial_54_v1/KNOWN_FAILURES.json`.
Implementation commit remains `59e12802f402ea06c3331c16b32c2cbb9216e900`.
Product authority remains `EVENT_169_APPLICABILITY_AND_OVERLAP_CANONICALIZATION_V369.md`.

## 2. Frozen product state

```text
source-owner universe                    66,987
INCLUDE_KO recipe coverage               52,491
role-aware structural fields             24,305
final write-responsibility units             80
candidate EVENT output                        0
runtime_hook_required                     false
product_milestone                  V369_UNCHANGED
```

No role/rule census or final-byte field discovery was reopened.

## 3. Partial active-request results

```text
actual Switch files replayed              54 / 169
file-local PASS                           54 / 54
remaining files                              115
owner identities observed                   45,669
recipe views observed                       35,913
field policies satisfied                    18,010
field writer / no-writer                    17,994 / 16
final-responsibility units observed             80 / 80
relation / support receipts                    130 / 5
late final fault discard probes                  80 / 80
obligations SAT / NOT_OBSERVED              3,163 / 2,105
```

All observed file assemblies had zero unassigned/multiply-assigned/conflicting bytes and FINAL_TABLE as last writer.
The 80/80 fault-probe result covers late final-responsibility corruption only; it is not full-product atomic acceptance.

## 4. Pending work

Legacy ECF overlays still to connect: direct-escape 350 rows, lexical 12 rows, derived/mixed 61 rows, non-particle suffix 3 rows.
The remaining 115 Switch inputs are not replayed. 21,318 owners, 16,578 recipe views and 6,295 field-policy rows remain unobserved in actual replay.
TAI5MSG 5 roots / 19 references, VAL01, IPS/package and runtime remain outside this partial checkpoint.

Source-identity provenance holds remain 60 with zero releases; eight held files matched prior observed byte identity in this scope.

## 5. Exact next scope

After a fresh explicit user execution signal, continue only:

`V371_ACTIVE_REQUEST_CONNECTION_AND_169_FILE_CANDIDATE_OFFLINE_VALIDATION`

Reuse the current adapter and frozen authorities. Connect existing legacy ECF evidence before the remaining 115-file replay; do not start another role/rule census.
