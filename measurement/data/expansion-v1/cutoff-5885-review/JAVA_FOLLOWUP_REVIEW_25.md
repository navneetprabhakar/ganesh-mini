# Java combined quality follow-up — batch 25

Positions361–375 of v14 Java queue1112, full prompt/reference read.
Nine new holds: six non-triviality and three primary static behavioral/contract findings.
1645 total holds (1642 additive+3),4062 unique outside inspections. Resume376.

| Position | ID | Finding |
| --- | --- | --- |
| 361 | exp-v1-java-generation-0256 | Criterion-positive option ownership and per-question selection bounds; static hold: U+2003-only prompts/options pass blank rejection. |
| 362 | exp-v1-java-generation-0257 | Criterion-positive duplicate-checked ordered replacement; static hold: U+2003-only name/channel pass blank rejection. Prompt also conflicts between missing-ID rejection and returning a list for empty input. |
| 363 | exp-v1-java-generation-0258 | Criterion-positive complete existing-state validation and detached insertion-order-preserving update/append. |
| 364 | exp-v1-java-repair-0169 | Non-triviality hold: adds one missing requireNonNull guard to a fully supplied snapshot routine. |
| 365 | exp-v1-java-repair-0170 | Non-triviality hold: flips the supplied visibility predicate. Static behavior defect: U+2003-only operation name passes blank rejection. |
| 366 | exp-v1-java-repair-0171 | Non-triviality hold: selects the directly specified anonymous-key prefix instead of always calling uriValue. Static behavior defect: U+2003-only URI/anonymous identifier passes nonblank validation. |
| 367 | exp-v1-java-repair-0172 | Non-triviality hold: substitutes channel for payload in the supplied membership test. Static behavior defect: U+2003-only channel/payload pass nonblank validation. |
| 368 | exp-v1-java-generation-0260 | Non-triviality hold: direct nested formatting loops transcribe supplied leading-space, row-count and separator formulas. |
| 369 | exp-v1-java-generation-0261 | Criterion-positive multi-shape numeric parsing and rectangular validation; static hold: U+2003-separated numbers and U+2003-only grid input violate the stated whitespace handling because trim/default regex whitespace do not recognize it. |
| 370 | exp-v1-java-generation-0262 | Criterion-positive mutable-object ownership boundary distinguishes missing versus null-mapped assets and copies current fields without imposing key/ID equality. |
| 371 | exp-v1-java-generation-0264 | Criterion-positive exact grouped aggregation and first-encounter ordering create independent immutable stats; key format explicitly fixes the enum prefix. |
| 372 | exp-v1-java-repair-0173 | Criterion-positive shared-endpoint intersection repair enforces both bounds' inclusivity and handles touching/empty intersections without overflow arithmetic. |
| 373 | exp-v1-java-repair-0174 | Criterion-positive mutable-element ownership repair renumbers detached Slot copies without modifying original objects, including late validation failures. |
| 374 | exp-v1-java-repair-0175 | Criterion-positive class-initialization publication preserves singleton identity and shared synchronized counter state across concurrent callers. |
| 375 | exp-v1-java-repair-0176 | Non-triviality hold: removes the directly prohibited READY alternative from the supplied PAUSE transition. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
