"""Source-frozen, non-release whole-message coverage experiment.

This is an explicitly scoped diagnostic, not the semantic admission/release
builder. It tests the omitted-payload mechanism with exact PC literal programs
whose target-VM control bytes agree, preserving the reviewed 217 baseline.
It must not issue INCLUDE_KO, runtime PASS, or V371 closure.
"""
from pathlib import Path
import argparse
import hashlib
import io
import json
import struct
import sys
import zipfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'vendor'))
from builder.selective_tai5msg import parse_tai5msg, _serialize_from_messages
from switch_vm_fields import inspect, structural_signature

PINS = {
    'original': 'aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f',
    'pc': 'e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090',
    'mapping': '429dccba3444caf9e63524908f3f00249504da56e60fe5249fb0f1ee0213146f',
    'baseline': '43894d52f3e5498ea3c5f2c7e0597f6f29ea24f40be6afd03d29d0b4e021cefe',
    'main': 'b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b',
}
TAI = 'romfs/TAI5MSG_JP.DAT'
CURRENT = 'eddf9cf57332f090fde2c6b9ed707342fc57c1ed6a366de89c553b707953ba1c'
BUILD = 'D9120950C258610A746F4A31CE3A3B376DE393D9'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def guarded(path, role):
    b = Path(path).read_bytes()
    require(sha(b) == PINS[role], 'INPUT_IDENTITY_' + role)
    return b


def source_gate(receipt_path, commit):
    receipt = json.loads(Path(receipt_path).read_text())
    plan = json.loads((HERE / 'SOURCE_MAP.json').read_text())
    require(receipt['repository'] == 'fsmkh1-crypto/Taiko5DX-Switch-Korean-Port', 'REPOSITORY')
    require(receipt['commit'] == receipt['remote_main_verified'] == commit, 'SOURCE_COMMIT')
    got = {r['repository_path']: r for r in receipt['files']}
    require(set(got) == {r['repository_path'] for r in plan}, 'EXACT_FROZEN_PATHS')
    for r in plan:
        b = (HERE / r['relative_path']).read_bytes()
        g = got[r['repository_path']]
        blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        require(sha(b) == r['sha256'] == g['sha256'] and blob == g['git_blob_sha'], 'SOURCE_BYTES')
    require(any(r['relative_path'] == 'build.py' for r in plan), 'BUILDER_NOT_FROZEN')


def prepare(args):
    raw = {k: guarded(getattr(args, k), k) for k in PINS}
    require(raw['main'][:4] == b'NSO0' and raw['main'][0x40:0x54].hex().upper() == BUILD, 'MAIN_BUILD_ID')
    with zipfile.ZipFile(io.BytesIO(raw['baseline'])) as z:
        require(len(z.namelist()) == 17 and z.testzip() is None, 'BASELINE_ZIP')
        members = {n.split('/', 1)[1]: z.read(n) for n in z.namelist()}
    require(sha(members[TAI]) == CURRENT, 'CURRENT_TAI_IDENTITY')
    source, pc, current = (parse_tai5msg(b) for b in (raw['original'], raw['pc'], members[TAI]))
    codes = {p[0] for p in json.loads(raw['mapping'])['entries']}
    rows, parsed, selected, hold = {}, {}, set(), {}
    preserved = identical = 0
    for bi, block in enumerate(source.blocks):
        for mi, a in enumerate(block.messages):
            key = f'B{bi}:{mi}'
            b, c = pc.blocks[bi].messages[mi], current.blocks[bi].messages[mi]
            row = dict(locator=key, original_sha256=sha(a), pc_sha256=sha(b), baseline_sha256=sha(c))
            if c != a:
                row['role'] = 'REVIEWED_BASELINE_PREREQUISITE'
                preserved += 1
            elif b == a:
                row['role'] = 'NO_CONTENT_DELTA'
                identical += 1
            else:
                row['role'] = 'DIAGNOSTIC_TARGET'
                x, y = inspect(a, codes), inspect(b, codes)
                parsed[key] = x
                if not x['complete'] or not y['complete']:
                    hold[key] = dict(reason='UNRESOLVED_FIELD_BOUNDARY', original=x['error'], pc=y['error'])
                elif structural_signature(a, x, False) != structural_signature(b, y, False):
                    hold[key] = dict(reason='PC_CONTROL_DIVERGENCE')
                else:
                    selected.add(key)
                    row['layout_delta'] = structural_signature(a, x) != structural_signature(b, y)
            rows[key] = row
    require((len(rows), preserved, identical, len(selected), len(hold)) == (14832, 3227, 1233, 10238, 134), 'FROZEN_COHORT_COUNTS')
    initial_holds = len(hold)
    while True:
        remove = {}
        for key in selected:
            bad = sorted({e['target'] for e in parsed[key]['edges'] if e['target'] in hold or e['target'] not in rows})
            if bad:
                remove[key] = dict(reason='EXPLICIT_DEPENDENCY_HOLD', targets=bad)
        if not remove:
            break
        selected.difference_update(remove)
        hold.update(remove)
    require((len(selected), len(hold)) == (10220, 152), 'DEPENDENCY_CLOSURE_COUNTS')
    for key in ('B4:82', 'B4:83', 'B8:11', 'B8:38', 'B8:39'):
        require(key in selected, 'FOCUSED_TARGET_NOT_SELECTED')
    targets = [list(b.messages) for b in current.blocks]
    for key in selected:
        bi, mi = map(int, key[1:].split(':'))
        targets[bi][mi] = pc.blocks[bi].messages[mi]
    for key, row in rows.items():
        bi, mi = map(int, key[1:].split(':'))
        row['output_sha256'] = sha(targets[bi][mi])
        row['diagnostic_selected'] = key in selected
        row['semantic_release_admission'] = False
        if key in hold:
            row['hold'] = hold[key]
    capacity = []
    for bi, block in enumerate(source.blocks):
        used = 2 + 4 * len(targets[bi]) + sum(map(len, targets[bi]))
        declared = max(block.declared_size, (used + 63) & ~63) if bi < 32 else block.declared_size
        require(declared <= 0x20000, 'RUNTIME_BLOCK_CAPACITY')
        require(bi != 32 or used <= block.physical_size, 'B32_CAPACITY')
        capacity.append(dict(block=bi, used=used, declared=declared))
    report = dict(schema='MESSAGE_COVERAGE_DIAGNOSTIC_218_V1', input_sha256=PINS,
                  records=14832, diagnostic_targets=10220, preserved_reviewed=3227,
                  unchanged_original_pc=1233, initial_holds=initial_holds, dependency_holds=18,
                  held_original=152, capacity=capacity, semantic_release_admissions=0,
                  runtime='NOT_RUN', V369='UNCHANGED', V371='PARTIAL_BLOCKED',
                  scope='Exact PC programs with matched target-VM controls; coverage experiment, not a release',
                  open_gates=['Native/EVENT all-caller semantic admission', 'Output/visual capacity and non-B24 reflow',
                              'Runtime branch/variable QA', 'TE5/SNR identity scope', '60 source-identity holds',
                              'Remaining 156 EVENT files', 'Legacy PASS provenance and circular readback'])
    return source, targets, members, rows, report


