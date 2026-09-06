# Python generation review, batch 32

Positions 466–480 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; four reproduced holds.
654 additive plus historical three = 657 holds; 1,713 unique outside-sample
inspections. No seven-criterion approval. Continue position 481.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 466 | 0540 | Iterative recurrence, modular arithmetic and empty-strip base case agree. Unbounded large-width performance remains a quality consideration; no new functional hold. |
| 467 | 0542 | Value/index ordering, descending odd assignment and fresh results agree; no new hold. |
| 468 | 0543 | Ordinary cycle detection, direct-key-before-descendant search, first occurrence and copied results agree. Deep trees, unsupported container leaves and scalar-root wording pending; no new hold. |
| 469 | 0545 | Majority cancellation plus strict two-thirds verification uses constant auxiliary space and preserves inputs; no new hold. |
| 470 | 0541 | Hold: exact Fraction greater than one accepted after float rounding. Ordinary sorted scores, reverse ranks and suffix minima agree with tests. Float formula versus decimalized computation and custom Real domains pending. |
| 471 | 0544 | Class inheritance/attributes, exact output key order and ordinary metadata copies agree. Arbitrary-copy and post-construction attribute mutation domains pending; no new hold. |
| 472 | 0546 | Hold: unhashable unsupported kind leaks TypeError instead of ValueError. Ordinary global ID uniqueness and project-scoped freezing agree. Parent-ID validation and directly constructed record validation pending. |
| 473 | 0547 | Ordinary expiration boundaries, lazy removal, replacement and None payload distinction agree. Arbitrary deepcopy/scalar-key domains pending; no new hold. |
| 474 | 0549 | Hold: finite cancelling large integers fail at float-based finiteness check although required total/mean are representable. Ordinary single consumption and normal arithmetic agree. |
| 475 | 0550 | Ordinary ID validation, monotonic IDs, toggle/delete and metadata copies agree. Exceptional-copy and mutable scalar-summary domains pending; no new hold. |
| 476 | 0551 | Ordered aliases, same-command identity, cross-command independence and collision checks agree. Shared one-shot iterable and arbitrary-copy domains pending; no new hold. |
| 477 | 0555 | Ordinary ASCII handle grammar, lowercase reservation check and age validation agree. Unicode casefold versus explicit lowercase normalization remains pending; no new hold. |
| 478 | 0556 | Hold: valid finite large-integer cell raises OverflowError in math.isfinite. Ordinary strict neighbors, cutoff, value preservation and sort order agree. |
| 479 | 0557 | Exact bool validation, cohort first order and FP/FN denominators including zero cases agree ordinarily; no new hold. |
| 480 | 0559 | Ordinary earliest unanswered items, client isolation, completion invalidation and report ordering agree. Equality-compatible non-string domains and embedded report line breaks pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up;
see QUALITY_STRATUM_657_BACKUP.md for verified evidence through position 480.

Four pinned Python 3.11.15 probe runs, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0541 | risk_fraction_range_probe.py / risk-fraction-range-result.json | 335 | Fraction greater than one accepted. |
| 0546 | portfolio_unhashable_kind_probe.py / portfolio-unhashable-kind-result.json | 570 | Unsupported list kind leaks TypeError. |
| 0549 | measure_cancelling_large_integers_probe.py / measure-cancelling-large-integers-result.json | 342 | OverflowError instead of count 2, total 0, mean 0. |
| 0556 | plateau_large_integer_probe.py / plateau-large-integer-result.json | 397 | OverflowError instead of one qualifying cell. |
