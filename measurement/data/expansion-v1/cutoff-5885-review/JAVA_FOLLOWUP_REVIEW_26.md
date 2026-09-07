# Java combined quality follow-up — batch 26

Positions376–390 of v14 Java queue1112, full prompt/reference read.
Eight new holds: seven non-triviality and one static behavioral finding.
1653 total holds (1650 additive+3),4077 unique outside inspections. Resume391.

| Position | ID | Finding |
| --- | --- | --- |
| 376 | exp-v1-java-generation-0259 | Non-triviality hold: five independent filters directly transcribe the specified scalar comparisons and substring predicates; no substantive shared state or algorithm. |
| 377 | exp-v1-java-generation-0265 | Criterion-positive ordered escaping protects the backslash/pipe serialization boundary after null substitution and redaction. |
| 378 | exp-v1-java-generation-0266 | Criterion-positive inclusive modular wrap uses long arithmetic for the MAX_VALUE-sized position domain and negative displacement without overflow. |
| 379 | exp-v1-java-generation-0267 | Static hold: U+2003-only labels/groups pass trim-based nonblank validation. Nested ownership and per-group uniqueness are otherwise criterion-positive. |
| 380 | exp-v1-java-generation-0269 | Criterion-positive full validation, stable duplicate-ID sorting and widened pagination bounds preserve detached mutable result ownership. |
| 381 | exp-v1-java-repair-0177 | Non-triviality hold: changes the supplied prefix-copy loop from <= to < with validation and copying already implemented. |
| 382 | exp-v1-java-repair-0178 | Criterion-positive frame cursor repair accounts for both the unsigned length header and payload, maintaining truncation and zero-length rejection. |
| 383 | exp-v1-java-repair-0179 | Non-triviality hold: substitutes the directly specified UTF_8 charset for UTF_16BE in a supplied byte-length wrapper. |
| 384 | exp-v1-java-repair-0180 | Non-triviality hold: swaps the reversed result operands in an already validated long-weight comparison. |
| 385 | exp-v1-java-generation-0272 | Criterion-positive fully validated ordered edits distinguish removal, update and recreation while returning an independent unmodifiable map. |
| 386 | exp-v1-java-generation-0273 | Criterion-positive ordered override semantics retain existing positions, append new keys and isolate immutable output after complete validation. |
| 387 | exp-v1-java-generation-0275 | Non-triviality hold: direct terminal-page/finish predicate and one-step increment transcribe the stated branch table. |
| 388 | exp-v1-java-generation-0276 | Criterion-positive complete forest validation and ancestor traversal reject existing and introduced cycles before detached reparenting. Quadratic validation is not an executed resource failure. |
| 389 | exp-v1-java-repair-0181 | Non-triviality hold: adds the directly specified contains("--") rejection to a fully supplied route validator. |
| 390 | exp-v1-java-repair-0182 | Non-triviality hold: replaces division with a single multiplyExact library call for the specified unit conversion. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
