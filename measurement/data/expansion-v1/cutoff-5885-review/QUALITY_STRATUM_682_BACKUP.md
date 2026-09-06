# Quality review backup: 682 holds

Verified GCS archive through Python generation position 570 (batch 38),
1,803 unique outside-sample inspections, 679 additive plus historical three
holds. Holds are pending disposition, not final rejections or training admission.

- Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-682-20260906.tar.gz`
- Generation: `1788713098979218`
- Bytes: `3047026`
- SHA-256: `403a8c5a514556fceb208b0612db283abb843c24ff0433b069c1cd69c9eedb54`
- Receipt: same campaign prefix, `audit/quality-stratum-followup-682-backup-receipt.json`
- Receipt generation: `1788713108360923`

Archive and receipt downloaded at their exact generations and hash-verified.
Archive includes review directory, relevant probe/audit tooling and tests,
handoff and project state. Its pending-backup wording predates verification.
All 97 data tooling tests pass; queue and unique hold counts reconcile;
candidate SHA remains unchanged. No VM or training started. This GCS evidence
does not establish account-wide GCS-only billing certification.
