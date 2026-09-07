# Java combined quality follow-up — batch 5

Positions61–75 of v14 Java queue1112, full prompt/reference read.
Seven non-triviality holds plus one static whitespace hold.1458 total holds
(1455 additive+3);3762 unique outside inspections. Resume76.

| Position | ID | Finding |
| --- | --- | --- |
| 61 | exp-v1-java-repair-0026 | Non-triviality hold: direct zero-based loop start and index-based separator guards implement a prescribed join. |
| 62 | exp-v1-java-repair-0027 | Criterion-positive: copies before sorting to repair caller ownership and distinct empty-array behavior. |
| 63 | exp-v1-java-repair-0028 | Non-triviality hold: one regex metacharacter escape fixes the supplied literal-pipe split. |
| 64 | exp-v1-java-generation-0043 | Criterion-positive: count-driven binary parsing validates every entry and trailing bytes before returning marker presence. |
| 65 | exp-v1-java-generation-0044 | Criterion-positive: record boundaries, nullable rows/cells and CSV quote-doubling preserve embedded delimiters. |
| 66 | exp-v1-java-generation-0045 | Static hold: surrounding whitespace removal uses trim(), so U+2003 around the directory key prevents recognition instead of setting it. |
| 67 | exp-v1-java-generation-0046 | Criterion-positive: mutable source fields, Date and token copies are isolated at transform and getter boundaries. |
| 68 | exp-v1-java-generation-0048 | Non-triviality hold: direct two-formula temperature conversion with literal scale guards. Static additional defect: finite MaxValue Fahrenheit overflows the multiply-before-divide intermediate although the Celsius result is representable. |
| 69 | exp-v1-java-repair-0029 | Non-triviality hold: substitutes the directly prescribed RUNTIME annotation-retention enum for CLASS. |
| 70 | exp-v1-java-repair-0032 | Non-triviality hold: strict-to-inclusive comparator replacement to choose the last maximum. |
| 71 | exp-v1-java-generation-0049 | Non-triviality hold: literal catalog/code lookup table with two default labels. |
| 72 | exp-v1-java-generation-0052 | Criterion-positive: delimiter-safe manifest records and separately ordered copied lists/map entries preserve duplicates and ownership. |
| 73 | exp-v1-java-generation-0054 | Non-triviality hold: two direct boolean-to-enum setters with null guards. |
| 74 | exp-v1-java-repair-0033 | Criterion-positive: replaces shared scalar accumulation with independent exact per-channel state. |
| 75 | exp-v1-java-repair-0034 | Criterion-positive: escape-aware cursor advancement validates and preserves existing escapes without double encoding. |

No new execution. generation0045 counterexample: a line with key
\\u2003directory\\u2003 and value chosen should recognize the key after the
required whitespace removal, but trim() leaves it unknown. generation0048
Double.MAX_VALUE Fahrenheit has a finite mathematical Celsius result near
9.99e307, but the intermediate multiplication produces infinity.
Focused positives are not all-seven-criterion passes or training admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

