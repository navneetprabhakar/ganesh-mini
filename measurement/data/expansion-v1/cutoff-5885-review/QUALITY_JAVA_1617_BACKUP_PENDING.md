# Java evidence backup awaiting reauthentication — 2026-09-07

The create-only upload of the checkpoint1617 archive failed because gcloud
could not refresh credentials without interactive reauthentication. No remote
generation was obtained and no upload/download verification is claimed.
Last verified GCS checkpoint remains1584 holds / Java270.

Preserved local archive (snapshot through Java330, not later batches):

- Path: artifacts/verification/cutoff-5885-vm/quality-java-followup-1617-20260907.tar.gz
- Bytes:6601505
- SHA256:285c485530778b841512b4160f77b246a2d5205ae191bbc0ab98766ba1b9feff
- Intended create-only object: gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-java-followup-1617-20260907.tar.gz

The user was asked to run gcloud auth login with the already-authorized bucket
account. Do not switch accounts, bypass reauthentication, overwrite objects or
claim a successful backup without exact-generation download and hash comparison.
After sign-in, reuse the unchanged archive bytes with create-only upload; if an
object already exists, inspect its exact generation and compare bytes rather
than replacing it. Produce and verify a create-only receipt. Later Java331–360
evidence requires a new distinct archive after this checkpoint or a new full
snapshot; never relabel the1617 archive as containing it.

Local review continued safely through Java360 (batch24):1636 total holds,
4047 unique outside inspections. Original candidates and historical partitions
remain unchanged. New evidence includes the executed generation0196 threshold
overflow probe. All103 data-tooling tests passed; position1–360 identity/order
and hold reconciliation passed. No VM or infrastructure action was attempted.
