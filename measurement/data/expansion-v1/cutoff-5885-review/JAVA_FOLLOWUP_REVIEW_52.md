# Java combined quality follow-up — batch 52

Positions766–780 of v14 Java queue1112, full prompt/reference read.
Seven new holds: two non-triviality and five static behavioral/contract findings.
1846 total holds (1843 additive+3),4467 unique outside inspections. Resume781.

| Position | ID | Finding |
| --- | --- | --- |
| 766 | exp-v1-java-generation-0547 | Criterion-positive immutable ledger updates, distinct sorted queries and deterministic frequency ties preserve old ledgers and mutable-result independence. |
| 767 | exp-v1-java-generation-0548 | Criterion-positive immutable store transitions distinguish automatic hundred-entry commits from explicit pending-only commits and isolate sorted query output. |
| 768 | exp-v1-java-generation-0552 | Criterion-positive immutable panel state and copied links preserve exactly-three constraints, toggling and empty instruction-line rendering. |
| 769 | exp-v1-java-repair-0365 | Non-triviality hold: changes the supplied endpoint predicate from >=length to >length around a regionMatches wrapper. |
| 770 | exp-v1-java-repair-0366 | Criterion-positive iterator-owned in-place removal preserves traversal validity and validates all nulls before any mutation. |
| 771 | exp-v1-java-repair-0367 | Criterion-positive copy-before-update repairs immutable registry ownership rather than mutating the original before copying. |
| 772 | exp-v1-java-repair-0368 | Criterion-positive supplied-field set value equality restores equality/hash consistency and omitted-versus-explicit-null semantics. |
| 773 | exp-v1-java-generation-0550 | Criterion-positive nested immutable directed routes and independently unique cargo lists preserve defensive access and deterministic network queries. |
| 774 | exp-v1-java-generation-0553 | Non-triviality hold: inheritance wrapper directly implements the two prescribed scalar geometry formulas and independent finite/nonnegative guards. |
| 775 | exp-v1-java-repair-0369 | Criterion-positive remainder allocation fixes balanced contiguous coverage so no extra task is assigned when the remainder is zero. |
| 776 | exp-v1-java-repair-0370 | Static hold: an out-of-order prefix returns false before validating later null/unknown tags; e.g. @return,@param,null bypasses required rejection. Surrounding U+2003 whitespace is also not trimmed. |
| 777 | exp-v1-java-repair-0371 | Static arithmetic/contract hold: valid production can exceed int queue capacity, e.g. {MAX_VALUE,MAX_VALUE}, consumption1; reference throws ArithmeticException although the stated rejection conditions do not exclude it and maximumQueued has no representable int result. Output-domain contract needs resolution. |
| 778 | exp-v1-java-generation-0554 | Static hold: U+2003-only contestant passes blank validation. points() also computes wins*3+draws in int without a stated bound (not executed). |
| 779 | exp-v1-java-generation-0556 | Static hold: U+2003-only title, label or basePath passes blank validation. Reference additionally trims basePath although only trailing slash removal is specified. |
| 780 | exp-v1-java-generation-0557 | Static hold: U+2003-only channel name passes blank validation; find(-1) returns null instead of rejecting a negative ID. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

