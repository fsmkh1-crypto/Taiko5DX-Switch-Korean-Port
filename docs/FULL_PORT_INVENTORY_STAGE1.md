# Full-port inventory/accounting validator — Stage 1

Date: 2026-09-11  
Status: CANONICAL DATA RUN COMPLETE / READ-ONLY

## 1. Scope

This stage executes the first read-only validator required by:

- `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`
- `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`

Implementation:

- `tools/full_port_inventory.py`

No builder transformation, IPS generation, game-file edit, or runtime diagnostic build was performed.

## 2. Canonical inputs

Switch `main`:

- Drive file ID `1nfnXSCmSHp0rP_bbDNSyhKCroKSTtTPQ`
- size `5,287,359`
- SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`

PC patch package:

- Drive file ID `1dYepodubrgFKIVByUtITkpclRJSGKbDE`
- size `170,498,865`
- ZIP SHA-256 `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`
- embedded `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- T5K121R SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`

All identity gates passed.

## 3. Source-denominator closure

The canonical package produced the exact accounting denominators:

```text
inline records            17,103 / 17,103
pointer records               56 / 56
mapping entries            10,036 / 10,036
descriptor containers          11 / 11
descriptor subpatches          14 / 14
helper semantic entries         2 / 2
RomFS data items              208 / 208
```

Additional PC runtime storage measurements reproduced from the canonical package:

- runtime helper blob: `158` bytes
- pointer replacement pool: `602` bytes
- pointer modes: mode 0 = `5`, mode 1 = `51`
- distinct mode-1 replacement targets: `47`

Stage 1 intentionally assigns no terminal port action. The generated source ledger therefore contains `27,430` rows with provisional `UNRESOLVED` disposition pending structural-rule promotion. This is a workflow state, not evidence that 27,430 independent manual fixes are required.

## 4. Switch structural inventory

Mapped-flat size:

- `0xA20430` = `10,617,904` bytes

RELA census:

- total entries: `40,410`
- `R_AARCH64_RELATIVE`: `40,023`
- type 257: `377`
- type 1025: `10`

This reproduces the canonical R0 relocation totals.

### Localization source tables

All three tables are complete with exactly one relative relocation per slot:

| domain | entries | relative slots present | unique source objects |
|---|---:|---:|---:|
| JP | 3,803 | 3,803 | 3,431 |
| CN | 3,803 | 3,803 | 2,933 |
| TW | 3,803 | 3,803 | 2,935 |

Missing/non-relative localization slots: `0`.
Duplicate relative relocations targeting the same source slot: `0`.

Distinct localization-source object ownership combinations:

```text
JP only       3,428
CN only       2,914
TW only       2,916
CN + TW          16
JP + CN + TW      3
```

These counts are language-domain inventory facts only. They do not establish which language-copy block is active on a given runtime route.

## 5. Inline discovery census

The 17,103 PC inline records contain `8,713` distinct original-byte patterns.

Raw Switch-candidate cardinality, counted per PC inline record with candidate lists capped at 64:

- zero raw candidates: `187`
- exactly one raw candidate: `6,053`
- more than one raw candidate: `10,863`
  - of these, `386` records reach the 64-candidate cap

The Stage-1 inline exception queue contains `11,050` rows:

```text
E_MULTI_CANDIDATE        10,747
E_OBJECT_UNKNOWN            187
E_REPLACEMENT_CONFLICT      116
```

Important interpretation:

- these are discovery exceptions, not final port failures;
- unique raw occurrence is not promoted to `DIRECT_PORT`;
- repeated/missing raw candidates must be reduced through structure/family rules before implementation.

Candidate-occurrence measurements across all inline rows:

```text
segment occurrences:
  STATIC_RODATA             111,017
  CODE                       10,954
  STATIC_DATA_OR_RELA_SLOT      786

exact localization-object starts:
  JP_ONLY                     4,885
  CN_ONLY                        12
  TW_ONLY                         2
  UNKNOWN                   117,858

known R0 place-table field starts:
  PLACE_TABLE_NAME              515
  PLACE_TABLE_YOMI              433
```

The candidate-occurrence counts are not source-record counts; repeated PC records/patterns may contribute repeated occurrences.

## 6. Preliminary invariant state

Stage-1 invariant state:

```text
PASS       1
UNKNOWN    1
NOT_RUN    9
```

- INV-8 target/input identity: `PASS`
- INV-6 mapping-consumer algorithm consistency: `UNKNOWN`
- all final action-dependent invariants remain `NOT_RUN` because no mutation/action set is authorized yet.

No input file was mutated. No IPS or game-file output was emitted.

## 7. Deterministic replay

The canonical inventory report set was emitted twice from the same inputs. All report hashes matched exactly.

First-run report hashes:

```text
SUMMARY.json                            d69e777102a785afb5079db8ca1c067556e4ae49c3235e22df2ef92e1627efbb
source_ledger.jsonl                     0ef81c629adb2e348a72922efcb030908c76fb3cff964804948bf84cd7fd1570
switch_inventory.json                   f481c437bc259fcef4c482560bb4b00f2c15364c96a462319576032c7a58a84f
exceptions.jsonl                        10b13fe7156225109d86f8d0707dd385d3c24c66dcbe590ae56425e1dc936257
invariants.json                         d826c50e3c22687b2be9a87edc815a3687d633641262e6e9748714706dce8959
localization_language_inventory.json    d7b90f7f7f1e43c54b87d97524b14b1582f390aa8a4672e25c2c48d2f9fac550
evidence_fanout.json                    a0f4238dcb33d301dae8b567b9f11df71d6186b941d37864fb82b4439d77925d
switch_action_proposals.jsonl           e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

The complete report bundle is retained in Google Drive `Test_Results`:

- file ID `1ezUGzY_eTnGBjs_YgUuTs19Sc0AeqPKT`
- name `canonical_inventory_stage1_reports_20260911.zip`

The uncompressed source ledger is approximately 38 MiB; the compressed report bundle is approximately 2 MiB. It is intentionally not committed to the repository.

## 8. Failed operational workaround retained

During the temporary local execution-backend outage, a one-off GitHub Actions download attempt was tested:

- workflow run `34604986859`
- result: failed before validator execution
- cause: canonical Drive files are private; `gdown` could not retrieve a public link

This rejects unauthenticated GitHub-runner download as a usable canonical-input transport. It says nothing about the validator or the game data. The one-off workflow is not part of the canonical validation design.

## 9. Review-claim boundary

Previously reported external measurements such as PC `.data` target counts remain non-canonical unless independently reproduced with the exact target-PC evidence required for that claim.

Two byte-window measurements can now be reproduced directly from T5K if needed, but they are not promoted by this Stage-1 report because the current objective is inventory/accounting closure rather than PC-window semantic classification.

## 10. Next-stage boundary

Stage 1 is complete.

The next useful stage is not implementation. It is corpus-wide promotion of verified structural rules over the candidate/exception populations, beginning with the highest-yield already-established structures and language/storage gates.

No builder patch, IPS, or runtime build is authorized by this report. A fresh user execution signal is required.