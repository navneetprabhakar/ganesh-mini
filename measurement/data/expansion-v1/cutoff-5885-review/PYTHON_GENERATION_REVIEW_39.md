# Python generation review, batch 39

Positions 571–585 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; five reproduced holds.
684 additive plus historical three = 687 holds; 1,818 unique outside-sample
inspections. No seven-criterion approval. Continue position 586.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 571 | 0667 | Hold: sorts by alphanumeric count, not full label length. Original test expects a! before c and endorses incorrect ordering. Ordinary trimming, casefold stability and empty labels agree. |
| 572 | 0671 | Ordinary credit/debit arithmetic, sequential statements, metadata copies and read-only properties agree. Copy failure after balance mutation is outside explicit insufficient-debit atomicity guarantee; pending broader disposition, no new hold. |
| 573 | 0674 | Ordinary nearest-neighbor sampling and palette arithmetic agree. Sequence-versus-iterable acceptance, oversized integer errors and newline palette output contract pending; no new hold. |
| 574 | 0675 | Hold: wrong actor ID type raises ValueError instead of TypeError. Ordinary atomic coordinate movement, order and independent dictionaries agree. Original tests accept either exception. |
| 575 | 0676 | Ordinary weighted strict-rank dynamic program, modular arithmetic and zero-group handling agree. Sequence breadth pending; no new hold. |
| 576 | 0677 | Ordinary update validation, alias conflict and copied preferences agree. Existing timezone spelling canonicalization and arbitrary copy domains pending; no new hold. |
| 577 | 0678 | Hold: zero-length block between overlapping nonzero intervals prevents their merge. Ordinary sorting, touching rule and new objects agree. Writable invalid endpoints and general numeric breadth pending. |
| 578 | 0679 | Ordinary sorted projection, required nested fields, extras preservation and deep copies agree. Arbitrary copy-compatible metadata domains pending; no new hold. |
| 579 | 0681 | Ordinary directed reachability, cycles excluding origin, unique edges and ordered ties agree; no new hold. |
| 580 | 0682 | Ordinary single lookup, ID validation, word initials and detached metadata agree. Arbitrary copied metadata and mutable scalar-subclass accessors pending; no new hold. |
| 581 | 0683 | Hold: delimiter-only nonblank rows skipped as blank. Ordinary duplicate replacement, exact lookup and nonnegative fares agree. CSV quoting/line semantics and dictionary content exception wording versus tests pending. |
| 582 | 0684 | Bad-character mismatch skips, one-step success shifts for overlaps, empty needle and Unicode indexing agree; no new hold. |
| 583 | 0685 | Ordinary dataclass fields, account copies, profile allowlist and detached result dictionaries agree. Mixed-type unsupported keys and arbitrary payload failures pending; no new hold. |
| 584 | 0686 | Ordinary exact tab field counts, ASCII IDs, reply root filtering and duplicate order agree. Non-string argument and extended line-separator domains pending; no new hold. |
| 585 | 0687 | Hold: mutating extractor changes caller-owned frame. Ordinary skip/quit boundaries, repeated labels and per-result copies agree. Unknown unvisited actions and malformed action types pending. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch awaits backup;
last verified backup is through 682 holds / Python position 570.

Five pinned Python 3.11.15 probes, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0667 | normalize_route_punctuation_length_probe.py / normalize-route-punctuation-length-result.json | 431 | a!/c instead of c/a!. |
| 0675 | actor_id_type_probe.py / actor-id-type-result.json | 406 | ValueError for non-string ID. |
| 0678 | block_zero_length_barrier_probe.py / block-zero-length-barrier-result.json | 438 | (0,10) and (6,12) remain unmerged around (5,5). |
| 0683 | fare_delimiter_only_probe.py / fare-delimiter-only-result.json | 532 | Three delimiter-only malformed rows accepted. |
| 0687 | extractor_frame_mutation_probe.py / extractor-frame-mutation-result.json | 471 | Caller frame list mutated. |
