# Quality stratum backup — 705 holds

Verified 2026-09-06. Covers Python generation positions 1–630, completed Rust
generation and array queues; 1,863 unique outside-sample inspections. There
are 702 additive holds plus historical three, not final rejections or admission.

Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-705-20260906.tar.gz`

- Generation: `1788713721168599`
- Bytes: 3,120,403
- SHA-256: `55fcce596906d243b66f778d67c1f21a920d6095240fc2a813bffb59f7001e74`
- Receipt: same base prefix, `audit/quality-stratum-followup-705-backup-receipt.json`
- Receipt generation: `1788713733054568`

Archive and receipt downloaded at their exact generations and verified against
local bytes. Frozen candidate hash and 630 queue positions reconciled; all 97
data tooling tests pass. Archive retains pre-upload checkpoint wording; this
note records subsequent successful verification.

No new VM or training. Historical teardown/resource inventories do not certify
account-wide GCS-only billing, which remains unverified.
