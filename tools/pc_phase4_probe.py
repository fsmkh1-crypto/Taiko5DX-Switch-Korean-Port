"""PHASE 4 read-only analysis probe; not a patcher or production builder.

Usage: python tools/pc_phase4_probe.py /path/to/T5K.bin
The narrow byte interpreter models only this helper's opcodes and branch predicates.
It is not a general x86 emulator and does not model faults or every EFLAGS bit.
No DLL/EXE execution, executable output, helper mutation, or network access.
"""
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys


def descriptors(b):
    cursor = 0x95540  # V041 established boundary
    result = []
    for index in range(11):
        start = cursor
        anchor, n, count, z = struct.unpack_from('<4I', b, cursor)
        cursor += 16
        name = b[cursor:cursor+z].decode('ascii')
        cursor += z
        so = cursor
        signature = b[cursor:cursor+n]
        cursor += n
        mo = cursor
        mask = b[cursor:cursor+n]
        cursor += n
        row = dict(index=index, resource_offset=start, name=name, anchor=anchor,
                   signature_len=n, signature_offset=so, mask_offset=mo,
                   signature=signature.hex(), mask=mask.hex(), patch_count=count,
                   subpatches=[])
        for j in range(count):
            off = cursor
            delta, length, kind, arg, plen = struct.unpack_from('<IIB3xII', b, cursor)
            cursor += 20
            pre = b[cursor:cursor+length]
            cursor += length
            payload = b[cursor:cursor+plen]
            cursor += plen
            assert all(not mask[delta+k] or signature[delta+k] == v
                       for k, v in enumerate(pre))
            row['subpatches'].append(dict(index=j, resource_offset=off, offset=delta,
                                         preimage_len=length, preimage=pre.hex(), kind=kind,
                                         arg=arg, payload_len=plen, payload=payload.hex(),
                                         successful_write_rva=anchor+delta))
        result.append(row)
    assert cursor == len(b)
    return result


FIXUPS = {0x18: 0x6933d5, 0x86: 0x6832bc, 0x90: 0x6832bc, 0x9a: 0x68328a}


def run_helper(h, start, ecx, trail=0):
    # Values deliberately include nonzero upper RAX to test 32-bit zero extension.
    eax = 0x1122334455667788
    rbx, rdi = 0x1000, 0x2000
    initial = (eax, rbx, rdi)
    mem, reads, trace = {}, [], []
    cf = zf = False
    pc = start
    for _ in range(64):
        trace.append(pc)
        op = h[pc:pc+8]
        if op[:2] == b'\x89\xc8':
            eax = ecx & 0xffffffff; pc += 2
        elif op[:3] == b'\xc1\xe8\x08':
            eax >>= 8; pc += 3
        elif op[0] == 0x2c:
            eax = (eax & ~255) | ((eax-op[1]) & 255); pc += 2
        elif op[0] == 0x3c:
            cf, zf = (eax & 255) < op[1], (eax & 255) == op[1]; pc += 2
        elif op[:2] == b'\x80\xf9':
            cf, zf = (ecx & 255) < op[2], (ecx & 255) == op[2]; pc += 3
        elif op[0] == 0x77:
            delta = struct.unpack_from('<b', h, pc+1)[0]
            pc += 2 + (delta if not cf and not zf else 0)
        elif op[0] == 0x0f and op[1] in (0x82, 0x86, 0x87):
            take = {0x82: cf, 0x86: cf or zf, 0x87: not cf and not zf}[op[1]]
            delta = struct.unpack_from('<i', h, pc+2)[0]
            pc += 6 + (delta if take else 0)
        elif op[:3] == b'\x0f\xb6\xc0':
            eax &= 255; pc += 3
        elif op[:3] == b'\x83\xc0\x31':
            eax = (eax+49) & 0xffffffff; pc += 3
        elif op[0] == 0xc3:
            return dict(exit='ret', eax=eax, rbx=rbx, rdi=rdi,
                        memory=mem, reads=reads, trace=trace)
        elif op[:5] == b'\x48\x89\x5c\x24\x08':
            mem['rsp+8:qword'] = rbx; pc += 5
        elif op[0] == 0xe9:
            assert pc+1 in FIXUPS
            return dict(exit=FIXUPS[pc+1], eax=eax, rbx=rbx, rdi=rdi,
                        memory=mem, reads=reads, trace=trace, cf=cf, zf=zf)
        elif op[:3] == b'\x0f\xb6\x03':
            reads.append(rbx); eax = trail; pc += 3
        elif op[:2] == b'\x88\x0f':
            mem[rdi] = ecx & 255; pc += 2
        elif op[:3] == b'\x88\x47\x01':
            mem[rdi+1] = eax & 255; pc += 3
        elif op[:4] == b'\x48\x83\xc7\x02':
            rdi += 2; pc += 4
        elif op[:3] == b'\x48\xff\xc3':
            rbx += 1; pc += 3
        elif op[:3] == b'\x48\xff\xc7':
            rdi += 1; pc += 3
        elif op[:3] == b'\x8d\x41\x22':
            eax = (ecx+34) & 0xffffffff; pc += 3
        else:
            raise AssertionError(('unknown instruction', hex(pc), op.hex(), initial))
    raise AssertionError('helper did not exit')


