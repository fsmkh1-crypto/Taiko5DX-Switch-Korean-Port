# ENDING HELP 39 CANDIDATE / CLASSIFICATION MATERIALIZATION — V298

Date: 2026-09-18 (KST)
Status: MATERIALIZED SELECTIVE R1 CORPUS ROWS / NO BUILDER / NO BUILD / NO IPS
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `SELECTIVE_KO_ENDING_HELP_39_CANDIDATE_CLASSIFICATION_MATERIALIZATION`
Parent: `e12394da74e4e0abf06da5bd90657a70340e72b1` (V297)

## 1. Summary

V298 materializes the first selective-product candidate/classification rows from the V297 ending-help closure.

This is not a template or family-level placeholder. The corpus contains 39 independent rows. Each row carries its own:

- candidate/classification ID;
- exact contributing PC inline source IDs/RNUMs/RVAs;
- complete Japanese logical payload;
- complete PC Korean logical payload and exact encoded bytes;
- exact Switch fixed-field owner offset and record base;
- Korean payload byte length and capacity result;
- caller/mechanism/usage/risk/evidence/provenance fields;
- derived product disposition.

Materialized result:

```text
candidate IDs               = 39  (SEL-CAND-000001..000039)
classification IDs          = 39  (SEL-CLS-000001..000039)
INCLUDE_KO rows             = 39
R1 rows in this materialized family = 39
PC source records represented       = 102
```

`INCLUDE_KO` is the selective content disposition. V298 does not authorize or claim builder realization, IPS creation, runtime write safety of a future implementation, gameplay PASS, layout PASS, or hardware PASS.

## 2. Artifact

Canonical artifact directory:

`selective_ko/artifacts/ending_help_39_candidate_classification_v1/`

Files:

```text
INDEX.json
ROWS_01.jsonl.gz  SEL-CAND-000001..000013
ROWS_02.jsonl.gz  SEL-CAND-000014..000026
ROWS_03.jsonl.gz  SEL-CAND-000027..000039
```

The INDEX contains one summary entry and SHA-256 for every row plus compressed/uncompressed shard hashes. The row shards are gzip-compressed JSONL; decompression restores the exact 39 row records.

## 3. Structural basis inherited from V297

The Switch ending table is a proven fixed-stride structure:

```text
record count  = 39
record stride = 0x3FF / 1023 bytes

title       +0x000 / 21 bytes
help        +0x015 / 501 bytes
narration   +0x20A / 501 bytes
```

The 39 ending-help physical owners therefore form the exact series:

```text
first help owner = 0x77148C
last help owner  = 0x77AC66
owner delta      = 0x3FF
```

The 39 rows preserve these exact per-object offsets rather than one generic table pointer.

## 4. Source / payload provenance

V297 reconstructed the whole ending table from exact PC patch records and Switch structural objects.

For the help family used by V298:

```text
help objects                       = 39
contributing PC inline records     = 102
unique contributing records        = 102
original-byte guard failures       = 0
affine relative-offset violations  = 0
Korean decode failures             = 0
```

The row data records the exact source RNUM list for each individual help object. The 39 completed Japanese payloads are all distinct; the 39 completed Korean payloads are also all distinct.

## 5. Classification gate

All 39 rows satisfy the common selective schema with:

```text
usage_class              = UI_DESCRIPTION
mechanism_class          = STATIC_COMPLETE
investigation_status     = RESOLVED
caller_count             = 1
append_after             = NO
variable_source_kind     = NONE
jp_particle_adjacency    = NO
dynamic_counter_decision = NO
cross_message_consumers  = []
risk_flags               = []
pc_conflict_class        = NONE
evidence_grade           = VERIFIED
manual_override          = false
translation_review_status= DEFER_TO_RUNTIME_QA
```

No row is included because of a manual override.

## 6. Capacity gate

All rows have the proven Switch help capacity:

```text
buffer_capacity = 501 bytes
```

Actual per-row Korean sizes are stored individually. Population result:

```text
minimum Korean payload including NUL = 48 bytes
maximum Korean payload including NUL = 412 bytes
minimum slack                         = 89 bytes
capacity failures                     = 0
```

No translation was shortened or rewritten for capacity.

## 7. Derived disposition

Under the canonical classification rules, `STATIC_COMPLETE + UI_DESCRIPTION + RESOLVED` is eligible for R1 when owner, caller, risk, capacity, and provenance gates are closed.

Those gates are represented and closed for each of these 39 rows. Therefore:

```text
derived_disposition = INCLUDE_KO  (39/39)
```

R1 release-set definition for these rows is satisfied at the classification layer:

```text
INCLUDE_KO + usage_class=UI_DESCRIPTION
```

This does not bypass later implementation/build/runtime validation gates.

## 8. Identity-in-prose policy

Some ending-help rows contain authored Korean person-name literals such as named protagonist conditions. These remain exactly as supplied by the PC Korean source authority.

V294 remains binding:

```text
dedicated identity presentation fields  -> KEEP_JP
authored Korean prose identity literals  -> PRESERVE_AS_AUTHORED_KO
runtime-inserted identity                -> KEEP_JP
reverse substitution                     -> FORBIDDEN
```

Therefore those rows are not identity-field Koreanization and do not violate the first-release identity policy.

## 9. R651 / other prompt work

V298 does not create a candidate row for R651 or the other UI prompts. Their owner results remain V297 provenance and are outside this 39-row ending-help materialization.

In particular, V297's selected-use R651 resolution to Switch `0x6A7C21` remains inherited and must not be returned to the historical L3 `UNRESOLVED` state without contradictory evidence.

## 10. Validation invariants

The generated artifact passed the following pre-materialization checks:

```text
rows                              39
unique candidate IDs              39
unique classification IDs         39
unique Switch owner IDs           39
record-base stride set            {1023}
owner-offset stride set           {1023}
contributing PC source records    102 unique / 102 total
required common metadata missing  0
capacity failures                 0
risk-flagged rows                 0
manual-override rows              0
non-INCLUDE_KO rows               0
```

The full 39-row source artifact SHA-256 before deterministic three-shard materialization was:

`16edb20a38b7a0e55a2d1c67699ccf5e2055d4f287bf2005fe8fcf3788856677`

## 11. Claim-strength boundary

V296 remains binding.

V298 proves/materializes classification-layer inclusion for this exact 39-row family. It does not imply:

- all external YES/UNCERTAIN inline objects are R1;
- all historical WRITE_SAFE rows are INCLUDE_KO;
- the future builder implementation is safe merely because the classification is INCLUDE_KO;
- a build or package is gameplay-validated;
- one later runtime test generalizes to unrelated families.

## 12. Next work

After a fresh explicit user execution signal, the broader read-only inventory resumes under:

`SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY`

Priority within that scope is the remaining inline R1 logical-object census outside the now-materialized ending-help 39, followed by the still-open TAI5MSG/EVENT/SNR field-availability work.

Builder/build/IPS remains a separate later authorization.
