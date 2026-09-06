# Quality review backup — 774 holds

Archive and receipt both passed exact-generation download/hash verification.
Preserves Python repair batches 1–6 through position 90, 774 holds
(771 additive plus historical three), and 2,007 outside-sample inspections.

- Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-774-20260906.tar.gz`
- Generation: `1788715118411001`
- Bytes: 3,288,380
- SHA-256: `9be666c6659d24da312b097cd8d3399af4535f30ca7ac098c3d5145b0e54ea97`
- Receipt: same campaign prefix, `audit/quality-stratum-followup-774-backup-receipt.json`
- Receipt generation: `1788715127802831`

Includes review notes, additive holds, probe source/results, helper/test code,
handoff and project state. Archive retains pre-upload pending-backup wording;
this note records subsequent verification. Later probes require later backup.

Frozen candidates, sample and partition unchanged; all 97 data-tooling tests
pass. No training admission, new VM, final rejection or new account-wide
billing certification.