def resolve(text, sig, mask, text_rva, anchor):
    # Specification model of DLL 0x3DA0, used only with synthetic byte arrays.
    if len(sig) != len(mask) or len(sig) > len(text):
        return None
    hits = []
    for p in range(len(text)-len(sig)+1):
        if all(not m or text[p+j] == sig[j] for j, m in enumerate(mask)):
            hits.append(text_rva+p)
            if len(hits) > 1:
                return None
    return hits[0] if len(hits) == 1 and hits[0] == anchor else None


def verify(h, ds):
    reached = set()
    outcomes = collections.Counter()
    for code in range(65536):
        r = run_helper(h, 0, code)
        reached.update(r['trace'])
        lead = code >> 8
        if 0xeb <= lead <= 0xf8:
            assert r['exit'] == 'ret' and r['eax'] == lead-0xeb+49 and not r['memory']
        else:
            assert r['exit'] == 0x6933d5 and r['memory'] == {'rsp+8:qword': 0x1000}
            assert r['eax'] == ((lead-0xeb) & 255)
        assert r['rbx'] == 0x1000 and r['rdi'] == 0x2000 and not r['reads']
    for lead in range(256):
        r = run_helper(h, 0, 0x12340055 | (lead << 8))
        assert (r['exit'] == 'ret') == (0xeb <= lead <= 0xf8)
    for lead in range(256):
        for trail in range(256):
            r = run_helper(h, 0x20, lead, trail)
            reached.update(r['trace'])
            two_lead = 0x81 <= lead <= 0x9f or 0xe0 <= lead <= 0xfc
            assert len(r['reads']) == int(two_lead)
            if 0xa1 <= lead <= 0xdf:
                outcomes['one_byte'] += 1
                assert r['exit'] == 0x6832bc and r['memory'] == {0x2000: lead}
                assert r['rbx'] == 0x1000 and r['rdi'] == 0x2001
                assert r['eax'] == 0x1122334455667788
            elif two_lead and (0x40 <= trail <= 0x7e or 0x80 <= trail <= 0xfc):
                outcomes['two_byte'] += 1
                assert r['exit'] == 0x6832bc and r['memory'] == {0x2000: lead, 0x2001: trail}
                assert r['rbx'] == 0x1001 and r['rdi'] == 0x2002 and r['eax'] == trail
            else:
                outcomes['fallback'] += 1
                assert r['exit'] == 0x68328a and not r['memory']
                assert r['rbx'] == 0x1000 and r['rdi'] == 0x2000
                assert r['eax'] == lead+34 and r['cf'] == (((lead+34) & 255) < 1)
                assert r['zf'] == (((lead+34) & 255) == 1)
    assert resolve(b'abXcd', b'ab0', b'\x01\xff\x00', 0x1000, 0x1000) == 0x1000
    assert resolve(b'zbXcd', b'ab0', b'\x01\xff\x00', 0x1000, 0x1000) is None
    assert resolve(b'abXabY', b'ab0', b'\x01\x01\x00', 0x1000, 0x1000) is None
    assert resolve(b'ZabX', b'ab0', b'\x01\x01\x00', 0x1000, 0x1000) is None
    assert resolve(b'ZabX', b'ab0', b'\x01\x01\x00', 0x1000, 0x1001) == 0x1001
    # 0x01 is a full-byte selector, not a bitmask of the input byte.
    assert resolve(b'\x03', b'\x01', b'\x01', 0x1000, 0x1000) is None
    # rel32 guard formulation used by the DLL: [-2^31,2^31-1] inclusive.
    for d in (-0x80000001, -0x80000000, -1, 0, 0x7fffffff, 0x80000000):
        assert (0 <= d+0x80000000 <= 0xffffffff) == (-0x80000000 <= d <= 0x7fffffff)
    pop = collections.Counter(p['kind'] for d in ds for p in d['subpatches'])
    assert len(ds) == 11 and pop == {0: 9, 1: 2, 2: 1, 3: 2}
    # Synthetic allocation: generated-value round trips, never written to a binary.
    M, P, H = 0x140000000, 0x143000000, 0x14300a000
    for d in ds:
        for p in d['subpatches']:
            W = M+p['successful_write_rva']; k = p['kind']
            value = (P-W-4) if k == 1 else (P-M) if k == 2 else (H+p['arg']-W-5)
            if k:
                raw = struct.pack('<i', value)
                decoded = struct.unpack('<i', raw)[0]
                assert (W+4+decoded if k == 1 else M+decoded if k == 2 else W+5+decoded) == (P if k in (1,2) else H+p['arg'])
    for operand, target in FIXUPS.items():
        delta = M+target-(H+operand+4)
        assert H+operand+4+struct.unpack('<i', struct.pack('<i', delta))[0] == M+target
    return dict(mapper_cases=65536, mapper_upper_ecx_cases=256,
                byte_validator_cases=65536, byte_validator_outcomes=dict(outcomes),
                reached_instruction_offsets=[hex(x) for x in sorted(reached)],
                descriptor_count=11, subpatch_count=sum(pop.values()), kinds=dict(pop),
                synthetic_search_cases=6, rel32_boundary_cases=6,
                limitation='Narrow raw-byte interpreter and specification models; not native DLL/EXE execution or full x86/fault/EFLAGS emulation')


if __name__ == '__main__':
    b = Path(sys.argv[1]).read_bytes()
    assert hashlib.sha256(b).hexdigest() == '5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29'
    ds = descriptors(b)
    print(json.dumps(dict(descriptors=ds, verification=verify(b[0x9f72:0xa010], ds)), indent=2))
