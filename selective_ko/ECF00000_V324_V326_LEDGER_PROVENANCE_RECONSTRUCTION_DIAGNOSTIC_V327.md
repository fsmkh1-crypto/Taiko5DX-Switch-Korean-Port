# ECF00000 V324/V326 LEDGER PROVENANCE RECONSTRUCTION DIAGNOSTIC — V327

Date: 2026-09-19 (KST)

```text
validation_id   V327
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_DIAGNOSTIC_CHECKPOINT
parent          c52ecfc948a09c19bfe984cab8dc2830870b252f / V326
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

## 1. Canonical aggregates preserved

V324/V325/V326 aggregate claims are not superseded:

```text
physical targets  4,444
messages          4,193
choices             251
Korean targets    4,238
INCLUDE_KO        4,123
UNRESOLVED          115
```

V327 changes only the provenance/materialization state: exact row membership for those aggregates is not yet reconstructed from persisted artifacts.

## 2. Eight-chunk reconstruction result

All 782 entrypoints were covered in eight bounded chunks and all 782 reached normal NUL under the simple outer walker.

After global physical-offset dedup:

```text
OUTER_PATH_SUBSET
physical targets  2,817
messages          2,569
choices             248
Korean targets    2,616
INCLUDE_KO        2,504
UNRESOLVED          112
```

This subset is diagnostic only. It is not the canonical 4,444 ledger and must not be used as serializer input.

## 3. Gate mismatch

```text
metric             canonical  outer subset  deficit
physical targets      4,444        2,817      1,627
messages              4,193        2,569      1,624
choices                 251          248          3
Korean targets        4,238        2,616      1,622
INCLUDE_KO            4,123        2,504      1,619
UNRESOLVED              115          112          3
```

All six reconstruction gates fail.

The outer subset reproducing UNRESOLVED=112 matches the previously recoverable old outer-path subset and strongly indicates the same incomplete traversal population.

## 4. Root-cause interpretation

The attempted walker follows only:

```text
current command
-> handler returned length
-> p += length
-> next outer command
```

This does not reproduce V324's 4,444-target census. The missing population is therefore associated with structural traversal not represented by this simple outer path, most likely nested / branch / internal command regions inside length-bearing commands.

The exact child traversal rule is not yet proven.

## 5. Do-not-repeat

Canonical failed approach:

> A pure `p += handler_length` outer execution-line walker over all 782 entrypoints cannot reconstruct the V324 4,444 physical-target census.

Also rejected:

- treating 2,817 rows as the canonical ledger;
- treating 112 unresolved rows as the full V326 115;
- blaming chunk splitting or cross-chunk dedup for the deficit;
- guessing the missing three unresolved rows;
- superseding V324/V326 aggregates solely because this weaker traversal disagrees;
- raw scanning bytes merely to force counts to 4,444.

## 6. Artifact preservation

Large artifacts are stored in Drive:

```text
Google Drive/GPT/태합입지전/ECF00000_V327_LEDGER_DIAGNOSTIC/
ECF00000_V327_LEDGER_DIAGNOSTIC.zip

folder id  1HipzsNVqrh-WMNlzuKkV6uUmcVt0nyrU
file id    1wo1nfMND8D3KRtXnyG_gRi69grcQmMl8
size       500,141 bytes
zip sha256 ab993eeff32a147cb64debdccd0b99cf25e859f25801603ffe4227dc2cca59d2

embedded manifest sha256
3c114c244c2e521eaff3d42159da43cfdcb4c5d3e4f1f554306de5c8ed4b6465
```

The ZIP contains chunk01..chunk08 ledgers, the combined outer-path ledger, and a manifest with per-file identities.

## 7. Impact boundary

Unchanged:

- V324 carrier/interpreter facts;
- V325 Mapping/font/glyph closure;
- V326 aggregate admission counts;
- identity/fixed-particle policies;
- TAI5MSG/B24;
- SNR.

Blocked until exact provenance closes:

- exact V326 4,123 serializer-input membership;
- exact 115-row semantic adjacency audit;
- EVENT selective serializer implementation based on row membership.

## 8. Exact next scope

After a fresh explicit execution signal:

`ECF00000_V324_NESTED_COMMAND_TRAVERSAL_RULE_RECOVERY_READ_ONLY`

Only a small representative set of length-bearing/branch-containing commands may be inspected first. Recover and prove the nested/internal traversal rule before any full 782-entrypoint rerun.

No payload rewrite, serializer implementation, build/package/IPS, unrelated EVENT work, or SNR work is authorized by V327.
