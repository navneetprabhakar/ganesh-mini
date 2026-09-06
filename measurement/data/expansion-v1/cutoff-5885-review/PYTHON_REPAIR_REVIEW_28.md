# Python repair review, batch 28

Positions 406–420 of 426: full prompts, known-bad/corrected source and original
tests read. Seven new holds, 919 additive plus historical three = 922;
2,337 unique outside-sample inspections. Pending dispositions, not final
rejections, seven-criterion approvals or new known-bad certifications.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 406 | 0477 | Numeric tuple repairs lexicographic revision comparison. Hold: valid leading-zero component hits digit limit. |
| 407 | 0478 | ASCII range repairs Unicode numeric classification. Han boundaries and exhaustive categories agree; no new hold. |
| 408 | 0479 | Deepcopy repairs value alias. Hold: finite deep cell value hits recursion limit. |
| 409 | 0480 | Explicit None repairs falsey integer/type behavior. Hold: valid leading-zero integer string hits digit limit. Surrounding whitespace accepted explicitly by tests. |
| 410 | 0481 | First-page heading repairs continuation label. Hold: finite deep row hits copy recursion limit. |
| 411 | 0483 | Final emit repairs trailing term loss. Apostrophe adjacency follows accumulator invariant; casefold/order agree. No new hold. |
| 412 | 0484 | Removing safe slash repairs segment encoding. Exact UTF-8 escapes agree; invalid scalar encoding policy not invented. No new hold. |
| 413 | 0485 | Snapshot repairs sequential averaging. Hold: identical finite large inputs average to infinity. |
| 414 | 0486 | Sentinel repairs None-cache misses. Full hashability precheck and repeated object identity agree. Private-sentinel collision scope pending; no new hold. |
| 415 | 0487 | ID index repairs name-based join. Hold: float conversion changes copied large integer amount. |
| 416 | 0488 | Whole-graph deepcopy repairs internal aliases/cycles. Explicit deepcopy-supported-object scope retained; no additional depth hold. |
| 417 | 0489 | Single append repairs duplicate registration. Existing names and exact returned list identity agree; no new hold. |
| 418 | 0490 | Y-first sorting repairs reading order. Hold: finite huge integer edge raises OverflowError. |
| 419 | 0491 | Correct booleans repair universal predicate. Empty true, strict boundary and full type validation agree; no new hold. |
| 420 | 0492 | Positive position repairs ascending order. Stable tie index, exact scalar schema and independent dictionaries agree; no new hold. |

Seven pinned Python 3.11.15 network-disabled/resource-limited probes exited 1
without timeout; seven failed/error tests. Original tests read, not rerun by
isolated probes. Runtime limits remain distinct from numeric correctness.
Candidate/test/sample/partition unchanged; candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0477 | repair_contract_0477 / repair-contract-0477 | 687 | digit-limit ValueError |
| 0479 | repair_contract_0479 / repair-contract-0479 | 705 | bounded RecursionError |
| 0480 | repair_contract_0480 / repair-contract-0480 | 698 | digit-limit ValueError |
| 0481 | repair_contract_0481 / repair-contract-0481 | 677 | bounded RecursionError |
| 0485 | repair_contract_0485 / repair-contract-0485 | 713 | infinite average |
| 0487 | repair_contract_0487 / repair-contract-0487 | 702 | integer amount changed |
| 0490 | repair_contract_0490 / repair-contract-0490 | 591 | OverflowError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits backup. GCS verified through repair390 / 911 holds / 2,307
outside-sample inspections: QUALITY_STRATUM_911_BACKUP.md. Continue position421.
