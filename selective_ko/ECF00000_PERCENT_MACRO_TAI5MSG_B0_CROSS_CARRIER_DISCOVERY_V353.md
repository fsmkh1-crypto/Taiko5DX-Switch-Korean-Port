# ECF00000 percent-macro ↔ TAI5MSG block-0 cross-carrier discovery — V353

Date: 2026-09-20 (KST)

```text
validation_id   V353
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CLOSURE
parent          9db0fef21a7941630625a3020a1ccdee139910fc / V352
implementation  NONE
product bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

## 1. Scope

V353 closes the exact V346 `NON_PARTICLE_SUFFIX_ADJACENCY` three-row runtime/data-ownership investigation and records the newly discovered cross-carrier dependency.

```text
row 4743   partition 208   original 0x60248   PC-KO 0x78624
row 5059   partition 215   original 0x64898   PC-KO 0x7DC28
row 11440  partition 604   original 0xC3988   PC-KO 0xF3C9C
```

PC-Korean EVENT surfaces include `\%21는 것도`, `\%15는데`, and `\%2A는 건`. These `는` surfaces are not ordinary noun-particle cases; they follow runtime grammar-formatting macros.

## 2. Switch percent-macro owner

The Switch v1.1.3 EVENT escape path contains a bounded 52-entry `%xx` dispatch table at `RODATA 0x6AC004`. The two hexadecimal digits after `%` index the table. The selected value is passed to TAI5MSG getter `0x43F2A4`, which resolves `block = message_id / 1000` and `local = message_id % 1000`.

```text
\%15 -> 209 -> TAI5MSG block 0 / local 209
\%21 -> 349 -> TAI5MSG block 0 / local 349
\%2A -> 395 -> TAI5MSG block 0 / local 395
```

Machine-readable authority: `selective_ko/artifacts/ecf00000_v353_percent_macro_tai5msg_b0_cross_carrier_v1/SUFFIX3_MACRO_BINDINGS.jsonl`

## 3. PC patch source authority

Actual PC original and PC Korean TAI5MSG block-0 content confirms the semantic roots:

```text
0:209  JP negative-register family -> KO 없습니다 / 없다 / 없어요 family
0:349  JP 言ｲﾏｽ / 言ｳ family       -> KO 말합니다 / 말한다 family
0:395  JP ﾐﾏｼｮｳ / ﾐﾖｳ family      -> KO 봅시다 / 보자 family
```

The PC Korean block-0 formatter graph is already established as graph/control-preserving relative to PC original; Koreanization changes content/output fragments rather than installing a different formatter graph.

## 4. CWTDAT hypothesis rejected

PC original ↔ PC Korean CWTDAT comparison does not establish `%15/%21/%2A` grammar ownership. Observed CWTDAT patch changes belong to name/reading/sample-data surfaces, not these grammar roots.

`CWTDAT_GRAMMAR_OWNER = REJECTED`

## 5. Current selective TAI5MSG gap

The current selective TAI5MSG product has exactly two selected Korean block-0 messages: locals 10 and 11. Required suffix-three roots 209, 349, and 395 are all unselected JP.

Therefore EVENT-only Korean overlay can produce:

```text
Korean EVENT literal
+ Japanese TAI5MSG formatter expansion
+ Korean EVENT suffix
```

Raw-copying the three PC-Korean EVENT commands is therefore not authorized.

## 6. Escape-family correction

V347 remains valid for its bounded direct-particle responsibility result, but its simplified value/control model must not be generalized to every `%xx` macro. In this bounded family, `%xx` dispatches to a language-bearing TAI5MSG block-0 formatter message.

```text
EVENT byte-validity PASS
!=
runtime language-dependency PASS
```

V349/V352 serializer/relocation validation remains valid. V353 does not roll those implementations back; it adds a separate cross-carrier integration gate.

## 7. Broader impact boundary

The issue is no longer safely scoped to only the three V346 suffix rows. The 52-entry `%xx` table requires a bounded product census: used macros in product-admitted EVENT rows, exact B0 roots, current selective TAI5MSG language state, nested B0 dependencies, and the exact missing support closure.

Do not blindly enable all 52 roots. Earlier TAI5MSG grammar work established caller-local erasure/materialization/phrase-rewrite responsibilities for some formatter families.

## 8. Rejected / do-not-repeat

- CWTDAT owns the three grammar macros;
- `%15` means TAI5MSG local 0x15, `%21` local 0x21, etc.;
- suffix-three is EVENT-local;
- suffix `는` is an ordinary particle;
- raw-copy suffix-three EVENT commands before TAI5MSG support closure;
- generalize V347 value-only escape model to all `%xx`;
- enable all 52 B0 roots without dependency/caller-responsibility census;
- reopen V346 suffix membership.

## 9. Current product state

```text
code-5 structurally implemented/offline PASS   423 / 426
suffix-three DEFER                               3 / 426
percent-macro runtime-language integration      OPEN
product bytes                                   UNCHANGED
```

## 10. Exact next scope

`ECF00000_PERCENT_MACRO_TAI5MSG_B0_CROSS_CARRIER_DEPENDENCY_CENSUS_READ_ONLY`

Use the already-proven 52-entry table at `0x6AC004`; census only exact product-admitted EVENT rows; map used `%xx` to exact B0 roots; compare against current selective TAI5MSG membership; compute nested B0 dependency closure only for actually used roots; preserve earlier caller-responsibility policy. No EVENT/TAI5MSG mutation, build/package/IPS, or hardware.
