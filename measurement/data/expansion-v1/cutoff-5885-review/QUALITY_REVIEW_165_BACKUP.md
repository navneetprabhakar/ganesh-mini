# 165-record quality-review evidence backup

Exact-generation upload/download SHA-256 verification succeeded for:

`gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-review-165-20260906.tar.gz`

- Generation: `1788661508166524`
- Bytes: 225,021
- SHA-256: `9c440cb4bd59a2f4f5d81283ebedce0806b2a8e98d696248250e15097fc3d491`
- Receipt: campaign `audit/quality-review-165-backup-receipt.json`, generation
  `1788661519789448`, also exact-generation roundtrip verified.

Includes review directory through THIRD_BATCH_REVIEW (165 inspections), probe
runner, provenance auditor, both helper test files, HANDOFF and PROJECT_STATE.
All 80 data tests passed at this checkpoint. Original candidates/teacher
history are in the earlier full-history archive, not duplicated here.

This receipt and FOURTH_BATCH_REVIEW onward postdate the archive and are not
included. No VM or new cloud compute was created. Broader GCS-only billing
certification remains unresolved; this backup is not a billing audit.
