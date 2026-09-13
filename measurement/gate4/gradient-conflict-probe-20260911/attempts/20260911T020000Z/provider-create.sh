#!/usr/bin/env bash
set -Eeuo pipefail

gcloud compute networks create ganesh-mini-g4-grad-20260911t020000z-net \
  --project=executespecv1 \
  --subnet-mode=custom \
  --quiet

gcloud compute networks subnets create ganesh-mini-g4-grad-20260911t020000z-subnet \
  --project=executespecv1 \
  --region=us-east1 \
  --network=ganesh-mini-g4-grad-20260911t020000z-net \
  --range=10.196.0.0/24 \
  --enable-private-ip-google-access \
  --quiet

gcloud compute instances create ganesh-mini-g4-grad-20260911t020000z \
  --project=executespecv1 \
  --zone=us-east1-c \
  --machine-type=g2-standard-8 \
  --provisioning-model=STANDARD \
  --maintenance-policy=TERMINATE \
  --no-restart-on-failure \
  --max-run-duration=7200s \
  --instance-termination-action=DELETE \
  --network-interface=network=ganesh-mini-g4-grad-20260911t020000z-net,subnet=ganesh-mini-g4-grad-20260911t020000z-subnet,no-address \
  --image=common-cu129-ubuntu-2204-nvidia-580-v20260831 \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=200GB \
  --boot-disk-type=pd-balanced \
  --boot-disk-device-name=ganesh-mini-g4-grad-20260911t020000z \
  --boot-disk-auto-delete \
  --service-account=1061994342941-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --metadata-from-file=startup-script=scripts/inference/gcloud_expansion_metadata_wrapper.sh \
  --metadata=ganesh-gcp-project=executespecv1,ganesh-gcs-bucket=ganesh-gate0-model-transfer-1061994342941,ganesh-gcs-prefix=ganesh-mini-1.0/training/gradient-conflict-probe-v4/attempts/20260911T020000Z,ganesh-attempt-id=20260911T020000Z,ganesh-execution-card-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/gradient-conflict-probe-v4/attempts/20260911T020000Z/input/execution-card.json#1789320280154764,ganesh-execution-card-sha256=c284839682c97855b232eaf7ad4fe90c4c43360767c1ebe902f5e441bbb0470f,ganesh-execution-card-size=4681,ganesh-controller-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/gradient-conflict-probe-v4/input/3ae2ca8a/startup-controller.sh#1789089731804252,ganesh-controller-sha256=5a624ac3e677afde2742f871e2a6d8b7c00f0d2a8ee4845cf9926e247d28a24a,ganesh-controller-size=12005,ganesh-wrapper-sha256=587ebff6c5dc4156375eeaffafcd8b5ac432a1989255222553db3ee0cf7bbd20,ganesh-wrapper-size=2691 \
  --labels=project=ganesh-mini,purpose=gradient-conflict-probe,attempt=20260911t020000z \
  --quiet
