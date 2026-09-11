# VALIDATION LEDGER — PCREF1 delivery verification

Date: 2026-09-11
Scope: historical PCREF1 emitted-IPS provenance only

## V062 — PCREF1 emitted-delivery integrity is not established

**Claim:** The historical `PCREF1` runtime no-change result cannot be used as negative evidence against the repeated/fixed-object mappings because the actual emitted PCREF1 IPS artifact and its delivery provenance are not retained.

**Status:** `NEEDS-REVERIFY`

**Evidence:**

- no PCREF1 ZIP/IPS, artifact SHA-256, record count, guard report, manifest, or reproducible PCREF1 builder is present in the canonical repository evidence available to this session;
- Google Drive project folders `Eden_Builds/` and `Test_Results/` are empty, and Drive search returned no PCREF1 artifact;
- File Library search returned no PCREF1 artifact;
- the surviving description reconstructs intended PCREF1 scope only, not actual emitted records;
- V014 still establishes the Eden `mapped + 0x100` coordinate rule;
- V024/V025/V033 still establish the relevant Switch object/fixed-field locations independently of PCREF1.

**What is not verified:**

- actual IPS record presence;
- actual emitted coordinates;
- payload bytes;
- guard skips;
- record count;
- EOF/serialization behavior;
- identity of the package actually runtime-tested.

**Reuse rule:**

- retain the PCREF1 screen-no-change report only as a historical runtime observation;
- do not use it to invalidate V024/V025/V033 or to conclude the game does not read those objects;
- before interpreting any new counterpart-derived runtime no-change result causally, use a separately authorized reproducible delivery-control diagnostic with retained manifest, SHA-256, guard report, and emitted-IPS round-trip evidence;
- a new delivery-control artifact validates the current pipeline only; it cannot retroactively prove the lost PCREF1 artifact.

Detailed report: `docs/PCREF1_DELIVERY_VERIFICATION.md`.
