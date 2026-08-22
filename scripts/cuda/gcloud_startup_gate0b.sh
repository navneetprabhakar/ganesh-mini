#!/usr/bin/env bash
set -Eeuo pipefail

required=(GANESH_GCP_PROJECT GANESH_GCS_BUCKET GANESH_GCS_PREFIX GANESH_WORKSPACE_ARCHIVE_URI GANESH_WORKSPACE_ARCHIVE_SHA256 GANESH_WORKSPACE_ARCHIVE_SIZE GANESH_MODEL_ARCHIVE_URI GANESH_MODEL_ARCHIVE_SHA256 GANESH_MODEL_ARCHIVE_SIZE GANESH_IMAGE_ARCHIVE_URI GANESH_IMAGE_ARCHIVE_SHA256 GANESH_IMAGE_ARCHIVE_SIZE GANESH_DOCKER_BUNDLE_URI GANESH_DOCKER_BUNDLE_SHA256 GANESH_DOCKER_BUNDLE_SIZE GANESH_CUDA_IMAGE_ID GANESH_CUDA_IMAGE_REF GANESH_ATTEMPT_ID GANESH_GPU_HOURLY_USD GANESH_CUMULATIVE_COST_USD GANESH_SUPPORT_RESERVE_USD GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH)
for name in "${required[@]}"; do [[ -n "${!name:-}" ]] || { echo "missing $name" >&2; exit 2; }; done
for name in GANESH_WORKSPACE_ARCHIVE_URI GANESH_MODEL_ARCHIVE_URI GANESH_IMAGE_ARCHIVE_URI GANESH_DOCKER_BUNDLE_URI; do
  case "${!name}" in *'#'[0-9]*) ;; *) echo "$name must include a GCS generation" >&2; exit 40;; esac
done
python3 - "$GANESH_CUMULATIVE_COST_USD" "$GANESH_GPU_HOURLY_USD" "$GANESH_SUPPORT_RESERVE_USD" <<'PY'
from decimal import Decimal
import sys
total=Decimal(sys.argv[1])+Decimal(sys.argv[2])*(Decimal(1200)/Decimal(3600))+Decimal(sys.argv[3])
if any(Decimal(value) < 0 for value in sys.argv[1:]) or Decimal(sys.argv[2]) <= 0:
    raise SystemExit("cost inputs must be nonnegative and GPU hourly rate positive")
if total >= Decimal("5"): raise SystemExit(f"cumulative qualification ceiling is not below USD 5: {total}")
PY

work_dir="/opt/ganesh-mini-gate0b"
evidence_dir="/var/lib/ganesh-mini-gate0b"
output_dir="$evidence_dir/output/$GANESH_ATTEMPT_ID"
[[ "$GANESH_ATTEMPT_ID" =~ ^[a-z0-9][a-z0-9-]{0,62}$ ]] || { echo "invalid attempt id" >&2; exit 40; }
terminal_prefix="runtime-terminal-$GANESH_ATTEMPT_ID"
mkdir -p "$work_dir" "$output_dir"
[[ -z "$(find "$output_dir" -mindepth 1 -print -quit)" ]] || { echo "attempt output is not fresh" >&2; exit 44; }
exec > >(tee -a "$evidence_dir/startup.stdout.log") 2> >(tee -a "$evidence_dir/startup.stderr.log" >&2)
started_epoch="$(date +%s)"
[[ "$GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH" =~ ^[0-9]+$ ]] || { echo "absolute hard deadline must be an epoch" >&2; exit 40; }
relative_hard_deadline_epoch="$((started_epoch + 1200))"
if (( GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH < relative_hard_deadline_epoch )); then
  hard_deadline_epoch="$GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH"
else
  hard_deadline_epoch="$relative_hard_deadline_epoch"
fi
relative_controller_deadline_epoch="$((started_epoch + 900))"
backup_reserved_deadline_epoch="$((hard_deadline_epoch - 300))"
if (( backup_reserved_deadline_epoch < relative_controller_deadline_epoch )); then
  controller_deadline_epoch="$backup_reserved_deadline_epoch"
else
  controller_deadline_epoch="$relative_controller_deadline_epoch"
