# Python generation review, batch 27

Positions 391–405 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; six reproduced holds.
632 additive plus historical three = 635 holds; 1,638 unique outside-sample
inspections. No seven-criterion approval. Continue position 406.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 391 | 0445 | Exact authentication identity, ordered duplicate preservation and ordinary field filters/copies agree. Original scalar-validation cases contain extra list wrappers, weakening coverage; filter and mapping-copy breadth remain pending, no new hold. |
| 392 | 0452 | Hold: validation MSE overflows during accumulation although its mean is representable. Ordinary minibatch averaging, reset and history behavior agree. Numeric/pair breadth remains pending. |
| 393 | 0453 | Hold: Unicode decimal digit rejected by assess despite its unrestricted decimal-digit category. Create explicitly selects ASCII and behaves accordingly; ordinary thresholds/fallback cycling agree. |
| 394 | 0455 | Ordinary custom exceptions, counts, seat validation and details copies agree. Falsey dictionary subclasses and unhashable reference/role domains remain pending; no new hold. |
| 395 | 0456 | Hold: coerced integer remainder differs from Python integer modulo. Ordinary formulas/vector shape agree; other exact arithmetic and numeric breadth remain pending. |
| 396 | 0451 | Hold: finite turn inputs overflow heading, breaking required unit-direction accessor. Ordinary capture, rotation-before-movement and diagonal normalization agree. |
| 397 | 0458 | Question storage, missing answers, cumulative/reset score and fresh containers agree ordinarily. General sequence support and malformed extra answers versus ignore-extras rule remain pending; no new hold. |
| 398 | 0459 | Exact fuel arithmetic, affordable-zero boundaries, stop count and second-toll refueling agree; no new hold. |
| 399 | 0460 | Exact field mapping, defaults, original strings and per-record label copies agree ordinarily. Scalar-subclass breadth remains pending; no new hold. |
| 400 | 0461 | Hold: device_kind is not excluded as an option, creating conflicting output requirements and overwriting the profile kind. Other Cartesian ordering, global columns and copies agree ordinarily. Contract disposition required, not an automatic implementation-only rejection. |
| 401 | 0462 | Days validation/copies, dual identity conflicts, insertion order and ordinary target copies agree. Pre-add mutation of public target fields and custom copying remain pending; no new hold. |
| 402 | 0463 | Existing order, missing-by-code defaults and ordinary deep copies agree. Boolean priority restriction is not explicit in prompt; domain clarification pending, no new hold. |
| 403 | 0464 | Required recursive insertion/sorting, same-list return and validation-before-mutation agree ordinarily. Runtime depth limits and mutation on recursion failure remain pending; no new hold. |
| 404 | 0465 | Family/member shapes, duplicate-name rule, name sorting and separate skill copies agree ordinarily. Scalar-subclass breadth remains pending; no new hold. |
| 405 | 0466 | Hold: CRLF blank-line separators fail. Ordinary LF card shape and validate-before-callback copies agree. Whitespace-only separators and answer-number grammar remain pending. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up;
see QUALITY_STRATUM_639_BACKUP.md for verified evidence through position 420.

Six pinned Python 3.11.15 probe runs, network disabled/resource limited, all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0452 | affine_validation_mean_overflow_probe.py / affine-validation-mean-overflow-result.json | 500 | Infinite MSE instead of approximately 1e308. |
| 0453 | badge_unicode_decimal_probe.py / badge-unicode-decimal-result.json | 351 | Decimal digit reported missing. |
| 0456 | report_integer_remainder_probe.py / report-integer-remainder-result.json | 335 | Remainder 0.0 instead of 1. |
| 0451 | rover_finite_turn_overflow_probe.py / rover-finite-turn-overflow-result.json | 344 | get_direction raises ValueError after update returns. |
| 0461 | device_kind_option_collision_probe.py / device-kind-option-collision-result.json | 334 | device_kind overwritten with option value. |
| 0466 | cards_crlf_separator_probe.py / cards-crlf-separator-result.json | 318 | ValueError on two valid CRLF cards. |
