# Go focused non-triviality review — batch 28

Positions406–420, full prompt/reference read; not a full new test/mutant review.
10 criterion-positive. 1325 total holds (1322 additive+3),3350 unique
outside inspections. Resume421.

| Position | ID | Finding |
| --- | --- | --- |
| 406 | exp-v1-go-generation-0346 | Criterion-positive: error accumulation, errors.Is join and clear-on-flush lifecycle. Simultaneous nil destination/oversized payload precedence remains unadjudicated. |
| 407 | exp-v1-go-generation-0348 | Criterion-positive: category equivalence and contextual unwrap/identity rules. Non-nil cause with empty Error text has underspecified formatting; no added nil-receiver requirement. |
| 408 | exp-v1-go-repair-0229 | Non-triviality hold: direct 42-to-zero maximum initialization. |
| 409 | exp-v1-go-repair-0230 | Non-triviality hold: direct zero-inclusive input guard; full-range square-search logic already supplied. |
| 410 | exp-v1-go-repair-0231 | Non-triviality hold: direct inclusive grace comparator. Also executed equal-speed arrival-gap failure from Inf minus Inf. |
| 411 | exp-v1-go-repair-0232 | Non-triviality hold: direct omitted-last-segment repair in supplied join loop. |
| 412 | exp-v1-go-generation-0345 | Criterion-positive: mode selection, detached decoded credentials and exact human/standard-JSON rendering. Base64 decoder permissiveness not adjudicated here. |
| 413 | exp-v1-go-generation-0349 | Criterion-positive command/state task; static contract hold: badgeSet rejects whitespace-only badges although badge rule rejects empty names, unlike the expressly trim-aware board/member rules. Score-overflow policy remains unadjudicated. |
| 414 | exp-v1-go-generation-0352 | Criterion-positive: assigned identity, atomic revisions, sorted filtered queries and defensive ingredient copies. No requirement for zero-value cookbook or executed astronomical ID exhaustion. |
| 415 | exp-v1-go-generation-0353 | Criterion-positive: capacity/level invariant checked by remaining capacity to avoid overflow; exact drain and nil contracts. |
| 416 | exp-v1-go-repair-0233 | Criterion-positive numeric normalization; executed behavioral hold: adjacent large int endpoints collapse on float conversion and become NaN. |
| 417 | exp-v1-go-repair-0234 | Criterion-positive: non-mutating maximum-distinct-rune selection with lexical tie break. |
| 418 | exp-v1-go-repair-0236 | Non-triviality hold: direct middle-element condition correction in supplied alternating-extremes routine. |
| 419 | exp-v1-go-generation-0358 | Criterion-positive: method/action precedence, structured error creation, byte-exact JSON echo and detached response storage. |
| 420 | exp-v1-go-generation-0360 | Criterion-positive full-input severity validation/filtering; executed behavioral hold: Unicode dotted-I accepted despite ASCII-only case-insensitive parsing. |

Five non-triviality holds plus three distinct behavioral/static holds; repair0231
has both non-triviality and behavioral findings but is counted only once.
Executed additive probes, Go1.22.12 exit[1], no timeout:
- go_0231_equal_speed_probe-result.json,27101ms: equal smallest-positive speeds and distance1/grace0 produce found=false, though equal speeds have zero arrival gap. Probe asserts eligibility, not finite representability of travel time.
- go_0233_endpoint_precision_probe-result.json,27501ms: [2^53,2^53+1] produces [NaN,NaN] instead of [0,1] on pinned 64-bit runtime.
- go_0360_ascii_case_probe-result.json,27451ms: U+0130NFO is accepted as Info.
Original tests retained; network off,1CPU/512MiB/64PIDs/60s. Full task, code,
runtime/output hashes retained. No executed badge/score claim.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

