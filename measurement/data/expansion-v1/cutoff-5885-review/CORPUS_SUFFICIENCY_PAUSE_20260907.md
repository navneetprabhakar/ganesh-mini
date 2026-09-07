# Corpus sufficiency: verified plan mismatch, pending user direction

2026-09-07. Current gate: expansion quality review before training admission.

The controlling plan at docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md requires a
4000–8000-record execution-verified diagnostic expansion. Its5885 construction
cutoff supersedes the old6000 construction quota, not quality/admission rules.
The current unique hold partition contains1890 rows (1887 additive plus3
historical), leaving an upper bound of3995 outside holds. These3995 are not
admitted: Java review is855/1112, the latest systematic scopes still require
reconciliation, and no revised dataset seal exists.

## Verified evidence

- Frozen candidate count5885; SHA256
  `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec` unchanged.
- `reconcile_sample_criteria.reconcile()` reports1890 unique corpus holds.
- Java note positions1–855 are continuous, unique and match v14 inventory IDs.
- Unique outside-sample inspections4542: prior2930 + Go757 + Java855.
- Frozen sample remains170 positive/130 held; these dispositions predate the
  newest scope reconciliation and are not an admission pass.
- Batch57 takes the maximum remaining below4000. Holds are reversible review
  quarantine; this does not establish permanent rejection or training failure.
- Newly executed page-end overflow: repair0318 compiles successfully and fails
  its semantic probe in the pinned network-disabled Java sandbox; evidence is
  candidate-bound in java-repair0318-page-end-overflow-result.json.

## Required decision

Do not silently lower the planned minimum, generate beyond the user's cutoff,
train on held rows, or call the project complete. Under AGENTS.md's verified
goal-divergence stop rule, pause further review mutations/training/compute;
reconciliation and preservation of current evidence are the only continuation.

Recommended route for user consideration: finish the remaining review, then
repair recoverable held examples in a separately versioned derived corpus,
preserving the original5885 and full parent lineage; rerun affected execution,
quality and separation checks, restore the planned admitted yield and seal it.
This recommendation is not an implemented or automatically approved plan change.
Alternative: explicitly revise the diagnostic minimum after reviewing final
yield and family/token balance. Do not waive correctness or evaluation separation.

No VM was created, started, stopped or deleted during this review continuation.
GCS preservation uses the previously authorized backup prefix. No claim of
global GCS-only billing is made; historic inventory limitations remain.

Preservation complete: create-only GCS archive/receipt for1890 holds passed
exact-generation download/hash checks. See QUALITY_JAVA_1890_BACKUP.md.
All103 data-tooling tests passed after the final review checkpoint.
