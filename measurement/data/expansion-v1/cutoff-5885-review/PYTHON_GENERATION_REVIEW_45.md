# Python generation review, batch 45

Positions 661–675 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; ten reproduced review holds.
728 additive plus historical three = 731 holds; 1,908 unique outside-sample
inspections. No seven-criterion approval. Continue position 676.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 661 | 0774 | Hold: valid range endpoint sequence rejected. Ordinary normalized deduplication, length/endpoint order and degree-limited Kruskal agree. Greedy inability is specified, not a global constrained-MST solver defect. |
| 662 | 0775 | Hold: valid range target sequence rejected. Ordinary distances, inclusive first reach and new path lists agree. Numeric representability pending. |
| 663 | 0779 | Hold: unsupported PATCH method parses 5,000-digit ID and raises instead of returning None. Ordinary canonical IDs, exact paths/methods and new dictionaries agree. |
| 664 | 0780 | Ordinary delimiter stack, ignored characters, empty/no-delimiter strings and full validation agree; no new hold. |
| 665 | 0776 | Hold: oversized invalid integer year raises OverflowError instead of ValueError. Ordinary Gregorian dates, zero-padding and range checks agree. General sequence acceptance pending. |
| 666 | 0781 | Hold: shared base rows cause one-row patch to overwrite another row too. Ordinary transparency, deep-copy boundaries and placement validation agree. Zero-width versus empty-rectangle fit wording pending. |
| 667 | 0782 | Ordinary requested-namespace duplicates, slug-ordered selection, preserved record order and normalized 24-character summary agree; no new hold. |
| 668 | 0783 | Ordinary title casing, key casefold collisions, call order and attribute copies agree. Exact reserved argument keyword binding versus ValueError wording and arbitrary copy domains pending; no new hold. |
| 669 | 0784 | Hold: shared category lists cause add in one category to alter another. Ordinary transactional input preservation, SKU rules and command ordering agree. |
| 670 | 0785 | Hold: standard UserDict index rejected despite mapping wording. Ordinary reserved command precedence, case/whitespace significance and output order agree. |
| 671 | 0786 | Hold: surrounding whitespace float string decoded despite explicit preservation rule. Ordinary bool/int/float decoding and first-key order agree. Long integer conversion domain pending. |
| 672 | 0788 | Hold: valid depth-1200 acyclic hierarchy exceeds recursion limit. Ordinary active-path cycle detection, repeated names and sorted attributes agree. Facts mapping breadth pending. |
| 673 | 0789 | Ordinary ragged-row omission, ignored negative/oversized positions and individual retained-cell copies agree. Arbitrary copy domains pending; no new hold. |
| 674 | 0790 | Hold: phase exponent reverses specified target-source difference; original tests endorse source-target. Ordinary layer order, swaps and immutable top-level structure agree. Empty-tuple freshness interpretation pending. |
| 675 | 0791 | Ordinary concrete class names, inherited notes, proper-subclass registration, exact retrieval and independent ordered catalog state agree. Invalid lookup type semantics pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up;
see QUALITY_STRATUM_733_BACKUP.md for verified backup of the full generation queue.

Eleven pinned Python 3.11.15 probe runs, network disabled/resource limited;
all exit 1 without timeout. Ten distinct holds, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0774 | links_range_edge_probe.py / links-range-edge-result.json | 821 | Range endpoint pair rejected. |
| 0775 | trajectory_range_target_probe.py / trajectory-range-target-result.json | 424 | Range target rejected. |
| 0779 | inventory_unmatched_large_id_probe.py / inventory-unmatched-large-id-result.json | 513 | Unsupported method raises decimal conversion error. |
| 0776 | moment_oversized_year_probe.py / moment-oversized-year-result.json | 783 | Wrong exception on oversized year. |
| 0781 | stamp_shared_row_probe.py / stamp-shared-row-result.json | 412 | Both shared rows overwritten. |
| 0784 | catalog_shared_category_probe.py / catalog-shared-category-result.json | 440 | Both shared category lists changed. |
| 0785 | requests_mapping_index_probe.py / requests-mapping-index-result.json | 431 | Mapping index rejected. |
| 0786 | options_spaced_float_probe.py / options-spaced-float-result.json | 478 | Spaced float converted. |
| 0788 | labels_deep_hierarchy_probe.py / labels-deep-hierarchy-result.json | 470 | Traceback capture truncated; retained as original evidence. |
| 0788 | labels_deep_bounded_probe.py / labels-deep-bounded-result.json | 449 | Bounded repeat explicitly captures RecursionError. |
| 0790 | counting_phase_exponent_probe.py / counting-phase-exponent-result.json | 524 | Phase value 4 instead of specified 1 at width two. |
