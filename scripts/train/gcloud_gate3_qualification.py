#!/usr/bin/env python3
"""Stage, launch and finalize exactly one approved $5 Gate 3 GPU qualification."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = 'executespecv1'
BUCKET = 'ganesh-gate0-model-transfer-1061994342941'
ZONE = 'us-east1-c'
IMAGE = 'common-cu129-ubuntu-2204-nvidia-580-v20260831'
QUALIFICATION_ZONES = ('us-east1-b','us-east1-c','us-east1-d','us-central1-a','us-central1-b','us-central1-c')
CANONICAL_RESCUE_PLAN = '0cb94af6f12bae840c6657c7d7f6402759b0313d7301b81c96afcb9fb5fb342e'
MATERIALIZER_SHA = '422a0559cf25de3d505304fcdcdf7aa1a92968268297c837a1ad14e2b5268b58'
USABLE_FLOOR_PLAN = '3bee60eb0987eccd8147d638b31beb5f4322539c32f68537b6c06d2943573de7'
WORKSPACE_V4_SHA = '0b044e5dc44cc7bc1828cc73f5964a825baafb90d16c7aeac4d8264537d114ae'

def region_for(zone):
    if zone not in QUALIFICATION_ZONES: raise ValueError('zone escaped bounded US qualification regions')
    return zone.rsplit('-',1)[0]

def sha(path):
    d = hashlib.sha256()
    with Path(path).open('rb') as h:
        for chunk in iter(lambda: h.read(1024*1024), b''): d.update(chunk)
    return d.hexdigest()

def seal(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()

def save(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as h: json.dump(value,h,indent=2,sort_keys=True); h.write('\n')

def run(out, label, *args):
    project_args=[] if any(a.startswith('--project=') for a in args) else [f'--project={PROJECT}']
    result = subprocess.run(['gcloud',*args,*project_args],capture_output=True,text=True,timeout=300)
    save(out / f'{label}.json', {'command':list(args),'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    if result.returncode: raise RuntimeError(f'{label}: {result.stderr}')
    return json.loads(result.stdout) if result.stdout.strip().startswith(('{','[')) else result.stdout

def upload(out, prefix, label, path):
    uri = f'{prefix}/input/{path.name}'
    run(out, f'upload-{label}', 'storage','cp',str(path),uri,'--if-generation-match=0')
    m=run(out,f'metadata-{label}','storage','objects','describe',uri,'--format=json')
    pinned=f"{uri}#{m['generation']}"
    target=out/'roundtrip'/path.name; target.parent.mkdir(exist_ok=True)
    run(out,f'roundtrip-{label}','storage','cp',pinned,str(target))
    if sha(target)!=sha(path) or target.stat().st_size != path.stat().st_size: raise ValueError('upload roundtrip mismatch')
    return {'uri':pinned,'sha256':sha(path),'size_bytes':path.stat().st_size}

def boundary(card):
    body=dict(card); claimed=body.pop('execution_sha256')
    if seal(body)!=claimed: raise ValueError('card seal mismatch')
    expected={'schema_version':'ganesh-mini-gate3-qualification-gcloud/v1',
              'absolute_incremental_ceiling_usd':'5','quality_pilot_allowed':False,
              'maximum_vm_seconds':7200,'probe_rows':16,'project':PROJECT}
    if any(card.get(k)!=v for k,v in expected.items()): raise ValueError('qualification boundary mismatch')
    region = region_for(card.get('zone'))
    if region == 'us-central1' and card.get('cross_region_transfer_reserve_usd') != '0.50':
        raise ValueError('cross-region transfer reserve required')
    spent=card.get('prior_spend_reserve_usd','0')
    if spent not in ('0','1.00','2.00','2.50'): raise ValueError('unbounded prior spending')
    if spent=='1.00' and (card.get('preprobe_startup_rescue_only') is not True or
                         len(card.get('prior_execution_card_sha256',''))!=64):
        raise ValueError('exact preprobe startup rescue binding required')
    if spent=='2.00':
        if (card.get('canonical_rescue_plan_sha256')!=CANONICAL_RESCUE_PLAN or
            card.get('maximum_additional_allocated_starts')!=1 or
            card.get('prior_paid_attempts')!=['20260929T112530Z','20260929T114450Z'] or
            card.get('support_reserve_usd')!='0.737956976' or
            card.get('cross_region_transfer_reserve_usd')!='0.50' or
            card.get('provider_two_hour_upper_usd')!='1.762043024' or
            card.get('inputs',{}).get('model_materializer',{}).get('sha256')!=MATERIALIZER_SHA):
            raise ValueError('canonical rescue approval/budget/input binding differs')
        total=sum(Decimal(card[k]) for k in ('prior_spend_reserve_usd','support_reserve_usd',
                                           'cross_region_transfer_reserve_usd','provider_two_hour_upper_usd'))
        if total!=Decimal('5'): raise ValueError('cumulative rescue budget differs')
    if spent=='2.50':
        if (card.get('usable_floor_plan_sha256')!=USABLE_FLOOR_PLAN or
            card.get('gpu_hardware_contract')!='ganesh-mini-gate3-l4-usable-v1' or
            card.get('l4_usable_floor_bytes')!=23622320128 or
            card.get('other_gpu_floor_bytes')!=24000000000 or
            card.get('maximum_additional_allocated_starts')!=1 or
            card.get('prior_paid_attempts')!=['20260929T112530Z','20260929T114450Z','20260929T133600Z'] or
            card.get('support_reserve_usd')!='0.237956976' or
            card.get('cross_region_transfer_reserve_usd')!='0.50' or
            card.get('provider_two_hour_upper_usd')!='1.762043024' or
            card.get('inputs',{}).get('workspace_archive',{}).get('sha256')!=WORKSPACE_V4_SHA or
            card.get('inputs',{}).get('model_materializer',{}).get('sha256')!=MATERIALIZER_SHA):
            raise ValueError('L4 usable-floor retry approval/budget/input binding differs')
        total=sum(Decimal(card[k]) for k in ('prior_spend_reserve_usd','support_reserve_usd',
                                           'cross_region_transfer_reserve_usd','provider_two_hour_upper_usd'))
        if total!=Decimal('5'): raise ValueError('cumulative L4 retry budget differs')

def usable_floor_retry_reserve(prior, approval):
    if approval!=USABLE_FLOOR_PLAN or sha(ROOT/'docs/plans/GATE3_L4_USABLE_MEMORY_RETRY_20260929.md')!=approval:
        raise ValueError('exact approved L4 floor proposal required')
    if prior.name!='20260929T133600Z': raise ValueError('exact hardware-guard attempt required')
    for attempt,digest,exit_code in [
        ('20260929T112530Z','f0268ab2cb3fede3034bb081e01a8e50b30dec141f218b75a919b256cbdf739a',2),
        ('20260929T114450Z','464bb74ce4eda39dcc939d8da5ff920202f6a3c57afccf0aac1af036cd0e4ce1',1),
        ('20260929T133600Z','f5a61b95a48fddf25e941613446d3e82ff259120dabb19e096f4abee542d21d5',1)]:
        folder=prior.parent/attempt
        c=json.loads((folder/'execution-card.json').read_text()); boundary(c)
        f=json.loads((folder/'finalization.json').read_text())
        if (c['execution_sha256']!=digest or f['status']!='terminal-backup-verified-and-exact-resources-absent-twice' or
            f['qualification_exit_code']!=exit_code or any((folder/'terminal-roundtrip').rglob('throughput.json'))):
            raise ValueError('prior paid attempt or no-measurement evidence differs')
        backup=json.loads((folder/'terminal-backup-verification.json').read_text())
        if backup['status']!='verified' or backup['object_count']<5: raise ValueError('prior backup not verified')
        vm=json.loads(json.loads(sorted(folder.glob('terminal-instance-*.json'))[-1].read_text())['stdout'])
        seconds=(datetime.fromisoformat(vm['lastStopTimestamp'])-datetime.fromisoformat(vm['lastStartTimestamp'])).total_seconds()
        if vm['status']!='TERMINATED' or not 0<seconds<=900: raise ValueError('prior paid runtime exceeded reserve bound')
    assessment=json.loads((prior/'hardware-guard-failure-assessment-v1.json').read_text())
    claimed=assessment.pop('evidence_sha256')
    if claimed!='ae5dd771eb6fe9796eafdad05be0d6a14679a114d6207a986c57936c26aca889' or seal(assessment)!=claimed:
        raise ValueError('exact hardware stop evidence differs')
    if sha(ROOT/'scripts/train/inspect_model_archive.py')!=MATERIALIZER_SHA:
        raise ValueError('tested model materializer differs')
    for path in prior.parent.glob('*/execution-card.json'):
        c=json.loads(path.read_text())
        if c.get('usable_floor_plan_sha256')==approval:
            result=path.parent/'create-instance.json'
            refusal=path.parent/'refusal-finalization.json'
            if not result.exists() or json.loads(result.read_text())['exit_code']==0 or not refusal.exists():
                raise ValueError('L4 retry already allocated or pending; never duplicate')
    return {'prior_spend_reserve_usd':'2.50','prior_paid_attempts':['20260929T112530Z','20260929T114450Z','20260929T133600Z'],
            'usable_floor_plan_sha256':approval,'maximum_additional_allocated_starts':1,
            'gpu_hardware_contract':'ganesh-mini-gate3-l4-usable-v1',
            'l4_usable_floor_bytes':23622320128,'other_gpu_floor_bytes':24000000000,
            'support_reserve_usd':'0.237956976','cross_region_transfer_reserve_usd':'0.50',
            'transfer_reserve_is_within_support_reserve':False}

def canonical_retry_reserve(prior, approval):
    if approval!=CANONICAL_RESCUE_PLAN or sha(ROOT/'docs/plans/GATE3_CANONICAL_MODEL_MATERIALIZATION_RESCUE_20260929.md')!=approval:
        raise ValueError('exact approved canonical rescue proposal required')
    if prior.name!='20260929T114450Z': raise ValueError('exact metadata-failure attempt required')
    preprobe_retry_reserve(prior.parent/'20260929T112530Z')
    card=json.loads((prior/'execution-card.json').read_text()); boundary(card)
    if card['execution_sha256']!='464bb74ce4eda39dcc939d8da5ff920202f6a3c57afccf0aac1af036cd0e4ce1':
        raise ValueError('metadata-failure card differs')
    ended=json.loads((prior/'finalization.json').read_text())
    if ended['status']!='terminal-backup-verified-and-exact-resources-absent-twice' or ended['qualification_exit_code']!=1:
        raise ValueError('verified metadata-failure teardown required')
    terminal=prior/'terminal-roundtrip'
    if 'model directory file inventory differs' not in (terminal/'startup.stderr.log').read_text() or any(terminal.rglob('throughput.json')):
        raise ValueError('not the exact unmeasured metadata failure')
    for name,expected in [('prior-runtime-budget-v1.json','d796e5160cedb4c8c40547b90b6047828544f7b7e1857c47c078b2557434d55e'),
                          ('model-archive-canonical-materialization-v1.json','fe540d05ffa45b1392b87d83885dda21d9598a6dc6b7f2b19a126b088bd98402'),
                          ('canonical-model-input-recheck.json','12ef547d30aac92d4303b30a2ae56295480a2dfaf2cd64905598702b1add1026')]:
        body=json.loads((prior/name).read_text()); claimed=body.pop('evidence_sha256')
        if claimed!=expected or seal(body)!=claimed: raise ValueError('CPU/prior-runtime evidence differs')
    if sha(ROOT/'scripts/train/inspect_model_archive.py')!=MATERIALIZER_SHA: raise ValueError('tested materializer drift')
    # A successful allocation consumes the exception even if its probe fails.
    for path in prior.parent.glob('*/execution-card.json'):
        previous=json.loads(path.read_text())
        if previous.get('canonical_rescue_plan_sha256')==approval:
            result=path.parent/'create-instance.json'
            refusal=path.parent/'refusal-finalization.json'
            if not result.exists() or json.loads(result.read_text())['exit_code']==0 or not refusal.exists():
                raise ValueError('canonical rescue already allocated or pending; never duplicate')
    return {'prior_spend_reserve_usd':'2.00','prior_paid_attempts':['20260929T112530Z','20260929T114450Z'],
            'canonical_rescue_plan_sha256':approval,'maximum_additional_allocated_starts':1,
            'support_reserve_usd':'0.737956976','cross_region_transfer_reserve_usd':'0.50'}

def preprobe_retry_reserve(prior):
    """One bootstrap-only rescue, not repetition of a measured/trained probe."""
    card=json.loads((prior/'execution-card.json').read_text()); boundary(card)
    if card.get('prior_spend_reserve_usd','0')!='0': raise ValueError('no chained paid startup retries')
    ended=json.loads((prior/'finalization.json').read_text())
    if ended['status']!='terminal-backup-verified-and-exact-resources-absent-twice' or ended['qualification_exit_code']!=2:
        raise ValueError('verified preprobe teardown required')
    terminal=prior/'terminal-roundtrip'
    if "python: can't open file '/workspace/scripts/cuda/qualify.py': [Errno 2] No such file or directory" not in (terminal/'startup.stderr.log').read_text():
        raise ValueError('not the exact inherited-entrypoint startup failure')
    if any(terminal.rglob('throughput.json')): raise ValueError('a measured probe cannot be repeated')
    latest=sorted(prior.glob('terminal-instance-*.json'))[-1]
    vm=json.loads(json.loads(latest.read_text())['stdout'])
    elapsed=(datetime.fromisoformat(vm['lastStopTimestamp'])-datetime.fromisoformat(vm['lastStartTimestamp'])).total_seconds()
    if vm['status']!='TERMINATED' or not 0<elapsed<=900: raise ValueError('first VM exceeded 15-minute cost envelope')
    return {'prior_spend_reserve_usd':'1.00','prior_execution_card_sha256':card['execution_sha256'],
            'preprobe_startup_rescue_only':True,'prior_runtime_seconds':elapsed,
            'prior_evidence_prefix':card['prefix']}

def prepare(out, zone=ZONE, reuse=None, prior_preprobe=None, canonical_prior=None, approval=None, usable_floor_prior=None):
    region_name = region_for(zone)
    retry=preprobe_retry_reserve(prior_preprobe) if prior_preprobe is not None else {}
    if canonical_prior is not None:
        if retry: raise ValueError('mutually exclusive rescue scopes')
        retry=canonical_retry_reserve(canonical_prior,approval)
    if usable_floor_prior is not None:
        if retry: raise ValueError('mutually exclusive rescue scopes')
        retry=usable_floor_retry_reserve(usable_floor_prior,approval)
    if out.exists(): raise ValueError('unused evidence directory required')
    out.mkdir(parents=True)
    attempt=out.name
    datetime.strptime(attempt,'%Y%m%dT%H%M%SZ')
    prefix=f'gs://{BUCKET}/ganesh-mini-1.0/gate3/capability-qualification/{attempt}'
    prior=json.loads((ROOT/'measurement/gate4/gradient-conflict-probe-20260914/attempts/20260914T003000Z/execution-card.json').read_text())
    inputs={k:prior['inputs'][k] for k in ('model_archive','cuda_image_archive','docker_bundle')}
    for k,r in inputs.items():
        m=run(out,f'inspect-{k}','storage','objects','describe',r['uri'],'--format=json')
        if str(m['generation'])!=r['uri'].rsplit('#',1)[1] or int(m['size'])!=r['size_bytes']: raise ValueError('pinned object mismatch')
    region=run(out,'region','compute','regions','describe',region_name,'--format=json')
    quotas={q['metric']:q for q in region['quotas']}
    if quotas['NVIDIA_L4_GPUS']['limit']-quotas['NVIDIA_L4_GPUS']['usage']<1: raise ValueError('no L4 quota')
    boot=run(out,'boot-image','compute','images','describe',IMAGE,'--project=deeplearning-platform-release','--format=json')
    if boot['status']!='READY' or boot['id']!='5785010291456121629': raise ValueError('boot image drift')
    workspace_version='v4' if usable_floor_prior is not None else 'v3'
    archive=ROOT/f'artifacts/train/gate3-capability-pilot-v2/workspace-{workspace_version}.tar.gz'
    manifest=ROOT/f'artifacts/train/gate3-capability-pilot-v2/workspace-{workspace_version}-manifest.json'
    m=json.loads(manifest.read_text())
    if sha(archive)!=m['archive_sha256']: raise ValueError('workspace archive drift')
    import tarfile
    with tarfile.open(archive) as t:
        members=t.getmembers()
        if len([x for x in members if x.isfile()])!=(73 if usable_floor_prior is not None else 72) or any('data/eval/' in x.name for x in members): raise ValueError('workspace boundary failed')
        for member in members:
            p=Path(member.name)
            if p.is_absolute() or '..' in p.parts or not (member.isfile() or member.isdir()): raise ValueError('unsafe workspace member')
    if reuse is not None:
        previous=json.loads((reuse/'execution-card.json').read_text()); boundary(previous)
        if previous.get('prior_spend_reserve_usd','0')!='0' and not retry:
            raise ValueError('capacity retry must retain the prior paid-attempt budget reserve')
        ended=json.loads((reuse/'refusal-finalization.json').read_text())
        if ended.get('gpu_runtime_cost_usd')!='0' or ended.get('status')!='capacity-refusal-preserved-resources-absent-twice':
            raise ValueError('reuse requires an independently finalized zero-runtime refusal')
        for label,path in [('workspace_archive',archive),('workspace_manifest',manifest)]:
            row=previous['inputs'][label]
            if row['sha256']!=sha(path) or row['size_bytes']!=path.stat().st_size: raise ValueError('workspace reuse drift')
            inputs[label]=row
    else:
        for label,path in [('workspace_archive',archive),('workspace_manifest',manifest)]: inputs[label]=upload(out,prefix,label,path)
    if canonical_prior is not None or usable_floor_prior is not None:
        inputs['model_materializer']=upload(out,prefix,'model-materializer',ROOT/'scripts/train/inspect_model_archive.py')
    stem=f'ganesh-g3-qual-{attempt.lower()}'
    card={'schema_version':'ganesh-mini-gate3-qualification-gcloud/v1','status':'authorized-qualification-only',
          'approved_at':datetime.now(timezone.utc).isoformat(),'approval':'Navneet: you can use GCP GPUs; yes to $5 qualification-only ceiling',
          'absolute_incremental_ceiling_usd':'5','quality_pilot_allowed':False,'probe_rows':16,
          'maximum_vm_seconds':7200,'controller_seconds':6000,'backup_reserve_seconds':1200,
          'project':PROJECT,'zone':zone,'machine_type':'g2-standard-8','prefix':prefix,
          'instance':stem,'disk':stem,'network':stem+'-net','subnet':stem+'-subnet',
          'boot_image':boot['selfLink'],'boot_image_id':boot['id'],
          'inputs':inputs,'compute_hourly_usd':'0.853624312','disk_hourly_usd':'0.027397200',
          'provider_two_hour_upper_usd':'1.762043024','support_reserve_usd':'3.237956976',
          'cross_region_transfer_reserve_usd':'0.50' if region_name=='us-central1' else '0',
          'transfer_reserve_is_within_support_reserve':True,
          'price_sources':['https://cloud.google.com/products/compute/pricing/accelerator-optimized','https://cloud.google.com/compute/disks-image-pricing'],
          'price_checked_at':datetime.now(timezone.utc).isoformat(),
          'teardown_requires':'verified terminal inventory and two independent GCS download hash checks',
          'cuda_image_id':prior['cuda_image']['image_id']}
    if retry:
        card.update(retry)
        if canonical_prior is not None: card['approval']='Navneet approved canonical rescue proposal '+approval+' under SAME cumulative $5 ceiling'
        elif usable_floor_prior is not None: card['approval']='Navneet approved L4 usable-floor retry proposal '+approval+' under SAME cumulative $5 ceiling'
        else: card['support_reserve_usd']='2.237956976'
    if region_name=='us-central1': card['price_sources'].append('https://cloud.google.com/storage/pricing')
    card['execution_sha256']=seal(card)
    boundary(card)
    save(out/'execution-card.json',card)
    startup=ROOT/'scripts/train/gcloud_gate3_qualification_startup.sh'
    startup_row=upload(out,prefix,'startup',startup)
    card_row=upload(out,prefix,'card',out/'execution-card.json')
    save(out/'launch-inputs.json',{'card':card_row,'startup':startup_row})
    print(json.dumps({'status':'staged','card_sha256':card['execution_sha256'],'evidence':str(out)}))

def launch(out):
    card=json.loads((out/'execution-card.json').read_text()); boundary(card)
    inputs=json.loads((out/'launch-inputs.json').read_text())
    # No duplicate VM or collisions; exact immutable names are used for every action.
    for kind,key in [('instances','instance'),('disks','disk'),('networks','network')]:
        rows=run(out,f'absence-{key}','compute',kind,'list',f"--filter=name={card[key]}",'--format=json')
        if rows: raise ValueError(f'existing {key}; do not duplicate')
    rows=run(out,'absence-subnet','compute','networks','subnets','list',f"--filter=name={card['subnet']}",'--format=json')
    if rows: raise ValueError('existing subnet')
    run(out,'create-network','compute','networks','create',card['network'],'--subnet-mode=custom')
    run(out,'create-subnet','compute','networks','subnets','create',card['subnet'],f"--region={region_for(card['zone'])}",f"--network={card['network']}",'--range=10.244.1.0/28','--enable-private-ip-google-access')
    startup=(out/'roundtrip'/ 'gcloud_gate3_qualification_startup.sh')
    if sha(startup)!=inputs['startup']['sha256']: raise ValueError('startup snapshot drift')
    metadata=','.join([f'ganesh-project={PROJECT}',f"ganesh-prefix={card['prefix']}",f"ganesh-card-uri={inputs['card']['uri']}",f"ganesh-card-sha={inputs['card']['sha256']}"])
    run(out,'create-instance','compute','instances','create',card['instance'],f"--zone={card['zone']}",
        '--machine-type=g2-standard-8',f"--image={card['boot_image']}",
        '--boot-disk-size=200GB','--boot-disk-type=pd-balanced',f"--boot-disk-device-name={card['disk']}",
        f"--network-interface=network={card['network']},subnet={card['subnet']},no-address",
        '--service-account=1061994342941-compute@developer.gserviceaccount.com','--scopes=cloud-platform',
        '--provisioning-model=STANDARD','--max-run-duration=2h','--instance-termination-action=STOP',
        '--maintenance-policy=TERMINATE','--no-restart-on-failure','--reservation-affinity=none',
        f'--metadata={metadata}',f'--metadata-from-file=startup-script={startup}',
        '--labels=project=ganesh-mini,gate=g3,purpose=qualification','--format=json')
    print(json.dumps({'status':'launched','instance':card['instance'],'ceiling_usd':'5'}))

def inspect(out):
    card=json.loads((out/'execution-card.json').read_text()); boundary(card)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    value=run(out,'status-'+stamp,'compute','instances','describe',card['instance'],f"--zone={card['zone']}",'--format=json')
    if value['status'] not in ('TERMINATED','STOPPING'):
        try:
            run(out,'serial-'+stamp,'compute','instances','get-serial-port-output',card['instance'],f"--zone={card['zone']}")
        except RuntimeError as error:
            # Serial availability is optional; the command/error is retained.
            # The authoritative instance state and terminal hash verification
            # still govern cleanup, never this best-effort diagnostic endpoint.
            print(json.dumps({'serial_unavailable':str(error)}))
    print(json.dumps({'status':value['status'],'instance':value['name']}))
    return value

def watch(out):
    """Observe this exact VM only; verify evidence before one finalization."""
    card=json.loads((out/'execution-card.json').read_text()); boundary(card)
    if (out/'finalization.json').exists(): raise ValueError('already finalized; do not duplicate watcher')
    # Exclusive local marker prevents a heartbeat from starting another watcher.
    save(out/'watcher-started.json',{'instance':card['instance'],
                                   'pid':os.getpid(),
                                   'started_at':datetime.now(timezone.utc).isoformat(),
                                   'maximum_watch_seconds':8100})
    deadline=time.monotonic()+8100
    while time.monotonic()<deadline:
        value=inspect(out)
        if value['status']=='TERMINATED':
            finalize(out)
            return
        time.sleep(60)
    raise RuntimeError('watch bound reached; preserve disk and inspect exact terminal backup before cleanup')

def finalize(out):
    card=json.loads((out/'execution-card.json').read_text()); boundary(card)
    target=out/'terminal-roundtrip'
    subprocess.run(['python3',str(ROOT/'scripts/cuda/gcloud_backup_manifest.py'),
                    '--project',PROJECT,'--prefix',card['prefix']+'/terminal',
                    '--output',str(out/'terminal-backup-verification.json'),'--download-dir',str(target)],check=True)
    files=(target/'runtime-files.sha256').read_text().splitlines()
    for line in files:
        digest,relative=line.split('  ',1)
        path=target/relative
        if not path.resolve().is_relative_to(target.resolve()) or sha(path)!=digest: raise ValueError('terminal inventory mismatch')
    if not files or not (target/'startup-exit-code.txt').exists(): raise ValueError('incomplete terminal backup')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    vm=run(out,'terminal-instance-'+stamp,'compute','instances','describe',card['instance'],f"--zone={card['zone']}",'--format=json')
    if vm['status']!='TERMINATED': raise ValueError('terminal is not stopped; do not delete running producer')
    run(out,'delete-instance','compute','instances','delete',card['instance'],f"--zone={card['zone']}",'--quiet')
    run(out,'delete-subnet','compute','networks','subnets','delete',card['subnet'],f"--region={region_for(card['zone'])}",'--quiet')
    run(out,'delete-network','compute','networks','delete',card['network'],'--quiet')
    for check in (1,2):
        for kind,key in [('instances','instance'),('disks','disk'),('networks','network')]:
            values=run(out,f'final-absence-{key}-{check}','compute',kind,'list',f"--filter=name={card[key]}",'--format=json')
            if values: raise ValueError('resource remains after teardown')
        values=run(out,f'final-absence-subnet-{check}','compute','networks','subnets','list',f"--filter=name={card['subnet']}",'--format=json')
        if values: raise ValueError('subnet remains')
    run(out,'project-instances-after','compute','instances','list','--format=json')
    run(out,'project-disks-after','compute','disks','list','--format=json')
    run(out,'project-addresses-after','compute','addresses','list','--format=json')
    save(out/'finalization.json',{'status':'terminal-backup-verified-and-exact-resources-absent-twice',
                               'qualification_exit_code':int((target/'startup-exit-code.txt').read_text()),
                               'quality_pilot_executed':False,'prefix':card['prefix']})
    run(out,'backup-local-evidence','storage','rsync',str(out),card['prefix']+'/local-evidence','--recursive')
    print(json.dumps({'status':'finalized','evidence':str(out)}))

def failure_finalize(out):
    card=json.loads((out/'execution-card.json').read_text()); boundary(card)
    result=json.loads((out/'create-instance.json').read_text())
    if result['exit_code']==0 or 'ZONE_RESOURCE_POOL_EXHAUSTED' not in result['stderr']:
        raise ValueError('not an exact capacity refusal')
    for kind,key in [('instances','instance'),('disks','disk')]:
        rows=run(out,'refusal-absence-'+key,'compute',kind,'list',f"--filter=name={card[key]}",'--format=json')
        if rows: raise ValueError('VM/disk exists: preserve and recover before cleanup')
    run(out,'backup-refusal','storage','rsync',str(out),card['prefix']+'/launch-refusal','--recursive')
    subprocess.run(['python3',str(ROOT/'scripts/cuda/gcloud_backup_manifest.py'),'--project',PROJECT,
                    '--prefix',card['prefix']+'/launch-refusal','--output',str(out/'refusal-backup-verification.json'),
                    '--download-dir',str(out/'refusal-roundtrip')],check=True)
    run(out,'delete-refusal-subnet','compute','networks','subnets','delete',card['subnet'],f"--region={region_for(card['zone'])}",'--quiet')
    run(out,'delete-refusal-network','compute','networks','delete',card['network'],'--quiet')
    for check in (1,2):
        for kind,key in [('instances','instance'),('disks','disk'),('networks','network')]:
            rows=run(out,f'refusal-final-{key}-{check}','compute',kind,'list',f"--filter=name={card[key]}",'--format=json')
            if rows: raise ValueError('refusal resource remains')
        rows=run(out,f'refusal-final-subnet-{check}','compute','networks','subnets','list',f"--filter=name={card['subnet']}",'--format=json')
        if rows: raise ValueError('refusal subnet remains')
    save(out/'refusal-finalization.json',{'status':'capacity-refusal-preserved-resources-absent-twice',
                                        'quality_result':False,'gpu_runtime_cost_usd':'0'})
    # Keep the independent roundtrip outside the recursive upload source.
    run(out,'backup-refusal-finalization','storage','cp',str(out/'refusal-finalization.json'),card['prefix']+'/refusal-finalization.json','--if-generation-match=0')
    run(out,'backup-refusal-cleanup-evidence','storage','rsync',str(out),card['prefix']+'/cleanup-evidence','--recursive','--exclude=refusal-roundtrip/.*')
    print(json.dumps({'status':'refusal-finalized','next_zone_allowed':True}))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['prepare','launch','inspect','watch','finalize','failure_finalize'])
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--zone',default=ZONE)
    parser.add_argument('--reuse-inputs',type=Path)
    parser.add_argument('--prior-preprobe-attempt',type=Path)
    parser.add_argument('--canonical-rescue-prior',type=Path)
    parser.add_argument('--usable-floor-retry-prior',type=Path)
    parser.add_argument('--approved-plan-sha')
    args=parser.parse_args()
    if args.stage=='prepare': prepare(args.output.resolve(),args.zone,args.reuse_inputs,args.prior_preprobe_attempt,
                                     args.canonical_rescue_prior,args.approved_plan_sha,args.usable_floor_retry_prior)
    else: globals()[args.stage](args.output.resolve())

if __name__=='__main__': main()
