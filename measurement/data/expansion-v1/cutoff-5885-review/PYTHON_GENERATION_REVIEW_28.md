# Python generation review, batch 28

Positions 406–420 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; four reproduced holds.
636 additive plus historical three = 639 holds; 1,653 unique outside-sample
inspections. No seven-criterion approval. Continue position 421.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 406 | 0467 | Entire payload validation precedes converter calls, including skipped categories; ordinary counts/order/container independence agree. Callback mutation and collection breadth pending; no new hold. |
| 407 | 0468 | Hold: malformed label field raises TypeError instead of specified ValueError. Ordinary registry ordering, patches and nested copies agree; public-field mutation/custom copying pending. |
| 408 | 0469 | Stable combined order, required adjacent swaps/early exit, full validation and ordinary deep copies agree. Arbitrary-copy domains pending; no new hold. |
| 409 | 0470 | Lifecycle, independent buffers, consumed rejected lines, decimal parsing and four-character boundary agree; no new hold. |
| 410 | 0471 | Hold: root directory in virtual entries is rejected by shared file-path validation. Ordinary nearest marker, direct-child and profile-before-anchor ordering agree. File/directory distinction remains under-specified. |
| 411 | 0473 | Page-gap stopping, visited-page prefilter validation, duplicates and ordinary nested copies agree. Required-fields wording says both exactly and extras allowed; implementation follows explicit extras allowance. No new hold. |
| 412 | 0474 | Ordinary full event/reference validation precedes counter change; duplicates and nested copies agree. Unreferenced store-key validation, shared input aliases and arbitrary-copy domains pending; no new hold. |
| 413 | 0472 | All-input validation, Cartesian order, exact integer formulas and fresh shape tuples agree. Scalar-subclass breadth pending; no new hold. |
| 414 | 0475 | Hold: Unicode long s accepted as ASCII S. Kelvin-sign probe did not reproduce acceptance and is preserved as negative evidence. Ordinary checksum, repetition and ASCII token boundaries agree. |
| 415 | 0476 | Mapping/field validation, ordered queries and ordinary record copies agree. Outer iterable and scalar-subclass contact-copy domains pending; no new hold. |
| 416 | 0477 | Consecutive duplicate handling, stop/read-only state and ordinary returned copies agree. Error precedence after stopping is not separately resolved; no new hold. |
| 417 | 0478 | Hold: whitespace-only title accepted despite blank-title rejection requirement. Ordinary count/record/finite coordinate validation and formatting agree. Decimal grammar breadth pending. |
| 418 | 0479 | Ordinary environment/workers selection, class attributes and independent discovery copies agree. Equality-compatible non-string environment objects pending; no new hold. |
| 419 | 0480 | Exact concatenation/count/newline rules agree for ordinary strings. Embedded newline in timestamp/target conflicts with literal one-line wording and remains pending; no new hold. |
| 420 | 0481 | Identifier/keyword validation, exact file output, ordered deduplication and independent containers agree. Unicode normalization and scalar-subclass breadth pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up;
see QUALITY_STRATUM_639_BACKUP.md for verified evidence through position 420.

Five pinned Python 3.11.15 probe runs, network disabled/resource limited; no
timeouts. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Exit / observed finding |
| --- | --- | ---: | --- |
| 0468 | asset_field_exception_probe.py / asset-field-exception-result.json | 360 | 1; TypeError for invalid label. |
| 0471 | bundle_root_entry_probe.py / bundle-root-entry-result.json | 315 | 1; ValueError for root entry. |
| 0475 | part_code_kelvin_probe.py / part-code-kelvin-result.json | 310 | 0; Kelvin example correctly rejected, no hold from this probe. |
| 0475 | part_code_long_s_probe.py / part-code-long-s-result.json | 387 | 1; returned SAA0000U for non-ASCII input. |
| 0478 | waypoint_blank_title_probe.py / waypoint-blank-title-result.json | 331 | 1; whitespace-only title returned in header. |
