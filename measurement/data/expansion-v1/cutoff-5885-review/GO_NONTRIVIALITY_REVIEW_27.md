# Go focused non-triviality review — batch 27

Positions391–405, full prompt/reference read; not a full new test/mutant review.
11 criterion-positive. Four non-triviality holds.
1317 total holds (1314 additive+3),3335 unique outside inspections. Resume406.

| Position | ID | Finding |
| --- | --- | --- |
| 391 | exp-v1-go-repair-0220 | Non-triviality hold: directly enumerate the six specified bytes instead of broad supplied range. |
| 392 | exp-v1-go-generation-0333 | Criterion-positive: conditional grouping, stable within-group order and deterministic lexical group order with exact framing. |
| 393 | exp-v1-go-generation-0335 | Non-triviality hold: fixed four-field ParseDuration/range-validation wrapper. |
| 394 | exp-v1-go-generation-0336 | Criterion-positive: insertion-ordered composite identity and deep label copies preserving nil versus empty. |
| 395 | exp-v1-go-repair-0221 | Non-triviality hold: direct library reverse-sort substitution for supplied nonnegative partition. |
| 396 | exp-v1-go-repair-0222 | Criterion-positive: flush pending final run after streaming run transitions, including singleton/all-equal input. |
| 397 | exp-v1-go-repair-0224 | Criterion-positive: draining must detach returned backing storage before subsequent publish can reuse capacity. |
| 398 | exp-v1-go-generation-0337 | Criterion-positive: full permutation validation and prefix inversion accounting. No huge-input runtime or int-count representability claim. |
| 399 | exp-v1-go-generation-0340 | Criterion-positive: ready/exact-match selection with stable highest-revision tie break and nil-aware detached labels. |
| 400 | exp-v1-go-generation-0341 | Criterion-positive: comment handling, first-equals split, exact untrimmed value and atomic key validation. |
| 401 | exp-v1-go-repair-0225 | Non-triviality hold: direct removal of extra one from supplied mean denominator. Integer sum bound is explicit. |
| 402 | exp-v1-go-repair-0226 | Criterion-positive: sorted-input validation plus distinct-run compaction and nil/empty shape preservation. |
| 403 | exp-v1-go-repair-0227 | Criterion-positive: ordered overlapping replacements must collapse CRLF before lone CR to avoid creating an extra newline. |
| 404 | exp-v1-go-repair-0228 | Criterion-positive: preserve former largest before replacement; distinct rank tracking without sentinel collision at int limits. |
| 405 | exp-v1-go-generation-0344 | Criterion-positive: concurrent vote count/history consistency and deterministic count/lexical standings with independent snapshots. |

Static review only; no new execution or full admission approval claimed.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

