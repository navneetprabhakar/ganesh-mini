#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  echo "usage: $0 APPROVAL_TEXT_FILE PRICE_EVIDENCE_JSON RUN_ID ZONE" >&2
  exit 2
}
[[ $# -eq 4 ]] || usage
approval_file="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
price_file="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
run_id="$3"
zone="$4"
[[ "$run_id" =~ ^[0-9]{8}T[0-9]{6}Z$ ]] || { echo "run ID must be an exact UTC timestamp" >&2; exit 2; }
case "$zone" in
  us-east1-b|us-east1-c|us-east1-d) ;;
  *) echo "zone must be an approved G2/L4 zone in us-east1" >&2; exit 2 ;;
esac
repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
[[ -z "$(git -C "$repo_root" status --porcelain --untracked-files=no)" ]] || { echo "tracked worktree must be clean" >&2; exit 3; }
source_commit="$(git -C "$repo_root" rev-parse HEAD)"

project=executespecv1
region=us-east1
machine_type=g2-standard-12
bucket=ganesh-gate0-model-transfer-1061994342941
prefix="ganesh-mini-1.0/gate3/$run_id"
run_id_lower="$(printf '%s' "$run_id" | tr '[:upper:]' '[:lower:]')"
instance="ganesh-mini-g3-l4-$run_id_lower"
disk="$instance"
network="ganesh-mini-g3-net-$run_id_lower"
subnet="ganesh-mini-g3-subnet-$run_id_lower"
cidr=10.244.0.160/28
boot_image_project=deeplearning-platform-release
boot_image_name=common-cu129-ubuntu-2204-nvidia-580-v20260818
boot_image="projects/$boot_image_project/global/images/$boot_image_name"
work_dir="$repo_root/measurement/gate3/gcloud/$run_id"
[[ ! -e "$work_dir" ]] || { echo "run directory already exists: $work_dir" >&2; exit 3; }
mkdir -p "$work_dir/raw" "$work_dir/input-metadata"
failure_prefix="gs://$bucket/$prefix/launch-failure"
resource_stage=0

