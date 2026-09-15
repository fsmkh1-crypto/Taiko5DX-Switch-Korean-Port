# FIXED PARTICLE POLICY

Date: 2026-09-15 (KST)
Status: CANONICAL SELECTIVE-KO PRODUCT POLICY / NO CORPUS REWRITE / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `SELECTIVE_KO_FIXED_PARTICLE_POLICY_MATERIALIZATION`
Policy ID: `FIXED_SURFACE_PARTICLE_V1`

## 1. Purpose

This policy fixes the first-release handling of Korean allomorphic particles when a runtime-inserted value would otherwise require pronunciation/final-consonant-dependent selection.

The selective release intentionally prefers broad, structurally stable Korean coverage over perfect particle agreement for this class.

This policy does **not** change the structural mechanism taxonomy. A row that is structurally `PARTICLE_SENSITIVE_INSERT` remains `PARTICLE_SENSITIVE_INSERT`. The release policy only supplies an approved surface choice for the particle responsibility.

Canonical release choice:

```text
particle_release_policy = FIXED_SURFACE_PARTICLE
particle_release_policy_version = FIXED_SURFACE_PARTICLE_V1
```

## 2. Authority and provenance

The policy consumes existing verified project evidence and does not reopen PC runtime reverse engineering.

Authority order remains:

```text
PC Korean translation/content/terminology     -> SOURCE_AUTHORITY
Switch script/control/owner/runtime structure -> STRUCTURAL_AUTHORITY
implementation                                -> Switch-native design
```

The relevant PC evidence is the canonical PC Korean-patched `TAI5MSG_JP.DAT` source used by the existing TAI5MSG parser/reconstruction path.

Canonical TAI5MSG identity already guarded by the repository:

```text
input SHA-256 = e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
blocks        = 33
messages      = 14,832
```

The fixed-particle read-only analysis on 2026-09-15 scanned the decoded canonical payload for explicit dual-form particle literals. It did not reanalyze `dinput8.dll` and did not create a build.

## 3. Fixed surface mapping

For first-release selective Korean output, the approved fixed forms are:

```text
은(는) / 는(은) -> 는
이(가) / 가(이) -> 가
을(를) / 를(을) -> 를
과(와) / 와(과) -> 와
(으)로 / 로(으) -> 로
```

The policy may also be applied to a separately proven particle-only selector leaf whose sole unresolved responsibility is choosing between the same allomorphic pair.

It must **not** be generalized into arbitrary substring replacement.

## 4. Exact applicability gate

A candidate is eligible for `FIXED_SURFACE_PARTICLE_V1` only when at least one of the following is proven:

1. the Korean source payload contains one of the explicit dual-form literals listed in section 3; or
2. a formatter/selector leaf is independently proven to own only the corresponding particle allomorph choice.

The following are not sufficient by themselves:

```text
mechanism_class = PARTICLE_SENSITIVE_INSERT
risk flag = PARTICLE_RISK
Japanese particle adjacency
presence of a person/place/item variable
surface text that merely looks particle-sensitive
```

Global replacement of ordinary standalone `은`, `는`, `이`, `가`, `을`, `를`, `과`, `와`, `으`, or `로` is forbidden.

## 5. Axis-independence rule

This is a release-surface policy, not a technical-axis shortcut.

Applying the policy must not silently change:

```text
mechanism_class
usage_class
investigation_status
switch_applicability
switch_realization
release_scope
```

In particular:

```text
PARTICLE_SENSITIVE_INSERT + FIXED_SURFACE_PARTICLE
!= VARIABLE_INSERT

FIXED_SURFACE_PARTICLE
!= DIRECT_DATA

FIXED_SURFACE_PARTICLE
!= IN_SCOPE
```

Applicability, realization, owner/caller closure, capacity/storage safety, and release scope continue to require their own evidence or explicit decision under the existing contracts.

## 6. Investigation effect

The policy may close only the narrow question:

> Which member of an allomorphic particle pair should the first-release surface use?

When that is the **only** remaining particle-specific uncertainty, pronunciation/final-consonant investigation is not required for first-release inclusion.

The original `PARTICLE_RISK` and structural mechanism classification must be preserved as provenance so a future grammar-accurate release can recover the affected population.

The policy does not close investigation for:

- unknown physical owner or caller topology;
- shared-owner conflicts;
- cross-message composition;
- copula/verb/speech-style/interrogative formatter responsibility;
- numeric-counter morphology;
- unknown Switch counterpart;
- unresolved storage/capacity/terminator safety;
- EVENT/TS5 locator determinism or serializer gaps.

## 7. PC TAI5MSG observed literal census

The read-only analysis of the canonical PC Korean-patched TAI5MSG found these exact dual-form literal occurrences:

