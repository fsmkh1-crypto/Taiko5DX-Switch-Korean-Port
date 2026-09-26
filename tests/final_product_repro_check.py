from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

BUILD_ID = "D9120950C258610A746F4A31CE3A3B376DE393D9"
EXPECTED_ROOT_TAI = "8c9a70575258fad362c0197c8b59190fd332843195f35e185894ee34fe6547b1"
EXPECTED_FINAL_TAI = "1b44170a817e047ba942ba10e46571049ff7405c7fac4278c3e1598089efd61e"
EXPECTED_IPS = "28c423a0a8e805308f8e935f2a3f5304fe12e3f948ca6468c46dd72a96cdcfae"
REJECTED_IPS = "dadb49f92fd66313145620194b05c108373f780f566bd5ba433f045e8acef7ec"
EXPECTED_RUNTIME_ZIP = "cfd14031bab300929a9926bae9bb82bf28f21a9d417aee50ca527b88df873c91"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run_builder(builder: Path, baseline_tai: Path, baseline_ips: Path, main: Path, plan_dir: Path, out: Path, expect_ok: bool = True):
    cmd = [
        sys.executable, str(builder), "--baseline-tai", str(baseline_tai),
        "--baseline-ips", str(baseline_ips), "--main", str(main),
        "--plan-dir", str(plan_dir), "--output-dir", str(out),
    ]
    cp = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if expect_ok and cp.returncode != 0:
        raise RuntimeError(f"builder failed:\nSTDOUT={cp.stdout}\nSTDERR={cp.stderr}")
    if not expect_ok and cp.returncode == 0:
        raise RuntimeError("negative builder test unexpectedly passed")
    return cp


def parse_tai_counts(blob: bytes) -> tuple[int, list[int]]:
    pairs = [struct.unpack_from("<II", blob, i * 8) for i in range(33)]
    counts = []
    for bi, (off, declared) in enumerate(pairs):
        end = pairs[bi + 1][0] if bi < 32 else len(blob)
        raw = blob[off:end]
        plain = bytes((x + 0x5B) & 0xFF for x in raw)
        counts.append(struct.unpack_from("<H", plain, 0)[0])
    return sum(counts), counts


