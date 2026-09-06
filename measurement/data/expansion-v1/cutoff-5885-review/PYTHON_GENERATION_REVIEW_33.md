# Python generation review, batch 33

Positions 481–495 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; five reproduced holds.
659 additive plus historical three = 662 holds; 1,728 unique outside-sample
inspections. No seven-criterion approval. Continue position 496.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 481 | 0560 | Hold: signed noncanonical JSON with duplicate sub claim accepted. Ordinary deterministic issuance, timing-safe comparison, expiry and uniform parsing errors agree. Canonical-reader enforcement versus issuer-only interpretation needs disposition. |
| 482 | 0562 | Exact float type, property validation, schema assignment/getter copies and nested mapping agree ordinarily. Mapping type-error conventions and mutable scalar subclasses pending; no new hold. |
| 483 | 0563 | Ordinary model validation, creator activity checks, price/SKU order and catalog copies agree. Public-field mutation before insertion and arbitrary-copy domains pending; no new hold. |
| 484 | 0564 | Hold: mutating parser receives caller-owned raw input, violating no-input-mutation boundary. Ordinary prevalidation, duplicate acceptance state and assessment copies agree. Error-name alias and callback ownership breadth pending. |
| 485 | 0561 | Exact integer sign counts, first malformed element and ordinary one-shot consumption agree; no new hold. |
| 486 | 0566 | Ordinary zero shapes, reset/load validation, float storage and independent matrices agree. General sequences, large numeric conversion and public dimension mutation pending; no new hold. |
| 487 | 0568 | Exact integer balance/transfer arithmetic, same-account handling and ordinary failure atomicity agree. Scalar-subclass arithmetic breadth pending; no new hold. |
| 488 | 0569 | Hold: valid monetary string with long zero prefix raises runtime conversion ValueError instead of returning 100 cents. Ordinary grammar, error precedence, sign and quantity inversion agree. |
| 489 | 0565 | Hold: repeated reference to one input record is normalized twice, yielding -2 instead of 0. Ordinary independent-record imputation/variance/copies agree. Nonfinite/numeric overflow and broader sequence domains pending. |
| 490 | 0567 | Ordinary BFS, cycle/duplicate suppression, reachability and exact entry output agree. Entry extras and unreachable identifier validation wording versus tests pending; no new hold. |
| 491 | 0570 | Ordinary dense/sparse tie and absent-bit behavior, identical duplicates and exact binary product agree. Malformed element exception distinction and general sequence breadth pending; no new hold. |
| 492 | 0571 | Hold: distinct exact integer constant polynomials compare equal after float coercion at zero tolerance. Ordinary Horner evaluation, inclusive tolerance and structural validation agree; other numeric breadth pending. |
| 493 | 0572 | Ordinary exact quantum rounding, independent metadata, callback target binding and pre-callback validation agree. Request sequence restriction and arbitrary-copy guarantees pending; no new hold. |
| 494 | 0574 | Ordinary encounter order, cache/duplicate filtering and separate metadata copies agree. Empty cached key restriction and old-style iterables pending; no new hold. |
| 495 | 0575 | Ordinary prefix cycling, all-input validation at zero count and distinct dictionaries agree. Mutable scalar-subclass destination domain pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch awaits backup;
last verified backup is through 657 holds / Python position 480.

Five pinned Python 3.11.15 probe runs, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0560 | credential_duplicate_claim_probe.py / credential-duplicate-claim-result.json | 347 | Duplicate sub claim accepted, last value wins. |
| 0564 | inbox_parse_input_mutation_probe.py / inbox-parse-input-mutation-result.json | 317 | Parser mutates raw input. |
| 0569 | cents_long_zero_prefix_probe.py / cents-long-zero-prefix-result.json | 388 | Runtime 4300-digit limit rejects valid amount. |
| 0565 | measurements_repeated_record_probe.py / measurements-repeated-record-result.json | 353 | Both repeated rows have -2 instead of 0. |
| 0571 | polynomial_integer_precision_probe.py / polynomial-integer-precision-result.json | 313 | Distinct integer constants reported equal at zero tolerance. |
