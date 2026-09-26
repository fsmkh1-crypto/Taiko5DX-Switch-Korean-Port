from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

import lz4.block

BLOCK_COUNT = 33
HEADER_SIZE = 0x140
ALIGN = 0x40
RUNTIME_BLOCK_CAPACITY = 0x20000
BUILD_ID = "D9120950C258610A746F4A31CE3A3B376DE393D9"
INDEX_NAME = "INDEX.json"
CALLER_PLAN_NAME = "ROOTCAUSE223_CALLER_BYTES_430.jsonl"
HELPER_PLAN_NAME = "ROOTCAUSE223_HELPER_BYTES_1321.jsonl"
B23_PLAN_NAME = "B23_REFLOW_MANIFEST_617.jsonl"
IPS_PLAN_NAME = "BUFFER8_IPS_PLAN_V2.json"


class FinalProductError(RuntimeError):
    pass


def fail(code: str, detail: str) -> None:
    raise FinalProductError(f"{code}: {detail}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def align64(value: int) -> int:
    return (value + ALIGN - 1) & ~(ALIGN - 1)


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def guard_bytes(path: Path, expected: dict, code: str) -> bytes:
    data = path.read_bytes()
    if len(data) != int(expected["bytes"]) or sha256(data) != expected["sha256"]:
        fail(code, f"identity mismatch: {path}")
    return data


def load_index(plan_dir: Path) -> dict:
    index = json.loads((plan_dir / INDEX_NAME).read_text(encoding="utf-8"))
    if index.get("schema") != "TAIKO5DX_FINAL_PRODUCT_BUILDER_INPUT_V1":
        fail("PLAN_INDEX", "unexpected schema")
    required = {
        CALLER_PLAN_NAME, HELPER_PLAN_NAME, B23_PLAN_NAME, IPS_PLAN_NAME,
        "CARRIER_MANIFEST_14.json", "PACKAGE_LAYOUT.json",
    }
    rows = {row["path"]: row for row in index.get("files", [])}
    if set(rows) != required:
        fail("PLAN_INDEX", f"unexpected plan files: {sorted(rows)}")
    for name, row in rows.items():
        b = (plan_dir / name).read_bytes()
        if len(b) != int(row["bytes"]) or sha256(b) != row["sha256"]:
            fail("PLAN_INDEX", f"identity mismatch: {name}")
    return index


def parse_tai(blob: bytes, expected_records: int | None = None) -> tuple[bytearray, list[dict]]:
    if len(blob) < HEADER_SIZE:
        fail("TAI_PARSE", "truncated header")
    pairs = [struct.unpack_from("<II", blob, i * 8) for i in range(BLOCK_COUNT)]
    if pairs[0][0] != HEADER_SIZE:
        fail("TAI_PARSE", "first block offset mismatch")
    for i in range(BLOCK_COUNT - 1):
        off, declared = pairs[i]
        if off % ALIGN or declared % ALIGN or off + declared != pairs[i + 1][0]:
            fail("TAI_PARSE", f"block {i} header extent mismatch")
    blocks = []
    total = 0
    for bi, (off, declared) in enumerate(pairs):
        end = pairs[bi + 1][0] if bi < BLOCK_COUNT - 1 else len(blob)
        raw = blob[off:end]
        if bi < BLOCK_COUNT - 1 and len(raw) != declared:
            fail("TAI_PARSE", f"block {bi} physical/declaration mismatch")
        if len(raw) > declared:
            fail("TAI_PARSE", f"block {bi} physical > declared")
        plain = bytes((x + 0x5B) & 0xFF for x in raw)
        if len(plain) < 2:
            fail("TAI_PARSE", f"block {bi} truncated")
        count = int.from_bytes(plain[:2], "little")
        table_end = 2 + 4 * count
        if table_end > len(plain):
            fail("TAI_PARSE", f"block {bi} offset table truncated")
        offsets = [int.from_bytes(plain[2 + 4 * i:6 + 4 * i], "little") for i in range(count)]
        if not offsets or offsets[0] != table_end or any(offsets[i] >= offsets[i + 1] for i in range(count - 1)):
            fail("TAI_PARSE", f"block {bi} offset table invalid")
        used_end = len(plain)
        while used_end and plain[used_end - 1] == 0x5B:
            used_end -= 1
        messages = []
        for mi, start in enumerate(offsets):
            stop = offsets[mi + 1] if mi + 1 < count else used_end
            if not start < stop <= used_end:
                fail("TAI_PARSE", f"B{bi}:{mi} bounds")
            messages.append(plain[start:stop])
        blocks.append({
            "block": bi, "declared": declared, "physical": end - off,
            "messages": messages, "count": count, "used_end": used_end,
        })
        total += count
    if expected_records is not None and total != expected_records:
        fail("TAI_PARSE", f"record count {total} != {expected_records}")
    return bytearray(blob[:HEADER_SIZE]), blocks


def compile_rootcause223(baseline_blocks: list[dict], plan_dir: Path, index: dict) -> list[list[bytes]]:
    callers = load_jsonl(plan_dir / CALLER_PLAN_NAME)
    helpers = load_jsonl(plan_dir / HELPER_PLAN_NAME)
    if len(callers) != index["counts"]["callers"] or len(helpers) != index["counts"]["helpers"]:
        fail("PLAN_COUNTS", f"caller/helper = {len(callers)}/{len(helpers)}")
    targets = [list(b["messages"]) for b in baseline_blocks]

    seen = set()
    for row in callers:
        loc = row["locator"]
        b = int(loc[1:].split(":")[0]); m = int(loc.split(":")[1])
        if (b, m) in seen:
            fail("CALLER_DUPLICATE", loc)
        seen.add((b, m))
        if b >= BLOCK_COUNT or m >= len(targets[b]):
            fail("CALLER_LOCATOR", loc)
        source = targets[b][m]
        if len(source) != int(row["source_bytes"]) or sha256(source) != row["source_sha256"] or source.hex() != row["source_hex"]:
            fail("CALLER_PREIMAGE", loc)
        target = bytes.fromhex(row["target_hex"])
        if len(target) != int(row["target_bytes"]) or sha256(target) != row["target_sha256"]:
            fail("CALLER_TARGET", loc)
        targets[b][m] = target

    seen_h = set()
    for row in helpers:
        loc = row["locator"]
        b = int(loc[1:].split(":")[0]); m = int(loc.split(":")[1])
        if (b, m) in seen_h:
            fail("HELPER_DUPLICATE", loc)
        seen_h.add((b, m))
        if b >= BLOCK_COUNT or m != len(targets[b]):
            fail("HELPER_ORDER", f"{loc}; expected B{b}:{len(targets[b])}")
        if int(row["global_id"]) != b * 1000 + m:
            fail("HELPER_GLOBAL_ID", loc)
        target = bytes.fromhex(row["target_hex"])
        if len(target) != int(row["target_bytes"]) or sha256(target) != row["target_sha256"]:
            fail("HELPER_TARGET", loc)
        targets[b].append(target)

    if (len(targets[0]), len(targets[7]), len(targets[18])) != (1000, 653, 909):
        fail("FINAL_NAMESPACE", f"B0/B7/B18={len(targets[0])}/{len(targets[7])}/{len(targets[18])}")
    if sum(map(len, targets)) != int(index["rootcause223_expected"]["records"]):
        fail("FINAL_COUNT", str(sum(map(len, targets))))
    return targets


def serialize_tai(header: bytearray, baseline_blocks: list[dict], targets: list[list[bytes]]) -> tuple[bytes, list[dict]]:
    out_header = bytearray(header)
    raw_blocks = []
    metrics = []
    file_offset = HEADER_SIZE
    for bi, messages in enumerate(targets):
        baseline = baseline_blocks[bi]
        table_end = 2 + 4 * len(messages)
        offsets = []
        cursor = table_end
        for msg in messages:
            offsets.append(cursor); cursor += len(msg)
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
            fail("BLOCK_CAPACITY", f"B{bi} declared=0x{declared:X}")
        plain = bytearray(struct.pack("<H", len(messages)))
        for off in offsets:
            plain += struct.pack("<I", off)
        plain += b"".join(messages)
        if len(plain) != used_end or len(plain) > physical:
            fail("TAI_SERIALIZE", f"B{bi} used/physical")
        plain += bytes([0x5B]) * (physical - len(plain))
        encrypted = bytes((x - 0x5B) & 0xFF for x in plain)
        raw_blocks.append(encrypted)
        struct.pack_into("<II", out_header, bi * 8, file_offset, declared)
        metrics.append({
            "block": bi, "messages": len(messages), "used": used_end,
            "declared": declared, "physical": physical,
            "spare_to_runtime_cap": RUNTIME_BLOCK_CAPACITY - declared,
        })
        file_offset += declared
    return bytes(out_header) + b"".join(raw_blocks), metrics


def independent_tai_readback(blob: bytes, expected: list[list[bytes]]) -> int:
    _, parsed = parse_tai(blob, expected_records=sum(map(len, expected)))
    checked = 0
    for bi in range(BLOCK_COUNT):
        if len(parsed[bi]["messages"]) != len(expected[bi]):
            fail("TAI_READBACK", f"B{bi} count")
        for mi, want in enumerate(expected[bi]):
            if parsed[bi]["messages"][mi] != want:
                fail("TAI_READBACK", f"B{bi}:{mi}")
            checked += 1
    return checked


def _lead(x: int) -> bool:
    return 0x81 <= x <= 0x9F or 0xE0 <= x <= 0xFC


def text_width(line: bytes) -> int:
    w = 0; p = 0
    while p < len(line):
        x = line[p]
        if x == 0x0A:
            fail("B23_WIDTH", "LF inside line")
        if x == 0x02 and p + 2 < len(line):
            p += 3; continue
        if x in (0x1A, 0x1B) and p + 1 < len(line):
            sub = line[p + 1]; p += 3 if sub == 0x43 and p + 2 < len(line) else 2; continue
        if x == 0x01 and p + 1 < len(line):
            sub = line[p + 1]; p += 4 if sub in (0x43, 0x4A) and p + 3 < len(line) else 2; continue
        if x == 0x05:
            if p + 2 < len(line) and line[p + 1] == 0x05:
                p += 3
            else:
                p += 1
            continue
        if _lead(x) and p + 1 < len(line):
            w += 2; p += 2; continue
        if x >= 0x20:
            w += 1
        p += 1
    return w


def line_widths(msg: bytes) -> list[int]:
    out = []; start = 0
    for i, b in enumerate(msg):
        if b == 0x0A:
            out.append(text_width(msg[start:i])); start = i + 1
    out.append(text_width(msg[start:]))
    return out


def apply_b23_reflow(rootcause_targets: list[list[bytes]], plan_dir: Path, index: dict) -> tuple[list[list[bytes]], dict]:
    rows = load_jsonl(plan_dir / B23_PLAN_NAME)
    if len(rows) != index["counts"]["b23_rows"]:
        fail("B23_PLAN", f"rows={len(rows)}")
    targets = [list(block) for block in rootcause_targets]
    if len(targets[23]) != 617:
        fail("B23_PLAN", f"B23 count={len(targets[23])}")
    changed = edits = s2n = n2s = 0
    for mi, row in enumerate(rows):
        if row["locator"] != f"B23:{mi}":
            fail("B23_PLAN", f"locator at {mi}")
        source = targets[23][mi]
        if len(source) != int(row["source_length"]) or sha256(source) != row["source_sha256"]:
            fail("B23_PREIMAGE", f"B23:{mi}")
        target = bytearray(source)
        for e in row["edits"]:
            pos = int(e["offset"]); old = int(e["from"], 16); new = int(e["to"], 16)
            if not (0 <= pos < len(target)) or target[pos] != old:
                fail("B23_EDIT_PREIMAGE", f"B23:{mi}+0x{pos:X}")
            if (old, new) not in ((0x20, 0x0A), (0x0A, 0x20)):
                fail("B23_NON_WHITESPACE", f"B23:{mi}+0x{pos:X}")
            target[pos] = new; edits += 1; s2n += (old, new) == (0x20, 0x0A); n2s += (old, new) == (0x0A, 0x20)
        target = bytes(target)
        for p in row["structural_lf_offsets"]:
            if source[p] != 0x0A or target[p] != 0x0A:
                fail("B23_STRUCTURAL_LF", f"B23:{mi}+0x{p:X}")
        if sha256(target) != row["target_sha256"]:
            fail("B23_TARGET", f"B23:{mi}")
        if line_widths(target) != row["target_line_widths"] or max(row["target_line_widths"] or [0]) > 32:
            fail("B23_WIDTH", f"B23:{mi}")
        if target != source:
            changed += 1
        targets[23][mi] = target
    if (changed, edits, s2n, n2s) != (462, 1844, 1179, 665):
        fail("B23_ACCOUNTING", f"{changed}/{edits}/{s2n}/{n2s}")
    return targets, {"changed": changed, "edits": edits, "space_to_lf": s2n, "lf_to_space": n2s}


def parse_ips(blob: bytes) -> list[tuple[int, bytes]]:
    if not blob.startswith(b"PATCH") or not blob.endswith(b"EOF"):
        fail("IPS_PARSE", "framing")
    pos = 5; end = len(blob) - 3; rows = []
    while pos < end:
        if pos + 5 > end:
            fail("IPS_PARSE", "record header")
        off = int.from_bytes(blob[pos:pos + 3], "big"); pos += 3
        size = int.from_bytes(blob[pos:pos + 2], "big"); pos += 2
        if size == 0:
            fail("IPS_PARSE", "RLE not accepted")
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
            fail("IPS_EMIT", f"0x{off:X}")
        out += off.to_bytes(3, "big") + len(payload).to_bytes(2, "big") + payload
    out += b"EOF"
    return bytes(out)


class NsoMappedImage:
    def __init__(self, nso: bytes):
        if nso[:4] != b"NSO0":
            fail("MAIN_PARSE", "not NSO0")
        flags = struct.unpack_from("<I", nso, 0x0C)[0]
        self.segments: list[tuple[int, bytes]] = []
        headers = [(0x10, 0x60, 0), (0x20, 0x64, 1), (0x30, 0x68, 2)]
        for hoff, csoff, bit in headers:
            file_off, mem_off, decomp_size = struct.unpack_from("<III", nso, hoff)
            comp_size = struct.unpack_from("<I", nso, csoff)[0]
            if flags & (1 << bit):
                src = nso[file_off:file_off + comp_size]
                try:
                    data = lz4.block.decompress(src, uncompressed_size=decomp_size)
                except Exception as e:
                    fail("MAIN_PARSE", f"LZ4 segment {bit}: {e}")
            else:
                data = nso[file_off:file_off + decomp_size]
            if len(data) != decomp_size:
                fail("MAIN_PARSE", f"segment {bit} size")
            self.segments.append((mem_off, data))
        self.segments.sort()

    def read(self, address: int, size: int) -> bytes:
        # NSO virtual memory is zero-filled between loaded segments (including rodata tail to data).
        out = bytearray(size)
        for mem_off, data in self.segments:
            a0 = max(address, mem_off)
            a1 = min(address + size, mem_off + len(data))
            if a0 < a1:
                out[a0 - address:a1 - address] = data[a0 - mem_off:a1 - mem_off]
        return bytes(out)


def build_ips(baseline_ips: bytes, main: bytes, plan_dir: Path, index: dict) -> tuple[bytes, dict]:
    plan = json.loads((plan_dir / IPS_PLAN_NAME).read_text(encoding="utf-8"))
    inherited = parse_ips(baseline_ips)
    if len(inherited) != int(index["baseline_ips"]["records"]):
        fail("IPS_BASE", f"records={len(inherited)}")
    mapped = NsoMappedImage(main)
    records = list(inherited)
    preimage_checked = 0
    for row in plan["records"]:
        if row.get("coordinate_domain") != "MAPPED_NSO":
            fail("IPS_COORDINATE", row["record_id"])
        moff = int(row["mapped_offset"], 16)
        eoff = int(row["emitted_offset"], 16)
        if eoff != moff + 0x100:
            fail("IPS_COORDINATE", f"{row['record_id']} +0x100")
        pre = bytes.fromhex(row["preimage_hex"])
        if mapped.read(moff, len(pre)) != pre:
            fail("IPS_MAIN_PREIMAGE", f"{row['record_id']} at 0x{moff:X}")
        repl = bytes.fromhex(row["replacement_hex"])
        if not repl:
            fail("IPS_PLAN", f"empty {row['record_id']}")
        records.append((eoff, repl))
        preimage_checked += 1
    records.sort(key=lambda x: x[0])
    for (a, pa), (b, pb) in zip(records, records[1:]):
        if a + len(pa) > b:
            fail("IPS_OVERLAP", f"0x{a:X} vs 0x{b:X}")
    emitted = emit_ips(records)
    exp = index["final_ips_expected"]
    if len(emitted) != int(exp["bytes"]) or len(records) != int(exp["records"]) or sha256(emitted) != exp["sha256"]:
        fail("IPS_OUTPUT_IDENTITY", f"{len(emitted)} {len(records)} {sha256(emitted)}")
    if parse_ips(emitted) != records:
        fail("IPS_READBACK", "record mismatch")
    # Explicit coordinate readback contract.
    for row in plan["records"]:
        eoff = int(row["emitted_offset"], 16); moff = eoff - 0x100
        if moff != int(row["mapped_offset"], 16):
            fail("IPS_READBACK", row["record_id"])
    return emitted, {"records": len(records), "new_preimages_checked": preimage_checked}


def build(baseline_tai_path: Path, baseline_ips_path: Path, main_path: Path, plan_dir: Path, output_dir: Path) -> dict:
    index = load_index(plan_dir)
    baseline_tai = guard_bytes(baseline_tai_path, index["baseline_tai"], "BASE_TAI_IDENTITY")
    baseline_ips = guard_bytes(baseline_ips_path, index["baseline_ips"], "BASE_IPS_IDENTITY")
    main = guard_bytes(main_path, index["main"], "MAIN_IDENTITY")

    header, blocks = parse_tai(baseline_tai, expected_records=index["baseline_tai"]["records"])
    root_targets = compile_rootcause223(blocks, plan_dir, index)
    root_tai, root_metrics = serialize_tai(header, blocks, root_targets)
    root_exp = index["rootcause223_expected"]
    if len(root_tai) != int(root_exp["bytes"]) or sha256(root_tai) != root_exp["sha256"]:
        fail("ROOTCAUSE223_OUTPUT_IDENTITY", f"{len(root_tai)} {sha256(root_tai)}")
    root_readback = independent_tai_readback(root_tai, root_targets)

    final_targets, b23_receipt = apply_b23_reflow(root_targets, plan_dir, index)
    final_tai, final_metrics = serialize_tai(header, blocks, final_targets)
    final_exp = index["final_tai_expected"]
    if len(final_tai) != int(final_exp["bytes"]) or sha256(final_tai) != final_exp["sha256"]:
        fail("FINAL_TAI_OUTPUT_IDENTITY", f"{len(final_tai)} {sha256(final_tai)}")
    final_readback = independent_tai_readback(final_tai, final_targets)

    ips, ips_receipt = build_ips(baseline_ips, main, plan_dir, index)

    if output_dir.exists() and any(output_dir.iterdir()):
        fail("NO_OVERWRITE", str(output_dir))
    (output_dir / "romfs").mkdir(parents=True, exist_ok=True)
    (output_dir / "exefs").mkdir(parents=True, exist_ok=True)
    (output_dir / "romfs/TAI5MSG_JP.DAT").write_bytes(final_tai)
    (output_dir / f"exefs/{BUILD_ID}.ips").write_bytes(ips)
    receipt = {
        "schema": "TAIKO5DX_FINAL_PRODUCT_BUILD_RECEIPT_V1",
        "status": "PASS_REPRODUCIBLE",
        "baseline_tai_sha256": sha256(baseline_tai),
        "baseline_ips_sha256": sha256(baseline_ips),
        "main_sha256": sha256(main),
        "rootcause223": {"bytes": len(root_tai), "records": sum(map(len, root_targets)), "sha256": sha256(root_tai), "readback": root_readback},
        "b23": b23_receipt,
        "final_tai": {"bytes": len(final_tai), "records": sum(map(len, final_targets)), "sha256": sha256(final_tai), "readback": final_readback},
        "final_ips": {"bytes": len(ips), "records": ips_receipt["records"], "sha256": sha256(ips), "mapped_preimages_checked": ips_receipt["new_preimages_checked"]},
        "selected_block_metrics": {"B0": final_metrics[0], "B7": final_metrics[7], "B18": final_metrics[18], "B23": final_metrics[23]},
        "builder_scope": "FINAL_TAI5MSG_AND_IPS_ONLY_NO_EVENT_MUTATION_NO_INSTALL_ZIP_NO_RUNTIME",
    }
    (output_dir / "BUILD_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


def main_cli() -> None:
    p = argparse.ArgumentParser(description="Reproduce the runtime-pass Taiko5DX final TAI5MSG + corrected IPS from Diagnostic218 inputs.")
    p.add_argument("--baseline-tai", required=True, type=Path)
    p.add_argument("--baseline-ips", required=True, type=Path)
    p.add_argument("--main", required=True, type=Path)
    p.add_argument("--plan-dir", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()
    receipt = build(a.baseline_tai, a.baseline_ips, a.main, a.plan_dir, a.output_dir)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main_cli()
