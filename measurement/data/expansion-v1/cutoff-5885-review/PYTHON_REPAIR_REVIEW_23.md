# Python repair review, batch 23

Positions 331–345 of 426: full prompts, known-bad/corrected source and original
tests read. Eight new holds, 888 additive plus historical three = 891;
2,262 unique outside-sample inspections. These are pending dispositions, not
final rejections, seven-criterion approvals or new known-bad certifications.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 331 | 0387 | Mapping default argument repairs falsey-value loss. Hold: valid getitem-based key iterable rejected. Identity requirements otherwise agree. |
| 332 | 0389 | Forward stages repair order. Hold: unhashable operation gives wrong exception; finite huge input rejected even with no stages. |
| 333 | 0390 | Integer floor division repairs rounding. Exact large-integer scaling, zero and duplicate-label rules agree; no new hold. |
| 334 | 0392 | Independent row allocation repairs product accumulation alias. Hold: finite huge integer entry rejected. Native floating cancellation breadth pending. |
| 335 | 0393 | First token selection repairs substring acceptance. Case, punctuation and whitespace agree; no new hold. |
| 336 | 0394 | Final element append repairs truncation. Explicit element/divider identity and fresh outer list agree; no new hold. |
| 337 | 0395 | Initial deepcopy repairs input mutation. Hold: finite deep profile fails with no updates. Full key validation precedes copies. |
| 338 | 0396 | Set argument repairs variadic construction. Distinct sorting, types and empties agree; no new hold. |
| 339 | 0397 | False on unmatched closing repairs acceptance. Hold: early mismatch hides subsequent non-bracket character. |
| 340 | 0398 | Full modulus repairs skipped last/single option. Explicit list annotation and full coordinate validation agree; no new hold. |
| 341 | 0400 | Integer parsing repairs lexical revisions. Hold: explicitly allowed leading-zero representation hits conversion limit. |
| 342 | 0401 | Negative position check repairs reverse lookup. Explicit failure-to-None behavior retained. No boolean/type restrictions invented; no new hold. |
| 343 | 0402 | Remove drain increment repairs double counting. FIFO and explicit payload aliases agree; no new hold. |
| 344 | 0403 | Inclusive comparisons repair adjacent equality. Hold: finite huge singleton rejected. |
| 345 | 0404 | Per-record deepcopy repairs aliasing. Hold: finite deep matching extra field fails copying. |

Eight pinned Python 3.11.15 network-disabled/resource-limited probes exited 1
without timeout; ten failing/error assertions including subtests. Source tests
were read, not rerun by these isolated probes. Candidate/test/sample/partition
unchanged; candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0387 | repair_indexed_lookup_iterable / repair-indexed-lookup-iterable | 805 | TypeError |
| 0389 | repair_transform_chain_contract / repair-transform-chain-contract | 872 | TypeError; OverflowError |
| 0392 | repair_matrix_product_integer / repair-matrix-product-integer | 432 | OverflowError |
| 0395 | repair_merge_profile_depth / repair-merge-profile-depth | 493 | bounded RecursionError |
| 0397 | repair_nested_invalid_suffix / repair-nested-invalid-suffix | 494 | two missing ValueErrors |
| 0400 | repair_needs_upgrade_digit_limit / repair-needs-upgrade-digit-limit | 463 | ValueError |
| 0403 | repair_classify_run_integer / repair-classify-run-integer | 611 | OverflowError |
| 0404 | repair_filter_inventory_depth / repair-filter-inventory-depth | 584 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits backup. GCS verified through repair315 / 876 holds / 2,232
outside-sample inspections: QUALITY_STRATUM_876_BACKUP.md. Continue position346.