cleanup_failed_launch() {
  local status="$?"
  trap - EXIT
  if (( status == 0 || resource_stage == 0 )); then exit "$status"; fi
  set +e
  verification_dir="$(mktemp -d "${TMPDIR:-/tmp}/ganesh-gate1-launch-verify.XXXXXX")"
  printf '%s\n' "$status" > "$work_dir/launch-exit-code.txt"
  gcloud storage rsync "$work_dir" "$failure_prefix" --recursive --project="$project"
  backup_status="$?"
  if (( backup_status == 0 )); then
    python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
      --project "$project" --prefix "$failure_prefix" \
      --output "$verification_dir/launch-failure-backup-manifest.json" \
      --download-dir "$verification_dir/launch-failure-download"
    backup_status="$?"
    if (( backup_status == 0 )); then cp "$verification_dir/launch-failure-backup-manifest.json" "$work_dir/"; fi
  fi
  if (( backup_status != 0 )); then
    echo "launch failed and failure evidence could not be verified; refusing resource deletion" >&2
    exit 97
  fi
  if gcloud compute instances describe "$instance" --zone="$zone" --project="$project" --format=json > "$work_dir/raw/failure-instance.json" 2>/dev/null; then
    gcloud storage rsync "$work_dir" "$failure_prefix" --recursive --project="$project" || exit 97
    echo "launch failed after the VM existed; preserving the STOP-bounded VM, disk, subnet, and network for terminal-backup verification" >&2
    exit 97
  fi
  if gcloud compute disks describe "$disk" --zone="$zone" --project="$project" --format=json > "$work_dir/raw/failure-disk.json" 2>/dev/null; then
    gcloud compute disks delete "$disk" --zone="$zone" --project="$project" --quiet || exit 98
  fi
  if gcloud compute networks subnets describe "$subnet" --region="$region" --project="$project" --format=json > "$work_dir/raw/failure-subnet.json" 2>/dev/null; then
    gcloud compute networks subnets delete "$subnet" --region="$region" --project="$project" --quiet || exit 98
  fi
  if gcloud compute networks describe "$network" --project="$project" --format=json > "$work_dir/raw/failure-network.json" 2>/dev/null; then
    gcloud compute networks delete "$network" --project="$project" --quiet || exit 98
  fi
  gcloud compute instances list --zones="$zone" --project="$project" --filter="name=('$instance')" --format=json > "$work_dir/raw/failure-absence-instance.json" || exit 99
  gcloud compute disks list --zones="$zone" --project="$project" --filter="name=('$disk')" --format=json > "$work_dir/raw/failure-absence-disk.json" || exit 99
  gcloud compute networks subnets list --regions="$region" --project="$project" --filter="name=('$subnet')" --format=json > "$work_dir/raw/failure-absence-subnet.json" || exit 99
  gcloud compute networks list --project="$project" --filter="name=('$network')" --format=json > "$work_dir/raw/failure-absence-network.json" || exit 99
  python3 - "$work_dir/launch-failure-cleanup.json" "$work_dir/raw" <<'PY' || exit 99
import hashlib,json,sys
out,root=sys.argv[1:]
files=['failure-absence-instance.json','failure-absence-disk.json','failure-absence-subnet.json','failure-absence-network.json']
for name in files:
 if json.load(open(root+'/'+name))!=[]: raise SystemExit('failed-launch resource still exists: '+name)
value={'schema_version':'ganesh-mini-gate1-launch-failure-cleanup/v1','status':'exact-resources-absent','absence_files':files}
value['evidence_sha256']=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
json.dump(value,open(out,'w'),indent=2,sort_keys=True)
PY
  gcloud storage rsync "$work_dir" "$failure_prefix" --recursive --project="$project" || exit 99
  python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
    --project "$project" --prefix "$failure_prefix" \
    --output "$verification_dir/launch-failure-final-backup-manifest.json" \
    --download-dir "$verification_dir/launch-failure-final-download" || exit 99
  cp "$verification_dir/launch-failure-final-backup-manifest.json" "$work_dir/"
  echo "launch failed; exact temporary resources were removed after verified GCS backup" >&2
  exit "$status"
}
trap cleanup_failed_launch EXIT

approval_text="$(cat "$approval_file")"
python3 - "$approval_text" "$zone" <<'PY'
import sys
text=' '.join(sys.argv[1].lower().split()); zone=sys.argv[2].lower()
required=('approved','gate 3','g2-standard-12',zone,'4 hours','usd 5')
missing=[token for token in required if token not in text]
if missing: raise SystemExit('approval does not bind this Gate 1 launch: '+repr(missing))
PY
eval "$(python3 - "$price_file" <<'PY'
import datetime,hashlib,json,shlex,sys
value=json.load(open(sys.argv[1])); claimed=value.pop('evidence_sha256',None)
actual=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
if claimed != actual or value.get('schema_version') != 'ganesh-mini-gate3-price-evidence/v2' or value.get('status') != 'verified': raise SystemExit('invalid price evidence')
checked=datetime.datetime.fromisoformat(value['checked_at'].replace('Z','+00:00'))
age=datetime.datetime.now(datetime.timezone.utc)-checked
if age < datetime.timedelta(minutes=-5): raise SystemExit('price evidence is dated in the future')
if age > datetime.timedelta(hours=24): raise SystemExit('price evidence is older than 24 hours')
if value.get('region')!='us-east1' or value.get('machine_type')!='g2-standard-12': raise SystemExit('price evidence scope mismatch')
for key in ('conservative_hourly_usd','support_reserve_usd','absolute_cost_ceiling_usd'): print(f'{key}={shlex.quote(str(value[key]))}')
PY
)"
python3 - "$conservative_hourly_usd" "$support_reserve_usd" "$absolute_cost_ceiling_usd" <<'PY'
from decimal import Decimal
import sys
hourly,reserve,ceiling=map(Decimal,sys.argv[1:])
upper=hourly*Decimal(4)+reserve
if hourly<=0 or reserve<0 or ceiling>Decimal('5.00') or upper>=ceiling: raise SystemExit('price evidence exceeds approval')
PY

