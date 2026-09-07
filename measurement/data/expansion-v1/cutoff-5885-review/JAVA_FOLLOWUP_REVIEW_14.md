# Java combined quality follow-up — batch 14

Positions196–210 of v14 Java queue1112, full prompt/reference read.
Nine new holds: four non-triviality and five static behavioral findings.
1549 total holds (1546 additive+3),3897 unique outside inspections. Resume211.

| Position | ID | Finding |
| --- | --- | --- |
| 196 | exp-v1-java-repair-0091 | Non-triviality hold: adds the standard negative split-limit argument to the already supplied escaped delimiter call. |
| 197 | exp-v1-java-generation-0138 | Criterion-positive full nested validation, filtering, ordered duplicate-preserving recipes and deep snapshots; static hold: valid Set.of enabled modules and List.of recipe lists are queried with contains(null), which may throw rather than accept valid inputs. |
| 198 | exp-v1-java-generation-0140 | Criterion-positive staged replacement and exact integer accumulation; static hold: two Double.MAX_VALUE decimals overflow the sum so decimalAverage returns infinity instead of the representable Double.MAX_VALUE average. Integer overflow policy is explicit and not newly held. |
| 199 | exp-v1-java-generation-0141 | Criterion-positive atomic checked pocket transfers and explicitly checked growth multiplication; static hold: U+2003-only key/name pass required nonblank registration validation. |
| 200 | exp-v1-java-generation-0142 | Criterion-positive defensive copies on storage, lookup and each snapshot element with insertion order. Admission validation is explicitly assigned to add; no extra constructor rejection rule imposed. |
| 201 | exp-v1-java-generation-0143 | Criterion-positive position-preserving atomic rename and exact-name collision handling; static hold: U+2003-only names pass required nonblank-after-trimming validation. |
| 202 | exp-v1-java-generation-0144 | Criterion-positive detached report iteration, runtime-exception sentinels and ordered snapshots; static hold: U+2003-only registration name passes nonblank validation. Paths use Character.isWhitespace; callback reentrant mutation interpretation is not newly adjudicated. |
| 203 | exp-v1-java-repair-0093 | Criterion-positive terminal callback control flow: return after success prevents failure fallthrough while preserving loader-exception continuation and exactly one selected callback. |
| 204 | exp-v1-java-repair-0094 | Criterion-positive ownership repair detaches work before set/remove/sort, supporting mutable, fixed-size and immutable inputs without changing caller positions. |
| 205 | exp-v1-java-repair-0095 | Non-triviality hold: replaces the null branch with a literal empty array; validation, constructor copy and getter copies are already complete. |
| 206 | exp-v1-java-generation-0139 | Criterion-positive length-prefixed UTF-16 codec with checked numeric accumulation, remaining-length bounds, exact delimiters, asset order and immutable nested ownership. |
| 207 | exp-v1-java-generation-0145 | Non-triviality hold: direct six-literal switch and counter increments with prescribed checked arithmetic. |
| 208 | exp-v1-java-generation-0146 | Non-triviality hold: straightforward first-UTF-16-character membership filter with supplied order/duplicate policy and element validation. |
| 209 | exp-v1-java-generation-0147 | Criterion-positive common monitor linearizability across registry operations, array copies at both boundaries and checked revision replacement semantics. |
| 210 | exp-v1-java-generation-0148 | Criterion-positive two-level independent mutable copies, full nested validation and insertion-position-preserving replacement/removal. |

No new execution. Null-query and numeric counterexamples here are static findings;
previous List.of probes are not reported as execution of generation0138 or Set.of.
Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
