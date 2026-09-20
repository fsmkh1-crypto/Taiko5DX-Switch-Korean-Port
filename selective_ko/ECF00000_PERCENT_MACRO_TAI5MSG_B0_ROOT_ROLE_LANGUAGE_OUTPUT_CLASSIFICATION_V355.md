# ECF00000 percent-macro ↔ TAI5MSG B0 root role / language-output classification — V355

Date: 2026-09-20 (KST)

```text
validation_id   V355
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CLOSURE
parent          4632e5bb3c8e8b303526d696436ad8944406b104 / V354
implementation  NONE
product bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

## 1. Scope and source authority

This scope inspects only the exact 46 B0 roots frozen by V354. PC source identities are the V314 canonical fast-cache identities: original TAI5MSG `aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f` and PC Korean v1.02 TAI5MSG `e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090`. No full 14,832-message scan, V288 grammar rescan, EVENT mutation, build, package, IPS, or hardware work was performed.

## 2. Exact classification result

```text
exact roots                         46
PC original != PC Korean            46 / 46
current Switch selective state      JP preserved 46 / 46
selector-program roots              42
short direct-literal roots           4
PC-KO aggregate payload delta      +578 bytes
positive-delta roots                44
zero-delta roots                     2
negative-delta roots                 0
```

The four short direct-literal roots are `%26 -> B0:M357`, `%2B -> B0:M373`, `%2F -> B0:M358`, and `%30 -> B0:M374`. The other 42 are self-contained selector programs whose payloads choose authored surface variants according to existing control state.

All 46 PC-Korean roots differ from the PC-original root at the same locator. There is therefore no language-neutral exception among the product-used 46-root set.

Machine-readable authority: `artifacts/ecf00000_v355_percent_macro_b0_root_role_classification_v1/ROOT_ROLE_CLASSIFICATION.json`.

## 3. Role conclusion

The 46 roots are authored language-output data, not merely neutral dispatch metadata. They cover self-reference/address selection, honorific/relationship terms, copula and verb morphology, request/volitional/past/negative surfaces, response/interjection fragments, and honorific prefixes.

The PC patch oracle translates these roots in place at the same B0 locators. This is materially stronger than inferring a Korean surface from EVENT callers: the actual PC patch supplies the replacement bytes and preserves the root's selector/control structure.

## 4. Nested-dependency boundary

No separate nested-root traversal subset is established by this bounded comparison.

The 42 long roots are selector programs, but their PC-Korean counterparts are self-contained replacements at the same locator. Their internal branch/control structure is not evidence of a second TAI5MSG root dependency. The four short roots are direct literals.

Accordingly:

```text
nested dependency subset requiring graph expansion   0 / 46
same-locator PC-KO replacement candidates           46 / 46
implementation authorization                         NOT YET
```

This does not authorize mutation yet. The next gate is serializer/capacity admission for the exact 46-root set, including block-0 growth and interaction with the existing V309 selective TAI5MSG serializer.

## 5. Impact range

V354's 2,440 product-admitted `%xx` occurrences all resolve through these 46 roots. Since every root is currently JP-preserved and every PC-Korean same-locator root is changed, the gap is systematic across the full used-token set rather than limited to the V353 suffix-three anchors.

The exact caller-local responsibility rule remains unchanged: this finding concerns the macro root output only and does not authorize unrelated EVENT text flattening or global grammar rewrites.

## 6. Rejected / do-not-repeat

- do not treat the 42 selector programs as 42 reasons to rescan all TAI5MSG;
- do not infer a nested dependency merely from local branch/control structure;
- do not hand-translate the roots: PC Korean replacement bytes exist and are the oracle;
- do not patch only `%15/%21/%2A`; they are three witnesses of a 46-root cause family;
- do not globally replace unrelated B0 messages;
- do not implement before exact 46-root serializer/capacity admission is closed.

## 7. Exact next scope

`ECF00000_PERCENT_MACRO_TAI5MSG_B0_46_ROOT_REPLACEMENT_PREIMPLEMENTATION_CAPACITY_AND_SERIALIZER_ADMISSION_READ_ONLY`

READ ONLY only. Admit exactly the V355 46-root set against the existing selective TAI5MSG serializer, calculate B0 declared/used growth and package impact, and define a guarded same-locator PC-KO overlay contract. No mutation, build/package/IPS, or hardware.
