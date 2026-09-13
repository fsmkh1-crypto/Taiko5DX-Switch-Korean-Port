# MASTER RULE REGISTRY

Date: 2026-09-13 (KST)  
Status: CANONICAL RULE-DISCOVERY / PRECEDENCE OVERLAY

## 1. Authority boundary

This registry centralizes operative rules already established by canonical project evidence. It is an index/normalization overlay, not a replacement for source evidence.

- `PROJECT_STATE.md` remains the sole resume authority.
- FZ001 and its frozen machine-accounting identities are unchanged.
- Historical evidence documents and rejected/superseded rules remain preserved.
- Counterpart/routing closure remains distinct from `WRITE_SAFE`.
- This registry creates zero new Switch write authorizations.

## 2. Precedence

When two statements appear to conflict, apply this order:

1. `PROJECT_STATE.md` current scope/boundary;
2. frozen FZ001 identities for the frozen schema domain;
3. later narrow canonical correction over an older broader claim;
4. source canonical evidence over this registry summary;
5. rejected/superseded rules only as negative provenance.

Machine registry: `data/post_freeze/master_rule_registry_v1/RULES.json` (78 rules).

## 3. OPERATING

- **MR-OP-001 — Explicit execution gate** [NORMATIVE]: No actual analysis, modification, build, runtime, or repository mutation begins without a fresh explicit user execution signal for the agreed scope.
- **MR-OP-002 — One signal one scope** [NORMATIVE]: One execution signal authorizes only the currently agreed scope. After a report/STOP boundary, a fresh signal is required for the next stage.
- **MR-OP-003 — Separate analysis and modification** [NORMATIVE]: Analysis and modification are distinct stages; an analysis report is not write authorization.
- **MR-OP-004 — Root-cause family before patch** [NORMATIVE]: Before patching a symptom, inspect the full same-root-cause impact across data, code paths, consumers, runtime handling, related functions, and similar symptoms.
- **MR-OP-005 — PC patch oracle first** [NORMATIVE]: When the PC Korean patch implements the relevant behavior, inspect its actual replacement, data structure, runtime ownership, pointer behavior, and encoding before inventing a Switch-specific mechanism.
- **MR-OP-006 — Source-grounded Korean data** [NORMATIVE]: Names, place names, Korean spellings, special glyph codes, and translations available from the PC patch must be taken from actual patch data rather than guessed.
- **MR-OP-007 — One cause family per diagnostic build** [NORMATIVE]: A diagnostic build tests one root-cause family; confirmed same-mechanism sites may be tested together, unrelated hypotheses may not.
- **MR-OP-008 — Preserve rejected hypotheses** [NORMATIVE]: Rejected, weakened, or superseded hypotheses remain recorded so later chats/models do not repeat them.
- **MR-OP-009 — No chat/model revalidation trigger** [NORMATIVE]: A new chat, model, agent, or tool is not by itself a reason to revalidate already VERIFIED evidence.
- **MR-OP-011 — Git object only write mode** [NORMATIVE]: Repository writes use only create_blob, create_tree, create_commit, and update_ref(force=false); contents-API writes, branch creation, force push, and history rewrite are forbidden.

## 4. AUTHORITY_PROVENANCE

- **MR-OP-010 — Project resume authority** [NORMATIVE]: PROJECT_STATE.md is the sole project-resume authority; historical plans, ledgers, and handoffs preserve provenance but do not override it.
- **MR-AC-005 — Facts and interpretations stay separate** [NORMATIVE]: Observed facts and interpretations are separate claims; interpretations must explicitly depend on the facts they use.
- **MR-AC-006 — Frozen FZ001 remains unchanged** [BOUNDARY]: The master registry is a discovery/provenance overlay and does not redesign or mutate the frozen FZ001 semantic schema or bindings.

## 5. ACCOUNTING_SCHEMA

- **MR-AC-001 — Immutable IDs and append-only histories** [NORMATIVE]: Issued IDs are stable and histories are append-only; corrections use explicit supersession rather than deletion or renumbering.
- **MR-AC-002 — Independent accounting axes** [NORMATIVE]: Applicability, analysis, target, action, and closure are separate axes and must not be collapsed into one status.
- **MR-AC-003 — Unknown is an authorization blocker** [BOUNDARY]: UNKNOWN or unresolved evidence may not silently authorize a write or remove a source from accounting.
- **MR-AC-004 — Source coverage is not action/release closure** [NORMATIVE]: Source coverage, action closure, and release closure are distinct; closing one does not imply the others.

