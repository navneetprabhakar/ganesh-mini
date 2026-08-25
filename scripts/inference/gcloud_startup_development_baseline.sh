#!/usr/bin/env bash
set -Eeuo pipefail

required=(GANESH_GCP_PROJECT GANESH_GCS_BUCKET GANESH_GCS_PREFIX GANESH_WORKSPACE_ARCHIVE_URI GANESH_WORKSPACE_ARCHIVE_SHA256 GANESH_WORKSPACE_ARCHIVE_SIZE GANESH_WORKSPACE_MANIFEST_URI GANESH_WORKSPACE_MANIFEST_SHA256 GANESH_WORKSPACE_MANIFEST_SIZE GANESH_TRAIN_WORKSPACE_ARCHIVE_URI GANESH_TRAIN_WORKSPACE_ARCHIVE_SHA256 GANESH_TRAIN_WORKSPACE_ARCHIVE_SIZE GANESH_TRAIN_WORKSPACE_MANIFEST_URI GANESH_TRAIN_WORKSPACE_MANIFEST_SHA256 GANESH_TRAIN_WORKSPACE_MANIFEST_SIZE GANESH_GATE0_REPORT_URI GANESH_GATE0_REPORT_SHA256 GANESH_GATE0_REPORT_SIZE GANESH_GATE2_REPORT_URI GANESH_GATE2_REPORT_SHA256 GANESH_GATE2_REPORT_SIZE GANESH_MODEL_ARCHIVE_URI GANESH_MODEL_ARCHIVE_SHA256 GANESH_MODEL_ARCHIVE_SIZE GANESH_IMAGE_ARCHIVE_URI GANESH_IMAGE_ARCHIVE_SHA256 GANESH_IMAGE_ARCHIVE_SIZE GANESH_DOCKER_BUNDLE_URI GANESH_DOCKER_BUNDLE_SHA256 GANESH_DOCKER_BUNDLE_SIZE GANESH_VERIFIER_ARCHIVE_URI GANESH_VERIFIER_ARCHIVE_SHA256 GANESH_VERIFIER_ARCHIVE_SIZE GANESH_VERIFIER_MANIFEST_URI GANESH_VERIFIER_MANIFEST_SHA256 GANESH_VERIFIER_MANIFEST_SIZE GANESH_CUDA_IMAGE_ID GANESH_CUDA_IMAGE_REF GANESH_ATTEMPT_ID GANESH_GPU_HOURLY_USD GANESH_SUPPORT_RESERVE_USD GANESH_ABSOLUTE_COST_CEILING_USD GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH GANESH_MAX_VM_LIFETIME_SECONDS GANESH_CONTROLLER_BUDGET_SECONDS GANESH_BACKUP_RESERVE_SECONDS GANESH_EXPECTED_MACHINE_TYPE GANESH_EXECUTION_CARD_URI GANESH_EXECUTION_CARD_SHA256 GANESH_EXECUTION_CARD_SIZE GANESH_EXECUTION_CARD_INTERNAL_SHA256 GANESH_CONTROLLER_URI GANESH_CONTROLLER_SHA256 GANESH_CONTROLLER_SIZE GANESH_METADATA_WRAPPER_URI GANESH_METADATA_WRAPPER_SHA256 GANESH_METADATA_WRAPPER_SIZE)
for name in "${required[@]}"; do [[ -n "${!name:-}" ]] || { echo "missing $name" >&2; exit 2; }; done
for name in GANESH_WORKSPACE_ARCHIVE_URI GANESH_WORKSPACE_MANIFEST_URI GANESH_TRAIN_WORKSPACE_ARCHIVE_URI GANESH_TRAIN_WORKSPACE_MANIFEST_URI GANESH_GATE0_REPORT_URI GANESH_GATE2_REPORT_URI GANESH_MODEL_ARCHIVE_URI GANESH_IMAGE_ARCHIVE_URI GANESH_DOCKER_BUNDLE_URI GANESH_VERIFIER_ARCHIVE_URI GANESH_VERIFIER_MANIFEST_URI GANESH_EXECUTION_CARD_URI; do
  case "${!name}" in *'#'[0-9]*) ;; *) echo "$name must include a GCS generation" >&2; exit 40;; esac
