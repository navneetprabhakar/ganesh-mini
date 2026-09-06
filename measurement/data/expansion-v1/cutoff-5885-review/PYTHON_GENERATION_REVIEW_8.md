# Python generation review, batch 8

Positions 106–120 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; eight reproduced holds.
528 additive plus historical three = 531 holds; 1,353 unique outside-sample
inspections. These are scoped inspections, not seven-criterion approvals.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 106 | 0115 | Exact hexadecimal validation, first-digit modulo and per-entry independent deepcopies agree. No new hold. |
| 107 | 0116 | Full monotonic validation and minimum resulting start-time/index tie-break agree. No new hold. |
| 108 | 0117 | Inclusive clipping, pre-clipping reversal checks and ordered boolean painting agree. Large-board resource envelope pending; no new hold. |
| 109 | 0118 | Hold: finite integer target 10**400 raises OverflowError even for empty profiles. Ordinary adjustment selection/ties and independent profile copies agree. |
| 110 | 0120 | Consecutive-frame stopping, all-key validation and integer nearest-neighbor indices agree. Boolean keys use the explicit invalid-key ValueError interpretation; no new hold. |
| 111 | 0122 | Hold: accepted large equal integer prices overflow validation although changes and scaled ranges are zero. Reserved derived-field collisions remain a separate wording question. |
| 112 | 0123 | Hold: unhashable unsupported policy raises TypeError instead of exact ValueError message. Stable descending sorting and full deepcopy agree. |
| 113 | 0124 | Hashability/duplicate/unknown checks, aligned counts and Shannon calculation agree. Empty entropy is numerically zero; no strict float-type condition imposed. No new hold. |
| 114 | 0125 | Hold: finite integer vector 10**400 raises OverflowError. Retained-row ordering, width and selection semantics otherwise agree. |
| 115 | 0126 | Hold: exact integer-only sum 10**400+7 is blocked by float-based finite validation. |
| 116 | 0128 | Hold: publicly mutated Boolean node value is accepted by merge despite task-wide integer requirement. Stable pairwise relinking and cycle/shared-node checks agree; temporary sentinel is not a replacement output node. |
| 117 | 0130 | Hold: unhashable event_code causes TypeError instead of malformed-input ValueError. Ordinary ordering, duplicates and unreserved labels agree. |
| 118 | 0131 | Balanced contiguous slicing, callback order/identity and unchanged exception propagation agree. Callback-caused input changes are not attributed to mapper; no new hold. |
| 119 | 0132 | First-unused suffix allocation on whole names and immediate occupancy agree. Repeated-name quadratic search envelope pending; no new hold. |
| 120 | 0133 | Hold: unordered sets are accepted although encoder inputs must be sequences. Integer drift, baseline and independent clamping agree. |

Eight pinned Python 3.11.15 probes, network disabled and resource limited,
each exit 1 without timeout. Candidate/task/probe/runtime hashes are preserved.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0118 | profiles_integer_target_probe.py / profiles-integer-target-result.json | 479 | OverflowError for finite target on empty input. |
| 0122 | quotes_integer_price_probe.py / quotes-integer-price-result.json | 465 | OverflowError before zero-change/range output. |
| 0123 | order_policy_probe.py / order-policy-result.json | 422 | TypeError for policy=[]. |
| 0125 | matrix_integer_probe.py / matrix-integer-result.json | 454 | OverflowError in finite integer vector validation. |
| 0126 | measurement_integer_sum_probe.py / measurement-integer-sum-result.json | 409 | OverflowError before exact integer-only addition. |
| 0128 | chain_mutated_value_probe.py / chain-mutated-value-result.json | 407 | ValueError not raised for Boolean public node value. |
| 0130 | reservation_code_probe.py / reservation-code-result.json | 369 | TypeError at unhashable event lookup. |
| 0133 | wheel_nonsequence_probe.py / wheel-nonsequence-result.json | 375 | Empty set inputs accepted without TypeError. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 121. No frozen sample/partition change, new VM or admission seal.
