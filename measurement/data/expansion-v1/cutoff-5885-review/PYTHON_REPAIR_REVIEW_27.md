# Python repair review, batch 27

Positions 391–405 of 426: full prompts, known-bad/corrected source and original
tests read. Four new holds, 912 additive plus historical three = 915;
2,322 unique outside-sample inspections. Pending dispositions, not final
rejections, seven-criterion approvals or new known-bad certifications.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 391 | 0458 | Removing break repairs cleanup continuation. Exception versus BaseException and non-callables agree; iterable-production failure policy unspecified. No new hold. |
| 392 | 0459 | Zero remainder repairs divisor check. Correct descending search for finite integers; linear search cost and nontriviality pending. No new hold. |
| 393 | 0461 | Lowercase branch repairs uppercase conversion. ASCII boundaries, Unicode preservation and pure repeat calls agree; no new hold. |
| 394 | 0462 | Key membership repairs falsey-cache misses. Hold: finite deep produced value hits copy recursion limit. |
| 395 | 0463 | Exact stride repairs skipped records. Tuple batches and explicitly structural-only independence agree; no new hold. |
| 396 | 0465 | Surrogate exclusion repairs invalid scalar acceptance. Prefix/hex/range validation and fresh mapping agree; no new hold. |
| 397 | 0466 | Seen-set insertion repairs duplicates. Strip/casefold matching, exact name deduplication and full row validation agree; no new hold. |
| 398 | 0467 | Inclusive sum check repairs exact-threshold prefix. Hold: zero-share result becomes nonempty after total overflows. |
| 399 | 0468 | Deepcopy repairs selected-value alias. Hold: finite deep selected value hits copy recursion limit. |
| 400 | 0469 | Default split repairs arbitrary whitespace. Name/address grouping and container errors agree; no new hold. |
| 401 | 0470 | Deletion repairs None handling. Hold: finite deep base hits copy recursion limit; Ellipsis precedence agrees. |
| 402 | 0471 | ASCII range repairs Unicode digit loss. Unicode tests and unchanged text agree; no new hold. |
| 403 | 0472 | Input category order repairs sorting. Large integers avoid float conversion, missing zero and full validation agree; no new hold. |
| 404 | 0474 | Indexed deletion repairs skipped elements. Prior removals on exception and nested identity agree. Callback structural mutation scope pending; no new hold. |
| 405 | 0476 | Base sixteen repairs decoding arithmetic. Full byte roundtrip plus independent literal cases, uppercase domain and empty handling agree; no new hold. |

Four pinned Python 3.11.15 network-disabled/resource-limited probes exited 1
without timeout; four failed tests. Original tests read, not rerun by isolated
probes. Runtime-limit findings remain distinct from algorithmic bugs.
Candidate/test/sample/partition unchanged; candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0462 | repair_memo_0462 / repair-memo-0462 | 655 | bounded RecursionError |
| 0467 | repair_prefix_0467 / repair-prefix-0467 | 508 | nonempty zero-share prefix |
| 0468 | repair_extract_0468 / repair-extract-0468 | 703 | bounded RecursionError |
| 0470 | repair_overrides_0470 / repair-overrides-0470 | 794 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits backup. GCS verified through repair390 / 911 holds / 2,307
outside-sample inspections: QUALITY_STRATUM_911_BACKUP.md. Continue position406.
