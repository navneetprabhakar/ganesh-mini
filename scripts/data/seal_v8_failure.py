#!/usr/bin/env python3
"""Seal V8's pre-execution validator failure and exact call accounting."""
import argparse, hashlib, json
from pathlib import Path
from scripts.data.build_capability_corpus_plan import canonical_sha256

def main():
    p=argparse.ArgumentParser(); p.add_argument('--plan',type=Path,required=True); p.add_argument('--readiness',type=Path,required=True); p.add_argument('--run-dir',type=Path,required=True); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
    readiness=json.loads(a.readiness.read_text()); runs=[]
    for path in sorted(a.run_dir.glob('*.test_author.json')):
        value=json.loads(path.read_text()); runs.append({'candidate_id':value['candidate_id'],'file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'artifact_sha256':value['artifact_sha256'],'response_sha256':canonical_sha256(value['response'])})
    if len(runs)!=2: raise ValueError('V8 failure accounting requires exact two role-author artifacts')
    report={'schema_version':'ganesh-mini-gate2-v8-qualification-failure/v1','contract_id':'capability-stratified-v8-two-role-correction/v1','status':'qualification-failed','reason':'rust-semantic-guard-overbroad-metadata-get-pattern','plan_sha256':hashlib.sha256(a.plan.read_bytes()).hexdigest(),'readiness_report_sha256':readiness['report_sha256'],'role_author_calls':2,'delta_audit_calls':0,'candidate_executable_suites':0,'role_runs':runs,'rust_response_observation':'behavioral assertions use metadata().get(&key) only for dynamically carried unrelated keys; no literal canonical key is asserted','python_response_observation':'tests only input non-mutation and contains no digest assertion or hash interception','evaluation_artifacts_read':0,'training_entry_eligible':False}
    report['report_sha256']=canonical_sha256(report); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n'); print(json.dumps({'status':report['status'],'report_sha256':report['report_sha256']},sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
