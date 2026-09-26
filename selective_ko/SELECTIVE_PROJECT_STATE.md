# SELECTIVE PROJECT STATE

Date: 2026-09-26 (KST)
Status: `FINAL PRODUCT V1 CANONICAL REPRODUCTION / USER RUNTIME OBSERVED PASS`
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository-level authority: `../PROJECT_STATE.md`.

Current executable authorities:

- builder: `../builder/final_product_candidate.py`
- frozen plans: `final_product_v1/INDEX.json`
- reproducibility verification: `final_product_v1/FINAL_PRODUCT_REPRO_VERIFICATION.json`
- current known failures: `final_product_v1/KNOWN_FAILURES.json`
- implementation report: `FINAL_PRODUCT_CANONICAL_REPRODUCTION_IMPLEMENTATION_20260926.md`

Do not resume from the historical V371 54/169 checkpoint unless the user explicitly opens that historical EVENT scope.

## 2. Active payload

```text
RootCause223 pre-B23 TAI   8c9a70575258fad362c0197c8b59190fd332843195f35e185894ee34fe6547b1
Final B23 TAI              1b44170a817e047ba942ba10e46571049ff7405c7fac4278c3e1598089efd61e
Corrected IPS               28c423a0a8e805308f8e935f2a3f5304fe12e3f948ca6468c46dd72a96cdcfae
Final records               16,153
EVENT carrier               13 files, preserved
FONT carrier                1 file, preserved
Runtime reference ZIP       cfd14031bab300929a9926bae9bb82bf28f21a9d417aee50ca527b88df873c91
```

Runtime reference Google Drive ID: `1yCgjdWKQUTpwEfLll_Y29ztKG96EkXv2`.

Observed runtime result: Korean loading restored and B23 card descriptions reported normal in the tested user scope.

## 3. Reproducibility closure

The additive final builder leaves the historical 15,460-record product-lowering builder untouched.

Verified from fresh inputs:

- Diagnostic218 -> RootCause223 TAI SHA exact
- RootCause223 -> B23 final TAI SHA exact
- exact Switch NSO mapped preimages 13/13 before Buffer8 IPS emission
- final IPS SHA exact
- independent TAI readback 16,153/16,153
- two clean builds byte-exact
- builder TAI/IPS equal the user-observed runtime-pass ZIP payloads
- carrier EVENT/FONT 14/14 byte-exact
- negative identity/tamper tests 3/3 fail closed

## 4. Historical V371

V371 EVENT is retained as historical partial work:

```text
actual replay 54 / 169
remaining     115
promotion     NO
current product blocker NO
```

Disposition: `HISTORICAL_NOT_PROMOTED_SUPERSEDED_FOR_CURRENT_PRODUCT`.

This does not claim V371 completion and does not delete its evidence.

## 5. Do-not-repeat

- Never accept IPS `dadb49f92fd66313145620194b05c108373f780f566bd5ba433f045e8acef7ec`.
- Buffer8 plan coordinates must remain typed `mapped_offset` and `emitted_offset`; `emitted = mapped + 0x100`.
- IPS readback alone is not target proof; the exact Switch `main` mapped preimages must pass.
- Do not rename the known-working mod root and assume activation is preserved.
- Do not overwrite the immutable runtime-pass reference merely to correct its stale metadata.
- Do not reopen B24, RootCause223, the 699/196 language contracts, or V366-V369 merely because this is a new session.

## 6. Next scope

For the current tested product: **none required**.

Optional after a fresh explicit user signal only:

`CANONICAL_RELEASE_METADATA_REFRESH_AND_RUNTIME_RETEST`

Git writes must use only `create_blob -> create_tree -> create_commit -> update_ref(force=false)`.
