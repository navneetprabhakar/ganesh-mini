# Java combined quality follow-up — batch 35

Positions511–525 of v14 Java queue1112, full prompt/reference read.
Seven new holds: six non-triviality and one static behavioral/contract finding.
1723 total holds (1720 additive+3),4212 unique outside inspections. Resume526.

| Position | ID | Finding |
| --- | --- | --- |
| 511 | exp-v1-java-repair-0242 | Criterion-positive composite identity repair distinguishes rows differing in the third field while preserving first occurrence and deep array ownership. |
| 512 | exp-v1-java-repair-0244 | Non-triviality hold: substitutes the directly specified doubled-quote replacement literal in an otherwise complete quoting wrapper. |
| 513 | exp-v1-java-generation-0367 | Static contract hold: append checks duplicates only against the new passage, allowing preexisting duplicate IDs or permit codes in history despite its duplicate-rejection language. |
| 514 | exp-v1-java-generation-0370 | Criterion-positive lexical cursor and offset handling distinguish identifiers, multi-character operators and malformed input without mutation. Java Character whitespace covers the reopened U+2003 criterion; broader Unicode property interpretation is not independently certified. |
| 515 | exp-v1-java-generation-0371 | Non-triviality hold: direct ordered validation table transcribes five supplied predicates and literal error messages. |
| 516 | exp-v1-java-repair-0245 | Non-triviality hold: changes the directly specified Running return literal. |
| 517 | exp-v1-java-repair-0246 | Non-triviality hold: replaces the supplied Character.isDigit predicate with the explicitly requested ASCII character range. |
| 518 | exp-v1-java-repair-0247 | Non-triviality hold: changes the directly specified port maximum constant from65536 to65535. |
| 519 | exp-v1-java-repair-0248 | Criterion-positive mutable Date ownership repair preserves Date values and isolates source/returned date mutations while retaining ordinary references as required. |
| 520 | exp-v1-java-generation-0369 | Criterion-positive strict delimiter/numeric ledger codec and immutable ordered map operations distinguish malformed, absent and empty-token states. Leading-zero normalization is not invented. |
| 521 | exp-v1-java-generation-0372 | Criterion-positive two-way array defensive copying and immutable catalog updates preserve document payload ownership; map-key/object-ID equality is not imposed beyond the prompt. |
| 522 | exp-v1-java-generation-0373 | Non-triviality hold: single scalar getter/setter/reset wrapped in prescribed inheritance boilerplate has no substantive state machine or ownership problem. |
| 523 | exp-v1-java-generation-0374 | Criterion-positive runtime annotation discovery filters declared public static methods rather than hardcoding the result, preserving deterministic immutable output. |
| 524 | exp-v1-java-generation-0376 | Criterion-positive zero-safe dynamic array growth, shifting/removal, null-preserving snapshots and structural-version iterator checks implement a substantive collection. Extreme capacity/version exhaustion is unexecuted and uncertified. |
| 525 | exp-v1-java-generation-0378 | Criterion-positive catalog identity rules, validated bulk deletion and widened pagination produce independent immutable search/page snapshots. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
