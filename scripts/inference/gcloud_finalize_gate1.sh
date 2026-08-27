#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  echo "usage: $0 EXECUTION_CARD RUN_DIRECTORY" >&2
  exit 2
}
[[ $# -eq 2 ]] || usage
card="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
run_dir="$(mkdir -p "$2" && cd "$2" && pwd)"
repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
[[ -z "$(find "$run_dir" -mindepth 1 -print -quit)" ]] || { echo "run directory must be empty" >&2; exit 3; }

eval "$(python3 - "$card" <<'PY'
import hashlib, json, shlex, sys
card=json.load(open(sys.argv[1],encoding='utf-8'))
claimed=card.pop('execution_sha256',None)
actual=hashlib.sha256(json.dumps(card,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
if claimed != actual or card.get('schema_version') not in {'ganesh-mini-staged-gcloud-execution/v1','ganesh-mini-gate3-gcloud-execution/v2'} or card.get('status') != 'authorized-executable':
    raise SystemExit('invalid executable card')
execution=card['execution']; resources=execution['resources']
values={
    'project':execution['gcp_project'],'region':execution['region'],'zone':execution['zone'],
    'bucket':execution['gcs_bucket'],'prefix':execution['gcs_prefix'],'attempt':execution['attempt_id'],
    'instance':resources['instance'],'disk':resources['disk'],'network':resources['network'],'subnet':resources['subnet'],
    'card_seal':claimed,'source_commit':card['source_commit'],
}
for key,value in values.items(): print(f'{key}={shlex.quote(str(value))}')
PY
)"
[[ "$(git -C "$repo_root" rev-parse HEAD)" == "$source_commit" ]] || { echo "finalizer source commit does not match the executable card" >&2; exit 3; }

provider_dir="$run_dir/provider"
terminal_dir="$run_dir/terminal-download"
postdelete_dir="$run_dir/post-delete"
mkdir -p "$provider_dir" "$terminal_dir" "$postdelete_dir"
terminal_prefix="gs://$bucket/$prefix/runtime-terminal-$attempt"
wrapper_prefix="gs://$bucket/$prefix/wrapper-failure-$attempt"
postdelete_prefix="gs://$bucket/$prefix/post-delete"
launch_plan="$(dirname "$card")/launch-plan.json"

gcloud compute networks describe "$network" --project="$project" --format=json > "$provider_dir/network-before-delete.json"
gcloud compute networks subnets describe "$subnet" --region="$region" --project="$project" --format=json > "$provider_dir/subnet-before-delete.json"
network_id="$(python3 -c 'import json,sys; v=json.load(open(sys.argv[1])); assert v["name"]==sys.argv[2]; print(v["id"])' "$provider_dir/network-before-delete.json" "$network")"
subnet_id="$(python3 -c 'import json,sys; v=json.load(open(sys.argv[1])); assert v["name"]==sys.argv[2]; print(v["id"])' "$provider_dir/subnet-before-delete.json" "$subnet")"
gcloud compute operations list --zones="$zone" --project="$project" --filter="targetLink~'/instances/$instance$'" --format=json > "$provider_dir/operations.json"

instance_present=false
deleted_args=()
if gcloud compute instances describe "$instance" --zone="$zone" --project="$project" --format=json > "$provider_dir/resource-terminated.json" 2> "$provider_dir/resource-describe.error.log"; then
  instance_present=true
  rm -f "$provider_dir/resource-describe.error.log"
  gcloud compute disks describe "$disk" --zone="$zone" --project="$project" --format=json > "$provider_dir/disk-before-delete.json"
  python3 - "$provider_dir/resource-terminated.json" "$instance" <<'PY'
import json,sys
value=json.load(open(sys.argv[1]))
if value.get('name') != sys.argv[2] or value.get('status') != 'TERMINATED' or not str(value.get('id','')).isdigit():
    raise SystemExit('exact Gate 1 VM is not stopped with a stable provider ID')
PY
  resource_state="$provider_dir/resource-terminated.json"
  resource_relative="resource-terminated.json"
  resource_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "$resource_state")"
  disk_id="$(python3 -c 'import json,sys; v=json.load(open(sys.argv[1])); assert v["name"]==sys.argv[2]; print(v["id"])' "$provider_dir/disk-before-delete.json" "$disk")"
else
  rm -f "$provider_dir/resource-terminated.json"
  gcloud compute instances list --zones="$zone" --project="$project" --filter="name=('$instance')" --format=json > "$provider_dir/absence-instance.json"
  gcloud compute disks list --zones="$zone" --project="$project" --filter="name=('$disk')" --format=json > "$provider_dir/absence-disk.json"
  python3 - "$launch_plan" "$card" "$provider_dir/operations.json" "$provider_dir/absence-instance.json" "$provider_dir/absence-disk.json" "$provider_dir/resource-deleted.json" "$instance" <<'PY'
import hashlib,json,sys
launch_path,card_path,operations_path,instance_absence_path,disk_absence_path,out,expected_name=sys.argv[1:]
canonical=lambda value:hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
file_sha=lambda path:hashlib.sha256(open(path,'rb').read()).hexdigest()
launch=json.load(open(launch_path)); launch_seal=launch.pop('evidence_sha256',None)
if launch_seal != canonical(launch) or launch.get('schema_version') != 'ganesh-mini-gate1-launch-plan/v1': raise SystemExit('invalid launch plan seal')
card=json.load(open(card_path)); execution=card['execution']
if launch.get('execution_sha256') != card.get('execution_sha256') or launch.get('source_commit') != card.get('source_commit'): raise SystemExit('launch plan does not bind execution card')
created=launch.get('provider_create')
if not isinstance(created,list) or len(created)!=1 or file_sha(str(__import__('pathlib').Path(launch_path).with_name('provider-instance-create.json'))) != launch.get('provider_create_sha256'): raise SystemExit('launch provider identity is not exact')
resource=created[0]; resource_id=str(resource.get('id',''))
if resource.get('name') != expected_name or not resource_id.isdigit() or execution.get('instance_termination_action') != 'DELETE': raise SystemExit('launch identity or automatic deletion contract mismatch')
if json.load(open(instance_absence_path)) != [] or json.load(open(disk_absence_path)) != []: raise SystemExit('instance or auto-delete disk remains present')
operations=json.load(open(operations_path)); required={'compute.instances.guestTerminate','compute.instances.deferredDelete'}
observed={row.get('operationType') for row in operations if str(row.get('targetId'))==resource_id and str(row.get('targetLink','')).endswith('/instances/'+expected_name) and row.get('status')=='DONE'}
if not required <= observed: raise SystemExit('provider operations do not prove guest termination and automatic deletion')
value={'schema_version':'ganesh-mini-gcloud-deleted-instance/v1','name':expected_name,'id':resource_id,'status':'DELETED','instance_termination_action':'DELETE','launch_plan_sha256':launch_seal,'provider_create_sha256':launch['provider_create_sha256'],'operations_sha256':file_sha(operations_path),'instance_absence_sha256':file_sha(instance_absence_path),'disk_absence_sha256':file_sha(disk_absence_path)}
value['evidence_sha256']=canonical(value)
json.dump(value,open(out,'w'),indent=2,sort_keys=True)
PY
  resource_state="$provider_dir/resource-deleted.json"
  resource_relative="resource-deleted.json"
  resource_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "$resource_state")"
  disk_id=""
  deleted_args=(--instance-absence-evidence "$terminal_dir/provider/absence-instance.json" --disk-absence-evidence "$terminal_dir/provider/absence-disk.json")
fi

gcloud logging read "resource.type=\"gce_instance\" AND resource.labels.instance_id=\"$resource_id\"" --project="$project" --format=json --limit=1000 > "$provider_dir/system-events.json"
if [[ "$instance_present" == true ]] && gcloud compute instances get-serial-port-output "$instance" --zone="$zone" --project="$project" --port=1 > "$provider_dir/serial-port.log" 2> "$provider_dir/serial-port.error.log" && [[ -s "$provider_dir/serial-port.log" ]]; then
  rm -f "$provider_dir/serial-port.error.log"
  serial_option=(--serial-evidence "$terminal_dir/provider/serial-port.log")
else
  rm -f "$provider_dir/serial-port.log"
  if [[ -s "$provider_dir/serial-port.error.log" ]]; then
    mv "$provider_dir/serial-port.error.log" "$provider_dir/serial-port-unavailable.txt"
  else
    printf 'provider returned empty serial output\n' > "$provider_dir/serial-port-unavailable.txt"
    rm -f "$provider_dir/serial-port.error.log"
  fi
  serial_option=(--serial-unavailable-evidence "$terminal_dir/provider/serial-port-unavailable.txt")
fi

for path in "$resource_state" "$provider_dir"/operations.json "$provider_dir"/system-events.json; do
  [[ -s "$path" ]] || { echo "provider evidence is empty: $path" >&2; exit 3; }
done

# The metadata wrapper can fail before the controller creates its runtime
# directory. Recover only when the terminal prefix is completely empty and the
# independently verified wrapper prefix is the exact bounded failure envelope.
if ! gcloud storage ls "$terminal_prefix/runtime-files.sha256" --project="$project" >/dev/null 2>&1; then
  terminal_listing="$run_dir/terminal-prefix-before-recovery.json"
  gcloud storage ls --json "$terminal_prefix/**" --project="$project" > "$terminal_listing" 2>/dev/null || printf '[]\n' > "$terminal_listing"
  python3 - "$terminal_listing" <<'PY'
import json,sys
if json.load(open(sys.argv[1])):
    raise SystemExit('refusing to synthesize over a non-empty partial terminal prefix')
PY
  python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
    --project "$project" --prefix "$wrapper_prefix" \
    --output "$run_dir/wrapper-failure-backup-manifest.json" --download-dir "$run_dir/wrapper-failure-download"
  early_terminal="$run_dir/early-wrapper-terminal"
  python3 "$repo_root/scripts/inference/synthesize_gate1_wrapper_terminal.py" \
    --backup-manifest "$run_dir/wrapper-failure-backup-manifest.json" \
    --download-root "$run_dir/wrapper-failure-download" --execution-card "$card" \
    --output-dir "$early_terminal"
  gcloud storage rsync "$early_terminal" "$terminal_prefix" --recursive --project="$project"
elif ! gcloud storage ls "$terminal_prefix/execution-card.json" --project="$project" >/dev/null 2>&1; then
  python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
    --project "$project" --prefix "$terminal_prefix" \
    --output "$run_dir/partial-terminal-backup-manifest.json" --download-dir "$run_dir/partial-terminal-download"
  python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
    --project "$project" --prefix "$wrapper_prefix" \
    --output "$run_dir/wrapper-failure-backup-manifest.json" --download-dir "$run_dir/wrapper-failure-download"
  recovered_terminal="$run_dir/recovered-partial-terminal"
  python3 "$repo_root/scripts/inference/synthesize_gate1_wrapper_terminal.py" \
    --backup-manifest "$run_dir/wrapper-failure-backup-manifest.json" \
    --download-root "$run_dir/wrapper-failure-download" --execution-card "$card" \
    --partial-backup-manifest "$run_dir/partial-terminal-backup-manifest.json" \
    --partial-download-root "$run_dir/partial-terminal-download" --output-dir "$recovered_terminal"
  gcloud storage rsync "$recovered_terminal" "$terminal_prefix" --recursive --project="$project"
fi

if [[ -f "$provider_dir/serial-port.log" ]]; then serial_source="$provider_dir/serial-port.log"; else serial_source="$provider_dir/serial-port-unavailable.txt"; fi
provider_uploads=("$resource_state" "$provider_dir/operations.json" "$provider_dir/system-events.json" "$serial_source")
if [[ "$instance_present" == false ]]; then provider_uploads+=("$provider_dir/absence-instance.json" "$provider_dir/absence-disk.json"); fi
for path in "${provider_uploads[@]}"; do
  gcloud storage cp "$path" "$terminal_prefix/provider/$(basename "$path")" --project="$project"
done

python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
  --project "$project" --prefix "$terminal_prefix" \
  --output "$run_dir/terminal-backup-manifest.json" --download-dir "$terminal_dir"
cmp "$card" "$terminal_dir/execution-card.json"
set +e
python3 "$repo_root/scripts/inference/verify_gate1_terminal.py" \
  --backup-manifest "$run_dir/terminal-backup-manifest.json" \
  --download-root "$terminal_dir" --execution-card "$card" \
  --expected-prefix "$terminal_prefix" --output "$run_dir/terminal-validation.json" \
  > "$run_dir/terminal-validation.stdout.log" 2> "$run_dir/terminal-validation.stderr.log"
terminal_status="$?"
set -e
if [[ "$terminal_status" != 0 && "$terminal_status" != 2 ]]; then
  python3 - "$run_dir/terminal-validation.json" "$card" "$run_dir/terminal-backup-manifest.json" "$run_dir/terminal-validation.stderr.log" "$terminal_prefix" "$attempt" <<'PY'
import hashlib,json,sys
out,card_path,manifest_path,error_path,prefix,attempt=sys.argv[1:]
sha=lambda path:hashlib.sha256(open(path,'rb').read()).hexdigest()
card=json.load(open(card_path)); manifest=json.load(open(manifest_path))
value={'schema_version':'ganesh-mini-gate1-terminal-validation/v1','status':'integrity-failure','attempt_id':attempt,'expected_prefix':prefix,'execution_sha256':card.get('execution_sha256'),'backup_manifest_sha256':manifest.get('evidence_sha256'),'validation_error_sha256':sha(error_path),'run':None,'deletion_eligible':'quarantine-only'}
value['evidence_sha256']=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
json.dump(value,open(out,'w'),indent=2,sort_keys=True)
PY
fi
if [[ "$terminal_status" == 2 ]]; then
  if [[ ! -f "$run_dir/wrapper-failure-backup-manifest.json" ]]; then
    python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
      --project "$project" --prefix "$wrapper_prefix" \
      --output "$run_dir/wrapper-failure-backup-manifest.json" --download-dir "$run_dir/wrapper-failure-download"
  fi
fi

deletion_args=(
  --phase gate1-baseline --backup-manifest "$run_dir/terminal-backup-manifest.json"
  --resource-state "$terminal_dir/provider/$resource_relative"
  --inventory "$terminal_dir/runtime-files.sha256" "${serial_option[@]}"
  --operations-evidence "$terminal_dir/provider/operations.json"
  --system-events-evidence "$terminal_dir/provider/system-events.json"
  --expected-resource-name "$instance" --expected-resource-id "$resource_id"
  --expected-prefix "$terminal_prefix" --output "$run_dir/deletion-gate.json" "${deleted_args[@]}"
)
set +e
python3 "$repo_root/scripts/cuda/verify_deletion_gate.py" "${deletion_args[@]}" \
  > "$run_dir/deletion-gate.stdout.log" 2> "$run_dir/deletion-gate.stderr.log"
deletion_status="$?"
set -e
if [[ "$deletion_status" != 0 ]]; then
  python3 "$repo_root/scripts/cuda/verify_deletion_gate.py" "${deletion_args[@]}" --integrity-mode quarantine
fi

if [[ "$instance_present" == true ]]; then gcloud compute instances delete "$instance" --zone="$zone" --project="$project" --quiet; fi
gcloud compute networks subnets delete "$subnet" --region="$region" --project="$project" --quiet
gcloud compute networks delete "$network" --project="$project" --quiet

gcloud compute instances list --zones="$zone" --project="$project" --filter="name=('$instance')" --format=json > "$postdelete_dir/absence-instance.json"
gcloud compute disks list --zones="$zone" --project="$project" --filter="name=('$disk')" --format=json > "$postdelete_dir/absence-disk.json"
gcloud compute networks subnets list --regions="$region" --project="$project" --filter="name=('$subnet')" --format=json > "$postdelete_dir/absence-subnet.json"
gcloud compute networks list --project="$project" --filter="name=('$network')" --format=json > "$postdelete_dir/absence-network.json"

cp "$provider_dir/network-before-delete.json" "$provider_dir/subnet-before-delete.json" "$postdelete_dir/"
if [[ -f "$provider_dir/disk-before-delete.json" ]]; then cp "$provider_dir/disk-before-delete.json" "$postdelete_dir/"; fi
python3 - "$postdelete_dir/absence-scope.json" "$project" "$region" "$zone" "$attempt" "$instance" "$resource_id" "$disk" "$disk_id" "$network" "$network_id" "$subnet" "$subnet_id" "$postdelete_dir" <<'PY'
import json,sys
out,project,region,zone,run_id,instance,instance_id,disk,disk_id,network,network_id,subnet,subnet_id,root=sys.argv[1:]
resources=[
 {'kind':'instance','name':instance,'id':instance_id},
 {'kind':'disk','name':disk,'id':disk_id},
 {'kind':'network','name':network,'id':network_id},
 {'kind':'subnet','name':subnet,'id':subnet_id},
]
queries=[
 {'kind':'instance','path':root+'/absence-instance.json','command':['gcloud','compute','instances','list','--zones='+zone,'--project='+project,"--filter=name=('"+instance+"')",'--format=json']},
 {'kind':'disk','path':root+'/absence-disk.json','command':['gcloud','compute','disks','list','--zones='+zone,'--project='+project,"--filter=name=('"+disk+"')",'--format=json']},
 {'kind':'network','path':root+'/absence-network.json','command':['gcloud','compute','networks','list','--project='+project,"--filter=name=('"+network+"')",'--format=json']},
 {'kind':'subnet','path':root+'/absence-subnet.json','command':['gcloud','compute','networks','subnets','list','--regions='+region,'--project='+project,"--filter=name=('"+subnet+"')",'--format=json']},
]
json.dump({'schema_version':'ganesh-mini-gcloud-absence-scope/v1','project':project,'region':region,'zone':zone,'run_id':run_id,'expected_resources':resources,'queries':queries},open(out,'w'),indent=2,sort_keys=True)
PY
python3 "$repo_root/scripts/cuda/verify_absence_proof.py" --scope "$postdelete_dir/absence-scope.json" --output "$postdelete_dir/absence-proof.json"
cp "$run_dir/terminal-backup-manifest.json" "$run_dir/terminal-validation.json" "$run_dir/deletion-gate.json" "$postdelete_dir/"
if [[ -f "$run_dir/wrapper-failure-backup-manifest.json" ]]; then cp "$run_dir/wrapper-failure-backup-manifest.json" "$postdelete_dir/"; fi
if [[ -f "$run_dir/partial-terminal-backup-manifest.json" ]]; then cp "$run_dir/partial-terminal-backup-manifest.json" "$postdelete_dir/"; fi
gcloud storage rsync "$postdelete_dir" "$postdelete_prefix" --recursive --project="$project"
python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
  --project "$project" --prefix "$postdelete_prefix" \
  --output "$run_dir/post-delete-backup-manifest.json" --download-dir "$run_dir/post-delete-download"

python3 - "$run_dir/finalization.json" "$card_seal" "$run_dir/terminal-backup-manifest.json" "$run_dir/terminal-validation.json" "$run_dir/deletion-gate.json" "$postdelete_dir/absence-proof.json" "$run_dir/post-delete-backup-manifest.json" <<'PY'
import hashlib,json,sys
out,card,*paths=sys.argv[1:]
def sealed(path,field):
 value=json.load(open(path)); claimed=value.pop(field,None)
 actual=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 if claimed != actual: raise SystemExit('invalid finalization input seal: '+path)
 return claimed
fields=['evidence_sha256']*5
deletion=json.load(open(paths[2])); integrity=deletion.get('integrity_mode','strict')
value={'schema_version':'ganesh-mini-gate1-gcloud-finalization/v1','status':'complete' if integrity=='strict' else 'complete-quarantined','integrity_mode':integrity,'execution_sha256':card,'terminal_backup_sha256':sealed(paths[0],fields[0]),'terminal_validation_sha256':sealed(paths[1],fields[1]),'deletion_gate_sha256':sealed(paths[2],fields[2]),'absence_proof_sha256':sealed(paths[3],fields[3]),'post_delete_backup_sha256':sealed(paths[4],fields[4])}
value['evidence_sha256']=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
json.dump(value,open(out,'w'),indent=2,sort_keys=True)
PY
gcloud storage cp "$run_dir/finalization.json" "$postdelete_prefix/finalization.json" --project="$project"
python3 "$repo_root/scripts/cuda/gcloud_backup_manifest.py" \
  --project "$project" --prefix "$postdelete_prefix" \
  --output "$run_dir/post-delete-final-backup-manifest.json" --download-dir "$run_dir/post-delete-final-download"
baseline_admissible="$(python3 -c 'import json,sys; validation=json.load(open(sys.argv[1])); finalization=json.load(open(sys.argv[2])); deletion=json.load(open(sys.argv[3])); print("yes" if validation.get("run") and finalization.get("status")=="complete" and deletion.get("admission_eligible",True) is True else "no")' "$run_dir/terminal-validation.json" "$run_dir/finalization.json" "$run_dir/deletion-gate.json")"
if [[ "$baseline_admissible" == yes ]]; then
  canonical_baseline="$repo_root/measurement/inference/development/qwen3.5-2b-base-v1"
  if [[ -d "$canonical_baseline" ]]; then
    printf 'Canonical Gate 1 baseline already exists; preserving it and retaining this run as revalidation evidence.\n'
  else
    python3 "$repo_root/scripts/inference/admit_gate1_baseline.py" --finalization-dir "$run_dir"
  fi
else
  printf 'Campaign produced no validated Gate 1 baseline; canonical baseline admission was correctly skipped.\n'
fi
printf 'Gate 1 finalization complete: %s (final backup: %s)\n' "$run_dir/finalization.json" "$run_dir/post-delete-final-backup-manifest.json"
