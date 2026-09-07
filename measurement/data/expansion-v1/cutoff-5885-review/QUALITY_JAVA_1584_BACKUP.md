# Java follow-up through position270 backup — 2026-09-07

Archive and receipt uploaded create-only, downloaded by exact GCS generation,
and verified byte-for-byte. Snapshot1584 holds,3957 unique outside inspections,
Go757/757 and Java270/1112. Includes Java batches1–18 and all fourteen new Java
probes/receipts. Historical sample170/130 still requires new-scope reconciliation.

- Archive: gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/archive/quality-java-followup-1584-20260907.tar.gz
- Generation:1788749988115631
- Bytes:6593584
- SHA256:d0bd9838d909ecbeeb46e3d8a230cf12b564213797d0e2e6c1d1b7802947dd9a
- Receipt:audit/quality-java-followup-1584-backup-receipt.json
- Receipt generation:1788750001825679

Evidence durability only, not admission or GCS-only billing certification.
No new cloud compute or infrastructure mutation was performed for this checkpoint.

## Corpus sufficiency risk

The unchanged5885-row frozen corpus minus1584 unique holds leaves at most4301
rows before remaining review, not an admitted dataset. Per-lane counts outside
the hold register: Go820,Java1001,JavaScript336,TypeScript336,Python729,Rust1079.
These sum to4301; token-family balance cannot be inferred from row counts.

The plan's diagnostic expansion range remains4000–8000. Only301 rows separate
the current upper bound from4000;302 additional unique holds would put even
that upper bound below the planned range. This is a risk, not a verified
shortfall yet. Do not silently lower the range, remove holds, resume generation,
or treat surviving rows as approved. Remaining systematic review and sample
reconciliation are required before choosing a seal or training configuration.

All103 data-tooling tests passed at this checkpoint. Java continuation starts271.