## 6. PC_RUNTIME_REFERENCE

- **MR-PC-001 — Reproduce semantics, not Windows mechanics** [PROMOTED_RULE]: Switch must reproduce the semantic obligations of the PC patch, not necessarily its Windows allocation, signature-search, instruction, or helper implementation mechanics.
- **MR-PC-002 — Full mapping-family obligation** [VERIFIED]: The PC patch mapping family is a complete 10,036-entry semantic obligation and must include all relevant consumers before mapping closure.
- **MR-PC-003 — Pointer population is exhaustive** [VERIFIED]: All 56 PC pointer records are accounted for; partial pointer handling is not full closure.
- **MR-PC-004 — Inline population is exhaustive** [VERIFIED]: All 17,103 PC inline records are part of the source-accounting obligation unless explicitly dispositioned.
- **MR-PC-005 — Runtime descriptors/helpers are semantic families** [VERIFIED]: Runtime descriptors and helpers are tracked by semantic behavior; Switch may use a structurally different equivalent mechanism if the semantic obligation is proven.

## 7. STRUCTURAL_TARGETING

- **MR-S1-001 — Raw candidate counts are discovery evidence** [NORMATIVE]: Raw candidate count, including a unique occurrence, is discovery evidence and does not by itself authorize a port action.
- **MR-S1-002 — Language-table ownership domains are distinct** [VERIFIED]: JP, CN, and TW localization tables are distinct ownership domains; a match in another language table is not automatically a JP/Korean write.
- **MR-S2-001 — Affine block target rule** [VERIFIED]: A Stage-2 affine target uses the block-specific fixed delta only inside its proven block and only when the exact original-byte guard succeeds.
- **MR-S2-002 — Affine relation does not cross gaps** [VERIFIED]: Affine relations cannot be extended across uncovered gaps or resets without independent exact evidence.
- **MR-S2-003 — Position can disambiguate repeated values** [VERIFIED]: Repeated raw text values need not require consumer tracing when position within an accepted structural block resolves the target unambiguously.
- **MR-S2-004 — DATA match is not a relocation cell** [BOUNDARY]: A data match does not automatically establish that the matched location is a relocation pointer cell.
- **MR-C64-001 — CAP64 censorship rule** [PROMOTED_RULE]: A stored raw candidate count of 64 means censored actual count >=64; it cannot prove absence, uniqueness, complete language coverage, or complete storage-mutability coverage.
- **MR-FW-001 — NUL-aware logical normalization** [PROMOTED_RULE]: NUL-aware logical windows may be the correct text-comparison unit for structural analysis.
- **MR-FW-002 — Empty logical string is not positive prefix evidence** [PROMOTED_RULE]: An empty logical string cannot be used as positive prefix-match evidence.
- **MR-FW-003 — Stable structural precedence** [VERIFIED]: Structural precedence is coherent table/storage/encoding family, then NUL-aware logical full match, shared-owner cardinality, logical prefix, embedded containment, then opaque/unknown structure.
- **MR-FW-004 — Formatter is an overlay** [PROMOTED_RULE]: Formatter classification is an overlay and does not replace the primary structural family.
- **MR-FW-005 — Historical 735/251 split is not a structure boundary** [VERIFIED]: The historical 735/251 split is provenance, not a guaranteed physical/semantic data-structure boundary.

## 8. WRITE_SAFETY