def independent_readback(emitted, targets):
    # Loader-level +0x5b decryption and u16/u32 directory lookup, independent
    # of parse_tai5msg. Final message length comes from frozen expected bytes.
    checked = 0
    for bi, expected in enumerate(targets):
        off = int.from_bytes(emitted[8*bi:8*bi+4], 'little')
        end = int.from_bytes(emitted[8*(bi+1):8*(bi+1)+4], 'little') if bi < 32 else len(emitted)
        plain = bytes((v + 91) % 256 for v in emitted[off:end])
        require(int.from_bytes(plain[:2], 'little') == len(expected), 'INDEPENDENT_COUNT')
        for mi, want in enumerate(expected):
            at = int.from_bytes(plain[2+mi*4:6+mi*4], 'little')
            require(plain[at:at+len(want)] == want, 'INDEPENDENT_MESSAGE_BYTES')
            if mi + 1 < len(expected):
                nxt = int.from_bytes(plain[6+mi*4:10+mi*4], 'little')
                require(nxt == at + len(want), 'INDEPENDENT_NEXT_OFFSET')
            checked += 1
    require(checked == 14832, 'INDEPENDENT_UNIVERSE')


def main():
    p = argparse.ArgumentParser()
    for k in PINS:
        p.add_argument('--' + k, required=True)
    p.add_argument('--preflight', action='store_true')
    p.add_argument('--receipt')
    p.add_argument('--commit')
    p.add_argument('--output', required=True)
    a = p.parse_args()
    if not a.preflight:
        source_gate(a.receipt, a.commit)
    source, targets, members, rows, report = prepare(a)
    out = Path(a.output)
    out.mkdir(parents=True, exist_ok=True)
    if not a.preflight:
        emitted, meta = _serialize_from_messages(source, targets)
        independent_readback(emitted, targets)
        members[TAI] = emitted
        report.update(builder_source_commit=a.commit, tai5msg_sha256=sha(emitted), tai5msg_bytes=len(emitted),
                      independently_read_messages=14832, serialized_blocks=list(meta))
        report['members'] = [{ 'path': n, 'bytes': len(b), 'sha256': sha(b)} for n,b in sorted(members.items()) if n != 'SELECTIVE_PACKAGE_INFO.json']
        members['SELECTIVE_PACKAGE_INFO.json'] = (json.dumps(report, indent=2) + '\n').encode()
        dest = out / 'TAIKO5DX_KR_DIAG_218_MESSAGE_COVERAGE.zip'
        require(not dest.exists(), 'NO_OVERWRITE')
        with zipfile.ZipFile(dest, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for n,b in sorted(members.items()):
                info = zipfile.ZipInfo('Taiko5DX_KR_DIAG_218/' + n, (2026,9,23,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info, b)
        with zipfile.ZipFile(dest) as z:
            require(len(z.namelist()) == 17 and z.testzip() is None, 'ZIP_INTEGRITY')
            for n,b in members.items():
                require(z.read('Taiko5DX_KR_DIAG_218/' + n) == b, 'ZIP_MEMBER_BYTES')
        report['zip'] = dict(name=dest.name, bytes=dest.stat().st_size, sha256=sha(dest.read_bytes()))
    (out / 'REPORT.json').write_text(json.dumps(report, indent=2) + '\n')
    (out / 'RECORD_LEDGER_14832.jsonl').write_text(''.join(json.dumps(rows[k], separators=(',',':'))+'\n' for k in rows))
    print(json.dumps({k:v for k,v in report.items() if k not in ('capacity','serialized_blocks','members')}, indent=2))


if __name__ == '__main__':
    main()
