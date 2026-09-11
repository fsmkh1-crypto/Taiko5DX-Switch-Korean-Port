# VALIDATION_LEDGER — PC DLL PHASE 4

Date: 2026-09-11

Fixed inputs:

- embedded `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- exact target EXE identity known, but exact EXE unavailable for whole-program XREF/UI naming
- PHASE 1–3 canonical findings reused without revalidation

Method: PHASE 4 DLL/T5K static analysis handoff covering helper control flow, descriptor search/application, generated patch formulas and whole 11/14 fixed-resource census. The handoff reports a raw-byte restricted interpreter that exercised 65,536 mapper inputs and 65,536 byte combinations. It was not an in-game runtime execution test.

Transfer provenance: the original handoff also listed `docs/PC_RUNTIME_PHASE4_VERIFICATION.json`, `tools/pc_phase4_probe.py`, and a ZIP with detailed raw signature/mask/preimage/payload evidence. Those auxiliary files were not available during canonical repository import and were not recreated. The claims below preserve the reported results; exact raw-byte reproduction may be revalidated later only if a high-risk implementation decision requires evidence absent from the imported detail record.

| ID | Claim | Status | Evidence / scope |
|---|---|---|---|
| V052 | The 158-byte helper has two descriptor-used logical entries at `+0x00` and `+0x20`; the handoff counts 42 reachable instructions plus 4 bytes of unreachable alignment/padding. | VERIFIED | `docs/PC_RUNTIME_PHASE4_HELPER_DESCRIPTOR_SPEC.md` §§5–7. |
| V053 | Helper `+0x00` handles Korean page mapping: lead `0xEB..0xF8` maps to pages `49..62` in `EAX` and returns; nonmatching input reproduces displaced original setup and jumps to EXE RVA `0x6933D5`. | VERIFIED | PHASE 4 spec §6. Exact containing function/UI name remains out of claim. |
| V054 | Helper `+0x20` is a copy-and-control-flow hook, not a Boolean validator: it directly handles accepted 1/2-byte ranges then jumps to EXE RVA `0x6832BC`; fallback reproduces displaced original operations and jumps to `0x68328A` rather than immediately rejecting input. | VERIFIED | PHASE 4 spec §7. |
| V055 | The helper contains four control-transfer addresses that are fixed up after runtime allocation so jumps return to the correct target-EXE continuations. Exact helper-byte fixup offsets were in the original handoff artifact but are not reproduced in the canonical import. | VERIFIED | PHASE 4 handoff + spec §§5,15. Narrow claim is count/role, not missing raw offsets. |
| V056 | Descriptor search scans target `.text`; mask byte `0` ignores that byte and nonzero compares the full signature byte. Success requires exactly one match **and** exact agreement with the declared anchor. Zero, multiple, or uniquely relocated matches fail. | VERIFIED | PHASE 4 spec §3. |
| V057 | Subpatch generation is: kind0=`payload`; kind1=`i32(P-W-4)`; kind2=`i32(P-M)`; kind3=`E9 || i32(H+arg-W-5)`. Kinds 1/2 do not use `arg`; kind3 uses `arg` as helper-entry offset. | VERIFIED | PHASE 4 spec §4. |
| V058 | The fixed package contains 11 descriptors / 14 subpatches with kind counts 9/2/1/2. Although 14 is not a parser hard denominator (PHASE 2), PHASE 4 establishes a separate staging-time fixed-package check for total 14. | VERIFIED | PHASE 4 spec §§3,8. |
| V059 | All 14 successful write RVAs are accounted for: `0x137A6A`, `0x137CEA`, `0x137EBF`, `0x13CBED`, `0x3EE13E`, `0x3EE1A5`, `0x66296C`, `0x662980`, `0x662B6E`, `0x662B7F`, `0x662B90`, `0x683285`, `0x693148`, `0x6933D0`, matching descriptor census and kind population. | VERIFIED | PHASE 4 spec §8. |
| V060 | `runtime_byte_validation` kind3 targets helper `+0x20`; `runtime_page_mapper` kind3 targets helper `+0x00`; `font_page_limit` raw behavior is compare threshold `0xFF -> 0xA0`, not a proven literal font-page-count assignment. | VERIFIED | PHASE 4 spec §§6–10. |
| V061 | PHASE 4 closes the DLL-generated runtime-code semantics but not whole-program EXE context: exact caller/XREF graph, exact screen/UI meaning, and actual target-process runtime success remain unresolved without the exact EXE/runtime test. | VERIFIED | Scope boundary, PHASE 4 spec §§13,16. |

Rejected/corrected in PHASE 4:

- a unique descriptor signature found at a different address is acceptable;
- helper `+0x20` is a Boolean-return validator;
- fallback is immediate invalid-input rejection;
- kind1/kind2 use `arg` in address generation;
- helper padding is reachable logic;
- `font_page_limit` is directly proven to be a literal font-page-count edit.

Next stage: PC Runtime Canonical Closure only after a fresh user execution signal. No Switch counterpart analysis, ARM64, IPS or build work is authorized by this ledger entry.
