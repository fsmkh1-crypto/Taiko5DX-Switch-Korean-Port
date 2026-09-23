# V371 owner identity / view extent gate 수정 및 bounded regression

Date: 2026-09-23 KST
Scope: `V371_OWNER_IDENTITY_AND_VIEW_EXTENT_GATE_FIX_AND_BOUNDED_REGRESSION`
Base HEAD: `3130e21e818d0ced734e9defab3f4c8fe7cfbfcf`
Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`, `main`

## 요약

관측 범위를 실제 owner 처리 범위로 사용하던 공통 검증 경계를 수정하였다.
최종 수정본의 이번 회귀 테스트 746/746이 통과하였고, 실제 Switch 입력 ECF00000.TS5와 EPF11700.TS5의 파일 단위 검증이 2/2 통과하였다.
실제 두 파일의 IM02 연결 오류는 0이며, 해당 입력에서 관측한 relation 69건이 통과하였다.
이는 169-file candidate acceptance가 아니다. Candidate EVENT 파일 출력은 0이며 product milestone은 V369_UNCHANGED이다.

Implementation commit: `59e12802f402ea06c3331c16b32c2cbb9216e900`.
이 checkpoint는 위 구현과 bounded 검증만 닫는다. Repository-level resume authority는 root PROJECT_STATE.md이며, 다음 실행 범위는 SELECTIVE_PROJECT_STATE.md를 따른다.

Evidence archive Drive ID: `1Xr1XIlI6OC34DgKvBTl3RQvby2lT8slk`.
Archive bytes: `42144503`; SHA-256: `aac97129f7e236339bd70a9f0c83880bac9cb134cb158d4faf00536fdfc0d071`.
Exact inputs, 746 per-test results, two-file receipts and initial failed-fix evidence are preserved there.
Index: `artifacts/event_169_owner_extent_gate_fix_v1/INDEX.json`.
Failures: `artifacts/event_169_owner_extent_gate_fix_v1/KNOWN_FAILURES.json`.

## 1. 확정된 사실

| 항목 | 결과 |
|---|---:|
| 최종 회귀 테스트 | 746 / 746 PASS |
| 이번 실행에서 수집한 기존 테스트 | 720 / 720 PASS |
| 신규 identity / extent 회귀 | 26 / 26 PASS |
| 실제 파일 단위 검증 | 2 / 2 PASS |
| ECF00000 owner identity | 15,951 / 15,951 |
| EPF11700 owner identity | 175 / 175 |
| 두 파일 exact recipe view | 14,281 + 155 |
| 두 파일 frozen relation owner view | 96 + 2 |
| 두 파일 IM02 bridge error | 0 |
| 실제 관측 relation receipt | 69 PASS |
| 전체 obligation receipt accounting | 5,268행, 누락 0, 중복 키 없음 |
| 전체 obligation 미관측 | 5,199 |
| Candidate EVENT 파일 출력 | 0 |

746은 이 실행의 실제 수집 결과이다. IM01 150, IM02 363, IM03 196, H01 7, 현재 compact role-policy test 4, 신규 extent test 26으로 구성된다.
기존 V371 문서의 731 PASS는 역사적 승계값이며, 이 실행의 746을 '731 + 신규 테스트'로 계산하거나 같은 모집단이라고 주장하지 않는다.
기존 VERIFIED/CLOSED 해석을 재분류하거나 재생성하지 않았고, 회귀에 필요한 기존 입력·fixture와 adapter만 소비하였다.

### 실제 파일 결과

| 파일 | 파일 단위 결과 | 메모리 내 조립 길이 | 미배정 / 중복배정 / 충돌 | 마지막 writer |
|---|---|---:|---|---|
| ECF00000.TS5 | PASS | 1,125,212 | 0 / 0 / 0 | FINAL_TABLE |
| EPF11700.TS5 | PASS | 10,460 | 0 / 0 / 0 | FINAL_TABLE |

두 파일 모두 기존 source identity와 일치한 동일 입력을 사용하였다. 출력 길이와 해시는 메모리 내 bounded 결과의 식별값이지 배포용 파일을 생성했다는 뜻이 아니다.
원본의 비규범적 NUL 관측 실패는 두 곳 모두 그대로 남겨 관측 결과로 기록하였고, 이를 payload 또는 runtime 범위의 실패로 승격하지 않았다.

### 적용한 수정

1. 모든 owner의 identity는 원본에서 유지된 header 시작점을 final layout으로 매핑하고 고정 폭 4바이트로 검증한다.
2. DIRECT는 실제 payload placement, DELEGATE는 준비된 exact source recipe span의 mapping으로 recipe 범위를 검증한다. 위임은 upstream recipe 준비를 면제하지 않는다.
3. Frozen relation의 member만 기존 retained view를 relation topology의 범위로 사용한다. 기존 cluster union 및 writer responsibility는 축소하지 않는다.
4. Established consumer의 모든 ProtectedRange는 기존 검사로 그대로 보존한다. Identity-only는 consumer 부재 또는 안전성을 뜻하지 않는다.
5. IM02의 owner view에 extent basis와 별도 recipe placement를 전달한다. Identity-only는 occurrence·relation·support range를 증명할 수 없다.
6. Occurrence는 recipe placement를 사용하고, relation은 frozen relation view를 사용하도록 분리하였다.
7. Source-copy, field-policy, H01, CONTACT, final partition table 및 writer audit 구현은 변경하지 않았다.

## 2. 유력한 가설

같은 호출 경계를 사용하는 보존·위임 owner에 대한 이번 수정은 주소별 예외 없이 적용 가능하다.
실제 두 파일 및 회귀 결과가 이를 뒷받침하지만, 아직 실행하지 않은 나머지 167개 Switch 파일의 성공까지 확정하지 않는다.

## 3. 미확정 사항

나머지 Switch 원본 167개에 대한 실제 replay, occurrence action/rewrite/preservation permit 연결, 전체 80개 transaction unit의 inner-before-outer 및 atomic commit/rollback acceptance, 전체 66,987개 owner의 final output accounting이 남아 있다.
전체 5,268 obligation 중 69 relation만 이번 두 입력에서 관측되었다. 5,199 NOT_OBSERVED를 PASS 또는 제외로 바꾸지 않았다.
Source identity 60개 provenance hold는 변경하지 않았다. 이 두 실데이터 입력은 그 60개 밖의 파일이며, 60개에 대한 신규 byte PASS를 주장하지 않는다.
TAI5MSG 5 roots / 19 references, VAL01, IPS/package, Eden 및 Switch 실기 검증은 하지 않았다.

## 4. 기각·실패한 접근

- 관측 범위 전체를 보편적인 runtime extent로 취급하는 접근은 사용하지 않는다.
- 두 주소만 예외 처리, partition 끝으로 강제 절단, 모든 consumer/relation view를 4바이트로 축소, partition gate 제거는 사용하지 않는다.
- 1차 수정에서 header [start,start+4)를 그대로 project한 방식은 source recipe가 4바이트뿐이고 payload가 늘어나는 경우 terminal payload anchor와 충돌하였다. 기존 회귀 3건이 이를 검출하였다. 최종 수정은 mapped header start + 고정 폭으로 분리하였고, 신규 양성 회귀를 추가한 뒤 746/746 PASS를 확인하였다.
- 초기 테스트 호출 두 번은 도구 실행 제한으로 종료되었다. 이를 테스트 PASS 또는 제품 오류로 집계하지 않았다.
- 기각된 geometry 개별 예외, CONTACT 전부 hook, EC500000:1DC hard-NUL, final-byte field 재발견, runtime hook 우선 구현을 다시 열지 않았다.

## 5. 관련 영향 범위

이전 조사에서 확정된 공통 fallback 모집단은 보존 14,496 + 위임 91 = 14,587개이다. 이는 오류 개수가 아니다.
이번 수정은 전체 공통 경로에 적용하였고, 실제 replay의 owner identity 검증은 두 파일 합계 16,126개이다.
91개 위임 계약의 recipe extent와 retained view 연결을 소비·대조하여 같은 source extent임을 기록하였으며, 별도 독립 writer를 만들지 않았다.
Recipe/field 정책 원장과 semantic admission, owner membership, FZ001 및 V366-V369 product authority는 변경하지 않았다.
수정된 제품 코드 파일은 selective_event_overlap.py 및 selective_event_obligation_receipts.py 두 개이다.

## 6. 다음 범위

이번 수정·회귀 범위의 결과를 보고하고 멈춘다. 새 실행 신호 후 다음 scope를 재개한다.

`V371_ACTIVE_REQUEST_CONNECTION_AND_169_FILE_CANDIDATE_OFFLINE_VALIDATION`

기존 169개 request 명세·52,491 recipe·24,305 field policy를 재사용하고, 아직 미완료인 실제 입력과 occurrence disposition 연결부터 계속한다.
이 보고 자체는 다음 전체 candidate 생성, VAL01 또는 실기 단계의 실행 신호가 아니다.
