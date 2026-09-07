# Java combined quality follow-up — batch 6

Positions76–90 of v14 Java queue1112, full prompt/reference read.
Six non-triviality holds and four static behavioral holds.1468 total holds
(1465 additive+3),3777 unique outside-sample inspections. Resume91.

| Position | ID | Finding |
| --- | --- | --- |
| 76 | exp-v1-java-repair-0035 | Criterion-positive: replaces in-place mutation with validated independent list construction; explicit String.trim semantics preserved. |
| 77 | exp-v1-java-generation-0051 | Criterion-positive: canonical signed fractions, negative-domain gcd and checked operations follow the explicitly required intermediate-overflow policy. |
| 78 | exp-v1-java-generation-0056 | Static hold: valid ordinary decimal operands surrounded by U+2003 whitespace are rejected because trim() leaves whitespace intact. |
| 79 | exp-v1-java-generation-0058 | Criterion-positive: record validation, full duplicate checks, stable replacement/removal and capped aggregation; isBlank and copied-list validation handle the observed Java pitfalls. |
| 80 | exp-v1-java-generation-0059 | Criterion-positive: validates the full list before actor short-circuit, then inclusive containment and stable highest-priority selection. |
| 81 | exp-v1-java-generation-0060 | Static hold: valid stationary point at Double.MAX_VALUE in a box spanning -Double.MAX_VALUE to Double.MAX_VALUE causes infinite width/offset and NaN reflection, then constructor failure. |
| 82 | exp-v1-java-repair-0037 | Non-triviality hold: direct length-to-codePointCount library substitution. |
| 83 | exp-v1-java-repair-0038 | Non-triviality hold: single loop-start literal 1-to-0 replacement; validation and delivery construction supplied. |
| 84 | exp-v1-java-repair-0039 | Non-triviality hold: direct inclusive-to-strict iteration-bound replacement. |
| 85 | exp-v1-java-repair-0040 | Non-triviality hold: replaces a single status equality with the explicitly prescribed 2xx range. |
| 86 | exp-v1-java-generation-0057 | Criterion-positive: complete list validation precedes blank-query/first-match short-circuits; exact first-match projection preserves immutable values. |
| 87 | exp-v1-java-generation-0061 | Criterion-positive insertion-ordered immutable registry; static hold: U+2003-only CaseRecord key passes trim().isEmpty(). |
| 88 | exp-v1-java-generation-0064 | Non-triviality hold: prescribed immutable field/getter hierarchy, one radius guard and literal formatting. |
| 89 | exp-v1-java-generation-0066 | Criterion-positive widened ratio/bar rendering; static hold: U+2003-only operator accepted despite nonblank requirement. Maximum-height capacity arithmetic is not separately adjudicated. |
| 90 | exp-v1-java-repair-0042 | Non-triviality hold: direct String identity-to-equals replacement. Static additional prompt/reference mismatch: U+2003-only input is accepted as OTHER despite all-whitespace rejection. |

No new execution. generation0060 uses point(MAX,0,0,0,0,0), box(-MAX,-1,MAX,1)
and seconds1. All public inputs and the unchanged expected output are finite;
max-min and raw-min overflow, so remainder becomes NaN. This is distinct from
asking an API to represent an inherently infinite final velocity.
Explicit intermediate-overflow errors in generation0051 are permitted by its
prompt; they are not classified as the unsupported-domain defect above.
Focused positives are not admission or full seven-criterion approval.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

