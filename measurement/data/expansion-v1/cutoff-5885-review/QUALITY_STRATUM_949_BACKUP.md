# Quality review backup through 949 holds

Verified on 2026-09-06. Archive includes JS/TS residual batches 1–4 through
position 60, 946 additive holds plus historical three, and 2,403 unique
outside-sample inspections. Python repair 426, Python generation 684, Rust
generation 684 and array queue 544 remain complete. Review is not admission.

- Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-949-20260906.tar.gz`
- Generation: `1788719281027490`
- Bytes: `3727746`
- SHA-256: `990f086220b1ebcb9a6a7ea979b50236990683fae2c1185dbff7516550591ed0`
- Receipt: same campaign `audit/quality-stratum-followup-949-backup-receipt.json`
- Receipt generation: `1788719292428022`

Archive was downloaded at its pinned generation and compared byte-hash to the
local archive. Receipt separately uploaded and round-trip verified. Pre-upload
documents inside the archive correctly state that backup was pending; this
note records its subsequent completion. No VM created or training seal issued.
