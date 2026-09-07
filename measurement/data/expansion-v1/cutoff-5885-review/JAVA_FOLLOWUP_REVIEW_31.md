# Java combined quality follow-up — batch 31

Positions451–465 of v14 Java queue1112, full prompt/reference read.
Nine new holds: four non-triviality and five static behavioral findings.
1690 total holds (1687 additive+3),4152 unique outside inspections. Resume466.

| Position | ID | Finding |
| --- | --- | --- |
| 451 | exp-v1-java-generation-0323 | Criterion-positive unique-code validation and fully deterministic descending-weight/ascending-code ordering preserve detached immutable records. |
| 452 | exp-v1-java-generation-0324 | Criterion-positive complete validation includes filtered-out readings, stable mixed-direction sorting avoids arithmetic comparison overflow and snapshots output. |
| 453 | exp-v1-java-repair-0213 | Non-triviality hold: substitutes the directly prescribed Class.isInstance library operation for exact-class equality. |
| 454 | exp-v1-java-repair-0214 | Criterion-positive duplicate-key parser repair prevents silent information loss while preserving encounter order and strict ASCII grammar. |
| 455 | exp-v1-java-repair-0216 | Non-triviality hold: swaps the two directly specified null-phase return literals. |
| 456 | exp-v1-java-generation-0325 | Static hold: U+2003-only scanned code and timestamp pass blank checks, allowing lookup/borrow contrary to malformed-code and timestamp rules. |
| 457 | exp-v1-java-generation-0326 | Static hold: U+2003-only query is not treated as blank; a matching recipe can be returned. Duplicate recipe references also yield duplicates despite the at-most-once recipe language. Ingredient ownership is otherwise substantive. |
| 458 | exp-v1-java-generation-0327 | Static hold: U+2003-only participant handle/contact pass blank validation and can be registered. Normalized uniqueness and detached storage are otherwise substantive. |
| 459 | exp-v1-java-generation-0328 | Static hold: U+2003-only peer can enter CONNECTING despite the nonblank-peer requirement. Session transitions/history ownership are otherwise substantive. |
| 460 | exp-v1-java-generation-0329 | Criterion-positive capacity/size invariants, vacated-slot clearing and separate active/backing snapshots preserve array ownership through reset and removal. |
| 461 | exp-v1-java-generation-0330 | Static hold: U+2003-only id/unit fields pass blank validation in registry add/find/change/remove. Immutable normalized replacement is otherwise substantive. |
| 462 | exp-v1-java-repair-0217 | Non-triviality hold: changes a supplied negative-step guard from <=0 to <0; all exact arithmetic is already implemented. |
| 463 | exp-v1-java-repair-0218 | Criterion-positive conversion ownership repair copies nullable-element tag lists so later source mutations cannot alter converted state; getter already returns a copy. |
| 464 | exp-v1-java-repair-0220 | Non-triviality hold: removes the explicitly forbidden empty-selection shortcut. Additional static null-query issue: a row null key can trigger selected.contains(null) on null-hostile Set implementations even when unselected. |
| 465 | exp-v1-java-generation-0331 | Criterion-positive JSON lexical escaping handles delimiters and all U+0000–001F controls without treating them as literal JSON text; scalar tick conversion alone is not the basis for this positive. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
