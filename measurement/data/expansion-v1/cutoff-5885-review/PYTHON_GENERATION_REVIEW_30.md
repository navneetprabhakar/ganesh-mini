# Python generation review, batch 30

Positions 436–450 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; five reproduced holds.
644 additive plus historical three = 647 holds; 1,683 unique outside-sample
inspections. No seven-criterion approval. Continue position 451.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 436 | 0501 | Ordinary ID/sequence allocation, failed validation, frozen records and independent details agree. Record-ID type domain and exceptional deepcopy atomicity pending; no new hold. |
| 437 | 0500 | Hold: control separator stripped and accepted despite rejection by Python int syntax. Ordinary signs, underscores, Unicode digits and large quotient handling agree. |
| 438 | 0505 | Hold: valid 5001-digit integer fails digital-root computation at runtime string-conversion limit. Ordinary reduction, cached node value, formatting and next identity agree. |
| 439 | 0506 | Literal conversion formulas, ties-to-even rounding and distinct batch lists agree. Nonfinite/overflow numeric domain and consumed iterable semantics pending; no new hold. |
| 440 | 0507 | Exact repr field order, whitespace validation, sequence order/duplicates and no trailing newline agree ordinarily. Custom repr domains pending; no new hold. |
| 441 | 0508 | Status-200 checks, missing-page handling, substring semantics, ordering and constructor copies agree ordinarily. General pair/scalar-subclass domains pending; no new hold. |
| 442 | 0509 | Hold: NaN dropout accepted although it does not satisfy positive-dropout precondition. Ordinary guidance formulas, independent invocations and output validation agree. Invalid-index exception contract and callable-model validation pending. |
| 443 | 0510 | Iterative reconstruction, uniqueness/set validation, distinct nodes and final consistency checks agree for ordinary values. Nonreflexive hashable values and custom equality domains pending; no new hold. |
| 444 | 0511 | Hold: mixed-type unknown keys leak sorting TypeError rather than required ValueError. Ordinary tags, span, trimming and override independence agree. General mapping validation pending. |
| 445 | 0514 | Ordinary simultaneous matching, overlap counts, gravity/refill order and rollback agree. Pre-existing unrelated runs versus swap-created runs, row-shape wording and scalar subclasses pending; no new hold. |
| 446 | 0516 | Exact manifest fields, modulo wrapping and fresh dict agree; no new hold. |
| 447 | 0513 | Hold: missing optional-header column does not mark row malformed. Ordinary tier normalization, physical row warnings and parsing-error conversion agree. Duplicate headers/multiline numbering pending. |
| 448 | 0517 | First qualifying script, path suffix, URL resolution, cached precedence and returned cache copies agree ordinarily. Malformed URLs, duplicate attributes and broader mapping types pending; no new hold. |
| 449 | 0518 | Ordinary oriented scaling/truncation, nearest-neighbor sampling, reduced grid independence and border threshold agree. Extreme paper integers and floating dimension rounding pending; no new hold. |
| 450 | 0520 | Namespace-local matching, direct precedence, sorted classification and ordinary parse failures agree. Empty manifest attributes and non-ParseError XML failures pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up;
see QUALITY_STRATUM_647_BACKUP.md for verified evidence through position 450.

Five pinned Python 3.11.15 probe runs, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0500 | division_control_separator_probe.py / division-control-separator-result.json | 341 | Control separator produces ok rather than invalid. |
| 0505 | digit_root_large_integer_probe.py / digit-root-large-integer-result.json | 504 | ValueError at 4300-digit conversion limit. |
| 0509 | guidance_nan_dropout_probe.py / guidance-nan-dropout-result.json | 306 | NaN dropout accepted. |
| 0511 | snippet_mixed_unknown_keys_probe.py / snippet-mixed-unknown-keys-result.json | 490 | TypeError sorting int and str unknown keys. |
| 0513 | enrollment_missing_optional_column_probe.py / enrollment-missing-optional-column-result.json | 333 | Malformed row admitted to starter with no warning. |
