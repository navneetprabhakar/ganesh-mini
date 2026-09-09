#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# != 1 ]]; then
  echo "usage: gcloud_startup_expansion_pilot.sh EXECUTION_CARD" >&2
  exit 2
fi
execution_card=$1
[[ -f "$execution_card" ]] || { echo "execution card is missing" >&2; exit 2; }

work_dir=/opt/ganesh-mini-gate4
evidence_dir=/var/lib/ganesh-mini-gate4
output_dir="$evidence_dir/output"
shared_tmp="$evidence_dir/shared-tmp"
if [[ -d "$work_dir" ]]; then
  prior_work_dir="/opt/ganesh-mini-gate4-prior-$(date -u +%Y%m%dT%H%M%SZ)"
  mv "$work_dir" "$prior_work_dir"
fi
if [[ -d "$evidence_dir" ]]; then
  prior_evidence_dir="/var/lib/ganesh-mini-gate4-prior-$(date -u +%Y%m%dT%H%M%SZ)"
  mv "$evidence_dir" "$prior_evidence_dir"
fi
mkdir -p "$work_dir" "$output_dir" "$shared_tmp"
env_file="$work_dir/execution.env"

python3 - "$execution_card" "$env_file" <<'PY'
import hashlib,json,pathlib,shlex,sys
source=pathlib.Path(sys.argv[1]); destination=pathlib.Path(sys.argv[2])
card=json.loads(source.read_text())
claimed=card.pop("execution_sha256",None)
actual=hashlib.sha256(json.dumps(card,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
if claimed!=actual or card.get("schema_version")!="ganesh-mini-gate4-gcloud-execution/v1" or card.get("status")!="authorized-executable":
    raise SystemExit("execution card seal/status mismatch")
execution=card["execution"]; cost=card["cost"]; cuda=card["cuda_image"]; inputs=card["inputs"]
values={
    "GANESH_EXECUTION_CARD_INTERNAL_SHA256":claimed,
    "GANESH_GCP_PROJECT":execution["project"], "GANESH_GCS_BUCKET":execution["gcs_bucket"],
    "GANESH_GCS_PREFIX":execution["gcs_prefix"], "GANESH_ATTEMPT_ID":execution["attempt_id"],
    "GANESH_EXPECTED_MACHINE_TYPE":execution["machine_type"],
    "GANESH_MAX_VM_LIFETIME_SECONDS":execution["maximum_vm_lifetime_seconds"],
    "GANESH_CONTROLLER_BUDGET_SECONDS":execution["controller_budget_seconds"],
    "GANESH_BACKUP_RESERVE_SECONDS":execution["backup_reserve_seconds"],
    "GANESH_GPU_HOURLY_USD":cost["compute_hourly_usd"],
    "GANESH_DISK_UPPER_USD":cost["boot_disk_upper_usd"],
    "GANESH_SUPPORT_RESERVE_USD":cost["support_reserve_usd"],
    "GANESH_ABSOLUTE_COST_CEILING_USD":cost["absolute_cost_ceiling_usd"],
    "GANESH_CUDA_IMAGE_ID":cuda["image_id"], "GANESH_CUDA_IMAGE_REF":cuda["ref"],
}
mapping={
    "eval_workspace_archive":"EVAL_ARCHIVE", "eval_workspace_manifest":"EVAL_MANIFEST",
    "train_workspace_archive":"TRAIN_ARCHIVE", "train_workspace_manifest":"TRAIN_MANIFEST",
    "training_execution_card":"TRAIN_CARD", "model_archive":"MODEL_ARCHIVE",
    "cuda_image_archive":"IMAGE_ARCHIVE", "docker_bundle":"DOCKER_BUNDLE",
    "verifier_archive":"VERIFIER_ARCHIVE", "verifier_manifest":"VERIFIER_MANIFEST",
}
for key,label in mapping.items():
    row=inputs[key]
    if not isinstance(row.get("uri"),str) or "#" not in row["uri"] or len(row.get("sha256",""))!=64:
        raise SystemExit(f"invalid immutable input binding: {key}")
    values[f"GANESH_{label}_URI"]=row["uri"]
    values[f"GANESH_{label}_SHA256"]=row["sha256"]
    values[f"GANESH_{label}_SIZE"]=row["size_bytes"]
destination.write_text("".join(f"export {key}={shlex.quote(str(value))}\n" for key,value in values.items()))
PY
source "$env_file"

[[ "$GANESH_ATTEMPT_ID" =~ ^[0-9]{8}T[0-9]{6}Z$ ]] || { echo "invalid attempt id" >&2; exit 40; }
for name in GANESH_EVAL_ARCHIVE_URI GANESH_EVAL_MANIFEST_URI GANESH_TRAIN_ARCHIVE_URI GANESH_TRAIN_MANIFEST_URI GANESH_TRAIN_CARD_URI GANESH_MODEL_ARCHIVE_URI GANESH_IMAGE_ARCHIVE_URI GANESH_DOCKER_BUNDLE_URI GANESH_VERIFIER_ARCHIVE_URI GANESH_VERIFIER_MANIFEST_URI; do
  case "${!name}" in *'#'[0-9]*) ;; *) echo "$name must include a GCS generation" >&2; exit 40;; esac
