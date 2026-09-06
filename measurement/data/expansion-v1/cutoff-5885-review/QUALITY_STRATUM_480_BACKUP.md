# Verified quality checkpoint: 480 holds, complete Rust queue

2026-09-06. Archive and receipt were uploaded to the authorized campaign GCS
prefix, downloaded at their exact generations and compared by SHA-256.

- Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-480-20260906.tar.gz`
- Generation: `1788685775251684`
- Bytes: `2380984`
- SHA-256: `2ccdc37673b61473f646e20ac32c10fef1ba0c0229901125ef0772bc1a6197d3`
- Receipt: same campaign prefix, `audit/quality-stratum-followup-480-backup-receipt.json`
- Receipt generation: `1788685785255804`

Contents include Rust batches 1–46, all review probes/results through complete
684-position queue, 477 additive holds (480 with historical three), 1,233
unique outside-sample inspections, review tooling/tests, and checkpoint process
documents. All 97 data-tooling tests passed; exact queue coverage, hold ID
uniqueness/evidence existence and original candidate SHA were verified locally.

This note and subsequent checkpoint edits postdate that archive. This is not
an admission seal, an unbiased defect rate, or account-wide GCS-only billing
certification. No new VM was used. Continue the remaining reopened strata.
