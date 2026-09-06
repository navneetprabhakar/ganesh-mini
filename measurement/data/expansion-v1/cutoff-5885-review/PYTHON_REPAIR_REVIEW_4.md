# Python repair review, batch 4

Positions 46–60 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Six new
additive holds: 756 additive plus historical three = 759; 1,977 unique
outside-sample inspections. Holds are pending review, not final rejections.
Source inspection is not seven-criterion approval, nontriviality admission
or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 46 | 0054 | Slash-separated paths repair failed lookups. Exact dict.get behavior, zero values and independent defaults agree; no new hold. |
| 47 | 0055 | Argument unpacking repairs handler call shape. Shallow mapping snapshot and ordinary return/exception behavior agree. Arbitrary handler side effects pending; no new hold. |
| 48 | 0056 | utf-8-sig repairs one leading BOM removal. Later BOM preservation and invalid UTF-8 propagation agree; no new hold. |
| 49 | 0057 | Prefix deletion repairs loss of unclaimed messages. Ordinary pending/in-flight transitions, acknowledgements and detached payloads agree. Hold: finite 600-level payload cannot be added. ID/copy-failure domains pending; no invented atomicity requirement. |
| 50 | 0058 | Tuple yield repairs mutable buffer exposure. Lazy consumption, partial batch and iteration-time validation agree. Nested item alias breadth pending; no new hold. |
| 51 | 0059 | Width mask repairs signed shift. Ordinary low-bit semantics, large shifts and validation agree. Extreme allocation bounds not exercised; no new hold. |
| 52 | 0060 | Single dollar emission repairs double-dollar escape. Literal replacement, left-to-right parsing and missing/empty names agree. Placeholder-name grammar breadth pending; no new hold. |
| 53 | 0064 | Pre-decrement repairs bijective base-26 column names. Boundaries and arbitrary-size integer loop agree; no new hold. |
| 54 | 0065 | Separate list comprehension repairs shared buckets. Round-robin order and validation agree. Exact-int versus integer subclass breadth pending; no new hold. |
| 55 | 0066 | ID comparison repairs title selection. Ordinary metadata copying, order and validation agree. Hold: finite 600-level metadata fails. |
| 56 | 0068 | Seen-ID set repairs duplicate identifier acceptance. Ordinary tags and ordering agree. Hold: valid identifier with 4300 leading zeroes rejected. |
| 57 | 0069 | Deepcopy repairs input mutation. Hold: shared preferences also changes another output field despite preservation wording; graph semantics need disposition. |
| 58 | 0070 | Conditional final append repairs trailing empty page. Ordinary page sizes and isolation agree. Hold: finite 600-level item fails. |
| 59 | 0071 | Composite key repairs module collisions. Replacement order, exact callable identity and no invocation agree; no new hold. |
| 60 | 0072 | Extend repairs replacement of existing records. Hold: shared source partition list causes unintended append to another output partition. |

Six pinned Python 3.11.15 network-disabled/resource-limited probes, each
exit 1 without timeout. Original tests read, not newly rerun by isolated
probes. Original candidates/tests/sample/partition unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0057 | repair_message_buffer_depth / repair-message-buffer-depth | 412 | bounded RecursionError diagnostic |
| 0066 | repair_panels_depth / repair-panels-depth | 660 | bounded RecursionError diagnostic |
| 0068 | repair_tags_decimal_width / repair-tags-decimal-width | 582 | valid identifier raises ValueError |
| 0069 | repair_session_shared_preferences / repair-session-shared-preferences | 598 | other output field also sanitized |
| 0070 | repair_pagination_depth / repair-pagination-depth | 486 | bounded RecursionError diagnostic |
| 0072 | repair_partition_shared_lists / repair-partition-shared-lists | 472 | untouched partition also extended |

Probe filenames append `_probe.py`; results append `-result.json`.
Batches 3–4 backed up in QUALITY_STRATUM_759_BACKUP.md.
Continue position 61.
