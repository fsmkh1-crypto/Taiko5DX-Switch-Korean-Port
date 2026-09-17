# INLINE R1 STATIC 47 CANDIDATE / CLASSIFICATION — V300

Date: 2026-09-18 (KST)
Status: CANONICAL CANDIDATE/CLASSIFICATION MATERIALIZATION / R1 STATIC_COMPLETE 47 / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V300`
Parent: `76de9d78d46eebafee08f432ca9184415a9fb904` / V299

## 1. Scope

This validation materializes only the 47 ordinary-inline R1 static rows already closed by the selected-use static49 audit.

Explicit exclusions:

```text
R2884  `２１に近い`
R2885  `方が勝ち`
```

Those two remain `CALLER_UNKNOWN / UNRESOLVED`. V300 does not promote, modify, reject, or re-audit them.

V300 performs no builder implementation, Switch game-byte mutation, IPS generation, runtime test, layout test, or hardware validation.

Canonical row artifact:

`selective_ko/artifacts/inline_r1_static_47_candidate_classification_v1/INDEX.json`

## 2. Materialized population

V300 adds:

```text
candidate IDs              47
classification IDs         47
INCLUDE_KO rows            47

SEL-CAND-000093 .. SEL-CAND-000139
SEL-CLS-000093  .. SEL-CLS-000139
```

Cumulative selective R1 classification after V300:

```text
V298 ending-help STATIC_COMPLETE        39
V299 numeric VARIABLE_INSERT            53
V300 ordinary-inline STATIC_COMPLETE    47
------------------------------------------
materialized INCLUDE_KO                139
```

The inline R1 source-role census remains 141; two rows remain unresolved.

## 3. Per-row evidence model

Every V300 row contains actual individual values for:

- exact PC inline source record ID / RNUM / RVA;
- contributing exact-pair group IDs;
- complete Switch Japanese logical object;
- complete reconstructed PC Korean logical payload;
- exact Switch physical owner;
- `.rela.dyn R_AARCH64_RELATIVE (0x403)` source/consumer slot;
- original NUL boundary and proven storage capacity;
- Korean payload byte length and slack;
- mechanism / usage / investigation axes;
- risk / conflict / provenance / derived disposition.

No family-placeholder row is used.

## 4. Population invariants

```text
physical owners                    47 unique
PC inline source records           49 unique
RELA consumer slots                47 unique
owners with one RELA slot          47
owners with shared slots            0

original guard failures             0
terminator failures                 0
capacity failures                   0
risk-flagged rows                   0
manual overrides                    0
non-INCLUDE rows                    0

mechanism_class       STATIC_COMPLETE 47/47
usage_class           UI_DESCRIPTION 47/47
investigation_status  RESOLVED 47/47
derived_disposition   INCLUDE_KO 47/47
```

Payload/storage:

```text
KO payload incl NUL     10..38 bytes
proven capacity         13..41 bytes
minimum slack           0 bytes
maximum slack           10 bytes
exact-fit rows           2
```

## 5. Reconstruction exceptions retained from the audit

The static49 audit established six non-ordinary cases. V300 includes only the four resolved cases and leaves the two unresolved cases excluded.

Resolved fixed-prefix owners:

```text
R234  raw patch starts 0x68A2F6 inside owner 0x68A2F2
      complete owner = `1000石あたり何貫か`

R235  raw patch starts 0x69DD51 inside owner 0x69DD4F
      complete owner = `10頭で何貫か`
```

Resolved split-diff owners:

```text
R485 + R486 -> owner 0x6A0570
`主人公の能力を入力してください`

R642 + R643 -> owner 0x69F2E1
`移動先または攻撃相手を選んでください`
```

The companion records are PC diff segmentation, not runtime fragment composition. The complete Switch object remains one semantic output object, therefore these rows remain `STATIC_COMPLETE`.

Excluded evidence waits:

```text
R2884
R2885
```

Their PC replacement removes an original terminator without proving the Switch consumer's length contract. They remain outside V300.

## 6. Consumer topology

V299 established a reusable ordinary-inline consumer route:

```text
.rela.dyn R_AARCH64_RELATIVE (0x403)
 -> r_offset runtime source/consumer slot
 -> r_addend Switch physical text owner
