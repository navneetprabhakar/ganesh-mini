# Rust generation review, batch 40

Positions 586–600 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; one sandbox-confirmed hold.
Total 1,149 unique outside-sample inspections; 470 additive plus historical
three = 473 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 586 | 0691 | Catalog-first validation, repeated details and last conclusion agree. Explicit empty-component rule qualifies general no-leading/trailing-newline wording; no new hold. |
| 587 | 0692 | Verbatim destination operands, terminator and help/revision syntax validation agree. No new hold. |
| 588 | 0693 | Widened inclusive union and distinct occupied subtraction agree; conversion occurs after subtraction. Off-row endpoint validation scope remains pending; no new hold. |
| 589 | 0694 | Front-to-back follower updates agree. Gap subtraction is bounded by the maintained adjacency invariant, not arbitrary i64 subtraction. Large chain/step resource envelope pending; no new hold. |
| 590 | 0695 | Unicode scalar buckets, bounce endpoints and excessive-row early return agree. No new hold. |
| 591 | 0696 | Alias/target validation, borrowing and recency agree. Private maximum-sequence early exhaustion remains unexecuted; no new hold. |
| 592 | 0698 | Monotonic sliding-window left bound and expected-linear hash lookup agree. No new hold. |
| 593 | 0700 | Ordinary bounded retention, independent cursors and exact lag count agree. Cross-hub subscriptions and private sequence exhaustion remain unspecified/unexecuted; no new hold. |
| 594 | 0701 | Owned checked meter update and exact suffix append agree. No new hold. |
| 595 | 0697 | Trimmed fields/tags and token alphabet agree. Original test requires WrongFieldCount for three-field input id,on:off,tag; this special error mapping is unstated and remains pending. No new hold. |
| 596 | 0703 | ASCII lowercase, sorted learned vocabulary and current-order first match agree. No new hold. |
| 597 | 0704 | Sandbox hold: one single-pixel tile with usize::MAX columns panics on capacity overflow instead of returning Overflow. |
| 598 | 0706 | Exact markers, list lengths, memo little endian and signed zigzag agree. Modulo collisions are requested behavior, not a cryptographic transcript guarantee. No new hold. |
| 599 | 0707 | Existing-duplicate preservation, encounter-order dedup and batch-only counters agree. No new hold. |
| 600 | 0708 | Checked ends, half-open containment, floor center and odd bisection agree. Size errors precede coordinate validation during scaling; no new hold. |

0704: atlas_capacity_overflow_probe.rs supplies one 1x1 tile with one byte
and usize::MAX columns. Size products fit usize, but Vec cannot represent
that allocation and panics with "capacity overflow". Prompt requires checked
arithmetic to report Overflow rather than panicking. The pinned Rust 1.85.0
network-disabled bounded sandbox records compile 0, test 101, 1,690 ms,
no timeout. See atlas-capacity-overflow-result.json. This is not an attempted
unbounded host allocation; generated code ran only inside the sandbox.

Original tests/candidates unchanged. Frozen candidate SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 601. No new VM or training seal.
