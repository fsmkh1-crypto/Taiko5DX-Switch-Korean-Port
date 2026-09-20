# ECF00000 0x1E SEMANTIC ADMISSION LEDGER MATERIALIZATION — V341

Date: 2026-09-20 (KST)

```text
validation_id   V341
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      LEDGER_MATERIALIZATION_AND_REPLAY_VALIDATION
parent          96153e28f1437c29285cefc06a9b14028367a1a2 / V340
scope           ECF00000_1E_SEMANTIC_ADMISSION_LEDGER_MATERIALIZATION
product_bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

V341 materializes the exact `0x1E` semantic classification established by the preceding READ ONLY audit. It does not apply any `0x1E` replacement to a product TS5 and does not resume S4.

## 1. Exact inputs

```text
stock ECF00000.TS5
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09

PC-KO ECF00000.TS5
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
```

Original and PC-KO `0x1E` objects map partition-locally by `0x1E` ordinal:

```text
original 1E rows          461
PC-KO 1E rows             461
partitions containing 1E   42
partition count mismatch    0
header mismatch             0
changed                   388
byte-identical             73
```

No final-Korean fresh parse is used as ownership authority.

## 2. Switch runtime role

Bounded Switch-main analysis identified `0x1E` as a string-slot assignment command. The header selects a string slot and the following string payload becomes that slot value. This matters because many apparently ordinary short strings are actually dynamic identity/name material rather than general prose.

The identity policy therefore remains binding:

```text
dedicated person/name identity   KEEP_JP
non-identity semantic label      PC-KO candidate
byte-identical object             preserve original
```

## 3. Exact semantic partition

The complete 461-row family is classified without unresolved semantic rows:

```text
KEEP_JP_IDENTITY             344
PRESERVE_IDENTICAL            73
semantic PC-KO candidates     44
-------------------------------
TOTAL                         461
semantic unresolved            0
```

Identity subtypes:

```text
PERSONAL_NAME                         103
CLAN_KABANE_IDENTITY_COMPOSITE         24
DYNAMIC_NAME_SLOT_Z001                216
NAMED_PERSON_HONORIFIC                  1
-----------------------------------------
KEEP_JP_IDENTITY                      344
```

The 216 `DYNAMIC_NAME_SLOT_Z001` rows are 24 repetitions of nine source strings (`国 / 徳 / 愛 / 義 / 豪 / 初 / 早川 / 永 / 冬`). They set string slot 1 and are subsequently referenced as dynamic identity through `\Z001`; they are not admitted merely because some individual tokens are ordinary words in isolation.

Semantic PC-KO candidate subtypes:

```text
STATUS_ROLE                 11
COURT_OFFICE                 3
POLITICAL_REGIME_TITLE      14
MARTIAL_ART_LABEL            6
ITEM_WEAPON_CATEGORY         9
KINSHIP_RELATION             1
------------------------------
semantic candidates         44
```

## 4. Runtime-admission split

Semantic admissibility is not equated with runtime admission.

The inherited V333 conservative MAY-reachable graph contains 179 `0x1E` logical objects. V340 corrected its residual-error gate but did not redefine MAY-reachable membership as exact gameplay feasibility.

Crossing the 44 semantic candidates with that graph produces:

```text
INCLUDE_KO_READY             23
INCLUDE_KO_RUNTIME_PENDING   21
```

`INCLUDE_KO_READY` subtype distribution:

```text
STATUS_ROLE                 11
COURT_OFFICE                 3
POLITICAL_REGIME_TITLE       4
ITEM_WEAPON_CATEGORY         4
KINSHIP_RELATION             1
------------------------------
TOTAL                       23
```

Ready row original labels:

```text
大名 / 武士 / 忍者 / 海賊 / 商人 / 浪人
征夷大将軍 / 関白 / 太政大臣
\#17F5幕府 / 将軍 / 室町幕府 / 将軍
浪人 / 武士 / 商人 / 忍び / 海賊
槍 / 苦無 / 鎖鎌 / 種子島
兄上
```

Ready growth if later materialized from PC-KO:

```text
rows          23
same length   21
+4 bytes       2
net growth    +8 bytes
partitions     0 / 11 / 72 / 161 / 681
```

The two +4 rows are `室町幕府` and `種子島`.

The 21 semantically valid but non-MAY rows remain `INCLUDE_KO_RUNTIME_PENDING`:

```text
POLITICAL_REGIME_TITLE      10
MARTIAL_ART_LABEL            6
ITEM_WEAPON_CATEGORY         5
------------------------------
TOTAL                       21
```

They are not promoted solely because their meanings are translatable.

## 5. Canonical artifact

Repository artifact directory:

`selective_ko/artifacts/ecf00000_v341_1e_semantic_admission_v1/`

Compact ledger:

```text
file         LEDGER_COMPACT.bin
records      461
record size   18 bytes
size        8,298 bytes
serialization
<HHIIHHBB
  partition:u16
  ordinal:u16
  original_offset:u32
  ko_offset:u32
  original_length:u16
  ko_length:u16
  disposition:u8
  subtype:u8
