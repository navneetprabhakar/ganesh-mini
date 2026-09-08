# Rust elementary-target reconciliation — batch 15

2026-09-08. Initially unheld positions 421–450, selected only by the frozen
queue's `prior_hold is None`: ten proposed holds and twenty scoped positives.
Sixteen fresh complete repair inspections (prompt, known-bad, reference and
tests); generation0360 reread in full. Other generation decisions reconcile
the cited prior record-specific full inspections. No new code execution.

Gate 2 quality reconciliation only. Candidate corpus SHA-256 remains
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
This parallel-review note does not update the central hold ledger, certify all
seven criteria, seal training admission, or establish an executed failure.
Unresolved API and resource-envelope issues remain open as identified below.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 421 | exp-v1-rust-repair-0234 | Non-triviality hold: replace one explicitly specified Warning description literal; direct constructor and notice formatting remain unchanged. |
| 422 | exp-v1-rust-repair-0235 | Fresh full repair inspection: half-open campaign expiry gates checked per-account and aggregate contributions, with rejection preserving funded state. Criterion positive; no unrequested target cap imposed. |
| 423 | exp-v1-rust-repair-0236 | Fresh full repair inspection: distinguish empty equal endpoints from midnight-wrapping and ordinary half-open intervals, after validating all hours. Criterion positive, consistent with frozen generation0132 cyclic-interval disposition. |
| 424 | exp-v1-rust-generation-0355 | RUST_STRATUM_REVIEW_21.md documents length limits, incomplete-input nonconsumption, malformed headers and ordered flush. Criterion positive. |
| 425 | exp-v1-rust-generation-0356 | RUST_STRATUM_REVIEW_21.md documents demand-driven left-first memoized graph evaluation and checked arithmetic. Criterion positive; deep recursive stack envelope remains untested. |
| 426 | exp-v1-rust-generation-0357 | RUST_STRATUM_REVIEW_21.md documents request ordering/encoding, reply rejection and ordered notes. Criterion positive; None and literal hyphen coupon deliberately share the explicitly prescribed encoding, not a newly invented reference defect. |
| 427 | exp-v1-rust-generation-0358 | RUST_STRATUM_REVIEW_21.md documents ordered per-account import, expected nonces and saturating counters. Criterion positive; private exhaustion boundary not practically executed. |
| 428 | exp-v1-rust-generation-0360 | Non-triviality hold after full reread: empty-title guard followed by explicitly suggested Vec::retain over the direct enabled-and-title predicate and length subtraction. Library retention already supplies the specified ordering/no-match behavior; no interacting catalog state. |
| 429 | exp-v1-rust-repair-0238 | Fresh full repair inspection: inclusive weight boundary must prune descendants at the selected node while depth and leaf terminal rules preserve ordered traversal. Criterion positive; unrestricted deep-tree stack envelope remains untested. |
| 430 | exp-v1-rust-repair-0239 | Static contract/clarity hold: public new(u64::MAX), submit(MAX), then drain removes the message but cannot advance expected once as promised; reference leaves MAX and permits submitting that nonce again. No exhaustion/terminal policy is specified. No execution claimed. Core gap-before-advance repair is substantive but cannot resolve this boundary contract. |
| 431 | exp-v1-rust-repair-0240 | Non-triviality hold: remove explicitly unwanted plus-one from direct zero-filled allocation length; capped allocation guard, slice getters and clear wrapper unchanged. |
| 432 | exp-v1-rust-generation-0361 | RUST_STRATUM_REVIEW_21.md documents five-field cardinality, supported escapes, required nonempty fields and owned output. Criterion positive. |
| 433 | exp-v1-rust-generation-0365 | RUST_STRATUM_REVIEW_21.md documents revision-history and ID behavior. Criterion positive only for non-triviality; Revision field types and exact exhaustion boundary remain incompletely specified and not approved here. |
| 434 | exp-v1-rust-repair-0241 | Non-triviality hold: removal directly reuses the already supplied normalize helper, with an error-to-false branch and unchanged position/remove path; normalization and ordered insertion machinery are already correct. |
| 435 | exp-v1-rust-repair-0242 | Non-triviality hold: replace non-strict comparison with the explicitly specified strict scalar threshold; decimal/error-text wrapper unchanged. |
| 436 | exp-v1-rust-repair-0244 | Fresh full repair inspection: advancing the oldest slot after overwrite must preserve chronological ring order through wrap, capacity one and clear/reuse. Criterion positive; bounded N prevents index-addition overflow for constructible instances. |
| 437 | exp-v1-rust-generation-0367 | RUST_STRATUM_REVIEW_21.md documents required artifact records, uniform line endings and attributes. Criterion positive; embedded bare CR versus literal retention remains ambiguous, and trailing newline rejection is only the recorded original-test behavior. |
| 438 | exp-v1-rust-generation-0369 | RUST_STRATUM_REVIEW_21.md documents registry API, lowercase/digit path validation, event order and independent snapshots. Criterion positive. |
| 439 | exp-v1-rust-generation-0370 | RUST_STRATUM_REVIEW_21.md documents FIFO lane API, pre-enqueue nonmutation and owned event snapshots. Criterion positive. |
| 440 | exp-v1-rust-repair-0246 | Fresh full repair inspection: parse and validate all replacement fields before touching the target, preserving existing items allocation on any malformed input and owning successful text. Criterion positive; unsigned-u64 wording does not independently ban the standard parser's leading plus. |
| 441 | exp-v1-rust-repair-0247 | Non-triviality hold: apply the explicitly prescribed negation of the right vector for left movement; finite-distance guard and shared shift unchanged. No extra finite-result invariant is inferred from constructor validation or literal f32 arithmetic. |
| 442 | exp-v1-rust-repair-0248 | Non-triviality hold: remove the two first-occurrence guards to implement expressly stated last-wins assignment; line grammar, malformed-prefix rejection and owned output unchanged. Blank versus whitespace-only line wording remains unresolved. |
| 443 | exp-v1-rust-generation-0373 | RUST_STRATUM_REVIEW_22.md documents ASCII priorities, alternating masks, complete quartet validation and checked sums. Criterion positive. |
| 444 | exp-v1-rust-generation-0375 | RUST_STRATUM_REVIEW_22.md documents transactional candidate buffering, early oversized-header rejection and owned frames. Criterion positive. |
| 445 | exp-v1-rust-generation-0376 | RUST_STRATUM_REVIEW_22.md documents count-before-number precedence, ASCII digits and ordered trail-error mapping. Criterion positive. |
| 446 | exp-v1-rust-generation-0377 | RUST_STRATUM_REVIEW_22.md documents presence entry/reentry order, no-op counting and retained successful batch prefix on failure. Criterion positive. |
| 447 | exp-v1-rust-repair-0249 | Non-triviality hold: replace checked_add with the explicitly named checked_mul in opcode20 dispatch; instruction decoding, address/error validation, no-write failure and resume machinery unchanged. This is an operation-selection substitution, not a repaired instruction-state interaction. |
| 448 | exp-v1-rust-repair-0250 | Non-triviality hold: swap the two explicitly ordered Subtract arguments; source validation, cache reuse and append-position bookkeeping are unchanged. |
| 449 | exp-v1-rust-repair-0251 | Fresh full repair inspection: newly encountered source blobs must join global seen state, so duplicates collapse within and across groups while optional existing participation and stable first occurrence are retained. Criterion positive. |
| 450 | exp-v1-rust-repair-0252 | Fresh full repair inspection: final nonempty suffix must be consumed exactly once through UTF-8 validation and the transition machine, without applying LF-only CR stripping. Criterion positive; split records and issue ordering retained. |

Proposed hold IDs: repair0234, generation0360, repair0239, repair0240,
repair0241, repair0242, repair0247, repair0248, repair0249 and repair0250
(all under exp-v1-rust-). Nine non-triviality holds and one static contract/
clarity hold. Parent reconciliation must apply central counts and validate
contiguous coverage; this note deliberately makes no cumulative-count claim.
