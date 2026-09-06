# Java criterion evidence backup — 2026-09-07

Verified create-only GCS upload and generation-pinned download of the archive
and receipt. Snapshot: 1113 holds, 2960 outside-sample inspections, scope v9,
116 sample dispositions (73 positive, 43 held); 100 data-tooling tests passed.
Includes the Go additive-probe documentation correction. No training admission.

- Archive: gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-java-criteria-1113-20260907.tar.gz
- Generation: 1788727049059803
- Bytes: 4910900
- SHA256: 7ba3e604cdc94f4a8a985d176e5fed45e512195e26dbd59eb5bd0c47b417e6c3
- Receipt: audit/quality-java-criteria-1113-backup-receipt.json
- Receipt generation: 1788727066102367

Both round trips verified. This records evidence durability, not GCS-only billing
certification or permission for new compute.
