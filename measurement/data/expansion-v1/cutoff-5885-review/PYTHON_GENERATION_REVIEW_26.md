# Python generation review, batch 26

Positions 376–390 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; one reproduced hold.
626 additive plus historical three = 629 holds; 1,623 unique outside-sample
inspections. No seven-criterion approval. Continue position 391.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 376 | 0427 | Exact index schema, ID validation, sorted query and fresh label lists agree ordinarily. Invalid query-index shape and mutable scalar-subclass breadth remain pending; no new hold. |
| 377 | 0429 | Monotonic IDs, rename validation before absent lookup, view shape and ordinary metadata copies agree. Copy-failure allocation and mutable name subclasses remain pending; no new hold. |
| 378 | 0431 | Exact-class singleton registry, later argument validation, first successful initialization and read-only fields agree ordinarily. Concurrency and custom subclass initialization remain pending; no new hold. |
| 379 | 0432 | Issuance order, non-reused IDs, validation for absent targets and independent ordinary outputs agree. Copy-failure allocation semantics remain pending; no new hold. |
| 380 | 0433 | Rotation normalization, ordered transforms, independent scale cells and copies agree ordinarily. List-form operations versus tuple examples and arbitrary copy behavior remain pending; no new hold. |
| 381 | 0434 | Insertion order, empty revisions, chronological history and ordinary nested-copy separation agree. Failed-copy revision atomicity is unspecified and remains pending; no new hold. |
| 382 | 0436 | Exact table order, row validation, active-source filtering and per-row copies agree ordinarily. Arbitrary copy/scalar subclasses remain pending; no new hold. |
| 383 | 0437 | Exact Fraction arithmetic, full integer validation and short-input fresh lists agree; no new hold. |
| 384 | 0441 | Required fields, casefold plus original-string sorting, ordered escaping and no trailing newline agree. Embedded line breaks and decimal digit limits remain pending; no new hold. |
| 385 | 0443 | Alphanumeric filtering precedes per-character Unicode casefold, then reversal; empty and expanded-fold behavior agree; no new hold. |
| 386 | 0444 | Trimmed casefold site identity, exact secrets, duplicate tags, sorted export and ordinary copies agree. Mutable secret subclasses and arbitrary copy behavior remain pending; no new hold. |
| 387 | 0439 | Hold: finite Celsius input has representable Fahrenheit result but intermediate multiplication returns infinity. Ordinary filter, order and copies agree; numeric-domain breadth remains pending. |
| 388 | 0442 | Default/override validation, first-spelling casefold deduplication and separate configuration copies agree ordinarily. Mutable subject/body subclasses remain pending; no new hold. |
| 389 | 0446 | Complete-word lookup, case-sensitive titles, two-sentence split and full mapping validation agree ordinarily. Unicode regex case equivalence and multiple command words remain pending; no new hold. |
| 390 | 0449 | Independent ID counters, cascades, placement order, idempotent watches and ordinary copies agree. Failed-text ID allocation and ID type breadth remain pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up
under QUALITY_STRATUM_629_BACKUP.md, through Python position 390.

One pinned Python 3.11.15 probe run, network disabled/resource limited, exit 1
without timeout. Hold is a review item, not a final rejection.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0439 | station_fahrenheit_overflow_probe.py / station-fahrenheit-overflow-result.json | 365 | Current temperature inf instead of approximately 3.6e307. |
