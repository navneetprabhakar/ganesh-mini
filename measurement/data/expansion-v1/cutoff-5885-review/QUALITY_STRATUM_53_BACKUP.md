# Targeted quality follow-up backup

The 53-hold checkpoint (50 additive plus historical three), initial 300 notes,
stratum inventory, ten outside-sample inspections, ten failing TS diagnostics,
passing JS first-match control, and updated probe helper are backed up.

- Object: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-stratum-followup-53-20260906.tar.gz`
- Generation: `1788662830557952`
- Bytes: 464,196
- SHA-256: `b2e4087581cfdfcdb5de7dd1aa1fee85a0a55a90dfd51152dda9b8fd103db3dd`
- Exact-generation download SHA matched. Receipt
  `audit/quality-stratum-followup-53-backup-receipt.json`, generation
  `1788662843841632`, also passed exact-generation download verification.

All 92 data-tooling tests passed in `.venv`; system Python 3.9 cannot collect
the full suite's modern type syntax. No candidate execution used the host.
Later array-review probes and this receipt postdate the archive. Earlier full
history and VM backups remain intact. No new VM or training run.
