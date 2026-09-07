# Go focused non-triviality review — batch 31

Positions451–465, full prompt/reference read; not a full new test/mutant review.
Six criterion-positive, nine non-triviality holds plus one static behavioral hold.
1346 total holds (1343 additive+3),3395 unique outside inspections. Resume466.

| Position | ID | Finding |
| --- | --- | --- |
| 451 | exp-v1-go-repair-0256 | Non-triviality hold: direct exclusive loop boundary for supplied half-open sum. |
| 452 | exp-v1-go-generation-0386 | Criterion-positive strict manifest task; static behavioral hold: struct decoding accepts case-insensitive field-name matches despite exact required JSON fields. DisallowUnknownFields does not enforce exact spelling; e.g. ITEMS and NEXT_CURSOR satisfy tagged pointers. |
| 453 | exp-v1-go-generation-0387 | Criterion-positive: ordered option application, validation before severity suppression and exact non-mutating encoding. |
| 454 | exp-v1-go-generation-0389 | Non-triviality hold: fixed describe/echo/upper response table with direct library case conversion. |
| 455 | exp-v1-go-repair-0258 | Criterion-positive: allocation must cap the served amount to remaining capacity while preserving later zero allocations. |
| 456 | exp-v1-go-generation-0391 | Non-triviality hold: two literal constructors and direct string equality. |
| 457 | exp-v1-go-generation-0395 | Non-triviality hold: fixed three-component label mapping, enabled-set insertion and library sorting. |
| 458 | exp-v1-go-generation-0396 | Criterion-positive: validate both collections before inclusive containment counts, preserving duplicate records and window order. |
| 459 | exp-v1-go-repair-0261 | Non-triviality hold: literal minimum-distinct-count four-to-three correction. |
| 460 | exp-v1-go-repair-0262 | Non-triviality hold: move explicitly named FailureInternal into the retryable switch case. |
| 461 | exp-v1-go-repair-0263 | Non-triviality hold: substitute directly specified six-ASCII-whitespace membership for Unicode library classification. |
| 462 | exp-v1-go-repair-0264 | Criterion-positive: copy caller bytes on ingress as well as egress; mutex alone cannot prevent external alias mutation. |
| 463 | exp-v1-go-generation-0398 | Non-triviality hold: fixed trim/default/format wrapper over package string variables. |
| 464 | exp-v1-go-generation-0399 | Criterion-positive: exact payload digest then canonical-text HMAC/base64 pipeline. Client-ID newlines are not prohibited; remaining fields constrain boundaries, and no extra rejection is invented. |
| 465 | exp-v1-go-repair-0265 | Non-triviality hold: direct bit-width minus-one correction in supplied signed-range formula. |

Static review only. generation0386 uses struct field matching, the same exact-
key issue demonstrated by prior go_0195_exact_patch_keys_probe-result.json; no new
execution is claimed for this record. A minimal example is an empty ITEMS array
and NEXT_CURSOR:0. Both required pointers become non-nil under folded matching.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