| literal | occurrences |
|---|---:|
| `을(를)` | 94 |
| `이(가)` | 17 |
| `은(는)` | 15 |
| `와(과)` | 2 |
| `(으)로` | 2 |
| **total** | **130** |

Observed distribution:

```text
affected messages = 70
affected blocks   = 14
```

These counts are evidence for the policy and byte-impact contract. They do not authorize a corpus rewrite in this materialization stage.

## 8. Byte-impact contract

Under the canonical compact Korean encoding used by this source family, each Hangul particle character above occupies two bytes. Parentheses occupy one byte each.

Therefore each explicit dual-form literal is six payload bytes and the fixed single-particle result is two payload bytes:

```text
6 bytes -> 2 bytes
payload delta = -4 bytes per normalized occurrence
```

For the 130 observed TAI5MSG occurrences:

```text
aggregate semantic-payload delta = -520 bytes
```

This policy is therefore shrink-only for the explicit TAI5MSG dual-form literals.

Consequences:

```text
capacity escalation caused solely by this normalization = NOT_REQUIRED
message offsets after changed messages                  = MUST_RECOMPUTE
message boundaries                                      = MUST_REVALIDATE
trailing block padding                                  = MUST_REBUILD
container/output hashes and deterministic guards        = MUST_REFRESH
```

Shrink-only does not authorize raw in-place deletion without container reserialization.

## 9. TAI5MSG container boundary

TAI5MSG is a block container with message offset tables, payloads, and trailing block padding. Fixed-particle normalization therefore belongs in a future canonical TAI5MSG serializer/reconstruction stage, not in an arbitrary byte patch.

The read-only simulation against the existing compact-byte preservation reconstruction showed:

```text
current preservation reconstruction  -> 2 grown blocks / +128 bytes
fixed-particle normalization first    -> 1 grown block  /  +64 bytes
```

This is supporting analysis evidence, not a release-build invariant. Any implementation must recompute the result from canonical inputs and then validate deterministic output.

## 10. EVENT/TS5 boundary

The PC Korean EVENT/TS5 corpus also contains dual-form particle literals, but this policy does not authorize EVENT byte rewriting.

Until the EVENT/TS5 production structure adapter reaches its required locator-determinism and serializer gates:

```text
particle policy             = CANONICAL
eligible literal detection  = ALLOWED
production byte rewrite     = NOT AUTHORIZED
```

EVENT/TS5 implementation must preserve its own script/operand/container structure and cannot borrow the TAI5MSG serializer assumptions.

## 11. Grammar families not solved by this policy

`FIXED_SURFACE_PARTICLE_V1` does not solve dynamic Korean grammar generally.

The following remain separate mechanism/root-cause families:

- copula selection such as `입니다/이오/이다/이네`;
- verb/register realization;
- sentence endings;
- honorific/speech-style selection;
- interrogative forms;
- relation-dependent morphology;
- cross-message stem/suffix composition;
- numeric-counter morphology.

Known malformed-output families must not be reclassified as solved merely because a particle policy exists.

## 12. Forbidden shortcuts

The following are forbidden:

1. globally replacing ordinary Korean particles in translated text;
2. guessing Japanese-name pronunciation to choose a Korean particle for this release;
3. rewriting the whole sentence merely to avoid byte accounting;
4. changing `PARTICLE_SENSITIVE_INSERT` into `VARIABLE_INSERT` because a fixed particle is accepted;
5. using the policy to infer `DIRECT_DATA`, `IN_SCOPE`, or `INCLUDE_KO`;
6. applying TAI5MSG byte/layout assumptions to EVENT/TS5;
7. treating shrink-only payload change as permission for raw in-place deletion without offset regeneration;
8. claiming copula/ending/formatter families are solved by this policy.

## 13. Current materialization boundary

Materialized by this document:

- the first-release fixed particle product decision;
- exact approved particle mapping;
- applicability gate;
- axis-independence rule;
- narrow investigation-relief rule;
- TAI5MSG observed literal census;
- shrink-only byte-impact contract;
- TAI5MSG and EVENT/TS5 implementation boundaries.

Not materialized by this document:

- corpus classification rows;
- release-scope decisions for individual/batch candidates;
- TAI5MSG rewritten bytes;
- EVENT/TS5 rewritten bytes;
- serializer or builder changes;
- Switch realization/action units;
- IPS/build/runtime release artifact.

No existing corpus row is automatically reclassified or included merely because this policy is canonical.

## 14. Next-stage interaction

The next planned selective stage remains:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION
```

That stage may carry this policy as provenance, but it must not broadly populate particle-policy classifications or perform TAI5MSG/EVENT rewrites unless separately authorized.
