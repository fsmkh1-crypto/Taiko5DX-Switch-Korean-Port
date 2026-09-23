from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Mapping, Sequence

V356_DIR = Path("selective_ko/artifacts/ecf00000_v356_percent_macro_b0_46_root_serializer_admission_v1")
V356_SCHEMA = "ECF00000_V356_PERCENT_MACRO_B0_46_ROOT_SERIALIZER_ADMISSION_V1"
V356_ROWS_BYTES = 11_742
V356_ROWS_SHA256 = "55d79c420255b2efdd01df859089f2b83048a1fd3ada721bb1739e933306ab80"
EXPECTED_ROOTS = 46
EXPECTED_PAYLOAD_DELTA = 578
EXPECTED_SOURCE_BYTES = 13_916
EXPECTED_TARGET_BYTES = 14_494
EXPECTED_BLOCK = 0
EXPECTED_STOCK_IDENTITY = {
    "size": 1_810_889,
    "sha256": "aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f",
}
EXPECTED_PC_KO_IDENTITY = {
    "size": 2_134_366,
    "sha256": "e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090",
}


class PercentMacroRootError(RuntimeError):
    pass


@dataclass(frozen=True)
class PercentMacroRootSpec:
    block: int
    local: int
    source_length: int
    target_length: int
    delta: int
    source_sha256: str
    target_sha256: str

    @property
    def locator(self) -> tuple[int, int]:
        return self.block, self.local


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fail(message: str) -> None:
    raise PercentMacroRootError(message)


def load_v356_percent_macro_root_specs(repo_root: Path) -> dict[tuple[int, int], PercentMacroRootSpec]:
    root = repo_root / V356_DIR
    index = json.loads((root / "INDEX.json").read_text(encoding="utf-8"))
    admission = json.loads((root / "ADMISSION.json").read_text(encoding="utf-8"))

    for obj, label in ((index, "index"), (admission, "admission")):
        if obj.get("schema") != V356_SCHEMA or obj.get("validation_id") != "V356":
            _fail(f"unexpected V356 {label} identity")
        if obj.get("result") != "PASS_EXACT_46_ROOT_SERIALIZER_ADMISSION":
            _fail(f"unexpected V356 {label} result")

    if index.get("rows_file") != "ADMISSION_ROWS.json" or admission.get("rows_file") != "ADMISSION_ROWS.json":
        _fail("V356 rows file binding mismatch")
    source_identity = admission.get("source_identity", {})
    if source_identity.get("pc_original") != EXPECTED_STOCK_IDENTITY:
        _fail("V356 stock identity mismatch")
    if source_identity.get("pc_korean") != EXPECTED_PC_KO_IDENTITY:
        _fail("V356 PC-KO identity mismatch")

    membership = admission.get("membership", {})
    expected_membership = {
        "roots": EXPECTED_ROOTS,
        "unique_locators": EXPECTED_ROOTS,
        "block": EXPECTED_BLOCK,
        "current_v303_b0_locals": [10, 11],
        "v303_overlap": 0,
        "source_bytes_total": EXPECTED_SOURCE_BYTES,
        "target_bytes_total": EXPECTED_TARGET_BYTES,
        "payload_delta": EXPECTED_PAYLOAD_DELTA,
    }
    if membership != expected_membership:
        _fail("V356 membership/census contract mismatch")

    rows_raw = (root / "ADMISSION_ROWS.json").read_bytes()
    if len(rows_raw) != V356_ROWS_BYTES or _sha(rows_raw) != V356_ROWS_SHA256:
        _fail("V356 rows transport identity mismatch")
    rows = json.loads(rows_raw.decode("utf-8"))
    if not isinstance(rows, list) or len(rows) != EXPECTED_ROOTS:
        _fail("V356 row count mismatch")

    out: dict[tuple[int, int], PercentMacroRootSpec] = {}
    source_total = 0
    target_total = 0
    delta_total = 0
    for row in rows:
        spec = PercentMacroRootSpec(
            block=int(row["block"]),
            local=int(row["local"]),
            source_length=int(row["source_length"]),
            target_length=int(row["target_length"]),
            delta=int(row["delta"]),
            source_sha256=str(row["source_sha256"]),
            target_sha256=str(row["target_sha256"]),
        )
        if spec.block != EXPECTED_BLOCK or spec.local < 0:
            _fail(f"V356 locator outside B0: {spec.locator}")
        if row.get("changed") is not True or spec.source_sha256 == spec.target_sha256:
            _fail(f"V356 source/target change contract failed at {spec.locator}")
        if spec.delta != spec.target_length - spec.source_length:
            _fail(f"V356 delta mismatch at {spec.locator}")
        if spec.locator in out:
            _fail(f"duplicate V356 locator: {spec.locator}")
        out[spec.locator] = spec
        source_total += spec.source_length
        target_total += spec.target_length
        delta_total += spec.delta

    if len(out) != EXPECTED_ROOTS:
        _fail("V356 unique locator count mismatch")
    if source_total != EXPECTED_SOURCE_BYTES or target_total != EXPECTED_TARGET_BYTES:
        _fail("V356 aggregate byte census mismatch")
    if delta_total != EXPECTED_PAYLOAD_DELTA:
        _fail("V356 aggregate payload delta mismatch")
    return out


def resolve_v356_percent_macro_root_targets(
    stock_messages: Sequence[Sequence[bytes]],
    pc_ko_messages: Sequence[Sequence[bytes]],
    specs: Mapping[tuple[int, int], PercentMacroRootSpec],
) -> dict[tuple[int, int], bytes]:
    if len(specs) != EXPECTED_ROOTS:
        _fail("V356 spec count mismatch before resolution")

    out: dict[tuple[int, int], bytes] = {}
    for locator, spec in specs.items():
        block, local = locator
        if block >= len(stock_messages) or block >= len(pc_ko_messages):
            _fail(f"V356 block out of range: {locator}")
        if local >= len(stock_messages[block]) or local >= len(pc_ko_messages[block]):
            _fail(f"V356 local out of range: {locator}")

        source = stock_messages[block][local]
        target = pc_ko_messages[block][local]
        if len(source) != spec.source_length or _sha(source) != spec.source_sha256:
            _fail(f"V356 stock source guard failed at {locator}")
        if len(target) != spec.target_length or _sha(target) != spec.target_sha256:
            _fail(f"V356 PC-KO target guard failed at {locator}")
        if source == target:
            _fail(f"V356 source/target unexpectedly identical at {locator}")
        out[locator] = target

    if len(out) != EXPECTED_ROOTS:
        _fail("V356 resolved root count mismatch")
    return out
