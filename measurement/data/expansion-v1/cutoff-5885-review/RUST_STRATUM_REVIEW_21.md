# Rust generation review, batch 21

Positions 301–315 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; two new holds. Total 864 unique
outside-sample inspections; 430 additive plus historical three = 433 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 301 | 0352 | Exact byte recipes, decoders, owned serialization and full-byte comparison loop. Integrity exercise explicitly not cryptography. No new hold. |
| 302 | 0353 | Checked shapes, finite inputs/final accumulation, specified activations and row ordering agree. Intermediate exp infinity can yield finite logistic zero; prompt only rejects accumulated/activated results, not each intermediate. No new hold. |
| 303 | 0354 | Static hold: str::lines requirement conflicts with unqualified carriage-return preservation. |
| 304 | 0355 | Length limits, incomplete input nonconsumption, malformed header and ordered flush agree. No new hold. |
| 305 | 0356 | Demand-driven left-first memoized graph evaluation and checked arithmetic agree. Deep recursive stack envelope remains untested. No new hold. |
| 306 | 0357 | Exact request ordering/encoding and reply rejection/ordered notes agree. None and literal hyphen coupon share encoding by explicit recipe; not held as a reference deviation. |
| 307 | 0358 | Ordered per-account imports, expected nonces and saturating counters agree. Private exhaustion boundary not practically executed. No new hold. |
| 308 | 0360 | Exact enabled/title predicate and Vec::retain preserve order/no-match allocation behavior. No new hold; elementary scope pending. |
| 309 | 0359 | Phase timing and affordable cost agree. Saturating damage multiplication width unspecified (reference widens to u64), and original boundary test cannot distinguish width because final addition saturates. Deferred ambiguity, no new hold. |
| 310 | 0361 | Exact five-field count, supported escapes, required nonempties and owned output agree. No new hold. |
| 311 | 0364 | Sandbox hold: subtree maximum masks underflow on another root-to-leaf path. |
| 312 | 0365 | Revision history/IDs and original tests agree; Revision field types and exact exhaustion boundary remain incompletely specified. No new concrete hold at this inspection. |
| 313 | 0367 | Exact artifact fields and required records, uniform line endings and attributes agree. Embedded bare CR versus literal retention ambiguous; trailing newline explicitly rejected by original tests. No new hold. |
| 314 | 0369 | Exact registry API, lowercase/digit path validation, event order and independent snapshots. No new hold. |
| 315 | 0370 | Exact FIFO lane API, pre-enqueue nonmutation and owned event snapshots. No new hold. |

0354 static comparison: prompt requires str::lines and also claims carriage
returns remain in line content. That is true for lone CR but not the CR in CRLF.
Reference uses lines; original test only covers a lone embedded CR. The two
requirements do not specify the same behavior for CRLF. No new execution claimed.

0364 diagnostic: `heaviest_route_hidden_overflow_probe.rs` and
`heaviest-route-hidden-overflow-result.json` bind the pinned network-disabled
Rust execution. Compile exit 0, test exit 101, 1,551 ms, no timeout. Edges are
0→1 weight -1, 1→2 weight i64::MIN, 1→3 weight 0. The first leaf's total
underflows; prompt requires None if any path overflows. Reference returns
Some(-1) because it discards the lower subtree value before adding -1.
Original overflow tests only use chains, not overflow on an unselected branch.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No-hold is not seven-criterion approval. Scope v6 and original evidence unchanged.
Continue position 316; no new VM, training seal or partition.
