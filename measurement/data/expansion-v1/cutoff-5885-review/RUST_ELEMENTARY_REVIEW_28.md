# Rust elementary-target reconciliation — batch 28

2026-09-08. Frozen initially-unheld positions 811–843 (intentional33-row batch):
ten proposed holds, twenty-three scoped positives. Thirteen fresh complete
repair reads include prompt, known-bad source, reference and tests. Generation
0685/0701/0703 prompt/reference rereads supplement per-ID reconciliation with
the prior full inspections cited below.

Gate 2 only; no execution, admission or central-state changes. Scoped positives
do not resolve all seven criteria. Frozen candidate SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 811 | exp-v1-rust-generation-0681 | RUST_STRATUM_REVIEW_39.md documents owned inclusive-range replies, exact MIME and sorted paths. Criterion positive; insertion-only validation does not imply a new invalid-fetch-path error. |
| 812 | exp-v1-rust-generation-0682 | RUST_STRATUM_REVIEW_39.md documents start-of-call flag guard, bounded navigation and SeqCst resume. Criterion positive. |
| 813 | exp-v1-rust-generation-0684 | RUST_STRATUM_REVIEW_39.md documents composite-key replacement, append-only parcels and owned sorted filtered replies. Criterion positive. |
| 814 | exp-v1-rust-repair-0453 | Non-triviality hold: swap the named left/right operands in subtraction, matching adjacent division and remainder; postfix stack and checked evaluation machinery unchanged. |
| 815 | exp-v1-rust-repair-0454 | Non-triviality hold: remove the explicitly forbidden missing-key insertion branch and return false; existing-key partial updates, cloning and sorted storage unchanged. |
| 816 | exp-v1-rust-repair-0455 | Non-triviality hold: remove negation of the explicitly active-high green argument; output ordering, repeated writes and color recording unchanged. Generic ownership does not certify external hardware alias exclusion. |
| 817 | exp-v1-rust-generation-0685 | Fresh reread and RUST_STRATUM_REVIEW_39.md: empty-ID validation precedes decisions, terminal decisions bypass lookup, undecided chooses first exact client and owns ordered scopes. Criterion positive for branch/error interaction. |
| 818 | exp-v1-rust-generation-0688 | RUST_STRATUM_REVIEW_39.md documents overflow-safe ceiling division and index-before-count validation. Criterion positive; valid index makes multiplication overflow unreachable. |
| 819 | exp-v1-rust-generation-0689 | RUST_STRATUM_REVIEW_39.md documents byte-count LRU, replacement discount, owned copies and zero-byte entries. Criterion positive. |
| 820 | exp-v1-rust-generation-0690 | RUST_STRATUM_REVIEW_39.md documents half-open intervals, cancellation reuse and ordered copies. Criterion positive; private saturating ID exhaustion remains unspecified/unexecuted. |
| 821 | exp-v1-rust-repair-0457 | Non-triviality hold: replace toggle with the directly named bit-clear operation; reserved-field update and other active-bit helpers unchanged. |
| 822 | exp-v1-rust-repair-0459 | Fresh full repair read: stop consuming unmatched responses/broadcasts while finding and removing the earliest exact response, preserving their relative order and failed-query nonmutation. Criterion positive. |
| 823 | exp-v1-rust-repair-0460 | Fresh full repair read: initialize intersection from each group's first person in both terminated and unterminated-line paths, distinguishing an empty intersection from no people. Criterion positive; large u32 total/person-count envelope remains unexecuted. |
| 824 | exp-v1-rust-generation-0691 | RUST_STRATUM_REVIEW_40.md documents catalog-first validation, repeated details and last conclusion. Criterion positive; explicit empty-component rule qualifies general newline wording. |
| 825 | exp-v1-rust-generation-0692 | RUST_STRATUM_REVIEW_40.md documents verbatim destination operands, terminator and help/revision syntax validation. Criterion positive. |
| 826 | exp-v1-rust-generation-0693 | RUST_STRATUM_REVIEW_40.md documents widened inclusive union and distinct occupied subtraction before conversion. Criterion positive; off-row endpoint validation scope remains unresolved. |
| 827 | exp-v1-rust-generation-0694 | RUST_STRATUM_REVIEW_40.md documents front-to-back follower updates with adjacency-bounded subtraction. Criterion positive; large chain/step resource envelope remains unresolved. |
| 828 | exp-v1-rust-generation-0695 | RUST_STRATUM_REVIEW_40.md documents Unicode scalar buckets, bounce endpoints and excessive-row early return. Criterion positive. |
| 829 | exp-v1-rust-generation-0696 | RUST_STRATUM_REVIEW_40.md documents alias/target validation, borrowing and recency. Criterion positive; private maximum-sequence early exhaustion remains unexecuted. |
| 830 | exp-v1-rust-repair-0461 | Non-triviality hold: clamp right movement to width-1 instead of width, directly matching downward movement's existing bound; optional cursor, saturation, save/restore and writing machinery unchanged. |
| 831 | exp-v1-rust-repair-0462 | Non-triviality hold: change the high-end filter to inclusive; bounded digit generation, sorting and negative-bound handling unchanged. |
| 832 | exp-v1-rust-repair-0463 | Fresh full repair read: save previous presence/value, evaluate temporary nested scope, restore on success or error while evaluating initializer before binding. Criterion positive for scoped rollback and shadowing. |
| 833 | exp-v1-rust-repair-0464 | Non-triviality hold: replace explicit maximum level101 with100; discovery validation and shared-ID lookup unchanged. Foreign handles with an identical local ID and the phrase belongs to the hub remain an unresolved identity-contract question. |
| 834 | exp-v1-rust-generation-0698 | RUST_STRATUM_REVIEW_40.md documents monotonic sliding-window left bound and expected-linear lookup. Criterion positive. |
| 835 | exp-v1-rust-generation-0700 | RUST_STRATUM_REVIEW_40.md documents bounded retention, independent cursors and exact lag. Criterion positive; cross-hub subscriptions and private exhaustion remain unspecified/unexecuted. |
| 836 | exp-v1-rust-generation-0701 | Non-triviality hold after reread: independent checked-add/update wrapper and exact String suffix append; consuming ownership does not add a multi-field transaction or interaction. |
| 837 | exp-v1-rust-repair-0465 | Static arithmetic-order hold: contract computes matrix multiplication before adding bias, but reference seeds accumulation with bias. With rows1/inner2/cols1, left[MAX,1], right[1,1], bias[-1], product accumulation must overflow whereas reference returns MAX. Bounded static reasoning, not executed evidence. The target stride substitution itself leaves this discrepancy intact; allocation envelope also unexecuted. |
| 838 | exp-v1-rust-repair-0467 | Non-triviality hold: delete percent from the explicit allowlist; raw-byte hexadecimal encoding and ordering unchanged. |
| 839 | exp-v1-rust-repair-0468 | Fresh full repair read: remaining room depends on current offset within the page, interacting with end-of-memory wrap and chunk log order across repeated wraps. Criterion positive; giant read length/start arithmetic resource envelope remains unexecuted. |
| 840 | exp-v1-rust-generation-0703 | Fresh reread and RUST_STRATUM_REVIEW_40.md: learned sorted/deduplicated vocabulary is replaced on fit, but transform must follow current public ordering and first duplicate with unknown ID0. Criterion positive. |
| 841 | exp-v1-rust-generation-0706 | RUST_STRATUM_REVIEW_40.md documents markers, list lengths, little-endian memo and signed zigzag. Criterion positive; requested modulo collisions are not cryptographic security. |
| 842 | exp-v1-rust-generation-0707 | RUST_STRATUM_REVIEW_40.md documents preservation of existing duplicates, encounter-order batch dedup and batch-only counters. Criterion positive. |
| 843 | exp-v1-rust-generation-0708 | RUST_STRATUM_REVIEW_40.md documents checked ends, half-open containment, floor center and odd bisection. Criterion positive; scaling size errors precede coordinate validation. |

Proposed holds: generation0701 and
repair0453/0454/0455/0457/0461/0462/0464/0465/0467.
All use exp-v1-rust- prefix: nine non-triviality holds and one static
arithmetic-order hold. Parent reconciles central counts; no cumulative coverage
or backup assertion is made here.
