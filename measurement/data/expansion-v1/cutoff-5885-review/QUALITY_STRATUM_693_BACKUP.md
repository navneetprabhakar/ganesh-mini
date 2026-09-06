# Quality stratum backup — 693 holds

Verified 2026-09-06. Covers Python generation positions 1–600, completed Rust
generation and array queues; 1,833 unique outside-sample inspections. There
are 690 additive holds plus historical three, not final rejections or admission.

Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-693-20260906.tar.gz`

- Generation: `1788713476605554`
- Bytes: 3,085,460
- SHA-256: `5715d71a84e88f81d1e4afdef93af782c4443357173c98a2154dc5ad78916ebe`
- Receipt: same base prefix, `audit/quality-stratum-followup-693-backup-receipt.json`
- Receipt generation: `1788713488394531`

Archive and receipt were downloaded at their exact generations and verified
against local bytes. Frozen candidate hash and 600 queue positions reconciled;
all 97 data tooling tests pass. Archive contains pre-upload checkpoint wording;
this receipt note records the subsequent successful verification.

No new VM or training. Prior VM and associated disk/network teardown evidence
is retained. Historical resource inventories are not account-wide GCS-only
billing certification; that remains unverified.
