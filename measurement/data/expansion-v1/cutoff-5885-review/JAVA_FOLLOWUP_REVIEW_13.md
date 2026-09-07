# Java combined quality follow-up — batch 13

Positions181–195 of v14 Java queue1112, full prompt/reference read.
Ten new holds: eight non-triviality and two static behavioral primary findings.
Some elementary records also contain documented static behavioral/contract defects.
1540 total holds (1537 additive+3),3882 unique outside inspections. Resume196.

| Position | ID | Finding |
| --- | --- | --- |
| 181 | exp-v1-java-generation-0127 | Non-triviality hold: direct unit-factor arithmetic and enum literals. Static behavior defect: converting Double.MAX_VALUE from KIBIBYTE to KIBIBYTE overflows the intermediate multiplication to infinity despite required identity conversion. |
| 182 | exp-v1-java-generation-0128 | Non-triviality hold: elementary decrement-and-delimiter loop. Static contract issue: explicitly valid Integer.MAX_VALUE requires a String exceeding Java's int-indexed String length; the output contract is unrepresentable, not merely a slow loop. |
| 183 | exp-v1-java-generation-0129 | Non-triviality hold: three literal map projections and placeholder formatting. Static behavior defect: U+2003-only values render as text rather than the required blank-value placeholder. |
| 184 | exp-v1-java-generation-0130 | Non-triviality hold: directly applies the three prescribed Character predicates to the prescribed code-point traversal and buckets; category policy and traversal are fully supplied. No surrogate-handling failure is alleged. |
| 185 | exp-v1-java-generation-0131 | Criterion-positive ordered callback pipeline and list ownership; static hold: Workflow(List.of()) throws from contains(null), rejecting the explicitly valid empty-stage workflow. |
| 186 | exp-v1-java-generation-0132 | Criterion-positive byte-format decoder with unsigned fields, remaining-capacity run bounds, exact fill, trailing-data rejection and fresh output. |
| 187 | exp-v1-java-repair-0085 | Criterion-positive state-source repair validates funds against sequential staged balances, preserving earlier-transfer visibility and failure isolation. |
| 188 | exp-v1-java-repair-0087 | Non-triviality hold: changes the final offset argument to offset+count; bounds, slicing and both defensive copies are already supplied. |
| 189 | exp-v1-java-repair-0088 | Non-triviality hold: selects the already supplied LowerNormalizer subclass in the true branch. Static behavior defect: U+2003-only input is not emptied despite the all-whitespace requirement. |
| 190 | exp-v1-java-generation-0133 | Criterion-positive independent channel eviction, reset state and ordered immutable snapshots with default initialization; add validates message fields as explicitly required. |
| 191 | exp-v1-java-generation-0134 | Criterion-positive strict calendar parsing, unsigned decimal grammar and bounded long conversion, fresh mutable output objects and immutable date values. No extra year restriction beyond the stated formatter pattern is imposed. |
| 192 | exp-v1-java-generation-0135 | Criterion-positive full nested validation before insertion, duplicate rejection, numeric boxed-ID equality and immutable insertion-ordered snapshots. |
| 193 | exp-v1-java-generation-0136 | Criterion-positive synchronized independent configuration state and defensive snapshots; static hold: U+2003-only authority/recipient are accepted as valid despite the non-whitespace requirement. |
| 194 | exp-v1-java-repair-0089 | Non-triviality hold: replaces a literal result branch with the Math.min formula explicitly supplied in the prompt. |
| 195 | exp-v1-java-repair-0090 | Non-triviality hold: moves the scalar accumulator initialization outside an otherwise complete running-total loop; normal int overflow is explicitly permitted and is not a behavioral defect. |

No new execution. List.of null-query failure is static propagation of previously
executed Java counterexamples, not an executed result for generation0131.
The maximum countdown output exceeds String representability; it was not attempted.
Unicode findings apply to blank/whitespace contracts, not explicit trim-nonempty
contracts. Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
