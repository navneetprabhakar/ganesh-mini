# Python repair review, batch 22

Positions 316–330 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Seven new
additive holds: 880 additive plus historical three = 883; 2,247 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 316 | 0370 | Return-edge addition repairs cycle optimization. Hold: finite huge diagonal rejected; overflowed totals select wrong route. Empty-start wording distinguishes nonempty index rule. |
| 317 | 0371 | Destination validation plus original iteration repairs simultaneous rename/collision/order. Hold: finite deep field fails copying. |
| 318 | 0372 | Final append repairs dropped last group. Hold: finite deep first element fails copying. Ordinary equality/copies agree. |
| 319 | 0373 | Row copies repair input mutation. Explicit untouched-cell identity retained; no deeper copy invented. Self-referential row/cell wording pending, no new hold. |
| 320 | 0374 | Folded prefix repairs insensitive selection. Full validation, sort tie-break and original formatting agree; no new hold. |
| 321 | 0376 | Video-first key repairs tied event priority. Full source validation and within-source order agree. Hold: finite deep payload fails copying. |
| 322 | 0377 | Escape-aware split repairs colon separation. Duplicate decoded keys and trailing escapes agree. New immutable-string identity wording pending; no new hold. |
| 323 | 0378 | Next-character whitespace check repairs shared word-prefix acceptance. Unicode whitespace and full validation agree; no new hold. |
| 324 | 0380 | Finally close repairs resource leak. Explicit reader/copy/close exception precedence and stop behavior agree; no runtime-copy hold where propagation is expressly required. |
| 325 | 0381 | Sender condition repairs outgoing transfers. Exact scalar schema, mapping conversion and self-transfer independence agree. Outer sequence wording pending; no new hold. |
| 326 | 0382 | Correct modular difference repairs cycle winner. All nine pairs covered and validation agrees; no new hold. |
| 327 | 0383 | ASCII validation/direct conversion repairs permissive numeric parsing. Hold: 4999 leading zeroes before 1 triggers conversion limit. |
| 328 | 0384 | Strict upper comparison repairs interval boundary. Full validation, greatest compatible release and empty rules agree; no new hold. |
| 329 | 0385 | Boolean reverse repairs descending order. Hold: valid getitem iterable rejected and finite deep extra field fails copying. Validation-before-sort holds; copy-before-validation not prohibited. |
| 330 | 0386 | Multiplication repairs coverage division. Hold: zero coverage yields NaN for finite extreme dimensions; finite huge dimension rejected. |

Seven pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; ten failing/error test cases. Original tests read,
not newly rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0370 | repair_minimum_tour_numeric / repair-minimum-tour-numeric | 609 | OverflowError; wrong route |
| 0371 | repair_rename_fields_depth / repair-rename-fields-depth | 638 | bounded RecursionError |
| 0372 | repair_group_adjacent_depth / repair-group-adjacent-depth | 1414 | bounded RecursionError |
| 0376 | repair_merge_events_depth / repair-merge-events-depth | 1380 | bounded RecursionError |
| 0383 | repair_charge_leading_zero_limit / repair-charge-leading-zero-limit | 511 | ValueError |
| 0385 | repair_select_records_contract / repair-select-records-contract | 721 | TypeError; bounded RecursionError |
| 0386 | repair_covered_area_extremes / repair-covered-area-extremes | 780 | NaN; OverflowError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 315 / 876 holds /
2,232 outside-sample inspections (QUALITY_STRATUM_876_BACKUP.md).
Continue position 331.
