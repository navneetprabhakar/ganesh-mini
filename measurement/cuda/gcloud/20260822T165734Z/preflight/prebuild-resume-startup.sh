#!/usr/bin/env bash
set -Eeuo pipefail
export GANESH_GCP_PROJECT=executespecv1
export GANESH_GCS_BUCKET=ganesh-gate0-model-transfer-1061994342941
export GANESH_GCS_PREFIX=ganesh-mini-1.0/gate0b/20260822T165734Z
export GANESH_CUDA_IMAGE_ID=sha256:37b7cbcb8280d469bad6213bf09bfa0ccb2dba96a912aaa105183069c2ce5351
export GANESH_CUDA_IMAGE_REF=ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1
export GANESH_PRIOR_BACKUP_MANIFEST_URI='gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/gate0b/20260822T165734Z/preflight/prebuild-failed-backup-manifest.json#1787422414260208'
export GANESH_PRIOR_BACKUP_MANIFEST_SHA256=50dc81dcfc784fc2e184c3eac87a68257f70a45f95848091524f3dfc42d4ef9c
export GANESH_SERIAL_RECOVERY_MANIFEST_URI='gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/gate0b/20260822T165734Z/preflight/serial-recovery-backup-manifest.json#1787428476414591'
export GANESH_SERIAL_RECOVERY_MANIFEST_SHA256=35c287c98c5fac33cf9125e8366d338af6aac8fbf81e74fafea31c57b8f2704b
export GANESH_SERIAL_RECOVERY_FINDING_SHA256=39d7ed06df7ce29ed4f98ade84dded5b3ad31255ea975a03a0f6d1049b21a0f9
export GANESH_WORKSPACE_ARCHIVE_URI='gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/gate0b/20260822T165734Z/input/workspace.tar.gz#1787418239797386'
export GANESH_WORKSPACE_ARCHIVE_SHA256=b940bcea2dad4e0318a6f77ca8ec6b299985d783d56d0e614ff8925932a84a12
export GANESH_WORKSPACE_GIT_COMMIT=df8fd6e
export GANESH_BUILD_INPUTS_SHA256=7a8405dd4631e198aae660c40f28eb65b18b344556386c3d752f13e74195dbfc
export GANESH_RESOURCE_NAME=ganesh-mini-prebuild-20260822t165734z
export GANESH_RESOURCE_ID=8798900559452333835
export GANESH_CUMULATIVE_COST_USD=1.080706193
export GANESH_RESUME_COMPUTE_UPPER_USD=0.134
export GANESH_SUPPORT_RESERVE_USD=0.25

resume_script=/opt/ganesh-mini-resume-prebuild.sh
gcloud storage cp 'gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/gate0b/20260822T165734Z/preflight/gcloud-resume-prebuild-gate0b.sh#1787428580977375' "$resume_script" --project=executespecv1 >/var/log/ganesh-resume-script-download.log 2>&1
printf '%s  %s\n' be5963874b0c77a1fa9da0abca113cf1b27fe5621fedd049f3ce5feafa5b586c "$resume_script" | sha256sum -c -
chmod 0755 "$resume_script"
exec "$resume_script"
