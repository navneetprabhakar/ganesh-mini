# Java combined quality follow-up — batch 28

Positions406–420 of v14 Java queue1112, full prompt/reference read.
Seven new holds: four non-triviality and three static behavioral findings.
1668 total holds (1665 additive+3),4107 unique outside inspections. Resume421.

| Position | ID | Finding |
| --- | --- | --- |
| 406 | exp-v1-java-generation-0288 | Static hold: U+2003-only task/dependency names pass nonblank validation. Complete round-based dependency scheduling and cycle detection are otherwise criterion-positive. |
| 407 | exp-v1-java-generation-0289 | Criterion-positive directory state combines case-insensitive uniqueness, non-reused IDs across ordinary deletion, sentinel lookup and immutable ordered snapshots. ID exhaustion is not executed or certified; prompt lookup-empty precedence is not strengthened. |
| 408 | exp-v1-java-generation-0291 | Criterion-positive ordered execution isolates RuntimeException failures, preserves null messages and propagates Error while snapshotting reports. No callback mutation/reentrancy contract is invented. |
| 409 | exp-v1-java-generation-0293 | Static hold: U+2003-only badge, secret and display name pass nonblank-after-trimming validation. Lockout/reset and immutable secret-free views are otherwise substantive. |
| 410 | exp-v1-java-repair-0193 | Static hold: U+2003-only Delta keys pass nonblank validation. Materialized-base snapshot repair preserves ordered current state; int wraparound is explicitly required, not a defect. |
| 411 | exp-v1-java-repair-0194 | Non-triviality hold: substitutes the explicitly specified subtraction for addition after complete supplied validation. |
| 412 | exp-v1-java-repair-0195 | Criterion-positive eager singleton identity repair shares synchronized mutable counter state across returned references, consistent with repair0175. |
| 413 | exp-v1-java-repair-0196 | Non-triviality hold: changes a supplied separator index threshold from >1 to >0. Tokens explicitly require trim/nonempty, not broader blank handling. |
| 414 | exp-v1-java-generation-0295 | Non-triviality hold: immutable DTO boilerplate and direct field-for-field conversions add no substantive transformation beyond the prescribed mapping. |
| 415 | exp-v1-java-generation-0296 | Criterion-positive staged replacement and detached snapshots preserve prior state on malformed input and prevent list aliases. |
| 416 | exp-v1-java-generation-0297 | Criterion-positive reservation/cancellation state conserves per-section capacity, avoids duplicate cancellation and snapshots ordered history. Unbounded ID exhaustion is not executed or certified. |
| 417 | exp-v1-java-generation-0298 | Criterion-positive validated keyed add/update distinctions and sorted detached room queries preserve immutable exhibit ownership. Constructor validation is not independently imposed beyond mutation validation. |
| 418 | exp-v1-java-generation-0299 | Criterion-positive exclusive builder dispatch, two-sided defensive copies and validate-before-store commit isolate malformed returned data without retaining aliases. |
| 419 | exp-v1-java-generation-0300 | Criterion-positive stable merge-sort implements half-open subrange isolation and overflow-safe comparisons without library sorting. |
| 420 | exp-v1-java-repair-0197 | Non-triviality hold: replaces the directly forbidden missing-account insertion with the explicitly prescribed false return in an otherwise complete withdrawal routine. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
