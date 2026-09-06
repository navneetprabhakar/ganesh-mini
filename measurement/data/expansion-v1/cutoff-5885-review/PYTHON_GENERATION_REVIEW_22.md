# Python generation review, batch 22

Positions 316–330 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; four reproduced holds.
606 additive plus historical three = 609 holds; 1,563 unique outside-sample
inspections. No seven-criterion approval. Continue position 331.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 316 | 0360 | Ordered field errors, ordinary action rules, ignored fields and fresh errors agree. Whitespace-plus-overlength error aggregation, non-string new-key comparison and unhashable action domain remain pending; no new hold. |
| 317 | 0362 | Field order, missing order, per-value deep copies and validation agree for ordinary containers. Arbitrary copy behavior and mutable scalar subclasses remain pending; no new hold. |
| 318 | 0363 | Section/item order, required-key validation and separate per-pair deep copies agree ordinarily. Arbitrary copy behavior remains pending; no new hold. |
| 319 | 0364 | Hold: finite constant signal has infinite normalized DC magnitude. Ordinary DFT bin range and normalization agree. |
| 320 | 0366 | Integer arithmetic, wrapped display, full counter and validation before mutation agree. Integer-subclass restriction remains pending; no new hold. |
| 321 | 0370 | Deterministic signing, claim keys, active interval and fresh decoded objects agree ordinarily. Canonical base64 pad bits, duplicate JSON keys and deep malformed JSON exception normalization remain pending; no new hold. |
| 322 | 0371 | Hold: constructor swallows a TypeError from copying and replaces it with ValueError, contrary to explicit propagation rule. Ordinary crate order and copies agree. |
| 323 | 0372 | Authorization, ASCII post IDs, Cc control rejection and sorted CSS agree ordinarily. Mutable scalar subclasses and unhashable query domains remain pending; no new hold. |
| 324 | 0367 | Hold: create_config emits a valid Unicode account that parse_config rejects because splitlines splits inside its JSON string. Signed integer grammar is also ambiguous between prompt and original test; not a separate reproduced hold. |
| 325 | 0373 | Exact gap arithmetic, label tie ordering, duplicate validation and new output lists agree; no new hold. |
| 326 | 0374 | Stored plugin identity, changing splits, load order and phase advancement for empty halves agree; no new hold. Public plugin mutation/exception domains remain pending. |
| 327 | 0375 | Arbitrary integer conversion, alphabet checks and sign agree. Immutable string interning is not a mutable alias defect; no new hold. |
| 328 | 0376 | FIFO exact-object identity, overflow atomicity, offsets and in-place clear agree. Original test excludes boolean offsets where prompt is less explicit; domain clarification pending, no new hold. |
| 329 | 0377 | Locale labels, required fields, fresh structures and collection copies agree ordinarily. Mutable scalar-subclass breadth remains pending; no new hold. |
| 330 | 0378 | Hold: singleton special case violates floor-defined bins. Original test expects that contradictory behavior. Numeric domain/overflow review remains pending. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up
under QUALITY_STRATUM_609_BACKUP.md, through Python position 330.

Four pinned Python 3.11.15 probe runs, network disabled/resource limited, all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0364 | frequency_large_constant_probe.py / frequency-large-constant-result.json | 332 | DC magnitude inf instead of 1e308. |
| 0371 | parcel_copy_typeerror_probe.py / parcel-copy-typeerror-result.json | 327 | Copy sentinel TypeError replaced with ValueError. |
| 0367 | config_unicode_roundtrip_probe.py / config-unicode-roundtrip-result.json | 428 | Parser raises ValueError on canonical output with U+2028. |
| 0378 | grid_singleton_floor_bins_probe.py / grid-singleton-floor-bins-result.json | 352 | Actual [[7, 0.0]], prompt requires [[0.0, 7]]. |
