# PC runtime -> Switch counterpart status matrix

Date: 2026-09-11
Status: CLOSURE BASELINE / NO NEW SWITCH SURVEY

## 1. Purpose

This matrix keeps two dimensions separate:

- **PC specification status**: whether PHASE 1–4 closed the Windows reference behavior;
- **Switch counterpart status**: what is already known from pre-existing Switch evidence, without performing new counterpart research in closure.

A completed PC row does not imply the Switch port is complete or feasible by the same mechanism.

## 2. Switch status vocabulary

- `UNSURVEYED`: no counterpart decision has been made.
- `PARTIAL_EVIDENCE`: existing Switch evidence touches the same semantic family, but complete equivalence is not established.
- `COUNTERPART_REQUIRED`: existing evidence already shows the PC semantic requirement is not fully satisfied by the known Switch baseline.
- `COUNTERPART_FOUND`: all relevant Switch locations for the family have been enumerated statically; implementation is still a later stage.
- `NATIVE_EQUIVALENT_CANDIDATE`: concrete Switch code/data evidence supports possible native equivalence. This status requires evidence and must never be assigned from absence of symptoms or intuition.
- `NATIVE_EQUIVALENT_VERIFIED`: the family is demonstrated equivalent within the stated static/runtime scope and needs no port edit.
- `UNRESOLVED`: evidence exists but competing interpretations remain.

`NATIVE POSSIBLE` without evidence is not an allowed shortcut. Unknown means `UNSURVEYED`.

## 3. Functional-family matrix

| Functional family | PC specification | Existing Switch evidence before survey | Current Switch status | Storage/capacity question | Required next survey result |
|---|---|---|---|---|---|
| Mapping table content | 10,036 entries = 7,494 original + 2,542 Korean; mapping data alone 40,144 bytes | Switch conversion loops are still known to use 7,494 entries | `COUNTERPART_REQUIRED` | 2,542 additions must be represented somewhere unless an equivalent full table already exists elsewhere | identify actual table storage, all consumers, feasible expanded representation |
| Mapping references/counts | PC relocates table and changes 3 address operands + 2 counts | known Switch loop counts include `0x4303AC` and `0x430624`, but full reference family not surveyed | `PARTIAL_EVIDENCE` | depends on chosen expanded mapping placement | enumerate every semantic table-base/count consumer; no unique-match gate |
| Pointer mode 0 | 5 records -> two module-resident targets; 8-byte pointer writes | no canonical per-record Switch counterpart census | `UNSURVEYED` | may reuse existing Switch objects; no pool inherently required | classify all 5 records and their two semantic targets |
| Pointer mode 1 / pool | 51 records -> 47 distinct replacement strings in 602-byte pool | no canonical per-record Switch counterpart census | `UNSURVEYED` | pool-equivalent storage may be required unless existing objects can be reused | classify all 51 records, object ownership, sharing and target storage |
| Inline 17,103 | same-length PC replacement layer, priority 0 | historical 5,519 subset; repeated-object/fixed-field evidence; full release coverage not complete | `PARTIAL_EVIDENCE` | same-length objects need no new pool inherently; pointer-owned/repeated objects remain separate | object-level correspondence for full semantic coverage, not uniqueness filtering |
| `runtime_page_mapper` / helper `+0x00` | `EB..F8 -> pages 49..62`; fallback to original PC flow | Switch page-mapper work around mapped `0x44650C` is already established | `PARTIAL_EVIDENCE` | helper storage may be avoidable if existing ARM64 path can be edited in place | prove all relevant Switch page-mapping paths and semantic equivalence |
| `runtime_byte_validation` / helper `+0x20` | direct accepted 1/2-byte copy path; fallback resumes original flow | per-character path around `0x445C60` accepts `A1..DF`; this does not prove all copy/validation paths are equivalent | `PARTIAL_EVIDENCE` | helper storage may be avoidable if equivalent in-place control flow exists | enumerate byte-copy/validation paths; determine whether any drops/transforms compact single-byte data |
| `font_page_limit` raw threshold | one PC compare `0xFF -> 0xA0` | W0 six `0x100 -> 0xA1` sites and W1 seventh width/layout site exist, but causal/equivalence claims are limited | `PARTIAL_EVIDENCE` | likely in-place if counterparts are instruction edits | classify all semantically corresponding Switch threshold/width sites; do not infer from W0/W1 alone |
| `ui_width_1..4` | four literal changes `170/150 -> 200` | no canonical Switch counterpart census | `UNSURVEYED` | likely in-place if equivalents exist | identify actual Switch role and all same-semantic sites |
| `description_font_1..2` | two argument changes `5 -> 4` | no canonical Switch counterpart census | `UNSURVEYED` | likely in-place if equivalents exist | identify Switch semantic equivalent or establish native equivalence with evidence |
| Descriptor search machinery | x86 `.text` masked unique search + exact anchor | not portable by byte signature | `UNRESOLVED` as port mechanism; semantic counterparts only | none required as a literal runtime mechanism | do not port x86 signature search; use it only as PC provenance |
| PC allocation/protection machinery | one contiguous VirtualAlloc split into prefix/helper regions, later R/RX | Windows-specific | not a Switch functional requirement | Switch needs only sufficient storage/addressability for chosen design | survey target memory/data layout after counterparts are known |
| Fail-closed transaction | preimage guard, overlap rejection, priority commit, best-effort rollback | eventual offline builder already has target guards in other areas; no new closure analysis | `UNSURVEYED` for final release integration | no runtime cave requirement by itself | later builder/release-validator design, not counterpart code survey |
| CWTDAT direct-copy compatibility | PC file was copied in Stage-1 control; DLL did not execute | structural PC/Switch compatibility is not proven by that control | `UNRESOLVED` | separate RomFS/data-layout question | explicit structure/version compatibility check on a later authorized data pass |

