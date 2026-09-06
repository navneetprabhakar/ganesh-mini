# Python generation review, batch 18

Positions 256–270 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; seven reproduced holds.
593 additive plus historical three = 596 holds; 1,503 unique outside-sample
inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 256 | 0293 | Hold: premature float conversion loses exact supplement of one between nearby integers. Shape and fresh-row handling agree ordinarily. |
| 257 | 0294 | Dataclass APIs, append/insert order, window and explicitly shallow independent text lists agree; no new hold. |
| 258 | 0289 | Hold: first positive weight underflows during normalization, so draw zero selects the later interval. Replay snapshots and ordinary controller behavior agree; model-side mutation of the snapshot remains pending. |
| 259 | 0295 | Range validation, atomic edits and independent history agree for ordinary strings/LF lines. Non-LF newline and mutable string subclass domain pending; no new hold. |
| 260 | 0296 | Hold: explicitly accepted arbitrary Python payload can be a function with mutable attributes; result mutation changes stored state because deepcopy retains the function. Ordinary data payload isolation agrees; copy-failure atomicity remains pending. |
| 261 | 0297 | Hold: repeated reference to one draft shipment is deep-copied with sharing intact and advanced twice, ending dispatch instead of queued. Queued zero-package rule is underspecified and separately pending. |
| 262 | 0298 | Casefold substring/fuzzy matching, exact filters and ranking/pagination agree ordinarily. Extreme integer ranks and broad copy domain pending; no new hold. |
| 263 | 0299 | Hold: undisclosed probability clipping changes post-epoch binary cross-entropy from 25 to 17.269388197455342. Ordinary batch-size gradients, ordering and snapshots agree. |
| 264 | 0300 | Marker presence, earliest associated version and digit/dot negative-lookahead agree with stated boundary, including suffix allowance; no new hold. |
| 265 | 0302 | Appended-object identity, existing entries and ordinary metadata deep copy agree. Arbitrary nested copy domain remains pending; no new hold. |
| 266 | 0303 | UTF-8 encoding, immutable binary copies, duplicate replacement order and names agree ordinarily. Surrogate text and general pair interpretation pending; no new hold. |
| 267 | 0304 | Hold: valid renderer integer fails at decimal formatting limit. Factorization agrees ordinarily; renderer only requires product equality, not prime/sorted factors. |
| 268 | 0305 | Hold: equal finite bounds yield infinite midpoint. Validation-before-finished, collaborator identity and state transitions agree ordinarily. |
| 269 | 0309 | Nodes, leaders, predecessors, immutable containers and explicitly required intra-block CFG edges agree. Custom opcode equality and mutable scalar subclasses pending; no new hold. |
| 270 | 0311 | Exact literal schema/order and fresh nested dictionaries agree. Complexity/diversity value of literal-output task remains pending; no new hold. |

Seven pinned Python 3.11.15 probe runs, network disabled/resource limited, all
exit 1 without timeout. Holds remain review items, not final rejection decisions.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0293 | cover_integer_difference_probe.py / cover-integer-difference-result.json | 808 | Supplement zero instead of one. |
| 0289 | distribution_zero_underflow_probe.py / distribution-zero-underflow-result.json | 815 | Index 1 instead of 0 at draw zero. |
| 0296 | inbox_function_payload_probe.py / inbox-function-payload-result.json | 743 | Returned function attribute mutation reaches storage. |
| 0297 | shipments_repeated_reference_probe.py / shipments-repeated-reference-result.json | 443 | Both occurrences advanced twice. |
| 0299 | trainer_unclipped_loss_probe.py / trainer-unclipped-loss-result.json | 405 | Bias -50 verified; clipped loss differs by 7.730611802544658. |
| 0304 | breakdown_decimal_render_probe.py / breakdown-decimal-render-result.json | 458 | Integer formatting ValueError. |
| 0305 | safety_finite_midpoint_probe.py / safety-finite-midpoint-result.json | 476 | Infinite midpoint for finite degenerate interval. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 271. Original candidates/tests/sample/partition unchanged.
