# Rust270 / 2251-hold backup verification

2026-09-08. Exact-generation roundtrip verified for both archive and receipt.

- Archive: `gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-rust270-2251-20260908.tar.gz`
- Generation: `1788839781303703`
- Bytes: `6887484`
- SHA-256: `73abfe437f38cd4aa36545bf89cfd00126e9dcbea44e4305ef356e6144122358`
- Receipt: `audit/quality-rust270-2251-backup-receipt.json` under the same prefix.
- Receipt generation: `1788839795028940`; downloaded exact-generation bytes match local receipt.

Includes review through Rust270,2251 corpus holds,4920 outside unique inspections,
sample165/135, all five Rust diagnostic probes and recovery-tooling preflight.
No training admission. This note and later review are not inside this archive.
Storage verification is not a project-wide billing certification.

