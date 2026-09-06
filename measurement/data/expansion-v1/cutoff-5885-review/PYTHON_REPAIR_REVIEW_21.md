# Python repair review, batch 21

Positions 301–315 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Three new
additive holds: 873 additive plus historical three = 876; 2,232 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 301 | 0350 | Enumerating from one repairs dropped first line and numbering. Explicit splitlines/blank/freshness rules agree; no new hold. |
| 302 | 0352 | Full path iteration repairs missing final node. Iterative shared-prefix construction, idempotence and validation agree; no new hold. |
| 303 | 0354 | Parameter split repairs media recognition. Explicit whitespace/slash/empty/suffix rules agree; no wider token grammar invented. No new hold. |
| 304 | 0356 | Absolute difference repairs order-sensitive closeness. Hold: float coercion loses integer distinction and rejects finite huge singleton. |
| 305 | 0358 | Strip repairs trailing whitespace retention. Full validation and duplicate/order preservation agree; no new hold. |
| 306 | 0359 | Prefix-first concatenation repairs physical key. Validation before mutation, empty bytes and survivor identities agree; no new hold. |
| 307 | 0360 | First colon partition repairs values containing colons. Entire-directive rejection, duplicate order and comments agree; no new hold. |
| 308 | 0361 | Correct right parent repairs layout. Tree freshness and exact parent identity agree; no new hold. |
| 309 | 0362 | Disable sorting repairs insertion order. Hold: tuple/nested non-string-key values accepted. Strict JSON versus Python encoder semantics require disposition. |
| 310 | 0363 | Read-backed initialization repairs zero default. Write-before-level update and validation agree; no constructor read-result validation invented. No new hold. |
| 311 | 0364 | Interface label repairs suffix classification. Simple-name/case/stem validation agree; no extra filename restrictions invented. No new hold. |
| 312 | 0365 | Any replaces all to repair substring matching. Full validation, empty needles and note order agree; input duplicate-occurrence wording pending, no new hold. |
| 313 | 0366 | Skip empty words repairs vacuous match. One-pass materialization and full validation agree; no new hold. |
| 314 | 0368 | Count after update repairs callback count. Zero-limit callback exclusion and check/update order agree; no new hold. |
| 315 | 0369 | Position increment repairs nontermination. Ordinary round-robin and copied output agree. Hold: finite deep channel element fails copying. |

Three pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; five failing/error assertions including subtests.
Original tests read, not newly rerun by isolated probes.
Candidate/test/sample/partition unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0356 | repair_close_pair_precision / repair-close-pair-precision | 512 | wrong True; OverflowError |
| 0362 | repair_encode_records_json_values / repair-encode-records-json-values | 445 | two unsupported values accepted |
| 0369 | repair_merge_channels_depth / repair-merge-channels-depth | 407 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 285 / 869 holds /
2,202 outside-sample inspections (QUALITY_STRATUM_869_BACKUP.md).
Continue position 316.
