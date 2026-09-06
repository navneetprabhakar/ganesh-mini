# Python repair review, batch 24

Positions 346–360 of 426: full prompts, known-bad/corrected source and original
tests read. Four new holds, 892 additive plus historical three = 895;
2,277 unique outside-sample inspections. Pending dispositions, not final
rejections, seven-criterion approvals or new known-bad certifications.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 346 | 0405 | Fullmatch repairs prefix acceptance. ASCII and length rules agree; test's apparent Unicode case contains control characters, broader test coverage pending. No new hold. |
| 347 | 0406 | Initial deepcopy repairs base mutation. Hold: mutable override key remains aliased; finite deep base fails copying. Key identity wording requires disposition. |
| 348 | 0407 | Stop boundary repairs inclusive range. Both directions, types and zero step agree; no new hold. |
| 349 | 0408 | Literal field regex repairs unrelated number extraction. Exact six digits and first match agree; apparent Unicode test is control-text, broader coverage pending. No new hold. |
| 350 | 0409 | Full count repairs run truncation. Explicit types, pair length and positive count agree; no new hold. Output-size limits not treated as a candidate bug. |
| 351 | 0410 | Separate padding rows repair aliases. Input rows copied and order/height preserved; no new hold. |
| 352 | 0411 | Strict comparisons repair tolerance equality. Hold: sign product underflow loses turning point. Real-type breadth and huge-integer handling pending. |
| 353 | 0412 | Offset plus length repairs slicing/bounds. Zero-length end, field validation and duplicate order agree; no new hold. |
| 354 | 0413 | Integer division repairs fractional capacity. Exact large integers/types agree; no new hold. |
| 355 | 0414 | Reversed flag values repair enablement. Feature order, ASCII naming and disabled membership agree; no new hold. |
| 356 | 0415 | Exact count repairs extra message. Hold: valid huge start fails single-line formatting under digit limit. |
| 357 | 0416 | Big endian repairs payload length. Exact bytes/schema/truncation/order agree; no new hold. |
| 358 | 0417 | Slice replacement repairs skipped handles while preserving required list alias. Idempotence/snapshot agree; post-construction external-state mutation policy unspecified. No new hold. |
| 359 | 0419 | Empty body precedence repairs content-type rejection. Hold: non-JSON constants accepted and finite deep parsed object fails copying. |
| 360 | 0420 | Raw bytes assignment repairs repr corruption. Full prevalidation, ordered operations and sorted output agree; no new hold. |

Four pinned Python 3.11.15 network-disabled/resource-limited probes exited 1
without timeout; seven failing/error assertions including subtests. Original
tests read, not rerun by isolated probes. Candidate/test/sample/partition
unchanged; candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0406 | repair_theme_alias_depth / repair-theme-alias-depth | 810 | aliased key; bounded RecursionError |
| 0411 | repair_turning_points_underflow / repair-turning-points-underflow | 895 | turning point omitted |
| 0415 | repair_numbered_message_digit_limit / repair-numbered-message-digit-limit | 413 | ValueError |
| 0419 | repair_decode_query_json_contract / repair-decode-query-json-contract | 686 | two invalid constants accepted; bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits backup. GCS verified through repair345 / 891 holds / 2,262
outside-sample inspections: QUALITY_STRATUM_891_BACKUP.md. Continue position361.
