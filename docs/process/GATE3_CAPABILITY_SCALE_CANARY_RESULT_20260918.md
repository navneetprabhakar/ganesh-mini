# Gate 3 capability-scale construction canary result — 2026-09-18

Status: passed; remaining first-pass teacher construction active locally

## Result

The prospective scale controller admitted one generation and one repair
candidate in every lane: 12/12 canary cells, zero unresolved outcomes, and zero
evaluation-artifact reads. The terminal result is sealed at
`dc239958fc66b793830a19c254c54cdfad316263cc0eb04607a0e76454a13ad3`.

The first teacher contract produced 12 source-unique candidates. Blind semantic
review passed 11/12, independent test authorship passed 12/12 structurally, and
blind delta review passed 5/12. The seven delta rejects were valid: the prompt
allowed the sole known-bad defect to target either the assigned primary
capability or the scheduled cross-cutting dimension, while admission requires
the defect to be primary-capability-specific.

The original evidence is immutable. Seven same-cell, source-unique reserves
were activated under seal
`3366e2dcf16c28b5e922c640eb97b28ff515cf89052d2ee6ee0eb3ec655517d8`.
The prospective `capability-scale-primary-delta-teacher-prompt/v2` requires the
single defect to exercise the assigned primary capability and the known-bad
implementation to already satisfy the cross-cutting behavior. All seven
reserve teachers, semantic reviews, test authors, and fresh delta audits passed.

The first reserve executable matrix admitted 5/7. Two authored suites failed
against the references: a Go non-mutation test conflated nil and empty slices,
and TypeScript suites failed strict compilation on unchecked map lookups. The
single permitted candidate correction was used as a fresh blind test reauthor
for only those two candidates. The reauthor saw no prior tests, reference, or
verifier output. Both fresh test-author results, fresh delta audits, and exact
four-way executable matrices passed under seal
`3edd12d0f16af3e38e88e4963c1a877fb9c9b290fff53fa3f5a405760e79d482`.

Final accounting is 19 teacher drafts, seven activated reserves, two blind test
reauthors, 12 admissions, 12 unique sources, and one admitted candidate per
lane/task-type canary cell. These 12 admissions do not yet change the sealed
174-row training-entry corpus; they become countable only in the final scale
admission package.

## Next action

Run the remaining 534 first-pass teacher requests under the corrected v2 prompt
without regenerating the consumed 12 requests. Then run blind semantic review,
independent tests, fresh delta audits, executable matrices, bounded reserve
activation, separation, and final corpus assembly. No GCloud resource or
training job is active.
