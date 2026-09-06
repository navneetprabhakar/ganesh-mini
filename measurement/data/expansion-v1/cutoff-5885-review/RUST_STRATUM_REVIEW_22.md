# Rust generation review, batch 22

Positions 316–330 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; two new holds. Total 879 unique
outside-sample inspections; 432 additive plus historical three = 435 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 316 | 0371 | Sandbox hold: unescaped NUL field boundaries allow undetected public transfer alteration under the required digest recipe. |
| 317 | 0373 | ASCII priorities, alternating masks, complete quartet validation and checked sums agree. No new hold. |
| 318 | 0375 | Exact decoder API, transactional candidate buffer, early oversized header and owned frames agree. No new hold. |
| 319 | 0376 | Exact parsers, count-before-number precedence, ASCII digits and ordered trail error mapping agree. No new hold. |
| 320 | 0377 | Exact presence API, entry/reentry order, no-op count and retained successful prefix on batch failure agree. No new hold. |
| 321 | 0378 | Static hold: midterm-first error requirement conflicts with any-nonfinite-input rule; original tests require OutOfRange for 101/NaN. |
| 322 | 0374 | Exact settings API, line precedence, setters and fixed encoding agree. Whitespace-only meaning of blank line remains unspecified; no new hold. |
| 323 | 0379 | Clipped row/column updates, saturating length, zero-size rendering and bounds agree with tests. Changed-versus-addressed count on same-character draw and huge zero-height allocation remain unresolved. No new hold. |
| 324 | 0380 | Exact bit order, count gate, byte checksum and widened combination agree. Tenths-byte values above 9 not explicitly rejected by contract; no new hold. |
| 325 | 0381 | Prefix/one-space handling, key block boundaries and text replacement/continuations agree. Bare prefix versus one-space-only body is ambiguous; no new hold. |
| 326 | 0382 | Exact layout, UTF-8 byte limits, checked decoder slicing and typed malformed errors agree. No new hold. |
| 327 | 0383 | Ethernet/IP gates, total-length-bounded port reads and fragment precedence agree. No new hold; pure classifier, not full protocol validation. |
| 328 | 0384 | Unsigned absolute magnitude handles minimum isize; manual digit conversion obeys forbidden-formatting rule. No new hold. |
| 329 | 0385 | Exact grant data/functions, checked funding, half-open times and owned snapshots agree. Error variants are author-selected and original tests accept any error; private ID exhaustion untested. No new hold. |
| 330 | 0386 | Exact declarations and literal decoding, normal empty-alias matching, ordered duplicates and owned strings agree. No new hold. |

0371: `transfer_log_delimiter_probe.rs` and `transfer-log-delimiter-result.json`
bind pinned network-disabled Rust execution: compile 0, test 101, 1,529 ms,
no timeout. Append from `a\0b` to `c`, then change only public sender/receiver
to `a` and `b\0c`. is_valid still returns true because serialized bytes are
identical under the explicitly required zero-delimiter recipe. This contradicts
the promise to detect public field alterations. It is a specification-level
encoding ambiguity, not a searched cryptographic hash collision. Both parties
remain nonempty, so append validation does not exclude this input.

0378: Prompt requires validating midterm first, but additionally says any
non-finite input yields NonFinite. Original test explicitly asserts
weighted_grade(101.0, NaN) yields OutOfRange, as the reference does. The shared
error type does not resolve these competing rules. Static hold, no new execution.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Inspection is not seven-criterion admission. Scope v6/sample/partition unchanged.
Continue 331; no new VM or training seal.
