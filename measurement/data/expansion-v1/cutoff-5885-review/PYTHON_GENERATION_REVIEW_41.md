# Python generation review, batch 41

Positions 601–615 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; four reproduced review holds.
694 additive plus historical three = 697 holds; 1,848 unique outside-sample
inspections. No seven-criterion approval. Continue position 616.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 601 | 0705 | Flood-fill region labels and maximal uninterrupted row/column spans agree, including same-region exclusion and empty dimensions. Integer subclass exactness pending; no new hold. |
| 602 | 0707 | Exact ordered JSON steps, standard indentation/newline, environment sorting and preserved sequence duplicates agree; no new hold. |
| 603 | 0708 | Longest prefix, overwritten segment, plain copied dictionaries and record order agree. Arbitrary mapping/copy domains pending; no new hold. |
| 604 | 0709 | Exact request shape, ordinary arithmetic, floor division and error results agree. Integer subclass acceptance pending; no new hold. |
| 605 | 0710 | Query shape, trimmed/default recipient and fresh nested response dictionaries agree; no new hold. |
| 606 | 0712 | Distinct-width count, empty inputs and nonmutation agree. Integer subclass acceptance pending; no new hold. |
| 607 | 0713 | Standard digest algorithms and sizes, exact rendering and two-digest matching agree; data is not retained. No new hold. |
| 608 | 0714 | Hold: finite valid depth-1500 tree hits recursion limit. Ordinary depth-first child order and structural validation agree. Detail-value restrictions versus string-key wording and cycle scope pending. |
| 609 | 0711 | Ordinary global uniqueness, tag filtering, sequence ordering and separate public/internal/result copies agree. Scalar subclass copy domains pending; no new hold. |
| 610 | 0715 | Hold: invalid unhashable state raises TypeError instead of required ValueError. Ordinary lifecycle event order, identity and per-manager histories agree. Post-construction invalid state semantics pending. |
| 611 | 0716 | Ordinary declarations, additional equals, parse-error suppression and duplicate warning order agree. Extended line separators pending; no new hold. |
| 612 | 0718 | Hold: finite large means produce infinity; squared distance raises OverflowError for finite values. Ordinary means, insertion order and lexical ties agree. Broader Real conversion domain pending. |
| 613 | 0719 | Ordinary selected angles, rounding, normalized zeros and fresh output agree. Real values outside float representability and trigonometric precision envelope pending; no new hold. |
| 614 | 0720 | Ordinary exact schemas, summed quantities including zero customers, sort keys and detached dictionaries agree; no new hold. |
| 615 | 0717 | Hold: standard MappingProxyType fields pass mapping validation but constructor deepcopy raises TypeError. Ordinary read-only properties and basic consistency checks agree. Invalid kind exception precedence and wider internal-corruption domains pending. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up;
see QUALITY_STRATUM_705_BACKUP.md for verified backup through Python position 630.

Four pinned Python 3.11.15 probes, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0714 | terminal_deep_tree_probe.py / terminal-deep-tree-result.json | 471 | RecursionError for finite depth-1500 tree. |
| 0715 | unit_unhashable_state_probe.py / unit-unhashable-state-result.json | 430 | TypeError for list state, rather than ValueError. |
| 0718 | centroid_finite_extremes_probe.py / centroid-finite-extremes-result.json | 527 | Infinite mean and squared-distance OverflowError. |
| 0717 | work_message_mapping_proxy_probe.py / work-message-mapping-proxy-result.json | 436 | Valid standard read-only mapping cannot be copied directly. |
