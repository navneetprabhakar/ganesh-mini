# Python generation review, batch 9

Positions 121–135 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; nine reproduced holds and
one static contradiction. 538 additive plus historical three = 541 holds;
1,368 unique outside-sample inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 121 | 0134 | Hold: valid non-string sequence-protocol iterable is rejected by Iterable ABC check. Ordinary batch validation/ID allocation agree; custom return-copy failure atomicity remains pending. |
| 122 | 0135 | Hold: successfully parsed NaN learning rate is accepted despite positive-value requirement. Legacy iterable and process-global help-program-name behavior remain pending. |
| 123 | 0137 | Hold: fmean overflows for equal finite groups whose means and all differences are representable. Nonsequence set acceptance and combinatorial resource envelope remain pending. |
| 124 | 0138 | Hold: out-of-range integer discount raises OverflowError instead of ValueError. Legacy iterable acceptance remains an additional static concern. |
| 125 | 0136 | Hold: exact upper endpoint 2**53+1 rounds down to 2**53. Ordinary direction and halfway handling agree. |
| 126 | 0139 | Full record validation, casefold matching, filtering before reset and ID sorting agree. reset_ids domain remains unspecified; no new hold. |
| 127 | 0140 | Standard CSV quoting, missing/None space rendering, partitioning and sort agree. Arbitrary str conversion limits remain pending; no new hold. |
| 128 | 0141 | Signed integer ceiling-to-multiple formula and inclusive range agree; docstring covers contract. No new hold. |
| 129 | 0142 | Hold: ASCII-only regex discards Unicode alphanumeric letters/digits despite unrestricted alphanumeric wording. |
| 130 | 0144 | Hold: canonical year 0001 rejected by strftime roundtrip on pinned runtime. Ordinary chronological tie handling agrees. |
| 131 | 0143 | Hold: get(tuple_scalar) falls back to an unrelated normalized list-key bucket, contradicting scalar normalization to one-item tuple; original set-key test requires that fallback. Empty add membership-return wording remains pending. |
| 132 | 0145 | Generator validates bounds, exact formula and required consuming sum agree. No new hold. |
| 133 | 0147 | Hold: explicitly ignored extra generator field causes deepcopy failure before rendering. Stable sorts and normal destination handling agree. |
| 134 | 0150 | Exact Fraction elimination, pivoting, integral/range checks and input preservation agree. No new hold. |
| 135 | 0146 | Static hold: nonempty-tag prompt has no strip restriction; original tests and reference reject whitespace-only tags. Counts versus per-record co-occurrence agree. |

Nine pinned Python 3.11.15 probes, network disabled and resource limited,
all exit 1 without timeout. Static tag contradiction is not an executed test.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0134 | planting_legacy_iterable_probe.py / planting-legacy-iterable-result.json | 425 | TypeError for __getitem__ iteration protocol. |
| 0135 | options_nan_rate_probe.py / options-nan-rate-result.json | 423 | ValueError not raised for NaN learning rate. |
| 0137 | partition_equal_finite_probe.py / partition-equal-finite-result.json | 408 | fsum intermediate OverflowError inside fmean. |
| 0138 | offer_discount_range_probe.py / offer-discount-range-result.json | 528 | OverflowError for invalid 10**400 discount. |
| 0136 | position_endpoint_probe.py / position-endpoint-result.json | 376 | 9007199254740992 returned rather than 9007199254740993. |
| 0142 | notes_unicode_alnum_probe.py / notes-unicode-alnum-result.json | 473 | ['caf'] instead of ['café', '१२']. |
| 0144 | activity_early_year_probe.py / activity-early-year-result.json | 416 | ValueError for canonical 0001-01-01 timestamp. |
| 0143 | relation_tuple_key_probe.py / relation-tuple-key-result.json | 500 | Unrelated list-key value returned for tuple scalar. |
| 0147 | service_ignored_field_probe.py / service-ignored-field-result.json | 399 | Ignored generator deepcopy error misreported as noniterable records. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 136. Original candidates/tests/sample/partition unchanged.
