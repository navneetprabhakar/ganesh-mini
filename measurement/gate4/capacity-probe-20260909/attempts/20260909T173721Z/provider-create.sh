#!/usr/bin/env bash
set -Eeuo pipefail

gcloud compute networks create ganesh-mini-g4-capacity-20260909t173721z-net \
  --project=executespecv1 \
  --subnet-mode=custom \
  --quiet

gcloud compute networks subnets create ganesh-mini-g4-capacity-20260909t173721z-subnet \
  --project=executespecv1 \
  --region=us-east1 \
  --network=ganesh-mini-g4-capacity-20260909t173721z-net \
  --range=10.195.0.0/24 \
  --enable-private-ip-google-access \
  --quiet

gcloud compute instances create ganesh-mini-g4-capacity-20260909t173721z \
  --project=executespecv1 \
  --zone=us-east1-c \
  --machine-type=g2-standard-8 \
  --provisioning-model=STANDARD \
  --maintenance-policy=TERMINATE \
  --no-restart-on-failure \
  --max-run-duration=7200s \
  --instance-termination-action=DELETE \
  --network-interface=network=ganesh-mini-g4-capacity-20260909t173721z-net,subnet=ganesh-mini-g4-capacity-20260909t173721z-subnet,no-address \
  --image=common-cu129-ubuntu-2204-nvidia-580-v20260831 \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=200GB \
  --boot-disk-type=pd-balanced \
  --boot-disk-device-name=ganesh-mini-g4-capacity-20260909t173721z \
  --boot-disk-auto-delete \
  --service-account=1061994342941-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --metadata-from-file=startup-script=scripts/inference/gcloud_expansion_metadata_wrapper.sh \
  --metadata=ganesh-gcp-project=executespecv1,ganesh-gcs-bucket=ganesh-gate0-model-transfer-1061994342941,ganesh-gcs-prefix=ganesh-mini-1.0/training/capacity-probe-v2/attempts/20260909T173721Z,ganesh-attempt-id=20260909T173721Z,ganesh-execution-card-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/capacity-probe-v2/attempts/20260909T173721Z/input/execution-card.json#1788979423030232,ganesh-execution-card-sha256=c6f13e92e9c19a33ec72da0e1b7e54e47557c676d150af8b6c157e554533f09d,ganesh-execution-card-size=4625,ganesh-controller-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/expansion-pilot-v1/input/gcloud-startup-expansion-pilot-v4.sh#1788922338878446,ganesh-controller-sha256=a0006bdb1ef68b3f4fe063fcfafae2b3631c26ddcd51d4611224e9e8b189327c,ganesh-controller-size=11598,ganesh-wrapper-sha256=587ebff6c5dc4156375eeaffafcd8b5ac432a1989255222553db3ee0cf7bbd20,ganesh-wrapper-size=2691 \
  --labels=project=ganesh-mini,purpose=capacity-probe,attempt=20260909t173721z \
  --quiet
