# V360 EVENT + V357 TAI5MSG Eden diagnostic package materialization — V361

Date: 2026-09-21 (KST)

```text
validation_id   V361
track           SWITCH_SELECTIVE_KOREANIZATION
parent          e036b3e49daf6b7dddd7f99fe8fee32257199737 / V360
scope_kind      DIAGNOSTIC_PACKAGE_MATERIALIZATION
package         MATERIALIZED
drive_roundtrip PASS_BYTE_IDENTICAL
Eden/runtime    NOT RUN
hardware        NOT RUN
```

## 1. Scope

V361 combines exactly the completed V360 EVENT payload and V357 TAI5MSG payload with the already
verified V358 IPS/font route. It is the first diagnostic package in this sequence that contains both
the selective EVENT carrier and the percent-macro TAI5MSG carrier.

V361 does not add or modify ordinary non-B24 584 reflow, inline 139, SNR, font, IPS, or any unrelated
translation/content family.

## 2. Exact package

`Taiko5DX_KR_SELECTIVE_V360_EVENT_V357_TAI5MSG_EDEN_DIAG.zip`

```text
bytes     3,638,158
sha256    bc62aa0c8e25b7d7338eb3bd47468d10335636a0c6385c9296e6814a48cfd2f7
entries   5
```

Strict allowlist:

```text
Taiko5DX_KR_SELECTIVE/SELECTIVE_PACKAGE_INFO.json
Taiko5DX_KR_SELECTIVE/exefs/D9120950C258610A746F4A31CE3A3B376DE393D9.ips
Taiko5DX_KR_SELECTIVE/romfs/EVENT/ECF00000.TS5
Taiko5DX_KR_SELECTIVE/romfs/FONT/FONT_JPN.G1T
Taiko5DX_KR_SELECTIVE/romfs/TAI5MSG_JP.DAT
```

No extra entry is present.

## 3. Component identities

```text
SELECTIVE_PACKAGE_INFO.json
  bytes   1,957
  sha256  2394fdce591b0643c0805d991a7d57798f9b88f52a0e24e00b9abda308ba48df

ExeFS integrated IPS
  bytes   2,742
  sha256  6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4

V360 ECF00000.TS5
  bytes   1,109,440
  sha256  4b31d771c9bb3736d7cbc5fc95c1a4e4c54a55e43f38606227cca32ecb22045d

Korean FONT_JPN.G1T
  bytes   16,779,036
  sha256  c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932

V357 TAI5MSG_JP.DAT
  bytes   1,840,329
  sha256  ad91776d47c3170573bed063dd6677716833e3a138be27474373ef5d2782e794
```

IPS, font and TAI5MSG are byte-identical to V358. The newly added product carrier is exact V360
`romfs/EVENT/ECF00000.TS5`.

## 4. Deterministic packaging

The inherited V358 packaging contract is preserved:

```text
entry order       lexicographically stable
timestamp         2026-09-18 00:00:00
Unix mode         0644
compression       DEFLATE level 9
top-level root    Taiko5DX_KR_SELECTIVE/
```

Two independent builds produced the same byte stream:

`DETERMINISTIC_REBUILD = PASS_BYTE_IDENTICAL`

The unpack/re-read allowlist and every component SHA matched the source identities above.

## 5. Drive archive and roundtrip

```text
folder ID   12yS6R9r045ZxfLzM4rytc8O2lBdfkc8N
ZIP ID      18Mux9kvYU5Qmx8ASuI7MELTAnTDuPE5p
report ID   1qepmjOUpTOcaQrdxoPdAIgmI7KJus0xm
```

ZIP roundtrip:

```text
local       3,638,158 / bc62aa0c8e25b7d7338eb3bd47468d10335636a0c6385c9296e6814a48cfd2f7
Drive back  3,638,158 / bc62aa0c8e25b7d7338eb3bd47468d10335636a0c6385c9296e6814a48cfd2f7
identity    PASS_BYTE_IDENTICAL
```

Report roundtrip:

```text
bytes       1,899
sha256      36c113bf25cd5bb5d69d0f5d49177a824bc5ddfb63cf9f30c6e39f63a2366608
identity    PASS_BYTE_IDENTICAL
```

Git remains canonical; Drive stores the large runtime package and transport report.

## 6. Expected runtime interpretation

V358 showed Korean description bodies but Japanese ordinary dialogue because EVENT was absent.
V361 now includes the completed V360 EVENT payload in addition to the exact same V357 TAI5MSG.

Therefore the isolated runtime expectation for V361 is:

```text
ordinary EVENT dialogue       should now use selective Korean EVENT payloads
%15/%21/%2A cross-carrier     EVENT V360 + B0 roots V357 are both present
identity/name/place fields    remain JP under binding policy
known description wrapping    may still be poor where non-B24 584 reflow is not implemented
scenario synopsis/SNR         no new claim; SNR is still absent
```

Runtime behavior is not a V361 PASS condition and remains unverified until Eden execution.

## 7. Mandatory next-runtime checks

Use this exact ZIP SHA only:

`bc62aa0c8e25b7d7338eb3bd47468d10335636a0c6385c9296e6814a48cfd2f7`

At minimum:

1. confirm boot/title and normal selected-Korean route;
2. revisit an ordinary dialogue screen that was Japanese under V358 and verify whether its body is now Korean;
3. preserve Japanese dedicated identity/name/place fields;
4. capture any crash, control-code leak, malformed dialogue, or obvious cross-carrier suffix failure;
5. do not fail V361 merely because the known ordinary non-B24 reflow remains visually poor;
6. do not treat the scenario synopsis as an EVENT failure without an exact carrier binding.

## 8. 확정된 사실

- exact V360 EVENT is present at `romfs/EVENT/ECF00000.TS5`;
- exact V357 TAI5MSG is present at `romfs/TAI5MSG_JP.DAT`;
- IPS/font/TAI5MSG are unchanged from V358;
- strict package allowlist is five files;
- deterministic independent rebuild is byte-identical;
- Drive ZIP/report roundtrips are byte-identical;
- Eden/runtime was not executed.

## 9. 유력한 가설

The Japanese ordinary-dialogue symptom observed with V358 should be removed for EVENT-owned dialogue
under V361 because the previously absent EVENT carrier is now present.

## 10. 미확정 사항

- actual Eden dialogue output under V361;
- exact runtime behavior of the three cross-carrier suffix rows;
- non-B24 584 reflow implementation;
- inline 139 implementation;
- exact SNR ownership of the Japanese scenario synopsis.

## 11. 기각된 가설 / do-not-repeat

- attribute V358 Japanese dialogue to a font or Mapping failure — REJECTED;
- test V360 EVENT without exact V357 TAI5MSG roots — REJECTED;
- mix ordinary non-B24 584 reflow into this EVENT diagnostic package — REJECTED;
- include inline 139 merely because its rows are classified INCLUDE_KO — REJECTED;
- include or guess SNR content in this package — REJECTED;
- treat deterministic packaging as runtime PASS — REJECTED.

## 12. 관련 영향 범위

Changed relative to V358:

- package metadata;
- added `romfs/EVENT/ECF00000.TS5`.

Unchanged:

- V357 TAI5MSG bytes;
- IPS bytes;
- font bytes;
- non-B24 584 reflow state;
- inline 139 state;
- SNR state.

## 13. 수정 제안 / exact next scope

`ECF00000_V361_EVENT_TAI5MSG_EDEN_RUNTIME_VALIDATION`

The next scope requires user-side Eden execution of the exact V361 ZIP. No new implementation should
be mixed into that runtime check.
