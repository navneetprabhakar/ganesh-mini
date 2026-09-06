# Python generation review, batch 5

Positions 61–75 of 684, v6 outside-sample Python generation queue. Fifteen full
prompt/reference/original-test inspections; four sandbox-confirmed holds and
one static locale-dependence hold. 505 additive plus historical three = 508
holds; 1,308 unique outside-sample inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 61 | 0066 | Full validation before filtering, exact category selection, field order and independently copied values agree. No new hold. |
| 62 | 0067 | Hold: range(3), a three-item integer sequence representing (0,1,2), is rejected by list/tuple-only validation. |
| 63 | 0069 | Typed validation, requested order then sorted extras, sign counts and fresh dictionaries agree. No new hold. |
| 64 | 0070 | Hold: valid assignment value ending in ] is misclassified as malformed header. Nested-bracket section-name restrictions remain a separate grammar question. |
| 65 | 0071 | Separate canonical deepcopies and intentional alias-to-copy identities agree. Arbitrary custom deepcopy hooks remain a contract boundary; no new hold. |
| 66 | 0072 | Full shape validation, exact-balance debit/transfer, creation order and self-transfer handling agree. Non-string operation error classification remains pending; no new hold. |
| 67 | 0073 | Static hold: datetime.strptime with %B uses process-locale month names despite explicit locale independence. Numeric season-string variants and date-width strictness remain pending. |
| 68 | 0074 | Hold: unhashable unknown section raises TypeError instead of ValueError. Staged ordinary updates otherwise preserve atomicity. |
| 69 | 0075 | Compact UTF-8 sizing, exact boundaries and ordered snapshots agree for valid JSON values. NaN/surrogate domain and quadratic construction envelope pending; no new hold. |
| 70 | 0077 | Exact enum types, frozen dataclass equality/hash and printed summary agree. Low-level Python immutability bypasses not imposed; no new hold. |
| 71 | 0076 | Ordinary LF framing, decoding order, bounded summaries, consistent node separators and scalar patterns agree. CRLF framing and finite decimal range wording remain pending; no new hold. |
| 72 | 0080 | Exact payload keys, normalization, one-based IDs and ordinary deep-copy isolation agree. Stateful custom deepcopy failure on the return copy remains pending; no new hold. |
| 73 | 0081 | Full integer/sorted validation and lower-bound binary search agree. No new hold. |
| 74 | 0082 | Hold: append with whitespace-only name raises KeyError, contrary to stated invalid-name ValueError rule. Ordinary commit/rollback/context copies agree. |
| 75 | 0083 | Normalized pair replacement retains inspector order; bounded scores, float mean and fresh entries agree. No new hold. |

Four probes ran in pinned Python 3.11.15, network disabled, resource limited;
each exited 1 without timeout. Hash-bound evidence preserves original candidate,
task, probe and runtime. Locale finding is static, not an executed locale test.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0067 | paint_range_span_probe.py / paint-range-span-result.json | 441 | TypeError rejects valid range sequence. |
| 0070 | section_bracket_value_probe.py / section-bracket-value-result.json | 400 | ValueError rejects value=items[0]. |
| 0074 | maintenance_section_probe.py / maintenance-section-result.json | 549 | TypeError at dictionary membership for section=[]. |
| 0082 | workspace_empty_name_probe.py / workspace-empty-name-result.json | 435 | KeyError for normalized empty name. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 76. Frozen sample and partition unchanged; no training seal.