done
python3 - "$GANESH_GPU_HOURLY_USD" "$GANESH_DISK_UPPER_USD" "$GANESH_SUPPORT_RESERVE_USD" "$GANESH_ABSOLUTE_COST_CEILING_USD" "$GANESH_MAX_VM_LIFETIME_SECONDS" "$GANESH_CONTROLLER_BUDGET_SECONDS" "$GANESH_BACKUP_RESERVE_SECONDS" <<'PY'
from decimal import Decimal
import sys
hourly,disk,reserve,ceiling=map(Decimal,sys.argv[1:5]); life,controller,backup=map(int,sys.argv[5:8])
if min(hourly,disk,reserve,ceiling)<=0 or not 3600<=life<=28800 or controller+backup>life or backup<1200:
    raise SystemExit("invalid cost/runtime guard")
upper=hourly*Decimal(life)/Decimal(3600)+disk+reserve
if upper>ceiling: raise SystemExit(f"provider upper cost {upper} exceeds ceiling {ceiling}")
PY
metadata_header='Metadata-Flavor: Google'
observed_machine_type=$(basename "$(curl -fsS -H "$metadata_header" http://metadata.google.internal/computeMetadata/v1/instance/machine-type)")
[[ "$observed_machine_type" == "$GANESH_EXPECTED_MACHINE_TYPE" ]] || { echo "machine type mismatch" >&2; exit 43; }
[[ "$(uname -s)" == Linux && "$(uname -m)" == x86_64 ]] || { echo "host must be Linux/AMD64" >&2; exit 43; }
(( $(nproc) >= 8 )) || { echo "host exposes fewer than 8 CPUs" >&2; exit 43; }
[[ -z "$(find "$output_dir" -mindepth 1 -print -quit)" ]] || { echo "attempt output is not fresh" >&2; exit 44; }