- **MR-S2-005 — Target resolution is not write safety** [BOUNDARY]: AFFINE_STATIC_BLOCK_PORT and other target-resolution states establish target identity, not final write safety.
- **MR-F1-001 — Accepted interval minimum** [VERIFIED]: An accepted anchor-bounded F1 interval must itself contain at least five rows.
- **MR-F1-002 — Exact guard and equal length are insufficient** [NORMATIVE]: Exact original guard plus equal replacement length is not sufficient to prove a safe static write.
- **MR-F1-003 — Terminating capacity is mandatory** [VERIFIED]: Write safety requires sufficient object capacity including terminator semantics, not merely payload fit.
- **MR-F1-004 — PC padding is not Switch capacity** [VERIFIED]: Padding available to the PC patch cannot be assumed reusable on Switch; padding mismatches require reconstruction evidence.
- **MR-F1-005 — Shared physical owner closure** [VERIFIED]: A shared physical Switch object requires closure of all logical-owner obligations before a global physical write is authorized.
- **MR-F1-006 — F1 authorization boundary** [BOUNDARY]: The 158 DIRECT_PORT rows are static-write-authorized but not implemented; the 75 padding, 25 shared-owner, 4 capacity-fail, and 16 rule-rejected rows are not silently promoted.
- **MR-WS-001 — Counterpart/routing closure is not WRITE_SAFE** [BOUNDARY]: TRACE=0 and complete counterpart/routing closure create no new Switch WRITE_SAFE authorization.
- **MR-WS-002 — Switch write requires capacity, terminator, storage and owner proof** [NORMATIVE]: A final write requires validated target ownership, storage/object boundary, capacity, terminator/control preservation, and any shared-owner obligations.
- **MR-WS-003 — Final patch round-trip and runtime boundary** [NORMATIVE]: Final emitted patch data must round-trip exactly; runtime success is sanity evidence and does not replace structural safety proof.
- **MR-WS-004 — Passing subsets do not construct the safe set** [NORMATIVE]: ddmin or passing halves may localize failure causes but cannot by themselves prove that every member of a combined set is safe.

## 9. SEMANTIC_ORACLE

- **MR-L3-001 — Evidence order before tracing** [PROMOTED_RULE]: Use Switch structure, PC occurrence mechanism, PC replacement/context, Switch neighborhood, and semantic role before consumer tracing.
- **MR-L3-002 — Strict prefix is not semantic ownership** [PROMOTED_RULE]: A strict-prefix relation does not prove semantic-owner identity.
- **MR-L3-003 — PC inline record can be a partial window** [VERIFIED]: A PC inline record may split a multibyte character or cover only part of a larger composite object; one record is not automatically one semantic string.
- **MR-OR-001 — Exact sequence lock** [PROMOTED_RULE]: Long exact sequence correspondence can deterministically bind a Switch target when sequence identity and context are preserved.
- **MR-OR-002 — Composite pair lock** [PROMOTED_RULE]: Adjacent PC records may jointly reconstruct one Switch object; the pair can resolve the target when the composite evidence is exact.
- **MR-OR-003 — Replacement full-object lock** [PROMOTED_RULE]: A PC replacement may identify the complete object represented on Switch when the full-object correspondence is exact and context-bound.
- **MR-OR-004 — Formatter template lock** [PROMOTED_RULE]: Formatter/template objects can be resolved by exact template structure rather than by fragment semantics alone.
- **MR-OR-005 — Cross-encoding exact-text lock** [PROMOTED_RULE]: Exact decoded text correspondence across encodings can resolve the same logical object.
- **MR-OR-006 — Strict reverse-context lock** [PROMOTED_RULE]: Reverse-context evidence is a hard resolver only when the context rule is strict enough to identify one target; loose context is not.
- **MR-OR-007 — Second-pass pair lock** [PROMOTED_RULE]: A later deterministic pair reconstruction is valid when it closes an earlier fragment ambiguity without semantic guessing.
- **MR-OR-008 — S3 partial-composite reconstruction lock** [PROMOTED_RULE]: S3 prefix fragments may be resolved as components of a larger composite object when the PC reconstruction and Switch full object agree.
- **MR-OR-009 — S3 formatter-composite reconstruction lock** [PROMOTED_RULE]: S3 formatter/control prefixes may resolve through full formatter-object reconstruction rather than standalone translation.
- **MR-OR-010 — S4B embedded-composite reconstruction lock** [PROMOTED_RULE]: Embedded fragments with multiple raw occurrences may resolve through exact composite reconstruction instead of occurrence count alone.
- **MR-OR-011 — Deterministic evidence before semantic/tracing** [NORMATIVE]: Exhaust deterministic PC-patch evidence before semantic adjudication, and use consumer tracing only for remaining structural, encoding, or ownership blockers.
- **MR-SA-001 — Counterpart dispositions are not write authorization** [BOUNDARY]: TARGET_RESOLVED and COMPOSITE_OR_FORMATTER_RESOLVED are counterpart/routing dispositions and do not imply WRITE_SAFE.
- **MR-SA-002 — Same-text occurrence is not ownership** [PROMOTED_RULE]: The existence of the same text at a Switch occurrence does not by itself establish semantic ownership.
- **MR-SA-003 — Astra is narrow adjudication** [NORMATIVE]: Astra is used as a narrow semantic/falsification adjudicator after deterministic evidence, not as the default resolver.
- **MR-TR-001 — Merged-consumer owner binding** [PROMOTED_RULE]: Long ordered lineage plus proven consumer reuse can bind a merged owner while leaving a separate presentation-policy conflict.
- **MR-TR-002 — Opening/closing owner binding** [PROMOTED_RULE]: Occurrence order or padding alone is insufficient; preserved local preimage structure plus full-object separation and Switch sequence correspondence can bind opening/closing owners.
- **MR-TR-004 — Alternative encoding before binary classification** [PROMOTED_RULE]: Failure under CP932 is not proof of non-text; alternative language-domain encodings must be considered when evidence indicates them.

