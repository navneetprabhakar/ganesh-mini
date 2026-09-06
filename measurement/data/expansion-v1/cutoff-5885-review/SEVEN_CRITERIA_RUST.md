# Rust frozen-sample criterion dispositions — 2026-09-07

All 62 frozen Rust sample records: 41 positive, 21 held (two existing, 19 new).
Initial full inspections are in FOURTH_BATCH_REVIEW.md; open cases were reread.
Candidate SHA: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
Criteria/patch-size policy follow SEVEN_CRITERIA_GO.md. Independent archived
test lineage and standard-library dependencies hold for all 62. This is not
training admission or release approval; holds remain reversible.

## Positive decisions (41)

Prefix: exp-v1-rust-.

| ID suffix | Basis / resolved concern |
| --- | --- |
| generation-0566 | Operand-order-preserving checked scalar/vector arithmetic and bracket grammar. Empty vector performs no element division; no scalar operation on absent elements is promised. |
| generation-0777 | Private nonzero invariant, const access and checked full-width doubling. Public free new plus self-taking methods resolves API placement. |
| generation-0028 | Exact simulation advance/observe sequencing and immediate stopping. |
| generation-0050 | Ordered overlay, precedence and detached rows. Explicit row joining governs zero-width rows; no extra terminal delimiter is appended. |
| generation-0065 | Shared Rc state and immediately ready delegation. ElementHandle is an abstract API sketch because the required state needs fields; unsafe no-op waker exists in tests, not reference. |
| generation-0083 | Permission precedence, audit values and sign-in/out state. |
| generation-0097 | Exact wrapping mixer schedule, endian conversion and hand-checked zero-round case. Educational formula, not cryptographic certification. |
| generation-0115 | ASCII-whitespace policy, bypass priority and checked big-endian bundle parsing. |
| generation-0132 | Wrapping versus nonwrapping half-open intervals, empty equality and validation priority without overflow. |
| generation-0171 | Complementary flag/reserved writes preserve the other state region, plus reset and raw visibility. |
| generation-0266 | One lock protects both indexes and reverse-index cleanup; no observed poison run claimed. |
| generation-0283 | Bit decoding, enum/control validation and exact rendering. |
| generation-0328 | Checked bounds and atomic overlapping writes, dirty state and saturation; private saturation limit reviewed statically. |
| generation-0513 | Wide intermediate products and bounded packed-output limits. |
| generation-0526 | Odd/even interleave, bounded rounds and atomic rejection. |
| generation-0587 | Bounded packet parsing, exact offsets and owned values. Unspecified semantic error variants are permissible choices; meaningful mutant is byte order, not an error-class choice. |
| generation-0600 | Bidirectional line counting and mutation-after-validation; no unrequested terminal-game lockout. |
| generation-0603 | FIFO, atomic paired configuration and watermark interrupt behavior; incremental allocation. |
| generation-0617 | Complete label validation, deterministic set order and saturated command count. Infeasible saturation boundary not claimed executed. |
| generation-0677 | Exact mapping, checksum byte order and retained duplicate response fields; no test-specific exception. |
| generation-0699 | Two-pass validation, Unicode cells and newline bounds. Impossible infallible-constructor allocations have no error-return promise. |
| generation-0779 | Exact modules, owned lookup and atomic nondecreasing-height state. |
| repair-0383 | Source-defined brace validation and literal substitution. No invented priority for multiple simultaneous errors. |
| repair-0458 | Checked address ranges and owned little-endian reads. Supplied bad source also has a type error; verifier mutant separately fixes that type issue to isolate boundary behavior. |
| repair-0098 | Final-run flush, 255 splitting and bounded decompression. |
| repair-0123 | Canonical field validation, inverse and identity arithmetic. No extra negate validation promise. |
| repair-0136 | Positioned nested expansion, absolute reset and exact expansion limit. |
| repair-0158 | Filter-before-window, borrowed stable results and atomic updates. |
| repair-0178 | Ordered accessor output and source-defined zero-ID rejection. |
| repair-0202 | Explicit emitter count independent of observers, shared drains and last-sender close. Fallible methods map poison; no public poison path established, and no private-state manipulation invented. |
| repair-0237 | Escape-state parser, four nonempty Unicode fields and trailing-escape rejection. |
| repair-0243 | Tie preserves borrowed self identity rather than merely an equal value; saturated adjustment. Small patch with an explicit identity boundary. |
| repair-0245 | Exact expiry and refreshed-token validation; constructor cache has a different expressly defined scope. |
| repair-0261 | First-delimiter split and stable selectors with sorted last-wins attributes. |
| repair-0295 | Cross-status movement, atomic validation and ordered lookup. |
| repair-0350 | Nondestructive owned reads and sorted borrowed keys. |
| repair-0385 | Strict attribute grammar, independent defaults and last recognized key. |
| repair-0389 | Final block flush, ordered atoms and exact line errors. |
| repair-0411 | Global uniqueness and referential integrity with distinct solved sum. Saturation reviewed statically. |
| repair-0032 | Streaming FIFO grouping and no eager usize::MAX allocation. |
| repair-0025 | Checked decimal accumulation across the full u64 boundary. |

