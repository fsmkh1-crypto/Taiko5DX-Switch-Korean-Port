# PC DLL PHASE 4 — helper and runtime-descriptor semantics

Date: 2026-09-11
Status: COMPLETE / STOP

## 1. Scope and provenance

This phase closes the remaining PC runtime-code layer for the Windows Korean patch `dinput8.dll`:

1. the 158-byte runtime helper; and
2. runtime-descriptor application semantics for all 11 descriptors / 14 subpatches.

It does not analyze Switch counterparts, ARM64, code/data caves, IPS, builds, or runtime behavior on Switch.

Canonical prior facts from PHASE 1–3 are reused without revalidation.

Fixed input identity:

- embedded `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- exact target EXE identity: Steam 1.2.1.0 build 9163702, 18,685,960 bytes, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`

The exact target EXE was not available for whole-program XREF/caller/UI naming. The helper and descriptor generation semantics are established from the DLL/T5K analysis handoff.

### Transfer note

The PHASE 4 handoff reported these auxiliary artifacts:

- `docs/PC_RUNTIME_PHASE4_VERIFICATION.json`
- `tools/pc_phase4_probe.py`
- a handoff ZIP containing the detailed raw signature/mask/preimage/payload evidence

Those raw files were not available to the canonicalizing agent at repository-import time. They are therefore **not fabricated or committed here**. This document imports the completed PHASE 4 findings and their stated verification method. If a later high-risk implementation decision requires exact raw signature/preimage bytes that are not reproduced below, validation rule 3 permits targeted revalidation or transfer of the original handoff artifact.

## 2. Executive result

PHASE 4 establishes:

- two logical helper entry points;
- 42 reachable helper instructions plus 4 bytes of unreachable alignment/padding;
- four helper return-address fixups;
- descriptor search across `.text` with unique-match and exact-anchor requirements;
- mask semantics: `0x00` = ignore byte, nonzero = compare the full byte;
- all four subpatch kinds and their byte-generation formulas;
- a staging-time invariant requiring the fixed resource to generate exactly 14 subpatches;
- all 11 descriptors / 14 subpatches and their successful write RVAs;
- the exact helper-entry routing for the two kind-3 hooks.

## 3. Descriptor search/application engine

The descriptor engine searches the target EXE `.text` region for each descriptor signature.

A descriptor succeeds only when:

1. the masked signature has exactly one match in `.text`; and
2. the resulting match address equals the descriptor's declared `anchor_rva` expectation.

Therefore a unique signature found at a different address is **not** accepted as relocation-tolerant success.

Mask semantics are byte-granular, not bit-granular:

```text
mask[i] == 0x00  -> ignore signature byte i
mask[i] != 0x00  -> compare the complete byte signature[i]
```

The successful write address is derived from the matched descriptor base plus each subpatch offset. The search anchor, signature match address, subpatch offset, and actual write address must not be collapsed into one concept.

Zero matches, multiple matches, or a unique match at the wrong anchor cause descriptor application failure and propagate through the PHASE-1 fail-closed staging path.

The fixed resource has 11 descriptors containing 14 subpatches. PHASE 2 established that 14 is not a parser-level hard denominator. PHASE 4 establishes that the runtime staging logic separately checks the resulting fixed-package total and requires 14 for this package.

Descriptor-generated writes are staged as the code-patch class and commit at PHASE-1 priority 2.

## 4. Subpatch generation semantics

Let:

```text
M = target EXE/module base
P = relocated private prefix base
H = runtime helper base
W = actual write address
```

The four kinds are:

### kind 0 — literal payload

```text
replacement = payload
arg         = unused
write size  = payload_len (= preimage_len, parser-enforced)
```

### kind 1 — RIP-relative relocated-prefix displacement

A four-byte displacement is generated so an x86-64 RIP-relative operand resolves to `P`:

```text
disp32 = P - W - 4
replacement = little_endian_i32(disp32)
arg = unused
```

### kind 2 — module-base-relative relocated-prefix displacement

A four-byte module-relative value is generated:

```text
value32 = P - M
replacement = little_endian_i32(value32)
arg = unused
```

### kind 3 — five-byte relative JMP to helper

The generated patch is:

```text
E9 <disp32>

disp32 = (H + arg) - W - 5
```

Here `arg` is the helper entry offset. In the fixed resource the two kind-3 patches target helper `+0x20` and helper `+0x00` respectively.

This corrects the earlier possibility that kinds 1/2 also add `arg` into their address calculation: they do not.

## 5. Runtime helper overview

The helper is 158 bytes (`0x9E`) and contains two logical entry points used by descriptors:

```text
helper +0x00
helper +0x20
```

The handoff counted 42 reachable instructions and 4 trailing/alignment bytes that are not part of a reachable instruction path.

The helper has four embedded control-transfer locations that are fixed up after allocation so fallback/success paths return to the correct target-EXE addresses. The exact four helper-byte offsets were present in the original PHASE 4 handoff artifacts but were not available during this canonical import; the semantic targets below are preserved.

The helper is not a standalone Boolean predicate API. Both entries are injected control-flow continuations/trampolines that either handle the Korean-specific case directly or reproduce displaced original behavior and jump back into the PC EXE.

