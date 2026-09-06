# Python generation review, batch 16

Positions 226–240 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; five reproduced holds.
584 additive plus historical three = 587 holds; 1,473 unique outside-sample
inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 226 | 0253 | Rotation, horizontal flip and separate deep-copied variants agree. Arbitrary noncopyable cells remain pending; no new hold. |
| 227 | 0254 | Inheritance, decorator identity, registry replacement, read-only mapping and serialization agree ordinarily; no new hold. |
| 228 | 0255 | Copy before one transmission, clear only on success, exception propagation and receipt identity agree. Adversarial copy hooks pending; no new hold. |
| 229 | 0256 | Full validation before zero limit, stable casefold ordering and dictionary order agree. Integer subclass domain pending; no new hold. |
| 230 | 0257 | Exact integer bucket offsets and differences agree; no new hold. |
| 231 | 0258 | Shrinking-remainder trial division and leftover prime agree with specified algorithm; no new hold. |
| 232 | 0261 | Resource copies, owner deduplication/order and sorted queries agree ordinarily. Post-construction name mutation outside explicit constructor validation remains pending; no new hold. |
| 233 | 0264 | Shape validation, confusion counts, ratios and explicit zero denominators agree. Integer subclass semantics pending; no new hold. |
| 234 | 0262 | CRUD key validation, copies and atomic updates agree ordinarily. Mutable string subclass inputs and broad original exception assertions pending; no new hold. |
| 235 | 0265 | Hold: finite gradient 1e200 overflows before clipping, although required clipped result is representable. |
| 236 | 0266 | Hold: valid huge integer horizon overflows in linear mode at position zero, whose result is exactly 1.0. |
| 237 | 0267 | Hold: valid price with 5000 leading zeroes rejected by runtime decimal conversion limit. Empty-string versus whitespace-only contract remains ambiguous, not separately held. |
| 238 | 0270 | Ordinary newline block parsing, normalized duplicate identity, retained spelling/order and fresh containers agree. Non-LF line-separator domain remains pending; no new hold. |
| 239 | 0272 | Hold: tuple(successors) copies the entire list, violating explicit constant auxiliary space. Floyd traversal and full reference validation otherwise agree. |
| 240 | 0274 | Hold: finite distance squaring overflows; repeated identical 1e308 points produce infinite mean instead of 1e308. Ordinary initialization/order/copy contract agrees. |

Five pinned Python 3.11.15 probe runs, network disabled/resource limited, all
exit 1 without timeout. Holds remain review items, not final rejection decisions.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0265 | weighted_round_large_gradient_probe.py / weighted-round-large-gradient-result.json | 628 | OverflowError before clipping. |
| 0266 | attenuation_large_horizon_probe.py / attenuation-large-horizon-result.json | 614 | Integer-to-float OverflowError. |
| 0267 | inventory_leading_zero_probe.py / inventory-leading-zero-result.json | 648 | Valid integer text rejected at 4300-digit runtime limit. |
| 0272 | loop_auxiliary_space_probe.py / loop-auxiliary-space-result.json | 1159 | 1,600,502 traced bytes for 200000-element input allocated before tracing, corroborating linear-space tuple copy. |
| 0274 | centroid_large_finite_probe.py / centroid-large-finite-result.json | 578 | OverflowError and infinite mean, both assertions executed. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 241. Original candidates/tests/sample/partition unchanged.