## Held decisions (21)

| ID suffix | Blocking criterion / evidence |
| --- | --- |
| generation-0192 | Existing literal test-specific colon-validation exception. |
| generation-0630 | Existing executed overflow raised for an incomplete dead-end tour. |
| generation-0279 | Missing referenced signatures; API incomplete. |
| generation-0291 | Missing field types, error variants and accessor signatures. |
| generation-0345 | Missing method signatures and Kind variants. |
| generation-0466 | Missing Command variants/fields, and original tests inspect counts rather than command contents/order. |
| generation-0568 | Missing Event fields and trait result signatures. |
| generation-0702 | Unresolved collection-versus-element nonempty requirement for Blanks names. |
| generation-0160 | Unresolved attribute-separator grammar: reference accepts adjacent attributes without whitespace in a tag described as syntactically well formed. No new execution claimed. |
| generation-0119 | Executed acceptance of a public Document literal with zero ID despite the document invariant; no private-state manipulation. |
| generation-0558 | Executed blank Zone lookup returns NotFound rather than Invalid. |
| repair-0322 | Plaintext-equality promise cannot be guaranteed by equality of a 64-bit digest over unrestricted strings. Static information-loss finding, no fabricated concrete collision or production-security approval. |
| generation-0149 | Non-triviality: elementary enum bounds/accessor dispatch with direct comparison. |
| generation-0363 | Non-triviality: fixed-format rendering and direct map/collect wrapper. |
| generation-0662 | Non-triviality: explicitly prescribed borrow/read/consume plus one saturating-add wrapper. |
| repair-0393 | Non-triviality: literal sign correction in a fixed directional mapping. |
| repair-0466 | Non-triviality: one prefix-character substitution beside the already correct parallel implementation. |
| repair-0018 | Non-triviality: direct parity-filter operator replacement. |
| repair-0040 | Non-triviality: explicitly named operand replacement in direct capped worker formula. |
| repair-0048 | Non-triviality: elementary delimiter join. |
| repair-0503 | Non-triviality: explicitly specified strict comparison replacing three non-strict comparisons in a record predicate. Checked multiplication order is source-defined; not a new overflow hold. |

## Executed diagnostics

- rust_0119_public_document_probe-result.json: rustc succeeded, test failed
  [0,101], no timeout, 1781 ms. First rejection assertion failed; the later
  empty-archive assertion was not reached.
- rust_0558_blank_lookup_probe-result.json: rustc succeeded, test failed
  [0,101], no timeout, 2233 ms; actual NotFound versus expected Invalid.

Both preserve original and replacement diagnostic tasks, hashes, output and
pinned Rust 1.85.0 identity. Network disabled, 1 CPU, 512 MiB, 64 PIDs, 60 s.
Original tests/mutants were not rerun by these diagnostics. Repeated elementary
targets require criterion-scoped follow-up of their full affected strata.
