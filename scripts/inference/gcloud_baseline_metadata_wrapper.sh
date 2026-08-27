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
  [GANESH_WORKSPACE_MANIFEST_URI]=ganesh-workspace-manifest-uri
  [GANESH_WORKSPACE_MANIFEST_SHA256]=ganesh-workspace-manifest-sha256
  [GANESH_WORKSPACE_MANIFEST_SIZE]=ganesh-workspace-manifest-size
  [GANESH_TRAIN_WORKSPACE_ARCHIVE_URI]=ganesh-training-workspace-archive-uri
  [GANESH_TRAIN_WORKSPACE_ARCHIVE_SHA256]=ganesh-training-workspace-archive-sha256
  [GANESH_TRAIN_WORKSPACE_ARCHIVE_SIZE]=ganesh-training-workspace-archive-size
  [GANESH_TRAIN_WORKSPACE_MANIFEST_URI]=ganesh-training-workspace-manifest-uri
  [GANESH_TRAIN_WORKSPACE_MANIFEST_SHA256]=ganesh-training-workspace-manifest-sha256
  [GANESH_TRAIN_WORKSPACE_MANIFEST_SIZE]=ganesh-training-workspace-manifest-size
  [GANESH_GATE0_REPORT_URI]=ganesh-gate0-report-uri
  [GANESH_GATE0_REPORT_SHA256]=ganesh-gate0-report-sha256
  [GANESH_GATE0_REPORT_SIZE]=ganesh-gate0-report-size
  [GANESH_GATE1_REPORT_URI]=ganesh-gate1-report-uri
  [GANESH_GATE1_REPORT_SHA256]=ganesh-gate1-report-sha256
  [GANESH_GATE1_REPORT_SIZE]=ganesh-gate1-report-size
  [GANESH_GATE2_REPORT_URI]=ganesh-gate2-report-uri
  [GANESH_GATE2_REPORT_SHA256]=ganesh-gate2-report-sha256
  [GANESH_GATE2_REPORT_SIZE]=ganesh-gate2-report-size
  [GANESH_MODEL_ARCHIVE_URI]=ganesh-model-archive-uri
  [GANESH_MODEL_ARCHIVE_SHA256]=ganesh-model-archive-sha256
  [GANESH_MODEL_ARCHIVE_SIZE]=ganesh-model-archive-size
  [GANESH_IMAGE_ARCHIVE_URI]=ganesh-image-archive-uri
  [GANESH_IMAGE_ARCHIVE_SHA256]=ganesh-image-archive-sha256
  [GANESH_IMAGE_ARCHIVE_SIZE]=ganesh-image-archive-size
  [GANESH_DOCKER_BUNDLE_URI]=ganesh-docker-bundle-uri
  [GANESH_DOCKER_BUNDLE_SHA256]=ganesh-docker-bundle-sha256
  [GANESH_DOCKER_BUNDLE_SIZE]=ganesh-docker-bundle-size
  [GANESH_VERIFIER_ARCHIVE_URI]=ganesh-verifier-archive-uri
  [GANESH_VERIFIER_ARCHIVE_SHA256]=ganesh-verifier-archive-sha256
  [GANESH_VERIFIER_ARCHIVE_SIZE]=ganesh-verifier-archive-size
  [GANESH_VERIFIER_MANIFEST_URI]=ganesh-verifier-manifest-uri
  [GANESH_VERIFIER_MANIFEST_SHA256]=ganesh-verifier-manifest-sha256
  [GANESH_VERIFIER_MANIFEST_SIZE]=ganesh-verifier-manifest-size
  [GANESH_CUDA_IMAGE_ID]=ganesh-cuda-image-id
  [GANESH_CUDA_IMAGE_REF]=ganesh-cuda-image-ref
  [GANESH_ATTEMPT_ID]=ganesh-attempt-id
  [GANESH_GPU_HOURLY_USD]=ganesh-gpu-hourly-usd
  [GANESH_SUPPORT_RESERVE_USD]=ganesh-support-reserve-usd
  [GANESH_ABSOLUTE_COST_CEILING_USD]=ganesh-absolute-cost-ceiling-usd
  [GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH]=ganesh-absolute-hard-deadline-epoch
  [GANESH_MAX_VM_LIFETIME_SECONDS]=ganesh-max-vm-lifetime-seconds
  [GANESH_CONTROLLER_BUDGET_SECONDS]=ganesh-controller-budget-seconds
  [GANESH_BACKUP_RESERVE_SECONDS]=ganesh-backup-reserve-seconds
  [GANESH_EXPECTED_MACHINE_TYPE]=ganesh-expected-machine-type
  [GANESH_EXECUTION_CARD_URI]=ganesh-execution-card-uri
  [GANESH_EXECUTION_CARD_SHA256]=ganesh-execution-card-sha256
  [GANESH_EXECUTION_CARD_SIZE]=ganesh-execution-card-size
  [GANESH_EXECUTION_CARD_INTERNAL_SHA256]=ganesh-execution-card-internal-sha256
  [GANESH_CONTROLLER_URI]=ganesh-controller-uri
  [GANESH_CONTROLLER_SHA256]=ganesh-controller-sha256
  [GANESH_CONTROLLER_SIZE]=ganesh-controller-size
  [GANESH_METADATA_WRAPPER_URI]=ganesh-metadata-wrapper-uri
  [GANESH_METADATA_WRAPPER_SHA256]=ganesh-metadata-wrapper-sha256
  [GANESH_METADATA_WRAPPER_SIZE]=ganesh-metadata-wrapper-size
)
for variable in "${!bindings[@]}"; do
  printf -v "$variable" '%s' "$(read_metadata "${bindings[$variable]}")"
  export "$variable"
