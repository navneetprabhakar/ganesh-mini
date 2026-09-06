# Quality review backup — 796 holds

Archive and receipt both passed exact-generation download/hash verification.
Preserves Python repair batches 1–9 through position 135, 796 holds
(793 additive plus historical three), and 2,052 outside-sample inspections.

- Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-796-20260906.tar.gz`
- Generation: `1788715668873096`
- Bytes: 3,336,550
- SHA-256: `8267c174aae30615ae7103da7660366e8e014f479aee9bfcc20e6b887b02d5db`
- Receipt: same campaign prefix, `audit/quality-stratum-followup-796-backup-receipt.json`
- Receipt generation: `1788715679482980`

Includes review notes, additive holds, probe source/results, helper/test code,
handoff and project state. Archive retains pre-upload pending-backup wording;
this note records subsequent verification. Frozen candidates unchanged;
all 97 data-tooling tests pass. No admission, final rejection, new VM or
account-wide GCS-only billing certification.
