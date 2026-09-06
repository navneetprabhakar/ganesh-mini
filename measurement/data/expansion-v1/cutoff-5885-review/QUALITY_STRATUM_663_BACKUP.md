# Quality review backup: 663 holds

Verified GCS archive through Python generation position 510 (batch 34),
1,743 unique outside-sample inspections, 660 additive plus historical three
holds. Holds are pending disposition, not final rejections or training admission.

- Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-663-20260906.tar.gz`
- Generation: `1788712647890671`
- Bytes: `2985853`
- SHA-256: `296bcae86843a3d735a648cf9d4899974bab414506b6f810ee2f40e6ec7808e0`
- Receipt: same campaign prefix, `audit/quality-stratum-followup-663-backup-receipt.json`
- Receipt generation: `1788712658836302`

Archive and receipt downloaded at their exact generations and hash-verified.
Archive includes review directory, relevant probe/audit tooling and tests,
handoff and project state. Its pending-backup wording predates verification.
All 97 data tooling tests pass; queue and unique hold counts reconcile;
candidate SHA remains unchanged. No VM or training started. This GCS evidence
does not establish account-wide GCS-only billing certification.