account="$(gcloud config get-value account 2>/dev/null)"
configured_project="$(gcloud config get-value project 2>/dev/null)"
[[ -n "$account" && "$configured_project" == "$project" ]] || { echo "GCloud identity/project mismatch" >&2; exit 4; }
gcloud compute regions describe "$region" --project="$project" --format=json > "$work_dir/raw/region.json"
gcloud compute machine-types describe "$machine_type" --zone="$zone" --project="$project" --format=json > "$work_dir/raw/machine.json"
gcloud compute images describe "$boot_image_name" --project="$boot_image_project" --format=json > "$work_dir/raw/boot-image.json"
gcloud compute instances list --zones="$zone" --project="$project" --filter="name=('$instance')" --format=json > "$work_dir/raw/absence-instance.json"
gcloud compute disks list --zones="$zone" --project="$project" --filter="name=('$disk')" --format=json > "$work_dir/raw/absence-disk.json"
gcloud compute networks list --project="$project" --filter="name=('$network')" --format=json > "$work_dir/raw/absence-network.json"
gcloud compute networks subnets list --regions="$region" --project="$project" --filter="name=('$subnet') OR ipCidrRange=('$cidr')" --format=json > "$work_dir/raw/absence-subnet-or-cidr.json"
if gcloud storage ls --json "gs://$bucket/$prefix/**" --project="$project" > "$work_dir/raw/prefix.json" 2>/dev/null; then :; else printf '[]\n' > "$work_dir/raw/prefix.json"; fi
gcloud storage buckets describe "gs://$bucket" --project="$project" --format=json > "$work_dir/raw/bucket.json"

roundtrip="$work_dir/raw/roundtrip.txt"
printf 'ganesh-mini-gate3-%s\n' "$run_id" > "$roundtrip"
roundtrip_sha="$(shasum -a 256 "$roundtrip" | awk '{print $1}')"
roundtrip_uri="gs://$bucket/$prefix/preflight/roundtrip.txt"
gcloud storage cp "$roundtrip" "$roundtrip_uri" --project="$project"
gcloud storage cp "$roundtrip_uri" "$work_dir/raw/roundtrip.downloaded.txt" --project="$project"
[[ "$(shasum -a 256 "$work_dir/raw/roundtrip.downloaded.txt" | awk '{print $1}')" == "$roundtrip_sha" ]]
gcloud storage rm "$roundtrip_uri" --project="$project"

python3 - "$work_dir" "$project" "$region" "$zone" "$machine_type" "$boot_image_name" <<'PY'
import json,sys
root,project,region,zone,machine,boot=sys.argv[1:]
load=lambda name:json.load(open(root+'/raw/'+name))
if load('region.json').get('status')!='UP': raise SystemExit('region is not UP')
m=load('machine.json')
if m.get('name')!=machine or m.get('guestCpus')!=12 or m.get('memoryMb')!=49152: raise SystemExit('machine contract mismatch')
if load('boot-image.json').get('name')!=boot: raise SystemExit('boot image mismatch')
bucket=load('bucket.json')
if bucket.get('location')!='US-EAST1' or bucket.get('default_storage_class')!='STANDARD': raise SystemExit('bucket location or storage class mismatch')
if bucket.get('uniform_bucket_level_access') is not True or bucket.get('public_access_prevention')!='enforced' or bucket.get('versioning_enabled') is not True: raise SystemExit('bucket immutability/privacy controls are incomplete')
for name in ('absence-instance.json','absence-disk.json','absence-network.json','absence-subnet-or-cidr.json','prefix.json'):
 if load(name)!=[]: raise SystemExit('preflight absence failed: '+name)
