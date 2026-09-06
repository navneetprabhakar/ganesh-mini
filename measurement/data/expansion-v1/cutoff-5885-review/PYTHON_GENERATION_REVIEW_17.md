# Python generation review, batch 17

Positions 241–255 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; two reproduced holds.
586 additive plus historical three = 589 holds; 1,488 unique outside-sample
inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 241 | 0275 | Full tuple validation, HTML escaping including attributes, order and exact missing-member exception agree; no new hold. |
| 242 | 0277 | Hold: identical finite 1e308 values sum to infinity, producing zero outputs instead of 5e307 at shrink 1e308. |
| 243 | 0278 | Complete ID validation, lookup and ordered deep copy agree ordinarily. Arbitrary noncopyable nested values remain pending; no new hold. |
| 244 | 0279 | Atomic duplicate validation, callable identity, alias order and separate instances agree; no new hold. |
| 245 | 0280 | Fixed kind/index order, exact formatting and separate dictionaries agree. Enormous requested output bounds remain unspecified; no new hold. |
| 246 | 0281 | Exact keys, subset/uniqueness checks and occurrence-level independent field lists agree; no new hold. |
| 247 | 0282 | Exact route match, exception types and absence of mutable global state agree; no new hold. |
| 248 | 0283 | Round-robin allocation, port boundaries, required internal identity and independent host lists agree. Integer subclass domain pending; no new hold. |
| 249 | 0284 | General mapping normalization, reverse order and independent dictionary copies agree ordinarily. Adversarial custom copy hooks pending; no new hold. |
| 250 | 0285 | Argparse defaults/validation, exactly-once factory/run, return identity and process argv behavior agree. Extreme numeric-token domain remains pending; no new hold. |
| 251 | 0286 | Duty normalization, append after success and cleanup with active-exception preservation agree. Full prevalidation versus immediate stop for invalid later members remains an ambiguity; no new hold. |
| 252 | 0287 | Exact command bytes, sequence wrap and immutable frames agree. Full prevalidation versus stop precedence remains pending; no new hold. |
| 253 | 0288 | Six operations, stable sorting, exact keys and independent payload/current copies agree ordinarily. Integer subclass domain and within-collection shared tag lists remain pending; no new hold. |
| 254 | 0291 | Hold: valid version component with 5000 leading zeroes rejected by decimal conversion limit. Ordinary numeric boundary and captured profile agree. |
| 255 | 0292 | Frozen dataclass, exact integer product and zero-participant adequacy agree; no new hold. |

Two pinned Python 3.11.15 probe runs, network disabled/resource limited, both
exit 1 without timeout. Holds remain review items, not final rejection decisions.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0277 | rebalance_large_mean_probe.py / rebalance-large-mean-result.json | 378 | Zero outputs instead of 5e307. |
| 0291 | renderer_version_leading_zero_probe.py / renderer-version-leading-zero-result.json | 485 | Valid version rejected at 4300-digit runtime limit. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 256. Original candidates/tests/sample/partition unchanged.
