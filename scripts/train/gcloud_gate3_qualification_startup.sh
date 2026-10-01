#!/usr/bin/env bash
# Qualification only: immutable inputs, offline CUDA probe, terminal backup, STOP.
set -Eeuo pipefail
meta=http://metadata.google.internal/computeMetadata/v1
getmeta() { curl -fsS --retry 3 -H 'Metadata-Flavor: Google' "$meta/$1"; }
project=$(getmeta instance/attributes/ganesh-project)
prefix=$(getmeta instance/attributes/ganesh-prefix)
card_uri=$(getmeta instance/attributes/ganesh-card-uri)
card_sha=$(getmeta instance/attributes/ganesh-card-sha)
work=/opt/ganesh-g3-qual
evidence=/var/lib/ganesh-g3-qual
mkdir -p "$work" "$evidence/output"
started=$(date +%s)
deadline=$((started+6000))
left() { local n=$((deadline-$(date +%s))); ((n>0)); printf '%s\n' "$n"; }
( sleep 7190; shutdown -h now ) & watchdog=$!
exec 3>&1 4>&2
exec > >(tee -a "$evidence/startup.stdout.log" >&3); outtee=$!
exec 2> >(tee -a "$evidence/startup.stderr.log" >&4); errtee=$!
checkpoint() { timeout 90 gcloud storage rsync "$evidence" "$prefix/checkpoints" --recursive --project="$project" >> /var/log/ganesh-g3-qual-backup.log 2>&1 || true; }
finish() {
  local status=$?
  trap - EXIT
  kill "${checkpoint_pid:-}" 2>/dev/null || true
  wait "${checkpoint_pid:-}" 2>/dev/null || true
  docker stop -t 10 ganesh-g3-qualification >/dev/null 2>&1 || true
  printf '%s\n' "$status" > "$evidence/startup-exit-code.txt"
  cp /var/log/ganesh-g3-qual-backup.log "$evidence/checkpoint-backup.log" 2>/dev/null || true
  exec 1>&3 2>&4
  wait "$outtee" "$errtee" || status=92
  (cd "$evidence" && find . -type f ! -name runtime-files.sha256 -print0 | sort -z | xargs -0 sha256sum > runtime-files.sha256) || status=91
  timeout 900 gcloud storage rsync "$evidence" "$prefix/terminal" --recursive --project="$project" || status=90
  kill "$watchdog" 2>/dev/null || true
  ( sleep 2; shutdown -h now ) >/dev/null 2>&1 &
  exit "$status"
}
trap finish EXIT
timeout 120 gcloud storage cp "$card_uri" "$work/card.json" --project="$project"
printf '%s  %s\n' "$card_sha" "$work/card.json" | sha256sum -c -
cp "$work/card.json" "$evidence/execution-card.json"
python3 - "$work/card.json" "$work/inputs.tsv" <<'PY'
import hashlib,json,pathlib,sys
c=json.load(open(sys.argv[1])); seal=c.pop('execution_sha256')
assert hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()==seal
assert c['schema_version']=='ganesh-mini-gate3-qualification-gcloud/v1'
assert c['absolute_incremental_ceiling_usd']=='5' and c['quality_pilot_allowed'] is False
assert c['maximum_vm_seconds']==7200 and c['probe_rows']==16
if c.get('prior_spend_reserve_usd')=='2.00':
 assert c['canonical_rescue_plan_sha256']=='0cb94af6f12bae840c6657c7d7f6402759b0313d7301b81c96afcb9fb5fb342e'
 assert c['maximum_additional_allocated_starts']==1
 assert c['inputs']['model_materializer']['sha256']=='422a0559cf25de3d505304fcdcdf7aa1a92968268297c837a1ad14e2b5268b58'
