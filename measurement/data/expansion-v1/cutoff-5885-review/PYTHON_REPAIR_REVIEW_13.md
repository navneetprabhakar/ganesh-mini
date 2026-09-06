# Python repair review, batch 13

Positions 181–195 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Eight new
additive holds: 822 additive plus historical three = 825; 2,112 unique
outside-sample inspections. Holds require disposition, not final rejection.
Inspection is not seven-criterion approval or executed known-bad certification.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 181 | 0211 | Forwarded options repair render/compiler equivalence. Ordinary cache identity and mapping checks agree. Format grammar and user-format-method side effects remain unspecified; no new hold. |
| 182 | 0212 | Boundary flood traversal repairs enclosed-region repaint. Hold: aliased input rows violate independent replacements; finite deep cell fails copying. |
| 183 | 0214 | Per-record details repairs shared dictionary. Hold: valid 5000-digit quantity rejected. Root restriction/comment handling wording pending. |
| 184 | 0215 | Direct channel index repairs off-by-one. Ordinary shape and copies agree. Hold: finite huge integer overflows validation. |
| 185 | 0217 | Deepcopy repairs session aliases while preserving internal sharing. Hold: finite deep extra field fails copying. |
| 186 | 0218 | Shared active-line mode repairs per-line toggling. Indentation and duplicate index checks agree. Line terminator interpretation pending; no new hold. |
| 187 | 0219 | Quote escaping repairs attribute breakout. Ordinary escaping agrees. URL scheme policy is not specified and no new prohibition invented; no new hold. |
| 188 | 0220 | Last-retained comparison repairs global deduplication. Fresh tuple and ordinary validation agree. Hold: finite huge coordinate overflows validation. |
| 189 | 0221 | False on nonbrackets repairs skipped invalid characters. Stack and type logic agree; no new hold. |
| 190 | 0223 | Register/count checksum repaired. Hold: bytes-like memoryview accepted. Finite count, one-shot and byte bounds agree. |
| 191 | 0224 | Positional-or-keyword signature restores compatibility. Effective truthiness and top-level copy agree; nested copy not required. No new hold. |
| 192 | 0225 | Casefold repairs Unicode equivalence. Required NFKC-then-fold order retained; no extra normalization invented. No new hold. |
| 193 | 0226 | Reverse pass includes index zero. Nearest-distance invariant and Unicode code-point tests agree; no new hold. |
| 194 | 0227 | Full length repairs final partial chunk. Independent per-chunk copy agrees ordinarily. Hold: finite deep record fails copying. |
| 195 | 0228 | Prefix repairs full leaf paths. Active ancestor set correctly permits shared branches. Hold: finite acyclic deep dictionary overflows traversal. Nonstring-key exception wording versus tests pending. |

Eight pinned Python 3.11.15 network-disabled/resource-limited executions each
exit 1 without timeout; nine failing/error test cases. Original tests read,
not newly rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0212 | repair_repaint_alias_rows / repair-repaint-alias-rows | 1137 | aliased replacements; bounded RecursionError |
| 0214 | repair_inventory_integer_limit / repair-inventory-integer-limit | 1223 | ValueError |
| 0215 | repair_channel_large_integer / repair-channel-large-integer | 956 | OverflowError |
| 0217 | repair_restore_session_depth / repair-restore-session-depth | 891 | bounded RecursionError |
| 0220 | repair_path_large_integer / repair-path-large-integer | 709 | OverflowError |
| 0223 | repair_register_memoryview / repair-register-memoryview | 444 | bytes-like input accepted |
| 0227 | repair_chunks_depth / repair-chunks-depth | 531 | bounded RecursionError |
| 0228 | repair_index_leaves_depth / repair-index-leaves-depth | 558 | bounded RecursionError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits GCS backup. Verified through position 165 / 811 holds /
2,082 outside-sample inspections (QUALITY_STRATUM_811_BACKUP.md).
Continue position 196.
