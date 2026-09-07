# Java combined quality follow-up — batch 18

Positions256–270 of v14 Java queue1112, full prompt/reference read.
Eight new holds: seven non-triviality and one executed behavioral finding.
1584 total holds (1581 additive+3),3957 unique outside inspections. Resume271.

| Position | ID | Finding |
| --- | --- | --- |
| 256 | exp-v1-java-repair-0118 | Criterion-positive ownership repair clones the replacement instead of returning an alias through the irrelevant original parameter. |
| 257 | exp-v1-java-repair-0120 | Criterion-positive nested ownership repair removes the equal-width alias path, preserving fresh rows across truncation, padding and unchanged dimensions. |
| 258 | exp-v1-java-generation-0181 | Non-triviality hold: three literal enum lookups and a constant fresh int array. |
| 259 | exp-v1-java-generation-0182 | Criterion-positive maximum-subarray recurrence with positive-only result, earliest-start/end tie handling and widened sums; zero prefix is retained to preserve earliest ties. |
| 260 | exp-v1-java-generation-0183 | Criterion-positive exact binary framing, unsigned length/level and strict malformed-UTF8 decoding with fresh output. No additional encode-time surrogate rejection or roundtrip premise is imposed. |
| 261 | exp-v1-java-generation-0184 | Non-triviality hold: directly transcribes three prescribed divisibility clauses with a positive-input guard. |
| 262 | exp-v1-java-generation-0186 | Criterion-positive invocation-local memoization and constant-space rolling recurrence agree with recursive bases across the bounded domain; no unexecuted runtime claim for n=40. |
| 263 | exp-v1-java-repair-0121 | Non-triviality hold: replaces a supplied unsafe removal loop with the exact List.removeIf API explicitly mandated by the prompt. |
| 264 | exp-v1-java-repair-0122 | Non-triviality hold: changes OR to AND in the supplied two-flag disclosure predicate. |
| 265 | exp-v1-java-repair-0123 | Non-triviality hold: replaces boxed Integer identity comparison with equals in the complete adjacent-run counter. |
| 266 | exp-v1-java-repair-0124 | Non-triviality hold: removes minus one from the supplied END branch, matching the literal boundary definition. |
| 267 | exp-v1-java-generation-0187 | Non-triviality hold: direct three-character path-prefix predicate and indexed literal formatting; no path parsing beyond the fully supplied rule. |
| 268 | exp-v1-java-generation-0190 | Executed behavioral hold: a Reading with NaN temperature produces no temperature alert although only the stated finite interval is normal. Static contract/format issue: nonblank ID a|b is accepted and encode emits six fields, which decode rejects; the format supplies no ID delimiter policy. |
| 269 | exp-v1-java-generation-0191 | Criterion-positive immutable batch transitions preserve pending/completed order and duplicates, terminal behavior and Unicode-aware blank checks. |
| 270 | exp-v1-java-generation-0192 | Criterion-positive full board validation, independent row/column copies and explicit winning-line precedence; cell-null exception rule is not expanded to an unstated outer-board-null rule. |

java_0190_nan_alert_probe.java and matching -result.json preserve the original
record/reference, hashes and sandbox output. Pinned Java21.0.11, network disabled,
1CPU,512MiB,64PIDs,60-second timeout: compile/run [0,1],2640ms,no timeout.
Only the NaN alert counterexample was executed; the ID delimiter issue is static.
Focused positives are not full seven-criterion approval or training admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
