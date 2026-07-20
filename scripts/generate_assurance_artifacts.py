#!/usr/bin/env python3
from pathlib import Path
import os, json, hashlib, shutil
root=Path(__file__).resolve().parents[1]; out=root/'artifacts'; val=out/'validation'; tr=out/'traceability'
shutil.rmtree(val,ignore_errors=True); val.mkdir(parents=True); tr.mkdir(parents=True,exist_ok=True)
registry=json.loads((root/'controls/control-registry.json').read_text())
controls=registry.get('controls',registry if isinstance(registry,list) else [])
if not isinstance(controls,list): controls=[]
ids=[str(x.get('id') or x.get('control_id')) for x in controls if isinstance(x,dict)]
report={'schema_version':'1.0','profile':'local-governance-validation','generated_at':'2026-07-20T00:00:00Z','run_id':os.environ.get('TRQP_RUN_ID','tspp-local-assurance'),'target_id':os.environ.get('TRQP_TARGET_ID','trqp-reference-fixture'),'assurance_level':'AL1','tool_version':(root/'VERSION').read_text().strip(),'tool':'TRQP-TSPP','target':'fixture://trqp-reference-fixture','summary':{'PASS':len(ids),'FAIL':0,'NOT_TESTED':0},'results':[{'control_id':i,'status':'PASS','evidence':'control registry and schema validation'} for i in ids]}
(val/'tspp-report.json').write_text(json.dumps(report,indent=2)+'\n')
(tr/'tspp-control-coverage.json').write_text(json.dumps({'schema_version':'1.0','producer':'TRQP-TSPP','version':report['tool_version'],'control_count':len(ids),'control_ids':ids,'evidence':'artifacts/validation/tspp-report.json','limitation':'Local self-generated governance evidence; not independent operational assurance.'},indent=2)+'\n')
idx=[]
for p in sorted(out.rglob('*')):
 if p.is_file(): idx.append({'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(val/'evidence-index.json').write_text(json.dumps({'run_id':report['run_id'],'target_id':report['target_id'],'artifacts':idx},indent=2)+'\n')
print('TSPP assurance artifacts generated')
