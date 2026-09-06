# Python repair review, batch 16

Positions 226–240 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Five new
additive holds: 840 additive plus historical three = 843; 2,157 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 226 | 0261 | Break repairs normal STOP termination. Snapshot, duplicate handlers and payload identity agree; no new hold. |
| 227 | 0262 | Retained buffer repairs bidirectional view aliasing. Factory validation/read-only shape property agree. Direct constructor scope and caller resizing behavior unspecified; no new hold. |
| 228 | 0263 | Per-result deepcopy repairs nested aliases. Full directory validation and duplicate independence agree ordinarily. Hold: finite deep present data fails copying. |
| 229 | 0264 | Seen-name lookup repairs resource collision. Immutable payload snapshots and ordinary entry handling agree. Entry protocol breadth pending; no new hold. |
| 230 | 0266 | Ascending sort repairs minimum spanning selection. Normalized tie order, direct-link matrix and self-links agree. Hold: finite huge cost overflows validation. |
| 231 | 0269 | Maximum y1 repairs enclosing rectangle. Hold: reversed integer bounds hidden by float rounding and finite huge coordinate rejected. |
| 232 | 0270 | Snapshot deepcopy repairs exposed payload. Sorted names and ordinary replacement agree. Hold: finite deep put fails copying. |
| 233 | 0271 | Subtraction repairs removal. Ordered underflow/validation and detached levels agree; no new hold. |
| 234 | 0272 | Deepcopy repairs flattened value aliases. Value scope explicitly limited to deepcopy-supported values; no new depth hold. Normalized duplicate validation/order agree. |
| 235 | 0274 | Row/column correspondence repairs Manhattan distance. Row-major ties and independent result rows agree. All-marker scan idiomatic-quality pending; no new hold. |
| 236 | 0275 | Break repairs processing beyond quit. Hold: legacy iterable rejected and large coordinate formatting fails. Exact field validation/quit short-circuit agree ordinarily. |
| 237 | 0276 | Dictionary comprehension repairs shared notices. Zero count, independent calls and no-I/O source agree; no new hold. |
| 238 | 0277 | Right-minus-left repairs asymmetric inventory difference. Sorted mismatch order and validation agree; no new hold. |
| 239 | 0278 | Continue repairs premature return after push. Stop/drop and malformed instructions agree. Outer program scope unspecified; no new hold. |
| 240 | 0279 | Reset current repairs record closure. Duplicate fields, empty records and independent dictionaries agree. Whitespace normalization wording pending; no new hold. |

Five pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; seven failing/error test cases. Original tests read,
not newly rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0263 | repair_merge_directory_depth / repair-merge-directory-depth | 799 | bounded RecursionError |
| 0266 | repair_minimum_network_large_integer / repair-minimum-network-large-integer | 751 | OverflowError |
| 0269 | repair_line_bounds_precision / repair-line-bounds-precision | 479 | reversed bounds accepted; OverflowError |
| 0270 | repair_reading_vault_depth / repair-reading-vault-depth | 629 | bounded RecursionError |
| 0275 | repair_summarize_events_contract / repair-summarize-events-contract | 660 | TypeError / ValueError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 225 / 838 holds /
2,142 outside-sample inspections (QUALITY_STRATUM_838_BACKUP.md).
Continue position 241.
