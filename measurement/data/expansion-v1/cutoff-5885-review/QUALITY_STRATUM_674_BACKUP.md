# Quality review backup: 674 holds

Verified GCS archive through Python generation position 540 (batch 36),
1,773 unique outside-sample inspections, 671 additive plus historical three
holds. Holds are pending disposition, not final rejections or training admission.

- Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-674-20260906.tar.gz`
- Generation: `1788712885613620`
- Bytes: `3020977`
- SHA-256: `4368282e510a115b29d72f304638e90b6fe770c595b5fbf426a360219e42447c`
- Receipt: same campaign prefix, `audit/quality-stratum-followup-674-backup-receipt.json`
- Receipt generation: `1788712898995234`

Archive and receipt downloaded at their exact generations and hash-verified.
Archive includes review directory, relevant probe/audit tooling and tests,
handoff and project state. Its pending-backup wording predates verification.
All 97 data tooling tests pass; queue and unique hold counts reconcile;
candidate SHA remains unchanged. No VM or training started. This GCS evidence
does not establish account-wide GCS-only billing certification.
