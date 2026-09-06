# Python repair review, batch 5

Positions 61–75 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Eight new
additive holds: 764 additive plus historical three = 767; 1,992 unique
outside-sample inspections. Holds remain review items, not final rejections.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 61 | 0073 | Deepcopy repairs shared defaults. Ordinary validated overrides and independent results agree. Scalar subclass copy breadth pending; no new hold. |
| 62 | 0074 | Iteration instead of reverse/pop repairs token mutation. Hold: early float conversion turns integer difference 1 into 0. |
| 63 | 0075 | Corrected regex and direct conversion reject underscores and accept ordinary whitespace. Hold: in-range dimension with 4300 leading zeroes rejected. Known-bad regex also has doubled whitespace escapes; the exactly-one-defect claim needs separate provenance review. |
| 64 | 0076 | First-equals partition repairs values containing equals. Trimming, duplicate replacement order and malformed segment checks agree; no new hold. |
| 65 | 0077 | Base-then-update merge repairs field priority. Ordinary independent row copies and new-ID order agree. Hold: finite 600-level row fails. |
| 66 | 0078 | Inclusive first slot repairs boundary scheduling. Integer modulo, first/input order and validation agree; no new hold. |
| 67 | 0079 | Strict majority repairs ties and empty batches. Ordinary lowercase-letter validation and fresh output agree. Letter-only interpretation supported by original tests; no new hold. |
| 68 | 0080 | Seen set with ordered append repairs sorted rather than first-occurrence output. Arbitrary-size ordinary ints and validation agree; no new hold. |
| 69 | 0081 | Fixed earliest origin repairs previous-event deltas. Stable order and ordinary extra fields agree. Hold: finite 600-level payload fails. |
| 70 | 0082 | Empty count 1 repairs derangement boundary. Integer recurrence and exact validation message agree; no new hold. |
| 71 | 0084 | Per-leaf deepcopy repairs input and repeated-reference aliasing. Hold: valid 600-dimensional singleton shape raises RecursionError. |
| 72 | 0086 | Current value repairs shifted column selection. Ordinary rectangular transpose and independent cells agree. Hold: finite 600-level cell fails. |
| 73 | 0087 | Decrement repairs non-progressing recursion. Hold: n=1100 exceeds runtime recursion depth. Prompt requires preserving recursive structure; domain bound needs disposition. |
| 74 | 0088 | Announce guard repairs suppressed callback behavior. Ordinary previous/new/callback copies and retained state after callback error agree. Hold: finite 600-level initial value fails. |
| 75 | 0089 | Exclusive slice endpoint repairs overlap. Empty, Unicode, exact chunks and positive integer limits agree; no new hold. |

Eight pinned Python 3.11.15 network-disabled/resource-limited probes, each
exit 1 without timeout. Original tests read, not newly rerun by isolated
probes. Candidates/tests/sample/partition unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0074 | repair_expression_integer_precision / repair-expression-integer-precision | 492 | zero instead of one |
| 0075 | repair_canvas_decimal_width / repair-canvas-decimal-width | 482 | valid padded dimension rejected |
| 0077 | repair_overlay_depth / repair-overlay-depth | 501 | bounded RecursionError |
| 0081 | repair_actions_depth / repair-actions-depth | 489 | bounded RecursionError |
| 0084 | repair_reshape_rank / repair-reshape-rank | 477 | bounded RecursionError |
| 0086 | repair_pivot_depth / repair-pivot-depth | 475 | bounded RecursionError |
| 0087 | repair_cumulative_depth / repair-cumulative-depth | 741 | bounded RecursionError |
| 0088 | repair_state_slot_depth / repair-state-slot-depth | 755 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batches 5–6 backed up in QUALITY_STRATUM_774_BACKUP.md.
Continue position 76.
