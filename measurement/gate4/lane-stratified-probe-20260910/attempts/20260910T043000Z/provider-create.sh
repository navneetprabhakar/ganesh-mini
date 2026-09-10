#!/usr/bin/env bash
set -Eeuo pipefail

gcloud compute networks create ganesh-mini-g4-lanes-20260910t043000z-net \
  --project=executespecv1 \
  --subnet-mode=custom \
  --quiet

gcloud compute networks subnets create ganesh-mini-g4-lanes-20260910t043000z-subnet \
  --project=executespecv1 \
  --region=us-east1 \
  --network=ganesh-mini-g4-lanes-20260910t043000z-net \
  --range=10.195.0.0/24 \
  --enable-private-ip-google-access \
  --quiet

gcloud compute instances create ganesh-mini-g4-lanes-20260910t043000z \
  --project=executespecv1 \
  --zone=us-east1-c \
  --machine-type=g2-standard-8 \
  --provisioning-model=STANDARD \
  --maintenance-policy=TERMINATE \
  --no-restart-on-failure \
  --max-run-duration=7200s \
  --instance-termination-action=DELETE \
  --network-interface=network=ganesh-mini-g4-lanes-20260910t043000z-net,subnet=ganesh-mini-g4-lanes-20260910t043000z-subnet,no-address \
  --image=common-cu129-ubuntu-2204-nvidia-580-v20260831 \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=200GB \
  --boot-disk-type=pd-balanced \
  --boot-disk-device-name=ganesh-mini-g4-lanes-20260910t043000z \
  --boot-disk-auto-delete \
  --service-account=1061994342941-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --metadata-from-file=startup-script=scripts/inference/gcloud_expansion_metadata_wrapper.sh \
  --metadata=ganesh-gcp-project=executespecv1,ganesh-gcs-bucket=ganesh-gate0-model-transfer-1061994342941,ganesh-gcs-prefix=ganesh-mini-1.0/training/lane-stratified-probe-v3/attempts/20260910T043000Z,ganesh-attempt-id=20260910T043000Z,ganesh-execution-card-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/lane-stratified-probe-v3/attempts/20260910T043000Z/input/execution-card.json#1789014452434622,ganesh-execution-card-sha256=832a36cc90bc35d4947931df70a934e541df94c6e8ff570a216633a6bfe8002c,ganesh-execution-card-size=4667,ganesh-controller-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/expansion-pilot-v1/input/gcloud-startup-expansion-pilot-v4.sh#1788922338878446,ganesh-controller-sha256=a0006bdb1ef68b3f4fe063fcfafae2b3631c26ddcd51d4611224e9e8b189327c,ganesh-controller-size=11598,ganesh-wrapper-sha256=587ebff6c5dc4156375eeaffafcd8b5ac432a1989255222553db3ee0cf7bbd20,ganesh-wrapper-size=2691 \
  --labels=project=ganesh-mini,purpose=lane-probe,attempt=20260910t043000z \
  --quiet
