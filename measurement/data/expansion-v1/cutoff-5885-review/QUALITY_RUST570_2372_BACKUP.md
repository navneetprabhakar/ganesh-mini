# Rust570 /2372-hold backup verification

2026-09-08. Archive and receipt uploaded create-only, downloaded by exact
generation and compared byte-for-byte. Both passed.

- Base: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/`
- Archive: `archive/quality-rust570-2372-pathfix-20260908.tar.gz`
- Generation: `1788854448469254`; bytes: `6926913`
- SHA256: `7a325710731f9fe9b3b3145337cf90299dcd5543187a21e4048d495413a11254`
- Receipt: `audit/quality-rust570-2372-backup-receipt.json`
- Receipt generation: `1788854508068371`

Contains integrated review1–570,2372 holds,5067 unique outside inspections,
sample165 positive/135 held and all eight Rust probes. Draft notes above19
were excluded from this checkpoint. No admission or billing certification.

Full103-test run found two failures caused by53 historical Rust evidence
fields containing filename-plus-prose rather than usable paths. Normalized
those paths and preserved prose in evidence_detail; all103 tests then passed.
No hold IDs or dispositions changed. The earlier pre-fix archive remains
preserved at archive/quality-rust570-2372-20260908.tar.gz, generation
1788854370386052 (also exact-generation byte-compared); this pathfix archive
supersedes it. This proof and subsequent reviews postdate both archives.
