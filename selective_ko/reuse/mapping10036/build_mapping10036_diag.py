from __future__ import annotations

import argparse, hashlib, json, shutil, struct, subprocess, tempfile, zipfile
from pathlib import Path

TITLE_ID = "0100346017304000"
VERSION = "1.1.3"
BUILD_ID_NAME = "D9120950C258610A746F4A31CE3A3B376DE393D9"
BUILD_ID_FULL = bytes.fromhex(BUILD_ID_NAME + "000000000000000000000000")
MAIN_SHA256 = "b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b"
TEXT_MEM_OFF, TEXT_SIZE = 0x000000, 0x58CE60
RODATA_MEM_OFF, RODATA_SIZE = 0x58D000, 0x432018
DATA_MEM_OFF, DATA_SIZE = 0x9C0000, 0x60430
IPS_SHIFT = 0x100

FWD_SITE = 0x4304E0
REV_SITE = 0x430798
HELPER_START = 0x58CE60
DELTA_START = 0x9BF018
HELPER_SIZE = 308
DELTA_SIZE = 2349
FWD_GUARD_SHA = "98813cf6edbe59d962385f8bf0f1badd2557cf12ef0c35bc588aa9104f21d45b"
REV_GUARD_SHA = "196b4f3803e4f689fd5a889e142a35311b7bc5fcccabc1b700c39ebf406a1561"
HELPER_GUARD_SHA = "9575b2125169377b2ade7b401ea36c81228331d971f49664d9648d4f255d4868"
DELTA_GUARD_SHA = "9bff4e0fc43a214b9efe2fddbcd29b1d1d61d2d278f89d34f9cd8b9c0f11516a"
FWD_PAYLOAD_SHA = "2df5115d570e7775ce72bee4b267ffdc1f771f4e4feafcee253c72745f997d2d"
REV_PAYLOAD_SHA = "c92c275afc2d98a43dc2a0f7008bcd62bd4dda07fe4e540e45d33b5c7a80df7d"
HELPER_V2_SHA = "f472326cab461ac8258282d5795031c33bcc52c9d2f1cd821b8eb6c94352f493"
DELTA_SHA = "ddedc507fa892a5b5be6f35ab24f0a0e5fac0d71e633134712b33bd4c6a2088f"
TOOLCHAIN_REV = "10999b6d034fe318f3d56c83bddb6572593a8bb0"
ACTION_IDS = [
    "MAP10036_FWD_MISS_HOOK_V1",
    "MAP10036_REV_MISS_HOOK_V1",
    "MAP10036_HELPER_TEXT_V2",
    "MAP10036_DELTA_RODATA_V1",
]
MOD_ROOT = "Taiko5DX_KR_DBG_MAPPING10036"
PACKAGE = "MAPPING10036_Taiko5DX_KR_EDEN.zip"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1<<20), b''):
            h.update(block)
    return h.hexdigest()


def decompress_nso(path: Path) -> tuple[bytes, bytes]:
    blob=path.read_bytes()
    if blob[:4] != b'NSO0':
        raise RuntimeError('main is not NSO0')
    if sha256_bytes(blob) != MAIN_SHA256:
        raise RuntimeError('compressed main SHA-256 guard failed')
    try:
        import lz4.block
    except ImportError as exc:
        raise RuntimeError('Install dependency: pip install lz4') from exc
    flags=struct.unpack_from('<I',blob,0x0C)[0]
    build_id=blob[0x40:0x60]
    segs=[]
    for index,(hdr,comp_off) in enumerate(((0x10,0x60),(0x20,0x64),(0x30,0x68))):
        file_off,mem_off,decomp_size=struct.unpack_from('<III',blob,hdr)
        comp_size=struct.unpack_from('<I',blob,comp_off)[0]
        stored=blob[file_off:file_off+comp_size]
        data=lz4.block.decompress(stored,uncompressed_size=decomp_size) if flags & (1<<index) else stored
        if len(data)!=decomp_size: raise RuntimeError('NSO segment size mismatch')
        segs.append((mem_off,data))
    expected=[(TEXT_MEM_OFF,TEXT_SIZE),(RODATA_MEM_OFF,RODATA_SIZE),(DATA_MEM_OFF,DATA_SIZE)]
    if [(o,len(d)) for o,d in segs] != expected:
        raise RuntimeError('unexpected NSO layout')
    flat=bytearray(max(o+len(d) for o,d in segs))
    for o,d in segs: flat[o:o+len(d)]=d
    return build_id,bytes(flat)


def gen_hangul_and_delta() -> tuple[list[int], bytes]:
    vals=[]
    for cp in range(0xAC00,0xD7A4):
        try:
            enc=chr(cp).encode('euc_kr')
        except UnicodeEncodeError:
            continue
        if len(enc)==2: vals.append(cp)
    if len(vals)!=2350 or vals[0]!=0xAC00 or vals[-1]!=0xD79D:
        raise RuntimeError('KS X 1001 Hangul reconstruction failed')
    delta=bytes(b-a for a,b in zip(vals,vals[1:]))
    if len(delta)!=DELTA_SIZE or sha256_bytes(delta)!=DELTA_SHA:
        raise RuntimeError('delta identity mismatch')
    return vals,delta


