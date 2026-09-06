# Python repair review, batch 3

Positions 31–45 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Seven new
additive holds: 750 additive plus historical three = 753; 1,962 unique
outside-sample inspections. Holds are pending review, not final rejections.
Source inspection is not seven-criterion approval, nontriviality admission
or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 31 | 0036 | Per-document normalized-topic set repairs duplicate contribution. Sorted keys/IDs, validation and ordinary detached containers agree. Scalar subclasses pending; no new hold. |
| 32 | 0037 | Left-first equal comparison repairs stable merging. Ascending order, fresh outer list and explicitly retained row identities agree; no new hold. |
| 33 | 0039 | Whitespace-cell filter repairs blank-row handling. Holds: CR-separated valid records rejected; valid 131073-character field rejected by inherited CSV field limit. |
| 34 | 0040 | Per-instance entries repair shared catalog state. Ordinary copies, validation and replacement agree. Hold: finite 600-level initial value raises RecursionError. |
| 35 | 0041 | Half-up expression repairs ordinary truncation. Hold: integer 2**52+1 at density 1 is spuriously increased by one. |
| 36 | 0042 | Starting at index 2 repairs selected positions. Ordinary ordering, shallow identity, fresh list and unorderable propagation agree; no new hold. |
| 37 | 0043 | Submission-order futures repair completion-order output. Standard executor bounds, one call per item and exact returned objects agree. Arbitrary worker side effects pending; no new hold. |
| 38 | 0044 | Source reservation repairs duplicate generated names. Source-first allocation and explicit collisions agree; no new hold. |
| 39 | 0045 | Product accumulation repairs quantity-only total. Hold: valid 4301-digit positive quantity with zero adjustment rejected by integer parsing limit. |
| 40 | 0046 | Percent normalization repairs quantile position. Hold: invalid unhashable scale produces TypeError rather than ValueError. Broader numeric boundaries pending. |
| 41 | 0047 | Removing clear from close repairs queue loss. Ordinary FIFO ownership transfer and closed-before-copy guard agree. Hold: finite 600-level add payload raises RecursionError. |
| 42 | 0048 | Independent deepcopy before each invocation repairs ordinary stage isolation. Copy failures explicitly allowed to propagate, so no depth hold. Immutable-object identity wording remains a contract question; no new hold. |
| 43 | 0049 | Correct style attribute repairs rendering. Frozen options and ordinary validation/rendering agree. Low-level mutation bypass not treated as ordinary API use; no new hold. |
| 44 | 0052 | Returning copied result repairs missing return. Ordinary event/result isolation and one call agree. Hold: finite 600-level handler-owned result cannot be copied. |
| 45 | 0053 | Actual request replaces fallback lookup. Skip behavior, exact response identity, configured header and natural missing-key behavior agree; no new hold. |

Seven pinned Python 3.11.15 network-disabled/resource-limited probes, each
exit 1 without timeout. Original tests read, not newly rerun by isolated
probes. Original candidates/tests/sample/partition unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0039 | repair_csv_record_boundary / repair-csv-record-boundary | 421 | two valid inputs raise ValueError |
| 0040 | repair_catalog_depth / repair-catalog-depth | 525 | bounded RecursionError diagnostic |
| 0041 | repair_canvas_integral_rounding / repair-canvas-integral-rounding | 492 | exact integer incremented by one |
| 0045 | repair_adjustment_decimal_width / repair-adjustment-decimal-width | 437 | valid quantity raises ValueError |
| 0046 | repair_position_scale_type / repair-position-scale-type | 637 | TypeError instead of ValueError |
| 0047 | repair_batch_depth / repair-batch-depth | 671 | bounded RecursionError diagnostic |
| 0052 | repair_event_result_depth / repair-event-result-depth | 500 | bounded RecursionError after one handler call |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch backed up in QUALITY_STRATUM_759_BACKUP.md.
Continue position 46.