exec > >(tee -a "$evidence_dir/startup.stdout.log") 2> >(tee -a "$evidence_dir/startup.stderr.log" >&2)
started_epoch=$(date +%s)
hard_deadline_epoch=$((started_epoch + GANESH_MAX_VM_LIFETIME_SECONDS))
controller_deadline_epoch=$((started_epoch + GANESH_CONTROLLER_BUDGET_SECONDS))
backup_deadline_epoch=$((hard_deadline_epoch - GANESH_BACKUP_RESERVE_SECONDS))
(( controller_deadline_epoch <= backup_deadline_epoch )) || controller_deadline_epoch=$backup_deadline_epoch
( sleep "$((GANESH_MAX_VM_LIFETIME_SECONDS - 10))"; shutdown -h now ) & watchdog_pid=$!
remaining() { local value=$((controller_deadline_epoch - $(date +%s))); (( value > 0 )) || return 1; echo "$value"; }
backup_remaining() { local value=$((hard_deadline_epoch - 20 - $(date +%s))); (( value > 0 )) || return 1; echo "$value"; }
checkpoint_prefix="runtime-checkpoints/$GANESH_ATTEMPT_ID"
terminal_prefix="runtime-terminal-$GANESH_ATTEMPT_ID"
checkpoint() { timeout 300 gcloud storage rsync "$evidence_dir" "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/$checkpoint_prefix" --recursive --exclude='shared-tmp/.*' --project="$GANESH_GCP_PROJECT" >> /var/log/ganesh-gate4-checkpoint.log 2>&1 || true; }
checkpoint_loop() { while true; do checkpoint; sleep 120; done; }
final_backup() { timeout "$(backup_remaining)" gcloud storage rsync "$evidence_dir" "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/$terminal_prefix" --recursive --exclude='shared-tmp/.*' --project="$GANESH_GCP_PROJECT" > /var/log/ganesh-gate4-final-backup.log 2>&1; }
stop_writers() { kill "$watchdog_pid" "${checkpoint_pid:-}" "${nvml_pid:-}" 2>/dev/null || true; wait "${checkpoint_pid:-}" "${nvml_pid:-}" 2>/dev/null || true; }
write_inventory() { (cd "$evidence_dir" && find . -type f ! -name runtime-files.sha256 -print0 | sort -z | xargs -0 sha256sum > runtime-files.sha256); }
finish() {
  local status=$?; trap - EXIT
  echo "$status" > "$evidence_dir/startup-exit-code.txt"
  stop_writers
  write_inventory || status=91
  final_backup || status=90
  ( sleep 2; shutdown -h now ) >/dev/null 2>&1 &
  exit "$status"
}
trap finish EXIT

download_verified() {
  local uri=$1 expected_sha=$2 expected_size=$3 destination=$4
  timeout "$(remaining)" gcloud storage cp "$uri" "$destination" --project="$GANESH_GCP_PROJECT"
  [[ "$(stat -c %s "$destination")" == "$expected_size" ]]
  echo "$expected_sha  $destination" | timeout 600 sha256sum -c -
}
download_verified "$GANESH_EVAL_ARCHIVE_URI" "$GANESH_EVAL_ARCHIVE_SHA256" "$GANESH_EVAL_ARCHIVE_SIZE" "$work_dir/eval.tar.gz"
download_verified "$GANESH_EVAL_MANIFEST_URI" "$GANESH_EVAL_MANIFEST_SHA256" "$GANESH_EVAL_MANIFEST_SIZE" "$work_dir/eval.manifest.json"
download_verified "$GANESH_TRAIN_ARCHIVE_URI" "$GANESH_TRAIN_ARCHIVE_SHA256" "$GANESH_TRAIN_ARCHIVE_SIZE" "$work_dir/train.tar.gz"
download_verified "$GANESH_TRAIN_MANIFEST_URI" "$GANESH_TRAIN_MANIFEST_SHA256" "$GANESH_TRAIN_MANIFEST_SIZE" "$work_dir/train.manifest.json"
download_verified "$GANESH_TRAIN_CARD_URI" "$GANESH_TRAIN_CARD_SHA256" "$GANESH_TRAIN_CARD_SIZE" "$work_dir/training-execution-card.json"
download_verified "$GANESH_MODEL_ARCHIVE_URI" "$GANESH_MODEL_ARCHIVE_SHA256" "$GANESH_MODEL_ARCHIVE_SIZE" "$work_dir/model.tar.gz"
download_verified "$GANESH_IMAGE_ARCHIVE_URI" "$GANESH_IMAGE_ARCHIVE_SHA256" "$GANESH_IMAGE_ARCHIVE_SIZE" "$work_dir/cuda-image.docker.tar.zst"
download_verified "$GANESH_DOCKER_BUNDLE_URI" "$GANESH_DOCKER_BUNDLE_SHA256" "$GANESH_DOCKER_BUNDLE_SIZE" "$work_dir/docker-bundle.tar.gz"
download_verified "$GANESH_VERIFIER_ARCHIVE_URI" "$GANESH_VERIFIER_ARCHIVE_SHA256" "$GANESH_VERIFIER_ARCHIVE_SIZE" "$work_dir/verifier-images.tar"
download_verified "$GANESH_VERIFIER_MANIFEST_URI" "$GANESH_VERIFIER_MANIFEST_SHA256" "$GANESH_VERIFIER_MANIFEST_SIZE" "$work_dir/verifier-manifest.json"

