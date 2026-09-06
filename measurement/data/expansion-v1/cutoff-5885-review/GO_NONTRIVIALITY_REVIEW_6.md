# Go focused non-triviality review — batch 6

Positions76–90, full prompt/reference read; not a full new test/mutant review.
Twelve criterion-positive, three non-triviality holds plus one behavioral hold.
1190 total holds (1187 additive+3),3020 unique outside inspections. Resume91.

| Position | ID | Finding |
| --- | --- | --- |
| 76 | exp-v1-go-generation-0062 | Criterion-positive: locked case-insensitive uniqueness, patch validation before commit and ID exhaustion. Unicode lowercase filtering versus EqualFold uniqueness is not a new executed finding. |
| 77 | exp-v1-go-generation-0063 | Criterion-positive: exact per-job goroutine invocation, index-stable results and wait-group synchronization. Panic behavior expressly excluded. |
| 78 | exp-v1-go-generation-0064 | Criterion-positive: complete exact-key configuration, typed values and parse-before-callback/error identity. Nil-interface scope explicit. |
| 79 | exp-v1-go-generation-0065 | Criterion-positive: sync.Once publication preserves one shared immutable first-namespace instance across concurrent callers. |
| 80 | exp-v1-go-generation-0066 | Criterion-positive: locked validation, monotonic/exhausted ID state and independent ordered snapshots. |
| 81 | exp-v1-go-repair-0041 | Criterion-positive: nested-depth parser retains byte offsets and rejects unmatched braces without partial groups. |
| 82 | exp-v1-go-repair-0042 | Criterion-positive: private typed context key avoids unrelated string-key collision while preserving child context and nil fallback. |
| 83 | exp-v1-go-repair-0043 | Non-triviality hold: elementary missing remaining-stock decrement in direct greedy allocation. |
| 84 | exp-v1-go-repair-0044 | Non-triviality hold: direct doubled-underscore literal correction in prescribed space-run encoding. |
| 85 | exp-v1-go-generation-0067 | Criterion-positive: defaults snapshot plus per-message precedence and separate returned map ownership. |
| 86 | exp-v1-go-generation-0068 | Criterion-positive: strict JSON decode/trailing-value checks and locked first-success-only initialization. No unstated JSON duplicate-key rejection. |
| 87 | exp-v1-go-generation-0069 | Criterion-positive: exact required-key parsing, password-free rendering and exact-origin comparison. Decimal sign grammar remains outside focused approval. |
| 88 | exp-v1-go-generation-0071 | Criterion-positive: global IDs, locked referential integrity and sorted independent member snapshots. |
| 89 | exp-v1-go-generation-0072 | Criterion-positive renderer, executed behavioral hold: Go string quoting emits a backslash-a escape invalid in JSON. |
| 90 | exp-v1-go-repair-0045 | Non-triviality hold: explicitly required alphabet-size literal replacement in shift wrapper. |

go_0072_json_control_probe-result.json: Go1.22.12, exit[1], no timeout,
27526ms. ASCII BEL is valid UTF-8 input; FormatJSON emits invalid JSON because
strconv.Quote uses a Go-only escape. json.Valid independently rejects it.
Additive test runs alongside original tests; no separate known-bad rerun.
Network off,1CPU/512MiB/64PIDs/60s; full task/output hashes retained.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
