# Python repair review, batch 20

Positions 286–300 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Four new
additive holds: 870 additive plus historical three = 873; 2,217 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 286 | 0333 | Ignore both file-header prefixes repairs added count. Exact prefixes, splitlines and frozen output agree; no new hold. |
| 287 | 0334 | Added closing bracket repairs punctuation trimming. Hold: malformed ports retained. Query/fragment preservation and suffix selection otherwise agree. |
| 288 | 0335 | Whole-structure deepcopy repairs cross-profile topology. Exact outer-list and supported-cycle requirements agree; no new hold. Explicit deepcopy support informs scope; runtime/custom-copy breadth remains pending. |
| 289 | 0337 | Separate y factor repairs scaling. Validation, new tuples/order agree. Native arithmetic boundary behavior pending; no extra finiteness requirement invented. No new hold. |
| 290 | 0338 | Binary label repairs legacy extension classification. Casefold and suffix boundaries agree; no new hold. |
| 291 | 0339 | Empty safe set repairs key slash encoding. Component validation and ordinary UTF-8 agree. Ill-formed Unicode has no specified encoding policy; no new hold. |
| 292 | 0341 | Doubling closing brackets repairs identifier quoting. Every occurrence/empty/type rules agree; no new hold. Minor spacing style only. |
| 293 | 0342 | Deep snapshot repairs nested alias. Hold: valid falsey child iterable discarded. Deepcopy runtime breadth remains pending. |
| 294 | 0343 | Previous-border indexing repairs fallback. KMP overlap, empty boundaries and fresh lists agree; no new hold. |
| 295 | 0344 | Index tie-break repairs fractional allocation order. Exact integer arithmetic, validation and minima agree; no new hold. |
| 296 | 0345 | Full length bound repairs dropped partial polling batch. Dedup order/validation/empty agree; no new hold. |
| 297 | 0346 | Nonmutating slices repair dequeue mutation. Hold: finite deep first row fails copying. Cross-result alias preservation not required. |
| 298 | 0347 | Wildcard substitution repairs advertised address. Hold: integer/boolean hosts accepted and bind string canonicalized contrary to literal return contract. |
| 299 | 0348 | Modulo repairs worker round-robin. Duplicate thread occurrences and process validation agree; no new hold. |
| 300 | 0349 | Selected-list return repairs ignored filtering. Boolean exclusion, order/duplicates/freshness agree; no new hold. |

Four pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; eight failing/error assertions including subtests.
Original tests read, not newly rerun by isolated probes.
Candidate/test/sample/partition unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0334 | repair_resource_links_port / repair-resource-links-port | 451 | two malformed ports retained |
| 0342 | repair_panel_falsey_iterable / repair-panel-falsey-iterable | 499 | valid children lost |
| 0346 | repair_dequeue_snapshot_depth / repair-dequeue-snapshot-depth | 488 | bounded RecursionError |
| 0347 | repair_endpoint_contract / repair-endpoint-contract | 446 | three invalid types accepted; bind changed |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 285 / 869 holds /
2,202 outside-sample inspections (QUALITY_STRATUM_869_BACKUP.md).
Continue position 301.