region_data=load('region.json'); quotas={q['metric']:q for q in region_data.get('quotas',[])}
available=lambda metric: float(quotas.get(metric,{}).get('limit',0))-float(quotas.get(metric,{}).get('usage',0))
preempt_limits=[float(quotas.get(metric,{}).get('limit',0)) for metric in ('PREEMPTIBLE_NVIDIA_L4_GPUS','PREEMPTIBLE_CPUS')]
if any(limit>0 for limit in preempt_limits):
 required={'PREEMPTIBLE_NVIDIA_L4_GPUS':1,'PREEMPTIBLE_CPUS':12}; mode='preemptible'
else:
 required={'NVIDIA_L4_GPUS':1,'CPUS':12}; mode='standard-fallback'
for metric,needed in required.items():
 if available(metric)<needed: raise SystemExit('insufficient '+metric)
json.dump({'quota_mode':mode,'required':required,'available':{key:available(key) for key in required}},open(root+'/raw/quota-mode.json','w'),indent=2,sort_keys=True)
PY

input_prefix="gs://$bucket/$prefix/input"
upload_bind() {
  local key="$1" source="$2" object="$3"
  local destination="$input_prefix/$object"
  local metadata="$work_dir/input-metadata/$key.json"
  gcloud storage cp "$source" "$destination" --project="$project"
  gcloud storage objects describe "$destination" --project="$project" --format=json > "$metadata"
  python3 - "$source" "$metadata" "$destination" <<'PY'
import hashlib,json,os,sys
source,meta,dest=sys.argv[1:]; value=json.load(open(meta)); digest=hashlib.sha256()
with open(source,'rb') as handle:
 for chunk in iter(lambda:handle.read(8*1024*1024),b''): digest.update(chunk)
size=os.path.getsize(source); digest=digest.hexdigest()
if int(value['size'])!=size or not str(value.get('generation','')).isdigit(): raise SystemExit('uploaded object metadata mismatch')
print(json.dumps({'uri':dest+'#'+str(value['generation']),'sha256':digest,'size_bytes':size},sort_keys=True))
PY
}

upload_bind workspace_archive "$repo_root/artifacts/eval/workspaces/development-v2.tar.gz" development-v2.tar.gz > "$work_dir/input-metadata/workspace_archive.binding.json"
upload_bind workspace_manifest "$repo_root/measurement/gate3/development_workspace_v2.json" development-workspace-v2.json > "$work_dir/input-metadata/workspace_manifest.binding.json"
upload_bind training_workspace_archive "$repo_root/artifacts/train/workspaces/seed-pilot-v2.tar.gz" training-workspace-v2.tar.gz > "$work_dir/input-metadata/training_workspace_archive.binding.json"
upload_bind training_workspace_manifest "$repo_root/measurement/gate3/training_workspace_v2.json" training-workspace-manifest-v2.json > "$work_dir/input-metadata/training_workspace_manifest.binding.json"
upload_bind gate0_report "$repo_root/measurement/gate0/readiness.json" gate0-readiness.json > "$work_dir/input-metadata/gate0_report.binding.json"
upload_bind gate1_report "$repo_root/measurement/gate1/readiness.json" gate1-readiness.json > "$work_dir/input-metadata/gate1_report.binding.json"
upload_bind gate2_report "$repo_root/measurement/gate2/readiness.json" gate2-readiness.json > "$work_dir/input-metadata/gate2_report.binding.json"
upload_bind model_archive "$repo_root/artifacts/gcloud-inputs/gate3/model.tar.gz" model.tar.gz > "$work_dir/input-metadata/model_archive.binding.json"
upload_bind cuda_image_archive "$repo_root/artifacts/gcloud-inputs/gate3/cuda-image.docker.tar.zst" cuda-image.docker.tar.zst > "$work_dir/input-metadata/cuda_image_archive.binding.json"
upload_bind docker_bundle "$repo_root/artifacts/gcloud-inputs/gate3/docker-bundle.tar.gz" docker-bundle.tar.gz > "$work_dir/input-metadata/docker_bundle.binding.json"
upload_bind verifier_archive "$repo_root/artifacts/eval/verifier-images/amd64-v1/verifier-images-amd64-v1.tar" verifier-images-amd64-v1.tar > "$work_dir/input-metadata/verifier_archive.binding.json"
upload_bind verifier_manifest "$repo_root/measurement/gate1/verifier_image_bundle_amd64_v1.json" verifier-image-bundle.json > "$work_dir/input-metadata/verifier_manifest.binding.json"
upload_bind controller "$repo_root/scripts/inference/gcloud_startup_development_baseline.sh" gcloud-startup-development-baseline.sh > "$work_dir/input-metadata/controller.binding.json"
upload_bind metadata_wrapper "$repo_root/scripts/inference/gcloud_baseline_metadata_wrapper.sh" gcloud-baseline-metadata-wrapper.sh > "$work_dir/input-metadata/metadata_wrapper.binding.json"

