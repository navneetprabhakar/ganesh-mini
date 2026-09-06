# Python generation review, batch 23

Positions 331–345 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; six reproduced holds.
612 additive plus historical three = 615 holds; 1,578 unique outside-sample
inspections. No seven-criterion approval. Continue position 346.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 331 | 0379 | Abstract API, action arithmetic, once input materialization and fresh ordered results agree ordinarily. Direct-action validation and non-string token policy remain pending; no new hold. |
| 332 | 0382 | Hold: huge out-of-range integer overflows in finite check instead of required ValueError. Ordinary bounded readings and list copies agree. |
| 333 | 0383 | Frequency ranking, first-appearance ties, distinct-count limit and once iteration agree; no new hold. |
| 334 | 0384 | Hold: valid 1200-step acyclic chain exceeds recursive traversal depth. Ordinary dependency ordering, shared prerequisite execution and registration copies agree. No preflight atomicity requirement inferred. |
| 335 | 0380 | Hold: huge integer unit count with zero floating rate raises OverflowError instead of zero pay. Other rounding/numeric breadth remains pending. |
| 336 | 0385 | Independent batch dictionaries, exact stock arithmetic, order and validation agree for ordinary scalar values. Shallow copy versus explicit deep-copy requirement for scalar subclasses remains pending; no new hold. |
| 337 | 0386 | Whole-list deep copy, original order, matching update and duplicate validation agree ordinarily. Arbitrary copy behavior and cross-record alias semantics remain pending; no new hold. |
| 338 | 0387 | Exact inclusive bounds, category order, complete validation and independent lists agree; no new hold. |
| 339 | 0388 | Round-robin removal, snapshot rotation and step copies agree ordinarily. Arbitrary copy failures and mutable scalar-subclass isolation remain pending; no new hold. |
| 340 | 0389 | First-seen axes, integer sums, zero fill and independent lists agree; no new hold. Scalar subclass breadth remains pending. |
| 341 | 0390 | Capacity, oldest eviction, zero retention and accessor deep copies agree ordinarily. Arbitrary copy behavior remains pending; no new hold. |
| 342 | 0391 | Address normalization, blank-recipient skipping, ordered deduplication and per-batch metadata copies agree ordinarily. Arbitrary copy behavior remains pending; no new hold. |
| 343 | 0392 | Hold: identical finite large positive-area boxes produce NaN IoU. Ordinary geometry and sorted frame summaries agree. Center overflow and pre-normalization exactness remain pending. |
| 344 | 0394 | Hold: valid max_checks=10**30 causes islice ValueError even with empty snapshots. Ordinary bounded replacement and validation atomicity agree. Zero-check iterator initialization and arbitrary copy behavior remain pending. |
| 345 | 0393 | Hold: nonempty whitespace client rejected contrary to prompt; original test specifies that stricter behavior. Ordinary counters, per-client reset and snapshot copies agree. Identity-sensitive window equality remains pending. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up
under QUALITY_STRATUM_623_BACKUP.md, through Python position 360.

Six pinned Python 3.11.15 probe runs, network disabled/resource limited, all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0382 | monitor_huge_out_of_range_probe.py / monitor-huge-out-of-range-result.json | 341 | OverflowError instead of ValueError. |
| 0384 | workflow_deep_chain_probe.py / workflow-deep-chain-result.json | 321 | RecursionError before successful traversal. |
| 0380 | piecework_huge_units_zero_rate_probe.py / piecework-huge-units-zero-rate-result.json | 326 | Integer-to-float overflow before zero multiplication. |
| 0392 | box_large_identical_iou_probe.py / box-large-identical-iou-result.json | 330 | NaN instead of 1.0. |
| 0394 | device_huge_check_limit_probe.py / device-huge-check-limit-result.json | 323 | islice limit ValueError instead of TimeoutError. |
| 0393 | quota_nonempty_whitespace_client_probe.py / quota-nonempty-whitespace-client-result.json | 411 | ValueError for nonempty client. |