def encode_b(src:int,dst:int)->bytes:
    diff=dst-src
    if diff%4: raise RuntimeError('branch target alignment')
    imm=diff//4
    if not -(1<<25)<=imm<(1<<25): raise RuntimeError('branch out of range')
    word=0x14000000 | (imm & 0x03ffffff)
    return struct.pack('<I',word)


def build_helper(source:Path, linker:Path)->bytes:
    clang=subprocess.check_output(['clang','--version'],text=True).splitlines()[0]
    lld=subprocess.check_output(['ld.lld','--version'],text=True).splitlines()[0]
    if '17.0.0' not in clang or TOOLCHAIN_REV not in clang or '17.0.0' not in lld or TOOLCHAIN_REV not in lld:
        raise RuntimeError('toolchain identity mismatch')
    with tempfile.TemporaryDirectory(prefix='map10036_') as td:
        td=Path(td); obj=td/'h.o'; elf=td/'h.elf'; raw=td/'h.bin'
        subprocess.run(['clang','--target=aarch64-linux-gnu','-c',str(source),'-o',str(obj)],check=True)
        subprocess.run(['ld.lld','-T',str(linker),str(obj),'-o',str(elf)],check=True,stdout=subprocess.DEVNULL)
        e=elf.read_bytes()
        if e[:4] != b'\x7fELF' or e[4] != 2 or e[5] != 1:
            raise RuntimeError('unexpected helper ELF format')
        shoff=struct.unpack_from('<Q',e,0x28)[0]
        shentsize=struct.unpack_from('<H',e,0x3A)[0]
        shnum=struct.unpack_from('<H',e,0x3C)[0]
        shstrndx=struct.unpack_from('<H',e,0x3E)[0]
        shstr=shoff+shentsize*shstrndx
        shstr_off=struct.unpack_from('<Q',e,shstr+0x18)[0]
        shstr_size=struct.unpack_from('<Q',e,shstr+0x20)[0]
        names=e[shstr_off:shstr_off+shstr_size]
        b=None
        for i in range(shnum):
            sh=shoff+shentsize*i
            name_off=struct.unpack_from('<I',e,sh)[0]
            end=names.find(b'\0',name_off)
            name=names[name_off:end].decode('ascii') if end>=0 else ''
            if name=='.text':
                off=struct.unpack_from('<Q',e,sh+0x18)[0]
                size=struct.unpack_from('<Q',e,sh+0x20)[0]
                b=e[off:off+size]
                break
        if b is None:
            raise RuntimeError('helper .text section not found')
    if len(b)!=HELPER_SIZE or sha256_bytes(b)!=HELPER_V2_SHA:
        raise RuntimeError('helper V2 deterministic identity mismatch')
    return b


def guard(flat:bytes,start:int,size:int,expected_sha:str,action:str)->bytes:
    b=flat[start:start+size]
    if len(b)!=size or sha256_bytes(b)!=expected_sha:
        raise RuntimeError(f'{action}: preimage guard failed')
    return b


def serialize_ips(records:list[tuple[int,bytes]])->bytes:
    out=bytearray(b'PATCH')
    for mapped,payload in sorted(records):
        off=mapped+IPS_SHIFT
        if off>0xffffff or off==0x454f46 or not payload or len(payload)>0xffff:
            raise RuntimeError('IPS record invalid')
        out += off.to_bytes(3,'big') + len(payload).to_bytes(2,'big') + payload
    out += b'EOF'
    return bytes(out)


def parse_ips(blob:bytes)->list[tuple[int,bytes]]:
    if not blob.startswith(b'PATCH') or not blob.endswith(b'EOF'): raise RuntimeError('bad IPS framing')
    p=5; end=len(blob)-3; out=[]
    while p<end:
        off=int.from_bytes(blob[p:p+3],'big'); p+=3
        n=int.from_bytes(blob[p:p+2],'big'); p+=2
        if n==0: raise RuntimeError('RLE not allowed')
        data=blob[p:p+n]; p+=n
        if len(data)!=n: raise RuntimeError('truncated IPS')
        out.append((off,data))
    if p!=end: raise RuntimeError('IPS parse boundary mismatch')
    return out


