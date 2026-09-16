# KO Grammar Register Normalize 125 Builder Implementation — V289

Date: 2026-09-17 (KST)
Status: CANONICAL IMPLEMENTATION CLOSURE / NO BUILD
Validation ID: `V289`
Scope: `KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILDER_IMPLEMENTATION_NO_BUILD`
Build authorization: NONE
Hardware-test authorization: NONE
New WRITE_SAFE authorization: 0

## 1. Authority and inherited state

This implementation consumes, without re-census or wording re-adjudication, the V288
static-write authorization materialized at canonical `main` HEAD
`29002c496bc3e11c7e7fac0d72af100d55d46098`.

The authoritative grammar artifact remains:

```text
selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/INDEX.json
rows              = 125
manifest-set SHA  = a17b5b493a4f529e6aa308954242434e13bede0dda14b075cc13a3a890bc254c
authorized output = 993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06
```

FZ001 and the explicit WRITE_SAFE total of 287 remain unchanged. V289 implements the
already-authorized grammar125 tranche; it does not create new authorization.

## 2. Builder implementation

Changed implementation file:

```text
builder/tai5msg.py
Git blob SHA = a1400db06828174fb6193eccb447bc16d7c2749e
UTF-8 bytes  = 15,336
SHA-256      = 7398b48626dc641fc995ee1c7e1215d37d0bfb901d6496056a36324ada1f7a62
```

The public builder interface remains `reconstruct_tai5msg_switch_native(blob)` and the
existing `Tai5MsgReconstructionReport` shape remains compatible with `builder/build.py`.

The implementation now performs one canonical-input transaction:

```text
verify PC Korean v1.02 input SHA
-> parse 33 blocks / 14,832 messages once
-> scan existing compact33 population
-> load and hash-verify V288 INDEX + 4 ordered row shards
-> verify all 125 source locator/length/SHA guards
-> apply source-coordinate edits in descending order
-> verify all 125 exact target length/SHA identities
-> enforce 177 removal / 125 preserved-call / -645 byte accounting
-> enforce grammar125 ∩ compact33 = 0
-> apply grammar125 and compact preservation before one block rebuild
-> preserve original physical block sizes and original header block pairs
-> reparse the result
-> verify 158 changed messages / 17 affected blocks / 44 protected compact occurrences
-> verify every V288 target identity again after rebuild
-> enforce final SHA-256 993d3fc2...
```

No grammar-modified intermediate is fed back through the serializer.

## 3. Fail-closed guards

The builder fails closed on:

- noncanonical TAI5MSG input SHA;
- V288 index SHA/schema/validation/authority mismatch;
- shard size/hash/order/row-count mismatch;
- manifest-set replay mismatch;
- duplicate or out-of-range locator;
- source length/SHA mismatch;
- invalid/overlapping edit span;
- target length/SHA mismatch;
- grammar accounting mismatch;
- compact census/state mismatch;
- grammar/compact overlap;
- affected-block-set mismatch;
- fixed physical block capacity overflow;
- V288 final-padding ledger mismatch;
- output-size/header-pair mismatch;
- changed-message/block accounting mismatch;
- post-rebuild target mismatch;
- final deterministic output SHA mismatch.

## 4. Local implementation validation

This scope did not run a builder build. It performed only function-level validation against
the already-proven canonical PC Korean `TAI5MSG_JP.DAT` input
`e3b4522a...6090` recovered from the verified v1.02 patcher payload.

Results:

```text
python syntax compilation          PASS
canonical function replay          PASS
second deterministic replay        byte-identical PASS
output SHA-256                     993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06
input/output size                  2,134,366 / 2,134,366
blocks/messages                    33 / 14,832
changed messages                   158
affected blocks                    17
grown blocks                       0
compact occurrences                44

negative: input one-byte mutation  rejected by canonical-input hash guard
negative: shard byte mutation      rejected by manifest shard hash guard
```

This validation proves the implementation consumes the V288 artifact and reproduces its
exact deterministic reconstruction. It is not a release build or hardware/runtime test.

## 5. Unchanged boundaries

V289 did not:

- modify the V288 manifest or Korean wording authority;
- change WRITE_SAFE accounting;
- modify the PC patch payload or repository gameplay binaries;
- generate a mod output or IPS;
- run a diagnostic/release build;
- perform hardware validation;
- modify unrelated F1, Mapping, CWTDAT, name/yomi, or formatter/runtime queues.

## 6. Next scope / STOP

The next eligible single scope, under a fresh explicit user execution signal, is:

`KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILD_VALIDATION`

That stage may execute one build whose new cause-family delta is the V289 grammar125
implementation, then verify the emitted TAI5MSG identity and build report against V288.
Hardware validation remains a later separate stage.

V289 ends here.
