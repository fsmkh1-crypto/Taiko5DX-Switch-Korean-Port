"""Canonical-source-gated entry point; candidate verification precedes ZIP emission."""
from pathlib import Path
import argparse,json,runpy,hashlib
from package_builder import verify_source_freeze,materialize,check

def main():
 p=argparse.ArgumentParser();p.add_argument('--checkout',required=True);p.add_argument('--commit',required=True);p.add_argument('--source-map',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 here=Path(__file__).resolve().parent;root=here.parents[1];rows=json.loads(Path(a.source_map).read_text())
 required=json.loads((here/'results/SOURCE_FREEZE_REQUIRED.json').read_text())
 required.append({'local_path':str(Path(__file__).resolve()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
 want={(str(Path(r['local_path']).resolve()),r['sha256']) for r in required};got={(str(Path(r['local_path']).resolve()),r['sha256']) for r in rows}
 check(want==got,'EXACT_SOURCE_FREEZE_COVERAGE')
 verify_source_freeze(a.checkout,a.commit,rows)
 state=runpy.run_path(str(here/'validate.py'));members=dict(state['members']);plan=json.loads((here/'results/CANDIDATE_MEMBER_PLAN.json').read_text())
 info={'schema':'BOUNDED_217_DIAGNOSTIC_PACKAGE_V1','builder_source_commit':a.commit,'title_id':plan['title_id'],'version':plan['version'],'build_id':plan['build_id'],'scope':'13_EVENT_FILES_PLUS_INHERITED_ROOT_PROFILE_FONT_IPS','implemented_boundaries':217,'candidate_fingerprint':state['result'].evidence.candidate.fingerprint,'files':plan['payload_members'],'V369':'UNCHANGED','V371':'PARTIAL_BLOCKED','runtime':'NOT_RUN','release_accepted':False}
 members['SELECTIVE_PACKAGE_INFO.json']=(json.dumps(info,sort_keys=True,indent=2)+'\n').encode()
 receipt=materialize(a.checkout,a.commit,rows,members,a.output,plan)
 (here/'PACKAGE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
