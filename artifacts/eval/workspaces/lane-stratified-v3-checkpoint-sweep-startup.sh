#!/usr/bin/env bash
set -Eeuo pipefail

[[ $# == 5 ]] || { echo "usage: gcloud_startup_checkpoint_sweep.sh CARD PROJECT BUCKET PREFIX ATTEMPT_ID" >&2; exit 2; }
card=$1; project=$2; bucket=$3; prefix=$4; attempt_id=$5
[[ -f "$card" && "$attempt_id" =~ ^[0-9]{8}T[0-9]{6}Z$ ]] || exit 40
work=/opt/ganesh-mini-checkpoint-sweep
evidence=/var/lib/ganesh-mini-checkpoint-sweep
output="$evidence/output"
shared_tmp="$evidence/shared-tmp"
mkdir -p "$work" "$output" "$shared_tmp"
env_file="$work/execution.env"
python3 - "$card" "$env_file" "$project" "$bucket" "$prefix" "$attempt_id" <<'PY'
import hashlib,json,os,pathlib,shlex,sys
p,out,project,bucket,prefix,attempt=sys.argv[1:]
c=json.load(open(p)); claimed=c.pop("execution_sha256",None)
actual=hashlib.sha256(json.dumps(c,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")).hexdigest()
if claimed!=actual or c.get("schema_version")!="ganesh-mini-checkpoint-sweep-gcloud-execution/v1" or c.get("status")!="authorized-executable": raise SystemExit("execution card seal/status mismatch")
e=c["execution"]
expected={"project":project,"gcs_bucket":bucket,"gcs_prefix":prefix,"attempt_id":attempt,"machine_type":"g2-standard-8","maximum_vm_lifetime_seconds":7200,"controller_budget_seconds":6000,"backup_reserve_seconds":1200,"automatic_restart":False,"external_ip":False,"boot_disk_auto_delete":True}
for k,v in expected.items():
 if e.get(k)!=v: raise SystemExit(f"execution card mismatch: {k}")
if c.get("promotion_authority")!="none" or c.get("training_allowed") is not False: raise SystemExit("evaluation-only boundary mismatch")
vals={"MAX_SECONDS":7200,"CONTROLLER_SECONDS":6000,"BACKUP_SECONDS":1200,"MACHINE":"g2-standard-8","IMAGE_REF":c["cuda_image"]["ref"],"IMAGE_ID":c["cuda_image"]["image_id"]}
for k,row in c["inputs"].items():
 if not row["uri"].startswith("gs://") or not row["uri"].rsplit("#",1)[-1].isdigit() or len(row["sha256"])!=64 or row["size_bytes"]<=0: raise SystemExit(f"invalid input: {k}")
 label=k.upper(); vals[label+"_URI"]=row["uri"]; vals[label+"_SHA"]=row["sha256"]; vals[label+"_SIZE"]=row["size_bytes"]
out=pathlib.Path(out); out.write_text(''.join(f'export {k}={shlex.quote(str(v))}\n' for k,v in vals.items()))
PY
source "$env_file"
[[ "$RECOVERY_ARCHIVE_URI" == *'#'* && "$RECOVERY_ARCHIVE_SHA" =~ ^[0-9a-f]{64}$ && "$RECOVERY_ARCHIVE_SIZE" -gt 0 ]]
observed_machine=$(basename "$(curl -fsS -H 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/instance/machine-type)")
[[ "$observed_machine" == "$MACHINE" && "$(nproc)" -ge 8 ]] || exit 43
terminal_prefix="runtime-terminal-$attempt_id"
checkpoint_prefix="runtime-checkpoints/$attempt_id"
[[ -z "$(find "$output" -mindepth 1 -print -quit)" ]] || exit 44
exec 3>&1 4>&2
exec > >(tee -a "$evidence/startup.stdout.log" >&3)
stdout_tee_pid=$!
exec 2> >(tee -a "$evidence/startup.stderr.log" >&4)
stderr_tee_pid=$!
started=$(date +%s); hard_deadline=$((started+MAX_SECONDS)); controller_deadline=$((started+CONTROLLER_SECONDS))
( sleep $((MAX_SECONDS-10)); shutdown -h now ) & watchdog=$!
remaining() { local n=$((controller_deadline-$(date +%s))); ((n>0)) || return 1; printf '%s\n' "$n"; }
backup_remaining() { local n=$((hard_deadline-20-$(date +%s))); ((n>0)) || return 1; printf '%s\n' "$n"; }
checkpoint() { timeout 300 gcloud storage rsync "$evidence" "gs://$bucket/$prefix/$checkpoint_prefix" --recursive --project="$project" >> /var/log/ganesh-checkpoint-sweep-backup.log 2>&1 || true; }
checkpoint_loop() { while true; do checkpoint; sleep 120; done; }
write_inventory() { (cd "$evidence" && find . -type f ! -name runtime-files.sha256 -print0 | sort -z | xargs -0 sha256sum > runtime-files.sha256); }
finish() {
  local status=$?
  trap - EXIT
  printf '%s\n' "$status" > "$evidence/startup-exit-code.txt"
  kill "$watchdog" "${checkpoint_pid:-}" 2>/dev/null || true
  wait "${checkpoint_pid:-}" 2>/dev/null || true
  exec 1>&3 2>&4
  wait "$stdout_tee_pid" "$stderr_tee_pid" || status=92
  write_inventory || status=91
  timeout "$(backup_remaining)" gcloud storage rsync "$evidence" "gs://$bucket/$prefix/$terminal_prefix" --recursive --project="$project" || status=90
  ( sleep 2; shutdown -h now ) >/dev/null 2>&1 &
  exit "$status"
}
trap finish EXIT
download() { timeout "$(remaining)" gcloud storage cp "$1" "$4" --project="$project"; [[ "$(stat -c %s "$4")" == "$3" ]]; printf '%s  %s\n' "$2" "$4" | sha256sum -c -; }
for name in WORKSPACE_ARCHIVE WORKSPACE_MANIFEST RECOVERY_ARCHIVE MODEL_ARCHIVE CUDA_IMAGE_ARCHIVE DOCKER_BUNDLE VERIFIER_ARCHIVE VERIFIER_MANIFEST; do
  uri_name="${name}_URI"; sha_name="${name}_SHA"; size_name="${name}_SIZE"
  download "${!uri_name}" "${!sha_name}" "${!size_name}" "$work/${name,,}"
done
mkdir "$work/workspace" "$work/recovery" "$work/model" "$work/docker-bundle"
tar -xzf "$work/workspace_archive" -C "$work/workspace"
python3 - "$work/recovery_archive" "$work/recovery" <<'PY'
import pathlib,sys,tarfile
dst=pathlib.Path(sys.argv[2]).resolve()
with tarfile.open(sys.argv[1],"r:gz") as t:
 for m in t.getmembers():
  p=pathlib.PurePosixPath(m.name)
  if m.name.startswith('/') or '..' in p.parts or (not m.isdir() and not m.isfile()): raise SystemExit('unsafe recovery archive')
 t.extractall(dst,filter='data')
PY
tar -xzf "$work/model_archive" -C "$work/model"
tar -xzf "$work/docker_bundle" -C "$work/docker-bundle" --strip-components=1
(cd "$work/docker-bundle" && sha256sum -c bundle-files.sha256)
export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true NEEDRESTART_MODE=a
timeout 300 dpkg --force-confold -i "$work"/docker-bundle/debs/*.deb > "$evidence/docker-offline-install.log" 2>&1 || timeout 300 dpkg --force-confold -i "$work"/docker-bundle/debs/*.deb >> "$evidence/docker-offline-install.log" 2>&1
nvidia-ctk runtime configure --runtime=docker; systemctl restart docker
timeout 30 bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done'
timeout 600 bash -c 'set -o pipefail; zstd -dc "$1" | docker load' _ "$work/cuda_image_archive"
[[ "$(docker image inspect --format '{{.Id}}' "$IMAGE_REF")" == "$IMAGE_ID" ]]
checkpoint_loop & checkpoint_pid=$!
training="$work/recovery/terminal/output/campaign/training/expansion-pilot"
configs="$work/workspace/measurement/gate4/lane-stratified-probe-checkpoint-sweep-20260910/configs"
controller_seconds=$(remaining)
PYTHONPATH="$work/workspace" python3 -B "$work/workspace/scripts/campaign/run_checkpoint_sweep_host.py" \
  --eval-workspace "$work/workspace" --eval-manifest "$work/workspace_manifest" --eval-archive "$work/workspace_archive" \
  --model "$work/model" --training "$training" \
  --training-terminal "$work/recovery/terminal/output/campaign/training-terminal.json" \
  --config-dir "$configs" --final-canary "$work/recovery/terminal/output/campaign/evaluation/canary" \
  --verifier-manifest "$work/verifier_manifest" --verifier-archive "$work/verifier_archive" \
  --output "$output" --shared-tmp "$shared_tmp" --cuda-image "$IMAGE_REF" --cuda-image-id "$IMAGE_ID" \
  --attempt-id "$attempt_id" --max-seconds "$controller_seconds" --per-checkpoint-max-seconds 1200 \
  --finalization-reserve-seconds 600