fi
(( hard_deadline_epoch - started_epoch > 320 )) || { echo "insufficient provider time remains for qualification and backup" >&2; exit 45; }
printf '%s\n' "$controller_deadline_epoch" > "$evidence_dir/controller-deadline-epoch.txt"
printf '%s\n' "$hard_deadline_epoch" > "$evidence_dir/hard-stop-deadline-epoch.txt"
( sleep "$((hard_deadline_epoch - started_epoch - 10))"; shutdown -h now ) & watchdog_pid="$!"
remaining() { local value=$((controller_deadline_epoch - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
backup_remaining() { local value=$((hard_deadline_epoch - 20 - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
inventory_remaining() { local value=$((hard_deadline_epoch - 240 - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
phase_timeout() { local cap="$1" left; left="$(remaining)" || return 1; (( left < cap )) && printf '%s\n' "$left" || printf '%s\n' "$cap"; }
checkpoint() {
  local stamp; stamp="$(date -u +%Y%m%dT%H%M%S%NZ)-$$-$RANDOM"
  timeout "$(phase_timeout 240)" gcloud storage rsync "$evidence_dir" "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/runtime-checkpoints/$GANESH_ATTEMPT_ID/$stamp" --recursive --project="$GANESH_GCP_PROJECT" >> "$evidence_dir/gcs-backup.log" 2>&1 || true
}
final_backup() {
  timeout "$(backup_remaining)" gcloud storage rsync "$evidence_dir" "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/$terminal_prefix" --recursive --project="$GANESH_GCP_PROJECT" > /var/log/ganesh-runtime-final-backup.log 2>&1
}
inventory_attempted=0
write_inventory() {
  inventory_attempted=1
  local budget; budget="$(inventory_remaining)" || return 1
  timeout "$budget" bash -c 'set -o pipefail; cd "$1"; find . -type f ! -name runtime-files.sha256 ! -name .runtime-files.sha256.tmp -print0 | sort -z | xargs -0 sha256sum > .runtime-files.sha256.tmp && mv .runtime-files.sha256.tmp runtime-files.sha256' _ "$evidence_dir"
}
finish() { local status="$?"; trap - EXIT; printf '%s\n' "$status" > "$evidence_dir/startup-exit-code.txt"; if (( inventory_attempted == 0 )) && ! write_inventory; then rm -f "$evidence_dir/.runtime-files.sha256.tmp"; printf 'terminal inventory failed\n' > "$evidence_dir/terminal-inventory-failure.txt"; status=91; fi; final_backup || status=90; kill "$watchdog_pid" 2>/dev/null || true; exit "$status"; }
trap finish EXIT
download_verified() {
  local uri="$1" expected_sha="$2" expected_size="$3" destination="$4"
  timeout "$(remaining)" gcloud storage cp "$uri" "$destination" --project="$GANESH_GCP_PROJECT"
  [[ "$(stat -c %s "$destination")" == "$expected_size" ]]
  printf '%s  %s\n' "$expected_sha" "$destination" | timeout "$(phase_timeout 180)" sha256sum -c -
}
download_verified "$GANESH_WORKSPACE_ARCHIVE_URI" "$GANESH_WORKSPACE_ARCHIVE_SHA256" "$GANESH_WORKSPACE_ARCHIVE_SIZE" "$work_dir/workspace.tar.gz"
download_verified "$GANESH_MODEL_ARCHIVE_URI" "$GANESH_MODEL_ARCHIVE_SHA256" "$GANESH_MODEL_ARCHIVE_SIZE" "$work_dir/model.tar.gz"
download_verified "$GANESH_IMAGE_ARCHIVE_URI" "$GANESH_IMAGE_ARCHIVE_SHA256" "$GANESH_IMAGE_ARCHIVE_SIZE" "$work_dir/cuda-image.docker.tar.zst"
download_verified "$GANESH_DOCKER_BUNDLE_URI" "$GANESH_DOCKER_BUNDLE_SHA256" "$GANESH_DOCKER_BUNDLE_SIZE" "$work_dir/docker-bundle.tar.gz"
mkdir "$work_dir/workspace" "$work_dir/model" "$work_dir/docker-bundle"
timeout "$(phase_timeout 180)" tar -xzf "$work_dir/workspace.tar.gz" -C "$work_dir/workspace"
timeout "$(phase_timeout 300)" tar -xzf "$work_dir/model.tar.gz" -C "$work_dir/model"
timeout "$(phase_timeout 120)" tar -xzf "$work_dir/docker-bundle.tar.gz" -C "$work_dir/docker-bundle" --strip-components=1
timeout "$(phase_timeout 120)" bash -c 'cd "$1" && sha256sum -c bundle-files.sha256' _ "$work_dir/docker-bundle"
timeout "$(phase_timeout 30)" bash -c "set -o pipefail; dpkg-query -W -f='\${Package}\\t\${Version}\\n' | sort" > "$evidence_dir/base-dpkg-packages.tsv"
timeout "$(phase_timeout 30)" cmp "$evidence_dir/base-dpkg-packages.tsv" "$work_dir/docker-bundle/base-dpkg-packages.tsv"
timeout "$(phase_timeout 300)" dpkg -i "$work_dir"/docker-bundle/debs/*.deb > "$evidence_dir/docker-offline-install.log" 2>&1 || timeout "$(phase_timeout 300)" dpkg -i "$work_dir"/docker-bundle/debs/*.deb >> "$evidence_dir/docker-offline-install.log" 2>&1
timeout "$(phase_timeout 30)" dpkg --audit > "$evidence_dir/dpkg-audit.txt"; [[ ! -s "$evidence_dir/dpkg-audit.txt" ]]
timeout "$(phase_timeout 10)" bash -c 'command -v nvidia-ctk' > "$evidence_dir/nvidia-ctk-path.txt"
timeout "$(phase_timeout 30)" nvidia-ctk runtime configure --runtime=docker > "$evidence_dir/nvidia-ctk-configure.log" 2>&1
timeout "$(phase_timeout 30)" systemctl restart docker; timeout "$(phase_timeout 30)" bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done'
timeout "$(phase_timeout 300)" bash -c 'set -o pipefail; zstd -dc "$1" | docker load' _ "$work_dir/cuda-image.docker.tar.zst" > "$evidence_dir/docker-load.txt"
observed_image_id="$(timeout "$(phase_timeout 30)" docker image inspect --format '{{.Id}}' "$GANESH_CUDA_IMAGE_REF")"
printf '%s\n' "$observed_image_id" > "$evidence_dir/observed-image-id.txt"; [[ "$observed_image_id" == "$GANESH_CUDA_IMAGE_ID" ]]
timeout "$(phase_timeout 10)" uname -a > "$evidence_dir/uname.txt"
env | sed -E 's/(TOKEN|SECRET|PASSWORD|KEY)=.*/\1=REDACTED/' | sort > "$evidence_dir/environment-redacted.txt"
timeout "$(phase_timeout 30)" nvidia-smi -q > "$evidence_dir/nvidia-smi-q.txt"
timeout "$(phase_timeout 30)" nvidia-smi --query-gpu=timestamp,name,uuid,driver_version,memory.total --format=csv,noheader > "$evidence_dir/gpu-identity.csv"
timeout "$(phase_timeout 30)" docker version > "$evidence_dir/docker-version.txt" 2>&1; timeout "$(phase_timeout 30)" docker info > "$evidence_dir/docker-info.txt" 2>&1
timeout "$(phase_timeout 30)" bash -c "set -o pipefail; dpkg-query -W -f='\${Package}\\t\${Version}\\n' | sort" > "$evidence_dir/runtime-dpkg-packages.tsv"
timeout "$(phase_timeout 120)" bash -c 'set -o pipefail; find "$1" "$2" -type f -print0 | sort -z | xargs -0 sha256sum' _ "$work_dir/workspace" "$work_dir/model" > "$evidence_dir/extracted-inputs.sha256"
(
  while true; do nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used,memory.total,power.draw,temperature.gpu --format=csv,noheader,nounits >> "$evidence_dir/nvml-samples.csv"; sleep 5; done
) & nvml_pid="$!"
(
  while true; do checkpoint; sleep 30; done
) & backup_pid="$!"
set +e
GANESH_GPU_HOURLY_USD="$GANESH_GPU_HOURLY_USD" GANESH_CUMULATIVE_COST_USD="$GANESH_CUMULATIVE_COST_USD" GANESH_SUPPORT_RESERVE_USD="$GANESH_SUPPORT_RESERVE_USD" GANESH_CONTROLLER_DEADLINE_EPOCH="$controller_deadline_epoch" GANESH_CUDA_IMAGE_REF="$GANESH_CUDA_IMAGE_REF" GANESH_CUDA_IMAGE_ID="$GANESH_CUDA_IMAGE_ID" GANESH_ATTEMPT_ID="$GANESH_ATTEMPT_ID" \
  "$work_dir/workspace/scripts/cuda/run_qualification.sh" "$work_dir/model" "$work_dir/workspace/data/seed/ganesh_v01/train.jsonl" "$output_dir" bf16-lora-primary-v1 > >(tee "$evidence_dir/controller.stdout.log") 2> >(tee "$evidence_dir/controller.stderr.log" >&2)
run_status="$?"; set -e
kill "$nvml_pid" "$backup_pid" 2>/dev/null || true; wait "$nvml_pid" "$backup_pid" 2>/dev/null || true
printf '%s\n' "$run_status" > "$evidence_dir/controller-exit-code.txt"
printf '%s\n' "$run_status" > "$evidence_dir/startup-exit-code.txt"
if ! write_inventory; then
  rm -f "$evidence_dir/.runtime-files.sha256.tmp"
  printf 'terminal inventory failed\n' > "$evidence_dir/terminal-inventory-failure.txt"
  exit 91
fi
final_backup
trap - EXIT; kill "$watchdog_pid" 2>/dev/null || true
exit "$run_status"