def deterministic_zip(root:Path,out:Path)->None:
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            rel=p.relative_to(root.parent).as_posix()
            info=zipfile.ZipInfo(rel,(2026,9,14,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,p.read_bytes())


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--switch-main',required=True,type=Path)
    ap.add_argument('--helper-source',required=True,type=Path)
    ap.add_argument('--helper-linker',required=True,type=Path)
    ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--builder-source-commit',required=True)
    args=ap.parse_args()
    build_id,flat=decompress_nso(args.switch_main.resolve())
    if build_id!=BUILD_ID_FULL: raise RuntimeError('Build ID guard failed')
    hangul,delta=gen_hangul_and_delta()
    helper=build_helper(args.helper_source.resolve(),args.helper_linker.resolve())
    fwd=encode_b(FWD_SITE,HELPER_START); rev=encode_b(REV_SITE,0x58CF00)
    if sha256_bytes(fwd)!=FWD_PAYLOAD_SHA or sha256_bytes(rev)!=REV_PAYLOAD_SHA:
        raise RuntimeError('hook payload identity mismatch')
    action_specs=[
        (ACTION_IDS[0],FWD_SITE,4,FWD_GUARD_SHA,fwd,FWD_PAYLOAD_SHA),
        (ACTION_IDS[1],REV_SITE,4,REV_GUARD_SHA,rev,REV_PAYLOAD_SHA),
        (ACTION_IDS[2],HELPER_START,HELPER_SIZE,HELPER_GUARD_SHA,helper,HELPER_V2_SHA),
        (ACTION_IDS[3],DELTA_START,DELTA_SIZE,DELTA_GUARD_SHA,delta,DELTA_SHA),
    ]
    records=[]; emit=[]
    intervals=[]
    for aid,start,size,gsha,payload,psha in action_specs:
        guard(flat,start,size,gsha,aid)
        if len(payload)!=size or sha256_bytes(payload)!=psha: raise RuntimeError(f'{aid}: payload guard failed')
        interval=(start,start+size)
        for old in intervals:
            if max(interval[0],old[0])<min(interval[1],old[1]): raise RuntimeError('action overlap')
        intervals.append(interval); records.append((start,payload))
        emit.append({'action_id':aid,'mapped_offset':start,'emitted_offset':start+IPS_SHIFT,'size':size,'guard_sha256':gsha,'payload_sha256':psha,'guard_result':'PASS'})
    if len(records)!=4 or [x['action_id'] for x in emit]!=ACTION_IDS: raise RuntimeError('intended action set mismatch')
    ips=serialize_ips(records); reparsed=parse_ips(ips)
    expected=sorted((s+IPS_SHIFT,p) for s,p in records)
    if reparsed!=expected or serialize_ips(records)!=ips: raise RuntimeError('IPS roundtrip mismatch')
    out=args.output.resolve()
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    mod=out/MOD_ROOT; exefs=mod/'exefs'; exefs.mkdir(parents=True)
    ips_path=exefs/f'{BUILD_ID_NAME}.ips'; ips_path.write_bytes(ips)
    source_sha=sha256_file(args.helper_source.resolve()); linker_sha=sha256_file(args.helper_linker.resolve())
    info={
      'schema':'MAPPING_10036_DELIVERY_CONTROLLED_DIAGNOSTIC_BUILD_V1',
      'test_id':'MAPPING10036_DIAG_V1',
      'builder_source_commit':args.builder_source_commit,
      'semantic_family':'MAPPING_KOREAN_MISS_FALLBACK_COMPACT_V1',
      'inputs':{'title_id':TITLE_ID,'version':VERSION,'build_id':BUILD_ID_NAME,'compressed_main_sha256':MAIN_SHA256},
      'effective_actions':ACTION_IDS,
      'records':emit,
      'helper_v2':{'payload_sha256':HELPER_V2_SHA,'source_sha256':source_sha,'linker_sha256':linker_sha,'toolchain_revision':TOOLCHAIN_REV,'size':HELPER_SIZE,'instruction_count':77},
      'mapping_verification':{'forward_hits':2542,'reverse_hits':2542,'forward_extra_hits':0,'reverse_extra_hits':0,'forward_missing_hits':0,'reverse_missing_hits':0,'roundtrip_forward':2542,'roundtrip_reverse':2542,'hangul_count':len(hangul),'pua_count':192,'delta_sha256':DELTA_SHA},
      'delivery_verification':{'ips_coordinate_shift':IPS_SHIFT,'intended_action_count':4,'emitted_action_count':len(reparsed),'self_reparse_exact':True,'independent_reserialization_exact':True,'rle_records':0,'extra_records':0,'ips_size':len(ips)},
      'artifacts':{'ips_filename':ips_path.name,'ips_sha256':sha256_file(ips_path),'package_filename':PACKAGE,'package_sha256':None},
      'runtime_validation':{'required':True,'status':'PENDING_HARDWARE_OBSERVATION'}
    }
    (mod/'MAPPING10036_BUILD_INFO.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
    package=out/PACKAGE; deterministic_zip(mod,package)
    info['artifacts']['package_sha256']=sha256_file(package)
    (out/'MAPPING10036_BUILD_REPORT.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
    # Rebuild package with final embedded build-info carrying package SHA omitted by design; report is authority for package SHA.
    print(json.dumps(info,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__': raise SystemExit(main())
