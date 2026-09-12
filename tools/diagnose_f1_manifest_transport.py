#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import io
import json
import re
from pathlib import Path

PATH = Path("docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST")
EXPECTED_CONTENT_SHA256 = "c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff"
EXPECTED_HISTORICAL_GZIP_SHA256 = "8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68"
EXPECTED_SOURCE_IDS_SHA256 = "87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e"
EXPECTED_ROWS = 158


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


idx_raw = (PATH / "INDEX.json").read_bytes()
idx = json.loads(idx_raw)
parts = idx["current_transport"]["parts"]
names = [p["name"] for p in parts]
assert names == [f"part-{i:02d}.jsonl" for i in range(1, 21)]
assert idx["current_transport"]["shard_count"] == 20
assert {p.name for p in PATH.iterdir() if p.is_file()} == {"INDEX.json", *names}

logical = bytearray()
rows = []
for part in parts:
    raw = (PATH / part["name"]).read_bytes()
    assert len(raw) == part["bytes"]
    assert sha256(raw) == part["sha256"]
    assert raw.endswith(b"\n")
    parsed = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    assert len(parsed) == part["rows"]
    assert parsed[0]["authorization_action_id"] == part["first_action_id"]
    assert parsed[-1]["authorization_action_id"] == part["last_action_id"]
    logical.extend(raw)
    rows.extend(parsed)

logical = bytes(logical)
source_ids_sha = sha256("\n".join(row["source_id"] for row in rows).encode("utf-8"))
out = io.BytesIO()
with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0, compresslevel=9) as gz:
    gz.write(logical)
historical_gzip_sha = sha256(out.getvalue())

print(f"transport_index_sha256={sha256(idx_raw)}")
print(f"shards={len(parts)}")
print(f"rows={len(rows)}")
print(f"logical_content_sha256={sha256(logical)}")
print(f"ordered_source_ids_sha256={source_ids_sha}")
print(f"reconstructed_historical_gzip_sha256={historical_gzip_sha}")
print(f"failed_transports_recorded={len(idx.get('failed_transports', []))}")

if not (
    len(rows) == EXPECTED_ROWS
    and sha256(logical) == EXPECTED_CONTENT_SHA256
    and source_ids_sha == EXPECTED_SOURCE_IDS_SHA256
    and historical_gzip_sha == EXPECTED_HISTORICAL_GZIP_SHA256
):
    raise SystemExit(2)
raise SystemExit(0)
