# RUNTIME TEST RESULTS

Observed Eden Android behavior for Taiko5DX Switch Korean-port development builds.

These observations are empirical evidence. They do not by themselves certify an inline candidate as SAFE.

## 2026-09-10

### Baseline / integrated tests

| Variant | Inline set | Other Korean-port components | Result |
|---|---:|---|---|
| Add-on disabled | 0 | none | Game boots/runs normally |
| v0.2a integrated | 5,519 selected patterns | 207 RomFS replacements + Korean font + IPS records emitted with the old offset convention | Freeze |
| v0.2b NO-INLINE | 0 | 207 RomFS replacements + Korean font + one page-mapper IPS record emitted with the old offset convention | Boots; Korean title `태합입지전 V DX` is displayed |
| v0.2c | 5,518 selected patterns | same old-offset IPS convention | Still fails/freezes |
| P0N v0.2f | 5,519 intended no-op records | same RomFS/font baseline + page mapper; **old IPS offsets** | Freeze |

### Address-ordered half split

The remaining 5,518 inline patterns were split by Switch offset order only for diagnosis. These builds also used the old IPS-offset convention and therefore cannot be used to infer candidate-level safety or multi-fault distribution.

| Group | Count | Approx. mapped Switch offset range | Result |
|---|---:|---|---|
| A | 2,759 | `0x682AE5..0x72028D` | Freeze |
| B | 2,759 | `0x72034F..0x783F9A` | Korean title appears; pressing a button causes forced exit/crash |

### Critical IPS-offset correction discovered after P0N failure

Inspection of Eden/Yuzu-derived NSO loading shows that ExeFS IPS patches are applied to an artificial patch image consisting of:

```text
0x000000..0x0000FF  NSOHeader (0x100 bytes)
0x000100..          decompressed mapped NSO image
```

Eden's NSO loader copies the decompressed `codeset.memory` after `sizeof(NSOHeader)`, and `NSOHeader` is statically `0x100` bytes. Therefore a mapped flat-image offset `X` must be emitted to classic IPS as **`X + 0x100`**.

All development IPS builds through P0N v0.2f emitted mapped offsets directly without the required `+0x100`. Consequently:

- the P0N records were **not true no-ops in Eden** even though they round-tripped against our flat-image model;
- a record intended for flat offset `X` actually overwrote flat offset `X - 0x100` in Eden;
- the page-mapper record intended for flat `0x44650C` was emitted at IPS `0x44650C`, which targets flat `0x44640C`; the correct Eden IPS offset is `0x44660C`;
- prior v0.2a/v0.2c/A/B crashes do **not** prove that the selected inline candidates themselves were wrong, because they were never applied at the intended addresses;
- v0.2b boot/Korean-title observation remains a real runtime fact, but it does **not** validate the intended page-mapper rewrite because that IPS record was also shifted by `-0x100` at application time.

This supersedes the earlier interpretation that the P0N failure demonstrated a large-record-count or semantic-inline failure.

### Next control

`P0N2 v0.2g` repeats the same 5,519 no-op control but emits every IPS offset as mapped offset `+0x100`. Only this corrected build can answer whether 5,519 no-op IPS records themselves are accepted by the target Eden runtime.

### Current interpretation

- The dominant confirmed implementation defect is the missing `+0x100` Eden/NSO-header IPS offset shift.
- Previous IPS-bearing runtime results remain useful historical observations but must not be used as candidate-safety evidence.
- Semantic inline validation is still required for release quality, but the old runtime failures cannot be cited as proof that the 5,519 mappings were inherently unsafe.
- Future IPS generators must validate both mapped offsets and emitted Eden IPS offsets separately.
