# Python generation review, batch 20

Positions 286–300 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; two reproduced holds.
598 additive plus historical three = 601 holds; 1,533 unique outside-sample
inspections. No seven-criterion approval. Continue position 301.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 286 | 0328 | Logical segment stack, rootedness, parent-underflow and NUL rejection agree; no new hold. |
| 287 | 0329 | JSON parsing, defaults, bounded retries, unique labels and fresh containers agree ordinarily. Nonstandard JSON constants and duplicate-key policy remain pending; no new hold. |
| 288 | 0325 | Exact integer totals, size boundaries, input order and required summary/lookup identity agree. Mutable scalar subclasses remain pending; no new hold. |
| 289 | 0326 | Axis ordering, duplicate checks, ratios and independent row lists agree ordinarily. Extreme integer finite checks remain pending; no new hold. |
| 290 | 0327 | Required schema replacements and unrelated content copies agree ordinarily. Internal aliases explicitly must be preserved; aliases crossing replaced fields create an unresolved contract ambiguity, not a new hold. |
| 291 | 0331 | Complete validation before state change, marker priority, tie-left turns, heading normalization and reset agree; no new hold. |
| 292 | 0332 | Bytearray payload copies, empty segments and half-open offsets agree. Empty bytes as outer iterable is rejected despite general empty-iterable wording; domain ambiguity pending, no new hold. |
| 293 | 0333 | isqrt and exact integer ranges meet arbitrary-integer arithmetic contract; no new hold. |
| 294 | 0335 | Active-cell bounding rectangle, complete validation and independent row slices agree. Active-coordinate allocation is unnecessary but no space bound specified; no new hold. |
| 295 | 0336 | Hold: arbitrary object label can be a function whose mutable attributes remain shared through deepcopy, exposing stored state. Ordinary transformation/copy paths agree. |
| 296 | 0338 | Frozen members, duplicate-code preservation, tuple property and original-text formatting agree; no new hold. |
| 297 | 0339 | Hold: finite radius 1e200 with zero length raises OverflowError instead of zero volume/area. Ordinary real-number validation/formulas agree. |
| 298 | 0340 | First repeated occurrence, exact counts, first-appearance order and fresh mapping agree; no new hold. |
| 299 | 0342 | CRUD ordering, monotonic IDs and tag-list copies agree ordinarily. Mutable scalar subclasses and custom copy failures remain pending; no new hold. |
| 300 | 0337 | Row-major children and per-occurrence row copies agree. Integer-subclass domain remains pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. Previous GCS authentication
block resolved; this batch is backed up under QUALITY_STRATUM_601_BACKUP.md.

Two pinned Python 3.11.15 probe runs, network disabled/resource limited, both
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0336 | sample_function_label_probe.py / sample-function-label-result.json | 601 | Returned label mutation reaches stored function attributes. |
| 0339 | pipe_zero_length_large_radius_probe.py / pipe-zero-length-large-radius-result.json | 624 | OverflowError before multiplication by zero. |
