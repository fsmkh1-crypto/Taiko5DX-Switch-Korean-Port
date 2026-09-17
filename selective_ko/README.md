# Taiko5DX Switch 선택형 한국어화

이 디렉터리는 기존 `Taiko5DX-Switch-Korean-Port`의 전체 포팅 트랙과 분리된 **선택형 한국어화 프로젝트**다.

기존 프로젝트의 검증 결과와 한국어 자산은 최대한 재사용하되, PC 한글패치 구현을 그대로 복제하지 않는다. 목표는 Nintendo Switch v1.1.3에서 게임 이해에 직접 필요한 콘텐츠를 안정적으로 한국어로 제공하는 것이다.

## 목표

우선 한국어화 대상:

- 인물 설명
- 지역 설명
- 도구/아이템 설명
- 기술/스킬 설명
- 이벤트 본문
- 안전하게 분리 가능한 이벤트/일반 대사
- 필요한 설명성 UI

기본적으로 일본어 유지:

- 인물 이름
- 지명 자체
- 연/월/일 및 달력 표현
- 요미/읽기/정렬용 필드
- 성/이름 분리 표시 로직
- 한글 작명 입력
- 동적 문법 formatter 의존 대사

동적 대사는 release 필수 범위가 아니다. 안정적인 family-level 한국어 문법 규칙이 증명된 경우에만 별도 단계에서 포함한다.

## 핵심 원칙

1. PC 한글패치는 **번역/용어/폰트/매핑 자산의 source reference**로 사용한다.
2. PC Windows 코드 패치, descriptor, helper, 우회 데이터는 **문제 해결 방식의 참고자료**이지 Switch 구현 명세가 아니다.
3. Switch에서는 원본 native 구조를 유지하고 필요한 한국어 semantic effect만 구현한다.
4. 이름/지명/날짜를 한국어화하기 위해 CWTDAT/yomi/name-composition 계층을 건드리지 않는다.
5. 문장별 땜질, `하하 -> 하`, `이이 -> 이` 같은 전역 문자열 중복 제거는 금지한다.
6. 동적 문법 문제는 formatter family 전체 caller를 조사한 뒤에만 해결한다.
7. 이미 VERIFIED인 Mapping 10,036 등 Switch-native 기반은 재사용하고 새 프로젝트라는 이유로 재검증하지 않는다.
8. V290/V291 full-port 통합 산출물은 selective 제품 baseline으로 재사용하지 않는다.

## 프로젝트 구조

- `SELECTIVE_PROJECT_STATE.md` — 이 선택형 트랙의 현재 상태와 **유일한 실행 next-scope authority**
- `ARCHITECTURE.md` — Switch-native 설계
- `CLASSIFICATION_SCHEMA.md` — 기존 한국어 corpus를 새 범위로 분류하는 규칙
- `MIGRATION_MANIFEST.json` — 기존 프로젝트/Drive에서 이관한 자료와 provenance
- `KNOWN_FAILURES.md` — 기존 전체포팅에서 확인된 실패 접근 및 재사용 금지 경로
- `reuse/` — 이미 검증되어 직접 재사용 가치가 높은 구현 자산
- `reference/` — 분석/추출용 legacy reference. release builder에 자동 포함하지 않음

## 기존 프로젝트와의 관계

기존 전체포팅 프로젝트의 Stage1/Stage2/F1/FZ001, Mapping, pointer, runtime 분석 자료는 삭제하지 않는다. 이 프로젝트는 그 위에서 **필요한 부분만 소비하는 새 제품 범위**다.

기존 17,103 inline record를 모두 구현하는 것은 더 이상 release 목표가 아니다. 대신 각 source를 명시적으로 `한국어화 포함 / 일본어 유지 / 동적 대사 보류 / 범위 밖`으로 disposition한다.

V285-V288 grammar125 분석/manifest는 optional R4 evidence로 보존한다. V289 구현은 reference only이며, V290 builder/build와 V291 package는 selective 제품에서 제외한다.

## 현재 단계 및 실행 라우팅

이 README는 실행 next scope를 선언하지 않는다.

현재 실행 가능한 정확한 다음 scope는 반드시:

`selective_ko/SELECTIVE_PROJECT_STATE.md`

에서 확인한다.

V293 이후에는 broad corpus classification에 앞서 콘텐츠 컨테이너/필드 가용성과 기존 owner/parser coverage를 먼저 조사하는 방향으로 재정렬되었다. 다른 설계/역사 문서의 과거 `next scope` 문구는 resume authority가 아니다.
