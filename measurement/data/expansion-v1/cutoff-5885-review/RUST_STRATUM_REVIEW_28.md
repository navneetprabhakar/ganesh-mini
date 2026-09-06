# Rust generation review, batch 28

Positions 406–420 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; one new sandbox-confirmed hold.
Total 969 unique outside-sample inspections; 448 additive plus historical three
= 451 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 406 | 0471 | Minimum-ID shelf lookup and atomic insertion agree. Combined duplicate/empty-name priority unstated; no new hold. |
| 407 | 0472 | Reverse traversal counts distinct other ancestors with self/cycle exclusion; validated edges and stable references agree. No new hold. |
| 408 | 0474 | Repeated writes increment, clear preserves count and checked exhaustion panics as requested. Private exhaustion not executed. No new hold. |
| 409 | 0469 | Ordered table store, exact family/qualifier and borrowed reads agree with original tests. Colon-containing configured family versus exactly-one-separator grammar remains an input-domain question; no new hold. |
| 410 | 0475 | Bracket/trim/last-value parsing agrees with tests. Empty semicolon fields are rejected though prompt only explicitly rejects nonempty separator-less fields; retained as ambiguity, not an invented acceptance oracle. No new hold. |
| 411 | 0476 | Physical-line diagnostics, first-colon split and last recognized values agree. No new hold; elementary scope pending. |
| 412 | 0477 | Exact three ASCII bytes and bounded digit sum agree. No new hold; elementary scope pending. |
| 413 | 0478 | Exact filters, strict ID cursor, stable time/ID ordering and duplicate retention agree. No new hold. |
| 414 | 0479 | i64 coordinate differences safely classify full i32 domain and enumerate valid strokes without arithmetic overflow. Extremely long accepted strokes have unbounded allocation/work; envelope pending, not executed. No new hold. |
| 415 | 0480 | Maximum revision, first-match clone and fixed peer metadata agree. No new hold; elementary scope pending. |
| 416 | 0481 | Widened area, strict unrotated containment and exact rendering agree. No new hold; elementary scope pending. |
| 417 | 0482 | Exact suffix error classifier agrees; never-success behavior is explicitly requested. No new hold; meaningfulness criterion pending. |
| 418 | 0483 | First ASCII-comma byte slice preserves original borrow; delimiter byte cannot split UTF-8. No new hold; elementary scope pending. |
| 419 | 0484 | Sixteen-channel prevalidation, persistent latch and single-channel clearing agree. No new hold. |
| 420 | 0485 | Sandbox hold: nested assignment mutates the outer target before a later evaluation error, violating target-preservation promise. |

0485: `nested_assignment_target_probe.rs` and
`nested-assignment-target-result.json` preserve compile 0 / test 101,
3,370 ms, no timeout in the pinned network-disabled/resource-limited sandbox.
Starting target=9, Assign(target, Add(Assign(target, Number(12)), Name(missing)))
returns the expected UnknownName error but leaves target=12 rather than 9.
The oracle tests only the explicit failed-assignment target guarantee; it does
not demand rollback of unrelated names. Original tests cover failed values
without nested target writes. The prompt's separate arithmetic nonmutation
promise also needs reconciliation with arbitrary nested Assign expressions.

Original tests/candidates unchanged. Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 421. No new VM or training seal.