python3 - "$repo_root" "$work_dir" "$run_id" "$project" "$region" "$zone" "$machine_type" "$bucket" "$prefix" "$boot_image" "$instance" "$disk" "$network" "$subnet" "$conservative_hourly_usd" "$support_reserve_usd" "$absolute_cost_ceiling_usd" <<'PY'
import hashlib,json,sys
root,out,run_id,project,region,zone,machine,bucket,prefix,boot,instance,disk,network,subnet,hourly,reserve,ceiling=sys.argv[1:]
load=lambda path:json.load(open(path))
prep=load(root+'/measurement/gate3/gcloud/preparation.json')
binding=lambda key:load(out+'/input-metadata/'+key+'.binding.json')
value={'schema_version':'ganesh-mini-gate3-gcloud-bindings/v2','status':'verified-generation-pinned','run_id':run_id,'preparation_sha256':prep['preparation_sha256'],
'preflight':{'project':project,'region':region,'zone':zone,'machine_type':machine,'gcs_bucket':bucket,'gcs_prefix':prefix,'boot_image':boot,'price_passed':True,'quota_passed':True,'machine_type_available':True,'exact_resources_absent':True,'bucket_round_trip_passed':True},
'cost':{'conservative_hourly_usd':hourly,'support_reserve_usd':reserve,'absolute_cost_ceiling_usd':ceiling},
'resources':{'instance':instance,'disk':disk,'network':network,'subnet':subnet},
'inputs':{'workspace_archive':binding('workspace_archive'),'workspace_manifest':binding('workspace_manifest'),'training_workspace_archive':binding('training_workspace_archive'),'training_workspace_manifest':binding('training_workspace_manifest'),'gate0_report':binding('gate0_report'),'gate1_report':binding('gate1_report'),'gate2_report':binding('gate2_report'),'verifier_archive':binding('verifier_archive'),'verifier_manifest':binding('verifier_manifest'),
'model_archive':binding('model_archive'),'cuda_image_archive':binding('cuda_image_archive'),'docker_bundle':binding('docker_bundle')},
'launch':{'controller':binding('controller'),'metadata_wrapper':binding('metadata_wrapper')}}
value['bindings_sha256']=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
json.dump(value,open(out+'/bindings.json','w'),indent=2,sort_keys=True)
PY

