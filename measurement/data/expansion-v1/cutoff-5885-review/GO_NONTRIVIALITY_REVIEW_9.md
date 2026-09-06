# Go focused non-triviality review — batch 9

Positions121–135, full prompt/reference read; not a full new test/mutant review.
Eight criterion-positive, seven non-triviality holds plus one behavioral hold.
1211 total holds (1208 additive+3),3065 unique outside inspections. Resume136.

| Position | ID | Finding |
| --- | --- | --- |
| 121 | exp-v1-go-repair-0064 | Non-triviality hold: disclosed upper-bound inclusive comparison correction. |
| 122 | exp-v1-go-generation-0099 | Criterion-positive: common increasing subsequence DP preserves per-right-index state and lower-value predecessor invariant in the required space bound. |
| 123 | exp-v1-go-generation-0100 | Criterion-positive: overflow-safe expiry and renewal/revision validation. Whether the returned renewal must itself have representable future expiry is not expressly stated; no new behavioral approval on that boundary. |
| 124 | exp-v1-go-generation-0101 | Criterion-positive: validation-before-replacement, original Unicode text preservation and sorted detached catalog values. |
| 125 | exp-v1-go-generation-0102 | Criterion-positive: account normalization, digest/token binding and failed-operation state rules; executed behavioral hold because altered newline-suffixed token is accepted. Toy password hashing is not a production recommendation. |
| 126 | exp-v1-go-repair-0065 | Non-triviality hold: direct divisor initialization from one to two. Full uint64 trial-division performance is not an executed timing finding. |
| 127 | exp-v1-go-repair-0066 | Non-triviality hold: directly replace assignment with delete in the explicitly named Remove branch; framing/order/error machinery is already supplied. |
| 128 | exp-v1-go-repair-0067 | Non-triviality hold: direct semicolon-to-comma literal correction in library splitter predicate. |
| 129 | exp-v1-go-repair-0068 | Criterion-positive: non-empty tree-path maximum must initialize from a real node, while preserving separate nil-tree behavior and recursive downward-gain invariant. |
| 130 | exp-v1-go-generation-0103 | Criterion-positive: usable zero-value registry, failure-preserving IDs and sorted detached snapshots. Eventual uint64 exhaustion is not a feasible executed probe here. |
| 131 | exp-v1-go-generation-0105 | Non-triviality hold: exact equality guard around strings.ToUpper. |
| 132 | exp-v1-go-generation-0106 | Criterion-positive: quantity and money overflow checks, metadata consistency and transactional snapshot restore. |
| 133 | exp-v1-go-repair-0069 | Non-triviality hold: direct parity-loop initial index correction in already supplied copy/sort/reinsert algorithm. |
| 134 | exp-v1-go-repair-0070 | Non-triviality hold: literal arithmetic addition-to-subtraction operator correction. |
| 135 | exp-v1-go-repair-0071 | Criterion-positive: buffer ownership correction preserves nil/non-nil-empty distinction and detaches mutations in both directions. |

go_0102_altered_token_probe-result.json: Go1.22.12 exit[1], no timeout,
27385ms. A publicly registered/authenticated account's valid token verifies,
and adding a newline to that token is incorrectly accepted despite the altered-token
rejection contract. Go base64 decoding ignores the suffix newline.
Additive test ran alongside original tests, not a separate known-bad rerun.
Network off,1CPU/512MiB/64PIDs/60s; task, code and output hashes retained.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
