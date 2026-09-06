# Python repair review, batch 26

Positions 376–390 of 426: full prompts, known-bad/corrected source and original
tests read. Eight new holds, 908 additive plus historical three = 911;
2,307 unique outside-sample inspections. These are pending dispositions,
not final rejections, seven-criterion approvals or new known-bad certifications.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 376 | 0440 | Cubing repairs wrong exponent. Integer validation and fresh empty list agree; no new hold. |
| 377 | 0441 | Year-first comparison repairs month ordering. ASCII format and month bounds agree; exact-type/subclass scope pending. No new hold. |
| 378 | 0442 | Joined recipient header repairs list representation. EmailMessage behavior retained; header-domain/type breadth pending. No new hold. |
| 379 | 0443 | Stored callable repairs eager execution. Ready ordering agrees; callback-failure policy and result-copy wording unspecified, not presumed guarantees. No new hold. |
| 380 | 0444 | Immediate return repairs last-match selection. Full rectangular validation and empty handling agree; no new hold. |
| 381 | 0445 | First retained row repairs width comparison. Hold: CR-only standard CSV rows rejected. |
| 382 | 0446 | Stable two-pass sort repairs metric direction and key tie order. Hold: finite huge integer metric raises OverflowError. |
| 383 | 0448 | Computation-before-predicate repairs missing enriched fields. Hold: finite deep row hits copy recursion limit. Callback side-effect/failure guarantees not invented. |
| 384 | 0449 | Initial deepcopy repairs base mutation. Hold: finite deep base hits copy recursion limit. Repeats compose_theme repair pattern; key-alias breadth and deduplication pending. |
| 385 | 0450 | True division repairs flooring. Hold: fractional coordinates above last pixel accepted. Sequence breadth and numeric extremes pending. |
| 386 | 0451 | Exact break replacement repairs line loss. Escaping, normalization and boundary newlines agree; no new hold. |
| 387 | 0452 | ROUND_CEILING repairs negative rounding. Hold: hexadecimal integer raises InvalidOperation rather than supported result or ValueError. Decimal-context/parser-depth scope pending. |
| 388 | 0453 | Deepcopy repairs snapshot mutation. Hold: finite deep snapshot hits copy recursion limit. |
| 389 | 0454 | Address-change condition repairs redundant observations. Skipped sequence validation and fresh empty output agree; no new hold. |
| 390 | 0456 | Ascending insertion-index tie repairs remainder order. Hold: floating conversion allocates more tokens than exact integer total. |

Eight pinned Python 3.11.15 network-disabled/resource-limited probes exited 1
without timeout; eight failing/error tests. Original tests read, not rerun by
isolated probes. Runtime-limit findings require separate disposition.
Candidate/test/sample/partition unchanged; candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0445 | repair_grid_cr / repair-grid-cr | 678 | ValueError wrapping csv.Error |
| 0446 | repair_compile_report_0446 / repair-compile-report-0446 | 431 | OverflowError |
| 0448 | repair_select_rows_depth / repair-select-rows-depth | 612 | bounded RecursionError |
| 0449 | repair_compose_theme_depth / repair-compose-theme-depth | 752 | bounded RecursionError |
| 0450 | repair_remap_bounds / repair-remap-bounds | 776 | missing ValueError |
| 0452 | repair_decimal_literal / repair-decimal-literal | 742 | InvalidOperation |
| 0453 | repair_revisions_depth / repair-revisions-depth | 770 | bounded RecursionError |
| 0456 | repair_distribute_exact_total / repair-distribute-exact-total | 461 | one excess token |

Probe filenames append `_probe.py`; results append `-result.json`.
A pre-existing report probe filename collision was caught before executing or
overwriting its result; the old probe was restored byte-for-byte and this
batch uses the distinct 0446 filenames above.
Batch awaits backup. GCS verified through repair345 / 891 holds / 2,262
outside-sample inspections: QUALITY_STRATUM_891_BACKUP.md. Continue position391.