## 10. REROUTE_SUBSUME

- **MR-TR-003 — Padding-extension component** [PROMOTED_RULE]: An empty logical window may be a padding-extension component of an adjacent object and should be absorbed into complete-object reconstruction rather than patched independently.
- **MR-TR-005 — CN exact identity does not authorize CN write** [BOUNDARY]: An exact CN-table counterpart can prove identity but does not automatically authorize a CN-table write in the Korean path.
- **MR-TR-006 — PC-only UTF16 may reroute to Switch semantic owner** [PROMOTED_RULE]: A PC-only UTF-16 object may be rerouted to an equivalent Switch-native localization owner when the semantic obligation and Korean oracle are proven.
- **MR-TR-007 — No silent omission of equivalent obligation** [PROMOTED_RULE]: Absence of the exact PC-specific object does not make it irrelevant if Switch carries the same semantic obligation; SUBSUMED requires an explicit linked non-SUBSUMED action.

## 11. REJECTED_SUPERSEDED

- **MR-C64-002 — Historical 700-complete assumption** [SUPERSEDED]: The historical 700-row forward-localization partition is provenance only and is not the complete current forward population.
- **MR-C64-003 — Historical R1291 L4 absence** [REJECTED]: The historical claim that R1291 had no JP localization start is retracted after the uncapped rescan.
- **MR-RJ-001 — Unique physical target plus replacement agreement** [REJECTED]: A unique physical target plus replacement agreement alone is insufficient target proof.
- **MR-RJ-002 — Full Switch object elsewhere in PC patch** [REJECTED]: The mere existence of the full Switch object elsewhere in the PC patch is insufficient target proof.
- **MR-RJ-003 — Loose reverse context** [REJECTED]: Loose reverse-context similarity is not a hard resolver.
- **MR-RJ-004 — Two-byte Korean containment** [REJECTED]: Short Korean replacement containment, especially two-byte fragments, is not hard evidence.
- **MR-RJ-005 — Sparse adjacency** [REJECTED]: Sparse adjacency alone cannot select a target.
- **MR-RJ-006 — Structural family as semantic target** [REJECTED]: A structural family label is not itself semantic target proof.
- **MR-RJ-007 — Same Korean replacement implies same target** [REJECTED]: Matching Korean replacement text does not prove common ownership or common Switch target.

## 12. Current porting boundary

- Stage 1 inventory: complete.
- Stage 2 structural targeting: complete.
- F1: 158 static-write-authorized but not implemented; 75 padding reconstruction, 25 shared-owner, 4 capacity fail, 16 rule rejects remain separate.
- Forward 986 counterpart/routing analysis: complete; `TRACE = 0`.
- `TRACE = 0` does not authorize implementation.
- Next logical scope is write-safety/action-ledger planning under a fresh execution signal.

## 13. Registry maintenance

Promote a new rule only when it changes downstream decisions, boundaries, evidence precedence, or rejected/superseded handling. Do not turn every historical prose sentence into a rule.
Every future rule addition must preserve provenance and explicitly record supersession/rejection relationships when applicable.
