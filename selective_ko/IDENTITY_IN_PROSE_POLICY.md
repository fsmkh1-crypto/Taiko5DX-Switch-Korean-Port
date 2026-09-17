# IDENTITY IN PROSE POLICY

Date: 2026-09-17 (KST)
Status: CANONICAL SELECTIVE-KO PRODUCT POLICY / NO GAMEPLAY REWRITE / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Policy ID: `IDENTITY_IN_PROSE_V1`

## 1. Purpose

This policy closes the product decision for person/place identity tokens that appear inside Korean explanatory, narrative, event, or dialogue prose.

The selective product deliberately accepts a low-cost presentation mismatch in exchange for avoiding name/yomi/CWTDAT/name-composition rework.

## 2. Canonical product decision

For the first selective release:

```text
identity presentation fields            -> KEEP_JP
PC Korean prose literals                -> PRESERVE_AS_AUTHORED_KO
runtime-inserted person/place identity   -> KEEP_JP
prose-literal reverse substitution       -> FORBIDDEN
```

Interpretation:

- dedicated person-name fields remain Japanese;
- dedicated place-name fields remain Japanese;
- yomi/readings/sort keys remain Japanese;
- surname/given-name composition remains Japanese;
- calendar/name-entry identity behavior remains Japanese;
- when the PC Korean translation already contains a Korean-rendered person/place name as ordinary prose text, that prose is preserved as authored;
- when the Switch runtime inserts a person/place identity variable, the inserted identity remains the Japanese original;
- the project does not create a transform that searches Korean prose and converts embedded Korean names/places back to Japanese.

Therefore mixed presentation such as a Japanese identity field and Korean prose spelling for the same person/place is explicitly acceptable for this release.

## 3. Authority boundary

This policy does not weaken source/structure authority separation.

```text
PC Korean prose content/terminology      -> SOURCE_AUTHORITY
Switch identity fields/runtime tokens    -> STRUCTURAL_AUTHORITY / KEEP_JP PRODUCT POLICY
implementation                           -> Switch-native design
```

Preserving an authored Korean prose literal is not person-name Koreanization. It is preservation of the selected Korean sentence payload.

Likewise, keeping a runtime identity token Japanese is not a translation defect. It is the product boundary.

## 4. No identity normalization transform

The first release must not add any of the following merely for visual consistency:

- Korean-name -> Japanese-name replacement inside prose;
- Japanese-name -> Korean-name replacement in identity fields;
- CWTDAT/yomi modification;
- surname/given-name composition modification;
- pronunciation inference for Japanese identity tokens;
- global morphology rewrite around mixed-script identities.

Any future identity normalization feature is a separate optional product scope and requires a fresh explicit authorization.

## 5. Particle / grammar interaction

This policy does not claim that every mixed Japanese/Korean sentence is grammatically safe.

For runtime-inserted Japanese identity tokens:

- `FIXED_SURFACE_PARTICLE_V1` may be used only where its existing exact applicability gate is satisfied;
- unknown caller/owner/cross-message/formatter/counter responsibilities remain unresolved;
- no pronunciation guessing is introduced;
- no mechanism class is changed merely because identity presentation is Japanese.

For Korean identity names already present as ordinary prose literals, no identity-specific transform is required. They remain part of the authored Korean payload and are evaluated under the same structural/capacity/owner gates as the surrounding sentence.

## 6. Classification metadata rule

Future corpus materialization should carry the product-policy state explicitly when identity content is present.

Recommended field:

```text
identity_token_policy
```

Allowed first-release values:

```text
KEEP_JP_IDENTITY_FIELD
PRESERVE_AUTHORED_KO_PROSE_LITERAL
KEEP_JP_RUNTIME_INSERT
NOT_APPLICABLE
```

This field is product metadata only. It must not silently change:

```text
mechanism_class
usage_class
investigation_status
switch_applicability
switch_realization
derived_disposition
```

`INCLUDE_KO` still requires the normal owner/caller/risk/capacity/provenance gates.

## 7. Mixed-script requirement

The policy permits mixed Japanese/Korean surfaces but does not globally prove every route safe.

For any selected family where Japanese runtime identity and Korean prose coexist, the actual Switch route must preserve:

- Japanese code-space/font behavior;
- Korean Mapping 10,036/font behavior;
- transport/normalization behavior for both scripts.

Historical mixed-script output is supporting evidence, not a universal route-wide proof.

## 8. Scope effect

This policy closes the V293 unresolved product decision:

```text
identity_in_prose_policy = RESOLVED_IDENTITY_IN_PROSE_V1
```

It does not:

- create corpus rows;
- issue candidate/classification IDs;
- rewrite TAI5MSG/EVENT/UI payloads;
- authorize person/place-name Koreanization;
- implement CWTDAT/yomi/name composition;
- implement a builder;
- create IPS/build/runtime artifacts.

The existing next selective read-only scope remains the cross-container content/field availability inventory. That inventory may now measure identity-in-prose exposure for coverage/QA planning, not to decide this policy again.

## 9. Do-not-repeat rule

Do not reopen this decision merely because Japanese identity fields and Korean prose spellings differ visually.

The mismatch is an intentional first-release cost tradeoff.

Reopen only if the user explicitly authorizes an identity-normalization product scope.
