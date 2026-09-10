#!/usr/bin/env bash
set -Eeuo pipefail

project=executespecv1
region=us-east1
zone=us-east1-c
instance=ganesh-mini-g4-v3-sweep-20260910t150000z
network=ganesh-mini-g4-v3-sweep-20260910t150000z-net
subnet=ganesh-mini-g4-v3-sweep-20260910t150000z-subnet
attempt_dir=measurement/gate4/lane-stratified-probe-checkpoint-sweep-20260910/attempts/20260910T150000Z

gcloud compute networks create "$network" \
  --project="$project" --subnet-mode=custom --bgp-routing-mode=regional \
  --format=json >"$attempt_dir/provider/network-create.json"

gcloud compute networks subnets create "$subnet" \
  --project="$project" --region="$region" --network="$network" \
  --range=10.93.0.0/28 --enable-private-ip-google-access \
  --format=json >"$attempt_dir/provider/subnet-create.json"

gcloud compute instances create "$instance" \
  --project="$project" \
  --zone="$zone" \
  --machine-type=g2-standard-8 \
  --provisioning-model=STANDARD \
  --maintenance-policy=TERMINATE \
  --no-restart-on-failure \
  --max-run-duration=7200s \
  --instance-termination-action=DELETE \
  --network="$network" \
  --subnet="$subnet" \
  --no-address \
  --image=common-cu129-ubuntu-2204-nvidia-580-v20260831 \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=200GB \
  --boot-disk-type=pd-balanced \
  --boot-disk-device-name="$instance" \
  --boot-disk-auto-delete \
  --service-account=1061994342941-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --metadata-from-file=startup-script=scripts/inference/gcloud_checkpoint_sweep_metadata_wrapper.sh \
  --metadata=ganesh-gcp-project=executespecv1,ganesh-gcs-bucket=ganesh-gate0-model-transfer-1061994342941,ganesh-gcs-prefix=ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/attempts/20260910T150000Z,ganesh-attempt-id=20260910T150000Z,ganesh-execution-card-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/attempts/20260910T150000Z/control/execution-card.json#1789061252857373,ganesh-execution-card-sha256=b6b8072d8e1e914b65b8490f22bb590a2486c00ce932c60775907f158e409e41,ganesh-execution-card-size=5816,ganesh-controller-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/evaluation/lane-stratified-v3-checkpoint-sweep/input/8ddeae14/startup.sh#1789051181042767,ganesh-controller-sha256=32ea79030c0917a0506bb6fe7a3a46f1226cd032f73fd770be21a0cf0b03c87e,ganesh-controller-size=7149,ganesh-wrapper-sha256=03b3128656bd3d7a787fdbaa5a81057895556420611b9bca2388ace20207ca52,ganesh-wrapper-size=2159 \
  --labels=project=ganesh-mini,purpose=v3-checkpoint-sweep,attempt=20260910t150000z \
  --format=json --quiet >"$attempt_dir/provider/instance-create.json"
