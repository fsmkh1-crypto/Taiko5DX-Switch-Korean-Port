# TAI5MSG FAST SOURCE CACHE AND TOOLING — V314

Date: 2026-09-18 (KST)  
Status: CLOSED / DRIVE ROUNDTRIP VERIFIED / CACHE-ONLY INSPECTION TOOLING MATERIALIZED / NO PRODUCT PAYLOAD CHANGE
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V314`
Parent canonical HEAD: `168f44588b43a588fbaf672ac1dea07db1b739cb` / V313

## 1. Purpose

V314 removes a recurring operational bottleneck: reassembling and re-extracting the 170+ MB PC v1.02 patcher merely to inspect already-verified TAI5MSG or Mapping data.

This stage creates a reusable source cache and cache-only inspection path. It does not repair B24, change translations, modify the selective serializer, build a package, or alter runtime payloads.

## 2. Canonical source identities

```text
PC original TAI5MSG
size    1,810,889
sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f
Drive   1E6Rq2P4E3DSL9Uk-t1FvoOh6Jx-oFTSJ

PC Korean v1.02 TAI5MSG
size    2,134,366
sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
Drive   1KRueqxUq4f0UdyUWOgfKcch26FOsD5jd

PC dinput8.dll
size    836,096
sha256  ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7

T5K RT_RCDATA/101
size    613,685
sha256  5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29
mapping entries 10,036
```

The PC-KO TAI5MSG was extracted once from the official v1.02 patcher and reproduced the already canonical PC-KO SHA exactly.

## 3. Drive cache

Folder:

```text
Google Drive/GPT/태합입지전/TAI5MSG_FAST_CACHE_V314
folder id 1yn5JMyhLt3Nhjfw4fTPC7PVrAXKXVtyN
```

Files:

```text
TAI5MSG_JP_PC_KO_v1.02.DAT
  id      1KRueqxUq4f0UdyUWOgfKcch26FOsD5jd
  bytes   2,134,366
  sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090

MAPPING_10036_CACHE.json
  id      1jlkBuH3_DJLrSo5ljQRP-43NJmxgjWu4
  bytes   139,920
  sha256  429dccba3444caf9e63524908f3f00249504da56e60fe5249fb0f1ee0213146f
  entries 10,036

B24_SOURCE_CACHE.jsonl
  id      1wtctzo118PQvd31NL3u_t_lZK9766NcY
  bytes   312,317
  sha256  bf72cd3b13ff9523e605a752cf479d874e1ec347fbd298e26a707dc8872ab733
  rows    124 / B24:M221..M344
```

All three files were downloaded again after upload. Size and SHA-256 matched the pre-upload bytes exactly: `PASS_BYTE_IDENTICAL`.

No commercial game binary or complete PC patch payload is added to Git.

## 4. Git cache pointer and hot anchors

Machine-readable pointer:

`selective_ko/artifacts/tai5msg_fast_source_cache_v1/INDEX.json`

The full B24 cache stays on Drive. Git stores only three hot defect anchors, M227/M228/M229, in:

`selective_ko/artifacts/tai5msg_fast_source_cache_v1/B24_ANCHORS.jsonl`

This allows the most common B24 defect inspection without any Drive read while avoiding a large repository duplicate.

## 5. Inspection helper

`tools/tai5msg_inspect.py`

Default mode reads the Git anchor cache. Example:

```bash
python tools/tai5msg_inspect.py --locator B24:M229
```

For any B24 selected row M221..M344, materialize the exact Drive `B24_SOURCE_CACHE.jsonl` and pass:

```bash
python tools/tai5msg_inspect.py \
  --full-cache /path/to/B24_SOURCE_CACHE.jsonl \
  --range B24:M221..M344
```

The helper validates cache size and SHA from the Git index before consuming it. It never opens or reconstructs the PC patcher.

## 6. Generic correction preparation

V314 also adds:

```text
selective_ko/TAI5MSG_CORRECTION_OVERLAY_SCHEMA_V1.md
builder/tai5msg_corrections.py
```

Supported operations are `EXACT_REPLACE_MESSAGE` and `DELETE_EXACT_BYTE` with exact source/target guards.

This is infrastructure only. Existing V304 production serializer behavior remains untouched.

## 7. Validation

Local bounded tests:

```text
Git anchor cache integrity + M229 semantic anchor PASS
EXACT_REPLACE_MESSAGE synthetic contract           PASS
DELETE_EXACT_BYTE synthetic contract                PASS
source guard rejection                              PASS
--------------------------------------------------------
4 / 4 PASS
```

Drive roundtrip:

```text
PC-KO TAI5MSG       PASS_BYTE_IDENTICAL
Mapping cache       PASS_BYTE_IDENTICAL
B24 source cache    PASS_BYTE_IDENTICAL
```

## 8. 확정된 사실

1. The repeated PC-patcher extraction path is no longer required for B24 M221..M344 inspection while V314 source identities remain unchanged.
2. The canonical PC-KO TAI5MSG and actual Mapping 10,036 are now directly cached on Drive with exact hashes.
3. B24 selected 124 source pairs are cached with raw bytes, decoded text, message hashes, controls and terminator metadata.
4. M227/M228/M229 hot anchors are available directly from Git.
5. The generic correction utility is available without changing the verified selective serializer.

## 9. 유력한 가설

Applying the same cache-pointer pattern to other stable TAI5MSG ranges will reduce future Drive/payload extraction latency when those ranges become active scopes.

This is an operational expectation, not a gameplay claim.

## 10. 미확정 사항

- No claim is made that every future content family should use the same cache shape.
- V304 has not yet been migrated to the generic correction module.
- The B24 semantic/layout audit and repairs remain separate product work.

## 11. 기각된 가설

```text
The entire v1.02 patcher must be reconstructed for each B24 lookup       REJECTED
A second copy of full commercial TAI5MSG binaries must be committed Git REJECTED
Existing selective serializer must be refactored to gain lookup speed   REJECTED
Operational cache identity can replace canonical source identity        REJECTED
```

## 12. 관련 영향 범위

Changed scope is operational/tooling only:

```text
Drive derived source cache
Git cache pointer + 3 hot anchors
cache-only inspection helper
generic future correction schema/utility
tests and resume state
```

Unchanged:

```text
V303 membership 3,179
V304 effective corrections 2
serializer output SHA from V309
V312 package bytes
ExeFS IPS / font / Mapping runtime integration
B24 payloads in any shipped/test package
```

## 13. 수정 제안 / operating rule

For future TAI5MSG work:

1. read the V314 cache index first;
2. use Git hot anchors when applicable;
3. otherwise fetch the exact cached Drive file by recorded ID and guard its hash;
4. do not reassemble/re-extract the PC patcher merely to reproduce cached data;
5. re-extract only when source identity changes, cache integrity fails, or the required source range is not represented;
6. use the generic correction schema for new exact-message correction overlays, but migrate existing production paths only under a separate explicit implementation scope.

The product next scope remains the B24 semantic/layout work already identified by V313; V314 changes only how its evidence is accessed.

## 14. Repository write boundary

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
