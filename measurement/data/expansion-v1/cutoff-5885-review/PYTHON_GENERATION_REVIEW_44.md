# Python generation review, batch 44

Positions 646–660 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; eight reproduced review holds.
718 additive plus historical three = 721 holds; 1,893 unique outside-sample
inspections. No seven-criterion approval. Continue position 661.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 646 | 0756 | Hold: script contents become visible button text. Ordinary nested text, entity decoding, duplicate replacement and incomplete button finalization agree. CSS visibility and br layout scope pending. |
| 647 | 0757 | Ordinary bytes-like snapshots, eight-byte rows, ASCII rendering and one-shot import agree. Four-digit offset requirement beyond 65535 and released memoryviews pending; no new hold. |
| 648 | 0758 | Full structural validation before copying and per-occurrence deep copies agree. Arbitrary copy-supported value domains pending; no new hold. |
| 649 | 0760 | Ordinary output key order, echoes, first match, mapped value and endpoints agree; no new hold. |
| 650 | 0752 | Enum codes, normalized reverse lookup, valid-only ranking and fresh ordered name list agree; no new hold. |
| 651 | 0761 | Full validation, maximum weight, lexical/earliest ties and exact selected identity agree; no new hold. |
| 652 | 0762 | Hold: finite 401-digit integer score raises OverflowError. Ordinary periodic/best ordering, independent planned copies, copy-failure atomicity and label-position replacement agree. Runtime retain_best mutation semantics pending. |
| 653 | 0763 | Hold: finite 401-digit integer temperature raises OverflowError. Ordinary strict limits, ordered reasons, validated state transition and detached history agree. Copy-failing scalar subclass atomicity pending. |
| 654 | 0764 | Ordinary trimmed attributes, inherited messages, ordered duplicate capabilities and fresh property lists agree; no new hold. |
| 655 | 0768 | Hold: squared-distance underflow joins distinct points at radius zero. Ordinary transitive components, label order and duplicates agree. Large-value overflow domain also pending. |
| 656 | 0769 | Hold: balanced finite extreme samples overflow intermediate sum and produce full drive instead of zero. Ordinary means, clamp, exact names, distinct commands and None short-circuit agree. |
| 657 | 0770 | Prefix/suffix output and O(n) concatenation stages agree. Character-copy cost is not claimed linear; no new hold. |
| 658 | 0771 | Contract hold: leading-zero nonnegative integer epoch silently discarded by unspecified canonical spelling restriction. Ordinary sections, duplicate replacement and finite metrics agree. |
| 659 | 0772 | Hold: finite 401-digit integer coordinate raises OverflowError. Ordinary validated put/replace, sorted output and detached copies agree. |
| 660 | 0773 | Hold: valid range frame rejected despite three-item sequence contract. Ordinary directional crash, three-step checkpoints and zero-goal frame short-circuit agree. Whole-input validation versus early-stop wording pending. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Original candidates/tests/sample/partition unchanged. This batch is backed up;
see QUALITY_STRATUM_721_BACKUP.md for verified backup through Python position 660.

Eight pinned Python 3.11.15 probes, network disabled/resource limited; all
exit 1 without timeout. Holds are review items, not final rejections.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0756 | button_hidden_text_probe.py / button-hidden-text-result.json | 671 | Script body included in button label. |
| 0762 | archive_large_score_probe.py / archive-large-score-result.json | 407 | Finite integer score conversion overflows. |
| 0763 | ventilation_large_integer_probe.py / ventilation-large-integer-result.json | 434 | Finite integer temperature conversion overflows. |
| 0768 | radius_zero_underflow_probe.py / radius-zero-underflow-result.json | 493 | Distinct points connected at radius zero. |
| 0769 | drive_cancellation_overflow_probe.py / drive-cancellation-overflow-result.json | 433 | Balanced values give drive 6 instead of 0. |
| 0771 | epoch_leading_zero_probe.py / epoch-leading-zero-result.json | 424 | Epoch 01 silently discarded. |
| 0772 | parcel_large_coordinate_probe.py / parcel-large-coordinate-result.json | 471 | Finite integer coordinate conversion overflows. |
| 0773 | cart_range_frame_probe.py / cart-range-frame-result.json | 429 | Valid range sequence frame rejected. |
