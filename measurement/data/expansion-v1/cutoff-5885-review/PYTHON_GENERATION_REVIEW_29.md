# Python generation review, batch 29

Positions 421–435 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; three reproduced holds.
639 additive plus historical three = 642 holds; 1,668 unique outside-sample
inspections. No seven-criterion approval. Continue position 436.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 421 | 0483 | Ordinary copy-on-put/read/take, overwrite order and discard/key validation agree. Arbitrary deepcopy domain and singleton empty-tuple identity wording pending; no new hold. |
| 422 | 0484 | Integer reserve/release bounds, atomic validation and independent snapshots agree. Unhashable section arguments and scalar-subclass domains pending; no new hold. |
| 423 | 0486 | Ordinary create/update/delete ordering, validation and nested copies agree. Custom copying and mutable scalar subclasses pending; no new hold. |
| 424 | 0487 | Field splitting, ordered rejection reasons and ordinary decimal/finite parsing agree. Large-decimal runtime limits and underscore grammar pending; no new hold. |
| 425 | 0488 | Exact isqrt-based ceiling and integer validation agree; no new hold. |
| 426 | 0489 | Monotonic tokens, logical durations, failed-finish preservation and returned copies agree. Simultaneous unknown-token/invalid-tick precedence pending; no new hold. |
| 427 | 0490 | Full validation, boundary ignores, revisits, score and board copy agree ordinarily. Scalar-subclass arithmetic domains pending; no new hold. |
| 428 | 0491 | Registration validation/replacement, handler rules and dispatch input/result copying agree ordinarily. Arbitrary deepcopy/callback side-effect domains pending; no new hold. |
| 429 | 0493 | Hold: representable finite straight speed overflows during addition, causing y to change from 5 to 0. Ordinary centrality/turn/clamping agree; general mapping and subnormal-area breadth pending. |
| 430 | 0495 | Ordered membership, exact credits, symmetric pair counts and validation-before-mutation agree. Scalar-subclass breadth pending; no new hold. |
| 431 | 0496 | Hold: missing field matches None filter. Ordinary names, fields, specialized queries and copies agree; general mapping-copy domains pending. |
| 432 | 0494 | Catalog membership/casefold, whitespace-normalized selection and fresh output tuple agree with original tests. Learner-code case normalization wording pending; no new hold. |
| 433 | 0497 | Full input validation, exact seed exclusion/deduplication and deterministic rating/casefold tie order agree. Consumed/shared iterable domains pending; no new hold. |
| 434 | 0498 | Hold: malformed non-ASCII MAC in string token raises TypeError instead of ValueError. Ordinary typed serialization, authentication and clearance agree; negative-clearance error contract and token grammar breadth pending. |
| 435 | 0499 | Complete tuple validation, duplicate order, exact True outcomes and ordinary per-probe copies agree. General pair iterables, BaseException and arbitrary deepcopy domains pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch awaits backup;
last verified backup is through 639 holds / Python position 420.

Three pinned Python 3.11.15 probe runs, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0493 | cart_straight_overflow_probe.py / cart-straight-overflow-result.json | 331 | y becomes 0 rather than remaining 5. |
| 0496 | catalog_missing_none_probe.py / catalog-missing-none-result.json | 307 | Both absent and explicit-None rows returned. |
| 0498 | sealed_nonascii_mac_probe.py / sealed-nonascii-mac-result.json | 363 | compare_digest TypeError escapes. |
