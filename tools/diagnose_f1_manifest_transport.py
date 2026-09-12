#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import json
import zlib
from pathlib import Path

PATH = Path("docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz")
EXPECTED_FILE_SHA256 = "8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68"
EXPECTED_CONTENT_SHA256 = "c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff"
EXPECTED_ROWS = 158

raw = PATH.read_bytes()
repo_sha = hashlib.sha256(raw).hexdigest()
print(f"repository_bytes={len(raw)}")
print(f"repository_file_sha256={repo_sha}")
print(f"expected_file_sha256={EXPECTED_FILE_SHA256}")

try:
    payload = gzip.decompress(raw)
    eof = True
except (EOFError, gzip.BadGzipFile, zlib.error):
    dec = zlib.decompressobj(16 + zlib.MAX_WBITS)
    payload = dec.decompress(raw)
    try:
        payload += dec.flush()
    except zlib.error:
        pass
    eof = dec.eof

print(f"gzip_eof={eof}")
print(f"recovered_payload_bytes={len(payload)}")
print(f"recovered_payload_sha256={hashlib.sha256(payload).hexdigest()}")
print(f"expected_content_sha256={EXPECTED_CONTENT_SHA256}")

lines = payload.splitlines(keepends=True)
complete_rows = 0
bad_line = None
bad_error = None
for idx, line in enumerate(lines, start=1):
    if not line.strip():
        continue
    try:
        json.loads(line)
        complete_rows += 1
    except json.JSONDecodeError as exc:
        bad_line = idx
        bad_error = str(exc)
        break

print(f"decoded_line_fragments={len(lines)}")
print(f"complete_json_rows={complete_rows}")
print(f"expected_rows={EXPECTED_ROWS}")
print(f"first_malformed_line={bad_line}")
print(f"first_malformed_error={bad_error}")
print(f"payload_ends_newline={payload.endswith(bytes([10]))}")

if repo_sha == EXPECTED_FILE_SHA256 and hashlib.sha256(payload).hexdigest() == EXPECTED_CONTENT_SHA256 and complete_rows == EXPECTED_ROWS and eof:
    raise SystemExit(0)
raise SystemExit(2)
