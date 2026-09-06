# Python repair review, batch 7

Positions 91–105 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Eight new
additive holds: 779 additive plus historical three = 782; 2,022 unique
outside-sample inspections. Holds remain review items, not final rejections.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 91 | 0108 | Per-sample deepcopy repairs cross-position aliasing. Ordinary schemas and order agree. Hold: finite 600-level sample fails; inner graph-sharing interpretation pending. |
| 92 | 0109 | Min repairs downward envelope. Ordinary recurrence and fresh list agree. Hold: finite huge integer rejected. |
| 93 | 0110 | Final suffix slice repairs dotted stems. Ordinary case-insensitive suffix and page lists agree. Extreme output size and integer-subclass breadth pending; no new hold. |
| 94 | 0111 | Current-state return repairs binary count. Ordinary recurrence and fixed number of accumulator objects agree; exact-int and bit-space wording pending, no new hold. |
| 95 | 0112 | Ascending keys repair fingerprint canonicalization. Explicit quote behavior and HMAC inputs agree. Non-UTF8-encodable surrogate domain pending; no new hold. |
| 96 | 0113 | Strict half comparison repairs exact-half boundary. Hold: rounded float half rejects valid large odd-modulus wrap. |
| 97 | 0114 | Per-cell copying repairs shared row cells. Ordinary shapes and zero dimensions agree. Hold: finite 600-level fill fails. |
| 98 | 0115 | Store-time bytes snapshot repairs mutable buffer aliasing. Ordinary overwrite order, independent instances and validation agree. Released views/scalar subclasses pending; no new hold. |
| 99 | 0116 | Numeric sort key repairs textual ordering. Hold: Unicode sharp-s expands to SS and bypasses digit alphabet restriction. |
| 100 | 0117 | Separate children repair shared tree nodes. Iterative breadth-first construction and ordinary validation agree. Intrinsically exponential output not stress allocated; no new hold. |
| 101 | 0118 | Min priority with earliest tie repairs selection. Hold: valid MappingProxyType cannot be deep-copied into returned dictionary. No network access performed. |
| 102 | 0119 | Key comparison repairs value-driven renaming. Ordinary collision/order and Mapping acceptance agree. Hold: finite 600-level symbol value fails. |
| 103 | 0121 | First accumulator repairs GCD return. Exact integer Euclidean recurrence, magnitudes and both-zero behavior agree; no new hold. |
| 104 | 0122 | Existing-secret conjunction repairs unknown-user authentication. Ordinary exact matches, malformed values and fresh users agree. Scalar subclass domains pending; no new hold. |
| 105 | 0123 | Named lookup repairs first-panel return. Ordinary order and detached selection agree. Hold: finite 600-level content fails. |

Eight pinned Python 3.11.15 network-disabled/resource-limited probes, each
exit 1 without timeout. Original tests read, not newly rerun by isolated
probes. Candidates/tests/sample/partition unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0108 | repair_sensors_depth / repair-sensors-depth | 645 | bounded RecursionError |
| 0109 | repair_envelope_large_integer / repair-envelope-large-integer | 616 | OverflowError |
| 0113 | repair_packet_half_precision / repair-packet-half-precision | 447 | valid wrap rejected |
| 0114 | repair_grid_fill_depth / repair-grid-fill-depth | 680 | bounded RecursionError |
| 0116 | repair_radix_unicode_expansion / repair-radix-unicode-expansion | 627 | invalid alphabet accepted |
| 0118 | repair_route_mapping_proxy / repair-route-mapping-proxy | 616 | TypeError copying standard mapping |
| 0119 | repair_bind_local_depth / repair-bind-local-depth | 504 | bounded RecursionError |
| 0123 | repair_panel_book_depth / repair-panel-book-depth | 440 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 90 / 774 holds /
2,007 outside-sample inspections (QUALITY_STRATUM_774_BACKUP.md).
Continue position 106.

