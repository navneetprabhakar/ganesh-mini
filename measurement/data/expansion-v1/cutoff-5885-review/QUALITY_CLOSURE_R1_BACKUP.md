# Original quality closure and recovery r1 backup

2026-09-08. Archive and receipt uploaded create-only, downloaded by exact object
generation, and compared byte-for-byte successfully (both cmp exit0).

- Base: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/`
- Archive: `archive/quality-closure-r1-20260908.tar.gz`
- Generation: `1788862365264157`; bytes: `9044611`
- SHA256: `32354f22fce2f7927c14501c1e7a8bda95df1b52e672f5db4eeaadc0a6539b16`
- Receipt: `audit/quality-closure-r1-backup-receipt.json`
- Receipt generation: `1788862509564516`

Includes2812-hold original review closure, full immutable r1 generation, all36
r1 sandbox program executions, reviewed quality findings, r2 request/plan and
Python diagnostics at the snapshot, and implementation/tests/docs.136 data
tests passed at this archive boundary. Later race/separation tooling is outside
this snapshot. Full r2 generation directory and later r2 Go/JS/TS diagnostics
require a separate terminal backup; they are not claimed preserved by this one.
This proof and later status updates postdate the archive. No recovered admission,
training, VM teardown or billing certification is implied by GCS preservation.
