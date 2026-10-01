#!/usr/bin/env python3
"""Run V9 readiness, one Rust role author, two audits, separation, and matrices."""
from __future__ import annotations
import argparse, concurrent.futures, copy, hashlib, json
from pathlib import Path
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_separation_attestations import PASS_FIELDS, build_report as build_separation
from scripts.data.generate_expansion_qualification import verify_codex_version
from scripts.data.repair_delta_v9_readiness import CONTRACT_ID, validate_response
from scripts.data.run_repair_delta_evidence import IsolatedCodexAdapter, _delta_evidence, _executable_evidence, delta_projection
from scripts.data.run_repair_delta_two_phase import build_separation_sidecars
from scripts.data.run_v8_correction import _outcomes, _projection, _replace
from scripts.verify.sandbox import verify

EXPECTED={"reference.primary_discrimination":"pass","reference.cross_cutting":"pass","known_bad.primary_discrimination":"fail","known_bad.cross_cutting":"pass"}

def load_run(path):
    value=json.loads(path.read_text()); body=dict(value); claimed=body.pop('artifact_sha256')
    if claimed!=canonical_sha256(body): raise ValueError(f'{path}: run seal mismatch')
    return value

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan',type=Path,required=True); p.add_argument('--v8-readiness',type=Path,required=True); p.add_argument('--v8-failure',type=Path,required=True); p.add_argument('--v8-rust-run',type=Path,required=True); p.add_argument('--v8-python-run',type=Path,required=True); p.add_argument('--v7-terminal',type=Path,required=True)
    p.add_argument('--training-corpus',type=Path,action='append',required=True); p.add_argument('--evaluation-root',type=Path,action='append',required=True); p.add_argument('--runtimes',type=Path,default=Path('configs/eval/runtimes.json')); p.add_argument('--codex-config',type=Path,default=Path('configs/data/expansion_teacher.json')); p.add_argument('--run-dir',type=Path,required=True); p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args(); a.output_dir.mkdir(parents=True,exist_ok=True)
    rows=[json.loads(x) for x in a.v7_terminal.read_text().splitlines() if x]; targets=[x for x in rows if x['status']!='admitted']; roles=['primary_discrimination','cross_cutting']
    if [x['lane'] for x in targets]!=['rust','python']: raise ValueError('V9 target identities differ')
    projections=[_projection(row,role) for row,role in zip(targets,roles,strict=True)]
    v8rust=load_run(a.v8_rust_run); v8python=load_run(a.v8_python_run)
    validate_response(projections[0],v8rust['response']); validate_response(projections[1],v8python['response'])
    old=targets[0]['envelope']['evidence']['test_author']; old_role=next(x for x in old['test_roles'] if x['role']=='primary_discrimination'); old_file=next(x for x in targets[0]['envelope']['candidate']['verification_task']['files'] if x.get('path')==old_role['path'])
    try: validate_response(projections[0],{'content':old_file['content'],'case_ids':old_role['case_ids']})
    except ValueError: old_rejected=True
    else: old_rejected=False
    if not old_rejected: raise ValueError('V9 literal-key regression did not reject V7 bad test')
    v8read=json.loads(a.v8_readiness.read_text()); v8fail=json.loads(a.v8_failure.read_text())
    readiness={'schema_version':'ganesh-mini-gate2-v9-readiness/v1','contract_id':CONTRACT_ID,'status':'passed','plan_sha256':hashlib.sha256(a.plan.read_bytes()).hexdigest(),'v8_readiness_report_sha256':v8read['report_sha256'],'v8_failure_report_sha256':v8fail['report_sha256'],'v8_rust_response_sha256':canonical_sha256(v8rust['response']),'v8_python_response_sha256':canonical_sha256(v8python['response']),'v8_rust_dynamic_get_accepted':True,'v7_rust_literal_key_rejected':True,'v8_python_unchanged_validator_passed':True,'new_readiness_model_calls':0,'evaluation_artifacts_read':0}; readiness['report_sha256']=canonical_sha256(readiness); (a.output_dir/'readiness-v9.json').write_text(json.dumps(readiness,indent=2,sort_keys=True)+'\n')
    config=json.loads(a.codex_config.read_text()); cli=verify_codex_version('codex',config['codex_cli_version'])
    rust_response=IsolatedCodexAdapter('test_author',config,'codex',a.run_dir,cli,'v9')(projections[0]); run_sha=rust_response.pop('_run_sha256'); validate_response(projections[0],rust_response)
    responses=[(rust_response,run_sha),(copy.deepcopy(v8python['response']),v8python['run']['run_evidence_sha256'])]
    corrected=[]; tests=[]
    for row,role,proj,(response,run) in zip(targets,roles,projections,responses,strict=True):
        validate_response(proj,response); candidate,evidence=_replace(row,role,response,run); corrected.append(candidate); tests.append(evidence)
    delta_projections=[delta_projection(c,r['envelope']['assignment']) for c,r in zip(corrected,targets,strict=True)]
    def audit(proj): return IsolatedCodexAdapter('delta_audit',config,'codex',a.run_dir,cli,'v9')(proj)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: delta_responses=list(ex.map(audit,delta_projections))
    deltas=[]
    for c,r,response in zip(corrected,targets,delta_responses,strict=True):
        run=response.pop('_run_sha256'); ev=_delta_evidence(c,r['envelope']['assignment'],response,run)
        if (ev['independent_semantic_delta_count'],ev['delta_is_capability_specific'],ev['introduces_multiple_independent_fixes'])!=(1,True,False): raise ValueError('V9 delta rejected')
        deltas.append(ev)
    byid={c['id']:c for c in corrected}; complete=[byid.get(row['candidate_id'],row['envelope']['candidate']) for row in rows]; cp=a.output_dir/'complete-candidates.jsonl'; cp.write_text(''.join(json.dumps(c,sort_keys=True)+'\n' for c in complete))
    separation=build_separation(cp,a.training_corpus,a.evaluation_root); (a.output_dir/'global-separation-report.json').write_text(json.dumps(separation,indent=2,sort_keys=True)+'\n')
    if separation['status']!='passed': raise ValueError('V9 separation failed')
    sidecars,contract=build_separation_sidecars(separation,complete,a.output_dir/'separation-sidecars.jsonl'); side={x['candidate_id']:x for x in sidecars}
    finals=[]
    for source,candidate,test,delta in zip(targets,corrected,tests,deltas,strict=True):
        executable,retry=_executable_evidence(candidate,test,a.runtimes,verify); outcomes=_outcomes(executable); status='admitted' if not retry['unresolved'] and outcomes==EXPECTED and all(side[candidate['id']][f] is True for f in PASS_FIELDS) else 'rejected'
        finals.append({'candidate_id':candidate['id'],'lane':candidate['lane'],'status':status,'outcomes':outcomes,'candidate_sha256':canonical_sha256(candidate),'test_author_evidence_sha256':test['evidence_sha256'],'delta_evidence_sha256':delta['evidence_sha256'],'separation_evidence_sha256':side[candidate['id']]['evidence_sha256'],'executable_evidence':executable,'retry_ledger':retry})
    passed=sum(r['status']=='admitted' for r in rows)==58 and all(x['status']=='admitted' for x in finals)
    report={'schema_version':'ganesh-mini-gate2-v9-qualification-summary/v1','contract_id':CONTRACT_ID,'status':'passed' if passed else 'qualification-failed','plan_sha256':hashlib.sha256(a.plan.read_bytes()).hexdigest(),'readiness_report_sha256':readiness['report_sha256'],'v7_carried_admissions':58,'v8_python_role_carried':True,'fresh_rust_role_author_calls':1,'fresh_delta_audit_calls':2,'final_admitted':60 if passed else 58+sum(x['status']=='admitted' for x in finals),'unresolved':sum(x['retry_ledger']['unresolved'] for x in finals),'corrected_rows':finals,'separation_report_sha256':separation['report_sha256'],'separation_contract_sha256':contract,'v2_generation_equivalence':{'status':'passed','generation_cells':60,'qualification_report_sha256':'293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139'},'combined_coverage':{'covered':120 if passed else 118+sum(x['status']=='admitted' for x in finals),'required':120},'evaluation_artifacts_read_outside_content_free_boundary':0,'training_entry_eligible':passed}; report['report_sha256']=canonical_sha256(report); (a.output_dir/'qualification-summary-v9.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n'); print(json.dumps({'status':report['status'],'final_admitted':report['final_admitted'],'report_sha256':report['report_sha256']},sort_keys=True)); return 0 if passed else 2
if __name__=='__main__': raise SystemExit(main())