done
python3 - "$GANESH_GPU_HOURLY_USD" "$GANESH_SUPPORT_RESERVE_USD" "$GANESH_ABSOLUTE_COST_CEILING_USD" "$GANESH_MAX_VM_LIFETIME_SECONDS" "$GANESH_CONTROLLER_BUDGET_SECONDS" "$GANESH_BACKUP_RESERVE_SECONDS" <<'PY'
from decimal import Decimal
import sys
hourly, reserve, ceiling = map(Decimal, sys.argv[1:4])
life, controller, backup = map(Decimal, sys.argv[4:7])
if hourly <= 0 or reserve < 0 or ceiling <= 0:
    raise SystemExit("invalid cost guard")
if life <= 0 or controller <= 0 or backup < 600 or controller + backup > life:
    raise SystemExit("invalid runtime budget")
if any(value != value.to_integral_value() for value in (life, controller, backup)):
    raise SystemExit("runtime budgets must be whole seconds")
upper = hourly * life / Decimal(3600) + reserve
if upper >= ceiling:
    raise SystemExit(f"baseline upper cost {upper} is not below ceiling {ceiling}")
PY

metadata_header='Metadata-Flavor: Google'
observed_machine_type="$(basename "$(curl -fsS -H "$metadata_header" http://metadata.google.internal/computeMetadata/v1/instance/machine-type)")"
[[ "$observed_machine_type" == "$GANESH_EXPECTED_MACHINE_TYPE" ]] || { echo "machine type mismatch: $observed_machine_type" >&2; exit 43; }
[[ "$(uname -s)" == Linux && "$(uname -m)" == x86_64 ]] || { echo "baseline host must be Linux/AMD64" >&2; exit 43; }
(( $(nproc) >= 12 )) || { echo "baseline host exposes fewer than 12 CPUs" >&2; exit 43; }

work_dir=/opt/ganesh-mini-gate1
evidence_dir=/var/lib/ganesh-mini-gate1
output_dir="$evidence_dir/output"
shared_tmp="$evidence_dir/shared-tmp"
terminal_prefix="runtime-terminal-$GANESH_ATTEMPT_ID"
checkpoint_prefix="runtime-checkpoints/$GANESH_ATTEMPT_ID"
[[ "$GANESH_ATTEMPT_ID" =~ ^[0-9]{8}T[0-9]{6}Z$ ]] || { echo "invalid attempt id" >&2; exit 40; }
mkdir -p "$work_dir" "$output_dir" "$shared_tmp"
[[ -z "$(find "$output_dir" -mindepth 1 -print -quit)" ]] || { echo "attempt output is not fresh" >&2; exit 44; }
for remote in "$terminal_prefix" "$checkpoint_prefix"; do
  existing="$(gcloud storage ls --json "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/$remote/**" --project="$GANESH_GCP_PROJECT" 2>/dev/null || true)"
  [[ -z "$existing" || "$existing" == "[]" ]] || { echo "remote attempt prefix is not fresh: $remote" >&2; exit 44; }
done

exec > >(tee -a "$evidence_dir/startup.stdout.log") 2> >(tee -a "$evidence_dir/startup.stderr.log" >&2)
started_epoch="$(date +%s)"
[[ "$GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH" =~ ^[0-9]+$ ]] || { echo "invalid absolute deadline" >&2; exit 40; }
relative_hard_deadline_epoch="$((started_epoch + GANESH_MAX_VM_LIFETIME_SECONDS))"
if (( GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH < relative_hard_deadline_epoch )); then hard_deadline_epoch="$GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH"; else hard_deadline_epoch="$relative_hard_deadline_epoch"; fi
controller_deadline_epoch="$((started_epoch + GANESH_CONTROLLER_BUDGET_SECONDS))"
backup_deadline_epoch="$((hard_deadline_epoch - GANESH_BACKUP_RESERVE_SECONDS))"
(( controller_deadline_epoch <= backup_deadline_epoch )) || controller_deadline_epoch="$backup_deadline_epoch"
(( controller_deadline_epoch - started_epoch >= 600 )) || { echo "insufficient provider time for baseline" >&2; exit 45; }
printf '%s\n' "$controller_deadline_epoch" > "$evidence_dir/controller-deadline-epoch.txt"
printf '%s\n' "$hard_deadline_epoch" > "$evidence_dir/hard-stop-deadline-epoch.txt"
( sleep "$((hard_deadline_epoch - started_epoch - 10))"; shutdown -h now ) & watchdog_pid="$!"
remaining() { local value=$((controller_deadline_epoch - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
backup_remaining() { local value=$((hard_deadline_epoch - 20 - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
phase_timeout() { local cap="$1" left; left="$(remaining)" || return 1; (( left < cap )) && printf '%s\n' "$left" || printf '%s\n' "$cap"; }
checkpoint() {
  timeout "$(phase_timeout 300)" gcloud storage rsync "$evidence_dir" "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/$checkpoint_prefix" --recursive --exclude='shared-tmp/.*' --project="$GANESH_GCP_PROJECT" >> /var/log/ganesh-gate1-checkpoint-backup.log 2>&1 || true
}
checkpoint_loop() { while true; do checkpoint || true; sleep 120; done; }
final_backup() { timeout "$(backup_remaining)" gcloud storage rsync "$evidence_dir" "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/$terminal_prefix" --recursive --exclude='shared-tmp/.*' --project="$GANESH_GCP_PROJECT" > /var/log/ganesh-gate1-final-backup.log 2>&1; }
capture_checkpoint_log() {
  if [[ -f /var/log/ganesh-gate1-checkpoint-backup.log ]]; then
    cp /var/log/ganesh-gate1-checkpoint-backup.log "$evidence_dir/gcs-backup.log"
  else
    : > "$evidence_dir/gcs-backup.log"
  fi
}
stop_runtime_writers() {
  local pid
  for pid in "$watchdog_pid" "${checkpoint_pid:-}" "${nvml_pid:-}"; do
    [[ -n "$pid" ]] || continue
    kill "$pid" 2>/dev/null || true
  done
  for pid in "${checkpoint_pid:-}" "${nvml_pid:-}"; do
    [[ -n "$pid" ]] || continue
    wait "$pid" 2>/dev/null || true
  done
}
write_inventory() { (cd "$evidence_dir" && find . -type f ! -name runtime-files.sha256 ! -name .runtime-files.sha256.tmp -print0 | sort -z | xargs -0 sha256sum > .runtime-files.sha256.tmp && mv .runtime-files.sha256.tmp runtime-files.sha256); }
inventory_attempted=0
finish() {
  local status="$?"; trap - EXIT
  printf '%s\n' "$status" > "$evidence_dir/startup-exit-code.txt"
  stop_runtime_writers
  capture_checkpoint_log
  if (( inventory_attempted == 0 )); then inventory_attempted=1; write_inventory || status=91; fi
  if final_backup; then
    :
  else
    status=90
  fi
  exit "$status"
}
trap finish EXIT
download_verified() {
  local uri="$1" expected_sha="$2" expected_size="$3" destination="$4"
  timeout "$(remaining)" gcloud storage cp "$uri" "$destination" --project="$GANESH_GCP_PROJECT"
  [[ "$(stat -c %s "$destination")" == "$expected_size" ]]
  printf '%s  %s\n' "$expected_sha" "$destination" | timeout "$(phase_timeout 300)" sha256sum -c -
}

download_verified "$GANESH_EXECUTION_CARD_URI" "$GANESH_EXECUTION_CARD_SHA256" "$GANESH_EXECUTION_CARD_SIZE" "$evidence_dir/execution-card.json"
python3 - "$evidence_dir/execution-card.json" <<'PY'
import hashlib, json, os, sys

path = sys.argv[1]
card = json.load(open(path, encoding="utf-8"))
claimed = card.pop("execution_sha256", None)
actual = hashlib.sha256(json.dumps(card, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
if claimed != actual or claimed != os.environ["GANESH_EXECUTION_CARD_INTERNAL_SHA256"]:
    raise SystemExit("execution card seal mismatch")
if card.get("schema_version") != "ganesh-mini-staged-gcloud-execution/v1" or card.get("status") != "authorized-executable" or card.get("gate_range") != [1,3]:
    raise SystemExit("execution card contract mismatch")

expected = {
    "attempt_id": os.environ["GANESH_ATTEMPT_ID"],
    "gcp_project": os.environ["GANESH_GCP_PROJECT"],
    "gcs_bucket": os.environ["GANESH_GCS_BUCKET"],
    "gcs_prefix": os.environ["GANESH_GCS_PREFIX"],
    "machine_type": os.environ["GANESH_EXPECTED_MACHINE_TYPE"],
    "maximum_run_seconds": int(os.environ["GANESH_MAX_VM_LIFETIME_SECONDS"]),
    "controller_budget_seconds": int(os.environ["GANESH_CONTROLLER_BUDGET_SECONDS"]),
    "backup_reserve_seconds": int(os.environ["GANESH_BACKUP_RESERVE_SECONDS"]),
    "conservative_hourly_usd": os.environ["GANESH_GPU_HOURLY_USD"],
    "support_reserve_usd": os.environ["GANESH_SUPPORT_RESERVE_USD"],
    "absolute_cost_ceiling_usd": os.environ["GANESH_ABSOLUTE_COST_CEILING_USD"],
}
observed = {**card.get("execution", {}), **card.get("cost", {})}
for key, value in expected.items():
    if observed.get(key) != value:
        raise SystemExit(f"execution card metadata mismatch: {key}")

bindings = {
    "workspace_archive": "WORKSPACE_ARCHIVE",
    "workspace_manifest": "WORKSPACE_MANIFEST",
    "training_workspace_archive": "TRAIN_WORKSPACE_ARCHIVE",
    "training_workspace_manifest": "TRAIN_WORKSPACE_MANIFEST",
    "gate0_report": "GATE0_REPORT",
    "gate2_report": "GATE2_REPORT",
    "model_archive": "MODEL_ARCHIVE",
    "cuda_image_archive": "IMAGE_ARCHIVE",
    "docker_bundle": "DOCKER_BUNDLE",
    "verifier_archive": "VERIFIER_ARCHIVE",
    "verifier_manifest": "VERIFIER_MANIFEST",
}
inputs = card.get("inputs", {})
for key, variable in bindings.items():
    row = inputs.get(key, {})
    expected_row = {
        "uri": os.environ[f"GANESH_{variable}_URI"],
        "sha256": os.environ[f"GANESH_{variable}_SHA256"],
        "size_bytes": int(os.environ[f"GANESH_{variable}_SIZE"]),
    }
    if row != expected_row:
        raise SystemExit(f"execution card input mismatch: {key}")
image = card.get("cuda_image", {})
if image != {"ref": os.environ["GANESH_CUDA_IMAGE_REF"], "image_id": os.environ["GANESH_CUDA_IMAGE_ID"]}:
    raise SystemExit("execution card CUDA image mismatch")
launch = card.get("launch", {})
expected_launch = {
    "controller": {
        "uri": os.environ["GANESH_CONTROLLER_URI"],
        "sha256": os.environ["GANESH_CONTROLLER_SHA256"],
        "size_bytes": int(os.environ["GANESH_CONTROLLER_SIZE"]),
    },
    "metadata_wrapper": {
        "uri": os.environ["GANESH_METADATA_WRAPPER_URI"],
        "sha256": os.environ["GANESH_METADATA_WRAPPER_SHA256"],
        "size_bytes": int(os.environ["GANESH_METADATA_WRAPPER_SIZE"]),
    },
}
if launch != expected_launch:
    raise SystemExit("execution card launch binding mismatch")
PY
download_verified "$GANESH_WORKSPACE_ARCHIVE_URI" "$GANESH_WORKSPACE_ARCHIVE_SHA256" "$GANESH_WORKSPACE_ARCHIVE_SIZE" "$work_dir/workspace.tar.gz"
download_verified "$GANESH_WORKSPACE_MANIFEST_URI" "$GANESH_WORKSPACE_MANIFEST_SHA256" "$GANESH_WORKSPACE_MANIFEST_SIZE" "$work_dir/workspace-manifest.json"
download_verified "$GANESH_TRAIN_WORKSPACE_ARCHIVE_URI" "$GANESH_TRAIN_WORKSPACE_ARCHIVE_SHA256" "$GANESH_TRAIN_WORKSPACE_ARCHIVE_SIZE" "$work_dir/training-workspace.tar.gz"
download_verified "$GANESH_TRAIN_WORKSPACE_MANIFEST_URI" "$GANESH_TRAIN_WORKSPACE_MANIFEST_SHA256" "$GANESH_TRAIN_WORKSPACE_MANIFEST_SIZE" "$work_dir/training-workspace-manifest.json"
download_verified "$GANESH_GATE0_REPORT_URI" "$GANESH_GATE0_REPORT_SHA256" "$GANESH_GATE0_REPORT_SIZE" "$work_dir/gate0-readiness.json"
download_verified "$GANESH_GATE2_REPORT_URI" "$GANESH_GATE2_REPORT_SHA256" "$GANESH_GATE2_REPORT_SIZE" "$work_dir/gate2-readiness.json"
download_verified "$GANESH_MODEL_ARCHIVE_URI" "$GANESH_MODEL_ARCHIVE_SHA256" "$GANESH_MODEL_ARCHIVE_SIZE" "$work_dir/model.tar.gz"
download_verified "$GANESH_IMAGE_ARCHIVE_URI" "$GANESH_IMAGE_ARCHIVE_SHA256" "$GANESH_IMAGE_ARCHIVE_SIZE" "$work_dir/cuda-image.docker.tar.zst"
download_verified "$GANESH_DOCKER_BUNDLE_URI" "$GANESH_DOCKER_BUNDLE_SHA256" "$GANESH_DOCKER_BUNDLE_SIZE" "$work_dir/docker-bundle.tar.gz"
download_verified "$GANESH_VERIFIER_ARCHIVE_URI" "$GANESH_VERIFIER_ARCHIVE_SHA256" "$GANESH_VERIFIER_ARCHIVE_SIZE" "$work_dir/verifier-images.tar"
download_verified "$GANESH_VERIFIER_MANIFEST_URI" "$GANESH_VERIFIER_MANIFEST_SHA256" "$GANESH_VERIFIER_MANIFEST_SIZE" "$work_dir/verifier-manifest.json"
mkdir "$work_dir/workspace" "$work_dir/training-workspace" "$work_dir/model" "$work_dir/docker-bundle"
timeout "$(phase_timeout 180)" tar -xzf "$work_dir/workspace.tar.gz" -C "$work_dir/workspace"
timeout "$(phase_timeout 180)" tar -xzf "$work_dir/training-workspace.tar.gz" -C "$work_dir/training-workspace"
timeout "$(phase_timeout 300)" tar -xzf "$work_dir/model.tar.gz" -C "$work_dir/model"
timeout "$(phase_timeout 120)" tar -xzf "$work_dir/docker-bundle.tar.gz" -C "$work_dir/docker-bundle" --strip-components=1
timeout "$(phase_timeout 120)" bash -c 'cd "$1" && sha256sum -c bundle-files.sha256' _ "$work_dir/docker-bundle"
timeout "$(phase_timeout 300)" dpkg -i "$work_dir"/docker-bundle/debs/*.deb > "$evidence_dir/docker-offline-install.log" 2>&1 || timeout "$(phase_timeout 300)" dpkg -i "$work_dir"/docker-bundle/debs/*.deb >> "$evidence_dir/docker-offline-install.log" 2>&1
timeout "$(phase_timeout 30)" dpkg --audit > "$evidence_dir/dpkg-audit.txt"; [[ ! -s "$evidence_dir/dpkg-audit.txt" ]]
timeout "$(phase_timeout 30)" nvidia-ctk runtime configure --runtime=docker > "$evidence_dir/nvidia-ctk-configure.log" 2>&1
timeout "$(phase_timeout 30)" systemctl restart docker
timeout "$(phase_timeout 30)" bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done'
timeout "$(phase_timeout 600)" bash -c 'set -o pipefail; zstd -dc "$1" | docker load' _ "$work_dir/cuda-image.docker.tar.zst" > "$evidence_dir/cuda-image-load.log"
observed_image_id="$(docker image inspect --format '{{.Id}}' "$GANESH_CUDA_IMAGE_REF")"
printf '%s\n' "$observed_image_id" > "$evidence_dir/observed-image-id.txt"
[[ "$observed_image_id" == "$GANESH_CUDA_IMAGE_ID" ]]
uname -a > "$evidence_dir/uname.txt"
docker version > "$evidence_dir/docker-version.txt" 2>&1
nvidia-smi -q > "$evidence_dir/nvidia-smi-q.txt"
env | sed -E 's/(TOKEN|SECRET|PASSWORD|KEY)=.*/\1=REDACTED/' | sort > "$evidence_dir/environment-redacted.txt"
(
  while true; do nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used,memory.total,power.draw,temperature.gpu --format=csv,noheader,nounits >> "$evidence_dir/nvml-samples.csv"; sleep 5; done
) & nvml_pid="$!"
checkpoint_loop & checkpoint_pid="$!"

set +e
python3 "$work_dir/workspace/scripts/campaign/run_host.py" \
  --eval-workspace "$work_dir/workspace" \
  --eval-manifest "$work_dir/workspace-manifest.json" \
  --eval-archive "$work_dir/workspace.tar.gz" \
  --train-workspace "$work_dir/training-workspace" \
  --train-manifest "$work_dir/training-workspace-manifest.json" \
  --train-archive "$work_dir/training-workspace.tar.gz" \
  --model "$work_dir/model" \
  --verifier-manifest "$work_dir/verifier-manifest.json" \
  --verifier-archive "$work_dir/verifier-images.tar" \
  --gate0-report "$work_dir/gate0-readiness.json" \
  --gate2-report "$work_dir/gate2-readiness.json" \
  --output "$output_dir/campaign" \
  --shared-tmp "$shared_tmp" \
  --cuda-image "$GANESH_CUDA_IMAGE_REF" \
  --cuda-image-id "$GANESH_CUDA_IMAGE_ID" \
  --attempt-id "$GANESH_ATTEMPT_ID" \
  --max-seconds "$(remaining)" \
  --finalization-reserve-seconds 1800 \
  --hourly-cost-usd "$GANESH_GPU_HOURLY_USD" \
  --training-cost-ceiling-usd "18.65" > "$evidence_dir/controller.stdout.log" 2> "$evidence_dir/controller.stderr.log"
run_status="$?"
set -e
printf '%s\n' "$run_status" > "$evidence_dir/controller-exit-code.txt"
stop_runtime_writers
printf '%s\n' "$run_status" > "$evidence_dir/startup-exit-code.txt"
capture_checkpoint_log
inventory_attempted=1
write_inventory
final_backup
trap - EXIT
kill "$watchdog_pid" 2>/dev/null || true
exit "$run_status"
