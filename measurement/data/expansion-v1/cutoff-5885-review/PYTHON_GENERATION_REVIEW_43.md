# Python generation review, batch 43

Positions 631–645 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; eight reproduced review holds.
710 additive plus historical three = 713 holds; 1,878 unique outside-sample
inspections. No seven-criterion approval. Continue position 646.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 631 | 0738 | Hold: shared account reference means changing selected email also changes another key's copied account. Ordinary existing/new account behavior and return identity agree. |
| 632 | 0739 | Ordinary exact cached identity including None, one provider call and exception-before-cache-write agree. Aliased provider/cache mappings and provider side effects pending; no new hold. |
| 633 | 0741 | Hold: valid UserDict record rejected despite mapping contract. Ordinary deterministic splits and independent target matrices agree. Broader sequence validation pending. |
| 634 | 0744 | Hold: valid UserDict item rejected despite mapping contract. Ordinary ordering, independent pagination, repeated resolved items and copies agree. item_ids sequence validation breadth pending. |
| 635 | 0740 | Hold: finite constant series produces infinity in all three averaging schemes. Ordinary windows, weighted means, exponential seed and span-one behavior agree. |
| 636 | 0742 | Hold: finite input multiplication overflow yields NaN even for single-class softmax, whose probability must be one. Ordinary cross-correlation, per-patch bias/ReLU and score normalization agree. Matrix sequence validation breadth pending. |
| 637 | 0745 | Ordinary insertion order, detached reads/revisions/removals and malformed-revision atomicity agree. Empty-change and mixed-error precedence wording pending; no new hold. |
| 638 | 0746 | Ordinary repeated requests, ordered missing keys and separately deep-copied occurrences agree. Wider deepcopy-supported scalar domains pending; no new hold. |
| 639 | 0747 | Hold: non-string UserString equal to yes authenticates despite required string type. Ordinary menu order, fallback and new menu lists agree. |
| 640 | 0748 | Full-list validation, earliest maximum and detached selected dictionary agree; no new hold. |
| 641 | 0749 | Ordinary integer rectangles, absolute coordinates, ordering and nonmutation agree. Literal no-alias wording versus immutable tuple reuse and scalar subclasses pending; no new hold. |
| 642 | 0750 | Ordinary whole-input validation, bounded inspection and case-insensitive standalone word matching agree. Extended Unicode word-boundary meaning pending; no new hold. |
| 643 | 0751 | Hold: submit receives caller-owned mutable identifier and can mutate nested input. Ordinary matching order and duplicate dispatch agree. Partial dispatch before malformed later entry has no explicit atomicity guarantee. |
| 644 | 0753 | Hold: 1,200-character input with only one possible split exceeds recursive depth. Ordinary lexicographic deduplicated splits and one-shot term import agree. |
| 645 | 0755 | Ordinary shared IDs, explicit IDs, rendering and positional/keyword configuration agree. Square width/height direct mutation and failed-construction counter consumption semantics pending; no new hold. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch awaits backup;
last verified backup is through 705 holds / Python position 630.

Eight pinned Python 3.11.15 probes, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0738 | identity_shared_account_probe.py / identity-shared-account-result.json | 469 | Unselected account email changes. |
| 0741 | examples_userdict_probe.py / examples-userdict-result.json | 584 | UserDict record rejected. |
| 0744 | catalog_userdict_probe.py / catalog-userdict-result.json | 489 | UserDict item rejected. |
| 0740 | smoothing_finite_mean_probe.py / smoothing-finite-mean-result.json | 444 | Mean, linear and exponential seed all overflow. |
| 0742 | patch_softmax_overflow_probe.py / patch-softmax-overflow-result.json | 559 | Single-class probability NaN. |
| 0747 | panel_nonstring_auth_probe.py / panel-nonstring-auth-result.json | 511 | UserString yes authenticates. |
| 0751 | dispatch_identifier_mutation_probe.py / dispatch-identifier-mutation-result.json | 439 | Submit mutates caller identifier list. |
| 0753 | compound_single_split_depth_probe.py / compound-single-split-depth-result.json | 454 | RecursionError on one-split input. |

