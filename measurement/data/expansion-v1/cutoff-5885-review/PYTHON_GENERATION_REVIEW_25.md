# Python generation review, batch 25

Positions 361–375 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; five reproduced holds.
625 additive plus historical three = 628 holds; 1,608 unique outside-sample
inspections. No seven-criterion approval. Continue position 376.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 361 | 0411 | Code equality/hash, first description, checked-out uniqueness and sorted immutable containers agree ordinarily. Equipment validation test contains malformed cases that raise via argument unpacking; coverage remains pending. Cross-depot policy and mutable public scalar attributes remain pending; no new hold. |
| 362 | 0412 | Left-to-right uncoerced arithmetic, identities, validation timing and closure binding agree; no new hold. |
| 363 | 0413 | Hold: retains empty columns despite explicit output exception; original test contradicts prompt. Ordinary strict-boundary classification and positive precedence agree. Numeric/sequence breadth remains pending. |
| 364 | 0414 | Signed magnitude padding, inclusive range, reversal and newline behavior agree. Runtime decimal-digit conversion limit remains pending; no new hold. |
| 365 | 0416 | Hold: concatenation permits a search substring to span separate fields. Ordinary first matching duplicate, sorting, paging and deep copies agree. ID-domain breadth remains pending. |
| 366 | 0418 | Once materialization, integer validation and earliest maximum tie agree; no new hold. |
| 367 | 0419 | Exact bool mask, complete validation and independent selected-row copies agree ordinarily. Arbitrary copy behavior remains pending; no new hold. |
| 368 | 0415 | Canonical live-record identity is explicitly required and preserved; metadata input copy and sorted snapshot agree. Mutation of indexed code through live record leaves ambiguous sorting/index semantics; pending, no new hold. |
| 369 | 0417 | Pre-update training loss, gradient update, post-update validation and strict-improvement patience agree ordinarily. Extreme arithmetic, all-nonfinite losses and pair-container breadth remain pending; no new hold. |
| 370 | 0420 | Iterative chain/cycle traversal, first-record deduplication, encountered-page validation and copies agree ordinarily. None-start versus malformed outer container is ambiguous; arbitrary copy behavior pending, no new hold. |
| 371 | 0421 | Descending products, self-iterator and reset-on-StopIteration agree with this explicit nonstandard restart contract; no new hold. |
| 372 | 0422 | Hold: unhashable unknown type raises TypeError instead of ValueError. Ordinary shapes, products, spec keys and index copies agree. Plane upper-bound policy and scalar-subclass breadth remain pending. |
| 373 | 0424 | Hold: numeric range rows are valid sequences but rejected. Ordinary windows, gaps, labels, copies and read-only properties agree. Zero-width row and general sequence domains remain pending. |
| 374 | 0425 | Hold: equal opposite large products return NaN instead of 0.5. Ordinary stable logistic branches and validation-before-update agree. Adjustment overflow remains pending. |
| 375 | 0426 | Full validation precedes callbacks; row-major once calls, truth conversion and unchanged exception propagation agree ordinarily. Callback mutation of source during traversal remains pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up
under QUALITY_STRATUM_629_BACKUP.md, through Python position 390.

Five pinned Python 3.11.15 probe runs, network disabled/resource limited, all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0413 | classify_empty_columns_probe.py / classify-empty-columns-result.json | 660 | Unexpected empty a/b columns in output. |
| 0416 | specimen_cross_field_match_probe.py / specimen-cross-field-match-result.json | 391 | Cross-field query incorrectly selects record. |
| 0422 | transform_unhashable_type_probe.py / transform-unhashable-type-result.json | 476 | TypeError instead of ValueError. |
| 0424 | window_range_row_probe.py / window-range-row-result.json | 350 | TypeError for numeric range rows. |
| 0425 | signal_cancelled_large_products_probe.py / signal-cancelled-large-products-result.json | 321 | NaN instead of 0.5. |
