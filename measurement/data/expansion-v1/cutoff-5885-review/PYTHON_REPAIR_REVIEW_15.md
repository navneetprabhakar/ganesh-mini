# Python repair review, batch 15

Positions 211–225 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Six new
additive holds: 835 additive plus historical three = 838; 2,142 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 211 | 0246 | Return after loop repairs truncated overline. Combining-class-zero implementation agrees with explicit rule; broader combining-character terminology and immutable identity wording pending. No new hold. |
| 212 | 0247 | Final run append repairs trailing selection loss. Per-frame ordinary independent copy agrees. Hold: finite deep selected frame fails copying. |
| 213 | 0248 | Optional digits repairs opening marker. Escaped labels and first-later closing agree. Horizontal whitespace breadth pending; no new hold. |
| 214 | 0249 | Bearer prefix repairs token comparison. Wraps, report identity and ordinary malformed headers agree. Token grammar/equality-subclass breadth pending; no new hold. |
| 215 | 0250 | Independent pre-operation snapshot repairs ledger assertions. Ordinary validation and conservation agree. Optimized-interpreter assertion behavior outside pinned execution pending; no new hold. |
| 216 | 0251 | Removing index adjustment repairs post-removal index. Hold: shared empty target/other columns cause unintended additional insertion. Global name-namespace wording pending. |
| 217 | 0252 | Prefix minima repair future-reading leakage. Independent channel state/new tuples and validation agree; no new hold. |
| 218 | 0253 | Absolute multiplier repairs negative operands. Shift-add invariant and arbitrary-size sign handling agree; no new hold. |
| 219 | 0254 | Per-character width check repairs overwide singleton. Explicit simplified width model and order agree; no new hold. |
| 220 | 0255 | Deepcopy repairs ordinary returned alias. Hold: early match skips malformed tail; finite deep match fails copying. |
| 221 | 0256 | Greater-or-equal eviction repairs capacity overflow. Ordinary oldest-first behavior agrees. Hold: finite deep value fails copying. No copy-failure atomicity invented. |
| 222 | 0257 | Per-request seen set repairs converging alias paths. Iterative traversal/reachable cycle scope agree; no new hold. |
| 223 | 0259 | Width stride repairs skipped items. Per-window independence agrees ordinarily. Hold: finite deep item fails copying. |
| 224 | 0260 | Strict interior split boundaries repair empty blocks. Negative/zero sums handled. Cubic repeated sums idiomatic-quality pending, no invented runtime bound or new hold. |
| 225 | 0258 | Second deepcopy repairs required consumption copy. Explicit copy-count test and one-use None handling agree. Hold: finite deep constructor payload fails copying. |

Six pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; seven failing test cases. Original tests read,
not newly rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0247 | repair_capture_runs_depth / repair-capture-runs-depth | 457 | bounded RecursionError |
| 0251 | repair_reposition_shared_empty / repair-reposition-shared-empty | 429 | unrelated column changed |
| 0255 | repair_find_record_contract / repair-find-record-contract | 666 | malformed tail ignored; bounded RecursionError |
| 0256 | repair_bounded_history_depth / repair-bounded-history-depth | 648 | bounded RecursionError |
| 0259 | repair_assign_windows_depth / repair-assign-windows-depth | 796 | bounded RecursionError |
| 0258 | repair_secret_envelope_depth / repair-secret-envelope-depth | 800 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 195 / 825 holds /
2,112 outside-sample inspections (QUALITY_STRATUM_825_BACKUP.md).
Continue position 226.
