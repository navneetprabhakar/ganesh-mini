# Go focused non-triviality review — batch 19

Positions271–285, full prompt/reference read; not a full new test/mutant review.
Nine criterion-positive, six non-triviality holds plus one behavioral hold.
1270 total holds (1267 additive+3),3215 unique outside inspections. Resume286.

| Position | ID | Finding |
| --- | --- | --- |
| 271 | exp-v1-go-repair-0150 | Non-triviality hold: direct right-denominator operand substitution in supplied rational arithmetic. Known-bad unused variable is not a newly executed semantic-mutant finding. |
| 272 | exp-v1-go-repair-0151 | Non-triviality hold: add direct library sort to supplied intersection output. |
| 273 | exp-v1-go-generation-0229 | Criterion-positive: repository sentinel errors, full replacement validation and sorted detached state. Simultaneously malformed/unknown replacement precedence is not adjudicated here. |
| 274 | exp-v1-go-generation-0231 | Non-triviality hold: fixed field validation and directly specified hex/padded-decimal formatting. |
| 275 | exp-v1-go-generation-0233 | Criterion-positive: synchronous exactly-once action, done-before-callback transition and bounded remaining count. |
| 276 | exp-v1-go-generation-0234 | Criterion-positive catalog; executed behavioral hold because canonical decimal string IDs are unnecessarily restricted to machine int range. |
| 277 | exp-v1-go-repair-0153 | Non-triviality hold: direct exclusive count-loop boundary correction. |
| 278 | exp-v1-go-repair-0154 | Criterion-positive: non-empty minimum subarray initialization must include the first value and all-positive/singleton cases. |
| 279 | exp-v1-go-repair-0155 | Non-triviality hold: direct multiplicative accumulator identity correction. |
| 280 | exp-v1-go-repair-0156 | Criterion-positive: required pointer identity is the actual caller slice element, not a copied value; unlike detached-copy tasks, aliasing is intentional here. |
| 281 | exp-v1-go-repair-0157 | Criterion-positive: negative-depth prefix invalidates nested bracket language even if later openings restore final balance. |
| 282 | exp-v1-go-repair-0159 | Criterion-positive: exact decimal half-away rounding interacts with asymmetric positive/negative int64 limits, without float conversion. |
| 283 | exp-v1-go-repair-0160 | Non-triviality hold: direct NumOut-to-NumIn loop bound selector replacement. |
| 284 | exp-v1-go-generation-0241 | Criterion-positive: explicit error/skip/fail/pass precedence and corresponding per-zone counters preserve order. Exact detail text is intentionally flexible. |
| 285 | exp-v1-go-generation-0244 | Criterion-positive: reached-clause validation and first-match short-circuit mean later malformed rules must remain unexamined. |

go_0234_decimal_id_probe-result.json: Go1.22.12 exit[1], no timeout,
26831ms. Canonical positive decimal ID string 9223372036854775808 is rejected
although no numeric ID bound is in the prompt and the API stores strings.
The subsequent Get assertion was not reached. This is small input, not a huge
allocation or resource-envelope finding.
Additive test ran alongside original tests, not a separate known-bad rerun.
Network off,1CPU/512MiB/64PIDs/60s; task, code and output hashes retained.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
