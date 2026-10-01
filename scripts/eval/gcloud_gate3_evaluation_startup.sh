#!/usr/bin/env bash
# One bounded, evaluation-only Gate 3 stage. Never opens decision tasks.
set -Eeuo pipefail
meta=http://metadata.google.internal/computeMetadata/v1
getmeta() { curl -fsS --retry 3 -H 'Metadata-Flavor: Google' "$meta/$1"; }
project=$(getmeta instance/attributes/ganesh-project)
prefix=$(getmeta instance/attributes/ganesh-prefix)
card_uri=$(getmeta instance/attributes/ganesh-card-uri)
card_sha=$(getmeta instance/attributes/ganesh-card-sha)
work=/opt/ganesh-g3-eval
evidence=/var/lib/ganesh-g3-eval
mkdir -p "$work" "$evidence/output"
started=$(date +%s)
deadline=$((started+6000))
left() { local seconds=$((deadline-$(date +%s))); ((seconds>0)); printf '%s\n' "$seconds"; }
( sleep 7190; shutdown -h now ) & watchdog=$!
exec 3>&1 4>&2
exec > >(tee -a "$evidence/startup.stdout.log" >&3); outtee=$!
exec 2> >(tee -a "$evidence/startup.stderr.log" >&4); errtee=$!
checkpoint() {
  timeout 90 gcloud storage rsync "$evidence" "$prefix/checkpoints" --recursive \
    --project="$project" >> /var/log/ganesh-g3-eval-backup.log 2>&1 || true
}
finish() {
  local status=$?
  trap - EXIT
  kill "${checkpoint_pid:-}" 2>/dev/null || true
  wait "${checkpoint_pid:-}" 2>/dev/null || true
  docker ps -q --filter label=ganesh.gate3.eval | xargs -r docker stop -t 10 >/dev/null 2>&1 || true
  cp /var/log/ganesh-g3-eval-backup.log "$evidence/checkpoint-backup.log" 2>/dev/null || true
  exec 1>&3 2>&4
  wait "$outtee" "$errtee" || status=92
  printf '%s\n' "$status" > "$evidence/startup-exit-code.txt"
  (cd "$evidence" && find . -type f ! -name runtime-files.sha256 -print0 | sort -z | \
    xargs -0 sha256sum > runtime-files.sha256) || status=91
  timeout 900 gcloud storage rsync "$evidence" "$prefix/terminal" --recursive \
    --project="$project" || status=90
  kill "$watchdog" 2>/dev/null || true
  ( sleep 2; shutdown -h now ) >/dev/null 2>&1 &
  exit "$status"
}
trap finish EXIT

