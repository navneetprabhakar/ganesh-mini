# Python repair review, batch 2

Positions 16–30 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Five new
additive holds: 743 additive plus historical three = 746; 1,947 unique
outside-sample inspections. Holds are review items, not final rejections.
Source inspection supports the stated repairs on ordinary inputs. Original
tests were read, not newly rerun in isolated probes. Seven-criterion quality,
nontriviality and known-bad execution certification remain pending.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 16 | 0020 | Inclusive comparison repairs equal-adjacent boundary. Filtering preserves order/duplicates and fresh output. Scalar subclass domains pending; no new hold. |
| 17 | 0021 | Length check repairs silent cyclic partial schedule. Contract hold: batched ready selection can put a later ready stage before an earlier newly ready stage. |
| 18 | 0022 | Subtracting one repairs mirrored index. Empty/single and ordinary value comparisons agree; custom equality/inequality domains pending, no new hold. |
| 19 | 0023 | Presence guard repairs earliest-source priority. Original value identity is explicitly required and preserved; no new hold. |
| 20 | 0024 | Strict comparison repairs fatal boundary at 1500. All ranges/type checks agree; no new hold. |
| 21 | 0025 | Zero initial total repairs double-counting and empty access. Ordinary arbitrary-size integer arithmetic and fresh list agree; no new hold. |
| 22 | 0026 | Zero base case repairs triangular recurrence. Hold: n=1100 raises RecursionError. Prompt requires recursion but gives no domain bound; disposition pending. |
| 23 | 0027 | Output-width loop repairs rectangular projection. Hold: tuple in first weight-row position raises ValueError rather than TypeError. Broader numeric domains pending. |
| 24 | 0029 | Value equality repairs channel selection. Ordinary validation-before-callback and separate payload copies agree. Hold: finite 600-level payload raises RecursionError. Arbitrary callback/copy effects pending. |
| 25 | 0030 | Orthogonal flood steps repair diagonal connectivity. Boundary detection, region ordering and detached output agree. Integer subclass breadth pending; no new hold. |
| 26 | 0031 | Exact-int check repairs boolean acceptance. Ordinary positive-multiple selection, duplicate/schema checks and order agree. This also narrows integer subclasses; contract breadth pending, no new hold. |
| 27 | 0032 | Direct Decimal parsing repairs binary-float conversion. Hold: mixed exponent span loses tiny term; malformed text changes caller context flags. |
| 28 | 0033 | Correct factor ratio repairs conversion direction. Exact Fraction arithmetic, signed/zero values and unit checks agree; no new hold. |
| 29 | 0034 | Exact length comparison repairs trailing-data acceptance. XOR, header, length and ordinary bytes roundtrip agree. Impractical >4 GiB allocation not executed; no new hold. |
| 30 | 0035 | Reverse stride accumulation repairs row-major layout. Scalar shape, arbitrary integer arithmetic and validation agree. Empty-tuple singleton wording is not treated as harmful aliasing; no new hold. |

Five pinned Python 3.11.15 network-disabled/resource-limited probes; all exit 1,
no timeout. Candidate SHA-256 remains
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/frozen sample and historical partition unchanged.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0021 | repair_schedule_ready_order / repair-schedule-ready-order | 404 | base,last,first rather than base,first,last |
| 0026 | repair_triangular_depth / repair-triangular-depth | 704 | bounded RecursionError diagnostic |
| 0027 | repair_project_first_row_type / repair-project-first-row-type | 723 | ValueError rather than TypeError |
| 0029 | repair_dispatch_depth / repair-dispatch-depth | 653 | bounded RecursionError diagnostic |
| 0032 | repair_decimal_precision_context / repair-decimal-precision-context | 452 | two assertions fail: exactness and caller flags |

Probe filenames append `_probe.py`; results append `-result.json`.
Batches 1–2 backed up in QUALITY_STRATUM_746_BACKUP.md. Continue position 31.