def parse_ips(blob: bytes) -> list[tuple[int, bytes]]:
    if not blob.startswith(b"PATCH") or not blob.endswith(b"EOF"):
        raise RuntimeError("IPS framing")
    pos = 5; end = len(blob) - 3; rows = []
    while pos < end:
        off = int.from_bytes(blob[pos:pos+3], "big"); pos += 3
        size = int.from_bytes(blob[pos:pos+2], "big"); pos += 2
        if size == 0: raise RuntimeError("RLE not expected")
        payload = blob[pos:pos+size]; pos += size
        rows.append((off, payload))
    if pos != end: raise RuntimeError("IPS boundary")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--builder", required=True, type=Path)
    ap.add_argument("--baseline-tai", required=True, type=Path)
    ap.add_argument("--baseline-ips", required=True, type=Path)
    ap.add_argument("--main", required=True, type=Path)
    ap.add_argument("--plan-dir", required=True, type=Path)
    ap.add_argument("--runtime-reference-zip", required=True, type=Path)
    a = ap.parse_args()

    if sha(a.runtime_reference_zip.read_bytes()) != EXPECTED_RUNTIME_ZIP:
        raise RuntimeError("runtime reference ZIP identity mismatch")

    with tempfile.TemporaryDirectory(prefix="taiko_final_repro_") as td:
        root = Path(td)
        out1 = root / "run1"; out2 = root / "run2"
        r1 = run_builder(a.builder, a.baseline_tai, a.baseline_ips, a.main, a.plan_dir, out1)
        r2 = run_builder(a.builder, a.baseline_tai, a.baseline_ips, a.main, a.plan_dir, out2)

        t1 = (out1 / "romfs/TAI5MSG_JP.DAT").read_bytes()
        t2 = (out2 / "romfs/TAI5MSG_JP.DAT").read_bytes()
        i1 = (out1 / f"exefs/{BUILD_ID}.ips").read_bytes()
        i2 = (out2 / f"exefs/{BUILD_ID}.ips").read_bytes()
        if t1 != t2 or i1 != i2:
            raise RuntimeError("two clean builds differ")
        if sha(t1) != EXPECTED_FINAL_TAI or sha(i1) != EXPECTED_IPS:
            raise RuntimeError("final hashes mismatch")
        if sha(i1) == REJECTED_IPS:
            raise RuntimeError("rejected boot-freeze IPS reproduced")

        total, counts = parse_tai_counts(t1)
        if total != 16153 or (counts[0], counts[7], counts[18], counts[23]) != (1000, 653, 909, 617):
            raise RuntimeError(f"TAI counts mismatch: total={total}, selected={counts[0]}/{counts[7]}/{counts[18]}/{counts[23]}")
        ips_rows = parse_ips(i1)
        if len(ips_rows) != 18:
            raise RuntimeError("IPS count mismatch")

        # Independent equality against the user-observed runtime-pass reference.
        with zipfile.ZipFile(a.runtime_reference_zip) as z:
            names = z.namelist()
            roots = {n.split('/')[0] for n in names if '/' in n}
            if len(roots) != 1:
                raise RuntimeError("runtime ZIP root ambiguity")
            zr = next(iter(roots)) + "/"
            ref_tai = z.read(zr + "romfs/TAI5MSG_JP.DAT")
            ref_ips = z.read(zr + f"exefs/{BUILD_ID}.ips")
            if t1 != ref_tai or i1 != ref_ips:
                raise RuntimeError("builder outputs differ from runtime-pass game payloads")

            carrier = json.loads((a.plan_dir / "CARRIER_MANIFEST_14.json").read_text(encoding="utf-8"))
            checked = 0
            for row in carrier["files"]:
                b = z.read(zr + row["path"])
                if len(b) != row["bytes"] or sha(b) != row["sha256"]:
                    raise RuntimeError(f"carrier mismatch: {row['path']}")
                checked += 1
            if checked != 14:
                raise RuntimeError("carrier count mismatch")

        # Negative 1: baseline TAI identity must fail closed.
        bad_tai = root / "bad_tai.dat"
        b = bytearray(a.baseline_tai.read_bytes()); b[-1] ^= 1; bad_tai.write_bytes(b)
        cp = run_builder(a.builder, bad_tai, a.baseline_ips, a.main, a.plan_dir, root / "bad_out1", expect_ok=False)
        if "BASE_TAI_IDENTITY" not in (cp.stderr + cp.stdout):
            raise RuntimeError("baseline TAI negative test failed for wrong reason")

        # Negative 2: Switch main identity must fail closed before NSO/preimage use.
        bad_main = root / "bad_main"
        b = bytearray(a.main.read_bytes()); b[-1] ^= 1; bad_main.write_bytes(b)
        cp = run_builder(a.builder, a.baseline_tai, a.baseline_ips, bad_main, a.plan_dir, root / "bad_out2", expect_ok=False)
        if "MAIN_IDENTITY" not in (cp.stderr + cp.stdout):
            raise RuntimeError("main negative test failed for wrong reason")

        # Negative 3: tampered frozen plan with unchanged INDEX must fail PLAN_INDEX.
        bad_plan = root / "bad_plan"; shutil.copytree(a.plan_dir, bad_plan)
        p = bad_plan / "ROOTCAUSE223_CALLER_BYTES_430.jsonl"
        raw = bytearray(p.read_bytes()); raw[100] ^= 1; p.write_bytes(raw)
        cp = run_builder(a.builder, a.baseline_tai, a.baseline_ips, a.main, bad_plan, root / "bad_out3", expect_ok=False)
        if "PLAN_INDEX" not in (cp.stderr + cp.stdout):
            raise RuntimeError("plan negative test failed for wrong reason")

        result = {
            "schema":"TAIKO5DX_FINAL_PRODUCT_REPRO_CHECK_V1",
            "status":"PASS",
            "clean_builds":2,
            "two_builds_byte_exact":True,
            "final_tai":{"bytes":len(t1),"sha256":sha(t1),"records":total,"B0":counts[0],"B7":counts[7],"B18":counts[18],"B23":counts[23]},
            "final_ips":{"bytes":len(i1),"sha256":sha(i1),"records":len(ips_rows),"rejected_sha_not_emitted":True},
            "runtime_reference":{"zip_sha256":EXPECTED_RUNTIME_ZIP,"tai_byte_exact":True,"ips_byte_exact":True,"carrier_files_byte_exact":"14/14"},
            "negative_tests":{"baseline_tai_identity":"PASS","main_identity":"PASS","plan_index_tamper":"PASS"},
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
