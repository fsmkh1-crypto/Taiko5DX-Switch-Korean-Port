# PC runtime reverse engineering — staged master

## 운영 상태

- PHASE 1 완료: DLL loading / proxy / initialization / EXE validation / patch transaction framework.
- PHASE 2 완료: T5K parser `0x2640` wire grammar / bounds / parsed representation / failure propagation.
- PHASE 3 완료: mapping 10,036 runtime storage / lookup relocation / pointer 56 mode-arg application engine.
- PHASE 4 완료: 158-byte helper / descriptor search+application / 11 descriptors / 14 subpatch semantics.
- 다음 단계는 PC Runtime Canonical Closure이며, 사용자의 새로운 실행 신호 없이는 시작하지 않는다.
- PC runtime closure 전까지 Switch counterpart 조사, ARM64, IPS, 빌드 생성을 하지 않는다.

## Canonical phase records

이 master는 단계별 상세 기록의 index다. 확정 사실을 새 채팅/모델이라는 이유로 재검증하지 않는다.

1. PHASE 1 상세: `docs/PC_RUNTIME_REVERSE_ENGINEERING_PHASE1.md`
2. PHASE 2 상세/인계: `docs/PC_RUNTIME_PHASE2_PARSER_SPEC.md`
3. PHASE 3 상세/인계: `docs/PC_RUNTIME_PHASE3_MAPPING_POINTER_SPEC.md`
4. PHASE 4 상세/인계: `docs/PC_RUNTIME_PHASE4_HELPER_DESCRIPTOR_SPEC.md`
5. 검증 원장 index: `docs/VALIDATION_LEDGER.md`
6. 현재 resume point: `PROJECT_STATE.md`

새 단계가 완료되면 해당 상세 문서를 추가하고 이 index, validation ledger, state, changelog를 함께 갱신한 뒤 STOP한다.

## Fixed PC inputs

- PC patch ZIP SHA-256: `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`
- embedded `dinput8.dll`: 836,096 bytes, SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` SHA-256: `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- exact PC target EXE: Steam 1.2.1.0 build 9163702, 18,685,960 bytes, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`
- supplied mismatched PC EXE must not be used for PC RVA neighborhood/XREF evidence.

## PHASE 3 canonical result

- The runtime prefix is `0x9F2A` bytes: 10,036 x 4-byte mapping entries (`0x9CD0`) plus a 602-byte pointer replacement pool (`0x25A`).
- The expanded mapping table is copied into private runtime storage; it is not builder-only metadata.
- Two lookup paths collectively redirect three table/address operands to relocated mapping storage and expand two limits from 7,494 (`0x1D46`) to 10,036 (`0x2734`).
- All 56 pointer records stage 8-byte absolute pointer writes.
- Mode 0 (5 records): destination = EXE/module base + `arg`; the five records converge on two module-resident targets translated by inline patches.
- Mode 1 (51 records): destination = private prefix base + `arg`; the 51 records reference 47 distinct replacement strings.
- Pointer-record application and mapping relocation are separate engines sharing the private prefix allocation.
- Exact target EXE absence limits whole-program XREF/table/UI naming only; it does not reopen the established base/count/write semantics.

## PHASE 4 canonical result

- The 158-byte helper has two descriptor-used logical entries: `+0x00` and `+0x20`.
- The helper handoff counts 42 reachable instructions plus 4 bytes of unreachable alignment/padding and four runtime-fixed control-transfer targets.
- Descriptor search scans `.text`; mask `0x00` ignores a byte and nonzero compares the whole byte. Success requires exactly one match and exact anchor agreement.
- Fixed-package staging separately requires 14 generated subpatches, even though 14 is not a PHASE-2 parser hard denominator.
- Subpatch formulas:
  - kind 0: literal payload;
  - kind 1: `i32(P-W-4)` RIP-relative relocated-prefix displacement;
  - kind 2: `i32(P-M)` module-relative relocated-prefix displacement;
  - kind 3: `E9 || i32(H+arg-W-5)` helper JMP.
- kind 1/2 do not use `arg`; kind 3 uses `arg` as helper-entry offset.
- `runtime_page_mapper` jumps to helper `+0x00`: `EB..F8 -> pages 49..62`, otherwise original-path continuation at EXE RVA `0x6933D5`.
- `runtime_byte_validation` jumps to helper `+0x20`: directly handles accepted 1/2-byte forms, successful handled cases jump to `0x6832BC`, other inputs resume the original path at `0x68328A`; it is not a Boolean-return validator.
- All 11 descriptors / 14 subpatches are accounted for with kind population `9/2/1/2`.
- Raw `font_page_limit` behavior is compare threshold `0xFF -> 0xA0`; a literal font-page-count interpretation is rejected.
- Exact EXE absence still limits caller/XREF/UI naming and actual target-process runtime confirmation, not the DLL-generated patch formulas/control flow.

## PHASE 4 transfer provenance

The original PHASE 4 handoff reported auxiliary verification JSON, a probe script and a ZIP containing raw signature/mask/preimage/payload evidence. Those files were not available to the repository-importing agent and were not recreated. The canonical PHASE 4 detail/ledger preserve the reported results and this transfer limitation explicitly.

## Next authorized scope after a fresh signal

The next stage is **PC Runtime Canonical Closure** only.

Closure should integrate PHASE 1–4, supersede/correct stale wording in `docs/PC_RUNTIME_DLL_SPEC.md` without losing provenance, separate raw byte behavior from inferred human-readable roles, and produce the authoritative PC reference package for later Switch counterpart analysis.

Do not inspect Switch counterparts, ARM64, code/data caves, IPS or builds until closure is separately authorized and completed.
