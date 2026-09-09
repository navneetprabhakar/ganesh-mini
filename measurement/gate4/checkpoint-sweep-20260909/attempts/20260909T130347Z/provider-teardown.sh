#!/usr/bin/env bash
set -Eeuo pipefail

project_id="executespecv1"
region="us-east1"
network_name="ganesh-mini-g4-sweep-net-20260909t130347z"
subnet_name="ganesh-mini-g4-sweep-subnet-20260909t130347z"
attempt_dir="measurement/gate4/checkpoint-sweep-20260909/attempts/20260909T130347Z"

access_token="$(gcloud auth print-access-token)"

delete_and_wait() {
  local resource_url="$1"
  local operation_scope_url="$2"
  local output_stem="$3"
  curl --fail --silent --show-error -X DELETE \
    -H "Authorization: Bearer ${access_token}" \
    "${resource_url}" \
    -o "${attempt_dir}/provider/${output_stem}-operation.json"
  local operation_name
  operation_name="$(jq -r '.name' "${attempt_dir}/provider/${output_stem}-operation.json")"
  local operation_state="PENDING"
  local poll_index
  for poll_index in 1 2 3 4 5 6 7 8 9 10 11 12; do
    curl --fail --silent --show-error \
      -H "Authorization: Bearer ${access_token}" \
      "${operation_scope_url}/${operation_name}" \
      -o "${attempt_dir}/provider/${output_stem}-status.json"
    operation_state="$(jq -r '.status' "${attempt_dir}/provider/${output_stem}-status.json")"
    if [[ "${operation_state}" == "DONE" ]]; then
      break
    fi
    sleep 5
  done
  [[ "${operation_state}" == "DONE" ]]
  jq -e '.error == null' "${attempt_dir}/provider/${output_stem}-status.json" >/dev/null
}

delete_and_wait \
  "https://compute.googleapis.com/compute/v1/projects/${project_id}/regions/${region}/subnetworks/${subnet_name}" \
  "https://compute.googleapis.com/compute/v1/projects/${project_id}/regions/${region}/operations" \
  "subnet-delete"

delete_and_wait \
  "https://compute.googleapis.com/compute/v1/projects/${project_id}/global/networks/${network_name}" \
  "https://compute.googleapis.com/compute/v1/projects/${project_id}/global/operations" \
  "network-delete"

printf 'subnet_and_network_deleted=true\n'
