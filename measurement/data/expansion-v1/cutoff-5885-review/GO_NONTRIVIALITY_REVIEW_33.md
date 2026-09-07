# Go focused non-triviality review — batch 33

Positions481–495, full prompt/reference read; not a full new test/mutant review.
Ten criterion-positive, five non-triviality holds plus one static behavioral hold.
1357 total holds (1354 additive+3),3425 unique outside inspections. Resume496.

| Position | ID | Finding |
| --- | --- | --- |
| 481 | exp-v1-go-generation-0417 | Criterion-positive: price/time priority matching with residual quantities, offer-price execution and no caller mutation. |
| 482 | exp-v1-go-generation-0419 | Criterion-positive: normalize before duplicate detection, atomic ordered replacement and stable-position updates. Pointer methods implement the declared interface. |
| 483 | exp-v1-go-generation-0420 | Non-triviality hold: fixed field grammar validation and five-line literal manifest formatting. |
| 484 | exp-v1-go-repair-0277 | Criterion-positive: first-occurrence deduplication makes additions-before-existing precedence semantically significant. |
| 485 | exp-v1-go-repair-0278 | Non-triviality hold: direct inclusive full-prefix loop boundary; UTF-8/rune handling already supplied. |
| 486 | exp-v1-go-repair-0279 | Criterion-positive: each decoded field must detach from input and other fields while preserving zero-length fields. |
| 487 | exp-v1-go-generation-0421 | Criterion-positive: authenticated atomic coupon-state copy and constant-time signature comparison. NUL concatenation is expressly prescribed; tuple-framing security weakness is not misreported as reference noncompliance. |
| 488 | exp-v1-go-generation-0422 | Criterion-positive catalog task; static behavioral hold: concatenating title, NUL and author introduces cross-field keyword matches absent from either field. |
| 489 | exp-v1-go-generation-0423 | Criterion-positive: validate every notice, descending sequence cursor and next-cursor only when an additional match exists. |
| 490 | exp-v1-go-generation-0426 | Criterion-positive: permit identity/update/delete state with independent sorted listing; extension explicitly replaces, not necessarily increases, expiration. |
| 491 | exp-v1-go-repair-0281 | Non-triviality hold: direct standard-library decimal formatting replaces rune conversion. No new known-bad compilation result claimed. |
| 492 | exp-v1-go-repair-0282 | Non-triviality hold: direct errors.Is replacement for supplied sentinel comparisons. Multi-target joined-error precedence remains unadjudicated. |
| 493 | exp-v1-go-repair-0283 | Criterion-positive: pointer receiver is needed for persistent mutation through the Adder interface across calls. |
| 494 | exp-v1-go-repair-0284 | Non-triviality hold: directly invert explicitly identified map-presence condition. Mixed missing/empty request precedence not adjudicated here. |
| 495 | exp-v1-go-generation-0427 | Criterion-positive: positive-charge sliding window maximizes retained length with stable earliest-left tie; sum bound expressly supplied. |

Static review only. generation0422: Title="a", Author="b", Keyword="a\x00b"
matches joined text but is a substring of neither title nor author. No input
rule excludes NUL keywords. No execution claimed for this record.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

