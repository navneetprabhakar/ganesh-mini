#!/usr/bin/env bash
set -Eeuo pipefail

project="executespecv1"
bucket="ganesh-gate0-model-transfer-1061994342941"
prefix="ganesh-mini-1.0/gate0b/20260822T155636Z"
work_dir="/opt/ganesh-mini-gate0b"
evidence_dir="/var/lib/ganesh-mini-gate0b"
output_dir="$evidence_dir/output"
mkdir -p "$work_dir" "$output_dir"
exec > >(tee -a "$evidence_dir/startup.stdout.log") \
  2> >(tee -a "$evidence_dir/startup.stderr.log" >&2)

backup() {
  stamp="$(date -u +%Y%m%dT%H%M%S%NZ)-$$-$RANDOM"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$evidence_dir/last-backup-at.txt"
  gcloud storage rsync "$evidence_dir" "gs://$bucket/$prefix/runtime-checkpoints/$stamp" \
    --recursive --project="$project" >> "$evidence_dir/gcs-backup.log" 2>&1 || true
}
finish() {
  status="$?"
  printf '%s\n' "$status" > "$evidence_dir/startup-exit-code.txt"
  backup
  exit "$status"
}
trap finish EXIT

started_epoch="$(date +%s)"
hard_deadline_epoch="$((started_epoch + 1700))"
controller_deadline_epoch="$((started_epoch + 1400))"
date -u +%Y-%m-%dT%H:%M:%SZ > "$evidence_dir/vm-run-started-at.txt"
printf '%s\n' "$started_epoch" > "$evidence_dir/vm-started-epoch.txt"
printf '%s\n' "$controller_deadline_epoch" > "$evidence_dir/controller-deadline-epoch.txt"
printf '%s\n' "$hard_deadline_epoch" > "$evidence_dir/hard-stop-deadline-epoch.txt"

# The pinned CUDA DLVM image carries the NVIDIA driver/tooling but not Docker.
# Resolve no floating Docker version: install the exact Jammy update package
# recorded in the run plan and capture both APT policy and installed packages.
docker_package_version="29.1.3-0ubuntu3~22.04.2"
printf '%s\n' "$docker_package_version" > "$evidence_dir/requested-docker-package-version.txt"
apt-get update > "$evidence_dir/apt-update.log" 2>&1
apt-cache policy docker.io > "$evidence_dir/docker-apt-policy.txt"
if ! grep -Fq "$docker_package_version" "$evidence_dir/docker-apt-policy.txt"; then
  echo "pinned docker.io package is unavailable: $docker_package_version" >&2
  exit 41
fi
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  "docker.io=$docker_package_version" > "$evidence_dir/docker-install.log" 2>&1
dpkg-query -W -f='${Package}\t${Version}\n' docker.io containerd runc \
  > "$evidence_dir/docker-package-versions.tsv"
if ! command -v nvidia-ctk > "$evidence_dir/nvidia-ctk-path.txt"; then
  echo "pinned DLVM image does not expose nvidia-ctk" >&2
  exit 42
fi
nvidia-ctk runtime configure --runtime=docker \
  > "$evidence_dir/nvidia-ctk-configure.log" 2>&1
systemctl restart docker
timeout 30s bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done'

uname -a > "$evidence_dir/uname.txt"
env | sed -E 's/(TOKEN|SECRET|PASSWORD|KEY)=.*/\1=REDACTED/' | sort > "$evidence_dir/environment-redacted.txt"
nvidia-smi -q > "$evidence_dir/nvidia-smi-q.txt"
nvidia-smi --query-gpu=timestamp,name,uuid,driver_version,memory.total --format=csv,noheader > "$evidence_dir/gpu-identity.csv"
docker version > "$evidence_dir/docker-version.txt" 2>&1
docker info > "$evidence_dir/docker-info.txt" 2>&1

gcloud storage rsync "gs://$bucket/$prefix/input/workspace" "$work_dir/workspace" --recursive --project="$project"
gcloud storage rsync "gs://$bucket/$prefix/input/model" "$work_dir/model" --recursive --project="$project"
chmod +x "$work_dir/workspace/scripts/cuda/run_qualification.sh"
find "$work_dir" -type f -print0 | sort -z | xargs -0 sha256sum > "$evidence_dir/downloaded-inputs.sha256"

(
  while true; do
    nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used,memory.total,power.draw,temperature.gpu --format=csv,noheader,nounits >> "$evidence_dir/nvml-samples.csv"
    sleep 5
  done
) &
nvml_pid="$!"
(
  while true; do backup; sleep 30; done
) &
backup_pid="$!"

set +e
GANESH_GPU_HOURLY_USD=2.12081 \
GANESH_CONTROLLER_DEADLINE_EPOCH="$controller_deadline_epoch" \
  "$work_dir/workspace/scripts/cuda/run_qualification.sh" \
  "$work_dir/model" \
  "$work_dir/workspace/data/seed/ganesh_v01/train.jsonl" \
  "$output_dir" \
  bf16-lora-primary-v1 \
  > >(tee "$evidence_dir/controller.stdout.log") \
  2> >(tee "$evidence_dir/controller.stderr.log" >&2)
run_status="$?"
set -e
kill "$nvml_pid" "$backup_pid" 2>/dev/null || true
wait "$nvml_pid" "$backup_pid" 2>/dev/null || true
printf '%s\n' "$run_status" > "$evidence_dir/controller-exit-code.txt"
find "$evidence_dir" -type f -print0 | sort -z | xargs -0 sha256sum > "$evidence_dir/runtime-files.sha256"
backup
exit "$run_status"
