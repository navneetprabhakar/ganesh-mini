# Python generation review, batch 1

Queue: filter the preserved v6 inventory in its existing order for lane python,
task_type generation, semantically_inspected_in_frozen_sample false. There are
684 entries across the already reopened first-pass/corrected strata. Positions
1–15 below were fully read (prompt, reference, original tests). No overlap with
the completed array/Rust queues or ten initial TypeScript/JavaScript reviews.

Seven new holds: one static and six with sandbox evidence. Total 484 additive
plus historical three = 487 holds; 1,248 unique outside-sample inspections.
No seven-criterion approval, revised admission seal, or new VM.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 1 | 0001 | Static hold: nonempty whitespace terms are forbidden by reference/tests though only title/section have a stripped-nonempty requirement. |
| 2 | 0002 | Hold: backend copy fabricates missing nested value; throwing close is invoked twice despite at-most-once contract. |
| 3 | 0003 | Hold: valid shared catalog-entry dictionaries remain aliased internally after deepcopy, causing two distinct part reservations to debit the same availability twice. |
| 4 | 0004 | Full type validation precedes lexicographic nested-loop pair search; arbitrary-precision sums agree. No new hold. |
| 5 | 0005 | Hold: finite training rows produce infinite representable mean; finite prediction distances raise OverflowError. |
| 6 | 0006 | Ordinary normalization/copy/format paths agree. Unbounded integer-to-float average and formatter consistency restrictions remain pending. No new hold. |
| 7 | 0007 | Kind type precedes mapping lookup; generator processing, exact keys, independent groups and normalized duplicates agree. Empty excluded iterable container interpretation pending; no new hold. |
| 8 | 0008 | Exact dictionary/bytes checks, digest authentication before XOR and independent containers agree. Exercise is explicitly not production cryptography; no new hold. |
| 9 | 0009 | Full rectangular/cell validation precedes endpoint checks; BFS order and owned result agree. No new hold. |
| 10 | 0010 | Exact header, four split fields, explicit float syntax and finite checks agree. No new hold. |
| 11 | 0011 | Hold: valid finite arbitrary-precision integer score raises OverflowError through math.isfinite conversion. |
| 12 | 0012 | Selection by strict greater then stable move preserves item identity and ties; no sorted/sort call. No new hold. |
| 13 | 0013 | Counter update precedes snapshot callbacks; duplicate ordinary functions deduplicate and independent copies agree. Callable equality/reentrant return semantics pending; no new hold. |
| 14 | 0015 | Hold: invalid large integer probability raises OverflowError instead of ValueError. Mutable hashable symbol deep-copy and broader numeric-type support remain pending. |
| 15 | 0016 | Hold: mutable Symbol is retained by alias despite immutable stored-scalar requirement; changing its public name changes sequence output. |

## Evidence

0001: Prompt says terms are nonempty strings, unlike its explicit stripping
condition on title/section. Reference applies `not term.strip()` and original
`test_term_validation_and_failed_analysis_is_stable` rejects `["   "]`.
That narrows a legitimate substring search. Static comparison, not new execution.

All six following diagnostics used pinned Python 3.11.15, network disabled and
the same resource-limited sandbox contract. Each exited 1 without timeout;
the stored result binds candidate/task/input hashes and original tests.

| ID | Probe / result stem | ms | Observed result |
| --- | --- | ---: | --- |
| 0002 | monitor_backend_contract_probe.py / monitor-backend-contract-result.json | 444 | Missing nested key did not raise KeyError; close count was 2 instead of 1. |
| 0003 | parts_shared_entry_probe.py / parts-shared-entry-result.json | 471 | Availability -1 instead of 0 after valid one-unit reservation of each part. |
| 0005 | nearest_mean_finite_probe.py / nearest-mean-finite-result.json | 437 | Mean inf instead of 1e308; squared distance on 1e200 raised OverflowError. |
| 0011 | artifact_score_integer_probe.py / artifact-score-integer-result.json | 455 | math.isfinite(10**400) raised OverflowError on a valid finite integer score. |
| 0015 | state_probability_integer_probe.py / state-probability-integer-result.json | 417 | Invalid 10**400 probability raised OverflowError, not specified ValueError. |
| 0016 | symbol_immutable_storage_probe.py / symbol-immutable-storage-result.json | 433 | b'{@changed}' instead of b'{@kept}' after caller mutation. |

0002 original backend unconditionally indexes `config["nested"]["values"]`
even when tests initialize with `{}`. Reference's special `_BackendConfig`
missing-key branch accommodates that fixture rather than preserving ordinary
dictionary behavior. Findings remain additive holds, not claims about intent.

Original candidates/tests/frozen sample unchanged. Candidate-file SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged: these rows already belong to reopened Python generation
strata. Continue position 16. Backup through Rust 684 predates this batch.
