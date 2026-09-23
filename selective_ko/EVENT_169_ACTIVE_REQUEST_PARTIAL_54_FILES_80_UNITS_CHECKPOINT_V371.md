# V371 active request 연결 및 offline 검증 — 부분 실행 기록

작성일: 2026-09-23 KST
Scope: `V371_ACTIVE_REQUEST_CONNECTION_AND_169_FILE_CANDIDATE_OFFLINE_VALIDATION`
Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`, branch `main`
Base canonical HEAD: `736f8b56ae641e847315f8e3735ad958f9538870`

## 요약

실제 Switch 입력 54개와 기존 PC 입력을 사용하여 active request 연결 및 파일 단위 offline 검증을 수행하였다. 54/54개가 통과하였다. 기존 80개 transaction unit이 속한 33개 파일을 모두 포함하며, relation 130건과 support 5건이 충족되었다.

그러나 이번 exact scope 전체는 **미완료**이다. 나머지 Switch 파일 115개의 실제 replay와 일부 기존 ECF 변환 연결이 남아 있다. Candidate EVENT 파일은 0개이며, product milestone은 `V369_UNCHANGED`이다. 현재 결과를 169-file acceptance 또는 VAL01 PASS로 승격하지 않는다.

이 문서는 이번 부분 실행을 canonical resume state로 승격하기 위한 checkpoint이다. Product milestone은 여전히 V369_UNCHANGED이며, 169-file candidate acceptance나 VAL01 PASS로 승격하지 않는다. Drive 대형 근거는 외부 보존하고 Git에는 checkpoint와 compact pointer만 기록한다.

## 1. 확정된 사실

| 항목 | 현재 실행 결과 |
|---|---:|
| 전체 request 명세 | 169개 유지 |
| 실제 Switch 원본 확보·길이/SHA 확인·replay | 54/169 |
| 실제 파일 단위 결과 | 54/54 PASS |
| 전체 PC KO 입력 | 기존 실제 추출 169개 재사용 |
| Recipe catalog 연결 | 52,491개 |
| 실제 확인한 recipe view | 35,913개 |
| Field policy catalog 연결 | 24,305개 |
| 실제 field 결과 | 18,010개 충족 |
| 실제 field writer / no-writer | 17,994 / 16 |
| 실제 owner identity | 45,669개 |
| 실행한 파일 안 owner 누락·중복 | 0 / 0 |
| 최종 책임 구간을 확인한 frozen unit | 80/80 |
| 해당 unit이 들어 있는 실제 파일 | 33/33 |
| Relation / support obligation | 130 / 5 충족 |
| IM02 bridge error | 0 |
| 후기 최종 책임 오류 주입 시 부분 결과 미반환 | 80/80 |
| 실제 EVENT 파일 출력 | 0 |

54개 파일의 원본 길이·SHA는 기존 입력 receipt와 일치한다. 여기에는 독립적 canonical 전체 파일 hash 근거가 미확정인 파일도 있으므로, observed receipt 일치를 provenance 보류 해제로 취급하지 않는다.

모든 실제 조립 결과의 unassigned / multiply_assigned / conflicting byte count는 0이고 마지막 writer는 FINAL_TABLE이다. ECF00000 메모리 내 결과는 1,119,656바이트, SHA-256 `9d9910e99296ab816b76961167d8a52baad044f0ba64f0c3a9504808030874e7`이다. 출력 파일 생성이나 실기 성공을 의미하지 않는다.

### Occurrence 연결

기존 V369 exact applicability 원장과 실제 PC KO preimage를 사용해 2,671개 occurrence를 연결하였다. 2,668개는 정확한 원장 행·좌표·바이트·ownership/runtime authority를 함께 확인하는 authored preservation action이며, 3개는 기존 frozen child delegation이다. 단순 분류명 또는 모델의 문법 추정으로 preservation permit을 만들지 않았다.

TAI5MSG root 데이터는 읽거나 연결하지 않았다. 이번에 실제 충족된 occurrence는 1,586건이며 나머지 1,085건은 NOT_OBSERVED이다.

### 기존 고정 조사 변환 연결

기존 canonical `selective_event_particle.py`의 `transform_particle_command` 및 V344 compact ledger를 소비하여 1,251개 recipe에 기존 고정 표면 변환을 연결하였다. 새 번역·문법·역할 정책은 만들지 않았다.

- 기존 변환 1,389곳, 총 5,556바이트 축소.
- 1,251개 transformed payload 모두 final buffer에서 exact readback 일치.
- 일반 exact recipe 1,250개와 frozen composite 1개(C31).
- C31은 기존 V369의 composite-before-approved-transform 순서를 사용하였다. 과거 raw PC command 길이를 현재 composite 길이로 오인해 자르지 않았다.
- V369 신규 occurrence owner와 이 고정 조사 owner의 교집합은 0이며, 별도의 임의 occurrence remap을 넣지 않았다.

### Unit / writer / 실패 시 동작

80개 unit 각각에 대해 실제 final ownership claim 존재와 delegate의 독립 payload write 부재를 확인하였다. 원본 frozen owner·field·relation membership은 그대로 소비하였다.

실제 journal의 FIELD_SLOT 2개인 ECF00000:E2A04 및 E2A28은 parent PREPARED_PAYLOAD보다 뒤, FINAL_TABLE보다 앞에 기록되었고 동일 parent writer에 종속되었다. 이 2개 journal slot을 전체 dual-view policy 8개와 동일한 모집단으로 세지 않는다. 이번 입력에서는 dual-view 정책 행 7개가 관측되었다.

후기 실패 주입 시험은 80개 unit 각각의 final ownership unit metadata 하나를 테스트 과정에서만 변조하여 수행하였다. Payload·field·table가 내부에 조립된 뒤 원래 audit가 FINAL_RESPONSIBILITY_UNIT_MISMATCH를 검출하고, run_file이 assembled object를 반환하지 않는 것을 확인하였다. 원본/PC bytes와 실제 구현 파일은 변경하지 않았다. 패치한 테스트 함수는 매 시험 후 복원하였다.

80/80은 **이 후기 최종 책임 오류 유형에 대한 discard 검증**이다. 모든 오류 지점의 rollback 또는 전체 제품 atomic acceptance가 아니다. Fault 시험의 33개 unit-file baseline은 최종 54-file replay의 원본·메모리 결과 hash와 모두 동일하다. 별도의 명시적 전체 unit scheduler/inner-before-outer acceptance 완료로 과장하지 않는다.

## 2. 유력한 가설

관측한 54개 파일과 모든 frozen unit에 대해서는 기존 source-plan field policy 및 owner identity/view 분리가 정상적으로 동작한다. 나머지 파일에도 같은 연결을 적용할 수 있을 것으로 보지만, 미실행 115개 파일의 성공을 확정하지 않는다.

## 3. 미확정 사항

| 범위 | 미완료 상태 |
|---|---|
| 나머지 Switch 원본/replay | 115개 미수행 |
| 전체 owner 최종 출력 | 21,318개 NOT_OBSERVED |
| 전체 recipe view | 16,578개 NOT_OBSERVED |
| 전체 field policy | 6,295개 NOT_OBSERVED |
| 기존 ECF direct-escape particle | 350행 연결 미완료 |
| 기존 lexical false-positive | 12행 연결 미완료 |
| 기존 derived/mixed | 61행 연결 미완료 |
| 기존 non-particle suffix | 3행 연결 미완료 |
| 전체 candidate / all-unit transaction acceptance | 미완료 |
| TAI5MSG 5 roots / 19 references | 별도 단계, 미관측 유지 |
| VAL01 / IPS / package / Eden / Switch | 미수행 |

기존 변환이 연결되지 않은 상태에서도 파일 구조 검증은 통과할 수 있다. 따라서 파일-local PASS를 기존 전체 한글 결과의 동일성 또는 모든 승인 변환 적용 완료로 사용하지 않는다. 기존 V348 direct applicability/occurrence 원장은 Git에 존재하나 이번 실행 환경의 실제 byte 입력 연결을 끝내지 못하였다. 이는 새로운 규칙 조사 필요 또는 원장 부재라는 뜻이 아니다.

### Source identity authority 60개

기존 provenance hold 60개 중 이번 실제 입력에 포함된 것은 8개이다. 8개 모두 기존 observed length/SHA와 일치하였다. 나머지 52개는 이번 byte replay를 하지 않았다. 독립 canonical 전체 파일 hash authority 보류는 **60개 모두 유지**하며 해제 건수는 0이다.

이번에 실제 byte 일치를 확인한 8개: EF520600, EFF01F00, EFF02000, EFF02300, EFF06D00, EFF07500, EFF07C00, EFF08C00.

### Obligation accounting

| 종류 | 충족 | NOT_OBSERVED |
|---|---:|---:|
| APP | 1,442 | 996 |
| OCC | 1,586 | 1,085 |
| REL | 130 | 0 |
| SUP | 5 | 0 |
| ROOT | 0 | 5 |
| ROOTREF | 0 | 19 |
| 합계 | 3,163 | 2,105 |

원장 5,268행을 모두 유지했고 누락·예상 외 키·중복이 없다. NOT_OBSERVED를 PASS나 제외로 바꾸지 않았다.

## 4. 기각된 가설 및 실패 기록

새로운 게임 데이터 예외나 core blocker는 이번 54개 파일에서 확인되지 않았다. 기존 기각 경로(geometry 개별 예외, CONTACT 전부 runtime hook, EC500000:1DC hard-NUL, final-byte field 재발견, runtime hook 우선 구현)는 재개하지 않았다.

기존 NUL 관측 실패는 관측 결과로 남겼으며 normative runtime/payload extent failure로 바꾸지 않았다. 이번 field 및 owner 정책 자체의 수정은 없었다.

실행 harness/도구 오류는 compact failure record에 제품 오류와 분리 기록하였다. 예: catalog object의 units/file 속성 접근 오류, 진단 JSON 기록의 로컬 파일 권한 오류, 허용되지 않는 GitHub binary archive fetch, raw 공개 파일 다운로드 경로 실패. 이들을 제품 테스트 실패나 PASS에 포함하지 않았다.

## 5. 관련 영향 범위

변경은 로컬 active request의 occurrence action/permit 및 기존 고정 조사 payload 연결과 진단 harness에 한정된다. Canonical serializer, field codec, H01, CONTACT, owner identity/extent, source-copy, final partition table 알고리즘은 변경하지 않았다. 66,987-owner/52,491-INCLUDE membership, 24,305 field authority, 80-unit membership, FZ001, V366–V369 제품 authority도 변경하지 않았다.

이번 단계의 54-file 결과와 80개 후기 실패 주입 시험은 과거 746개 regression 또는 과거 731개 regression과 다른 모집단이다. 기존 24,305/24,305 source/output oracle PASS를 이번 전체 재실행 결과로 표시하지 않는다.

## 6. 다음 진행 제안

동일 scope를 미완료 상태로 이어간다. 먼저 기존 변환의 exact applicability/occurrence/binding byte 입력을 현재 요청에 연결하고, 남은 115개 실제 source를 기존 receipt로 확인하여 replay한다. 이미 완료한 원장 해석이나 semantic admission을 다시 분류하지 않는다.

그 후 모든 변환을 포함한 169-file 조립, 66,987 owner와 24,305 field 전수 결과, 보호 범위·branch·partition·writer 책임, 전체 transaction acceptance를 확인해야 한다. 이번 결과 보고 자체로 다음 구현·수정·검증을 자동 시작하지 않는다. TAI5MSG·VAL01·IPS·실기는 계속 별도 단계이다.

## 보존 및 실행

동봉 `CURRENT_SCOPE_RESULT.json`, `diagnostics/`, `LATE_FAILURE_DISCARD_80.json`, `SOURCE_IDENTITY_HOLDS_60_CURRENT_SCOPE.json`, `OWNER_AND_FIELD_ACCOUNTING.json`, `active_inputs/`, `authorities/` 및 `replay.py`가 이번 실행의 상세 근거이다.

`replay.py --output <새 디렉터리>`는 포함된 실제 입력만 재생하여 JSON 진단을 생성하고, 누락 파일을 명시한다. EVENT 바이너리는 생성하지 않는다. 필요 시 `--late-failure-probes`로 같은 후기 실패 주입 시험을 실행할 수 있다. 기존 authority archive는 hash 확인 후 소비하며, 역사적 역할·semantic 정책을 재생성하지 않는다.

최종 immutable package의 `PACKAGE_MEMBERS.json`에 각 파일 SHA-256을 기록한다. ZIP 자체의 size/SHA는 별도 포장 receipt로 제공한다. 2026-09-23 재시도에서 Google Drive 업로드가 실제로 가능함을 확인하였고, 아래 네 파일을 `GPT/태합입지전 프로젝트/CODEX`에 새 파일로 보존하였다. 기존 파일은 덮어쓰지 않았다.

- report Drive ID: `18aGjvV3Dr6wwB_x5tUMzjRXANajCksWK`
- archive Drive ID: `1_2ndn8EbetZa-6qGSvN3fMWkFp7et01Z`
- result Drive ID: `1-JRBbrI4Guwie2BDpDPblRa6QYtbD04Q`
- packaging receipt Drive ID: `1_uge2S9RbQjb2mc3GLg5NyHWaBja5tqM`

Repository publication uses only the permitted Git-object route: `create_blob -> create_tree -> create_commit -> update_ref(force=false)`. The large ZIP is not stored in Git; this checkpoint and its compact artifact/failure records preserve the resume authority and Drive identities.
