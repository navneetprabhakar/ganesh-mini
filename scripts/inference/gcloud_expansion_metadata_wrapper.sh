#!/usr/bin/env bash
set -Eeuo pipefail

metadata_root=http://metadata.google.internal/computeMetadata/v1/instance/attributes
read_metadata() { curl -fsS --retry 3 --retry-delay 1 -H 'Metadata-Flavor: Google' "$metadata_root/$1"; }

GANESH_GCP_PROJECT=$(read_metadata ganesh-gcp-project)
GANESH_GCS_BUCKET=$(read_metadata ganesh-gcs-bucket)
GANESH_GCS_PREFIX=$(read_metadata ganesh-gcs-prefix)
GANESH_ATTEMPT_ID=$(read_metadata ganesh-attempt-id)
GANESH_EXECUTION_CARD_URI=$(read_metadata ganesh-execution-card-uri)
GANESH_EXECUTION_CARD_SHA256=$(read_metadata ganesh-execution-card-sha256)
GANESH_EXECUTION_CARD_SIZE=$(read_metadata ganesh-execution-card-size)
GANESH_CONTROLLER_URI=$(read_metadata ganesh-controller-uri)
GANESH_CONTROLLER_SHA256=$(read_metadata ganesh-controller-sha256)
GANESH_CONTROLLER_SIZE=$(read_metadata ganesh-controller-size)
GANESH_WRAPPER_SHA256=$(read_metadata ganesh-wrapper-sha256)
GANESH_WRAPPER_SIZE=$(read_metadata ganesh-wrapper-size)

for uri in "$GANESH_EXECUTION_CARD_URI" "$GANESH_CONTROLLER_URI"; do
  case "$uri" in *'#'[0-9]*) ;; *) echo "launch URI must include a GCS generation" >&2; exit 40;; esac
done
[[ "$(stat -c %s "$0")" == "$GANESH_WRAPPER_SIZE" ]]
echo "$GANESH_WRAPPER_SHA256  $0" | sha256sum -c -

wrapper_dir=/var/lib/ganesh-mini-gate4-wrapper
mkdir -p "$wrapper_dir"
exec > >(tee -a "$wrapper_dir/wrapper.stdout.log") 2> >(tee -a "$wrapper_dir/wrapper.stderr.log" >&2)
controller=/opt/ganesh-gcloud-expansion-pilot.sh
execution_card=/opt/ganesh-gate4-execution-card.json

download_verified() {
  local uri=$1 expected_sha=$2 expected_size=$3 destination=$4
  timeout 300 gcloud storage cp "$uri" "$destination" --project="$GANESH_GCP_PROJECT"
  [[ "$(stat -c %s "$destination")" == "$expected_size" ]]
  echo "$expected_sha  $destination" | sha256sum -c -
}
download_verified "$GANESH_EXECUTION_CARD_URI" "$GANESH_EXECUTION_CARD_SHA256" "$GANESH_EXECUTION_CARD_SIZE" "$execution_card"
download_verified "$GANESH_CONTROLLER_URI" "$GANESH_CONTROLLER_SHA256" "$GANESH_CONTROLLER_SIZE" "$controller"
chmod 700 "$controller"
sha256sum "$0" "$controller" "$execution_card" > "$wrapper_dir/bootstrap-files.sha256"

set +e
"$controller" "$execution_card"
controller_status=$?
set -e
echo "$controller_status" > "$wrapper_dir/controller-exit-code.txt"
if (( controller_status != 0 )); then
  wrapper_prefix="gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/wrapper-failure-$GANESH_ATTEMPT_ID"
  for attempt in 1 2 3; do
    gcloud storage rsync "$wrapper_dir" "$wrapper_prefix" --recursive --project="$GANESH_GCP_PROJECT" && break
    (( attempt == 3 )) || sleep 10
  done
fi
( sleep 2; shutdown -h now ) >/dev/null 2>&1 &
exit "$controller_status"
