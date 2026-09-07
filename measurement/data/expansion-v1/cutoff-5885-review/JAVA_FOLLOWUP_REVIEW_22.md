# Java combined quality follow-up — batch 22

Positions316–330 of v14 Java queue1112, full prompt/reference read.
Eleven new holds: ten non-triviality and one primary static contract finding.
1617 total holds (1614 additive+3),4017 unique outside inspections. Resume331.

| Position | ID | Finding |
| --- | --- | --- |
| 316 | exp-v1-java-generation-0223 | Criterion-positive ordered upsert/delete/reinsert semantics clone each array separately, including a shared input array used for different keys. Returned value arrays are not required to be deeply immutable. |
| 317 | exp-v1-java-generation-0224 | Non-triviality hold: sortedness validation followed by direct TreeSet union and array projection, without a coupled merge invariant or required linear-time algorithm. |
| 318 | exp-v1-java-generation-0225 | Criterion-positive duplicate-ID validation before independent aggregate reporting with exact long sum and frozen sorted failure IDs. |
| 319 | exp-v1-java-generation-0227 | Criterion-positive exact separator count and ASCII numeric grammar preserve empty content and unnormalized label/content while bounding the code. |
| 320 | exp-v1-java-generation-0228 | Non-triviality hold: direct fixed range-condition truth table and literal formatting for null/equal/inclusive endpoints. |
| 321 | exp-v1-java-repair-0150 | Non-triviality hold: substitutes RoundingMode.UNNECESSARY for HALF_UP in an otherwise complete exact decimal conversion. |
| 322 | exp-v1-java-repair-0151 | Non-triviality hold: substitutes Integer.compareUnsigned for Integer.compare. |
| 323 | exp-v1-java-repair-0152 | Non-triviality hold: adds Locale.ROOT to the supplied lowercase call; prefix parsing and output preservation are already supplied. |
| 324 | exp-v1-java-generation-0226 | Non-triviality hold: fixed three-field validation messages and scalar age rule. Static contract mismatch: 01 is a positive base-10 integer not prohibited by the prompt, but the reference rejects leading zeros. |
| 325 | exp-v1-java-generation-0229 | Non-triviality hold: trim/regex/lowercase wrapper chain. Static behavior defect: trim removes edge U+0000, which is not one of the six explicitly enumerated ASCII whitespace characters and should be preserved. |
| 326 | exp-v1-java-generation-0230 | Non-triviality hold: direct adjacent-order validation and elementary first qualifying bound scan. |
| 327 | exp-v1-java-generation-0231 | Non-triviality hold: scalar checked summation with nonnegative guards. |
| 328 | exp-v1-java-generation-0232 | Non-triviality hold: direct three-way adjacent comparison counters and literal result array. |
| 329 | exp-v1-java-generation-0233 | Criterion-positive sequential greedy load assignment uses updated loads and strict comparison to preserve the lowest-index tie invariant, with checked addition. |
| 330 | exp-v1-java-generation-0234 | Criterion-positive staged ordered updates and exact arithmetic; static contract hold: initial [-1] with update [0,1] is rejected although the prompt constrains each resulting updated value, not initial values. |

No new execution. Static counterexamples distinguish explicit ASCII whitespace,
canonical decimal spelling and initial-state constraints from unstated assumptions.
Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
