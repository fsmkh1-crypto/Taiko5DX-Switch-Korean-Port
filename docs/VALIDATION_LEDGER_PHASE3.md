# VALIDATION_LEDGER — PC DLL PHASE 3

Date: 2026-09-11
Inputs:

- embedded DLL SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- PHASE 1/2 canonical records reused without revalidation
- exact target EXE identity known, but exact target EXE unavailable for whole-program XREF naming

Method: DLL/T5K runtime-application analysis constrained to mapping relocation and pointer-record semantics. Helper and generic runtime-descriptor semantics were excluded.

| ID | Claim | Status | Evidence / reuse rule |
|---|---|---|---|
| V046 | The `0x9F2A` prefix is runtime data copied into private storage and semantically splits into 10,036 x 4-byte mapping entries (`0x9CD0` bytes) followed by a 602-byte (`0x25A`) pointer replacement pool. Mapping is not builder-only metadata. | VERIFIED | `docs/PC_RUNTIME_PHASE3_MAPPING_POINTER_SPEC.md` §§2,8. |
| V047 | Mapping lookup relocation changes five operands across two lookup paths: three table/address references are redirected to relocated private mapping storage and two count limits change `0x1D46` (7,494) -> `0x2734` (10,036). | VERIFIED | PHASE 3 spec §3. Exact whole-program caller naming remains outside this claim. |
| V048 | All 56 pointer records use an 8-byte absolute-pointer staging write. Runtime destination calculation is mode-dependent: mode 0 = `EXE/module base + arg`; mode 1 = `private prefix base + arg`. This semantic applies to the PHASE-2 canonical wire grammar (`u8 mode + reserved[3] + u32 arg`). | VERIFIED | Full 56-record engine survey; PHASE 3 spec §4. |
| V049 | Pointer population is mode0=5 and mode1=51. The five mode-0 records converge on two module-resident targets that are translated by the inline layer. The 51 mode-1 records reference 47 distinct replacement strings in private-prefix storage. | VERIFIED | Whole-population classification; PHASE 3 spec §§5–6. |
| V050 | Mapping relocation and pointer-record application are separate engines sharing the private prefix allocation. The 56 pointer records do not themselves relocate the 10,036-entry mapping table. | VERIFIED | Integrated data-flow analysis; PHASE 3 spec §7. |
| V051 | Without the exact target PC EXE, complete XREF/caller/table naming and per-pointer screen/UI roles remain unassigned; this does not invalidate the established storage, base-selection, count, and pointer-write semantics. | VERIFIED-SCOPE | PHASE 3 spec §§9–10. Do not use the mismatched supplied PC EXE for those names. |

Rejected/corrected in PHASE 3:

- mapping 10,036 as builder-only data;
- pointer 56 as the mechanism that directly relocates the mapping table;
- treating a search/signature anchor as an actual runtime EXE address without application context;
- applying runtime semantics to the obsolete `<IIII>` pointer interpretation instead of the PHASE-2 canonical grammar.

Deferred to PHASE 4: 158-byte helper machine-code semantics, runtime-descriptor kind/arg semantics, generic descriptor application semantics, and any Switch counterpart/ARM64/IPS/build work.