python3 "$repo_root/scripts/inference/build_gate1_gcloud_execution.py" --bindings "$work_dir/bindings.json" --approval-text-file "$approval_file" --source-commit "$source_commit" --output "$work_dir/execution-card.json"
upload_bind bindings "$work_dir/bindings.json" bindings.json > "$work_dir/input-metadata/bindings.binding.json"
upload_bind execution_card "$work_dir/execution-card.json" execution-card.json > "$work_dir/input-metadata/execution_card.binding.json"
cp "$price_file" "$work_dir/raw/price-evidence.json"
python3 - "$work_dir/preflight.json" "$work_dir" "$roundtrip_sha" <<'PY'
import hashlib,json,sys
out,root,roundtrip_sha=sys.argv[1:]
def sha(path):
 digest=hashlib.sha256()
 with open(path,'rb') as handle:
  for chunk in iter(lambda:handle.read(1024*1024),b''): digest.update(chunk)
 return digest.hexdigest()
files=['region.json','machine.json','boot-image.json','absence-instance.json','absence-disk.json','absence-network.json','absence-subnet-or-cidr.json','prefix.json','bucket.json','price-evidence.json','quota-mode.json']
value={'schema_version':'ganesh-mini-gate1-preflight/v1','status':'verified','roundtrip_sha256':roundtrip_sha,'files':{name:sha(root+'/raw/'+name) for name in files}}
value['evidence_sha256']=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
json.dump(value,open(out,'w'),indent=2,sort_keys=True)
PY
gcloud storage rsync "$work_dir/raw" "gs://$bucket/$prefix/preflight/raw" --recursive --project="$project"
gcloud storage cp "$work_dir/preflight.json" "gs://$bucket/$prefix/preflight/preflight.json" --project="$project"
python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
  --project "$project" --prefix "gs://$bucket/$prefix/preflight" \
  --output "$work_dir/preflight-backup-manifest.json" \
  --download-dir "$work_dir/preflight-download"
execution_card_uri="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["uri"])' "$work_dir/input-metadata/execution_card.binding.json")"
execution_card_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["sha256"])' "$work_dir/input-metadata/execution_card.binding.json")"
execution_card_size="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["size_bytes"])' "$work_dir/input-metadata/execution_card.binding.json")"
execution_card_internal="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["execution_sha256"])' "$work_dir/execution-card.json")"
controller_uri="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["uri"])' "$work_dir/input-metadata/controller.binding.json")"
wrapper_uri="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["uri"])' "$work_dir/input-metadata/metadata_wrapper.binding.json")"
controller_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["sha256"])' "$work_dir/input-metadata/controller.binding.json")"
wrapper_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["sha256"])' "$work_dir/input-metadata/metadata_wrapper.binding.json")"
controller_size="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["size_bytes"])' "$work_dir/input-metadata/controller.binding.json")"
wrapper_size="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["size_bytes"])' "$work_dir/input-metadata/metadata_wrapper.binding.json")"

