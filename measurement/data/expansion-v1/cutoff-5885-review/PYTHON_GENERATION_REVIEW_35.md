# Python generation review, batch 35

Positions 511–525 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; four reproduced holds.
664 additive plus historical three = 667 holds; 1,758 unique outside-sample
inspections. No seven-criterion approval. Continue position 526.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 511 | 0595 | Ordinary full eligible batches, input order, duplicate edges and cycle detection agree; no new hold. |
| 512 | 0598 | Hold: overriding one path changes another path sharing a default dictionary. Ordinary structure checks, required paths and input isolation agree. Dictionary keys nested inside non-dictionary payloads and cyclic structures pending. |
| 513 | 0600 | Ordinary quota arithmetic, validated self-transfer, deletion/recreation order, read-only remaining and fresh snapshots agree; no new hold. |
| 514 | 0601 | Hold: valid date 0001-01-01 silently dropped on pinned runtime by strftime roundtrip. Ordinary conversion, sorting and malformed-record filtering agree; numeric grammar breadth pending. |
| 515 | 0602 | Exact name grammar, actual-int replica validation, range and output text agree; no new hold. |
| 516 | 0603 | Ordinary finite float operand parsing, operators and signed-zero division agree. Decimal grammar breadth and finite mathematical numbers outside float range pending; no new hold. |
| 517 | 0604 | Hold: mean of two selected 1e308 values returns infinity. Ordinary shapes, mask validation, zero-width and empty selections agree; other large-integer breadth pending. |
| 518 | 0605 | Ordinary one-pass consumption, exact-int/range validation and in-memory WAV metadata/PCM agree. Format maximum size not separately certified; no new hold. |
| 519 | 0606 | Hold: finite 10**400 initial value raises OverflowError with empty signals. Ordinary retention updates, key order and separate list snapshots agree; numeric domain breadth pending. |
| 520 | 0608 | Ordinary integer deduplication, trimming and arithmetic mean agree. Nonrepresentable float output domain pending; no new hold. |
| 521 | 0611 | Ordinary defaults, explicit collection, document copies and intentional returned-entry/Vault identity agree. Arbitrary payload-copy and mutable scalar-subclass breadth pending; no new hold. |
| 522 | 0613 | Ordinary wavefront direction, rectangular bounds, validation and fresh flat list agree. Mutable scalar-subclass alias interpretation pending; no new hold. |
| 523 | 0614 | Ordinary imprint/title/code order, exact shape, uniqueness and nested details isolation agree. Arbitrary copy domains pending; no new hold. |
| 524 | 0616 | Ordinary class registration, lexical namespace order, aliases and duplicate-error propagation agree. Custom class equality/hash and non-string namespace keys pending; no new hold. |
| 525 | 0617 | Ordinary local/shared copies, instance separation and class replacement visibility agree. Arbitrary deepcopy-compatible values pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch awaits backup;
last verified backup is through 663 holds / Python position 510.

Four pinned Python 3.11.15 probes, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0598 | snapshot_shared_default_probe.py / snapshot-shared-default-result.json | 474 | Both paths changed instead of only the overridden one. |
| 0601 | telemetry_early_year_probe.py / telemetry-early-year-result.json | 552 | Valid early-year record omitted. |
| 0604 | masked_mean_overflow_probe.py / masked-mean-overflow-result.json | 522 | Infinity instead of representable 1e308 mean. |
| 0606 | blend_large_integer_probe.py / blend-large-integer-result.json | 426 | OverflowError during finiteness validation. |
