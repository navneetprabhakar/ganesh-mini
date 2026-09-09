#!/usr/bin/env bash
set -Eeuo pipefail

metadata_root=http://metadata.google.internal/computeMetadata/v1/instance/attributes
read_metadata() { curl -fsS --retry 3 --retry-delay 1 -H 'Metadata-Flavor: Google' "$metadata_root/$1"; }

project=$(read_metadata ganesh-gcp-project)
bucket=$(read_metadata ganesh-gcs-bucket)
prefix=$(read_metadata ganesh-gcs-prefix)
attempt_id=$(read_metadata ganesh-attempt-id)
card_uri=$(read_metadata ganesh-execution-card-uri)
card_sha=$(read_metadata ganesh-execution-card-sha256)
card_size=$(read_metadata ganesh-execution-card-size)
controller_uri=$(read_metadata ganesh-controller-uri)
controller_sha=$(read_metadata ganesh-controller-sha256)
controller_size=$(read_metadata ganesh-controller-size)
wrapper_sha=$(read_metadata ganesh-wrapper-sha256)
wrapper_size=$(read_metadata ganesh-wrapper-size)

for uri in "$card_uri" "$controller_uri"; do case "$uri" in *'#'[0-9]*) ;; *) echo "launch URI must include a GCS generation" >&2; exit 40;; esac; done
[[ "$(stat -c %s "$0")" == "$wrapper_size" ]]
printf '%s  %s\n' "$wrapper_sha" "$0" | sha256sum -c -
wrapper_dir=/var/lib/ganesh-mini-checkpoint-sweep-wrapper
mkdir -p "$wrapper_dir"
exec > >(tee -a "$wrapper_dir/wrapper.stdout.log") 2> >(tee -a "$wrapper_dir/wrapper.stderr.log" >&2)
download() { timeout 300 gcloud storage cp "$1" "$4" --project="$project"; [[ "$(stat -c %s "$4")" == "$3" ]]; printf '%s  %s\n' "$2" "$4" | sha256sum -c -; }
card=/opt/ganesh-checkpoint-sweep-execution.json
controller=/opt/ganesh-checkpoint-sweep-controller.sh
download "$card_uri" "$card_sha" "$card_size" "$card"
download "$controller_uri" "$controller_sha" "$controller_size" "$controller"
chmod 700 "$controller"
sha256sum "$0" "$controller" "$card" > "$wrapper_dir/bootstrap-files.sha256"
set +e
"$controller" "$card" "$project" "$bucket" "$prefix" "$attempt_id"
status=$?
set -e
printf '%s\n' "$status" > "$wrapper_dir/controller-exit-code.txt"
if (( status != 0 )); then
  timeout 300 gcloud storage rsync "$wrapper_dir" "gs://$bucket/$prefix/wrapper-failure-$attempt_id" --recursive --project="$project" || true
fi
( sleep 2; shutdown -h now ) >/dev/null 2>&1 &
exit "$status"
