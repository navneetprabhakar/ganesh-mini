# Rust elementary-target reconciliation — batch 14

2026-09-08. Initially unheld391–420: nine holds and21 scoped positives.
Fourteen fresh complete repair prompt/known-bad/reference/test inspections;
generation0327 prompt/reference reread; other generation rows reconcile the
record-specific prior full inspections cited below. No new candidate execution.
Candidate corpus SHA256:
680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

This is Gate2 criterion-scoped review, not all-seven-criterion approval,
training admission or a release decision. Small patch size alone does not
determine non-triviality; ownership, ordering and numeric interactions are
assessed in the complete task. Unresolved other criteria remain open. The
original5885, central holds and cumulative state are not modified by this note.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 391 | exp-v1-rust-generation-0327 | Non-triviality hold: six fixed-format tuple fields plus directly prescribed first-three join and length guard; independent elementary formatting utilities without interacting state. Fresh prompt/reference reread confirms RUST_STRATUM_REVIEW_19.md elementary-scope concern. |
| 392 | exp-v1-rust-generation-0329 | RUST_STRATUM_REVIEW_19.md documents checked endpoints, alignment, sorted virtual nonoverlap, allowed physical overlap and half-open translation. Criterion positive. |
| 393 | exp-v1-rust-generation-0330 | RUST_STRATUM_REVIEW_19.md documents atomic invalid selection, stable page IDs and ordered round-trip restoration. Criterion positive. |
| 394 | exp-v1-rust-repair-0217 | Fresh full repair inspection: carry word-boundary state across empty and adjacent chunks, count Unicode whitespace boundaries and stop consumption at first input error. Criterion positive; impractical usize word-count exhaustion not newly adjudicated. |
| 395 | exp-v1-rust-repair-0218 | Fresh full repair inspection: failed transaction restores the same owned value so subsequent mutation/replacement remains usable without a Clone bound. Criterion positive. Panic recovery and arbitrary interior-mutable values are not newly certified by ordinary success/error tests. |
| 396 | exp-v1-rust-repair-0219 | Non-triviality hold: directly prescribed from_be_bytes to from_le_bytes substitution in an otherwise unchanged fixed-stride decoder; record alignment, offsets and unused measurement handling already implemented. |
| 397 | exp-v1-rust-repair-0220 | Fresh full repair inspection: newest insertion order must govern borrowed, channel-filtered, limited results independently of nonmonotonic or duplicate sequence numbers. Criterion positive; reversal placement relative to take is material. |
| 398 | exp-v1-rust-generation-0332 | RUST_STRATUM_REVIEW_19.md documents CRUD behavior and matching ordinary tests. Criterion positive; combined missing-ID/invalid-time replacement precedence remains ambiguous and unresolved. |
| 399 | exp-v1-rust-generation-0333 | RUST_STRATUM_REVIEW_19.md documents duplicate-before-existence precedence, successful attempts and distinct solved weights. Criterion positive; u32 identifier population and weights bound the sum within u64. |
| 400 | exp-v1-rust-generation-0334 | RUST_STRATUM_REVIEW_19.md documents lexical replacement, ordered filters, identifier validation and literal/null formatting. Criterion positive; no database execution or SQL-safety certification. |
| 401 | exp-v1-rust-generation-0335 | RUST_STRATUM_REVIEW_20.md documents significant whitespace, required fields and numeric bounds. Criterion positive; extra equals in kind remains a grammar ambiguity, not resolved by reference rejection. |
| 402 | exp-v1-rust-generation-0336 | RUST_STRATUM_REVIEW_20.md documents heap priority/FIFO, stale-generation exclusion and atomic checked sequence handling. Criterion positive; private exhaustion remains unexecuted. |
| 403 | exp-v1-rust-repair-0221 | Non-triviality hold: elementary single-slot Some/take/Empty ownership exercise with no interacting state beyond one redemption flag. Known-bad source attempts a move out of borrowed self and is a compile-error repair; behavioral-only mutant qualification remains unresolved. |
| 404 | exp-v1-rust-repair-0223 | Static numeric hold: valid chart object_count=u32::MAX and play misses=u32::MAX, passed_objects=None, combo=u32::MAX, accuracy1 cause misses as i32 to become -1. The implemented penalty is therefore 0.97^-1 instead of the specified 0.97^4294967295; with Tap rating1 other factors equal1. No allocation-heavy setup is needed, but no new execution is claimed. Cache identity repair itself is substantive; public invalid cache stars and extreme rating behavior remain unadjudicated. |
| 405 | exp-v1-rust-generation-0337 | RUST_STRATUM_REVIEW_20.md documents parser ranges and patch/default/disabled interactions. Criterion positive; whitespace, signed-positive grammar and malformed public patches remain unresolved. |
| 406 | exp-v1-rust-generation-0338 | RUST_STRATUM_REVIEW_20.md documents generic move/activate/leave transitions with owned listener and immutable reads. Criterion positive. |
| 407 | exp-v1-rust-generation-0340 | RUST_STRATUM_REVIEW_20.md documents option bits, conveyor transitions, fault gate, alarm and atomic errors. Criterion positive. |
| 408 | exp-v1-rust-generation-0341 | RUST_STRATUM_REVIEW_20.md documents checked revision before mutation, no-op at maximum and byte-length encoding. Criterion positive; malformed public ID/map states remain unresolved. |
| 409 | exp-v1-rust-repair-0225 | Non-triviality hold: directly specified inclusive comparison replaces strict comparison in elementary independent per-gene arithmetic; unsigned magnitude and prevalidation already correct. Meaning of changed count for zero scale/sample or rounding-to-same value remains unresolved, not newly claimed executed failure. |
| 410 | exp-v1-rust-repair-0226 | Non-triviality hold: replace contains with explicitly prescribed exact equality in already complete validated route parser; whole-document validation, first selection and ownership unchanged. |
| 411 | exp-v1-rust-repair-0227 | Non-triviality hold: replace height with width in explicitly named output field; complete parsing, duplicate policy, numeric validation and tag handling remain unchanged. |
| 412 | exp-v1-rust-repair-0228 | Non-triviality hold: replace bx with explicitly prescribed by in fixed squared-distance formula beside correct x expression. Pre-subtraction widening and generic blanket implementation already correct. Stateful Located implementations and self-identity behavior remain unadjudicated. |
| 413 | exp-v1-rust-repair-0229 | Fresh full repair inspection: byte-based span endpoints and character-boundary validation must coexist with per-line Unicode-scalar columns, including zero-width and multiline/end positions. Criterion positive; no added source-token matching requirement. |
| 414 | exp-v1-rust-repair-0230 | Fresh full repair inspection: missing cube axis requires retaining signed widened axial differences before combining them, then taking maximum magnitudes; this distinguishes same-sign from opposing deltas over full i32 domain. Criterion positive. |
| 415 | exp-v1-rust-repair-0231 | Fresh full repair inspection: borrow ready packet rather than consume state while appending exactly one transformed sink entry per call, preserving readiness across repeated flushes. Criterion positive; IEEE multiplication is explicitly ordinary, not a finiteness promise. |
| 416 | exp-v1-rust-generation-0350 | RUST_STRATUM_REVIEW_20.md documents generic one-time move, mixed FIFO signals, pending/end distinction and close-drain behavior. Criterion positive. |
| 417 | exp-v1-rust-generation-0351 | RUST_STRATUM_REVIEW_20.md documents wide derived coordinate, level-before-shift validation and six ordered offsets. Criterion positive. |
| 418 | exp-v1-rust-generation-0352 | RUST_STRATUM_REVIEW_21.md documents exact byte recipes, decoders, owned serialization and full-byte comparison. Criterion positive; integrity exercise is explicitly not cryptography. |
| 419 | exp-v1-rust-generation-0353 | RUST_STRATUM_REVIEW_21.md documents checked shapes, finite inputs/final accumulation, activations and row ordering. Criterion positive; intermediate exp infinity leading to finite logistic zero is not separately prohibited. |
| 420 | exp-v1-rust-repair-0233 | Non-triviality hold: change one explicitly listed source-field shift from29 to30 in a fixed mapping; masks, reserved-bit preservation and atomic validation already correct. |

Proposed holds: generation0327; repairs0219,0221,0223,0225,0226,0227,0228,0233.
All14 repair IDs are fresh outside-sample inspections. Parent integration must
validate this contiguous queue segment and combine counts with disjoint parallel
work before updating central holds or state. No backup completion is claimed.
