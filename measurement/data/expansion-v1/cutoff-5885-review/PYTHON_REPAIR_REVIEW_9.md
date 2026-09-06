# Python repair review, batch 9

Positions 121–135 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Five new
additive holds: 793 additive plus historical three = 796; 2,052 unique
outside-sample inspections. Holds are review items, not final rejections.
Inspection is not seven-criterion approval or executed known-bad certification.
Supersedes the partial working note without erasing its audit trail.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 121 | 0145 | Inclusive comparisons repair shelf boundaries. Ordinary exact and integer-subclass rules agree; no new hold. |
| 122 | 0146 | Row slicing repairs left/width and structural independence; cell identity intentionally shared. Invalid grid-container policy unspecified; no invented validation requirement, no new hold. |
| 123 | 0147 | Removing space repairs single-hyphen joining. Hold: double trailing hyphen also removed. Blank-line precedence remains pending. |
| 124 | 0148 | Inclusive delay repairs zero/boundary budget. Delay/index ordering and intentional payload identity agree. Non-iterable outer input policy unspecified; no new hold. |
| 125 | 0149 | Half factor repairs energy formula. Hold: float conversion collapses valid adjacent integer positions and rejects them. Extreme product overflow remains pending. |
| 126 | 0150 | Empty-count guard repairs missing-value mean. Single traversal agrees. Hold: finite representable average overflows. |
| 127 | 0151 | Longest mark first repairs UTF-32/16 prefix precedence. Ordinary bytes validation agrees. Ambiguous partial-longer-mark/complete-shorter-mark wording pending; no new hold. |
| 128 | 0153 | Inclusive availability repairs exact-stock allocation. Sequential unknown-code handling and nonmutation agree. Broad wrong-type versus malformed-pair exception wording needs disposition; no new hold. |
| 129 | 0154 | Per-row copy repairs input mutation and shared-row output aliases. Half-open occupancy/empty-range checks agree for ordinary integers; subclass behavior pending, no new hold. |
| 130 | 0155 | Applying injector repairs missing context. Exact output format, defaults, final-slash split and ignored unknown fields agree. No deep-copy requirement inferred for ignored fields; no new hold. |
| 131 | 0156 | Conjunction repairs team authorization. Public/owner/disabled decisions and ordinary schema validation agree; no new hold. |
| 132 | 0157 | Recursive visit repairs transitive dependency closure. Ordinary preorder/cycles agree. Hold: finite 1100-document chain fails by recursion. Immutable bytes sharing intentional. |
| 133 | 0158 | Width modulus repairs unavailable final bit/width-one error. Specified digest algorithm and circular offsets agree. UTF-8 surrogate domain and extreme allocation bounds pending; no new hold. |
| 134 | 0159 | Inclusive threshold repairs score-three classification. Exact order/weights and ignored validated unknown keys agree. Direct dataclass construction invariants unspecified; no new hold. |
| 135 | 0160 | Missing negation repairs closing-bracket validation. Snapshot subscriptions, duplicate callbacks and ordinary isolated payload copies agree. Hold: finite 600-level payload fails before callback. |

Five pinned Python 3.11.15 network-disabled/resource-limited probes, each
exit 1 without timeout. Original tests read, not newly rerun by isolated probes.
Candidates/tests/sample/partition unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0147 | repair_reflow_double_hyphen / repair-reflow-double-hyphen | 531 | word-next instead of word-- next |
| 0149 | repair_strain_position_precision / repair-strain-position-precision | 1038 | valid positions rejected |
| 0150 | repair_average_present_overflow / repair-average-present-overflow | 1004 | infinity instead of 1e308 |
| 0157 | repair_collect_assets_depth / repair-collect-assets-depth | 888 | bounded RecursionError |
| 0160 | repair_event_hub_depth / repair-event-hub-depth | 429 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 120 / 791 holds /
2,037 outside-sample inspections (QUALITY_STRATUM_791_BACKUP.md).
Continue position 136.
