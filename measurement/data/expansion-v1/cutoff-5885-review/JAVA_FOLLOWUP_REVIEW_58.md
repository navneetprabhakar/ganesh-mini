# Java combined quality follow-up — batch 58

Positions856–870 of v14 Java queue1112, full prompt/reference read.
Resumed under Navneet's2026-09-07 approval of review completion and versioned recovery.
Eight new holds: four non-triviality and four static behavioral/contract findings.
1898 total holds (1895 additive+3),4557 unique outside inspections. Resume871.
The3987 unheld upper bound is not admission; approved recovery is still pending.

| Position | ID | Finding |
| --- | --- | --- |
| 856 | exp-v1-java-generation-0612 | Criterion-positive defensive byte-array ownership on input, previous-value return and load; delete distinguishes a present null from absence. |
| 857 | exp-v1-java-repair-0405 | Non-triviality hold: removes minus one from the supplied ticket-loop endpoint; validation and close/count behavior are already supplied. |
| 858 | exp-v1-java-repair-0406 | Criterion-positive even-median indexing restores the two central positions while retaining widened addition and detached sorting. |
| 859 | exp-v1-java-repair-0407 | Criterion-positive type-directed conversion replaces an invalid String-to-List cast, preserving ordered normalization across both accepted input forms. |
| 860 | exp-v1-java-repair-0408 | Non-triviality hold: replaces Integer.reverse and narrowing cast with the direct Long.reverse library call. |
| 861 | exp-v1-java-generation-0615 | Criterion-positive discount-before-tax composition and quotient/remainder basis-point calculation avoid unnecessary intermediate overflow while preserving exact final arithmetic. |
| 862 | exp-v1-java-generation-0618 | Criterion-positive stateful token histogram tracks boundaries with Character.isWhitespace, exact count addition and detached ordered snapshots/reset. |
| 863 | exp-v1-java-repair-0409 | Static hold: allowedKeys.contains(null) can throw for valid null-free immutable sets; it also rejects null set elements although the prompt only prohibits null arguments. No new execution. |
| 864 | exp-v1-java-repair-0410 | Criterion-positive clockwise coordinate mapping repair preserves rectangular shape conversion and independent rows for every supported rotation. |
| 865 | exp-v1-java-repair-0411 | Non-triviality hold: swaps two prescribed standard-library comparator priorities in an otherwise complete sorting wrapper. |
| 866 | exp-v1-java-repair-0412 | Criterion-positive canonical-decimal conversion avoids binary floating-point expansion before HALF_UP rounding, preserving the explicit2.675 example. |
| 867 | exp-v1-java-generation-0616 | Static contract hold: unspecified-width decimal counts are restricted to long; e.g.9223372036854775808|9223372036854775808 satisfies stated grammar/order but is rejected. Count-domain/getter representation needs clarification. |
| 868 | exp-v1-java-generation-0617 | Static hold: groups.contains(null) can throw for valid null-free immutable sets before selection. No separate candidate execution. |
| 869 | exp-v1-java-generation-0620 | Non-triviality hold: scalar min/max canonicalization, prescribed BigInteger product and independent boolean setter. |
| 870 | exp-v1-java-generation-0622 | Static hold: U+2003-only builder strings pass required nonblank-after-trimming validation. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission. Original holds retained.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

