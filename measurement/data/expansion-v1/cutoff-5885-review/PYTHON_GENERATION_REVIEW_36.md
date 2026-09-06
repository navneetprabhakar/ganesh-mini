# Python generation review, batch 36

Positions 526–540 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; seven reproduced holds.
671 additive plus historical three = 674 holds; 1,773 unique outside-sample
inspections. No seven-criterion approval. Continue position 541.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 526 | 0615 | Ordinary option validation, defaults and load-size fallback agree. Option-looking text values and large integer parsing breadth pending; no new hold. |
| 527 | 0620 | Window order, separate cross-window deep copies and ordinary validation agree. Arbitrary deepcopy domain pending; within-window alias preservation is not forbidden explicitly; no new hold. |
| 528 | 0623 | Arithmetic alignment, positive progression, reversed interval validation and inclusive bounds agree; no new hold. |
| 529 | 0624 | Hold: embedded newline in text breaks required output line width. Ordinary padding, truncation, column order and weight format agree. Text normalization/restriction policy needs disposition; large integer weights pending. |
| 530 | 0621 | Hold: finite representable mean squared error becomes infinity via intermediate sum. Ordinary build, parameter names and regularization agree; other numeric breadth pending. |
| 531 | 0622 | Ordinary builder validation, registry atomicity, complete config copies and intentional buffer identity agree. Arbitrary copied payloads and public field mutation pending; no new hold. |
| 532 | 0625 | Hold: tag stripping merges distinct strings despite only names being specified for stripping. Ordinary ID progression, invalid command isolation and independent snapshots agree. |
| 533 | 0627 | Exact integer monotone binary search, zero-job validation and non-expansion agree; no new hold. |
| 534 | 0628 | Hold: finite large integer input raises OverflowError before identity model. Ordinary loader precedence, evaluation hook, callback copies and output width agree; general Real domain pending. |
| 535 | 0629 | Ordinary stripped style assignment, independent cycles, fresh entries and float coordinates agree. Nonrepresentable coordinate and mutable numeric-subclass domains pending; no new hold. |
| 536 | 0630 | Ordinary aggregation, classification, sort and specified escape order agree. Very large integer text conversion pending; no new hold. |
| 537 | 0631 | Hold: valid 1500-node tree raises RecursionError. Ordinary mirror structure, payload identity, cycle/shared-child rejection agree. |
| 538 | 0633 | Ordinary mapping/generator order, exact boolean flags and tuple projections agree. Malformed duck-typed mapping error normalization pending; no new hold. |
| 539 | 0634 | Hold: oversized malformed port aborts whole call instead of unsuccessful candidate. Ordinary bounded active probes, duplicates, result order and singleton True agree. Unicode decimal and cancellation interpretation pending. |
| 540 | 0635 | Hold: overflow-generated NaN treated as converged. Ordinary in-place Gauss-Seidel, endpoints and iteration cap agree. Invalid sequence type exception normalization and numeric domain pending. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up
through 674 holds / Python position 540; see QUALITY_STRATUM_674_BACKUP.md.

Seven pinned Python 3.11.15 probes, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0624 | parcel_embedded_newline_probe.py / parcel-embedded-newline-result.json | 415 | Text newline creates short extra output lines. |
| 0621 | layered_loss_mean_overflow_probe.py / layered-loss-mean-overflow-result.json | 509 | Infinity instead of finite mean squared error. |
| 0625 | membership_tag_whitespace_probe.py / membership-tag-whitespace-result.json | 516 | Two distinct tags become one stripped tag. |
| 0628 | pipeline_large_integer_probe.py / pipeline-large-integer-result.json | 472 | OverflowError for finite integer input. |
| 0631 | mirror_deep_tree_probe.py / mirror-deep-tree-result.json | 511 | RecursionError for valid deep tree. |
| 0634 | endpoints_long_port_probe.py / endpoints-long-port-result.json | 537 | Integer conversion exception escapes candidate filter. |
| 0635 | chain_overflow_convergence_probe.py / chain-overflow-convergence-result.json | 478 | Returns (2, nan, 2). |
