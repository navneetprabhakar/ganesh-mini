# Go focused non-triviality review — batch 25

Positions361–375, full prompt/reference read; not a full new test/mutant review.
Seven criterion-positive, eight non-triviality holds. 1306 total holds
(1303 additive+3),3305 unique outside inspections. Resume376.

| Position | ID | Finding |
| --- | --- | --- |
| 361 | exp-v1-go-repair-0200 | Criterion-positive: set equality requires both inclusion directions/cardinality, with rune rather than byte membership and multiplicity ignored. |
| 362 | exp-v1-go-generation-0304 | Non-triviality hold: fixed get/set/reset dispatcher with direct Atoi range validation and formatting. |
| 363 | exp-v1-go-generation-0305 | Non-triviality hold: directly transcribed ordered fixed-condition/error-message table. |
| 364 | exp-v1-go-generation-0306 | Criterion-positive: cancellation/terminal precedence, final-emission done semantics and copied sequence. |
| 365 | exp-v1-go-repair-0201 | Criterion-positive: terminal parser state must be a digit; a trailing separator cannot be erased into an accepted number. |
| 366 | exp-v1-go-repair-0202 | Non-triviality hold: remove redundant minus-sign addition around a standard-library formatter. |
| 367 | exp-v1-go-repair-0203 | Non-triviality hold: direct addition-to-subtraction substitution for specified deltas. |
| 368 | exp-v1-go-repair-0204 | Criterion-positive: strict upper bound and pre-increment arithmetic guard jointly preserve termination near MaxInt. |
| 369 | exp-v1-go-generation-0308 | Criterion-positive: overflow-safe counter/level updates, bucket placement and detached aggregates. Floating aggregate overflow and astronomical observation-count overflow are not adjudicated here; no full numeric approval. |
| 370 | exp-v1-go-generation-0309 | Criterion-positive: recursively insert at bottom using only Push/Pop, satisfying prohibition on auxiliary collections. |
| 371 | exp-v1-go-generation-0312 | Criterion-positive: cancellable progress state machine, capped progress without addition overflow and terminal/nil behavior. |
| 372 | exp-v1-go-repair-0205 | Non-triviality hold: direct OR-to-AND substitution for explicitly stated duplicate pair. |
| 373 | exp-v1-go-repair-0206 | Non-triviality hold: direct nil-callback guard in supplied dispatch. |
| 374 | exp-v1-go-repair-0207 | Non-triviality hold: explicitly identified continue-after-CLOSE repaired by direct break substitution. |
| 375 | exp-v1-go-repair-0210 | Non-triviality hold: directly specified literal base-case correction in supplied recurrence. |

Static review only. Criterion-positive is not full admission; numeric questions
for generation0308 remain unresolved, not claimed as executions or failures.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

