# Array-validation follow-up, batch 23

Positions 331–345: 15 new / 353 unique outside-sample inspections. Nine new
holds: **250 additive / 253 including historical three**. Full prompts,
references and original tests inspected; truncated board-test section reread.

| Position | Candidate | Finding |
| --- | --- | --- |
| 331 | TS generation0213 | Phase 2^-52 loses its representable pulse increment. pulse-small-positive-phase-result.json, 2018 ms. |
| 332 | TS repair0141 | Required entry code lost when non-enumerable. reading-shelf-required-code-result.json, 2390 ms. |
| 333 | TS repair0142 | Missing full-record tag accepted. decode-record-missing-tag-result.json, 2256 ms. |
| 334 | JS generation0257 | Missing concept accepted. concept-missing-record-result.json, 458 ms. |
| 335 | JS repair0169 | Promise.all resolves values in order, defers mapper throws into rejection; array-only copying allowed by explicit object-identity test. No new hold; missing-slot mapper semantics unspecified. |
| 336 | JS repair0171 | Missing order line accepted. order-missing-line-result.json, 340 ms. |
| 337 | TS generation0217 | Explicit required-field/label copies, Map key identity and code-unit ordering. Missing-label rejection is not specifically defined by blank-label policy; no new hold from this scoped inspection. |
| 338 | TS generation0219 | Explicit card copies and independently copied response bodies; authentication precedes request-field checks. Malformed state policy not specified. No new hold. |
| 339 | TS generation0220 | Internally generated dense signals with fixed enum color mapping; failed blank-text calls leave counter unchanged. No new hold. |
| 340 | TS generation0222 | Missing string-list member serialized as null. string-list-missing-member-result.json, 2088 ms. |
| 341 | TS repair0146 | Dense internal tuples, case-normalized replacement preserves position and latest spelling; fresh tuple outputs. No new hold. |
| 342 | TS repair0147 | Missing movement accepted. stock-missing-movement-result.json, 2830 ms. |
| 343 | TS repair0148 | Last operator/action selection, explicit field copies, key order from Object.keys per contract, mutation restricted to chosen action slot. No new hold. |
| 344 | JS generation0264 | Extra non-enumerable group field accepted despite only-stated-own-fields contract. member-hidden-extra-field-result.json, 850 ms. |
| 345 | JS repair0173 | Extra non-enumerable detail field accepted before changing state. preference-hidden-extra-field-result.json, 681 ms. |

All nine probes failed at runtime without timeout in pinned network-disabled,
resource-limited sandboxes; TS compilation passed. No duplicates added. Animation
reflection also deserves termination review (zero available span and extreme
overshoots), but no timeout was executed or claimed here. Numeric probe uses a
bounded, representable result and does not exercise that loop.

These remain scoped inspections, not seven-criterion approvals. Frozen sample,
partition and candidate data unchanged; no training seal. GCS verified through
244 holds / batch 22; batch 23 pending backup. Continue position 346.
