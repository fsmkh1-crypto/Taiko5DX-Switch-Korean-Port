# EVENT 169 Role-Aware Field-Policy Adapter Implementation — V371

Date: 2026-09-23 (KST)  
Track: `SWITCH_SELECTIVE_KOREANIZATION`  
Base HEAD: `fedf8f2dc7161f4aae145fa59fecfe47d0658389`  
Implementation commit: `4c5d2c4e010bf9c760337d39c0a64b6a82314918`

## 확정된 사실

- 24,305개 retained structural field 모두 exact role-aware policy와 결합됨.
- generic field는 source-plan owner/stage-count를 사용하며 final-byte reparsing을 사용하지 않음.
- 24,284개 writer policy와 21개 no-writer preservation policy가 분리됨.
- `CONTACT:<owner>`와 `CONTACT:O:<owner>`를 모두 처리함.
- H01은 exact `ECF00000:E29F4` identity parent와 내부 field slot 2개에만 열림.
- dual-view slot 8개는 `parent payload -> subordinate slot -> final partition table` 순서를 사용함.
- manifest field-rule override는 canonical policy가 활성화된 경우 차단됨.
- bounded test 731개 및 full-policy source/output oracle 24,305개가 모두 통과함.
- 실제 EVENT candidate, IPS, package, runtime output은 생성하지 않음.

## 유력한 가설

현재 adapter를 실제 169-file request에 연결하면 Switch runtime hook 없이 정적 candidate를 만들 가능성이 높음. 전체 candidate replay 전에는 제품 수준 확정으로 승격하지 않음.

## 미확정 사항

- 169개 actual request materialization
- 52,491 recipe와 24,305 policy의 전체 연결
- source identity authority 60개
- 80 transaction unit atomic layout
- 66,987 owner final output accounting
- TAI5MSG 5 roots / 19 references readback
- VAL01, IPS/package, Eden 및 Switch 실기

## 기각된 가설

- geometry-change 11,764개가 개별 예외라는 가설
- contact field 700개가 전부 runtime hook 대상이라는 가설
- `EC500000:1DC`가 정적 방식으로 불가능한 NUL 충돌이라는 가설
- final bytes를 다시 훑어 field writer를 발견해야 한다는 가설
- request manifest의 field-rule override가 허용되어야 한다는 가설

## 관련 영향 범위

- V366 binding, V367 endpoint, V368 semantic policy, V369 applicability/overlap authority는 변경하지 않음.
- 66,987 owner 및 52,491 recipe membership은 그대로 유지됨.
- 변경은 field-policy adapter, exact H01 contract, bounded tests, CLI wiring 및 CI에 한정됨.
- product bytes는 mutation하지 않았음.

## 수정 내용·검증

| 항목 | 결과 |
|---|---:|
| IM01 | 150/150 PASS |
| IM02 | 363/363 PASS |
| IM03 | 196/196 PASS |
| H01 | 7/7 PASS |
| Role adapter | 11/11 PASS |
| Canonical compact | 4/4 PASS |
| Total | 731 PASS |
| Full policy source oracle | 24,305/24,305 PASS |
| Full policy output oracle | 24,305/24,305 PASS |
| Product outputs | 0 |

Implementation package:

- name: `V371_ROLE_AWARE_FIELD_POLICY_ADAPTER_IMPLEMENTATION_AND_BOUNDED_VALIDATION_20260923.zip`
- SHA-256: `a8f11bcdf712f7995a749a381ff2dd400acf26f784605cadd32a16041f10a1c0`
- bytes: `139343`
- Drive ID: `1DUK7JUgY17PFw8_Ma3csgCA2uOR58h6S`

Full policy authority package:

- Drive ID: `1RiWHEyUTrOW-Ctc3WxG_q-Q6nCf8vRle`
- field ledger SHA-256: `4cdf5df2c6b7264641374d459ef1dc7484749ea6adfb99b5646a6c40cfddfeff`

## Claim boundary

This checkpoint closes only the bounded adapter implementation. It does not close 169-file product serialization, VAL01, packaging, or runtime safety.

## Exact next scope

`V371_ACTIVE_REQUEST_CONNECTION_AND_169_FILE_CANDIDATE_OFFLINE_VALIDATION`
