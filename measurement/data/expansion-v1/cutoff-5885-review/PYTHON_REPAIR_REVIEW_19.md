# Python repair review, batch 19

Positions 271–285 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Six new
additive holds: 866 additive plus historical three = 869; 2,202 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 271 | 0318 | Validate before parity filtering repairs skipped malformed values. Laziness, one-pass and deferred exceptions agree; no new hold. |
| 272 | 0319 | Attribute-based calling repairs inheritance restriction. Error order and protocol agree; no caller-defined method purity guarantee invented. No new hold. |
| 273 | 0320 | Specific signature first repairs classification. Bytes-like conversion and partial general signature agree; truncated wording pending, no new hold. |
| 274 | 0321 | Row/column indexing repairs score transpose. Ordinary order and independent emission agree. Hold: finite deep Cartesian value fails copying. |
| 275 | 0322 | Deepcopy repairs shallow settings alias. Separate layer values and validation agree. Hold: finite deep settings fails copying. |
| 276 | 0323 | Remove reverse repairs leaf-to-root order. Full validation and separate record copies agree. Hold: finite deep extra field fails copying. |
| 277 | 0324 | Forward iteration repairs preference priority. Primary-subtag/fallback order agree. Malformed language syntax undefined; do not invent BCP rules. No new hold. |
| 278 | 0325 | Presence check repairs stored None retrieval. Key validation and insertion order agree. Hold: finite deep value fails storage. |
| 279 | 0326 | Escaping repairs literal marker search. First occurrence, empty prefix and whitespace agree; no new hold. |
| 280 | 0327 | Owner comparison repairs unregister authorization. Missing/replace/sorted snapshot and validation agree; no new hold. |
| 281 | 0328 | Boundary stripping repairs internal whitespace deletion. First separator and ASCII identifier rules agree; no new hold. |
| 282 | 0329 | Zero starting index repairs first-sample retention. Rates, iterables and fresh outer list agree; nested-copy requirement not invented. No new hold. |
| 283 | 0330 | Correct offset repairs dropped body byte. Both tag markers, bounds and formatting agree. New immutable bytes identity wording pending; no new hold. |
| 284 | 0331 | Nested comprehensions repair generated row/cell aliases. Hold: set_cell changes another cell for aliased input rows; finite deep fill fails copying. |
| 285 | 0332 | Sentinel-only branch repairs explicit unlimited timeout. Hold: non-int/float Fraction accepted; negative huge integer produces wrong exception. Positive unrepresentable-float wording pending. |

Six pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; eight failing/error test cases. Original tests read,
not newly rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0321 | repair_expand_grid_depth / repair-expand-grid-depth | 969 | bounded RecursionError |
| 0322 | repair_snapshot_layers_depth / repair-snapshot-layers-depth | 979 | bounded RecursionError |
| 0323 | repair_normalize_chain_depth / repair-normalize-chain-depth | 961 | bounded RecursionError |
| 0325 | repair_sparse_table_depth / repair-sparse-table-depth | 948 | bounded RecursionError |
| 0331 | repair_grid_alias_depth / repair-grid-alias-depth | 626 | changed other cell; bounded RecursionError |
| 0332 | repair_timeout_numeric_contract / repair-timeout-numeric-contract | 687 | invalid type accepted; OverflowError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 255 / 853 holds /
2,172 outside-sample inspections (QUALITY_STRATUM_853_BACKUP.md).
Continue position 286.
