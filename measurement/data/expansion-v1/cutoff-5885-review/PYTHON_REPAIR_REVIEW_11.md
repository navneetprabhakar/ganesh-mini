# Python repair review, batch 11

Positions 151–165 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Nine new
additive holds: 808 additive plus historical three = 811; 2,082 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 151 | 0178 | Ascending value/descending index repairs ordering; fresh list and nonmutation agree. No new hold. |
| 152 | 0179 | Removing reverse repairs annotation order. Hold: mapping entries accepted despite sequence requirement. |
| 153 | 0180 | Subtracting one repairs estimate. Hold: finite huge radix at level zero overflows validation despite representable zero result. No invented overflow-output policy. |
| 154 | 0181 | Immediate indexed ValueError repairs skipped malformed measurements. Hold: valid 5000-digit integer rejected. Underscore/Unicode grammar pending. |
| 155 | 0182 | Previous-result recurrence repairs progressive bands. Hold: finite huge integer overflows validation. |
| 156 | 0183 | Iteration repairs eager materialization; immediate validation and category-space bound agree. Hold: finite huge integer overflows validation. |
| 157 | 0184 | Operations lookup repairs recipe iteration; preparation precedes action calls. Unused action-map entries/global validation wording pending; no new hold. |
| 158 | 0185 | Enabled condition repaired; increment precedes same-control callback and exceptions propagate. Boolean-enabled test restriction wording pending; no new hold. |
| 159 | 0186 | Field length repairs off-by-one; separator, empty and type behavior agree. No new hold. |
| 160 | 0188 | Span 95 repairs inclusive printable ASCII rotation; arbitrary integer modulo and inverse agree. No new hold. |
| 161 | 0189 | Finally-close repairs loop closure; ordinary reader/error paths agree. Hold: finite deep result fails copying; probe confirms closure still occurs. |
| 162 | 0191 | State-offset repairs bucket selection and independent ordinary copies. Hold: finite deep item fails copying. Exact-int breadth pending. |
| 163 | 0192 | Lower wrap repaired; ordinary interval validation and arbitrary-size arithmetic agree. Exact-int breadth pending; no new hold. |
| 164 | 0193 | Reverse column repairs clockwise indexing. Hold: set row accepted and finite deep cell fails copying. |
| 165 | 0194 | Deepcopy repairs ordinary task aliases and preserves extras. Hold: finite deep extra field fails copying. |

Nine pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; ten failing assertions. Original tests read, not newly
rerun by isolated probes. Candidate/test/sample/partition unchanged. Candidate
SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0179 | repair_annotations_sequence / repair-annotations-sequence | 722 | invalid mapping accepted |
| 0180 | repair_compressed_large_radix / repair-compressed-large-radix | 766 | OverflowError |
| 0181 | repair_measurements_integer_limit / repair-measurements-integer-limit | 816 | ValueError |
| 0182 | repair_bands_large_integer / repair-bands-large-integer | 778 | OverflowError |
| 0183 | repair_stream_totals_large_integer / repair-stream-totals-large-integer | 740 | OverflowError |
| 0189 | repair_reader_values_depth / repair-reader-values-depth | 506 | bounded RecursionError |
| 0191 | repair_partition_state_depth / repair-partition-state-depth | 548 | bounded RecursionError |
| 0193 | repair_rotate_board_contract / repair-rotate-board-contract | 533 | set accepted; bounded RecursionError |
| 0194 | repair_claim_completed_depth / repair-claim-completed-depth | 557 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 135 / 796 holds /
2,052 outside-sample inspections (QUALITY_STRATUM_796_BACKUP.md).
Continue position 166.
