"""Guarded, separate expanded-profile diagnostic. Canonical serializer is unchanged."""
import argparse,hashlib,json,struct,zipfile,io
from pathlib import Path
import readback
HERE=Path(__file__).resolve().parent
TAI='romfs/TAI5MSG_JP.DAT';MOD='Taiko5DX_KR_DIAG_222_COMPOSITION'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(condition,message):
    if not condition:raise ValueError(message)
def load_inputs(baseline_path,main_path):
    c=json.loads((HERE/'CONTRACT.json').read_text());planbytes=(HERE/'MESSAGE_PLAN.json').read_bytes()
    require(sha(planbytes)==c['message_plan_sha256'],'plan identity');plan=json.loads(planbytes)
    raw=Path(baseline_path).read_bytes();require(sha(raw)==c['baseline_zip_sha256'],'baseline ZIP identity')
    main=Path(main_path).read_bytes();require(sha(main)==c['main_sha256'],'main identity')
    require(main[0x40:0x54].hex().upper()==c['build_id'],'main build ID')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        require(z.testzip() is None and len(z.namelist())==17,'baseline ZIP envelope')
        members={n.split('/',1)[1]:z.read(n) for n in z.namelist()}
    require(sha(members[TAI])==c['baseline_tai_sha256'],'baseline TAI identity')
    return c,plan,members

def prepare(c,plan,baseline):
    # Writer-side reader. Independent readback uses different byte access and explicit last lengths.
    source=[];layouts=[]
    for b,n in enumerate(c['baseline_counts']):
        off,size=struct.unpack_from('<II',baseline,b*8)
        end=struct.unpack_from('<I',baseline,(b+1)*8)[0] if b<32 else len(baseline)
        plain=bytes((v+91)&255 for v in baseline[off:end]);count=struct.unpack_from('<H',plain)[0]
        require(count==n,'baseline block count')
        starts=list(struct.unpack_from('<'+'I'*n,plain,2));stops=starts[1:]+[starts[-1]+c['base_last_lengths'][b]]
        require(starts[0]==2+4*n and stops[-1]<=len(plain),'baseline layout')
        source.append([plain[a:z] for a,z in zip(starts,stops)]);layouts.append((size,end-off))
    require(sum(map(len,source))==14832,'source universe')
    target=[list(rows) for rows in source]
    require(set(plan)==set(c['preimages'])|{f'B0:{i}' for i in range(471,511)},'exact write scope')
    for key,digest in c['preimages'].items():
        b,m=map(int,key[1:].split(':'));require(sha(source[b][m])==digest,'preimage '+key)
    for key,value in plan.items():
        b,m=map(int,key[1:].split(':'));value=bytes.fromhex(value)
        if m<len(source[b]):target[b][m]=value
    for m in range(471,511):target[0].append(bytes.fromhex(plan[f'B0:{m}']))
    require(target[0][:471]==source[0],'original B0 preserved')
    for r in c['clone_sources']:
        require(sha(source[0][r['source_root']])==r['source_sha256'],'clone source')
        require(sha(target[0][r['id']])==r['decoded_sha256'],'clone output')
    require(sum(map(len,target))==14872,'extended profile universe')
    return source,target,layouts

