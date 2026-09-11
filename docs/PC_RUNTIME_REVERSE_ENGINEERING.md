# PC runtime reverse engineering — staged master

## 운영 상태

- PHASE 1 완료: DLL loading / proxy / initialization / EXE validation / patch transaction framework.
- PHASE 2 완료: T5K parser `0x2640` wire grammar / bounds / parsed representation / failure propagation.
- PHASE 3 완료: mapping 10,036 runtime storage / lookup relocation / pointer 56 mode-arg application engine.
- PHASE 4 완료: 158-byte helper / descriptor search+application / 11 descriptors / 14 subpatch semantics.
- **PC Runtime Canonical Closure 완료.**
- 다음 단계는 **Switch Functional Counterpart Survey**이며, 사용자의 새로운 실행 신호 없이는 시작하지 않는다.
- counterpart survey 전에는 ARM64 구현, code/data cave 설계 확정, IPS, 빌드 생성을 하지 않는다.

## Canonical records

확정 사실을 새 채팅/모델이라는 이유만으로 재검증하지 않는다.

1. PHASE 1: `docs/PC_RUNTIME_REVERSE_ENGINEERING_PHASE1.md`
2. PHASE 2: `docs/PC_RUNTIME_PHASE2_PARSER_SPEC.md`
3. PHASE 3: `docs/PC_RUNTIME_PHASE3_MAPPING_POINTER_SPEC.md`
4. PHASE 4: `docs/PC_RUNTIME_PHASE4_HELPER_DESCRIPTOR_SPEC.md`
5. Canonical closure: `docs/PC_RUNTIME_CANONICAL_CLOSURE.md`
6. Closed PC runtime spec: `docs/PC_RUNTIME_DLL_SPEC.md`
7. PC -> Switch status matrix: `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md`
8. next-stage survey rules: `docs/SWITCH_COUNTERPART_SURVEY_RULES.md`
9. validation authority: `docs/VALIDATION_LEDGER.md`
10. current resume point: `PROJECT_STATE.md`

## Fixed PC inputs

- PC patch ZIP SHA-256: `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`
- embedded `dinput8.dll`: 836,096 bytes, SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` SHA-256: `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- exact PC target EXE: Steam 1.2.1.0 build 9163702, 18,685,960 bytes, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`
- supplied mismatched PC EXE must not be used for PC RVA neighborhood/XREF evidence.

## Closure canonical result

### Initialization / transaction

- `DllMain` does not apply the patch; `DirectInput8Create` triggers separate proxy and patch once guards.
- T5K parse -> disk identity -> memory PE profile -> private storage -> staging -> final storage protections -> commit.
- one contiguous private allocation contains page-aligned prefix/helper regions.
- staging requires exact preimage and rejects overlap; no record-by-record skip on mismatch.
- commit priorities are inline 0 -> pointer 1 -> code 2.
- failure is fail-closed; rollback is best-effort, not a full atomicity guarantee.

### T5K grammar

- exact `0x48` header and fixed parser denominators are established.
- pointer wire grammar is `u32 slot, u32 original_target, u8 mode, reserved[3], u32 arg`; the older `<IIII>` representation is superseded.
- 14 subpatches are a fixed-resource population and staging invariant, not a parser hard denominator.

### Mapping / pointer data layer

- prefix total `0x9F2A = 40,746` bytes = mapping `0x9CD0 = 40,144` bytes + pool `0x25A = 602` bytes.
- mapping content is 7,494 originals + 2,542 Korean = 10,036.
- two lookup paths alter three mapping-address operands plus two `7,494 -> 10,036` limits.
- all 56 pointer records stage 8-byte absolute writes.
- mode 0: 5 records, destination = EXE/module base + `arg`, converging on two inline-translated module targets.
- mode 1: 51 records, destination = private prefix base + `arg`, referencing 47 distinct pool strings.
- mapping relocation and pointer application are separate engines.

### Helper / descriptor code layer

- helper: 158 bytes, descriptor-used entries `+0x00` and `+0x20`.
- descriptor search is PC `.text` masked search with exact uniqueness + exact anchor requirement.
- kind formulas:
  - kind0 = payload
  - kind1 = `i32(P-W-4)`
  - kind2 = `i32(P-M)`
  - kind3 = `E9 || i32(H+arg-W-5)`
- kind1/2 do not use `arg`; kind3 uses helper-entry offset.
- page mapper `+0x00`: `EB..F8 -> pages 49..62`; otherwise returns to original PC flow at `0x6933D5`.
- byte-validation/copy `+0x20`: handles accepted one/two-byte forms then jumps to `0x6832BC`; other input resumes original processing at `0x68328A`. It is not a Boolean validator.
- all 11 descriptors / 14 subpatches are accounted for; kind population `9/2/1/2`.
- raw `font_page_limit` behavior is threshold `0xFF -> 0xA0`, not a proven literal page-count edit.

## Closure corrections to stale SPEC wording

The closed `docs/PC_RUNTIME_DLL_SPEC.md` now corrects all identified PHASE 2–4 conflicts:

- pointer record grammar / universal string-offset naming;
- separate-allocation wording for helper;
- helper `+0x20` fallback semantics;
- `font_page_limit` semantic overclaim;
- PC descriptor uniqueness policy being misread as a future Switch discovery gate.

The closure introduces no V062+ factual validations. V001–V061 remain the factual ledger authority.

## PC completion vs Switch completion

The PC runtime reference is closed. Switch porting is not.

The next-stage matrix intentionally keeps Switch statuses separate. In particular:

- mapping additional capacity is a primary unresolved placement risk;
- pointer 56 remains a separate survey axis and shares replacement-storage concerns with mapping/prefix design;
- helper code space is not assumed mandatory because equivalent behavior may be achievable in existing ARM64 control flow;
- `NATIVE_EQUIVALENT` claims require concrete Switch evidence; otherwise status remains `UNSURVEYED` / `PARTIAL_EVIDENCE` / `UNRESOLVED`.

The missing compact `쓰` symptom remains a three-path unresolved model: data selection / pointer-reference selection / byte-validation-copy path. No single path is promoted to root cause by closure.

PCREF1 delivery verification may run in parallel with static counterpart survey but must be closed before a new counterpart-derived runtime result is used as causal evidence.

## PHASE 4 transfer provenance

The original PHASE 4 handoff reported `docs/PC_RUNTIME_PHASE4_VERIFICATION.json`, `tools/pc_phase4_probe.py`, and a raw-evidence/handoff ZIP. Those auxiliary files were not available at canonical-import time and were not fabricated. This remains recorded provenance, not a reason to reopen already-validated PHASE 4 claims absent a high-risk evidence need.

## Next authorized scope after a fresh signal

**Switch Functional Counterpart Survey only.**

Follow `docs/SWITCH_COUNTERPART_SURVEY_RULES.md`. Survey the five primary axes (mapping, pointer 56, helper semantics, descriptor 14 semantics, inline/data-selection coverage), keep CWTDAT as a separate data axis, produce full counterpart and space/capacity matrices, report, and STOP.

Do not proceed directly to implementation, IPS, diagnostic build or runtime testing under the closure authorization.
