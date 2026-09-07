# Java combined quality follow-up — batch 40

Positions586–600 of v14 Java queue1112, full prompt/reference read.
Nine new holds: five non-triviality and four static behavioral findings.
1757 total holds (1754 additive+3),4287 unique outside inspections. Resume601.

| Position | ID | Finding |
| --- | --- | --- |
| 586 | exp-v1-java-repair-0278 | Non-triviality hold: moves the supplied comma emission behind the direct non-first-element guard. |
| 587 | exp-v1-java-repair-0279 | Criterion-positive closed-overlap repair removes adjacency merging and preserves distinct one-unit-gap ranges without input mutation. |
| 588 | exp-v1-java-repair-0280 | Static hold: U+2003-only tags, keys and values pass nonblank validation. Requested-before-default resolution repair is otherwise criterion-positive. |
| 589 | exp-v1-java-generation-0420 | Static hold: U+2003-only member text passes nonblank validation. Uniqueness uses equalsIgnoreCase rather than the specified Locale.ROOT normalization, so dotless-i and i collide despite distinct ROOT lowercase forms. |
| 590 | exp-v1-java-generation-0421 | Criterion-positive stable ranking and capacity-limited rendering preserve full input validation, exact highlight identity and mandatory final title. |
| 591 | exp-v1-java-generation-0422 | Non-triviality hold: three direct immutable record factories populate the explicitly prescribed nullable field combinations. |
| 592 | exp-v1-java-generation-0423 | Criterion-positive fully validated permutation simulation distinguishes stack-realizable orders from impossibility and returns ordered push/pop evidence without mutating targets. |
| 593 | exp-v1-java-generation-0424 | Criterion-positive nested list ownership and duplicate-preserving registry lifecycle support immutable insertion-order snapshots and re-add ordering. |
| 594 | exp-v1-java-repair-0282 | Non-triviality hold: changes the supplied expiration predicate from <= to the explicitly required strict <. |
| 595 | exp-v1-java-repair-0283 | Criterion-positive normalization ownership repair avoids caller-list mutation, including immutable lists and late null-element failure. |
| 596 | exp-v1-java-repair-0284 | Non-triviality hold: forwards the explicitly supplied label to the existing validated factory instead of the default-label overload. |
| 597 | exp-v1-java-generation-0425 | Non-triviality hold: direct field-length/regex/state-membership validation transcribes the supplied independent address rules. Bounded numeric length makes parseInt safe. |
| 598 | exp-v1-java-generation-0427 | Static hold: existing lists with duplicate IDs are accepted by check and propagated by operations despite the unique-ID requirement. Add only compares the new ID against existing ones. |
| 599 | exp-v1-java-generation-0428 | Static hold: U+2003-only labels are preserved rather than normalized to null under the whitespace-only label rule. Finite/clamped viewport geometry is otherwise substantive. |
| 600 | exp-v1-java-generation-0429 | Criterion-positive immutable panel choice uniqueness, referential selection and enabled-choice transitions preserve independent snapshots and empty/no-selection behavior. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
