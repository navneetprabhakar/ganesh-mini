# Python repair review, batch 6

Positions 76–90 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Seven new
additive holds: 771 additive plus historical three = 774; 2,007 unique
outside-sample inspections. Holds remain review items, not final rejections.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 76 | 0090 | Reverse bit indexing repairs channel order. Marker/range checks and active-low tuple agree; no new hold. |
| 77 | 0091 | Old-query prefix repairs lost parameters. Ordinary escaping/order, fragments and exact empty-mapping return agree. URL normalization/component-preservation breadth pending; no new hold. |
| 78 | 0092 | Counter repairs multiplicities. Unicode codepoint equality, empty and validation agree; no new hold. |
| 79 | 0094 | Intersection repairs detached selection outside container. Ordinary iterable validation and independent frozensets agree; no new hold. |
| 80 | 0095 | Deepcopy repairs input mutation. Hold: shared time mapping changes nonmatching output event too. |
| 81 | 0096 | Count denominator repairs incorrect normalization. Hold: mean of finite absolute errors overflows despite representable answer. |
| 82 | 0097 | One split repairs equals-containing values. Empty values, trimming and last-key value agree; no new hold. |
| 83 | 0098 | Deepcopy repairs input sort mutation. Ordinary stable reverse sort and incomparable-type translation agree. Hold: finite 600-level metadata fails. |
| 84 | 0099 | Removing reverse repairs dependency-first order. Alphabetical DFS matches stated traversal, unlike generic ready-priority sorting. Hold: 1100-package acyclic chain exceeds recursion depth. |
| 85 | 0100 | Interpreter executable repairs invocation target. Fresh argv, exact schemas and ordinary validation agree; no new hold. |
| 86 | 0101 | Trimmed-line suffix repairs padded headings. Repeat-heading append, entry order and independent calls agree; no new hold. |
| 87 | 0102 | Exclusive slice end repairs overlapping batches. Ordinary copy and permitted shared-reference behavior agree. Hold: finite 600-level item fails. |
| 88 | 0104 | Per-column last value repairs cross-column carry. Marker identity and ordinary separate copies agree. Hold: finite 600-level nonmarker cell fails. |
| 89 | 0105 | Independent cube containers repair shared channels. Ordinary index order and float conversion agree. Hold: invalid huge channel raises OverflowError instead of ValueError. |
| 90 | 0106 | Final append repairs lost last run. Unicode classification, exact text and independent calls agree; no new hold. |

Seven pinned Python 3.11.15 network-disabled/resource-limited probes, each
exit 1 without timeout. Original tests read, not newly rerun by isolated
probes. Candidates/tests/sample/partition unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0095 | repair_reschedule_shared_time / repair-reschedule-shared-time | 585 | nonmatching time also changed |
| 0096 | repair_mae_finite_mean / repair-mae-finite-mean | 611 | infinity instead of 1e308 |
| 0098 | repair_assets_depth / repair-assets-depth | 563 | bounded RecursionError |
| 0099 | repair_installation_chain / repair-installation-chain | 578 | bounded RecursionError |
| 0102 | repair_make_batches_depth / repair-make-batches-depth | 415 | bounded RecursionError |
| 0104 | repair_carry_forward_depth / repair-carry-forward-depth | 524 | bounded RecursionError |
| 0105 | repair_color_range_error / repair-color-range-error | 535 | wrong exception for invalid range |

Probe filenames append `_probe.py`; results append `-result.json`.
Batches 5–6 backed up in QUALITY_STRATUM_774_BACKUP.md.
Continue position 91.
