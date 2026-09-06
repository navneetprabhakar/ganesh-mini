# Python generation review, batch 3

Positions 31–45 of 684, v6 outside-sample Python generation queue. Fifteen full
prompt/reference/original-test inspections; four sandbox-confirmed holds.
496 additive plus historical three = 499 holds; 1,278 unique outside-sample
inspections. Scope v6 unchanged. No admission seal or seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 31 | 0032 | Full validation then frozen bindings preserve input order and labels. No new hold. |
| 32 | 0033 | Hold: two finite 1e308 track widths overflow total width, yielding NaN/infinite centers instead of representable offsets. |
| 33 | 0034 | Ordered counts, frozen tuples and integer exact sum agree. Float mean beyond representable range remains a contract envelope question; no new hold. |
| 34 | 0035 | Hold: in-range quantity with 5,000 leading zeroes rejected by pinned Python integer-string limit. |
| 35 | 0036 | Required keys, duplicate extras, ASCII year/color/serial checks agree. Wider Unicode blank-line interpretation pending; no new hold. |
| 36 | 0037 | All-notice validation, priority/id selection and full deep copy agree. No new hold. |
| 37 | 0038 | Concrete enums, boolean exclusions, capacity/duplicate checks and staged debit agree. Unspecified public plan reassignment not imposed as a requirement; no new hold. |
| 38 | 0039 | Recursive dictionary merge and independent replacement/defaults agree. Cyclic inputs and meaning of JSON-like finite numbers remain pending; no new hold. |
| 39 | 0040 | Heap selection key and final stable start order preserve duplicates and deep copies. Full validation at zero limit agrees; no new hold. |
| 40 | 0042 | Request identity, permissions, transitions and copied payload snapshots agree. Unspecified competing error precedence not strengthened; no new hold. |
| 41 | 0043 | Ordinary integer modulo and half-open wrap windows agree. Exact-int versus int-subclass acceptance remains pending; no new hold. |
| 42 | 0044 | Exact pre-normalization uniqueness, sorted labels and copy-exception mapping agree. Custom deepcopy hooks returning mutable identity remain a contract boundary; no new hold. |
| 43 | 0045 | Hold: unhashable kind/level raises TypeError instead of required ValueError. Ordinary LIFO and finish order agree. |
| 44 | 0048 | Full validation, score/input ranking and independent unlimited related-link order agree. Exact-int subclass boundary pending; no new hold. |
| 45 | 0047 | Hold: unhashable change/remove IDs raise TypeError instead of required ValueError. Ordinary copied sequential mutation agrees. |

All four probes used pinned Python 3.11.15 in network-disabled resource-limited
sandbox, each exit 1 without timeout. Original task, candidate and probe hashes
are preserved in each result; no candidate/test alteration.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0033 | rail_width_finite_probe.py / rail-width-finite-result.json | 452 | First center (nan, -inf), not (0.0, -5e307). Second assertion was not reached. |
| 0035 | quantity_leading_zeros_probe.py / quantity-leading-zeros-result.json | 525 | ValueError at 4,300-digit conversion limit on 5,001 digits representing one. |
| 0045 | span_enum_validation_probe.py / span-enum-validation-result.json | 476 | Both kind=[] and level=[] raised TypeError. |
| 0047 | registry_id_validation_probe.py / registry-id-validation-result.json | 455 | Both change/remove id=[] raised TypeError. |

Candidate-file SHA-256 unchanged:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue Python position 46. No new VM or training seal.