mkdir "$work_dir/eval" "$work_dir/train" "$work_dir/model" "$work_dir/docker-bundle"
tar -xzf "$work_dir/eval.tar.gz" -C "$work_dir/eval"
tar -xzf "$work_dir/train.tar.gz" -C "$work_dir/train"
tar -xzf "$work_dir/model.tar.gz" -C "$work_dir/model"
tar -xzf "$work_dir/docker-bundle.tar.gz" -C "$work_dir/docker-bundle" --strip-components=1
( cd "$work_dir/docker-bundle" && sha256sum -c bundle-files.sha256 )
export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true
export NEEDRESTART_MODE=a
timeout 300 dpkg --force-confold -i "$work_dir"/docker-bundle/debs/*.deb > "$evidence_dir/docker-offline-install.log" 2>&1 || \
  timeout 300 dpkg --force-confold -i "$work_dir"/docker-bundle/debs/*.deb >> "$evidence_dir/docker-offline-install.log" 2>&1
dpkg --audit > "$evidence_dir/dpkg-audit.txt"; [[ ! -s "$evidence_dir/dpkg-audit.txt" ]]
nvidia-ctk runtime configure --runtime=docker > "$evidence_dir/nvidia-ctk-configure.log" 2>&1
systemctl restart docker
timeout 30 bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done'
timeout 600 bash -c 'set -o pipefail; zstd -dc "$1" | docker load' _ "$work_dir/cuda-image.docker.tar.zst" > "$evidence_dir/cuda-image-load.log"
observed_image_id=$(docker image inspect --format '{{.Id}}' "$GANESH_CUDA_IMAGE_REF")
[[ "$observed_image_id" == "$GANESH_CUDA_IMAGE_ID" ]]
uname -a > "$evidence_dir/uname.txt"
docker version > "$evidence_dir/docker-version.txt" 2>&1
nvidia-smi -q > "$evidence_dir/nvidia-smi-q.txt"
( while true; do nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used,memory.total,power.draw,temperature.gpu --format=csv,noheader,nounits >> "$evidence_dir/nvml-samples.csv"; sleep 5; done ) & nvml_pid=$!
checkpoint_loop & checkpoint_pid=$!

set +e
PYTHONPATH="$work_dir/eval" python3 -B "$work_dir/eval/scripts/campaign/run_expansion_host.py" \
  --eval-workspace "$work_dir/eval" --eval-manifest "$work_dir/eval.manifest.json" --eval-archive "$work_dir/eval.tar.gz" \
  --train-workspace "$work_dir/train" --train-manifest "$work_dir/train.manifest.json" --train-archive "$work_dir/train.tar.gz" \
  --card "$work_dir/training-execution-card.json" --model "$work_dir/model" \
  --verifier-manifest "$work_dir/verifier-manifest.json" --verifier-archive "$work_dir/verifier-images.tar" \
  --output "$output_dir/campaign" --shared-tmp "$shared_tmp" --cuda-image "$GANESH_CUDA_IMAGE_REF" --cuda-image-id "$GANESH_CUDA_IMAGE_ID" \
  --attempt-id "$GANESH_ATTEMPT_ID" --max-seconds "$(remaining)" --finalization-reserve-seconds 1800 \
  --hourly-cost-usd "$GANESH_GPU_HOURLY_USD" --absolute-cost-ceiling-usd "$GANESH_ABSOLUTE_COST_CEILING_USD" \
  > "$evidence_dir/controller.stdout.log" 2> "$evidence_dir/controller.stderr.log"
controller_status=$?
set -e
echo "$controller_status" > "$evidence_dir/controller-exit-code.txt"
exit "$controller_status"
