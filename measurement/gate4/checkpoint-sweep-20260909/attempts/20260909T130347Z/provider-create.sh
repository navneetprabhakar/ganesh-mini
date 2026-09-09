#!/usr/bin/env bash
set -Eeuo pipefail

gcloud compute instances create ganesh-mini-g4-sweep-20260909t130347z \
  --project=executespecv1 \
  --zone=us-east1-c \
  --machine-type=g2-standard-8 \
  --provisioning-model=STANDARD \
  --maintenance-policy=TERMINATE \
  --no-restart-on-failure \
  --max-run-duration=7200s \
  --instance-termination-action=DELETE \
  --network=ganesh-mini-g4-sweep-net-20260909t130347z \
  --subnet=ganesh-mini-g4-sweep-subnet-20260909t130347z \
  --no-address \
  --image=common-cu129-ubuntu-2204-nvidia-580-v20260831 \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=200GB \
  --boot-disk-type=pd-balanced \
  --boot-disk-device-name=ganesh-mini-g4-sweep-20260909t130347z \
  --boot-disk-auto-delete \
  --service-account=1061994342941-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --metadata-from-file=startup-script=scripts/inference/gcloud_checkpoint_sweep_metadata_wrapper.sh \
  --metadata=ganesh-gcp-project=executespecv1,ganesh-gcs-bucket=ganesh-gate0-model-transfer-1061994342941,ganesh-gcs-prefix=ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/attempts/20260909T130347Z,ganesh-attempt-id=20260909T130347Z,ganesh-execution-card-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/attempts/20260909T130347Z/control/execution-card.json#1788959132311948,ganesh-execution-card-sha256=528ff613dc6b4966e9f8cdc3ba5c46c95fbc5477208999670286abd28885a0b2,ganesh-execution-card-size=4766,ganesh-controller-uri=gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/input/1a5a2e0/gcloud_startup_checkpoint_sweep.sh#1788958261821760,ganesh-controller-sha256=202730fe842e272c302d1624a9dd1b1195e8c470e6557ad48de5129ac355ad97,ganesh-controller-size=7198,ganesh-wrapper-sha256=03b3128656bd3d7a787fdbaa5a81057895556420611b9bca2388ace20207ca52,ganesh-wrapper-size=2159 \
  --labels=project=ganesh-mini,purpose=checkpoint-sweep,attempt=20260909t130347z \
  --quiet