def serialize(baseline,target,layouts):
    header=bytearray(baseline[:320]);parts=[];file_offset=320
    for b,rows in enumerate(target):
        cursor=2+4*len(rows);offsets=[]
        for value in rows:offsets.append(cursor);cursor+=len(value)
        old_declared,old_physical=layouts[b]
        declared=max(old_declared,(cursor+63)//64*64) if b<32 else old_declared
        physical=declared if b<32 else old_physical
        require(cursor<=physical<=declared<=131072,'block capacity/physical contract')
        plain=struct.pack('<H',len(rows))+struct.pack('<'+'I'*len(rows),*offsets)+b''.join(rows)
        plain+=b'\x5b'*(physical-len(plain));parts.append(bytes((v-91)&255 for v in plain))
        struct.pack_into('<II',header,b*8,file_offset,declared);file_offset+=physical
    return bytes(header)+b''.join(parts)

def source_gate(receipt_path,commit):
    receipt=json.loads(Path(receipt_path).read_text())
    require(receipt['commit']==receipt['remote_main_verified']==commit,'source commit not verified')
    for row in receipt['files']:
        data=(HERE/row['local_name']).read_bytes();require(sha(data)==row['sha256'],'frozen source changed')
    require({r['local_name'] for r in receipt['files']}=={'build.py','readback.py','CONTRACT.json','MESSAGE_PLAN.json','README.md'},'source freeze file set')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',required=True);ap.add_argument('--main',required=True);ap.add_argument('--out',required=True);ap.add_argument('--source-receipt');ap.add_argument('--source-commit');ap.add_argument('--check',action='store_true');a=ap.parse_args()
    c,plan,members=load_inputs(a.baseline,a.main);source,target,layouts=prepare(c,plan,members[TAI])
    # Preparation may run before source freeze; no candidate bytes are generated in --check.
    if a.check:
        print(json.dumps({'status':'PREPARED_NO_GAME_BYTES_EMITTED','guarded_original_changes':len(c['preimages']),'appended_helpers':40}));return
    require(a.source_receipt and a.source_commit,'source freeze required');source_gate(a.source_receipt,a.source_commit)
    candidate=serialize(members[TAI],target,layouts);verified=readback.verify(members[TAI],candidate,c,plan)
    negative=[]
    for label,at in [('stored_payload',verified['blocks'][0]['offset']+2046),('appended_helper',verified['blocks'][0]['offset']+2046+sum(map(len,target[0][:471]))),('header_offset',8),('block_count',verified['blocks'][0]['offset'])]:
        bad=bytearray(candidate);bad[at]^=1
        try:readback.verify(members[TAI],bytes(bad),c,plan)
        except (ValueError,IndexError):negative.append(label)
        else:raise ValueError('independent reader accepted corruption')
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);members[TAI]=candidate
    inherited=json.loads(members['SELECTIVE_PACKAGE_INFO.json'])
    members['SELECTIVE_PACKAGE_INFO.json']=(json.dumps({'diagnostic':'COMPOSITION222','builder_source_commit':a.source_commit,'profile':c['profile'],'tai_sha256':sha(candidate),'original_records':14832,'changed_original_records':18,'appended_helpers':40,'runtime':'NOT_RUN','product_state':'V369_UNCHANGED','v371':'PARTIAL_BLOCKED','inherited_218_metadata':inherited},ensure_ascii=False,indent=2)+'\n').encode()
    package=out/'TAIKO5DX_KR_DIAG_222_COMPOSITION.zip'
    with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(members.items()):
            info=zipfile.ZipInfo(MOD+'/'+name,date_time=(2026,9,23,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    with zipfile.ZipFile(package) as z:
        require(z.testzip() is None and len(z.namelist())==17,'ZIP readback')
        require(set(z.namelist())=={MOD+'/'+n for n in members},'ZIP member scope')
        for name,data in members.items():require(z.read(MOD+'/'+name)==data,'ZIP exact bytes')
        readback.verify(load_inputs(a.baseline,a.main)[2][TAI],z.read(MOD+'/'+TAI),c,plan)
    ledger=verified.pop('ledger');(out/'RECORD_LEDGER.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in ledger))
    report={'test_id':'COMPOSITION222','builder_source_commit':a.source_commit,'inputs':c,'verification':verified,'negative_readback_probes_rejected':negative,'members':[{'path':n,'size':len(d),'sha256':sha(d),'role':'DIAGNOSTIC_TAI' if n==TAI else 'DIAGNOSTIC_METADATA' if n=='SELECTIVE_PACKAGE_INFO.json' else 'UNCHANGED_218_PREREQUISITE'} for n,d in sorted(members.items())],'artifact':{'filename':package.name,'bytes':package.stat().st_size,'sha256':sha(package.read_bytes()),'tai_sha256':sha(candidate)},'unchanged_prerequisite_product_members':15,'runtime':'NOT_RUN','product_state':'V369_UNCHANGED','v371':'PARTIAL_BLOCKED','semantic_release_admissions':0}
    (out/'BUILD_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['artifact']))
if __name__=='__main__':main()
