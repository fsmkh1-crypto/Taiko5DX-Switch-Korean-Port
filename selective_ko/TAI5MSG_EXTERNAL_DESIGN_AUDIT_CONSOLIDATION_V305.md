# TAI5MSG EXTERNAL DESIGN AUDIT CONSOLIDATION — V305

Date: 2026-09-18 (KST)
Status: CANONICAL TEXT-ONLY AUDIT CONSOLIDATION / NO NEW BINARY CLAIM / NO IMPLEMENTATION
Track: SWITCH_SELECTIVE_KOREANIZATION
Validation ID: V305
Parent: 2b0da47d8fc455181eb64259712f5205868622a2

## 1. Purpose and evidence class

V305 consolidates four user-supplied external text-only red-team reviews of the V303/V304 selective TAI5MSG serializer design.

The external reviews were performed without direct access to the canonical binaries. Therefore V305 does not promote external reviewer speculation into new binary facts.

V305 records only accepted design gates, narrowed/partial findings, rejected repeat hypotheses, and the next bounded read-only scope.

No gameplay data, candidate/classification row, builder, serializer, TAI5MSG output, IPS, build, or runtime package is created by V305.

## 2. Canonical carrier separation

GLOBAL selective INCLUDE_KO corpus = 3,318

- inline R1 materialized rows = 139; carrier = Switch main / inline object families; TAI5MSG membership = NO.
- TAI5MSG V303 release rows = 3,179; carrier = RomFS TAI5MSG_JP.DAT; processed by TAI5MSG serializer = YES.

The shared SEL-CAND/SEL-CLS ID namespace is a project-wide classification namespace, not a storage-container namespace.

Therefore TAI5MSG serializer population = 3,179 while global selective corpus = 3,318.

## 3. Accepted external findings

### 3.1 DETERMINISTIC_PADDING_GATE

A future serializer must define canonical bytes in every logical/physical region between rebuilt used-data end and the applicable block physical/declaration boundary.
Do not guess 0x00 merely because it is a common filler value.
Required proof: inspect stock decrypted block filler semantics; distinguish decrypted logical filler from encrypted on-disk bytes; reproduce the stock rule deterministically; never leave uninitialized/stale host-memory data.

### 3.2 ZERO_REPLACEMENT_IDENTITY_REBUILD_GATE

Before applying Korean replacement, serializer primitives must prove an identity rebuild:
stock TAI5MSG -> parse/decrypt -> zero replacements -> rebuild offsets/blocks/header -> encrypt/emit -> exact stock output.

Preferred acceptance condition: zero-replacement emitted bytes == canonical stock TAI5MSG bytes.
If stock permits multiple byte-distinct but semantically equivalent encodings, that must be independently proven before weakening byte identity.

This gate jointly tests parser/writer agreement, block layout reconstruction, padding determinism, encrypt/decrypt determinism, block-offset regeneration, and B32 final-block partial-EOF handling.

### 3.3 CONTROL_AND_CODE_VALIDATION_GATE

Production consumption must revalidate the effective V303+V304 payload set rather than merely trust the earlier census.
For every effective TAI5MSG release row: tokenize with the measured game-code/control grammar; reject invalid lead/trail pairs; require text codes inside the authorized mapping domain; reject unknown/malformed tokens; require unauthorized semantic insertion count = 0; preserve identity policy; abort instead of silently repairing new defects.

V304 remains the only currently authorized PC-payload correction overlay.

### 3.4 STRONG_REPARSE_OFFSET_GATE

Inherited verified structure:
block +0x00 = u16 message_count
block +0x02 + local_index*4 = u32 message offset

Future postconditions must include: per-block message counts unchanged; total messages = 14,832; offset entry count matches message count; offsets satisfy verified ordering/bounds; no message overlap; each message end stays inside the applicable physical block extent; emitted bytes are reparsed through the reader path; reparsed 14,832 logical payloads exactly match the intended target set.

### 3.5 MAPPING_TO_GLYPH_CLOSURE_GATE

Release/package integration must close:
effective emitted Korean game codes <= deployed Mapping 10,036 realization <= deployed page/glyph realization <= deployed Korean font glyph availability.

This is a release/package gate, not a reason to couple the pure TAI5MSG RomFS serializer to every ExeFS/font build input.
font asset identity PASS != runtime render-path PASS remains binding.

## 4. Accepted release-QA follow-up

