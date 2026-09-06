# Go criteria and first 30 follow-ups backup — 2026-09-07

Archive and receipt uploaded create-only, downloaded by exact generation and
verified byte-for-byte. Includes scope v7, Go sample decisions, first 30 focused
Go checks and both executed diagnostics. 1092 holds, 2960 outside-sample scoped
inspections, 100 data-tooling tests passed; no training seal or VM.

- Archive: gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-go-criteria-1092-20260907.tar.gz
- Generation: 1788724359149856
- Bytes: 4393025
- SHA-256: 89b7ba9d42fc976410a999f2aa88d51c27056792c7a6f6daacab4f3f25ce18c5
- Receipt: gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/audit/quality-go-criteria-1092-backup-receipt.json
- Receipt generation: 1788724372518701

Post-archive correction: GO_NONTRIVIALITY_REVIEW_1.md now correctly states
that the Go probes add a diagnostic file alongside original tests. The archive's
earlier 'isolated replacement' prose is wrong; preserved task files and
probe_mode=additive already record the correct executed configuration. Results,
holds and counts do not change. The next archive must include this correction.
