# Python generation review, batch 4

Positions 46–60 of 684, v6 outside-sample Python generation queue. Fifteen full
prompt/reference/original-test inspections; four sandbox-confirmed holds.
500 additive plus historical three = 503 holds; 1,293 unique outside-sample
inspections. Scope v6 unchanged. No admission seal or seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 46 | 0049 | ASCII letter counts and first-occurrence tie handling agree. No new hold. |
| 47 | 0052 | First-character capitalization and preservation of remaining text agree. No new hold. |
| 48 | 0053 | Validation before mutation, cross-section IDs, sorted labels and independent repeated seals agree. No new hold. |
| 49 | 0054 | Bounded-width cursor DP and modular recurrence agree. Extreme action-count resource envelope pending; no new hold. |
| 50 | 0050 | Hold: permitted nonempty Unicode stored hash causes TypeError during login instead of AuthError. Stored-hash case normalization remains a separate contract question. |
| 51 | 0051 | Framing/checksum/status callback order agree. Empty-bytes identity and mutable callback retention boundaries pending; no new hold. |
| 52 | 0055 | Hold: finite integer 10**400 causes OverflowError during finite-value validation. |
| 53 | 0057 | Hold: invalid negative integer -10**400 causes OverflowError instead of ValueError. Positive unrepresentable float outputs remain a separate contract question. |
| 54 | 0059 | Typed null validation precedes enum lookup; stable present/null identity partition agrees. No new hold. |
| 55 | 0060 | Locked/fault transitions and copied accepted history agree. Custom equality behavior is not imposed as a new requirement; no new hold. |
| 56 | 0061 | Invalid string filtering, exact pipe count and trimmed session counting agree. No new hold. |
| 57 | 0062 | Complete integer validation and every-third-position selection agree. Triviality criterion pending; no new hold. |
| 58 | 0063 | Hold: valueless rel becomes None and aborts recovery with AttributeError, losing later recoverable image links. |
| 59 | 0064 | Full normalization/validation, cyclic win relationships and fresh ordered round dictionaries agree. No new hold. |
| 60 | 0065 | Integer/boolean validation, stable modulo sharding, final-batch dropping and cross-input deepcopy agree. Intra-output shared identity is not prohibited by the contract; no new hold. |

All four probes used pinned Python 3.11.15 in network-disabled resource-limited
sandbox, each exit 1 without timeout. Result files preserve candidate, task,
probe and sandbox hashes; frozen candidates and original tests are unchanged.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0050 | permit_unicode_hash_probe.py / permit-unicode-hash-result.json | 567 | hmac comparison raises TypeError for non-ASCII stored hash. |
| 0055 | extremes_integer_probe.py / extremes-integer-result.json | 463 | Finite integer cannot be converted to float by math.isfinite. |
| 0057 | bucket_negative_integer_probe.py / bucket-negative-integer-result.json | 460 | OverflowError rather than required invalid-input ValueError. |
| 0063 | preload_valueless_rel_probe.py / preload-valueless-rel-result.json | 444 | None.lower AttributeError before later image is recovered. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue Python position 61. No new VM or training seal.