The 191 external-caller wait rows remain Japanese by policy. Future visual/runtime QA must check whether any contiguous included/wait ranges produce materially confusing mixed JP/KO lists or screens.
This is not a structural serializer blocker and does not authorize promotion of the 191 waits.

## 5. Partially accepted / narrowed findings

### 5.1 Offset-table concern

Stronger offset/boundary postconditions are accepted. The claim that offset width or table placement is unknown is rejected because V302 already established u16 count + u32 offsets[] and the getter's block-local access.

### 5.2 Encryption concern

A round-trip/identity-rebuild proof is accepted. Encryption is not promoted to an unknown new format merely because text-only reviewers were not given the prior primitive evidence.
Logical postconditions are decrypt/reparse semantics; physical postconditions are emitted header/block offsets/sizes/file extent/EOF behavior.

### 5.3 V304 verdict wording

V304's exact two-row repair remains authorized. Historical authoring/tool cause remains unknown.
Preferred narrow description: defect class = MALFORMED_TRAILING_LEAD / PC_PAYLOAD_DEFECT; authorized repair = DROP exact trailing FB under V304 guards; historical cause = UNKNOWN.

## 6. Rejected external hypotheses — do not repeat

1. Inline 139 must be added to TAI5MSG 3,179 — REJECTED. Different carriers.
2. V304 payload lengths prove a per-message length prefix — REJECTED. Lengths are artifact-level payload lengths; no such field is established.
3. A movable block-local offset-table pointer must be updated — REJECTED. Getter indexes block_buffer +0x02 + local_index*4.
4. Block checksum regeneration is required — REJECTED as unsupported. No TAI5MSG CRC/HMAC/checksum field is established.
5. V304 changes release growth from +0x7780 — REJECTED. B19 used 0xF5D6->0xF5D5 with declared 0xF600 unchanged; B30 used 0x9E0A->0x9E09 with declared 0xA540 unchanged.
6. Reverse mapping conflicts with reverse-substitution policy — REJECTED. Encoding conversion and localization rewrite are different layers.
7. Remaining 05 05 05 after V304 is a newly introduced unknown Switch sequence — REJECTED. V304 removes the malformed extra FB and restores the stock-style ending shape.

+0x7780 is an expected recomputed postcondition, not an input constant to hard-code.

## 7. Claim-boundary clarifications

Use: selected internal TAI5MSG C/J edges = 0; selected semantic 0x02 insertions = 0; external caller resolution = separate axis.
Do not broaden this into a blanket claim about unresolved external-caller composition semantics.

Existing claim ladder remains: target resolved != WRITE_SAFE != INCLUDE_KO != implementation/build PASS != runtime-path PASS != gameplay QA PASS.

## 8. Consolidated preimplementation gate set

GATE-1 DETERMINISTIC_PADDING_GATE
GATE-2 ZERO_REPLACEMENT_IDENTITY_REBUILD_GATE
GATE-3 CONTROL_AND_CODE_VALIDATION_GATE
GATE-4 STRONG_REPARSE_OFFSET_GATE
GATE-5 MAPPING_TO_GLYPH_CLOSURE_GATE

GATE-5 is a release/package integration gate. GATE-1 through GATE-4 directly constrain the TAI5MSG serializer path.

## 9. External-review limitations

External reviews are useful for arithmetic consistency, claim-strength auditing, missing-invariant discovery, and documentation ambiguity. They are not authority for new fields, new checksum assumptions, new binary structures, or new runtime behavior.
Any external concern contradicting a closed VERIFIED fact requires new binary evidence before reopening that fact.

## 10. Next scope

After a fresh explicit user signal, resume exactly:
TAI5MSG_SELECTIVE_SERIALIZER_IDENTITY_REBUILD_AND_PADDING_PROVENANCE_READ_ONLY

Scope: READ ONLY. Inspect stock 33-block padding/filler semantics; verify parse/decrypt -> zero-replacement rebuild -> encrypt identity; verify B32 final-block physical EOF/partial-tail behavior; separate logical plaintext from physical emitted-file invariants; record failures/rejected hypotheses.

NO serializer implementation, gameplay-data mutation, TAI5MSG release output, IPS/build/package, or hardware execution.

Stop after the six-part analysis report. A further explicit user signal is required before any implementation or following materialization.

## 11. Repository write boundary

create_blob -> create_tree -> create_commit -> update_ref(force=false)
