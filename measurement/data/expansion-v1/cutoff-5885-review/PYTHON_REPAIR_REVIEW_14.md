# Python repair review, batch 14

Positions 196–210 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Seven new
additive holds: 829 additive plus historical three = 832; 2,127 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 196 | 0229 | Factor multiplication repairs factorial. Triangular values, order and fresh results agree. Repeated factorial work idiomatic-quality pending; no invented runtime limit or new hold. |
| 197 | 0230 | Extend repairs overwritten descendant branches. Ordinary preorder and validation agree. Hold: finite 1200-node chain fails recursion. |
| 198 | 0231 | Row comprehension repairs structural sharing while preserving required fill/value identities. Snapshot structure and bounds agree; no new hold. |
| 199 | 0232 | All-markers branch repairs partial classification. Exact substrings/order independence agree; no new hold. |
| 200 | 0233 | Channel receiver repairs missing method. Ordinary collaborator order, identity and exception behavior agree. Constant-lookup subclass breadth and collaborator-mutation wording pending; no new hold. |
| 201 | 0234 | Any cleaned cell repairs whitespace-only records. Hold: CR separators and valid large field reported malformed. |
| 202 | 0235 | Staticmethod repairs instance/class call compatibility. Normal arithmetic exceptions explicitly allowed; no new hold. |
| 203 | 0238 | Strict-shorter boundary repairs immediate complete frames. Hold: released view gives wrong invalid-input exception. Immutable empty bytes identity wording pending. |
| 204 | 0239 | Deprecation-first test repairs inheritance classification. No instantiation and ordinary invalid values agree; no new hold. |
| 205 | 0240 | Visible-key filtering repairs caller mapping mutation. Validation precedes formatting. Hold: finite large integer repr fails. Custom repr side effects not newly prohibited. |
| 206 | 0241 | Positive index tiebreak repairs FIFO dispatch. Hold: empty jobs fail with huge valid worker count. Exact-int breadth/linear worker scan quality pending. |
| 207 | 0242 | Maximum stage repairs bottleneck formula. Zero-batch validation and large arithmetic agree. Exact-int breadth pending; no new hold. |
| 208 | 0243 | Inclusive threshold repairs equality. Hold: integer precision lost through float coercion and huge finite integer rejected. |
| 209 | 0244 | Postorder append repairs dependency ordering. Full structural validation/reachable cycle scope agree. Hold: finite deep dependency chain fails recursion. |
| 210 | 0245 | Full string length repairs remainder loss. Unicode code-point boundaries and validation agree; no new hold. |

Seven pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; nine failing/error test cases. Original tests read,
not newly rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0230 | repair_group_tree_depth / repair-group-tree-depth | 760 | bounded RecursionError |
| 0234 | repair_measurements_csv_limits / repair-measurements-csv-limits | 679 | two ValueErrors |
| 0238 | repair_frame_released_view / repair-frame-released-view | 863 | ValueError instead of TypeError |
| 0240 | repair_label_integer_limit / repair-label-integer-limit | 884 | ValueError |
| 0241 | repair_dispatch_empty_workers / repair-dispatch-empty-workers | 505 | OverflowError |
| 0243 | repair_margin_precision / repair-margin-precision | 711 | wrong label; OverflowError |
| 0244 | repair_bundle_order_depth / repair-bundle-order-depth | 645 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 195 / 825 holds /
2,112 outside-sample inspections (QUALITY_STRATUM_825_BACKUP.md).
Continue position 211.
