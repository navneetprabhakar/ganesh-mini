# Python generation review, batch 21

Positions 301–315 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; four reproduced holds.
602 additive plus historical three = 605 holds; 1,548 unique outside-sample
inspections. No seven-criterion approval. Continue position 316.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 301 | 0343 | Rectangular affine map, entry-parameter input gradients, validation before updates and independent rows agree ordinarily. Extreme arithmetic and mutable scalar subclasses remain pending; no new hold. |
| 302 | 0344 | Bounded cycle/slot validation, once materialization, deduplication and sorted formatting agree; no new hold. |
| 303 | 0345 | Hold: constant finite sample produces infinite mean. Later variance/z-score assertions were not reached. |
| 304 | 0347 | Mapping validation, token uniqueness, first-delimiter split and independent channel lists agree ordinarily. Duck-typed mappings and separator-containing tokens remain pending; no new hold. |
| 305 | 0349 | Hold: 600 nested lists form a valid acyclic catalog but raise RecursionError. Ordinary cycle detection and shared-node per-occurrence counting agree. |
| 306 | 0350 | Token ordering, owner idempotence, release/reacquire order and snapshot copies agree. Mutable string subclasses remain pending; no new hold. |
| 307 | 0351 | Exact global integer addition and validation before mutation agree; no new hold. Triviality/diversity review remains pending. |
| 308 | 0352 | Exact bounds, in-range counts, early stop before later malformed elements and once iteration agree; no new hold. |
| 309 | 0354 | Hold: deepcopy preserves a shared observed record alias, so the second digest replacement overwrites the first. First-digest assertion fails; later assertion not reached. |
| 310 | 0353 | Ordinary line JSON, defaults, ordering and recognized duplicates agree. Literal Unicode line separators and nonstandard JSON constants remain pending; no new hold. |
| 311 | 0355 | Four-byte descriptors, byte copies, once batch materialization and duplicate positions agree ordinarily. Name/mapping/buffer domain breadth remains pending; no new hold. |
| 312 | 0356 | Once probes, boolean conversion, reader-builder-signer ordering, exact prints and exception propagation agree ordinarily. Dynamic bound-method changes remain pending; no new hold. |
| 313 | 0357 | Dataclass fields, placeholder replacement, falsey option retention, mapping/default copies and independent samples agree ordinarily. Arbitrary copy and scalar-subclass domains remain pending; no new hold. |
| 314 | 0359 | Row/column order, empty rows, complete validation and immutable bytes agree. Integer subclasses remain pending; no new hold. |
| 315 | 0358 | Hold: length excludes underscores, accepting 21 underscores despite total length bound 20. Ordinary hashing, salt copying and comparison agree. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up
under QUALITY_STRATUM_609_BACKUP.md, through Python position 330.

Four pinned Python 3.11.15 probe runs, network disabled/resource limited, all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0345 | samples_large_constant_probe.py / samples-large-constant-result.json | 496 | Mean is inf instead of 1e308. |
| 0349 | payload_deep_acyclic_probe.py / payload-deep-acyclic-result.json | 664 | RecursionError for an acyclic input. |
| 0354 | reconcile_shared_record_probe.py / reconcile-shared-record-result.json | 428 | First digest becomes the second expected digest. |
| 0358 | credential_underscore_length_probe.py / credential-underscore-length-result.json | 466 | Overlength underscore-only handle accepted. |
