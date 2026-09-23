"""Deterministic diagnostic packager; requires exact source freeze before emission."""
from pathlib import Path
import hashlib,json,subprocess,zipfile,io
TITLE='0100346017304000';BUILD='D9120950C258610A746F4A31CE3A3B376DE393D9'
BASE_IPS='6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4'
FONT='c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932'
def sha(b):return hashlib.sha256(b).hexdigest()
def check(ok,why):
 if not ok:raise ValueError(why)
def prerequisites(archive):
 from builder.selective_package import parse_ips,serialize_mapped_ips,MAPPING_ACTIONS,PAGE_MAPPER_SITE,PAGE_MAPPER_REPLACEMENT
 b=Path(archive).read_bytes();check(len(b)==3638158 and sha(b)=='bc62aa0c8e25b7d7338eb3bd47468d10335636a0c6385c9296e6814a48cfd2f7','BASE_ARCHIVE_IDENTITY')
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  prefix='Taiko5DX_KR_SELECTIVE/';ips=z.read(prefix+'exefs/'+BUILD+'.ips');font=z.read(prefix+'romfs/FONT/FONT_JPN.G1T')
 check(len(ips)==2742 and sha(ips)==BASE_IPS,'IPS_IDENTITY');check(len(font)==16779036 and sha(font)==FONT,'FONT_IDENTITY')
 records=parse_ips(ips);expected={r.mapped_offset+0x100:(r.size,r.payload_sha256) for r in MAPPING_ACTIONS};expected[PAGE_MAPPER_SITE+0x100]=(len(PAGE_MAPPER_REPLACEMENT),sha(PAGE_MAPPER_REPLACEMENT))
 check(len(records)==5 and len(expected)==5,'IPS_RECORD_COUNT')
 for off,payload in records:check(off in expected and (len(payload),sha(payload))==expected[off],'IPS_RECORD_PLAN')
 check(serialize_mapped_ips([(off-0x100,payload) for off,payload in records])==ips,'IPS_ROUNDTRIP')
 return ips,font,{'base_archive_sha256':sha(b),'ips_sha256':sha(ips),'font_sha256':sha(font),'ips_records':5,'exact_record_plan_and_roundtrip':True,'main_guard':'Inherited unchanged IPS provenance; local game main and installed game version were not verified','title_id':TITLE,'version':'1.1.3','build_id':BUILD}
def verify_source_freeze(checkout,commit,source_map):
 check(bool(source_map),'SOURCE_MAP_REQUIRED')
 check(len({r['repository_path'] for r in source_map})==len(source_map),'DUPLICATE_SOURCE_MAP_PATH')
 check(any(Path(r['local_path']).resolve()==Path(__file__).resolve() for r in source_map),'PACKAGER_SOURCE_NOT_FROZEN')
 check(len(commit)==40 and all(c in '0123456789abcdef' for c in commit),'BUILDER_COMMIT_REQUIRED')
 # Authenticated connector readback is supported where no local Git checkout is mounted.
 # The receipt must bind every exact source to the same already-published commit.
 if Path(checkout).is_file():
  receipt=json.loads(Path(checkout).read_text())
  check(receipt['repository']=='fsmkh1-crypto/Taiko5DX-Switch-Korean-Port' and receipt['commit']==commit and receipt['remote_main_verified']==commit,'REMOTE_COMMIT_RECEIPT')
  observed={r['repository_path']:r for r in receipt['files']}
  check(set(observed)=={r['repository_path'] for r in source_map},'REMOTE_SOURCE_COVERAGE')
  for row in source_map:
   data=Path(row['local_path']).read_bytes();git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();actual=observed[row['repository_path']]
   check(actual['commit']==commit and actual['sha256']==row['sha256']==sha(data) and actual['git_blob_sha']==git_blob,'REMOTE_SOURCE_BYTE_IDENTITY')
  return
 def git(*args):return subprocess.check_output(['git','-C',str(checkout),*args],stderr=subprocess.PIPE)
 check(git('rev-parse','HEAD').decode().strip()==commit,'CHECKOUT_HEAD_MISMATCH')
 check(not git('status','--porcelain'),'CHECKOUT_NOT_CLEAN')
 for row in source_map:
  check(sha(git('show',commit+':'+row['repository_path']))==row['sha256'],'COMMITTED_SOURCE_MISMATCH')
  check(sha(Path(row['local_path']).read_bytes())==row['sha256'],'LOCAL_SOURCE_CHANGED')
def materialize(checkout,commit,source_map,members,output,member_plan):
 verify_source_freeze(checkout,commit,source_map)
 names=set(members);check(len(names)==len(members),'DUPLICATE_MEMBER')
 expected={r['path']:r for r in member_plan['payload_members']}
 check(names==set(expected)|{'SELECTIVE_PACKAGE_INFO.json'},'EXACT_PACKAGE_ALLOWLIST')
 for name,row in expected.items():check(len(members[name])==row['bytes'] and sha(members[name])==row['sha256'],'CANDIDATE_MEMBER_IDENTITY')
 info=json.loads(members['SELECTIVE_PACKAGE_INFO.json'])
 check(info['builder_source_commit']==commit,'PACKAGE_COMMIT_BINDING')
 check(all(not n.startswith('/') and '..' not in Path(n).parts for n in names),'UNSAFE_MEMBER')
 check('SELECTIVE_PACKAGE_INFO.json' in members,'PACKAGE_INFO_REQUIRED')
 out=Path(output);check(not out.exists(),'NO_OVERWRITE')
 with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in sorted(members.items()):
   info=zipfile.ZipInfo('Taiko5DX_KR_DIAG_217/'+name,(2026,9,23,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,data)
 with zipfile.ZipFile(out) as z:
  check(z.testzip() is None,'PACKAGE_CRC')
  check(set(z.namelist())=={'Taiko5DX_KR_DIAG_217/'+n for n in members},'MEMBER_SET')
  for name,data in members.items():check(z.read('Taiko5DX_KR_DIAG_217/'+name)==data,'PACKAGE_READBACK')
 return {'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'members':len(members),'builder_source_commit':commit}
