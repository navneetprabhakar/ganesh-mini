# Go focused non-triviality review — batch 26

Positions376–390, full prompt/reference read; not a full new test/mutant review.
10 criterion-positive. Five non-triviality holds plus two behavioral holds.
1313 total holds (1310 additive+3),3320 unique outside inspections. Resume391.

| Position | ID | Finding |
| --- | --- | --- |
| 376 | exp-v1-go-repair-0212 | Non-triviality hold: direct two-byte shift/operand swap for explicitly specified big-endian length. |
| 377 | exp-v1-go-generation-0319 | Criterion-positive: argument validation precedes accessed-key reporting; decode into existing destination and marshal-before-store atomicity. |
| 378 | exp-v1-go-generation-0321 | Criterion-positive: independent template compilation retains all successes and ordered failures instead of short-circuiting. |
| 379 | exp-v1-go-generation-0322 | Criterion-positive: immutable error-detail ownership through constructor, accessor and derived-error operation. |
| 380 | exp-v1-go-generation-0323 | Non-triviality hold: fixed integer/enum/string lookup table with range guards. |
| 381 | exp-v1-go-repair-0213 | Non-triviality hold: direct DecodeLastRune/IsDigit library substitution in supplied validator. |
| 382 | exp-v1-go-repair-0215 | Criterion-positive: ordered intersection must retain first-left occurrence rather than iterate the membership map. |
| 383 | exp-v1-go-repair-0216 | Non-triviality hold: explicitly identified strict-to-inclusive loop comparator; overflow guards are already supplied unchanged. |
| 384 | exp-v1-go-generation-0325 | Criterion-positive: concurrent vault with digest-only storage and optional replacement preservation. Astronomical uint64 ID exhaustion not executed or approved. |
| 385 | exp-v1-go-generation-0326 | Criterion-positive layout validation/serialization; executed behavioral hold: span sum wraps and bypasses capacity rejection. |
| 386 | exp-v1-go-generation-0327 | Criterion-positive concurrent ledger; executed behavioral hold: mean of identical finite observations overflows to infinity. |
| 387 | exp-v1-go-generation-0328 | Criterion-positive: validate complete input before effects; ordered success prefix and wrapped original failure. |
| 388 | exp-v1-go-repair-0217 | Criterion-positive: reset reusable buffer between frames while retaining independently copied results. |
| 389 | exp-v1-go-repair-0218 | Criterion-positive: count previously seen same-residue index pairs rather than complementary residues; negative normalization retained. |
| 390 | exp-v1-go-repair-0219 | Non-triviality hold: directly reject odd-length input rather than prepending zero in a supplied hex decoder. |

Executed additive probes, Go1.22.12 exit[1], no timeout:
- go_0326_layout_overflow_probe-result.json,29648ms: two segments MaxInt and1 with capacity MaxInt are accepted after signed overflow.
- go_0327_finite_mean_probe-result.json,29856ms: two MaxFloat64 observations yield +Inf,true instead of their representable common value.
Original tests retained. Network off,1CPU/512MiB/64PIDs/60s; complete task,
code, runtime/output hashes in receipts. No new known-bad rerun claimed.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

