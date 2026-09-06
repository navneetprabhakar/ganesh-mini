# Completed sample dispositions backup — 2026-09-07

Create-only GCS archive and receipt uploads passed generation-pinned download
verification. Snapshot: all 300 sample dispositions, 170 positive/130 held;
1167 corpus holds; 2960 outside-sample inspections; scope v13; 103 tests passed.
This is evidence durability, not training admission or billing certification.

- Archive: gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-sample-criteria-1167-20260907.tar.gz
- Generation: 1788727668814587
- Bytes: 6122831
- SHA256: 3d92190b117cffa76627042f8282bd259134c16cef7aa6ef4bf466282bc668df
- Receipt: audit/quality-sample-criteria-1167-backup-receipt.json
- Receipt generation: 1788727694933465

Both archive and receipt round trips verified. Later Go follow-up work is not
included in this snapshot and requires its own backup.
