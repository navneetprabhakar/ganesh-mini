# Python repair review, batch 18

Positions 256–270 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Ten new
additive holds: 860 additive plus historical three = 863; 2,187 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 256 | 0298 | Sum of widths repairs canvas size. Hold: finite deep tile cell fails copying. Ordinary shape/order behavior agrees. |
| 257 | 0303 | Bytes conversion repairs mutable archive payload aliasing. Key precedence, order and empty content agree; no new hold. Malformed lookup key wording pending. |
| 258 | 0304 | Inclusive bottom bound repairs region clearing. Hold: standard UserList sequence rejected despite sequence contract. |
| 259 | 0305 | Unconditional callback loop repairs preview behavior. Callback identity/order agree; no registration snapshot guarantee invented. No new hold. |
| 260 | 0306 | Removing falsey-cost rejection repairs zero delivery cost. Hold: finite huge integer cost raises OverflowError. |
| 261 | 0307 | Apostrophe-aware regex repairs tokenization. ASCII boundaries, order and empty input agree; no new hold. |
| 262 | 0308 | Zero-size base case repairs empty combination. Hold: 1200-item single full-size combination fails recursion, without combinatorial output growth. |
| 263 | 0309 | Modulo repairs time wraparound. Input bounds and boolean exclusion agree; no new hold. |
| 264 | 0310 | First label repairs tenant extraction. Hold: embedded hostname newline and empty explicit port accepted. URL wording requires disposition. |
| 265 | 0311 | Removing early break repairs grading all responses. Hold: finite deep response fails copying. Custom equality breadth pending. |
| 266 | 0313 | Unconditional assignment repairs last-value retention. Hold: finite deep options value fails copying. |
| 267 | 0314 | Recorded key order repairs incomparable-key sorting. Hold: finite deep mapped value fails copying. Callback exceptions remain explicitly propagated. |
| 268 | 0315 | Increment on None repairs nontermination. Full validation, first occupied level and empty-column discard agree; no new hold. |
| 269 | 0316 | Restore-tuples mode repairs thawed points. Hold: finite huge integer coordinate fails both freeze and thaw. JSON-compatible metadata wording breadth pending. |
| 270 | 0317 | Padded integer comparison repairs lexical version comparison. Hold: valid long decimal component hits interpreter limit. |

Ten pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; twelve failing/error test cases. Original tests read,
not newly rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0298 | repair_join_tiles_depth / repair-join-tiles-depth | 879 | bounded RecursionError |
| 0304 | repair_clear_region_sequence / repair-clear-region-sequence | 892 | ValueError |
| 0306 | repair_delivery_cost_large_integer / repair-delivery-cost-large-integer | 581 | OverflowError |
| 0308 | repair_choose_groups_depth / repair-choose-groups-depth | 569 | bounded RecursionError |
| 0310 | repair_tenant_url_validation / repair-tenant-url-validation | 646 | two malformed URLs accepted |
| 0311 | repair_grade_responses_depth / repair-grade-responses-depth | 795 | bounded RecursionError |
| 0313 | repair_assemble_sections_depth / repair-assemble-sections-depth | 718 | bounded RecursionError |
| 0314 | repair_map_groups_depth / repair-map-groups-depth | 462 | bounded RecursionError |
| 0316 | repair_report_large_integer / repair-report-large-integer | 661 | two OverflowErrors |
| 0317 | repair_version_integer_limit / repair-version-integer-limit | 703 | ValueError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 255 / 853 holds /
2,172 outside-sample inspections (QUALITY_STRATUM_853_BACKUP.md).
Continue position 271.
