# F1 STATIC WRITE AUTHORIZATION CLOSURE

Date: 2026-09-12  
Canonical base HEAD: `b6c106a675c90b2e958632bf16547ff41200c1f1`  
Scope: row-level provenance and static write authorization for the 158 rows previously classified by V089 as `TARGET_RESOLVED_WRITE_SAFE_STATIC`. No builder, IPS, runtime artifact, game-file modification, yomi work, shared-owner closure, padding reconstruction, F2-F5, CN sequence, or UTF-16 work is included.

## 1. Result

The missing F1 row-level provenance has been closed deterministically.

The historical F1 selector was reconstructed from the canonical Stage-1 report bundle and canonical Switch `main` using the original rule, not a new selector:

- PC search scope: `R1-R3250`;
- logical object = bytes before the first PC NUL;
- reject a candidate row if any nonzero byte occurs after its first PC NUL;
- anchor length >= 8 bytes;
- anchor logical value occurs exactly once in PC `R1-R3250` and exactly once among the 3,803 JP logical localization entries;
- candidate correspondence is `JP localization ID = PC record number + segment delta`;
- search segments are maximal consecutive correspondence runs of at least five rows;
- each search segment requires at least two anchors with the same delta;
- no candidate gap or delta reset is crossed;
- historical mapping is bounded from the first accepted anchor through the last accepted anchor;
- canonical V088 promotion additionally requires that final bounded interval itself contain at least five rows.

The replay reproduces all prior F1 measurements exactly:

```text
search segments                         142
anchor-bounded mapped rows            1,402
Stage-2 residual rows in those bounds   278
accepted final segments                 112
accepted mapped rows                  1,311
accepted residual rows                  262
F1_RULE_REJECTED                         16

historical full-window rows              197
historical padding-mismatch rows           81
accepted full-window rows                187
accepted padding-reconstruction rows      75
capacity/NUL failures                      4
shared-owner blockers                     25
static write-authorized rows             158
```

The exact 16 rejected residual source rows also reproduce V088:

`R284, R286, R821, R1275, R1985, R1986, R1987, R2014, R2015, R2161, R2253, R2425, R2426, R2480, R3181, R3182`.

## 2. Canonical inputs and deterministic replay

Inputs:

- Switch `main` SHA-256: `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- Build ID (canonical project identity, 20 bytes): `D9120950C258610A746F4A31CE3A3B376DE393D9`
- NSO header Build-ID field (`0x40:0x60`, 32 bytes): the 20-byte identity above followed by 12 zero padding bytes. The existing replay tool intentionally validates the entire 32-byte field. In `F1_STATIC_WRITE_AUTHORIZATION_SUMMARY.json` schema V1, the legacy key `canonical_build_id` stores this full serialized 32-byte field; do not reinterpret the trailing zero padding as part of the canonical project Build ID.
- Stage-1 `source_ledger.jsonl`: `0ef81c629adb2e348a72922efcb030908c76fb3cff964804948bf84cd7fd1570`
- Stage-1 `exceptions.jsonl`: `10b13fe7156225109d86f8d0707dd385d3c24c66dcbe590ae56425e1dc936257`
- Stage-1 `localization_language_inventory.json`: `d7b90f7f7f1e43c54b87d97524b14b1582f390aa8a4672e25c2c48d2f9fac550`
- Stage-2 block definitions: V082 / `docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md`

Replay tool:

- `tools/f1_static_authorization.py`

The tool is read-only with respect to canonical inputs and fails closed if the canonical hashes, Build ID, Stage-2 residual count, F1 segment counts, rejected-row set, capacity-fail set, shared-owner count, overlap proofs, or final authorization count do not reproduce.

Two consecutive local replays produced byte-identical outputs.

Output hashes:

- manifest content (uncompressed JSONL): `c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff`
- canonical `.jsonl.gz` file: `8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68`
- summary: `e77662199707ab5597d2e387fe76d5eda5fe12dc0d211bf40333e0fa6563d140`
- ordered authorized `source_id` list SHA-256: `87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e`

## 3. Row-level authorization result

Manifest:

- `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz`
- rows: 158
- unique PC source IDs: 158
- unique localization IDs: 158
- unique physical target objects: 158
- unique authorization action IDs: 158

Every manifest row records:

- PC source ID / record / RVA;
- original and replacement bytes;
- F1 search run, bounded interval, delta, and anchor provenance;
- Switch localization ID;
- JP source slot and runtime destination-cell identity;
- static rodata target object and write interval;
- language ownership;
- physical logical-owner cardinality;
- exact original-byte guard;
- terminating-NUL preservation mode and offset;
- F1 and Stage-2 overlap state;
- terminal-disposition overlay and stable authorization action ID;
- evidence scope and falsification condition.

All 158 satisfy:

```text
language domain                  JP_ONLY
storage                          STATIC_RODATA
PC-window -> Switch-object       1:1
physical localization owners     1
exact original-byte guard        PASS
terminating NUL preservation     PASS
unintended F1 overlap            0
Stage-2 target overlap           0
capacity failure                 0
shared-owner blocker             0
```

Terminator handling among the 158:

- existing NUL immediately after the unchanged-length write is preserved: 124;
- replacement contains its terminating NUL inside the guarded window: 34.

## 4. Authorization semantics

For these exact 158 rows only, the prior V089 audit classification is promoted to a row-level static authorization overlay:

```text
terminal_disposition_overlay = DIRECT_PORT
action_family                = F1_LOCALIZATION_STATIC_DIRECT
action_status                = STATIC_WRITE_AUTHORIZED_NOT_IMPLEMENTED
```

This means the 158 actions may be consumed by a later builder implementation without repeating the F1 selector analysis, provided all manifest guards and canonical identities still match.

This stage does not emit or modify a builder, IPS, ZIP, runtime diagnostic artifact, or game file. Implementation remains a separate stage requiring a fresh execution signal.

## 5. Excluded F1 populations remain unchanged

The following rows are not covered by this authorization:

- 4 capacity/NUL failures: `R2674`, `R2684`, `R2712`, `R3142`;
- 75 accepted padding-reconstruction rows;
- 25 accepted shared-owner blocker rows;
- 16 V088-rejected residual rows.

The 25 shared-owner rows remain outside this action set even where known PC replacements appear compatible. Their relevant logical-owner obligations must be closed separately before any shared physical overwrite is authorized.

## 6. Rejected shortcuts retained

This closure does not revive any previously rejected shortcut:

- raw occurrence uniqueness is not a selector;
- pooled rodata identity is not logical localization identity;
- pre-trim five-row search length is not sufficient for canonical F1 promotion;
- full original guard plus same replacement length is not sufficient without NUL/capacity proof;
- PC padding is not assumed reusable when Switch storage differs;
- shared objects are not globally overwritten without owner-obligation closure;
- target resolution and implementation remain separate stages.

## 7. Stopping point

F1 row-level provenance/static authorization closure is complete for the 158-row set.

No builder/IPS/runtime implementation was performed. A fresh user execution signal is required before consuming these actions in the builder or starting another F1/F2-F5 family.
