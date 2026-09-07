# Java combined quality follow-up — batch 23

Positions331–345 of v14 Java queue1112, full prompt/reference read.
Nine new non-triviality holds; six focused positives.
1626 total holds (1623 additive+3),4032 unique outside inspections. Resume346.

| Position | ID | Finding |
| --- | --- | --- |
| 331 | exp-v1-java-repair-0154 | Non-triviality hold: substitutes batchSize for the supplied loop stride and widens the end calculation. Very-large-array offset increment overflow remains an unexecuted concern outside this bounded review. |
| 332 | exp-v1-java-repair-0155 | Non-triviality hold: moves a direct null guard outside the supplied parse/default path and narrows the catch to NumberFormatException. |
| 333 | exp-v1-java-repair-0156 | Non-triviality hold: adds the explicitly missing reserved subtraction to the supplied checked arithmetic chain. |
| 334 | exp-v1-java-generation-0237 | Criterion-positive fixed-width inverse bit encoding uses unsigned byte masks and shifts to preserve all signed-int bit patterns with fresh storage. |
| 335 | exp-v1-java-generation-0238 | Non-triviality hold: direct quotient-plus-remainder ceiling formula with two guards. |
| 336 | exp-v1-java-generation-0239 | Non-triviality hold: scalar widened addition, int-range check and cast. |
| 337 | exp-v1-java-generation-0240 | Criterion-positive detached sequential update state preserves repeated-index dependence and caller ownership under validation/overflow failures. |
| 338 | exp-v1-java-repair-0157 | Non-triviality hold: substitutes startsWith for contains in a fully supplied filter. |
| 339 | exp-v1-java-repair-0158 | Criterion-positive binary-search partition repair preserves the first-not-less-than invariant under duplicate target values and empty inputs. |
| 340 | exp-v1-java-repair-0159 | Criterion-positive exception-safe scoped mutation restores absent versus present-null prior state while preserving changes to unrelated keys. |
| 341 | exp-v1-java-repair-0160 | Non-triviality hold: replaces a missing-key dereference with getOrDefault in a fully supplied template scanner; nested malformed delimiter interpretation is not newly adjudicated. |
| 342 | exp-v1-java-generation-0241 | Criterion-positive exact per-account aggregation and deterministic lexicographic tie selection separate identity grouping from maximum choice. |
| 343 | exp-v1-java-generation-0242 | Non-triviality hold: four literal character-to-string cases with a default and ordered array projection. |
| 344 | exp-v1-java-generation-0244 | Non-triviality hold: literal alias assignment and a second scalar value construction inside wrapper classes. |
| 345 | exp-v1-java-generation-0245 | Criterion-positive ordered grid overwrite with widened placement bounds and exact row serialization; large output allocations are not runtime-certified here. |

No new execution. Focused positives are not full seven-criterion approval or
admission. Resource-envelope concerns are not presented as executed failures.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
