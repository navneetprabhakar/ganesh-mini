#!/usr/bin/env bash
set -Eeuo pipefail

gcloud compute networks create ganesh-mini-g4-grad-20260914t003000z-net \
  --project=executespecv1 \
  --subnet-mode=custom \
  --quiet

gcloud compute networks subnets create ganesh-mini-g4-grad-20260914t003000z-subnet \
  --project=executespecv1 \
  --region=us-east1 \
  --network=ganesh-mini-g4-grad-20260914t003000z-net \
  --range=10.196.0.0/24 \
  --enable-private-ip-google-access \
  --quiet

gcloud compute instances create ganesh-mini-g4-grad-20260914t003000z \
  --project=executespecv1 \
  --zone=us-east1-c \
  --machine-type=g2-standard-8 \
  --provisioning-model=STANDARD \
  --maintenance-policy=TERMINATE \
  --no-restart-on-failure \
  --max-run-duration=7200s \
  --instance-termination-action=DELETE \
  --network-interface=network=ganesh-mini-g4-grad-20260914t003000z-net,subnet=ganesh-mini-g4-grad-20260914t003000z-subnet,no-address \
  --image=common-cu129-ubuntu-2204-nvidia-580-v20260831 \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=200GB \
  --boot-disk-type=pd-balanced \
  --boot-disk-device-name=ganesh-mini-g4-grad-20260914t003000z \
  --boot-disk-auto-delete \
  --service-account=1061994342941-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --metadata-from-file=startup-script=scripts/inference/gcloud_expansion_metadata_wrapper.sh \
  --metadata=ganesh-gcp-project=executespecv1,ganesh-gcs-bucket=ganesh-gate0-model-transfer-1061994342941,ganesh-gcs-prefix=ganesh-mini-1.0/training/gradient-conflict-probe-v4/attempts/20260914T003000Z,ganesh-attempt-id=20260914T003000Z,ganesh-execution-card-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/gradient-conflict-probe-v4/attempts/20260914T003000Z/input/execution-card.json#1789357653715057,ganesh-execution-card-sha256=0f7a15880f68bc1d2c20eecbe53e9e622a514f7cdadc6234bf0912756e0b194d,ganesh-execution-card-size=4681,ganesh-controller-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/gradient-conflict-probe-v4/input/c01a99b8/startup-controller.sh#1789344952897289,ganesh-controller-sha256=e4aaecc2025d841cffdd9e75d105de62967d88425aa76015107d41275c618085,ganesh-controller-size=12148,ganesh-wrapper-sha256=587ebff6c5dc4156375eeaffafcd8b5ac432a1989255222553db3ee0cf7bbd20,ganesh-wrapper-size=2691 \
  --labels=project=ganesh-mini,purpose=gradient-conflict-probe,attempt=20260914t003000z \
  --quiet
