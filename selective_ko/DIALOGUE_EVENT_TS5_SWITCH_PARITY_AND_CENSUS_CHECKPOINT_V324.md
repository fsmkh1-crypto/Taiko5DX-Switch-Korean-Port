# DIALOGUE EVENT TS5 SWITCH PARITY AND CENSUS CHECKPOINT V324

Date: 2026-09-19 (KST)

```text
checkpoint_id   V324
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CHECKPOINT
parent          8323d7cdca0d66301d61cb8066b3a0b2cbdd69e7 / V323
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint closes the V323 finite EVENT command census, corrects the TS5 offset-table execution model, and records the exact Switch v1.1.3 ECF00000.TS5 parity result. All earlier VERIFIED/CLOSED facts remain inherited unless explicitly superseded here.

## 1. Exact source identities

PC Korean-patched ECF00000.TS5:

```text
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
```

Switch v1.1.3 ECF00000.TS5 extracted from Eden RomFS dump:

```text
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09
```

The Switch v1.1.3 file is byte-exact identical to the PC-original ECF00000.TS5 identity recorded by the PC patch manifest. Therefore this carrier does not require a Switch-specific source-layout reconstruction merely because the platform differs.

The PC patch manifest replaces ECF00000.TS5 and does not require replacing the paired ECF00000.TE5 for this payload.

## 2. Corrected EVENT entrypoint model

The V323 working assumption that each offset-table pair forms a non-overlapping script range is superseded.

Runtime execution is entrypoint-based:

```text
select offset[index]
-> inspect current command byte
-> 0x00 terminates the stream
-> otherwise dispatch handler
-> handler returns consumed byte length
-> current += returned length
-> repeat until 0x00
```

The next table offset is not the runtime end boundary for the current entrypoint.

The finite walker closes all 782 entrypoints:

```text
entrypoints       782
normal NUL end    782
unresolved opcode   0
loop                0
EOF overrun          0
```

Observed relation to the next offset:

```text
stream end + 4 == next offset   511
stream ends before next offset  239
stream crosses next offset       32
non-partition-compatible total  271 / 782
```

Additional structural evidence:

```text
entrypoints contained inside another long command span  42
containment relations                                 69
entrypoints reused as normal command starts            22
terminator addresses shared by multiple entrypoints    21
```

Containment relations by containing command:

```text
0x0A  39
0x0B  14
0x19   8
0x0D   4
0x05   2
0x02   2
```

Opcode bytes outside the 0x01..0x60 dispatch range are not automatically parser failures; the observed default record consumption is 4 bytes.

## 3. Exact message/choice census

Counts must distinguish entrypoint-path occurrences from unique physical commands because shared tails can revisit the same physical command.

```text
opcode   path occurrences   unique physical
0x11          3,678             3,664
0x12            101                98
0x13            433               431
0x15            252               251
TOTAL         4,464             4,444
```

Exactly 20 target physical commands are revisited through shared entrypoint paths; observed sharing is at most two entrypoints per shared target.

Message commands:

```text
unique 0x11/0x12/0x13 commands    4,193
non-empty message strings          4,187
empty message strings                  6
empty-message opcode                  0x13
```

Explicit newline census inside message strings:

```text
physical 0x0A newline bytes        4,212
path-observed newline occurrences  4,232
messages with >=1 manual newline   2,821 / 4,187
```

Manual line-count distribution for non-empty messages:

```text
1 line   1,366
2 lines  1,457
3 lines  1,350
4 lines      5
5 lines      5
6 lines      4
```

Inline-control byte 0x1B inside 0x11/0x12/0x13 message strings: 0.
Inline-control byte 0x1B inside 0x15 choice strings: 0.

Command-boundary values remain a separate layer:

```text
command 0x0A  path 1,338 / physical 1,298
command 0x1B  path     4 / physical     4
```

Choice census:

```text
unique choice commands      251
path choice occurrences     252
2-choice commands           249
3-choice commands             2
unique physical strings     504
path-observed strings       506
3-choice command offsets    0x54640 / 0x1014AC
```

## 4. Switch / PC structural parity

Both the Switch-original and PC-Korean payloads retain:

```text
script/entrypoint count   782
offset entries            783
header/table end          0xC44
first entrypoint          0xC44
last offset               physical EOF
```

All 782 corresponding entrypoints begin with the same opcode between Switch-original/PC-original and PC-Korean payloads.

The PC-Korean ECF00000.TS5 walks 782/782 entrypoints successfully under the Switch EVENT interpreter consumption rules established in V323/V324.

The Switch EVENT loader at 0x158A58 consumes the count and count+1 offset table and does not establish the stock 931,936-byte file size as a fixed script-container boundary. No evidence from this bounded analysis requires a Switch-specific serializer solely to admit the grown PC payload.

## 5. Rejected / do-not-repeat

The following hypotheses or analysis paths are rejected for ECF00000.TS5:

- offset[i]..offset[i+1] is one non-overlapping script container;
- offset[i+1] is the runtime termination boundary for entrypoint i;
- script 60 is uniquely corrupt because a long command crosses later offsets;
- any byte >0x60 proves walker desynchronization;
- the full semantic meaning of all 96 dispatch opcodes must be reverse-engineered before a finite census;
- Switch requires a new TS5 layout/serializer merely because the platform differs;
- ECF00000.TE5 must be replaced together with the PC-patched TS5;
- PC-Korean payload growth is disproven by a fixed 931,936-byte EVENT script-container limit.

Do not repeat broad recursive EVENT caller-graph traversal. V322 already records that analysis-path failure.

## 6. Product-boundary consequence

Structural compatibility is not product admission.

The current selective-product policies remain binding:

- identity presentation fields remain Japanese;
- authored Korean prose literals are preserved as authored when admitted;
- runtime-inserted identity remains Japanese;
- unresolved dynamic grammar remains deferred;
- layout quality remains a separate runtime-QA concern.

Therefore the exact PC-Korean ECF00000.TS5 is now a structurally eligible carrier candidate, not yet an automatically admitted whole-file product replacement.

## 7. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_PC_KO_SWITCH_CODE_GLYPH_AND_PRODUCT_ADMISSION_AUDIT_READ_ONLY`

Required bounded checks:

1. enumerate the actual game codes emitted by the PC-Korean ECF00000 visible message/choice payloads;
2. verify Mapping 10,036 coverage for that exact population;
3. verify visible-glyph/font closure for that exact population;
4. classify product-admission conflicts with identity policy or unresolved dynamic grammar;
5. retain layout/reflow as a separately reported QA dimension;
6. do not build, package, replace RomFS, modify translation, or mutate gameplay bytes in this audit.

No product byte, builder, IPS, package, or runtime artifact is changed by V324.