[[ "$project" == executespecv1 ]]
[[ "$(basename "$(getmeta instance/machine-type)")" == g2-standard-8 ]]
timeout 120 gcloud storage cp "$card_uri" "$work/card.json" --project="$project"
printf '%s  %s\n' "$card_sha" "$work/card.json" | sha256sum -c -
cp "$work/card.json" "$evidence/execution-card.json"
python3 - "$work/card.json" "$work/inputs.tsv" "$prefix" <<'PY'
import hashlib,json,sys
card=json.load(open(sys.argv[1])); claim=card.pop('execution_sha256')
digest=hashlib.sha256(json.dumps(card,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
assert claim==digest
assert card['schema_version']=='ganesh-mini-gate3-gcloud-evaluation/v2'
assert card['plan_sha256']=='d4659d3b503d4eb0a0a38d5af6129f668ccef7994a7f678e920ced1a5e55dd09'
assert card['project']=='executespecv1' and card['prefix']==sys.argv[3]
assert card['maximum_vm_seconds']==7200 and card['absolute_incremental_ceiling_usd']=='15'
assert card['decision_tasks_opened']==0 and card['phase'] in ('canary','development')
assert card['evaluation_workspace_manifest_sha256']=='8ed2f45d87b3b867a59c6eca03be6e9d991bd1070037bd52311ed63a07585edc'
assert card['canary_manifest_sha256']=='0b7483141ba64ba223bc976ed7711ad847bc1056888be0e7bd9d261b85cffa44'
assert card['cuda_image_id']=='sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860'
assert card['inputs']['cuda_host_floor']['sha256']=='b45bfdbff03e37d7c2ffb2b6f82b8077a8e19e1408ffb13bef623cf2a3197f68'
assert card['inputs']['model_preflight_module']['sha256']=='163582e1087362a1cda943937e65ffb804227810e2f49358926a02706b1d78ff'
if card['phase']=='development':
 assert card['selected_learning_rate'] in ('1e-5','3e-5') and card['selection_report_sha256']
else:
 assert card['selected_learning_rate'] is None and card['selection_report_sha256'] is None
with open(sys.argv[2],'x') as handle:
 for name,row in card['inputs'].items():
  assert row['uri'].startswith('gs://') and row['uri'].rsplit('#',1)[-1].isdigit()
  assert len(row['sha256'])==64 and row['size_bytes']>0
  handle.write('\t'.join((name,row['uri'],row['sha256'],str(row['size_bytes'])))+'\n')
PY
nvidia-smi -q > "$evidence/nvidia-smi.txt"
( while true; do checkpoint; sleep 120; done ) & checkpoint_pid=$!
while IFS=$'\t' read -r name uri sha size; do
  timeout "$(left)" gcloud storage cp "$uri" "$work/$name" --project="$project"
  [[ "$(stat -c %s "$work/$name")" == "$size" ]]
  printf '%s  %s\n' "$sha" "$work/$name" | sha256sum -c -
done < "$work/inputs.tsv"
mkdir "$work/workspace" "$work/model" "$work/candidates" "$work/bundle" "$work/configs" "$work/shared-tmp"
tar -xzf "$work/evaluation_workspace" -C "$work/workspace"
tar -xzf "$work/candidate_inputs" -C "$work/candidates"
python3 - "$work" <<'PY'
import hashlib,json,os,sys
from pathlib import Path
w=Path(sys.argv[1]); card=json.load(open(w/'card.json'))
staging=json.load(open(w/'staging_card'))
claim=staging.pop('card_sha256')
assert hashlib.sha256(json.dumps(staging,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()==claim==card['staging_card_sha256']
manifest=json.load(open(w/'evaluation_manifest')); seal=manifest.pop('manifest_sha256')
assert hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()==seal==card['evaluation_workspace_manifest_sha256']
expected={row['path']:row['sha256'] for row in manifest['files']}
observed={str(p.relative_to(w/'workspace')) for p in (w/'workspace').rglob('*') if p.is_file()}
assert observed==set(expected) and not any('decision' in Path(name).parts for name in observed)
for name,digest in expected.items():
 p=w/'workspace'/name
 assert not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==digest
expected_bundle={row['path']:row['sha256'] for row in staging['candidate_input_bundle']['files']}
observed_bundle={str(p.relative_to(w/'candidates')) for p in (w/'candidates').rglob('*') if p.is_file()}
assert observed_bundle==set(expected_bundle)
for name,digest in expected_bundle.items():
 p=w/'candidates'/name
 assert not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==digest
for name,row in staging['configs'].items():
 if name in card['inputs']:
  assert hashlib.sha256((w/name).read_bytes()).hexdigest()==row['sha256']
PY
# The Docker daemon cannot create a nested bind target under a read-only
# workspace mount. The original 587-file workspace and the candidate bundle
# were independently verified above; combine only these two evaluation inputs
# before mounting the resulting tree read-only in the inference container.
cp -a "$work/candidates/candidate-inputs" "$work/workspace/candidate-inputs"
python3 - "$work" "$evidence/overlay-inventory.json" <<'PY'
import hashlib,json,sys
from pathlib import Path
w=Path(sys.argv[1]); staging=json.load(open(w/'staging_card'))
expected={row['path']:row['sha256'] for row in staging['candidate_input_bundle']['files']}
overlaid={str(p.relative_to(w/'workspace')):p for p in (w/'workspace'/'candidate-inputs').rglob('*') if p.is_file()}
assert set(overlaid)==set(expected)
assert all(not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==expected[name] for name,p in overlaid.items())
assert all(name.startswith('candidate-inputs/') and '/decision/' not in name and '/train/' not in name for name in overlaid)
record={'schema_version':'ganesh-mini-evaluation-overlay/v1','status':'verified','original_workspace_manifest_sha256':staging['evaluation_workspace_manifest_sha256'],'files':expected}
record['evidence_sha256']=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
Path(sys.argv[2]).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
PY
# The pinned materializer imports this one stdlib-only preflight module. Keep
# the sealed 587-file evaluation archive unchanged; add the independently
# downloaded and hashed dependency only to this ephemeral evaluation tree.
python3 - "$work" "$evidence/model-preflight-overlay.json" <<'PY'
import hashlib,json,shutil,sys
from pathlib import Path
w=Path(sys.argv[1]); card=json.load(open(w/'card.json'))
source=w/'model_preflight_module'
target=w/'workspace/scripts/train/preflight_gate3_capability_pilot.py'
expected='163582e1087362a1cda943937e65ffb804227810e2f49358926a02706b1d78ff'
assert card['inputs']['model_preflight_module']['sha256']==expected
assert source.is_file() and not source.is_symlink()
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
assert not target.exists() and not target.parent.exists()
target.parent.mkdir()
shutil.copyfile(source,target)
assert hashlib.sha256(target.read_bytes()).hexdigest()==expected
record={'schema_version':'ganesh-mini-model-preflight-overlay/v1','status':'verified',
        'original_workspace_manifest_sha256':card['evaluation_workspace_manifest_sha256'],
        'path':'scripts/train/preflight_gate3_capability_pilot.py','sha256':expected}
record['evidence_sha256']=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
Path(sys.argv[2]).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
PY
archive_sha=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["inputs"]["model_archive"]["sha256"])' "$work/card.json")
timeout "$(left)" env PYTHONPATH="$work/workspace" python3 -B "$work/model_materializer" \
  --archive "$work/model_archive" \
  --inventory "$work/workspace/configs/model/qwen3_5_2b.inventory.json" \
  --archive-sha256 "$archive_sha" --materialize-dir "$work/model" \
  --output "$evidence/model-canonical-materialization.json"
tar -xzf "$work/docker_bundle" -C "$work/bundle" --strip-components=1
(cd "$work/bundle" && sha256sum -c bundle-files.sha256)
export DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a
timeout 300 dpkg --force-confold -i "$work"/bundle/debs/*.deb > "$evidence/docker-install.log" 2>&1 || \
  timeout 300 dpkg --force-confold -i "$work"/bundle/debs/*.deb >> "$evidence/docker-install.log" 2>&1
nvidia-ctk runtime configure --runtime=docker
systemctl restart docker
timeout 30 bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done'
timeout "$(left)" bash -c 'set -o pipefail; zstd -dc "$1" | docker load' _ "$work/cuda_image_archive"
image=ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082
[[ "$(docker image inspect --format '{{.Id}}' "$image")" == sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860 ]]
timeout 120 docker run --pull=never --rm --name ganesh-g3-eval-hardware \
  --entrypoint python3 --gpus device=0 --network none --cpus 2 --memory 8g \
  --pids-limit 512 --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=256m \
  --mount "type=bind,src=$work/cuda_host_floor,dst=/preflight/cuda_host_floor.py,readonly" \
  --mount "type=bind,src=$evidence/output,dst=/output" \
  --env PYTHONPATH=/preflight "$image" -B -c \
  'import torch; from pathlib import Path; from cuda_host_floor import assess_cuda_host; report=assess_cuda_host(torch,Path("/output/evaluation-gpu-hardware-preflight.json")); assert report["gpu_name"]=="NVIDIA L4"'
timeout "$(left)" docker load --input "$work/verifier_images" > "$evidence/verifier-image-load.log"
PYTHONPATH="$work/workspace" python3 -B "$work/workspace/scripts/eval/verify_runtime_images.py" \
  --config "$work/workspace/configs/eval/runtimes.json" \
  --output "$evidence/verifier-runtime-readiness.json"
docker_bin=$(command -v docker)
phase=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["phase"])' "$work/card.json")
if [[ "$phase" == canary ]]; then configs=(canary-1e-5.json canary-3e-5.json)
else selected=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["selected_learning_rate"])' "$work/card.json"); configs=("development-$selected.json")
fi
for config in "${configs[@]}"; do
  cp "$work/$config" "$work/configs/$config"
  label=${config%.json}
  mkdir "$evidence/output/$label"
  lr=${label##*-}; lr=${label#${phase}-}
  timeout "$(left)" docker run --pull=never --rm --name "ganesh-g3-eval-$label" \
    --label ganesh.gate3.eval=1 --entrypoint python3 \
    --gpus device=0 --network none --cpus 8 --memory 30g --pids-limit 4096 \
    --read-only --cap-drop ALL --security-opt no-new-privileges \
    --tmpfs /tmp:rw,noexec,nosuid,nodev,size=8g \
    --tmpfs /var/cache/triton:rw,exec,nosuid,nodev,size=1g \
    --mount "type=bind,src=$work/workspace,dst=/workspace,readonly" \
    --mount "type=bind,src=$work/model,dst=/model,readonly" \
    --mount "type=bind,src=$work/configs,dst=/control,readonly" \
    --mount "type=bind,src=$evidence/output/$label,dst=/output" \
    --mount "type=bind,src=$work/shared-tmp,dst=$work/shared-tmp" \
    --mount "type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock" \
    --mount "type=bind,src=$docker_bin,dst=/usr/local/bin/docker,readonly" \
    --env "TMPDIR=$work/shared-tmp" --env HF_HUB_OFFLINE=1 --env TRANSFORMERS_OFFLINE=1 \
    --env PYTHONPATH=/workspace --env TRITON_CACHE_DIR=/var/cache/triton \
    --workdir /workspace "$image" -B scripts/inference/run_evaluation.py \
    --config "/control/$config" --model-dir /model \
    --adapter-dir "/workspace/candidate-inputs/$lr/adapter-final" --output-dir /output
  python3 - "$evidence/output/$label/run.json" "$phase" <<'PY'
import hashlib,json,sys
value=json.load(open(sys.argv[1])); claimed=value.pop('run_sha256')
digest=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
assert claimed==digest and value['classification']=='private_candidate_development'
assert value['schema_version']=='ganesh-mini-inference-run/v2'
expected=30 if sys.argv[2]=='canary' else 180
counts=value['task_accounting']
assert counts['expected']==counts['completed']==expected and counts['pending']==0
assert counts['passed']+counts['failed']==expected
PY
done
