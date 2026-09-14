# Runtime byte copy / normalization route binding — progress

Date: 2026-09-15 (KST)
Scope: `RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_READ_ONLY`
Parent HEAD at analysis start: `f3ae1fafa359cce7b3e9b7ff2c290445a9a3ad18`

This is an intermediate canonical analysis checkpoint. It does not close the cause family, authorize implementation, create a diagnostic build, or add WRITE_SAFE authority.

## PC_PATCH_ORACLE_GATE

`PASS`.

The actual PC Korean patch package was re-opened only to establish provenance for this currently open family, not to revalidate previously VERIFIED stages. The embedded PC runtime/data oracle matched the already-canonical artifacts:

- `dinput8.dll` SHA-256: `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- embedded T5K resource SHA-256: `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- canonical inline source count reproduced: 17,103
- records containing standalone susceptible compact byte `0xA6..0xDF`: 2,057

Semantic obligation remains unchanged: preserve PC compact Korean one-byte values and ordinary two-byte values through upstream copy/normalization to the existing Switch consumer without unintended Japanese halfwidth transformation. The PC x86 helper mechanism itself is not a Switch implementation prescription.

## Confirmed facts

### 1. The 2,057-row risk upper bound is mostly already target-resolved

Intersecting the exact 2,057 PC source rows with the already-VERIFIED Stage2 affine blocks gives:

```text
Stage2 affine target-resolved risk rows   1,993
non-Stage2 risk rows                         64
TOTAL                                      2,057
```

Stage2 storage split:

```text
RODATA   1,953
DATA        40
TOTAL    1,993
```

Therefore the open route-binding problem must not be treated as 2,057 independent unknown target-location problems. For 1,993 rows, target identity follows the existing affine rule and exact original-byte guard.

### 2. Stage2 risk-row distribution by affine block

```text
R3251-R3875       32
R3876-R3996        6
R3997-R4188        2
R4189-R4417        8
R4418-R4569        2
R4570-R14429   1,686
R14430-R14541      1
R14551-R14683     23
R14737-R15462     90
R15463-R15613      0
R15614-R15619      1
R15620-R15679      2
R15680-R15719     10
R15720-R15927      4
R15928-R16229     66
R16230-R16284      4
R16285-R16367      8
R16368-R16427      8
R16428-R16446      0
R16467-R16872     40
R16873-R16902      0
R16903-R17103      0
```

The dominant source family is therefore the existing R4570-R14429 structured RODATA block, not a random set of isolated strings.

### 3. Place-table risk rows preserve the existing name/yomi distinction

The 32 risk rows in Stage2 block R3251-R3875 resolve inside the Switch Japanese place table at `0x6ADA10`:

```text
place name field starts   17
place yomi field starts   15
interior/other             0
TOTAL                     32
```

This reinforces the existing rule that main/display text and yomi/auxiliary text cannot share a global normalization override.

### 4. Dominant structured table has a shared native owner family

Static xref analysis of the dominant R4570-R14429 target range (`0x711DA0` onward) found a Switch-native record-access family that selects language-specific bases and addresses records with stride `0xC2`. The Japanese-side target base used by that family is `0x711DA0`; the same function family chooses parallel language tables under existing language-state branches.

This is strong structural evidence that the 1,686 susceptible rows in this block belong to a shared structured-table consumer family. They should be traced as a family from record/field access to text normalization/output, not as 1,686 separate raw-string cases.

### 5. Downstream decode address provenance remains consistent

The reconstructed Switch NSO reproduces the already-canonical six direct callers of mapped decode/renderer `0x445C60`:

`0x445F24`, `0x4460F8`, `0x4471BC`, `0x447534`, `0x447B94`, `0x44D920`.

This was used only as an address-map sanity check. It does not reopen V265-V270.

## Strong hypotheses

- The minimum repair owner is likely above the renderer and below/inside the native structured-table-to-text normalization boundary for one or more consumer families.
- The dominant R4570-R14429 block is likely reducible to a small number of field/consumer routes because its Switch-native accessors operate on a common fixed-stride table.
- Place-name and place-yomi rows must remain separately controlled even if they share the same physical table.

These remain hypotheses until each storage family is bound to the actual normalization/copy route and active conversion mode.

## Unconfirmed items

- Exact identity/address of the generic halfwidth normalization owner responsible for the canonical 1,078-call-site census has not yet been re-bound in this run.
- The 64 non-Stage2 risk rows still require reuse of existing F1/forward/gap target/owner provenance before consumer tracing.
- Stage2 blocks other than the dominant structured table and place table still require family-level consumer-route binding.
- No source family is yet proven to require a specific patch site or branch condition.

## Rejected hypothesis / false lead

A Switch target at `0x263C5C` was initially noticed because it has 1,078 direct callers. Direct disassembly shows it tail-branches to an unrelated calculation/copy routine at `0x43F2A4`; caller-count equality alone is not semantic proof. It is therefore rejected as the generic halfwidth normalizer candidate and must not be reused as such.

## Related impact scope

Current exact source-risk denominator remains 2,057. The newly established structural split is:

- 1,993: existing Stage2 affine target identity available;
- 64: non-Stage2 rows requiring existing canonical F1/forward/gap provenance;
- within Stage2, 1,686: dominant fixed-stride structured RODATA family;
- within Stage2, 32: place table, already split into 17 name / 15 yomi starts;
- within Stage2, 40: DATA targets;
- remaining Stage2 risk rows: other RODATA families requiring grouped consumer tracing.

This is an impact/route-analysis partition only. It does not equal Action Ledger cardinality.

## Proposed correction direction

No implementation is authorized yet.

The next deterministic steps are:

1. bind the 64 non-Stage2 rows to their already-canonical F1/forward/gap owners without raw-value guessing;
2. trace the dominant `0x711DA0` fixed-stride structured-table family from field access to its text-copy/normalization consumers;
3. bind the remaining Stage2 RODATA/DATA block families similarly;
4. recover the actual generic halfwidth-normalization function by behavior/signature/control flow, not caller-count coincidence;
5. classify every resulting family as direct-renderer / generic-normalizer / explicit-yomi / other proven route and record active conversion mode;
6. only after full family coverage, design the minimum Switch-native conditional raw-preservation realization and a single-cause diagnostic build.

## Boundaries preserved

- Existing VERIFIED Stage1/Stage2/F1/FZ001/forward/Oracle/Pointer/Mapping facts unchanged.
- No builder/runtime implementation performed.
- No diagnostic build generated.
- No new WRITE_SAFE authority.
- No global Japanese halfwidth-disable design permitted.
- A auxiliary-name issue remains `HOLD_FOR_CWTDAT` and was not touched in this scope.
