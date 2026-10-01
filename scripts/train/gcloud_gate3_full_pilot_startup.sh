#!/usr/bin/env bash
# One full-epoch Gate 3 LR candidate; terminal evidence is backed before STOP.
set -Eeuo pipefail
meta=http://metadata.google.internal/computeMetadata/v1
getmeta() { curl -fsS --retry 3 -H 'Metadata-Flavor: Google' "$meta/$1"; }
project=$(getmeta instance/attributes/ganesh-project)
prefix=$(getmeta instance/attributes/ganesh-prefix)
card_uri=$(getmeta instance/attributes/ganesh-card-uri)
card_sha=$(getmeta instance/attributes/ganesh-card-sha)
work=/opt/ganesh-g3-pilot
evidence=/var/lib/ganesh-g3-pilot
mkdir -p "$work" "$evidence/output/probe" "$evidence/output/training"
started=$(date +%s)
deadline=$((started+6000))
left() { local seconds=$((deadline-$(date +%s))); ((seconds>0)); printf '%s\n' "$seconds"; }
( sleep 7190; shutdown -h now ) & watchdog=$!
exec 3>&1 4>&2
exec > >(tee -a "$evidence/startup.stdout.log" >&3); outtee=$!
exec 2> >(tee -a "$evidence/startup.stderr.log" >&4); errtee=$!
checkpoint() {
  timeout 90 gcloud storage rsync "$evidence" "$prefix/checkpoints" --recursive \
    --project="$project" >> /var/log/ganesh-g3-pilot-backup.log 2>&1 || true
}
finish() {
  local status=$?
  trap - EXIT
  kill "${checkpoint_pid:-}" 2>/dev/null || true
  wait "${checkpoint_pid:-}" 2>/dev/null || true
  docker stop -t 10 ganesh-g3-pilot-training >/dev/null 2>&1 || true
  docker stop -t 10 ganesh-g3-pilot-probe >/dev/null 2>&1 || true
  docker stop -t 10 ganesh-g3-pilot-card >/dev/null 2>&1 || true
  printf '%s\n' "$status" > "$evidence/startup-exit-code.txt"
  cp /var/log/ganesh-g3-pilot-backup.log "$evidence/checkpoint-backup.log" 2>/dev/null || true
  exec 1>&3 2>&4
  wait "$outtee" "$errtee" || status=92
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
timeout 120 gcloud storage cp "$card_uri" "$work/card.json" --project="$project"
printf '%s  %s\n' "$card_sha" "$work/card.json" | sha256sum -c -
cp "$work/card.json" "$evidence/execution-card.json"
python3 - "$work/card.json" "$work/inputs.tsv" "$prefix" <<'PY'
import hashlib,json,sys
card=json.load(open(sys.argv[1])); claim=card.pop('execution_sha256')
seal=hashlib.sha256(json.dumps(card,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
assert claim==seal
assert card['schema_version']=='ganesh-mini-gate3-gcloud-full-pilot/v1'
assert card['project']=='executespecv1'
assert card['plan_sha256']=='d4659d3b503d4eb0a0a38d5af6129f668ccef7994a7f678e920ced1a5e55dd09'
assert card['absolute_incremental_ceiling_usd']=='15'
assert card['maximum_vm_seconds']==7200 and card['probe_rows']==16
assert card['training_rows']==900 and card['training_input_tokens']==651639
assert card['decision_tasks_opened']==0
assert card['learning_rate'] in ('1e-5','3e-5')
assert card['prefix']==sys.argv[3]
assert card['inputs']['workspace_archive']['sha256']=='a9eee2d31de0cf3728d10c8ee5652615006df83dbb371cf942a4e4ee79a036d8'
with open(sys.argv[2],'x') as handle:
 for name,row in card['inputs'].items():
  assert row['uri'].startswith('gs://') and row['uri'].rsplit('#',1)[-1].isdigit()
  handle.write('\t'.join((name,row['uri'],row['sha256'],str(row['size_bytes'])))+'\n')
PY
observed_machine=$(basename "$(getmeta instance/machine-type)")
[[ "$observed_machine" == g2-standard-8 ]]
instance_id=$(getmeta instance/id)
instance_name=$(getmeta instance/name)
zone=$(basename "$(getmeta instance/zone)")
printf '%s\n' "$instance_id" > "$evidence/instance-id.txt"
nvidia-smi -q > "$evidence/nvidia-smi.txt"
( while true; do checkpoint; sleep 120; done ) & checkpoint_pid=$!
while IFS=$'\t' read -r name uri sha size; do
  timeout "$(left)" gcloud storage cp "$uri" "$work/$name" --project="$project"
  [[ "$(stat -c %s "$work/$name")" == "$size" ]]
  printf '%s  %s\n' "$sha" "$work/$name" | sha256sum -c -
done < "$work/inputs.tsv"
mkdir "$work/workspace" "$work/model" "$work/bundle"
tar -xzf "$work/workspace_archive" -C "$work/workspace"
[[ ! -d "$work/workspace/data/eval" && ! -d "$work/workspace/scripts/eval" ]]
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

probe_seconds=$(left)
((probe_seconds<=1800)) || probe_seconds=1800
timeout "$probe_seconds" docker run --pull=never --rm --name ganesh-g3-pilot-probe --entrypoint python3 \
  --gpus device=0 --network none --cpus 8 --memory 30g --pids-limit 4096 \
  --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=8g \
  --tmpfs /var/cache/triton:rw,exec,nosuid,nodev,size=1g \
  --mount "type=bind,src=$work/workspace,dst=/workspace,readonly" \
  --mount "type=bind,src=$work/model,dst=/model,readonly" \
  --mount "type=bind,src=$evidence/output,dst=/output" \
  --env HF_HUB_OFFLINE=1 --env TRANSFORMERS_OFFLINE=1 \
  --env PYTHONPATH=/workspace --env TRITON_CACHE_DIR=/var/cache/triton \
  --workdir /workspace "$image" -B \
  scripts/train/measure_gate3_capability_throughput.py \
  --model-dir /model --instance-id "$instance_id" \
  --output /output/probe/throughput.json \
  --hourly-cost-usd 0.881021512 --absolute-incremental-ceiling-usd 15

mkdir -p "$work/workspace/runtime-evidence"
cp "$evidence/output/probe/throughput.json" "$work/workspace/runtime-evidence/throughput.json"
roundtrip_uri="$prefix/preflight/card-roundtrip.json"
timeout 120 gcloud storage cp "$work/card.json" "$roundtrip_uri" \
  --if-generation-match=0 --project="$project"
generation=$(gcloud storage objects describe "$roundtrip_uri" --format='value(generation)' --project="$project")
timeout 120 gcloud storage cp "$roundtrip_uri#$generation" "$work/roundtrip-card.json" --project="$project"
candidate_lr=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["learning_rate"])' "$work/card.json")
prior_cost=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["prior_cost_usd"])' "$work/card.json")
candidate_ceiling=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["candidate_cost_ceiling_usd"])' "$work/card.json")
PYTHONPATH="$work/workspace" python3 -B \
  "$work/workspace/scripts/train/build_gate3_gcloud_provider_evidence.py" \
  --root "$work/workspace" \
  --throughput "$work/workspace/runtime-evidence/throughput.json" \
  --roundtrip-source "$work/card.json" --roundtrip-copy "$work/roundtrip-card.json" \
  --roundtrip-object-uri "$roundtrip_uri#$generation" \
  --output-dir "$work/workspace/runtime-evidence/provider" \
  --instance-id "$instance_id" --instance-name "$instance_name" \
  --zone "$zone" --durable-backup-uri "$prefix" \
  --hourly-cost-usd 0.881021512 --prior-cost-usd "$prior_cost" \
  --cost-ceiling-usd "$candidate_ceiling"
