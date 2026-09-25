from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

BLOCK_COUNT = 33
HEADER_SIZE = 0x140
ALIGN = 0x40
RUNTIME_BLOCK_CAPACITY = 0x20000
BUILD_ID = "D9120950C258610A746F4A31CE3A3B376DE393D9"

BASE_TAI_SHA256 = "b41edad60a02824c8b3c025f54f9a26a073710c0ae397be8450ec0070e0cdd1f"
BASE_TAI_RECORDS = 14_832
BASE_IPS_SHA256 = "6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4"
BASE_IPS_RECORDS = 5

EXPECTED_TAI_SHA256 = "e8738545c3248db23dedbd4dff6ef7dc253b19260b6da613af0aa5186dc8cc28"
EXPECTED_TAI_SIZE = 2_195_465
EXPECTED_TAI_RECORDS = 15_460
EXPECTED_IPS_SHA256 = "dadb49f92fd66313145620194b05c108373f780f566bd5ba433f045e8acef7ec"
EXPECTED_IPS_SIZE = 2_999
EXPECTED_IPS_RECORDS = 18

INDEX_NAME = "INDEX.json"
MANIFEST_NAME = "TAIKO5DX_PRODUCT_LOWERING_MANIFEST_CORRECTED_20260925.json"
CALLER_PLAN_NAME = "TAIKO5DX_PRODUCT_LOWERING_PREFLIGHT_CALLER_BYTES_120_20260925.jsonl"
HELPER_PLAN_NAME = "TAIKO5DX_PRODUCT_LOWERING_PREFLIGHT_HELPER_BYTES_628_20260925.jsonl"
IPS_PLAN_NAME = "TAIKO5DX_BUFFER8_PREFLIGHT_IPS_RECORDS_13_20260925.json"


class ProductLoweringError(RuntimeError):
    pass


