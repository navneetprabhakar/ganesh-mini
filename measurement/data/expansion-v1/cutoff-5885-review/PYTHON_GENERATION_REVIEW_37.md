# Python generation review, batch 37

Positions 541–555 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; six reproduced holds.
677 additive plus historical three = 680 holds; 1,788 unique outside-sample
inspections. No seven-criterion approval. Continue position 556.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 541 | 0636 | Hold: noniterable absence field raises TypeError instead of ValueError. Ordinary window inclusion, validation outside window, counts and first-day/group order agree. |
| 542 | 0632 | Ordinary instrument order, interleaving, unmatched start, byte validation and tuple output agree; no new hold. |
| 543 | 0642 | Hold: unit segment at integer origin 2**53 collapses to zero length. Ordinary route order and charge formula agree. Route result finiteness and other numeric breadth pending. |
| 544 | 0639 | Hold: finite integer 10**400 rejected by float-based finiteness check. Ordinary stride indexing, active/completed clearing and returned copies agree. |
| 545 | 0640 | Ordinary check ordering, context identity, exception continuation and intentional within-result alias preservation agree. Reentrant registration, noncopyable returns and exception formatting breadth pending; no new hold. |
| 546 | 0641 | Hold: valid decimal zero index with 5000 zero digits raises conversion ValueError. Ordinary path variables, wildcard order and output graph alias preservation agree; empty-expansion validation scope pending. |
| 547 | 0644 | Ordinary one fetch, frozen variants, duplicate keys and fetch exception identity agree. Extra-key wording and malformed returned iterable handling pending; no new hold. |
| 548 | 0645 | Hold: nullable update changes unrelated aliased column in both upgrade/downgrade. Ordinary metadata preservation, copies and idempotence agree. Immutable Mapping support pending. |
| 549 | 0646 | Ordinary logging, detached record copies, save calls and repeated-source separation agree. Save-return-value interpretation and mutable extended record fields pending; no new hold. |
| 550 | 0643 | Ordinary stopwatch transitions, integer cap, reset and fresh state dictionaries agree. Starting after cap follows explicit original test; prompt interpretation noted, no new hold. |
| 551 | 0649 | Ordinary binary validation, tie-to-one, inverse and exact base-2 product agree; no new hold. |
| 552 | 0650 | Hold: NaN accepted as positive scale. Ordinary scaled coordinates, ordering and separate metadata copies agree. General numeric/sequence breadth and mixed layout-key validation pending. |
| 553 | 0651 | Exact hexadecimal grammar, arbitrary allowed separator placement, normalization and complete allowlist validation agree; no new hold. |
| 554 | 0652 | Ordinary depth limits, terminal nodes, shorter-path revisits, cycle suppression and exclusions agree. Prefix container breadth pending; no new hold. |
| 555 | 0654 | Ordinary stage suffix, option validation/overrides and separate mutable containers agree. Scalar-subclass copying and unspecified bool position wording pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up
through 682 holds / Python position 570; see QUALITY_STRATUM_682_BACKUP.md.

Six pinned Python 3.11.15 probes, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0636 | absence_malformed_iterable_probe.py / absence-malformed-iterable-result.json | 622 | TypeError for malformed absent field. |
| 0642 | route_integer_precision_probe.py / route-integer-precision-result.json | 420 | Zero instead of unit route length. |
| 0639 | stroke_large_integer_probe.py / stroke-large-integer-result.json | 434 | OverflowError for finite integer coordinate. |
| 0641 | select_values_zero_index_probe.py / select-values-zero-index-result.json | 494 | Valid index zero rejected by decimal conversion limit. |
| 0645 | schema_shared_column_probe.py / schema-shared-column-result.json | 427 | Both operations also change unrelated column. |
| 0650 | layout_nan_positive_probe.py / layout-nan-positive-result.json | 449 | No ValueError for NaN scale. |
