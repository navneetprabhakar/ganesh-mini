#!/usr/bin/env bash
set -Eeuo pipefail

project_id="executespecv1"
zone="us-east1-c"
region="us-east1"
instance_name="ganesh-mini-g4-sweep-20260909t130347z"
disk_name="ganesh-mini-g4-sweep-20260909t130347z"
subnet_name="ganesh-mini-g4-sweep-subnet-20260909t130347z"
network_name="ganesh-mini-g4-sweep-net-20260909t130347z"
attempt_dir="measurement/gate4/checkpoint-sweep-20260909/attempts/20260909T130347Z"
access_token="$(gcloud auth print-access-token)"

capture() {
  local url="$1"
  local body_path="$2"
  local code_path="$3"
  curl --silent --show-error \
    -H "Authorization: Bearer ${access_token}" \
    -o "${body_path}" \
    -w '%{http_code}\n' \
    "${url}" >"${code_path}"
}

audit_pass() {
  local pass_name="$1"
  local pass_dir="${attempt_dir}/provider/${pass_name}"
  mkdir -p "${pass_dir}"
  date -u '+%Y-%m-%dT%H:%M:%SZ' >"${pass_dir}/checked-at.txt"

  capture \
    "https://compute.googleapis.com/compute/v1/projects/${project_id}/zones/${zone}/instances/${instance_name}" \
    "${pass_dir}/target-instance.json" "${pass_dir}/target-instance.http"
  capture \
    "https://compute.googleapis.com/compute/v1/projects/${project_id}/zones/${zone}/disks/${disk_name}" \
    "${pass_dir}/target-disk.json" "${pass_dir}/target-disk.http"
  capture \
    "https://compute.googleapis.com/compute/v1/projects/${project_id}/regions/${region}/subnetworks/${subnet_name}" \
    "${pass_dir}/target-subnet.json" "${pass_dir}/target-subnet.http"
  capture \
    "https://compute.googleapis.com/compute/v1/projects/${project_id}/global/networks/${network_name}" \
    "${pass_dir}/target-network.json" "${pass_dir}/target-network.http"

  local resource_kind
  for resource_kind in instances disks addresses forwardingRules routers reservations subnetworks; do
    capture \
      "https://compute.googleapis.com/compute/v1/projects/${project_id}/aggregated/${resource_kind}" \
      "${pass_dir}/inventory-${resource_kind}.json" "${pass_dir}/inventory-${resource_kind}.http"
  done
  for resource_kind in snapshots images machineImages networks; do
    capture \
      "https://compute.googleapis.com/compute/v1/projects/${project_id}/global/${resource_kind}" \
      "${pass_dir}/inventory-${resource_kind}.json" "${pass_dir}/inventory-${resource_kind}.http"
  done

  grep -qx '404' "${pass_dir}/target-instance.http"
  grep -qx '404' "${pass_dir}/target-disk.http"
  grep -qx '404' "${pass_dir}/target-subnet.http"
  grep -qx '404' "${pass_dir}/target-network.http"
}

audit_pass "absence-1"
sleep 12
audit_pass "absence-2"
printf 'two_pass_absence=true\n'
