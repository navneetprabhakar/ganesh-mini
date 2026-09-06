# Python repair review, batch 10

Positions 136–150 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Six new
additive holds: 799 additive plus historical three = 802; 2,067 unique
outside-sample inspections. Holds are review items, not final rejections.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 136 | 0161 | End slice repairs half-open replacement. Boundary/empty slice validation agrees. Immutable string identity wording pending; no new hold. |
| 137 | 0162 | False default repairs readonly inversion. Mapping/sequence validation and ordinary detached structure agree. Immutable tuple sharing and scalar-subclass breadth pending; no new hold. |
| 138 | 0164 | Removing getattr/filter repairs descriptors and callable inclusion. Built-in dir behavior and sorting agree. Custom dir side effects are not a newly inferred guarantee; no new hold. |
| 139 | 0165 | BIL index repairs per-row channel planes. Three layouts and zero shapes agree. Hold: unhashable malformed layout gives wrong exception. |
| 140 | 0167 | Append repairs repeated-key overwrite. Order, empty strings and fresh value lists agree. Scalar-subclass aliases pending; no new hold. |
| 141 | 0168 | Deepcopy repairs ordinary nested metadata aliases. Hold: zero limit still copies matched records and fails on finite deep metadata. |
| 142 | 0169 | Trailing check repairs extra JSON acceptance. Hold: valid 5000-digit integer rejected. Duplicate-key/whitespace grammar breadth pending. |
| 143 | 0170 | Inclusive square bound repairs composite primality. Distinct increasing factors and exact-int validation agree. No runtime bound invented; no new hold. |
| 144 | 0171 | Uppercase hex class repairs mixed-case parsing. Fullmatch and output order agree; line-separator breadth pending, no new hold. |
| 145 | 0172 | Increment repairs duplicate-level overwrite. First-observation order and independent dictionaries agree. Embedded newline/delimiter grammar pending; no new hold. |
| 146 | 0173 | Identity repairs equality-based removal. Snapshot pipeline and repeated registration agree. Test accesses private _hooks for decorator assertion; unnecessary representation constraint pending, no new hold. |
| 147 | 0174 | Exact-int check repairs booleans. Hold: terminal-newline identifier accepted and unhashable operator gives wrong exception. Literal/depth bounds pending. |
| 148 | 0175 | ASCII lookarounds repair Unicode word-boundary mismatch. Exact case, spacing and iterable semantics agree; no new hold. |
| 149 | 0176 | Deepcopy repairs overlay value aliasing. Hold: overlay-only mutable hashable key is still retained by identity. Cyclic/deep merge behavior pending. |
| 150 | 0177 | Integer midpoint repairs float indexing. Binary-search invariant and post-validation complexity agree. Hold: set accepted as sequence. |

Six pinned Python 3.11.15 network-disabled/resource-limited probe executions,
each exit 1 without timeout; seven assertions exposed defects. Original tests
read, not newly rerun by isolated probes. Candidates/tests/sample/partition
unchanged. Candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0165 | repair_scan_layout_type / repair-scan-layout-type | 893 | TypeError instead of ValueError |
| 0168 | repair_context_zero_limit_depth / repair-context-zero-limit-depth | 789 | bounded RecursionError |
| 0169 | repair_envelope_integer_limit / repair-envelope-integer-limit | 442 | ValueError for valid integer |
| 0174 | repair_expression_validation / repair-expression-validation | 616 | newline accepted; wrong exception |
| 0176 | repair_settings_key_alias / repair-settings-key-alias | 644 | retained mutable key identity |
| 0177 | repair_lower_bound_sequence / repair-lower-bound-sequence | 548 | invalid set accepted |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 135 / 796 holds /
2,052 outside-sample inspections (QUALITY_STRATUM_796_BACKUP.md).
Continue position 151.
