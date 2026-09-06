# Python generation review, batch 14

Positions 196–210 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; four reproduced holds.
571 additive plus historical three = 574 holds; 1,443 unique outside-sample
inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 196 | 0216 | Exact handler/payload identity, successful-call counting, snapshots and close/reopen agree. Reentrant close semantics pending; no new hold. |
| 197 | 0214 | Hold: valid decimal one with leading zeroes rejected; 400 nested parentheses hit RecursionError. Ordinary precedence, left associativity and division types agree. |
| 198 | 0217 | Iterative terminal traversal and new list containers agree. Original tests explicitly retain mutable leaf-value identity; do not impose deep-copy semantics absent clarification. |
| 199 | 0218 | FIFO links, item identity, final empty state and independent list container agree. Externally corrupted public link chains are unspecified; no new hold. |
| 200 | 0220 | Outcome identity, normal load/initialize stopping and document copies agree. General mapping deepcopy compatibility and non-boolean remember domain pending; no new hold. |
| 201 | 0221 | Exact workflow comparisons, active-is-True, stage order and narrow catches agree. Custom equality exceptions follow Python semantics; no new hold. |
| 202 | 0222 | Multi-pointer product enumeration suppresses duplicate values and supports composite factors; independent calls agree. Resource envelope pending; no new hold. |
| 203 | 0224 | Explicit ASCII boundary/lookaround regex and bounded nonzero coordinates agree; no new hold. |
| 204 | 0226 | Ordered path creation/overwrite and independent copies agree. Malformed outer iterable and custom copy semantics pending; no new hold. |
| 205 | 0227 | Hold: two equal finite large scores return zero confidence instead of 50. Ordinary exact tie selection and details copy agree. |
| 206 | 0228 | Hold: nested specs silently accepted for automatic/positional roots due to early continue. Normal named roots/order agree; conversion syntax validation pending. |
| 207 | 0230 | Required fields, platform dispatch and per-machine complete copies agree. Version inequality versus semantic outdated wording pending; no new hold. |
| 208 | 0231 | Stable LSD bucket passes, duplicates, zero/empty inputs and base validation agree. No prohibited comparison sort used; no new hold. |
| 209 | 0232 | Explicit ASCII digit search and direction/validation agree; no new hold. |
| 210 | 0233 | Hold: valid integer seed cannot format even one requested line beyond decimal conversion limit. Ordinary inclusive range and spacing agree. |

Five pinned Python 3.11.15 probe runs for four records, network disabled/resource
limited, all exit 1 without timeout. Initial formula traceback exceeded runtime
stderr capture length; original truncated capture is retained. A separate bounded
trace probe confirms RecursionError without replacing that evidence.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0214 | formula_depth_decimal_probe.py / formula-depth-decimal-result.json | 388 | Decimal conversion ValueError and nested-input error; stderr capture truncated. |
| 0214 | formula_depth_bounded_trace_probe.py / formula-depth-bounded-trace-result.json | 385 | Explicitly caught RecursionError at nesting400. |
| 0227 | classification_equal_large_scores_probe.py / classification-equal-large-scores-result.json | 406 | Confidence 0.0 instead of 50.0. |
| 0228 | template_positional_nested_probe.py / template-positional-nested-result.json | 409 | Both automatic and positional nested specs accepted. |
| 0233 | progression_decimal_limit_probe.py / progression-decimal-limit-result.json | 384 | ValueError formatting single valid integer line. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 211. Original candidates/tests/sample/partition unchanged.
