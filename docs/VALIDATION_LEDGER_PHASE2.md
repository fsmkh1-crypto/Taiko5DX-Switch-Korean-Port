# VALIDATION_LEDGER — PC DLL PHASE 2

Date: 2026-09-11
Inputs:

- embedded DLL SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- parser authority: DLL RVA `0x2640`

Method: static x86-64 parser reconstruction plus exact-consumption parse of the fixed RCDATA. Mapping/pointer/helper/descriptor runtime semantics were deliberately excluded.

| ID | Claim | Status | Evidence / reuse rule |
|---|---|---|---|
| V040 | T5K header is exactly `0x48` bytes: magic[8], version u32, inline/pointer/descriptor counts u32, prefix_len u32, helper_len u32, target EXE size **u64**, SHA-256[32]. Parser hard-denominators are version=1, counts=17103/56/11, prefix=`0x9F2A`, helper=`0x9E`; target size/hash are preserved for later identity validation, not hard-coded by the parser. There is no mapping-count header field. | VERIFIED | Parser `0x26E5..0x2764`; PHASE 2 spec §§2–3. |
| V041 | Top-level parse order is header -> prefix -> helper -> 17,103 inline -> 56 pointer -> 11 descriptors, with fixed-resource boundaries `0x48/0x9F72/0xA010/0x951C0/0x95540/0x95D35`. Cursor must equal resource end after descriptor 11; trailing data is rejected. | VERIFIED | Parser `0x2777..0x3025`; exact fixed-resource reparse; PHASE 2 spec §3. |
| V042 | Inline wire record is `u32 pc_rva, u32 length, original[length], replacement[length]`; pointer wire record is `u32 slot_rva, u32 original_target_rva, u8 mode, reserved[3], u32 arg`. Parser enforces nonzero inline length, bounds, and `mode<=1`. Current pointer population is 51 mode1 / 5 mode0. | VERIFIED | Inline parser `0x2870..0x290E`; pointer parser `0x29E0..0x2A75`; PHASE 2 spec §§4–5. |
| V043 | Descriptor header is four u32 fields `(anchor_rva, signature_len, patch_count, name_len)` followed by length-delimited name/signature/mask and variable subpatches. Subpatch header is `offset u32, preimage_len u32, kind u8, reserved[3], arg u32, payload_len u32`; parser enforces signature/name/count bounds, `kind<=3`, in-signature preimage bounds, kind0 payload length equality, and zero payload for kinds1..3. Current 14 subpatches are an observed population, not a parser denominator. | VERIFIED | Descriptor parser `0x2BA4..0x2C5F`; subpatch parser `0x2D90..0x2E84`; PHASE 2 spec §6. |
| V044 | Parsed recipe is typed/span-based rather than a second full blob copy: raw `0x48` header, zero-copy prefix/helper and payload spans, vectors for inline/pointer/descriptors. Observed recipe object is `0xB0`, inline entry `0x28`, descriptor entry `0x60`, subpatch entry `0x30`. Explicit validation failure returns false and init does not proceed to disk identity/staging/commit. | VERIFIED | Parsed layout around output object `+0x48..+0xA8`; caller failure at `0x7A5E`; PHASE 2 spec §§7–8. |
| V045 | Current `builder/t5k.py` is not canonical PC wire-format authority: it reads EXE size as u32, hard-checks target size during parse, does not reproduce exact prefix/helper denominators, folds pointer mode/reserved into u32, and treats descriptors as residual substring data. `mapping_lookup_1A/2A` are cross-boundary substring false positives; actual names are `mapping_lookup_1/2`, followed by signature byte `0x41 ('A')`. Existing fixed-blob count/mapping uses remain valid where separately established. | VERIFIED | Direct source audit against DLL parser grammar; PHASE 2 spec §9. No builder source changed in PHASE 2. |

Rejected in PHASE 2: mapping-count header field; parser-hardcoded target size/hash approval; pointer mode as full u32 wire field; NUL/substr descriptor grammar; trailing-data tolerance; parser hard-denominator of 14 subpatches.

Deferred: prefix mapping/string-pool runtime meaning, pointer mode/arg runtime semantics, helper code semantics, descriptor kind/arg runtime semantics, signature-mask staging semantics. These are PHASE 3/4 topics and are not revalidation triggers for V040–V045.