sha256      4e84b8278e1fe6b13a7945c6ba13a5b2922cb686b79746a510c92fd2ce856b35
```

Disposition codes:

```text
0 PRESERVE_IDENTICAL
1 KEEP_JP_IDENTITY
2 INCLUDE_KO_READY
3 INCLUDE_KO_RUNTIME_PENDING
```

A human-readable `LEDGER.jsonl`, exact V333 MAY-reachable `0x1E` rowset, replay validation, INDEX, and manifest are stored beside the compact ledger.

## 6. Exact rowset gates

All rowsets serialize each row as:

`<HHII = partition:u16 + ordinal:u16 + original_offset:u32 + ko_offset:u32>`

```text
all 461
50f296c1fa044020d48024c52b41f9409e06c453d24dff5d7a8c3257f01b1046

changed 388
51c4cc5846b20023879b5aee64219eeb9f0770d309cde4fbe1d7278a222a89cc

KEEP_JP_IDENTITY 344
9cd043a25c74f1be3a8581c2beb9738bf0723dfcb095a4c852f18e295c2a261f

PRESERVE_IDENTICAL 73
b413f729be26351a12ba85f2c95e0ee3955f065453193fbefc747d634320a03f

semantic PC-KO candidates 44
e9387e902b795a675c496a3208604670c13a17ba97924b89daeaf0dab124802a

INCLUDE_KO_READY 23
0011c816ae8519750c79b3a1917b830decce3b7f466fe6735212f433859fc38d

INCLUDE_KO_RUNTIME_PENDING 21
42d87f675644aeaf995e9a3beac217acdb21164b10b3e3d2461feeec9f4566cd

MAY-reachable 1E 179
883bfcc51b919cd62adadd05991c409c7ddb2dd7bd642ed8a0a1ff488cff03c9
```

## 7. Replay validation

Materialization replay gates:

```text
input identity                 PASS
mapping rows                   461 / 461
partition count mismatch       0
header mismatch                0
semantic unresolved            0
exact disposition counts       PASS
all required rowset hashes     PASS
compact ledger deterministic   PASS
product bytes changed          NO
```

## 8. Rejected / do-not-repeat

Reject:

- copy all 461 PC-KO `0x1E` objects;
- copy all 388 changed `0x1E` objects;
- treat only the 103 obvious personal names as identity;
- translate the 216 dynamic `\Z001` name-slot fragments as ordinary words;
- translate the 24 clan/kabane identity composites;
- treat `秀吉ｻﾏ` as a generic honorific label;
- equate the 44 semantically translatable rows with immediate runtime admission;
- promote the 21 runtime-pending rows without additional provenance;
- reopen the V340 `0x0E` residual as an `0x1E` omission problem.

## 9. Scope boundary / next

V341 materializes classification only. It does not implement the 23 ready replacements.

```text
V336 S1 serializer core       CLOSED
V337 generic relocation       CLOSED
V338 special spans            CLOSED
V339 5A composite             CLOSED
V340 residual gate            CLOSED
V341 1E semantic ledger       MATERIALIZED

1E ready replacements         23 / NOT IMPLEMENTED
1E runtime pending            21
3C                            KEEP_JP / not materialized
code-3 fixed particle         OPEN
full S4                       NOT RESUMED
product/build/package/IPS     NONE
```

Exact next scope after a fresh explicit user signal:

`ECF00000_1E_INCLUDE_KO_READY_23_IMPLEMENTATION_OFFLINE_VALIDATION`

Implement and offline-validate only the 23 `INCLUDE_KO_READY` rows using exact PC-KO payload bytes, then run existing V337/V338/V339/V340 structural gates. Do not promote the 21 runtime-pending rows, implement code-3 particles, resume full S4, build/package/IPS, or run hardware in that scope.
