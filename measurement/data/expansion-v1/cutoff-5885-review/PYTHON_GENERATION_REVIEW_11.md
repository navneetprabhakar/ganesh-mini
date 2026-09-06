# Python generation review, batch 11

Positions 151–165 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; six reproduced holds.
551 additive plus historical three = 554 holds; 1,398 unique outside-sample
inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 151 | 0168 | Cursor aliases list and returns original entries; ordinary remove/iteration agree. External insertion/deletion semantics are unspecified and pending; no new hold. |
| 152 | 0169 | Four direct arithmetic operations and stateless validation agree. Conflicting-invalid-argument priority unspecified; no new hold. |
| 153 | 0170 | Hold: explicitly present finish=None accepted despite when-present date requirement. Normal normalization/order/tag copying agree; datetime subclass compatibility pending. |
| 154 | 0171 | Hold: valid 4301-digit Lucas target hits pinned decimal conversion limit; exact threshold oracle completes. |
| 155 | 0172 | Exact class identity, duplicate stability and insertion order agree. Non-string lookup domain unspecified; no new hold. |
| 156 | 0173 | Ordinary ASCII residue validation, enumerated whitespace and rounding agree. Unicode uppercase compatibility characters remain an interpretation issue; no new hold. |
| 157 | 0174 | Tiling, centering, inclusive unknown fraction, duplicate ordering and ordinary regex handling agree. Pair container breadth and invalid replacement on empty output remain pending; no new hold. |
| 158 | 0177 | Hold: comma-containing valid text corrupts CSV columns; equal finite durations overflow average. Snapshot large-integer precision remains additional concern. |
| 159 | 0180 | Full validation before exact reachable-state evaluation and signed truncation agree. Exponential enumeration/resource envelope remains pending; no new hold. |
| 160 | 0175 | Hold: valid digit run with leading zeroes rejected by int conversion limit. Ordinary ASCII/apostrophe tokens, stop words and lexicons agree. |
| 161 | 0176 | Materialization, ordinary token tags, escaping and line preservation agree. Non-ASCII letters classified as punctuation despite narrower wording remain pending; no new hold. |
| 162 | 0179 | Full ordinary validation, region/action sorting and no-op handling agree. Extra state fields and duplicate custom-mapping rule semantics pending; no new hold. |
| 163 | 0181 | Hold: 3,000-character palindrome hits linear recursion depth. Numeric span and ordinary casefold behavior agree; expanded combining-mark normalization pending. |
| 164 | 0182 | Hold: accepted positive starting number cannot be formatted as ID beyond decimal limit. Ordinary deep copies/ordering agree; exceptional deepcopy atomicity pending. |
| 165 | 0186 | Threshold validation, channel checks, clamped neighbor contrast and independent integer mark rows agree. Row-container breadth pending; no new hold. |

Six pinned Python 3.11.15 probes, network disabled/resource limited, all exit
1 without timeout. Holds remain review items, not final rejection decisions.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0170 | expedition_explicit_finish_probe.py / expedition-explicit-finish-result.json | 407 | ValueError not raised for explicitly supplied None finish. |
| 0171 | lucas_digit_limit_probe.py / lucas-digit-limit-result.json | 2030 | ValueError converting Lucas term beyond 4300 digits. |
| 0177 | timing_csv_fields_probe.py / timing-csv-fields-result.json | 403 | Seven CSV columns instead of six; average inf instead of 1e308. |
| 0175 | phrase_long_decimal_probe.py / phrase-long-decimal-result.json | 414 | 5001-character representation of seven rejected. |
| 0181 | palindrome_recursion_probe.py / palindrome-recursion-result.json | 484 | RecursionError on 3000 identical letters. |
| 0182 | allocation_large_start_probe.py / allocation-large-start-result.json | 406 | ID integer formatting ValueError. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 166. Original candidates/tests/sample/partition unchanged.