python3 - "$work_dir/metadata.txt" "$work_dir/bindings.json" "$execution_card_uri" "$execution_card_sha" "$execution_card_size" "$execution_card_internal" "$controller_uri" "$controller_sha" "$controller_size" "$wrapper_uri" "$wrapper_sha" "$wrapper_size" "$project" "$bucket" "$prefix" "$run_id" "$machine_type" "$conservative_hourly_usd" "$support_reserve_usd" "$absolute_cost_ceiling_usd" <<'PY'
import json,sys,time
out,bindings_path,card_uri,card_sha,card_size,card_internal,controller_uri,controller_sha,controller_size,wrapper_uri,wrapper_sha,wrapper_size,project,bucket,prefix,run_id,machine,hourly,reserve,ceiling=sys.argv[1:]
b=json.load(open(bindings_path)); i=b['inputs']
rows={
'ganesh-gcp-project':project,'ganesh-gcs-bucket':bucket,'ganesh-gcs-prefix':prefix,'ganesh-attempt-id':run_id,'ganesh-expected-machine-type':machine,
'ganesh-gpu-hourly-usd':hourly,'ganesh-support-reserve-usd':reserve,'ganesh-absolute-cost-ceiling-usd':ceiling,
'ganesh-absolute-hard-deadline-epoch':str(int(time.time())+7200+14400+600),'ganesh-max-vm-lifetime-seconds':'14400','ganesh-controller-budget-seconds':'12600','ganesh-backup-reserve-seconds':'1800',
'ganesh-execution-card-uri':card_uri,'ganesh-execution-card-sha256':card_sha,'ganesh-execution-card-size':card_size,'ganesh-execution-card-internal-sha256':card_internal,
'ganesh-controller-uri':controller_uri,'ganesh-controller-sha256':controller_sha,'ganesh-controller-size':controller_size,
'ganesh-metadata-wrapper-uri':wrapper_uri,'ganesh-metadata-wrapper-sha256':wrapper_sha,'ganesh-metadata-wrapper-size':wrapper_size,
'ganesh-cuda-image-id':'sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860','ganesh-cuda-image-ref':'ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082'}
for key,prefix_name in [('workspace_archive','workspace-archive'),('workspace_manifest','workspace-manifest'),('training_workspace_archive','training-workspace-archive'),('training_workspace_manifest','training-workspace-manifest'),('gate0_report','gate0-report'),('gate1_report','gate1-report'),('gate2_report','gate2-report'),('model_archive','model-archive'),('cuda_image_archive','image-archive'),('docker_bundle','docker-bundle'),('verifier_archive','verifier-archive'),('verifier_manifest','verifier-manifest')]:
 row=i[key]; rows['ganesh-'+prefix_name+'-uri']=row['uri']; rows['ganesh-'+prefix_name+'-sha256']=row['sha256']; rows['ganesh-'+prefix_name+'-size']=str(row['size_bytes'])
open(out,'w').write(','.join(k+'='+str(v) for k,v in rows.items()))
PY

resource_stage=1
gcloud compute networks create "$network" --project="$project" --subnet-mode=custom
gcloud compute networks subnets create "$subnet" --project="$project" --region="$region" --network="$network" --range="$cidr" --enable-private-ip-google-access
project_number="$(gcloud projects describe "$project" --format='value(projectNumber)')"
gcloud compute instances create "$instance" --project="$project" --zone="$zone" --machine-type="$machine_type" \
  --image-project="$boot_image_project" --image="$boot_image_name" --boot-disk-size=200GB --boot-disk-type=pd-balanced --no-address \
  --network-interface="network=$network,subnet=$subnet,no-address" --service-account="$project_number-compute@developer.gserviceaccount.com" --scopes=cloud-platform \
  --provisioning-model=FLEX_START --request-valid-for-duration=2h --max-run-duration=4h --instance-termination-action=STOP --maintenance-policy=TERMINATE --reservation-affinity=none \
  --metadata="$(cat "$work_dir/metadata.txt")" --metadata-from-file="startup-script=$repo_root/scripts/inference/gcloud_baseline_metadata_wrapper.sh" \
  --format=json > "$work_dir/provider-instance-create.json" 2> "$work_dir/provider-instance-create.stderr.txt"

python3 - "$work_dir" "$source_commit" "$approval_text" <<'PY'
import hashlib,json,sys
root,commit,approval=sys.argv[1:]
def sha(path): return hashlib.sha256(open(path,'rb').read()).hexdigest()
card=json.load(open(root+'/execution-card.json')); bindings=json.load(open(root+'/bindings.json')); created=json.load(open(root+'/provider-instance-create.json'))
value={'schema_version':'ganesh-mini-gate1-launch-plan/v1','status':'submitted','source_commit':commit,'approval':approval,'execution_sha256':card['execution_sha256'],'bindings_sha256':bindings['bindings_sha256'],'provider_create_sha256':sha(root+'/provider-instance-create.json'),'provider_create':created}
value['evidence_sha256']=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
json.dump(value,open(root+'/launch-plan.json','w'),indent=2,sort_keys=True)
PY
gcloud storage cp "$work_dir/launch-plan.json" "$input_prefix/launch-plan.json" --project="$project"
printf 'Gate 3 Flex-start request submitted. Launch plan: %s\n' "$work_dir/launch-plan.json"
