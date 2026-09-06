# Python repair review, batch 12

Positions 166–180 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Six new
additive holds: 814 additive plus historical three = 817; 2,097 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 166 | 0195 | Exclusive stop repairs stride boundary. Hold: two-value stride fails on 5000-digit decimal rendering. |
| 167 | 0196 | Full input length repairs partial final chunk. Tuple shape, order, empty and type validation agree. Integer-subclass mutable attributes wording pending; no new hold. |
| 168 | 0197 | Inclusive endpoint repairs range expansion. Hold: valid 5000-digit singleton rejected. Unicode numeric grammar breadth pending. |
| 169 | 0198 | Any nonblank cell repairs row retention. Row strings are iterables of strings, not explicitly prohibited. Fresh rows and ordinary type checks agree; no new hold. |
| 170 | 0199 | Axis-one comprehension repaired. Hold: bytes line accepted and finite huge integer overflows validation. |
| 171 | 0200 | Explicit missing-ticket check repairs release. Ordinary order/isolation agree. Hold: finite deep constructor value fails copying. No copy-failure atomicity invented. |
| 172 | 0201 | Missing-selection clearing repairs option update. Normalization, input copying and ordinary invalid-update state agree; no new hold. |
| 173 | 0202 | Split once repairs embedded equals. Last-value/first-position and explicit shallow-copy semantics agree; no new hold. |
| 174 | 0203 | Retries plus one repairs zero-attempt case. Consumption retries, final exception identity and partial-value discard agree; no new hold. |
| 175 | 0204 | Removing clear repairs flush persistence. Ordinary ID allocation and commit agree. Hold: finite deep staged record fails copying. |
| 176 | 0205 | Pop before None check repairs nontermination. Reference preservation and nonmutation agree. Quadratic front-pop retained: idiomatic-quality review pending, no invented runtime limit or new hold. |
| 177 | 0206 | Finally-close repairs skipped cleanup. Exception precedence and exact result identity agree; no new hold. |
| 178 | 0208 | Exact equality repairs frequency threshold. Largest candidate, input preservation and validation agree; no new hold. |
| 179 | 0209 | Final append repairs dropped last run. Integer iterable, empty and ordering agree; no new hold. |
| 180 | 0210 | Kilometer conversion repairs units. Hold: meter overflow falsely reports unreachable despite representable kilometer result; finite huge edge also breaks same-endpoint zero. |

Six pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; eight failing/error test cases. Original tests read,
not newly rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0195 | repair_stride_integer_limit / repair-stride-integer-limit | 596 | ValueError |
| 0197 | repair_ranges_integer_limit / repair-ranges-integer-limit | 611 | ValueError |
| 0199 | repair_axis_sums_contract / repair-axis-sums-contract | 652 | bytes accepted; OverflowError |
| 0200 | repair_reservation_depth / repair-reservation-depth | 673 | bounded RecursionError |
| 0204 | repair_async_buffer_depth / repair-async-buffer-depth | 635 | bounded RecursionError |
| 0210 | repair_distance_overflow / repair-distance-overflow | 508 | None for reachable route; OverflowError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 165 / 811 holds /
2,082 outside-sample inspections (QUALITY_STRATUM_811_BACKUP.md).
Continue position 181.