## 4. Storage risk by axis

### Mapping — highest currently identified capacity risk

The PC semantic requirement contains 2,542 mappings beyond the original 7,494. If the Switch original table has only the known 7,494-entry footprint and no equivalent expanded table elsewhere, those entries require additional capacity somewhere. Closure does not choose whether that capacity is a contiguous unused region, repurposed data, another static object, or another safe representation.

### Pointer replacement strings

The PC implementation stores 602 bytes in a private pool. Switch may need new storage, but per-record analysis could prove that some/all required strings already exist as suitable objects. Do not assume either outcome before the 56-record survey.

### Helper semantics

PC uses 158 bytes of new x86-64 helper code. Switch need not mirror that implementation. Existing ARM64 functions may support equivalent behavior through in-place edits; therefore helper code space is unresolved rather than presumed mandatory.

### Descriptor literal families

The width/font/threshold edits may be implementable in place. Their risk is counterpart completeness, not necessarily space.

## 5. Compact `쓰` symptom status

Do not use this symptom to collapse the survey scope. Three unresolved paths remain in parallel:

| Path | Existing evidence | Status |
|---|---|---|
| data selection / active fixed field | two Switch `松平元康` fixed fields were missed by the historical unique-only selector; active rendered slot is not established | `UNRESOLVED` |
| pointer/reference selection | pointer 56 is a first-class PC layer, but per-record Switch correspondence has not been surveyed | `UNSURVEYED` |
| byte-validation/copy | basic Switch decode accepts `A1..DF`, but another path could still differ; PC has a separate copy/control-flow hook | `PARTIAL_EVIDENCE` |

W1 only invalidates the claim that mapped `0x44D9D0` by itself is the direct missing-`쓰` cause. It does not select one of the three paths above.

## 6. PCREF1 gate

PCREF1 emitted-IPS reverse verification is **not** a prerequisite for static counterpart discovery. It is a prerequisite before interpreting the first new counterpart-derived runtime build, because otherwise a no-change screen can remain ambiguous between counterpart error and patch-delivery error.

Therefore later work may run:

```text
Switch counterpart survey  ||  PCREF1 delivery verification
```

but must satisfy:

```text
PCREF1 delivery state closed
    BEFORE
counterpart-derived runtime result is used as causal evidence
```

## 7. Closure boundary

This file does not add new Switch counterpart findings. It freezes the starting classification for the next authorized survey.

STOP.