cp -a "$work/workspace/runtime-evidence" "$evidence/output/provider-evidence"

timeout 120 docker run --pull=never --rm --name ganesh-g3-pilot-card --entrypoint python3 \
  --gpus device=0 --network none --cpus 8 --memory 30g --pids-limit 4096 \
  --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=1g \
  --mount "type=bind,src=$work/workspace,dst=/workspace,readonly" \
  --mount "type=bind,src=$evidence/output,dst=/output" \
  --env PYTHONPATH=/workspace --workdir /workspace "$image" -B \
  scripts/train/build_gate3_capability_card.py \
  --provider-evidence /workspace/runtime-evidence/provider/provider-evidence.json \
  --output /output/candidate-card.json

timeout "$(left)" docker run --pull=never --rm --name ganesh-g3-pilot-training \
  --entrypoint python3 --gpus device=0 --network none --cpus 8 --memory 30g \
  --pids-limit 4096 --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=8g \
  --tmpfs /var/cache/triton:rw,exec,nosuid,nodev,size=1g \
  --mount "type=bind,src=$work/workspace,dst=/workspace,readonly" \
  --mount "type=bind,src=$work/model,dst=/model,readonly" \
  --mount "type=bind,src=$evidence/output,dst=/output" \
  --env HF_HUB_OFFLINE=1 --env TRANSFORMERS_OFFLINE=1 \
  --env PYTHONPATH=/workspace --env TRITON_CACHE_DIR=/var/cache/triton \
  --workdir /workspace "$image" -B scripts/train/run_sft.py \
  --phase lr-candidate --card /output/candidate-card.json \
  --config configs/train/gate3_capability_pilot_v1.json \
  --prepared-manifest artifacts/train/gate3-capability-pilot-v2/prepared-manifest.json \
  --prepared-data artifacts/train/gate3-capability-pilot-v2/prepared-train.jsonl \
  --validation-data artifacts/train/expansion-pilot-v1/prepared-validation.jsonl \
  --model-dir /model --output /output/training \
  --learning-rate "$candidate_lr" --maximum-seen-tokens 651639 \
  --hourly-cost-usd 0.881021512 --prior-cost-usd "$prior_cost" \
  --cost-ceiling-usd "$candidate_ceiling"
