# ECF00000 partition-593 0x0E residual root cause / validator gate — V340

Date: 2026-09-20 (KST)

```text
validation_id   V340
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          042f3b9f549ef155ec951ed965bdaa5afe08a88b / V339
scope           ECF00000_PARTITION593_0E_RESIDUAL_RUNTIME_OVERRUN_ROOT_CAUSE_AND_VALIDATOR_GATE
product_bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

V340 closes the sole V339 state-aware diagnostic residual at partition 593 / original `0xBDD78` / opcode `0x0E`. The residual is not repaired in product bytes. It is classified as a stock-pre-existing MAY-model artifact and the validation gate is changed from absolute zero-error to a stock-differential logical-residual gate.

## 1. Exact baseline and candidate residual

Stock original and V339 diagnostic both expose the same logical residual:

```text
                    stock original          V339 diagnostic
partition           593                     593
original anchor     0xBDD78                 0xBDD78
current position    0xBDD78                 0xDDD84
header              0E 02 D5 1F             0E 02 D5 1F
opcode              0x0E                    0x0E
decoded length      0x7F5408                0x7F5408
```

`0x7F5408` is the exact Switch `0x01/0x02/0x0E/0x0F` parent-length formula result:

```text
word = LE32(0E 02 D5 1F) = 0x1FD5020E
length = (word >> 6) & 0x3FFFFFC
       = 0x7F5408
```

Therefore V339 did not introduce or mutate this logical residual. It only relocated the same original object after valid payload growth.

## 2. Switch `main` identity and bounded handler evidence

Exact Switch v1.1.3 `main`:

```text
size    5,287,359
sha256  b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b
```

Decompressed text segment:

```text
size    5,820,000
sha256  c80792d1c104320ce995fef3ec4ac798870da85ae8f86c3f52e209e478d0bf35
```

Bounded disassembly confirms:

```text
0x15F2C0  common interpreter loop
0x15F44C  EVENT record dispatch
0x15FCB8  EVENT 0x0E handler
0x15FD60  0x0E parent-length decode path
0x16087C  0x5A handler
```

The `0x5A` handler confirms the V339 runtime-length reconstruction: the two JP-name fields and dialogue are terminated by NUL and aligned to four-byte boundaries before consumed length is returned. The stock second `0x5A` therefore genuinely lands on `0xBDD78`; this is not a V339 `0x5A` length-formula defect.

The `0x0E` handler confirms `p+4` recursive EVENT evaluation and the parent-length formula above. The very large encoded parent length is therefore not a decode bug.

## 3. Missing state in the diagnostic model

The common interpreter loop contains control state beyond the V333 conservative identity `(context, physical_address, S, F)`.

Bounded Switch evidence reads or writes at least:

```text
context mode        +0x08
result              +0x0C
control             +0x10
control             +0x11
branch-chain        +0x12
global stop/state   runtime object +0x54
```

After a record handler returns a consumed length, the loop does not unconditionally execute `p += length`. It first performs opcode-specific post-processing and checks the additional mode/control/global state. EVENT `0x0E` also executes a nested EVENT context with mode `2` before returning its encoded parent length.

V333 intentionally defined the 13,075-row source universe as conservative MAY-reachable rather than exact gameplay-feasible. The residual is consistent with that conservative over-approximation: the diagnostic state vector can combine a physical address and `S/F` state without carrying all interpreter control-mode correlation.

V340 does not claim the exact concrete gameplay predicate for root 593. It establishes the narrower fact required for release validation: the same residual exists in unmodified stock and no V339 product mutation created it.

## 4. Root-cause disposition

```text
V339 5A runtime formula          NOT CAUSE
V337 generic relocation          NOT CAUSE
V338 special spans               NOT CAUSE
1E omission                      NOT CAUSE
3C omission                      NOT CAUSE
0x0E payload mutation            NOT CAUSE

root cause
STATEAWARE_WALKER_STATE_VECTOR_INCOMPLETE_RELATIVE_TO_SWITCH_INTERPRETER_CONTROL_MODE
```

The residual is classified:

`STOCK_PREEXISTING_MAY_MODEL_ARTIFACT_NON_BLOCKING`

No `0x0E` byte patch is authorized.

## 5. Validator-gate correction

New module:

`builder/selective_event_validation.py`

New tests:

`tests/test_selective_event_validation.py`

The gate is differential.

Logical residual identity is:

```text
(kind, partition, original_offset, opcode, decoded_length)
```

`current_offset` is provenance only and is deliberately excluded because legitimate selective growth can relocate the same original logical object.

Policy:

```text
same stock-preexisting logical residual   NON_BLOCKING_DIAGNOSTIC
stock residual disappears                NON_BLOCKING
new logical residual                     BLOCKING
same anchor but changed opcode/length     BLOCKING
candidate duplicate logical residual      BLOCKING
```

Canonical stock baseline:

```text
partition        593
original anchor  0xBDD78
opcode           0x0E
decoded length   0x7F5408
```

## 6. Unit validation

```text
canonical stock residual                     PASS
0x0E exact length formula                    PASS
shifted same logical residual nonblocking    PASS
resolved stock residual nonblocking          PASS
novel residual blocking                      PASS
changed-length same-anchor blocking           PASS
duplicate candidate residual rejection       PASS
-------------------------------------------------
unit                                           PASS_7_OF_7
```

## 7. Rejected / do-not-repeat

Reject:

- require `state-aware errors == 0` as an absolute product gate;
- patch `0x0E @ 0xBDD78` merely to make the diagnostic count zero;
- force the preceding `0x5A` to PC-KO geometry solely to avoid this stock-preexisting path;
- reopen V339 `0x5A` because this residual remains;
- attribute the residual to missing `1E` or `3C` payload without new evidence;
- compare candidate residuals by relocated current offset instead of original logical provenance;
- treat MAY-reachable membership as proven exact gameplay-feasible execution.

## 8. Impact boundary

Unchanged and still closed:

```text
V336 S1 serializer core          CLOSED
V337 generic relocation          CLOSED
V338 Switch special spans        CLOSED
V339 5A composite               CLOSED
```

No product bytes, final ECF, package, IPS, or hardware state changed in V340.

## 9. Current disposition / next scope

```text
partition-593 0x0E product blocker       CLEARED
classification                           NON_BLOCKING_DIAGNOSTIC
validator gate                           STOCK_DIFFERENTIAL_NOVEL_ONLY_BLOCKING
1E semantic admission                    OPEN
3C                                       KEEP_JP / not materialized
code-3 fixed particle                    OPEN
full S4                                  NOT RESUMED
```

Exact next scope after a fresh explicit user signal:

`ECF00000_1E_SEMANTIC_ADMISSION_LEDGER_READ_ONLY`

READ ONLY only. Classify the `0x1E` family using actual original/PC-KO payload semantics while preserving dedicated identity fields in Japanese. Do not resume full S4, code-3 particle implementation, package/build/IPS, or hardware in that scope.