if c.get('prior_spend_reserve_usd')=='2.50':
 assert c['usable_floor_plan_sha256']=='3bee60eb0987eccd8147d638b31beb5f4322539c32f68537b6c06d2943573de7'
 assert c['gpu_hardware_contract']=='ganesh-mini-gate3-l4-usable-v1'
 assert c['l4_usable_floor_bytes']==23622320128 and c['other_gpu_floor_bytes']==24000000000
 assert c['maximum_additional_allocated_starts']==1
 assert c['inputs']['workspace_archive']['sha256']=='0b044e5dc44cc7bc1828cc73f5964a825baafb90d16c7aeac4d8264537d114ae'
 assert c['inputs']['model_materializer']['sha256']=='422a0559cf25de3d505304fcdcdf7aa1a92968268297c837a1ad14e2b5268b58'
with open(sys.argv[2],'x') as h:
 for key,r in c['inputs'].items():
  assert r['uri'].startswith('gs://') and r['uri'].rsplit('#',1)[-1].isdigit()
  h.write('\t'.join([key,r['uri'],r['sha256'],str(r['size_bytes'])])+'\n')
PY
observed_machine=$(basename "$(getmeta instance/machine-type)")
[[ "$observed_machine" == g2-standard-8 ]]
getmeta instance/id > "$evidence/instance-id.txt"
nvidia-smi -q > "$evidence/nvidia-smi.txt"
( while true; do checkpoint; sleep 120; done ) & checkpoint_pid=$!
while IFS=$'\t' read -r name uri sha size; do
  timeout "$(left)" gcloud storage cp "$uri" "$work/$name" --project="$project"
  [[ "$(stat -c %s "$work/$name")" == "$size" ]]
  printf '%s  %s\n' "$sha" "$work/$name" | sha256sum -c -
done < "$work/inputs.tsv"
mkdir "$work/workspace" "$work/model" "$work/bundle"
tar -xzf "$work/workspace_archive" -C "$work/workspace"
if [[ -f "$work/model_materializer" ]]; then
  archive_sha=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["inputs"]["model_archive"]["sha256"])' "$work/card.json")
  timeout "$(left)" env PYTHONPATH="$work/workspace" python3 -B "$work/model_materializer" \
    --archive "$work/model_archive" \
    --inventory "$work/workspace/configs/model/qwen3_5_2b.inventory.json" \
    --archive-sha256 "$archive_sha" --materialize-dir "$work/model" \
    --output "$evidence/model-canonical-materialization.json"
else
  tar -xzf "$work/model_archive" -C "$work/model"
fi
tar -xzf "$work/docker_bundle" -C "$work/bundle" --strip-components=1
(cd "$work/bundle" && sha256sum -c bundle-files.sha256)
export DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a
timeout 300 dpkg --force-confold -i "$work"/bundle/debs/*.deb > "$evidence/docker-install.log" 2>&1 || timeout 300 dpkg --force-confold -i "$work"/bundle/debs/*.deb >> "$evidence/docker-install.log" 2>&1
nvidia-ctk runtime configure --runtime=docker
systemctl restart docker
timeout 30 bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done'
timeout "$(left)" bash -c 'set -o pipefail; zstd -dc "$1" | docker load' _ "$work/cuda_image_archive"
image=ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082
[[ "$(docker image inspect --format '{{.Id}}' "$image")" == sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860 ]]
probe_seconds=$(left)
(( probe_seconds <= 1800 )) || probe_seconds=1800
timeout "$probe_seconds" docker run --pull=never --rm --name ganesh-g3-qualification \
  --entrypoint python3 \
  --gpus device=0 --network none --cpus 8 --memory 30g --pids-limit 4096 \
  --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=8g \
  --tmpfs /var/cache/triton:rw,exec,nosuid,nodev,size=1g \
  --mount "type=bind,src=$work/workspace,dst=/workspace,readonly" \
  --mount "type=bind,src=$work/model,dst=/model,readonly" \
  --mount "type=bind,src=$evidence/output,dst=/output" \
  --env HF_HUB_OFFLINE=1 --env TRANSFORMERS_OFFLINE=1 --env PYTHONPATH=/workspace \
  --env TRITON_CACHE_DIR=/var/cache/triton --workdir /workspace "$image" \
  -B scripts/train/measure_gate3_capability_throughput.py \
  --model-dir /model --instance-id "$(cat "$evidence/instance-id.txt")" \
  --output /output/throughput.json --hourly-cost-usd 0.881021512 \
  --absolute-incremental-ceiling-usd 5