## 6. Helper entry `+0x00` — runtime page mapper

Referenced by:

- descriptor `runtime_page_mapper`
- kind 3 subpatch at write RVA `0x6933D0`

Input/behavior:

- examines the upper byte/code-page component supplied through the original path (reported through the `ECX`-derived value);
- when the lead byte is `0xEB..0xF8`, returns Korean font-page indices `49..62` in `EAX`;
- otherwise reproduces the displaced original `RBX`-save/setup instruction and jumps to target EXE RVA `0x6933D5`.

Logical Korean-specific mapping:

```text
lead = code >> 8
if 0xEB <= lead <= 0xF8:
    EAX = (lead - 0xEB) + 49
    RET
else:
    reproduce displaced original operation
    JMP EXE RVA 0x6933D5
```

Important correction: the helper is not simply a global font-page-count function. Its directly established behavior is a lead-byte-to-page mapping hook plus fallback to the original EXE path.

## 7. Helper entry `+0x20` — byte-validation/copy hook

Referenced by:

- descriptor `runtime_byte_validation`
- kind 3 subpatch at write RVA `0x683285`

Inputs reported by the PHASE 4 analysis:

- current byte in `CL`;
- next-input location through `RBX`;
- output destination through `RDI`.

Behavior:

- accepted one-byte and two-byte ranges are copied/emitted directly;
- successful helper-handled cases jump to EXE RVA `0x6832BC`;
- non-helper cases do **not** return Boolean false and do **not** immediately reject input;
- instead the helper reproduces the displaced original `LEA/CMP` behavior and jumps back to EXE RVA `0x68328A`, allowing the original EXE path to continue.

The directly handled ranges are consistent with the previously observed Korean-patch behavior:

```text
single byte: 0xA1..0xDF

two-byte lead:
  0x81..0x9F
  0xE0..0xFC

trail:
  0x40..0x7E
  0x80..0xFC
```

The important PHASE 4 correction is control-flow semantics: this entry is a copy-and-jump hook with an original-path fallback, not a Boolean validator function.

## 8. Descriptor/subpatch census

Successful target write RVAs from the PHASE 4 handoff:

| Descriptor | Subpatch | Kind | Write RVA | Established raw change |
|---|---:|---:|---:|---|
| `ui_width_1` | 0 | 0 | `0x137A6A` | `R9D` immediate `170 -> 200` |
| `ui_width_2` | 0 | 0 | `0x137CEA` | `R9D` immediate `170 -> 200` |
| `ui_width_3` | 0 | 0 | `0x137EBF` | `R9D` immediate `170 -> 200` |
| `ui_width_4` | 0 | 0 | `0x13CBED` | `R9D` immediate `150 -> 200` |
| `description_font_1` | 0 | 0 | `0x3EE13E` | stack argument `5 -> 4` |
| `description_font_2` | 0 | 0 | `0x3EE1A5` | stack argument `5 -> 4` |
| `mapping_lookup_1` | 0 | 1 | `0x66296C` | RIP-relative displacement targeting `P` |
| `mapping_lookup_1` | 1 | 0 | `0x662980` | mapping limit `7,494 -> 10,036` |
| `mapping_lookup_2` | 0 | 1 | `0x662B6E` | RIP-relative displacement targeting `P` |
| `mapping_lookup_2` | 1 | 0 | `0x662B7F` | mapping limit `7,494 -> 10,036` |
| `mapping_lookup_2` | 2 | 2 | `0x662B90` | module-relative displacement targeting `P` |
| `runtime_byte_validation` | 0 | 3 | `0x683285` | `JMP helper+0x20` |
| `font_page_limit` | 0 | 0 | `0x693148` | compare threshold `255 -> 160` (`0xFF -> 0xA0`) |
| `runtime_page_mapper` | 0 | 3 | `0x6933D0` | `JMP helper+0x00` |

Count check:

```text
descriptors = 11
subpatches  = 14
kind 0      = 9
kind 1      = 2
kind 2      = 1
kind 3      = 2
```

This matches the PHASE-2 fixed-resource population.

## 9. Raw behavior vs semantic names

The following raw byte effects are VERIFIED at the PHASE 4 level:

- four immediate changes `170/150 -> 200`;
- two stack-argument changes `5 -> 4`;
- three mapping-address generation patches;
- two mapping-count changes `7,494 -> 10,036`;
- one compare-threshold change `255 -> 160`;
- two helper JMPs.

Names such as `ui_width_*` and `description_font_*` are useful descriptor labels, but without the exact target EXE whole-program context their complete screen/UI semantics, measurement units, and exact font-role naming remain inferential.

Likewise `font_page_limit` must not be documented as a proven literal page-count setter. The raw confirmed change is a compare threshold `0xFF -> 0xA0`; its broader display meaning belongs to the later PC-runtime closure / Switch counterpart analysis.

## 10. Audit of earlier `PC_RUNTIME_DLL_SPEC.md` claims

### CONFIRMED

