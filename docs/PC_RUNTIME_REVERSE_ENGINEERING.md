# PC runtime reverse engineering — staged master

## 운영 상태

- PHASE 1 완료: DLL loading / proxy / initialization / EXE validation / patch transaction framework.
- PHASE 2 완료: T5K parser `0x2640` wire grammar / bounds / parsed representation / failure propagation.
- PHASE 3 완료: mapping 10,036 runtime storage / lookup relocation / pointer 56 mode-arg application engine.
- PHASE 4 이후는 미착수. 사용자의 새로운 실행 신호 없이는 진행하지 않는다.
- PHASE 1~5에서는 Switch counterpart 조사, ARM64, IPS, 빌드 생성을 하지 않는다.

## Canonical phase records

이 master는 단계별 상세 기록의 index다. 확정 사실을 새 채팅/모델이라는 이유로 재검증하지 않는다.

1. PHASE 1 상세: `docs/PC_RUNTIME_REVERSE_ENGINEERING_PHASE1.md`
2. PHASE 2 상세/인계: `docs/PC_RUNTIME_PHASE2_PARSER_SPEC.md`
3. PHASE 3 상세/인계: `docs/PC_RUNTIME_PHASE3_MAPPING_POINTER_SPEC.md`
4. 검증 원장 index: `docs/VALIDATION_LEDGER.md`
5. 현재 resume point: `PROJECT_STATE.md`

새 단계가 완료되면 해당 phase 상세 문서를 추가하고 이 index, validation ledger, state, changelog를 함께 갱신한 뒤 STOP한다.

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

## Next authorized scope after a fresh signal

PHASE 4 is limited to the remaining PC runtime code layer:

- 158-byte helper machine-code semantics and entry/fixup behavior;
- runtime descriptor/subpatch application semantics, including kind/arg meanings.

Do not inspect Switch counterparts, ARM64, code caves, IPS or builds during PHASE 4. After PHASE 4, perform a separate PC-runtime canonical closure before beginning Switch-equivalent design.