```

V300 applies that already-proven route to the 47 selected static owners.

Result:

```text
47/47 owners have exactly one RELA consumer slot
0 owners have shared RELA slots
0 owners lack a RELA slot
```

This closes the materialization caller/consumer metadata for these selected rows without claiming that every low-level formatting/display function callsite has been individually enumerated.

## 7. Row list

| Candidate | PC source | Switch owner | RELA slot | KO/cap | JP object | PC Korean payload |
|---|---|---:|---:|---:|---|---|
| SEL-CAND-000093 | R2541 | 0x682B0F | 0x9C0998 | 18/25 | 軍団長を決定してください | 군단장을 정하세요 |
| SEL-CAND-000094 | R2546 | 0x682B28 | 0x9C09C0 | 19/25 | 軍馬数を決定してください | 군마 수를 정하세요 |
| SEL-CAND-000095 | R641 | 0x682D71 | 0x9C3870 | 22/23 | どの命令を出しますか？ | 어느 명령을 내립니까? |
| SEL-CAND-000096 | R2800 | 0x683F61 | 0x9C1200 | 17/21 | 何日間瞑想しますか？ | 며칠 명상할까요? |
| SEL-CAND-000097 | R552 | 0x6840FF | 0x9C3570 | 20/23 | 寿命を入力してください | 수명을 입력하십시오 |
| SEL-CAND-000098 | R2886 | 0x6853A9 | 0x9C14B0 | 15/15 | ２２以上は負け | 22 이상은 패배 |
| SEL-CAND-000099 | R553 | 0x685502 | 0x9C3578 | 20/23 | 野心を入力してください | 야심을 입력하십시오 |
| SEL-CAND-000100 | R563 | 0x686A6F | 0x9C35C8 | 22/25 | 新武将を設定してください | 신장수를 설정하십시오 |
| SEL-CAND-000101 | R825 | 0x686ACC | 0x9C3EE0 | 33/36 | 列伝を104文字以内で入力してください | 열전을 104자 이내로 입력하십시오 |
| SEL-CAND-000102 | R2856 | 0x689022 | 0x9C13C0 | 15/19 | 複数の弾を操作可能 | 다중 탄환 조작 |
| SEL-CAND-000103 | R234 | 0x68A2F2 | 0x9C29C8 | 14/19 | 1000石あたり何貫か | 1000석당 관수 |
| SEL-CAND-000104 | R550 | 0x68A37D | 0x9C3560 | 20/23 | 生年を入力してください | 생년을 입력하십시오 |
| SEL-CAND-000105 | R2799 | 0x68B737 | 0x9C11F8 | 15/19 | いくらにしますか？ | 얼마로 할까요? |
| SEL-CAND-000106 | R2540 | 0x68DCEA | 0x9C0990 | 25/31 | 出陣する軍団を編成してください | 출진할 군단을 편성하세요 |
| SEL-CAND-000107 | R2798 | 0x68DDCE | 0x9C11F0 | 17/21 | 何日間待機しますか？ | 며칠 대기할까요? |
| SEL-CAND-000108 | R415 | 0x68DEE5 | 0x9C2FE0 | 19/23 | いくらお布施しますか？ | 얼마를 보시합니까? |
| SEL-CAND-000109 | R644 | 0x6904B6 | 0x9C3880 | 22/23 | 移動先を選んでください | 이동처를 선택하십시오 |
| SEL-CAND-000110 | R647 | 0x6904CD | 0x9C3898 | 23/33 | （右クリックでメニューを閉じる） | (우클릭으로 메뉴 닫기) |
| SEL-CAND-000111 | R2801 | 0x691890 | 0x9C1208 | 17/21 | 何日間採集しますか？ | 며칠 채집할까요? |
| SEL-CAND-000112 | R2943 | 0x6918B8 | 0x9C1680 | 15/15 | 計算順に注意！ | 계산순서 주의! |
| SEL-CAND-000113 | R2550 | 0x692C20 | 0x9C09E0 | 21/27 | 大型船数を決定してください | 대형선 수를 정하세요 |
| SEL-CAND-000114 | R2549 | 0x693F50 | 0x9C09D8 | 19/25 | 関船数を決定してください | 관선 수를 정하세요 |
| SEL-CAND-000115 | R3034 | 0x693FDA | 0x9C19F8 | 19/21 | いくら寄付しますか？ | 얼마를 기부할까요? |
| SEL-CAND-000116 | R487 | 0x6940BB | 0x9C3278 | 38/41 | ゲームに登場させる新武将を選んでください | 게임에 등장시킬 신장수를 선택하십시오 |
| SEL-CAND-000117 | R739 | 0x6963B6 | 0x9C3BE0 | 35/41 | 作成した新武将をゲームに登場させますか？ | 만든 신장수를 게임에 등장시킵니까? |
| SEL-CAND-000118 | R2547 | 0x6976D9 | 0x9C09C8 | 19/25 | 鉄砲数を決定してください | 조총 수를 정하세요 |
| SEL-CAND-000119 | R2797 | 0x698B22 | 0x9C11E8 | 19/21 | いくら支払いますか？ | 얼마를 지불할까요? |
| SEL-CAND-000120 | R2944 | 0x698B55 | 0x9C1688 | 14/19 | 左から順に計算する | 왼쪽부터 계산 |
| SEL-CAND-000121 | R958 | 0x698CC5 | 0x9C4370 | 20/23 | 環境設定をしてください | 환경설정을 해주세요 |
| SEL-CAND-000122 | R3013 | 0x699E8E | 0x9C18B8 | 15/19 | いくら渡しますか？ | 얼마를 줄까요? |
| SEL-CAND-000123 | R489 | 0x69B6A1 | 0x9C3288 | 22/25 | シナリオを選んでください | 시나리오를 선택하세요 |
| SEL-CAND-000124 | R235 | 0x69DD4F | 0x9C29D0 | 12/13 | 10頭で何貫か | 10필당 관수 |
| SEL-CAND-000125 | R640 | 0x69DE37 | 0x9C3868 | 22/27 | どの備に命令を出しますか？ | 어느 진에 명령합니까? |
| SEL-CAND-000126 | R645 | 0x69DE52 | 0x9C3888 | 24/25 | 攻撃相手を選んでください | 공격상대를 선택하십시오 |
| SEL-CAND-000127 | R646 | 0x69DE6B | 0x9C3890 | 23/31 | （右クリックでメニューを開く） | (우클릭으로 메뉴 열기) |
| SEL-CAND-000128 | R642,R643 | 0x69F2E1 | 0x9C3878 | 33/37 | 移動先または攻撃相手を選んでください | 이동처나 공격상대를 선택하십시오 |
| SEL-CAND-000129 | R485,R486 | 0x6A0570 | 0x9C3270 | 27/31 | 主人公の能力を入力してください | 주인공 능력을 입력하십시오 |
| SEL-CAND-000130 | R488 | 0x6A058F | 0x9C3280 | 22/23 | 主人公を選んでください | 주인공을 선택하십시오 |
| SEL-CAND-000131 | R2975 | 0x6A2917 | 0x9C1788 | 14/19 | いくつ買いますか？ | 몇 개 살까요? |
| SEL-CAND-000132 | R2545 | 0x6A3D09 | 0x9C09B8 | 19/25 | 兵士数を決定してください | 병사 수를 정하세요 |
| SEL-CAND-000133 | R2548 | 0x6A3D22 | 0x9C09D0 | 19/25 | 大筒数を決定してください | 대포 수를 정하세요 |
| SEL-CAND-000134 | R2551 | 0x6A3D3B | 0x9C09E8 | 21/27 | 鉄甲船数を決定してください | 철갑선 수를 정하세요 |
| SEL-CAND-000135 | R2945 | 0x6A3DD1 | 0x9C1690 | 14/17 | ここから計算する | 여기부터 계산 |
| SEL-CAND-000136 | R2981 | 0x6A52D2 | 0x9C17B8 | 10/15 | 外に出ますか？ | 나갈까요? |
| SEL-CAND-000137 | R2542 | 0x6A8B7E | 0x9C09A0 | 28/37 | 備大将を決定してください（最大４人） | 부대장을 정하세요(최대 4명) |
| SEL-CAND-000138 | R2544 | 0x6A8BA3 | 0x9C09B0 | 18/25 | 軍資金を決定してください | 군자금을 정하세요 |
| SEL-CAND-000139 | R1357 | 0x6A8E7C | 0x9C5A40 | 23/29 | 人物の能力を変更してください | 인물 능력을 변경하세요 |

## 8. Claim boundary

V296 remains binding:

```text
target resolved != WRITE_SAFE
WRITE_SAFE != INCLUDE_KO
INCLUDE_KO != implementation/runtime PASS
build/package PASS != gameplay PASS
```

V300 is a candidate/classification materialization only.

It does not imply:

```text
builder PASS
IPS PASS
font/render PASS
layout PASS
runtime PASS
hardware/gameplay PASS
```

## 9. Inline R1 state after V300

```text
INLINE R1 source-role total            141

V298 ending-help                        39  INCLUDE_KO materialized
ordinary inline                        102
  V300 static resolved                  47  INCLUDE_KO materialized
  static unresolved                      2  R2884 / R2885
  V299 numeric VARIABLE_INSERT          53  INCLUDE_KO materialized
```

Therefore:

```text
materialized R1 INCLUDE_KO = 139
remaining inline R1 unresolved = 2
```

The two unresolved rows remain evidence waits. They may be revisited when later consumer-route work provides the required semantics; V300 does not force a dedicated trace now.

## 10. Next routing

After V300, do not reopen the 139 materialized inline rows merely because work moves to another container.

The two unresolved inline rows remain deferred evidence waits.

The next product-facing read-only work should move to another selective content family/container. The recommended next focus is TAI5MSG selective message classification, preserving the V295 rule that container membership never determines usage/mechanism by itself.

No next implementation/build step is authorized by this document.

## 11. Repository write boundary

Repository writes remain restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
