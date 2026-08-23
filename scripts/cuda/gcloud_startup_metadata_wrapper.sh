#!/usr/bin/env bash
set -Eeuo pipefail

metadata_root="http://metadata.google.internal/computeMetadata/v1/instance/attributes"
read_metadata() {
  curl -fsS --retry 3 --retry-delay 1 -H 'Metadata-Flavor: Google' "$metadata_root/$1"
}

declare -A bindings=(
  [GANESH_GCP_PROJECT]=ganesh-gcp-project
  [GANESH_GCS_BUCKET]=ganesh-gcs-bucket
  [GANESH_GCS_PREFIX]=ganesh-gcs-prefix
  [GANESH_WORKSPACE_ARCHIVE_URI]=ganesh-workspace-archive-uri
  [GANESH_WORKSPACE_ARCHIVE_SHA256]=ganesh-workspace-archive-sha256
  [GANESH_WORKSPACE_ARCHIVE_SIZE]=ganesh-workspace-archive-size
  [GANESH_MODEL_ARCHIVE_URI]=ganesh-model-archive-uri
  [GANESH_MODEL_ARCHIVE_SHA256]=ganesh-model-archive-sha256
  [GANESH_MODEL_ARCHIVE_SIZE]=ganesh-model-archive-size
  [GANESH_IMAGE_ARCHIVE_URI]=ganesh-image-archive-uri
  [GANESH_IMAGE_ARCHIVE_SHA256]=ganesh-image-archive-sha256
  [GANESH_IMAGE_ARCHIVE_SIZE]=ganesh-image-archive-size
  [GANESH_DOCKER_BUNDLE_URI]=ganesh-docker-bundle-uri
  [GANESH_DOCKER_BUNDLE_SHA256]=ganesh-docker-bundle-sha256
  [GANESH_DOCKER_BUNDLE_SIZE]=ganesh-docker-bundle-size
  [GANESH_CUDA_IMAGE_ID]=ganesh-cuda-image-id
  [GANESH_CUDA_IMAGE_REF]=ganesh-cuda-image-ref
  [GANESH_ATTEMPT_ID]=ganesh-attempt-id
  [GANESH_GPU_HOURLY_USD]=ganesh-gpu-hourly-usd
  [GANESH_CUMULATIVE_COST_USD]=ganesh-cumulative-cost-usd
  [GANESH_SUPPORT_RESERVE_USD]=ganesh-support-reserve-usd
  [GANESH_ABSOLUTE_CUMULATIVE_CEILING_USD]=ganesh-absolute-cumulative-ceiling-usd
  [GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH]=ganesh-absolute-hard-deadline-epoch
  [GANESH_MAX_VM_LIFETIME_SECONDS]=ganesh-max-vm-lifetime-seconds
  [GANESH_CONTROLLER_BUDGET_SECONDS]=ganesh-controller-budget-seconds
  [GANESH_BACKUP_RESERVE_SECONDS]=ganesh-backup-reserve-seconds
  [GANESH_EXPECTED_MACHINE_TYPE]=ganesh-expected-machine-type
  [GANESH_EXECUTION_CARD_URI]=ganesh-execution-card-uri
  [GANESH_EXECUTION_CARD_SHA256]=ganesh-execution-card-sha256
  [GANESH_EXECUTION_CARD_SIZE]=ganesh-execution-card-size
)
for variable in "${!bindings[@]}"; do
  printf -v "$variable" '%s' "$(read_metadata "${bindings[$variable]}")"
  export "$variable"
done

controller_uri="$(read_metadata ganesh-controller-uri)"
controller_sha256="$(read_metadata ganesh-controller-sha256)"
case "$controller_uri" in *'#'[0-9]*) ;; *) echo "controller URI must include a GCS generation" >&2; exit 40;; esac
controller=/opt/ganesh-gcloud-startup-gate0b.sh
timeout 120 gcloud storage cp "$controller_uri" "$controller" --project="$GANESH_GCP_PROJECT"
printf '%s  %s\n' "$controller_sha256" "$controller" | sha256sum -c -
chmod 700 "$controller"
exec "$controller"
