# KO Full-Sentence Grammar Flattening V1 Design

Date: 2026-09-16 (KST)
Status: CANONICAL READ-ONLY DESIGN — V285-V287 REGISTER-NORMALIZE CLOSURE INCORPORATED
Scope ID: `KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1`
Implementation authorization: NONE
Build authorization: NONE
New WRITE_SAFE authorization: 0

The previous canonical design remains an immutable inherited base:

```text
commit  dfe3b4acaeecba9c28e33db3ad6112752a26defa
path    docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md
blob    41307556cad1d6547a04f85276901450fcbf798a
```

All sections and evidence through V284 in that blob remain valid unless explicitly
narrowed below. In particular, the core rule remains:

`preserve dynamic meaning / flatten inherited Japanese dynamic grammar`

SC/TW remains structural evidence only; JP meaning, actual PC Korean patch wording, and
caller-local Korean context remain the wording authority.

## 15. V285 — pure register-normalization caller responsibility

The V284 highest-confidence pure `REGISTER_NORMALIZE_CANDIDATE` population is exactly
125 callers / 177 grammar edges. It is not one mechanical erase set.

```text
CALL_ERASURE_ONLY             99 callers / 138 grammar edges
CALLER_ENDING_MATERIALIZE     17 callers /  26 grammar edges
CALLER_PHRASE_REWRITE          6 callers /   9 grammar edges
BOUNDARY_JOIN_NORMALIZE        3 callers /   4 grammar edges
TOTAL                        125 callers / 177 grammar edges
```

The tranche contains 47 callers with 113 dynamic-semantic edges. Those dynamic calls
remain dynamic and are preserved in ID/order.

Edge-level accounting is:

```text
erasure-only grammar edges     148
non-erasure grammar edges        29
TOTAL                           177
```

Thus the design rule is caller-local:

- erase a grammar call only where the surrounding Korean caller already owns a complete
  natural grammatical construction;
- materialize the ending in the caller where removal leaves an incomplete utterance;
- rewrite the caller phrase where Japanese segmentation itself conflicts with Korean
  clause/order construction;
- normalize only the literal boundary where the remaining defect is spacing/joining;
- preserve every required dynamic-semantic call and caller control branch.

The V285 analysis matrix is fixed by SHA-256
`f638048e3f178551978dd3422e9c170532cfcfdcdc7190cfa179e36551693756`.
Its exact caller membership is copied into the dedicated V-ledger so later work does not
re-census this tranche.

## 16. V286 — literal wording adjudication

The 23 callers requiring substantive Korean wording work are closed at design level:
17 ending-materialize + 6 phrase-rewrite callers. Their wording is branch-local and
chosen from JP meaning, actual PC Korean wording, and same-caller tone/context rather
than by replaying an assumed global formatter register.

The 3 boundary-normalize callers are separately closed by post-erasure boundary
normalization. Pure-125 wording-design UNRESOLVED is therefore zero.

Representative target responsibilities include:

```text
2:179   이게 무슨 짓이오!
2:182   없는 돈을 내놓을 수는 없다 / 없는 돈을 내놓을 수는 없습니다
8:199   그럼 이만 실례하지
13:10   받은 약을 먹고 있어서… / 미안하네, 오늘은 / 대련에 응할 수 없네
16:568  현재 협력하여 전투 중입니다 / 그런 이야기를 나눌 때가 아닙니다
24:114  자기 머리부터 걱정하게
```

The complete 23-caller target set is preserved in the dedicated V-ledger.

This adjudication is a Korean V1 target design. It does not claim exact reconstruction
of the unavailable PC v1.02 runtime formatter branch for each historical execution.

## 17. V287 — materialization/write-safety design

The full 125-caller virtual transform was composed with the existing compact-byte
preservation transform against canonical PC Korean TAI5MSG input.

```text
grammar logical byte delta            -645
compact preservation control delta    +176
combined used-data delta              -469
combined changed messages              158
combined affected blocks                17
grown blocks                              0
file-size delta                           0
```

The 125 grammar callers and 33 compact-only messages have zero message-level overlap.
All 33 block identities and all 14,832 logical slots survive the combined reparse.
Header block offsets/sizes remain byte-identical to the canonical input layout.
All 44 compact susceptible bytes are protected after reconstruction and none remain
unprotected.

Therefore this tranche does not require a new block relocation strategy or TAI5MSG file
growth. The preferred implementation architecture is one transaction from the canonical
PC Korean input:

```text
parse canonical input once
-> verify exact 125 source guards
-> apply 125 caller transforms
-> apply existing compact-preservation controls
-> rebuild affected message-offset tables once
-> keep all physical block sizes fixed
-> encrypt once
-> verify deterministic output
```

Do not pipe an intermediate grammar-mutated file back through the current input-SHA
guard. The current builder entry point assumes the canonical PC Korean payload as its
single reconstruction input.

Analysis candidate output SHA-256 is
`993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06`.
This is not yet a canonical build-output identity.

### 17.1 Remaining authorization gate

V287 is a write-safety design closure, not a WRITE_SAFE grant. Before implementation,
create an exact 125-row static-write authorization manifest containing at minimum:

- `(block_index, local_message_index)` identity;
- canonical original-message hash/length;
- exact target-message hash/length;
- exact grammar-call removal count/families;
- preserved dynamic/non-register call sequence;
- preserved caller control/branch fingerprint;
- per-message and per-block capacity checks;
- final deterministic whole-file output hash;
- explicit residual target grammar-call count = 0.

The next analysis scope is
`KO_GRAMMAR_REGISTER_NORMALIZE_125_STATIC_WRITE_AUTHORIZATION_READ_ONLY`.

No implementation, TAI5MSG mutation, builder modification, build, IPS, or hardware test
is authorized by V285-V287 themselves.
