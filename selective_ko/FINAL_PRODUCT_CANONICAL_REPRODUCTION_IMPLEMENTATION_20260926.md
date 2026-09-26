# TAIKO5DX — Final Product Canonical Reproduction Implementation

Date: 2026-09-26 KST  
Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`  
Branch: `main`  
Verified HEAD: `0d3b90b92da069c928a4539c319b43383dfb123f`

## Result

`PASS / FINAL TAI + CORRECTED IPS REPRODUCIBLE / RUNTIME-PASS PAYLOAD BYTE-EXACT / GIT NOT WRITTEN`

## Confirmed facts

A new additive final-product builder was implemented without modifying the historical
`builder/product_lowering_candidate.py` path. It starts only from the Diagnostic218 TAI,
the Diagnostic218 five-record IPS, the Switch 1.1.3 NSO `main`, and frozen plans.
It does not consume the final TAI or runtime-pass ZIP as a build input.

Pipeline:

`Diagnostic218 (14,832) -> frozen 430 caller / 1,321 helper plan -> RootCause223 (16,153) -> B23 617-row reflow -> final TAI`

Exact identities:

- RootCause223 pre-B23 TAI: `8c9a70575258fad362c0197c8b59190fd332843195f35e185894ee34fe6547b1`
- final B23 TAI: `1b44170a817e047ba942ba10e46571049ff7405c7fac4278c3e1598089efd61e`
- corrected IPS: `28c423a0a8e805308f8e935f2a3f5304fe12e3f948ca6468c46dd72a96cdcfae`

TAI independent readback: `16,153 / 16,153` for both the pre-B23 and final stages.

B23 stage:

- 617 rows
- 462 reflow / 155 preserve
- 1,844 whitespace-byte edits
- 1,179 SPACE->LF / 665 LF->SPACE
- other byte changes 0
- target overflow >32 units 0

Buffer8 IPS:

- `main` SHA is guarded before use.
- NSO text/rodata/data segments are actually decompressed with LZ4.
- virtual mapped zero-fill between rodata and data is represented explicitly.
- 12 RELA preimages plus the 96-byte zero pool preimage are checked: 13/13 PASS.
- every Buffer8 plan row is typed `MAPPED_NSO`; emission is only through `emitted = mapped + 0x100`.
- rejected boot-freeze SHA `dadb49f92fd66313145620194b05c108373f780f566bd5ba433f045e8acef7ec` is not emitted.

Reproducibility:

- two independent clean output directories: byte-exact TAI and IPS
- final TAI equals the user-observed runtime-pass ZIP payload byte-for-byte
- final IPS equals the same runtime-pass ZIP payload byte-for-byte
- EVENT 13 + FONT 1 carrier files: 14/14 byte-exact against the runtime-pass ZIP

Fail-closed tests:

1. one-byte-modified Diagnostic218 TAI -> `BASE_TAI_IDENTITY` failure
2. one-byte-modified Switch main -> `MAIN_IDENTITY` failure
3. one-byte-modified frozen caller plan with unchanged INDEX -> `PLAN_INDEX` failure

## Leading hypothesis

None is required for the working product. The remaining work is repository adoption and state canonicalization, not a new game-data root-cause investigation.

## Unconfirmed items

- The new builder has not yet been committed to Git.
- Root `PROJECT_STATE.md` and `selective_ko/SELECTIVE_PROJECT_STATE.md` still describe the older V371/product-lowering state.
- A newly regenerated install ZIP with corrected final metadata has not been runtime-tested; the known-working runtime reference remains immutable.

## Rejected hypotheses / failed approaches

- Use the final TAI itself as the builder baseline: rejected.
- Change the historical 15,460-record builder in place: rejected; historical reproducibility is preserved.
- Keep a generic Buffer8 `offset` field mixing mapped and emitted coordinates: rejected.
- Accept classic-IPS container readback as proof of correct mapped NSO targets: rejected.
- Reuse the `dadb49f9...` boot-freeze IPS: rejected.
- Require V371 remaining replay completion before current-product canonicalization: rejected for the current runtime-pass product path.

## Related impact range

Implementation files in this packet:

- `builder/final_product_candidate.py`
- `tests/final_product_repro_check.py`
- `selective_ko/final_product_v1/*` frozen plans

No EVENT, FONT, historical builder, repository state file, Git object, install ZIP, or runtime environment was modified in this stage.

## Modification proposal

Next separately authorized scope: `FINAL_PRODUCT_CANONICAL_REPRODUCTION_GIT_ADOPTION`.

Before any write, re-check remote main is still `0d3b90b9...`. Git writes are restricted to exactly:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

The adoption commit should add this new builder/test/plan path, update repository resume authorities, mark the defective IPS as DO NOT USE, and mark V371 partial EVENT work as historical / not promoted / superseded for the current product.

STOP.
