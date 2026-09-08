# Rust elementary-target reconciliation — batch 18

2026-09-08. Frozen initially-unheld positions 511–540: sixteen proposed holds,
fourteen scoped positives. Fourteen fresh complete repair inspections include
prompt, known-bad source, reference and tests. Generation0429/0431/0440/0444/
0446 prompt/reference rereads resolve elementary-scope questions; other
generation records reconcile the cited previous full inspections.

Gate 2 only. No execution, central ledger change or training admission.
Original candidate SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scoped positives do not resolve every other criterion or admit training rows.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 511 | exp-v1-rust-generation-0428 | RUST_STRATUM_REVIEW_25.md documents state-reducer validation before mutation and flag/screen transitions. Criterion positive. |
| 512 | exp-v1-rust-generation-0429 | Fresh prompt/reference reread: arbitrary non-power-of-two alignment and already-aligned maximum values require remainder-based rounding without premature overflow; zero alignment has separate precedence. Criterion positive. |
| 513 | exp-v1-rust-generation-0430 | RUST_STRATUM_REVIEW_25.md documents trimmed uniqueness, checked IDs and exact permits/documents. Criterion positive; malformed public registry state and combined error precedence remain unresolved. |
| 514 | exp-v1-rust-generation-0431 | Fresh prompt/reference reread: two optional minima preserve distinctness through duplicates and replacement of the smallest value, with no sentinel collision across full i64 range and no sorting/allocation. Criterion positive. |
| 515 | exp-v1-rust-generation-0432 | RUST_STRATUM_REVIEW_25.md documents grouped textual-digit keys, alphabetic filtering and original tie-break. Criterion positive; per-character versus contextual whole-string Unicode lowercase remains an unresolved contract question. |
| 516 | exp-v1-rust-repair-0285 | Non-triviality hold: substitute the explicitly supplied canonical coordinate formula by swapping the two stride operands; compact/dense transitions and bounds checks unchanged. Behavior for publicly supplied malformed Dense lengths remains unresolved, not an executed failure. |
| 517 | exp-v1-rust-repair-0286 | Non-triviality hold: swap two explicitly ordered proof-format fields; owner validation and directory mutation machinery unchanged. Initial nonzero next_id is explicitly an expected valid-state precondition, so no zero-ID defect is invented here. |
| 518 | exp-v1-rust-repair-0287 | Non-triviality hold: substitute is_ascii_hexdigit for is_ascii_digit in the named hexadecimal validator; field validation order and atomic update unchanged. |
| 519 | exp-v1-rust-repair-0288 | Static API/contract hold: public ScopeStack with empty frames and next_token0 returns token0 from open despite promised nonzero tokens; no constructor or explicit nonzero initial-state precondition excludes this value. Escape's once-per-top-frame repair is substantive but cannot repair the ID contract. Generic owned value preservation on failure also remains unresolved; no execution claimed. |
| 520 | exp-v1-rust-repair-0289 | Non-triviality hold: replace ANSI color31 with explicitly required33; classification, cloned sorting and numeric formatting unchanged. |
| 521 | exp-v1-rust-repair-0290 | Non-triviality hold: direct two-case platform separator literal dispatch; fixed command sequence and URL/argument formatting unchanged. Prefix-internal separator normalization is not newly specified by this review. |
| 522 | exp-v1-rust-repair-0291 | Non-triviality hold: replace unwrap_or(true) with explicitly required false for the direct optional-Boolean conversion; field copying and reverse conversion unchanged. |
| 523 | exp-v1-rust-repair-0292 | Non-triviality hold: delete explicitly forbidden ampersand from the direct percent-encoding allowlist; UTF-8 byte encoding, validation and fixed mail construction unchanged. Literal base-URL recipe does not authorize adding a different query-join rule. |
| 524 | exp-v1-rust-generation-0439 | RUST_STRATUM_REVIEW_26.md documents nonfinite-input rejection and horizontal sliding. Criterion positive; pitch convention and finite-arithmetic overflow policy remain incompletely stated, with no invented finite-output requirement. |
| 525 | exp-v1-rust-generation-0440 | Non-triviality hold after reread: fixed three-word count, direct alphabetic validation and library uppercase expansion of each first scalar. Unicode support alone does not add an algorithm or interacting state beyond these independent wrappers. |
| 526 | exp-v1-rust-generation-0442 | RUST_STRATUM_REVIEW_26.md documents three-token parsing and checked signed operations. Criterion positive; combined parse/operator error precedence remains unresolved. |
| 527 | exp-v1-rust-generation-0444 | Non-triviality hold after reread: six fixed i32 values widened and summed followed by direct enum multiplier selection and multiplication; inert flags/aliases do not add interaction. Wider types correctly preserve the stated exact intermediate sum. |
| 528 | exp-v1-rust-repair-0293 | Fresh full repair inspection: exact match must still override prefixes while nonexact selection distinguishes zero, one and multiple matches independently of map ordering and returns the original borrowed object. Criterion positive. |
| 529 | exp-v1-rust-repair-0294 | Non-triviality hold: swap Node/Link result variants in the final parity predicate; graph construction, cycle detection and parity propagation unchanged. |
| 530 | exp-v1-rust-repair-0296 | Non-triviality hold: change bias shift16 to the explicitly designated8, already shown in getter and write_fields; reserved-mask handling and sequential setter machinery unchanged. |
| 531 | exp-v1-rust-generation-0445 | RUST_STRATUM_REVIEW_26.md documents required recursive pop/sort/reinsert with stability and insertion after equals. Criterion positive; large recursion envelope remains unresolved. |
| 532 | exp-v1-rust-generation-0446 | Non-triviality hold after reread: two exact append-format branches and one no-op implementation; trait boilerplate does not introduce interacting state. |
| 533 | exp-v1-rust-generation-0448 | RUST_STRATUM_REVIEW_26.md documents interning and catalog-wide fresh IDs. Criterion positive; private u64 exhaustion remains unexecuted, not a demonstrated reachable defect. |
| 534 | exp-v1-rust-repair-0298 | Non-triviality hold: correct the two explicitly named route/style assignment targets in otherwise unchanged six-key parser. Terminal-newline/CRLF interpretation is not newly adjudicated. |
| 535 | exp-v1-rust-repair-0299 | Non-triviality hold: replace word-count parity with already computed digit-sum parity; ASCII validation and fixed name rendering unchanged. No impractical sum-overflow execution claimed. |
| 536 | exp-v1-rust-repair-0300 | Non-triviality hold: direct checked_sub/error-before-assignment wrapper, mirroring adjacent checked_add; a single scalar counter has no multi-field transaction or other interacting state. |
| 537 | exp-v1-rust-generation-0451 | RUST_STRATUM_REVIEW_26.md documents stipulated saturating multiplication-before-division and ordered projection. Criterion positive; unstated final subtraction saturation remains unresolved rather than assigned an invented oracle. |
| 538 | exp-v1-rust-generation-0452 | RUST_STRATUM_REVIEW_26.md documents ordered prefix lookup and canonical u64 LEB128 termination, overflow and minimality. Criterion positive. |
| 539 | exp-v1-rust-generation-0453 | RUST_STRATUM_REVIEW_26.md documents bounded runs, repeated XOR, exact FNV tag and single suffix removal. Criterion positive; stipulated codec is not authenticated encryption or a security certification. |
| 540 | exp-v1-rust-generation-0454 | RUST_STRATUM_REVIEW_27.md documents authentication-before-availability, exact key lookup and cloned JSON-labelled reply. Criterion positive. |

Proposed holds: generation0440/0444/0446 and
repair0285/0286/0287/0288/0289/0290/0291/0292/0294/0296/0298/0299/0300.
All use exp-v1-rust- prefix. Fifteen non-triviality holds and one static
API/contract hold. Parent must reconcile central counts; no cumulative
coverage or backup claim is made by this parallel note.
