# Go focused non-triviality review — batch 32

Positions466–480, full prompt/reference read; not a full new test/mutant review.
11 criterion-positive, four non-triviality holds plus one static behavioral hold.
1351 total holds (1348 additive+3),3410 unique outside inspections. Resume481.

| Position | ID | Finding |
| --- | --- | --- |
| 466 | exp-v1-go-repair-0266 | Criterion-positive: reject negative-depth prefixes before bracket slicing can use an invalid start; final balance alone is insufficient. |
| 467 | exp-v1-go-generation-0403 | Criterion-positive: concurrent composite-key vault with validated identifiers/kind and defensive byte ownership. |
| 468 | exp-v1-go-generation-0406 | Criterion-positive: read-only expiry lookup must preserve cache for later earlier-time observations; concurrent access and exact boundary. |
| 469 | exp-v1-go-generation-0407 | Criterion-positive: validate unrelated observations, default ports and first-requested-port deduplication with existential exposure matching. No actual networking. |
| 470 | exp-v1-go-generation-0408 | Criterion-positive: concurrent replacement/reset/expiry lifecycle and remaining-lifetime comparison without uint64 addition overflow. |
| 471 | exp-v1-go-repair-0270 | Criterion-positive: collapse mixed separator runs using parser state while trimming boundary runs and preserving character order. |
| 472 | exp-v1-go-repair-0271 | Non-triviality hold: direct inclusive maximum-run comparator correction. |
| 473 | exp-v1-go-repair-0272 | Non-triviality hold: exact prefix literal capitalization change; regex/name logic already supplied. |
| 474 | exp-v1-go-generation-0409 | Criterion-positive partial-update ownership/atomicity; static behavioral hold: empty code returns zero before lookup even when table contains that key, contrary to original-item-on-any-error requirement. |
| 475 | exp-v1-go-generation-0410 | Criterion-positive: validate all destinations before filtered receipts, with exact uniqueness and preserved source text. |
| 476 | exp-v1-go-generation-0411 | Non-triviality hold: directly transcribed fixed path/method response table. |
| 477 | exp-v1-go-generation-0414 | Criterion-positive: decorator retains actual response and records after completed call, including nil-handler fallback. No unrequested concurrency/reentrancy contract. |
| 478 | exp-v1-go-repair-0273 | Criterion-positive: range byte offsets identify rune boundaries without copying or splitting immutable input strings. |
| 479 | exp-v1-go-repair-0276 | Non-triviality hold: direct nonpositive base-case guard in supplied bounded countdown recurrence. |
| 480 | exp-v1-go-generation-0415 | Criterion-positive: concurrent idle bound, ingress copies and zeroing reused blocks while preserving exact length/capacity. |

Static review only. For generation0409, table may contain an empty key because
no global table invariant forbids it. Calling with code="" must still fail, but
the explicit error-result contract requires its existing original item; the
reference returns the zero item. No executed result claimed for this record.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

