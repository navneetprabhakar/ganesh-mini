# Python generation review, batch 13

Positions 181–195 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; four reproduced holds.
567 additive plus historical three = 570 holds; 1,428 unique outside-sample
inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 181 | 0199 | Full grid validation, signed deltas and per-result deep copies agree. Row-container breadth remains pending; no new hold. |
| 182 | 0201 | Sorted combinations correctly implement casefold/original spelling ordering, including zero-size bundle. Combinatorial resource envelope pending; no new hold. |
| 183 | 0202 | Ticket invalidation, secret update, consumption, validation and fresh snapshots agree. Four-digit sequence wording beyond 9999 is ambiguous; no new hold. |
| 184 | 0203 | Default order, ordinary override validation and independent deep copies agree. Literal exact-type wording versus subclasses remains pending; no new hold. |
| 185 | 0204 | Full validation and exact integer displacement agree. Direct multiplication is equivalent to unit-step simulation; no new hold. |
| 186 | 0206 | Settings copies, ordinary connection reuse/close and validation-before-replacement agree. Externally mutated protocol and close methods that do not update closed remain pending; no new hold. |
| 187 | 0207 | Hold: finite negative integer below valid temperature raises OverflowError instead of NaN. Formula singularity at dewpoint -273.15 remains a contract-domain issue. |
| 188 | 0208 | Explicit Unicode word regex, casefold, first occurrence and separator validation agree; no new hold. |
| 189 | 0209 | Hold: integer temperature changes before one-decimal rendering. Embedded newlines versus exactly-three-lines and conversion overflow remain pending. |
| 190 | 0210 | Per-record tag dedup, global first occurrence, top sorting and independent columns agree; no new hold. |
| 191 | 0205 | Hold: non-real value in unselected sensor column bypasses row validation. Ordinary selected-prefix nearest match/ties/refit/copy behavior agree; distance overflow and sequence-container breadth pending. |
| 192 | 0211 | Ordinary filters, inclusive threshold and stable reverse sorting agree. Broad-type versus invalid-option precedence ambiguous; no new hold. |
| 193 | 0212 | Hold: six identical 0.1 scores fall below inclusive 0.1 cutoff due to accumulation rounding. Ordinary record copy and within-record alias preservation agree. |
| 194 | 0213 | Exact target construction, command identity, duplicate preservation and specified newline validation agree; no new hold. |
| 195 | 0215 | Greedy toggling/minimum result, empty inputs and oversized width cases agree. Quadratic runtime envelope pending; no new hold. |

Four pinned Python 3.11.15 probes, network disabled/resource limited, all exit
1 without timeout. Holds remain review items, not final rejection decisions.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0207 | humidex_negative_integer_probe.py / humidex-negative-integer-result.json | 464 | OverflowError instead of documented NaN for temperature below20. |
| 0209 | observation_integer_precision_probe.py / observation-integer-precision-result.json | 433 | Exact integer temperature rounded down by one. |
| 0205 | planner_unselected_sensor_probe.py / planner-unselected-sensor-result.json | 413 | Invalid sensor string accepted in unselected column. |
| 0212 | ratings_equal_boundary_probe.py / ratings-equal-boundary-result.json | 488 | Record incorrectly excluded at inclusive cutoff. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 196. Original candidates/tests/sample/partition unchanged.