done
[[ "$(stat -c %s "$0")" == "$GANESH_METADATA_WRAPPER_SIZE" ]]
printf '%s  %s\n' "$GANESH_METADATA_WRAPPER_SHA256" "$0" | sha256sum -c -

case "$GANESH_CONTROLLER_URI" in *'#'[0-9]*) ;; *) echo "controller URI must include a GCS generation" >&2; exit 40;; esac
case "$GANESH_METADATA_WRAPPER_URI" in *'#'[0-9]*) ;; *) echo "metadata wrapper URI must include a GCS generation" >&2; exit 40;; esac
controller=/opt/ganesh-gcloud-development-baseline.sh
timeout 120 gcloud storage cp "$GANESH_CONTROLLER_URI" "$controller" --project="$GANESH_GCP_PROJECT"
[[ "$(stat -c %s "$controller")" == "$GANESH_CONTROLLER_SIZE" ]]
printf '%s  %s\n' "$GANESH_CONTROLLER_SHA256" "$controller" | sha256sum -c -
chmod 700 "$controller"
wrapper_dir=/var/lib/ganesh-mini-gate1-wrapper
mkdir -p "$wrapper_dir"
set +e
"$controller" > >(tee "$wrapper_dir/controller.stdout.log") 2> >(tee "$wrapper_dir/controller.stderr.log" >&2)
controller_status="$?"
set -e
if (( controller_status != 0 )); then
  printf '%s\n' "$controller_status" > "$wrapper_dir/controller-exit-code.txt"
  sha256sum "$0" "$controller" > "$wrapper_dir/bootstrap-files.sha256"
  terminal_prefix="gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/runtime-terminal-$GANESH_ATTEMPT_ID"
  if [[ -d /var/lib/ganesh-mini-gate1 ]]; then
    for attempt in 1 2 3; do
      gcloud storage rsync /var/lib/ganesh-mini-gate1 "$terminal_prefix" --recursive --project="$GANESH_GCP_PROJECT" && break
      if (( attempt < 3 )); then sleep 10; fi
    done
  fi
  wrapper_prefix="gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/wrapper-failure-$GANESH_ATTEMPT_ID"
  wrapper_backed=0
  for attempt in 1 2 3; do
    if gcloud storage rsync "$wrapper_dir" "$wrapper_prefix" --recursive --project="$GANESH_GCP_PROJECT"; then wrapper_backed=1; break; fi
    if (( attempt < 3 )); then sleep 10; fi
  done
  (( wrapper_backed == 1 )) || exit 92
else
  rm -rf "$wrapper_dir"
fi
( sleep 2; shutdown -h now ) >/dev/null 2>&1 &
exit "$controller_status"
