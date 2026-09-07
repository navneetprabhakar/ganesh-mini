# Java combined quality follow-up — batch 32

Positions466–480 of v14 Java queue1112, full prompt/reference read.
Six new holds: four non-triviality and two static behavioral findings.
1696 total holds (1693 additive+3),4167 unique outside inspections. Resume481.

| Position | ID | Finding |
| --- | --- | --- |
| 466 | exp-v1-java-generation-0332 | Criterion-positive full nested key/map validation and authorization-aware existence search deliberately uses containsKey rather than inspecting possibly null values. |
| 467 | exp-v1-java-generation-0333 | Static hold: U+2003-only endpoints pass the non-whitespace requirement through trim-based validation. Cursor-preserving removal is otherwise substantive. |
| 468 | exp-v1-java-generation-0334 | Static hold: TemplateField(List.of()) queries contains(null), which throws on valid empty immutable Java lists. Same candidate-bound defect family as the previously executed List.of null-query probes; this candidate was not executed. |
| 469 | exp-v1-java-repair-0221 | Non-triviality hold: substitutes the explicitly requested substring contains call for equals. |
| 470 | exp-v1-java-repair-0223 | Non-triviality hold: adds a double cast to the supplied total/count expression; long accumulation and validation are already present. |
| 471 | exp-v1-java-repair-0224 | Criterion-positive lifetime ordering captures mutable field text before releasing its reference and makes subsequent finish calls idempotent. |
| 472 | exp-v1-java-generation-0337 | Non-triviality hold: fixed enum data declaration and explicit-code linear lookup directly transcribe the supplied table. |
| 473 | exp-v1-java-generation-0338 | Criterion-positive grouped latest-event selection separates later-tie wins from first-retained-user ordering and snapshots immutable summaries. |
| 474 | exp-v1-java-generation-0339 | Criterion-positive bounded binary framing validates unsigned fields, exact length, version and checksum before detached XOR decoding. |
| 475 | exp-v1-java-generation-0340 | Criterion-positive parent-before-child catalog invariant makes direct-child rejection sufficient for all descendants; detached ordered queries preserve ownership. |
| 476 | exp-v1-java-generation-0341 | Criterion-positive recursive composite rule ownership and ordered short-circuit evaluation preserve empty all/any identities. |
| 477 | exp-v1-java-repair-0228 | Non-triviality hold: moves the explicit null-element guard before trim in an otherwise supplied join routine. |
| 478 | exp-v1-java-generation-0342 | Criterion-positive declaration-ordered recognized overrides and defensive configuration/accessor copies isolate caller state and preserve empty overrides. |
| 479 | exp-v1-java-generation-0343 | Criterion-positive registry operations preserve unrelated state, distinguish undefined versus false and return sorted independent mutable names. No concurrency guarantee is invented. |
| 480 | exp-v1-java-generation-0344 | Criterion-positive keyed add/update distinction and detached numeric-order listing preserve immutable records and mutable registry boundaries. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
