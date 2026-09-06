# Python repair review, batch 8

Positions 106–120 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Nine new
additive holds: 788 additive plus historical three = 791; 2,037 unique
outside-sample inspections. Holds are review items, not final rejections.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 106 | 0124 | Positive retention condition repairs disabled/enabled inversion. Original result identity and function-failure behavior agree. Hold: finite 600-level result cannot be retained. No copy-failure atomicity promise inferred. |
| 107 | 0126 | Copying untouched branches repairs shallow merge. Ordinary order, tuple replacement and cycle checks agree. Hold: finite 600-level allowed list fails; nested Mapping breadth pending. |
| 108 | 0127 | Starting at context children repairs context inclusion. Ordinary validation/preorder agree. Hold: valid 1100-link unique-id tree fails validation by recursion. |
| 109 | 0128 | All repairs any-scope grant and empty requirements. Hold: accepts set instead of requiring sequence. |
| 110 | 0130 | Removing sort repairs component order. Escape order, duplicates, whitespace segments and ordinary validation agree; no new hold. |
| 111 | 0131 | Full-turn increments repair half-turn wrapping. Hold: prompt interval impossible for some accepted inputs, reproduced [0,100] with limit 30 returning an out-of-range difference. No invented rejection policy; extreme finite progress pending. |
| 112 | 0133 | Keeping earliest prefix repairs widest neutral window. Prefix-balance argument, zero cases and ordinary validation agree; no new hold. |
| 113 | 0134 | Dictionary result repairs outer shape. Ordinary nested-copy semantics agree. Hold: finite 600-level field fails. |
| 114 | 0135 | Return after loop repairs premature/absent result. Full-input validation and stop exclusion agree; no new hold. |
| 115 | 0136 | Equality to zero repairs successful-count inversion. Empty universal truth and range/type checks agree; no new hold. |
| 116 | 0137 | Equality repairs identity-based casefold matching. Mapping normalization and order agree. Hold: finite 600-level string-subclass metadata fails; this metadata domain is explicitly in original tests. |
| 117 | 0139 | Right operand repairs doubled-left counts. Lexicographic union, arbitrary integer arithmetic and nonmutation agree; no new hold. |
| 118 | 0141 | Whole-graph deepcopy repairs shallow copy and preserves internal sharing/cycles. Hold: finite 600-level value fails. |
| 119 | 0143 | Multiplicity count repairs distinct-factor count. Decreasing remainder/increasing divisor ensures finite termination for ordinary integers. No performance bound inferred; large-prime runtime not certified, no new hold. |
| 120 | 0144 | Inclusive slice repairs omitted current value. Hold: finite representable average overflows its intermediate sum. |

Nine pinned Python 3.11.15 network-disabled/resource-limited probes, each
exit 1 without timeout. Original tests read, not newly rerun by isolated probes.
Candidates/tests/sample/partition unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0124 | repair_runner_result_depth / repair-runner-result-depth | 795 | bounded RecursionError |
| 0126 | repair_bundle_depth / repair-bundle-depth | 752 | bounded RecursionError |
| 0127 | repair_find_nodes_depth / repair-find-nodes-depth | 763 | bounded RecursionError |
| 0128 | repair_authorize_sequence / repair-authorize-sequence | 532 | invalid set accepted |
| 0131 | repair_headings_infeasible_limit / repair-headings-infeasible-limit | 495 | 100 exceeds 30 |
| 0134 | repair_build_record_depth / repair-build-record-depth | 543 | bounded RecursionError |
| 0137 | repair_runtime_command_depth / repair-runtime-command-depth | 527 | bounded RecursionError |
| 0141 | repair_duplicate_bundle_depth / repair-duplicate-bundle-depth | 497 | bounded RecursionError |
| 0144 | repair_trailing_average_overflow / repair-trailing-average-overflow | 482 | infinity instead of 1e308 |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 90 / 774 holds /
2,007 outside-sample inspections (QUALITY_STRATUM_774_BACKUP.md).
Continue position 121.
