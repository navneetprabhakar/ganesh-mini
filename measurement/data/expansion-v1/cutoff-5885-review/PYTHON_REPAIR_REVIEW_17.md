# Python repair review, batch 17

Positions 241–255 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Ten new
additive holds: 850 additive plus historical three = 853; 2,172 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 241 | 0280 | Issued lookup repairs field typo. Record validation, order and duplicates agree. Outer malformed-input exception wording pending; no new hold. |
| 242 | 0281 | Parameter split repairs media selection. Hold: XML input field order constrained by implementation/tests but absent from input prose. Attribute/text breadth and XML character representation pending. |
| 243 | 0282 | Empty fallback repairs None drain. Hold: nested caller mutation changes repeat results; shallow-versus-deep copy wording requires disposition. Explicit str protocol not replaced. |
| 244 | 0283 | Escape lines before tags repairs markup escaping. Hold: single empty line produces empty paragraph. Boundary newline semantics require disposition. |
| 245 | 0285 | Modulo successor repairs ring closure. Empty/single/duplicate behavior and validation agree; no new hold. |
| 246 | 0287 | Final append repairs dropped final run. Unicode code points and empty validation agree; no new hold. |
| 247 | 0288 | Zero canonicalization and denominator sign repair ratio. GCD/large integer arithmetic agree; no new hold. |
| 248 | 0289 | Initial deepcopy repairs stage mutation of input. Ordinary stage/result isolation agrees. Hold: finite deep input fails even with no stages. |
| 249 | 0291 | Assignment repairs first-event retention. Ordinary configured order/full validation agree. Hold: finite deep matching event fails copying. Chronological ordering assumption pending. |
| 250 | 0292 | Strict overflow comparison repairs exact boundary packing. Oversized and zero-field rows agree. Hold: finite deep row fails copying. Within-row duplicated-value alias wording pending. |
| 251 | 0294 | Metadata deepcopy repairs hierarchy aliasing. Hold: missing ancestor gives wrong exception with child-first order; finite deep metadata fails copying. |
| 252 | 0296 | Credentials condition repairs wildcard acceptance. Hold: internal-space hostname accepted. Empty query/fragment/port and control-character validation breadth pending. |
| 253 | 0297 | Per-column bounds repair global scaling. Hold: finite opposite extremes yield wrong zero/NaN; finite huge constant rejected. |
| 254 | 0299 | Less-than repairs negative filtering. Infinity and signed-zero semantics agree, no finiteness requirement invented; no new hold. |
| 255 | 0300 | Full membership repairs substring owner match. Hold: mixed list/tuple inputs fail, malformed nondecimal digit PID aborts, and valid large PID rejected. |

Ten pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; fourteen failing/error test cases. Original tests read,
not newly rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0281 | repair_packet_xml_order / repair-packet-xml-order | 597 | ValueError / prompt-test mismatch |
| 0282 | repair_task_drainer_nested_alias / repair-task-drainer-nested-alias | 571 | changed subsequent output |
| 0283 | repair_notes_empty_line / repair-notes-empty-line | 486 | empty paragraph emitted |
| 0289 | repair_pipeline_depth / repair-pipeline-depth | 510 | bounded RecursionError |
| 0291 | repair_latest_job_depth / repair-latest-job-depth | 501 | bounded RecursionError |
| 0292 | repair_pack_rows_depth / repair-pack-rows-depth | 542 | bounded RecursionError |
| 0294 | repair_hierarchy_contract / repair-hierarchy-contract | 529 | KeyError; bounded RecursionError |
| 0296 | repair_origin_space_host / repair-origin-space-host | 532 | malformed host accepted |
| 0297 | repair_scale_axes_extremes / repair-scale-axes-extremes | 578 | wrong scaling; OverflowError |
| 0300 | repair_privileged_tasks_contract / repair-privileged-tasks-contract | 623 | TypeError; two ValueErrors |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 225 / 838 holds /
2,142 outside-sample inspections (QUALITY_STRATUM_838_BACKUP.md).
Continue position 256.
