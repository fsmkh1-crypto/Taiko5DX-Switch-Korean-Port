# RUNTIME TEST RESULTS

Observed Eden Android behavior for Taiko5DX Switch Korean-port development builds.

These observations are empirical evidence. They do not by themselves certify an inline candidate as SAFE.

## 2026-09-10

### Baseline / integrated tests

| Variant | Inline set | Other Korean-port components | Result |
|---|---:|---|---|
| Add-on disabled | 0 | none | Game boots/runs normally |
| v0.2a integrated | 5,519 selected patterns | 207 RomFS replacements + Korean font + page mapper | Freeze |
| v0.2b NO-INLINE | 0 | 207 RomFS replacements + Korean font + page mapper | Boots; Korean title `태합입지전 V DX` is displayed |
| v0.2c | 5,518 selected patterns | same baseline components; one suspicious inline removed | Still fails/freezes |

### Address-ordered half split

The remaining 5,518 inline patterns were split by Switch offset order only for diagnosis. This split is **not** a safety classifier.

| Group | Count | Approx. Switch offset range | Result |
|---|---:|---|---|
| A | 2,759 | `0x682AE5..0x72028D` | Freeze |
| B | 2,759 | `0x72034F..0x783F9A` | Korean title appears; pressing a button causes forced exit/crash |

### Interpretation

- The NO-INLINE baseline demonstrates that the current RomFS replacement set, Korean font, and page mapper can at least boot and render the Korean title together.
- Inline patches are the differentiating failure source in the current builds.
- Failure exists in both address halves, so a single-bad-record assumption is invalid.
- A/B passing/failing behavior cannot prove that other records in either half are safe; later-game failures may remain latent.
- Future inline inclusion must follow `docs/INLINE_VALIDATION_POLICY.md` rather than exact-unique matching or binary-split survival.