def fail(code: str, detail: str) -> None:
    raise ProductLoweringError(f"{code}: {detail}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def guarded_file(path: Path, expected_sha256: str, code: str) -> bytes:
    data = path.read_bytes()
    if sha256(data) != expected_sha256:
        fail(code, f"SHA-256 mismatch: {path}")
    return data


def align64(value: int) -> int:
    return (value + ALIGN - 1) & ~(ALIGN - 1)


def load_index(plan_dir: Path) -> dict:
    index = json.loads((plan_dir / INDEX_NAME).read_text(encoding="utf-8"))
    if index.get("schema") != "TAIKO5DX_PRODUCT_LOWERING_BUILDER_INPUT_V1":
        fail("PLAN_INDEX", "unexpected schema")
    if index.get("repository_head") != "46442da4a5b8767733aa4e3bc864ba21f5e718ce":
        fail("PLAN_INDEX", "repository head mismatch")
    expected = {row["path"]: row for row in index.get("files", [])}
    required = {MANIFEST_NAME, CALLER_PLAN_NAME, HELPER_PLAN_NAME, IPS_PLAN_NAME}
    if set(expected) != required:
        fail("PLAN_INDEX", f"unexpected plan files: {sorted(expected)}")
    for name, row in expected.items():
        p = plan_dir / name
        b = p.read_bytes()
        if len(b) != int(row["bytes"]) or sha256(b) != row["sha256"]:
            fail("PLAN_INDEX", f"input identity mismatch: {name}")
    return index


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def parse_baseline_tai(blob: bytes) -> tuple[bytearray, list[dict]]:
    if sha256(blob) != BASE_TAI_SHA256:
        fail("BASE_TAI_IDENTITY", "Diagnostic218 TAI5MSG SHA mismatch")
    if len(blob) < HEADER_SIZE:
        fail("BASE_TAI_PARSE", "truncated header")
    pairs = [struct.unpack_from("<II", blob, i * 8) for i in range(BLOCK_COUNT)]
    if pairs[0][0] != HEADER_SIZE:
        fail("BASE_TAI_PARSE", "first block offset mismatch")
    for i in range(BLOCK_COUNT - 1):
        off, declared = pairs[i]
        if off % ALIGN or declared % ALIGN or off + declared != pairs[i + 1][0]:
            fail("BASE_TAI_PARSE", f"block {i} header extent mismatch")
    blocks: list[dict] = []
    total = 0
    for bi, (off, declared) in enumerate(pairs):
        end = pairs[bi + 1][0] if bi < BLOCK_COUNT - 1 else len(blob)
        raw = blob[off:end]
        if bi < BLOCK_COUNT - 1 and len(raw) != declared:
            fail("BASE_TAI_PARSE", f"block {bi} physical/declaration mismatch")
        if len(raw) > declared:
            fail("BASE_TAI_PARSE", f"block {bi} physical > declared")
        plain = bytes((x + 0x5B) & 0xFF for x in raw)
        count = int.from_bytes(plain[:2], "little")
        table_end = 2 + 4 * count
        offsets = [int.from_bytes(plain[2 + 4 * i: 6 + 4 * i], "little") for i in range(count)]
        if not offsets or offsets[0] != table_end or any(offsets[i] >= offsets[i + 1] for i in range(count - 1)):
            fail("BASE_TAI_PARSE", f"block {bi} offset table invalid")
        used_end = len(plain)
        while used_end and plain[used_end - 1] == 0x5B:
            used_end -= 1
        messages = []
        for mi, start in enumerate(offsets):
            stop = offsets[mi + 1] if mi + 1 < count else used_end
            if not start < stop <= used_end:
                fail("BASE_TAI_PARSE", f"block {bi} message {mi} bounds")
            messages.append(plain[start:stop])
        blocks.append({
            "block": bi, "declared": declared, "physical": end - off,
            "messages": messages, "count": count,
        })
        total += count
    if total != BASE_TAI_RECORDS:
        fail("BASE_TAI_PARSE", f"record count {total} != {BASE_TAI_RECORDS}")
    return bytearray(blob[:HEADER_SIZE]), blocks


def compile_targets(blocks: list[dict], plan_dir: Path) -> list[list[bytes]]:
    manifest = json.loads((plan_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    if manifest.get("implementation_state") != "CORRECTED_MANIFEST_ADOPTED_IMPLEMENTATION_NOT_STARTED":
        fail("MANIFEST_STATE", "corrected manifest not adopted")
    if manifest["namespace"]["b0_final_count"] != 1000 or manifest["namespace"]["b7_final_count"] != 653:
        fail("MANIFEST_STATE", "namespace mismatch")

    callers = jsonl(plan_dir / CALLER_PLAN_NAME)
    helpers = jsonl(plan_dir / HELPER_PLAN_NAME)
    if len(callers) != 120 or len(helpers) != 628:
        fail("PLAN_COUNTS", f"caller/helper counts {len(callers)}/{len(helpers)}")

    targets = [list(block["messages"]) for block in blocks]
    seen_callers: set[tuple[int, int]] = set()
    for row in callers:
        locator = row["locator"]
        b = int(locator[1:].split(":")[0])
        local = int(locator.split(":")[1])
        key = (b, local)
        if key in seen_callers:
            fail("CALLER_DUPLICATE", locator)
        seen_callers.add(key)
        if b >= BLOCK_COUNT or local >= len(targets[b]):
            fail("CALLER_LOCATOR", locator)
        source = targets[b][local]
        if sha256(source) != row["source_sha256"] or source.hex() != row["source_hex"]:
            fail("CALLER_PREIMAGE", locator)
        target = bytes.fromhex(row["target_hex"])
        if sha256(target) != row["target_sha256"]:
            fail("CALLER_TARGET", locator)
        targets[b][local] = target

    seen_helpers: set[tuple[int, int]] = set()
    for row in helpers:
        locator = row["locator"]
        b = int(locator[1:].split(":")[0])
        local = int(locator.split(":")[1])
        key = (b, local)
        if key in seen_helpers:
            fail("HELPER_DUPLICATE", locator)
        seen_helpers.add(key)
        if b >= BLOCK_COUNT or local != len(targets[b]):
            fail("HELPER_ORDER", f"{locator}; next is B{b}:{len(targets[b])}")
        if row["global_id"] != b * 1000 + local:
            fail("HELPER_GLOBAL_ID", locator)
        target = bytes.fromhex(row["target_hex"])
        if len(target) != row["target_bytes"] or sha256(target) != row["target_sha256"]:
            fail("HELPER_TARGET", locator)
        targets[b].append(target)

    if len(targets[0]) != 1000 or len(targets[7]) != 653:
        fail("FINAL_NAMESPACE", f"B0/B7 = {len(targets[0])}/{len(targets[7])}")
    if sum(map(len, targets)) != EXPECTED_TAI_RECORDS:
        fail("FINAL_COUNT", str(sum(map(len, targets))))
    return targets


def serialize_expanded_tai(header: bytearray, baseline_blocks: list[dict], targets: list[list[bytes]]) -> tuple[bytes, list[dict]]:
    if len(targets) != BLOCK_COUNT:
        fail("SERIALIZE", "block count")
    out_header = bytearray(header)
    raw_blocks: list[bytes] = []
    metas: list[dict] = []
    file_offset = HEADER_SIZE
    for bi, messages in enumerate(targets):
        baseline = baseline_blocks[bi]
        table_end = 2 + 4 * len(messages)
        offsets = []
        cursor = table_end
        for msg in messages:
            offsets.append(cursor)
            cursor += len(msg)
        used_end = cursor
        if bi < BLOCK_COUNT - 1:
            declared = max(int(baseline["declared"]), align64(used_end))
            physical = declared
        else:
            declared = int(baseline["declared"])
            physical = int(baseline["physical"])
            if used_end > physical:
                fail("B32_CAPACITY", f"{used_end}>{physical}")
        if declared > RUNTIME_BLOCK_CAPACITY:
            fail("BLOCK_CAPACITY", f"B{bi} {declared}")
        plain = bytearray(struct.pack("<H", len(messages)))
        for offset in offsets:
            plain += struct.pack("<I", offset)
        plain += b"".join(messages)
        if len(plain) != used_end or len(plain) > physical:
            fail("SERIALIZE", f"B{bi} used-end")
        plain += bytes([0x5B]) * (physical - len(plain))
        encrypted = bytes((x - 0x5B) & 0xFF for x in plain)
        raw_blocks.append(encrypted)
        struct.pack_into("<II", out_header, bi * 8, file_offset, declared)
        metas.append({
            "block": bi, "offset": file_offset, "messages": len(messages),
            "used": used_end, "declared": declared, "physical": physical,
            "filler": physical - used_end,
        })
        file_offset += declared
    emitted = bytes(out_header) + b"".join(raw_blocks)
    if len(emitted) != EXPECTED_TAI_SIZE or sha256(emitted) != EXPECTED_TAI_SHA256:
        fail("TAI_OUTPUT_IDENTITY", f"{len(emitted)} {sha256(emitted)}")
    return emitted, metas


def independent_tai_readback(blob: bytes, expected: list[list[bytes]]) -> int:
    checked = 0
    for bi in range(BLOCK_COUNT):
        off = int.from_bytes(blob[8 * bi:8 * bi + 4], "little")
        end = int.from_bytes(blob[8 * (bi + 1):8 * (bi + 1) + 4], "little") if bi < BLOCK_COUNT - 1 else len(blob)
        plain = bytes((v + 91) & 255 for v in blob[off:end])
        count = int.from_bytes(plain[:2], "little")
        if count != len(expected[bi]):
            fail("TAI_READBACK", f"B{bi} count")
        offsets = [int.from_bytes(plain[2 + 4 * i:6 + 4 * i], "little") for i in range(count)]
        if not offsets or offsets[0] != 2 + 4 * count or any(offsets[i] >= offsets[i + 1] for i in range(count - 1)):
            fail("TAI_READBACK", f"B{bi} offsets")
        for mi, want in enumerate(expected[bi]):
            start = offsets[mi]
            if mi + 1 < count:
                got = plain[start:offsets[mi + 1]]
            else:
                got = plain[start:start + len(want)]
            if got != want:
                fail("TAI_READBACK", f"B{bi}:{mi}")
            checked += 1
    if checked != EXPECTED_TAI_RECORDS:
        fail("TAI_READBACK", f"checked {checked}")
    return checked


def parse_ips(blob: bytes) -> list[tuple[int, bytes]]:
    if not blob.startswith(b"PATCH") or not blob.endswith(b"EOF"):
        fail("IPS_PARSE", "framing")
    pos = 5
    end = len(blob) - 3
    rows: list[tuple[int, bytes]] = []
    while pos < end:
        if pos + 5 > end:
            fail("IPS_PARSE", "record header")
        off = int.from_bytes(blob[pos:pos + 3], "big"); pos += 3
        size = int.from_bytes(blob[pos:pos + 2], "big"); pos += 2
        if size == 0:
            fail("IPS_PARSE", "RLE not accepted in product-lowering input")
        payload = blob[pos:pos + size]; pos += size
        if len(payload) != size:
            fail("IPS_PARSE", "payload")
        rows.append((off, payload))
    if pos != end:
        fail("IPS_PARSE", "end boundary")
    return rows


def emit_ips(records: list[tuple[int, bytes]]) -> bytes:
    out = bytearray(b"PATCH")
    for off, payload in sorted(records):
        if not (0 <= off <= 0xFFFFFF) or not (1 <= len(payload) <= 0xFFFF):
            fail("IPS_EMIT", f"record 0x{off:X}")
        out += off.to_bytes(3, "big") + len(payload).to_bytes(2, "big") + payload
    out += b"EOF"
    return bytes(out)


def build_ips(baseline: bytes, plan_dir: Path) -> tuple[bytes, list[tuple[int, bytes]]]:
    if sha256(baseline) != BASE_IPS_SHA256:
        fail("BASE_IPS_IDENTITY", "Diagnostic218 IPS SHA mismatch")
    inherited = parse_ips(baseline)
    if len(inherited) != BASE_IPS_RECORDS:
        fail("BASE_IPS_IDENTITY", f"records {len(inherited)}")
    plan = json.loads((plan_dir / IPS_PLAN_NAME).read_text(encoding="utf-8"))
    if len(plan.get("inherited_ips_records", [])) != BASE_IPS_RECORDS or len(plan.get("new_records", [])) != 13:
        fail("IPS_PLAN", "record counts")
    for got, exp in zip(inherited, plan["inherited_ips_records"]):
        if got[0] != int(exp["offset"], 16) or got[1].hex() != exp["payload_hex"]:
            fail("IPS_PLAN", f"inherited mismatch at {exp['offset']}")
    records = list(inherited)
    for row in plan["new_records"]:
        records.append((int(row["offset"], 16), bytes.fromhex(row["replacement_hex"])))
    records.sort(key=lambda x: x[0])
    for (off_a, a), (off_b, b) in zip(records, records[1:]):
        if off_a + len(a) > off_b:
            fail("IPS_OVERLAP", f"0x{off_a:X} vs 0x{off_b:X}")
    emitted = emit_ips(records)
    if len(emitted) != EXPECTED_IPS_SIZE or sha256(emitted) != EXPECTED_IPS_SHA256:
        fail("IPS_OUTPUT_IDENTITY", f"{len(emitted)} {sha256(emitted)}")
    readback = parse_ips(emitted)
    if readback != records or len(readback) != EXPECTED_IPS_RECORDS:
        fail("IPS_READBACK", "record mismatch")
    return emitted, records


def build(baseline_tai_path: Path, baseline_ips_path: Path, plan_dir: Path, output_dir: Path) -> dict:
    load_index(plan_dir)
    baseline_tai = guarded_file(baseline_tai_path, BASE_TAI_SHA256, "BASE_TAI_IDENTITY")
    baseline_ips = guarded_file(baseline_ips_path, BASE_IPS_SHA256, "BASE_IPS_IDENTITY")
    header, blocks = parse_baseline_tai(baseline_tai)
    targets = compile_targets(blocks, plan_dir)
    tai, metas = serialize_expanded_tai(header, blocks, targets)
    checked = independent_tai_readback(tai, targets)
    ips, records = build_ips(baseline_ips, plan_dir)

    if output_dir.exists() and any(output_dir.iterdir()):
        fail("NO_OVERWRITE", str(output_dir))
    (output_dir / "romfs").mkdir(parents=True, exist_ok=True)
    (output_dir / "exefs").mkdir(parents=True, exist_ok=True)
    tai_path = output_dir / "romfs/TAI5MSG_JP.DAT"
    ips_path = output_dir / f"exefs/{BUILD_ID}.ips"
    tai_path.write_bytes(tai)
    ips_path.write_bytes(ips)
    receipt = {
        "schema":"TAIKO5DX_PRODUCT_LOWERING_BUILD_RECEIPT_V1",
        "status":"PASS_REPRODUCIBLE",
        "baseline_tai_sha256":sha256(baseline_tai),
        "baseline_ips_sha256":sha256(baseline_ips),
        "candidate_tai":{"bytes":len(tai),"sha256":sha256(tai),"records":EXPECTED_TAI_RECORDS},
        "candidate_ips":{"bytes":len(ips),"sha256":sha256(ips),"records":len(records)},
        "independent_tai_readback":checked,
        "B0":metas[0],
        "B7":metas[7],
        "builder_scope":"TAI5MSG_AND_IPS_ONLY_NO_EVENT_NO_PACKAGE_NO_RUNTIME",
    }
    (output_dir / "BUILD_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> None:
    p = argparse.ArgumentParser(description="Reproduce the Taiko5DX product-lowering TAI5MSG + IPS candidates.")
    p.add_argument("--baseline-tai", required=True, type=Path)
    p.add_argument("--baseline-ips", required=True, type=Path)
    p.add_argument("--plan-dir", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()
    receipt = build(a.baseline_tai, a.baseline_ips, a.plan_dir, a.output_dir)
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
