# Python generation review, batch 12

Positions 166–180 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; twelve reproduced holds.
563 additive plus historical three = 566 holds; 1,413 unique outside-sample
inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 166 | 0183 | Hold: valid in-range decimal coordinate with leading zeroes rejected by int conversion limit. Ordinary formulas/commands/copies agree; exceptional copy atomicity pending. |
| 167 | 0184 | Hold: same-title duplicate code accepted, overwriting stored record and duplicating order entries. Original collision test explicitly requires this despite unique-code prompt. |
| 168 | 0185 | Ordinary gateway routing, CORS, strict percent/UTF-8 handling and logging agree. Raw surrogate/path domain remains pending; no new hold. |
| 169 | 0188 | Hold: plain mode emits input escape characters despite no-escape requirement. Unrestricted strings versus fixed four-line/value preservation also needs contract clarification. |
| 170 | 0189 | Hold: pagination link inside a valid article is ignored. Ordinary page-level DFS/order/entities agree; malformed valueless attributes and deep recursion pending. |
| 171 | 0190 | Hold: finite correlation with cancelling large products returns zero rather than representable one. Ordinary cross-correlation/ReLU/tie logic agree. |
| 172 | 0191 | Hold: malformed deflate escapes as zlib.error; valid U+2028 inside JSON string incorrectly splits into two invalid lines. Ordinary HTML escaping/order agree. |
| 173 | 0192 | Hold: finite distinct subnormal endpoints underflow bin width to zero. General sequence validation and large integer precision remain pending. |
| 174 | 0187 | Hold: empty input with finite positive radius overflows unnecessary square computation. Ordinary density/noise promotion agree; numeric boundary precision pending. |
| 175 | 0193 | Ordinary categories, duplicate IDs, defaults and independent payload copies agree. Explicit arbitrary nested payload domain versus noncopyable objects remains pending; no new hold. |
| 176 | 0194 | Hold: missing first key short-circuits required type validation of later requested key. Ordinary parser identifiers/first equals/last wins agree. |
| 177 | 0195 | Hold: numeric integer fee silently rounds during undocumented float conversion. Enum/frozen dataclass/stop-at-empty/raw copying agree; broader numeric domain pending. |
| 178 | 0196 | Hold: non-ASCII sharp-s accepted after uppercase expansion to SS despite ASCII-only input contract. Ordinary Morse patterns/spacing/sampling agree. |
| 179 | 0197 | Hold: one-cell total of 1.0 becomes zero because unrelated large prefix absorbs it. Clipping, zero-width and immutable tuple semantics agree. |
| 180 | 0198 | Ordinary equality-based partition/dedup and per-position deepcopy agree. Stateful equality/custom-copy contract limitations remain pending; no new hold. |

Twelve pinned Python 3.11.15 probes, network disabled/resource limited, all exit
1 without timeout. Holds remain review items, not final rejection decisions.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0183 | grid_leading_zero_coordinate_probe.py / grid-leading-zero-coordinate-result.json | 448 | Valid coordinate one raises ValueError. |
| 0184 | document_duplicate_code_probe.py / document-duplicate-code-result.json | 404 | Duplicate code not rejected. |
| 0188 | status_embedded_escape_probe.py / status-embedded-escape-result.json | 385 | Escape emitted with color disabled. |
| 0189 | catalog_nested_next_probe.py / catalog-nested-next-result.json | 401 | Next page absent from result. |
| 0190 | correlation_finite_cancellation_probe.py / correlation-finite-cancellation-result.json | 389 | Score 0.0 instead of 1.0. |
| 0191 | contacts_gzip_unicode_probe.py / contacts-gzip-unicode-result.json | 398 | Uncaught zlib.error; two spurious NDJSON errors. |
| 0192 | histogram_subnormal_probe.py / histogram-subnormal-result.json | 489 | ZeroDivisionError for valid endpoints. |
| 0187 | clustering_empty_large_radius_probe.py / clustering-empty-large-radius-result.json | 399 | OverflowError for empty input. |
| 0194 | profile_late_key_type_probe.py / profile-late-key-type-result.json | 379 | Required key TypeError not raised. |
| 0195 | exhibit_integer_fee_probe.py / exhibit-integer-fee-result.json | 416 | 2**53+1 fee rounded down. |
| 0196 | morse_nonascii_expansion_probe.py / morse-nonascii-expansion-result.json | 455 | Unsupported sharp-s accepted. |
| 0197 | region_single_cell_precision_probe.py / region-single-cell-precision-result.json | 498 | Isolated cell total 0.0 rather than 1.0. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 181. Original candidates/tests/sample/partition unchanged.
