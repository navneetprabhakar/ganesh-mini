# Go focused non-triviality review — batch 7

Positions91–105, full prompt/reference read; not a full new test/mutant review.
Eleven criterion-positive, four non-triviality holds plus two behavioral holds.
1196 total holds (1193 additive+3),3035 unique outside inspections. Resume106.

| Position | ID | Finding |
| --- | --- | --- |
| 91 | exp-v1-go-repair-0046 | Non-triviality hold: direct zero-inclusive filter comparison. |
| 92 | exp-v1-go-repair-0047 | Non-triviality hold: compare already constructed set sizes rather than input lengths. |
| 93 | exp-v1-go-repair-0048 | Criterion-positive adjacent-span/tie invariant; executed behavioral hold for signed subtraction overflow. |
| 94 | exp-v1-go-generation-0073 | Criterion-positive: full constructor validation, unique insertion and independent shelf snapshots. |
| 95 | exp-v1-go-generation-0074 | Criterion-positive: validated stock mutation and sorted pantry snapshots; arithmetic explicitly fits int. |
| 96 | exp-v1-go-generation-0075 | Criterion-positive: factory validation, independent resolver map and returned byte ownership. No unstated protection against source callback mutating its argument. |
| 97 | exp-v1-go-generation-0077 | Criterion-positive: retry-local map ownership, controller mutation allowance and resource path grammar. |
| 98 | exp-v1-go-generation-0078 | Criterion-positive: predicate-once ordered emission, duplicate preservation and immediate attachment semantics. No added callback-reentrancy requirement. |
| 99 | exp-v1-go-repair-0049 | Non-triviality hold: direct removal of extra one from math.Mod wrapper. |
| 100 | exp-v1-go-repair-0051 | Criterion-positive: snapshot copies mutable tally state instead of exporting the live map. |
| 101 | exp-v1-go-generation-0076 | Criterion-positive: value-based policy deduplication, ordered removal and snapshot independence. |
| 102 | exp-v1-go-generation-0079 | Criterion-positive: normalized email uniqueness, validation and no plaintext secret storage. Not a recommendation of this toy secret hash for production authentication. |
| 103 | exp-v1-go-generation-0082 | Non-triviality hold: direct badge regex and map lookup/error wrappers. |
| 104 | exp-v1-go-generation-0083 | Criterion-positive: complete prevalidation, deterministic artifact ordering and independent option copies. No unstated line-escaping requirement. |
| 105 | exp-v1-go-generation-0084 | Criterion-positive AST matching; executed behavioral hold because Unicode lowercasing violates explicitly ASCII-only folding. |

go_0048_span_overflow_probe-result.json: Go1.22.12 exit[1], no timeout,
28355ms. Input MinInt64,0,1 selects (MinInt64,0) instead of (0,1).
go_0084_ascii_fold_probe-result.json: Go1.22.12 exit[1], no timeout,
29981ms. AK and A followed by Kelvin sign incorrectly match under ASCII-only folding.
Both additive tests ran alongside original tests, not separate known-bad reruns.
Network off,1CPU/512MiB/64PIDs/60s; task, code and output hashes retained.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
