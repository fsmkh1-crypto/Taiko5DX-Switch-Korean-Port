# TAIKO5DX — Final Product Canonical Reproduction Git Adoption

Date: 2026-09-26 KST
Scope: `FINAL_PRODUCT_CANONICAL_REPRODUCTION_GIT_ADOPTION`
Parent canonical HEAD: `0d3b90b92da069c928a4539c319b43383dfb123f`

## Result target

Adopt the already verified final-product builder and frozen plans without changing the historical 15,460-record builder.

Canonical expected payloads:

- RootCause223 intermediate TAI: `8c9a70575258fad362c0197c8b59190fd332843195f35e185894ee34fe6547b1`
- final B23 TAI: `1b44170a817e047ba942ba10e46571049ff7405c7fac4278c3e1598089efd61e`
- corrected IPS: `28c423a0a8e805308f8e935f2a3f5304fe12e3f948ca6468c46dd72a96cdcfae`

The user-observed runtime-pass reference ZIP remains an immutable large artifact, SHA-256 `cfd14031bab300929a9926bae9bb82bf28f21a9d417aee50ca527b88df873c91`, Drive ID `1yCgjdWKQUTpwEfLll_Y29ztKG96EkXv2`.

## Adopted source set

- additive `builder/final_product_candidate.py`
- `tests/final_product_repro_check.py`
- frozen 430-caller / 1,321-helper plan
- B23 617-row reflow manifest
- coordinate-typed Buffer8 IPS V2 plan
- carrier/package-layout manifests
- final reproducibility verification and failure authority
- repository and selective resume-state updates

Python bytecode caches are intentionally excluded.

## State transition

Historical V371 evidence is retained but is no longer the active next scope for the current product. Its 115 unreplayed EVENT files remain historical partial work and are not claimed complete.

The defective Buffer8 IPS SHA `dadb49f92fd66313145620194b05c108373f780f566bd5ba433f045e8acef7ec` is explicitly `DO_NOT_USE`.

No current-product implementation blocker remains after adoption. Metadata-corrected release repackaging is optional and requires its own runtime retest; the known-working runtime reference must not be overwritten.

## Git write invariant

This adoption is authorized only through:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No contents-API write, branch creation, deletion API, update-file API, or force update is authorized.
