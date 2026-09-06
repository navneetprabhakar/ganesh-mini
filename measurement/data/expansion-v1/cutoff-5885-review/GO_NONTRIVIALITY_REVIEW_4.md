# Go focused non-triviality review — batch 4

Positions 46–60, full prompt/reference read; no new full test/mutant review.
Eleven criterion-positive, four non-triviality holds, plus one behavioral hold.
Five new holds: total1179 (1176 additive+3), 2990 unique outside inspections.

| Position | ID | Finding |
| --- | --- | --- |
| 46 | exp-v1-go-generation-0035 | Criterion-positive matcher composition and reflection; executed typed-nil unsafe.Pointer omitted from IsNil. |
| 47 | exp-v1-go-generation-0036 | Non-triviality hold: collection of direct library casts/encoding wrappers and elementary boolean dispatch. |
| 48 | exp-v1-go-repair-0021 | Non-triviality hold: one direct sort comparator direction in a library-popcount ordering wrapper. |
| 49 | exp-v1-go-repair-0022 | Criterion-positive: removes recursive RLock acquisition under writer preference, preserving one-lock consistent snapshot. |
| 50 | exp-v1-go-repair-0023 | Criterion-positive: Euclidean remainder invariant and termination, including unsigned magnitude of MinInt64. |
| 51 | exp-v1-go-repair-0024 | Criterion-positive: mutable big.Int accumulation versus overwriting, strict byte grammar and base conversion. No impractically huge input execution claimed. |
| 52 | exp-v1-go-generation-0037 | Criterion-positive: ordered typed JSON and payload-bound digest. Formula-specific exercise, not production signing recommendation. |
| 53 | exp-v1-go-generation-0038 | Criterion-positive: cross-list referential validation, rounded-up half without overflow and ordered copied penalties. Future-compatible prose does not waive current conflict-subset rule. |
| 54 | exp-v1-go-generation-0039 | Criterion-positive: recursive shape validation and serial/concurrent wave composition. Cyclic self-referential slice graphs not adjudicated here. |
| 55 | exp-v1-go-generation-0040 | Criterion-positive: atomic locked insert-only catalog, copied value queries and constructor-only scope. |
| 56 | exp-v1-go-repair-0026 | Non-triviality hold: fixed whitespace literal replacement in strings.Repeat wrapper. |
| 57 | exp-v1-go-repair-0027 | Criterion-positive: unique validated client/service mapping then ordered call routing. Source-defined method validation retained. |
| 58 | exp-v1-go-repair-0028 | Non-triviality hold: explicitly identified n-squared recurrence term. 32-bit range portability not measured; pinned runtime is 64-bit. |
| 59 | exp-v1-go-generation-0045 | Criterion-positive: transactional sequential batch on a copied map with locked atomic commit and indexed errors. |
| 60 | exp-v1-go-generation-0046 | Criterion-positive: recursive polymorphic expression formatting and explicit nil-interface fallback. No extra typed-nil receiver guarantee inferred. |

go_0035_unsafe_nil_probe-result.json: Go1.22.12, exit[1], no timeout,
26674ms. Additive review_test.go runs with original tests; typed nil
unsafe.Pointer returns false. The probe merely constructs a nil pointer value,
never dereferences or converts memory. Network off, 1CPU/512MiB/64PIDs/60s.
Full original/additive task and hashes retained. No separate mutant rerun.
Resume61; all dispositions are criterion-scoped, not seven-criterion admission.
