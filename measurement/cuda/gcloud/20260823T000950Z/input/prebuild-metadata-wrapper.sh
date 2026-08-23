#!/usr/bin/env bash
set -Eeuo pipefail

export GANESH_GCP_PROJECT="executespecv1"
export GANESH_GCS_BUCKET="ganesh-gate0-model-transfer-1061994342941"
export GANESH_GCS_PREFIX="ganesh-mini-1.0/gate0b/20260823T000950Z"
export GANESH_WORKSPACE_ARCHIVE_URI="gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/gate0b/20260823T000950Z/input/workspace.tar.gz#1787443867923167"
export GANESH_WORKSPACE_ARCHIVE_SHA256="825c10edaa25666c44649126ee60b0d1cd24e95e807cd6ccc17b0d06e56d37e2"
export GANESH_WORKSPACE_ARCHIVE_SIZE="2663016"
export GANESH_CUMULATIVE_COST_USD="2.506167860"
export GANESH_BUILDER_HOURLY_USD="0.268"
export GANESH_SUPPORT_RESERVE_USD="0.25"

controller_uri="gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/gate0b/20260823T000950Z/input/gcloud_prebuild_gate0b.sh#1787443902265773"
controller_sha256="ecd393eb8c224ae833659efa05c6c86f3e02bdbb302de75540f326e2ecc6effa"
controller="/opt/ganesh-gcloud-prebuild-gate0b.sh"

timeout 120 gcloud storage cp "$controller_uri" "$controller" --project="$GANESH_GCP_PROJECT"
printf '%s  %s\n' "$controller_sha256" "$controller" | sha256sum -c -
chmod 700 "$controller"
exec "$controller"