- kind 0 is literal payload replacement;
- kind 1 generates a RIP-relative reference to relocated mapping/prefix storage;
- kind 2 generates a module-base-relative relocated-prefix reference;
- kind 3 generates a five-byte relative JMP to a helper entry;
- helper entry offsets `+0x00` and `+0x20`;
- `EB..F8 -> pages 49..62` at the page-mapper entry;
- the mapping descriptor family changes relocated table references and `7,494 -> 10,036` limits.

### PARTIALLY CONFIRMED

- the `runtime_byte_validation` label: accepted ranges are directly handled, but the helper is not a Boolean validator;
- `ui_width_*` and `description_font_*` human-readable roles: raw immediate/argument changes are established, exact screen/function roles are not;
- the display meaning attached to the `0xFF -> 0xA0` comparison: raw threshold change is established, a literal page-count interpretation is not.

### CORRECTED

- helper fallback/return semantics: helper paths either `RET` for the direct page-map result or jump back into specific original EXE continuations; fallback is not generic failure;
- byte-validation fallback: non-helper input returns to the original processing path at `0x68328A` rather than being immediately rejected.

### REJECTED

- interpreting `font_page_limit` as a directly proven literal font-page-count change;
- accepting a unique descriptor signature found at a relocated/different address: the required anchor must also match.

## 11. Confirmed facts

- The helper has two logical entry points used by descriptors: `+0x00` and `+0x20`.
- The fixed helper has 42 reachable instructions and 4 bytes of unreachable alignment/padding.
- Four helper control-transfer addresses require runtime fixup after helper allocation.
- Descriptor search covers target `.text` and requires both uniqueness and exact anchor agreement.
- Descriptor masks are byte-select masks: zero ignores, nonzero compares the entire byte.
- The fixed package's 14-subpatch total is separately checked during staging even though 14 is not a parser hard denominator.
- kind-0/1/2/3 generation semantics are defined by the formulas in §4.
- kind 1 and kind 2 do not use `arg` in target calculation.
- kind 3 uses `arg` as the helper-entry offset.
- All 11 descriptors / 14 subpatches are accounted for in §8.
- `runtime_page_mapper` targets helper `+0x00`; `runtime_byte_validation` targets helper `+0x20`.
- helper `+0x20` is not a Boolean-return validator; it directly copies accepted forms and otherwise restores the original EXE path.

## 12. Likely hypotheses

- `ui_width_1..4` likely modify UI/text extent dimensions, based on descriptor naming and the immediate changes, but exact units and individual screens remain unproven without the exact target EXE.
- `description_font_1..2` likely alter a font-selection or text-rendering argument, but the exact font identity and call-site semantics remain unproven.

## 13. Unresolved

The exact target PC EXE is still required for:

- complete whole-program XREF/caller relationships;
- exact containing-function semantics and C++-level naming;
- full instructions beyond helper return points;
- exact screen/UI effect of each width/font descriptor;
- direct runtime confirmation that the generated package executes successfully in the target process.

These are contextual/runtime-verification gaps, not gaps in the DLL-generated patch formulas and helper control flow established here.

## 14. Rejected/corrected hypotheses

- Rejected: a unique signature at any address is acceptable.
- Rejected: helper `+0x20` is a Boolean validator returning true/false.
- Rejected: fallback from `+0x20` means immediate invalid-input rejection.
- Rejected: kind 1/2 add `arg` to their generated addresses.
- Rejected: helper padding bytes are reachable executable logic.
- Corrected: raw `font_page_limit` behavior is threshold `255 -> 160`, not a proven literal page-count assignment.

## 15. Affected runtime-code surface

PHASE 4 closes the PC code-patch layer over:

- four UI/width immediates;
- two stack arguments;
- five mapping-related code operands;
- one `0xFF -> 0xA0` comparison threshold;
- two helper-entry JMPs;
- four helper return/control-transfer fixups;
- the descriptor signature/mask search/application engine.

Combined with PHASE 1–3, the PC Korean patch's runtime package is now structurally specified through initialization, parser grammar, mapping/pointer runtime data, helper logic, descriptor generation, staging, and transaction commit.

## 16. Verification method reported by PHASE 4 handoff

The PHASE 4 handoff reports a raw-byte-based restricted interpreter/probe that exercised:

- all 65,536 mapper input values; and
- 65,536 byte combinations for the byte-processing path,

along with descriptor/subpatch count and formula checks.

This was **static/restricted interpretation**, not execution of the actual target DLL inside the game process. Runtime success of the original target EXE remains outside this validation claim.

## 17. Next stage handoff

The next planned stage is **PC Runtime Canonical Closure**, not further PHASE-4 analysis.

Closure should:

- integrate PHASE 1–4 into one canonical PC runtime specification;
- resolve/supersede stale wording in earlier `PC_RUNTIME_DLL_SPEC.md` without losing provenance;
- keep raw byte behavior separate from inferred human-readable function names;
- preserve the strict descriptor-anchor rule and the staging-time 14-subpatch invariant;
- classify what is PC patcher machinery versus what is semantic game behavior that a Switch equivalent must reproduce.

This document does not authorize or begin closure, Switch counterpart analysis, ARM64 work, IPS, or builds.

STOP.
