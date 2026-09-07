# Java combined quality follow-up — batch 46

Positions676–690 of v14 Java queue1112, full prompt/reference read.
Nine new holds: four non-triviality and five static behavioral/contract findings.
1810 total holds (1807 additive+3),4377 unique outside inspections. Resume691.

| Position | ID | Finding |
| --- | --- | --- |
| 676 | exp-v1-java-generation-0481 | Criterion-positive independently normalized permission/role snapshots validate selected lists without retaining mutable aliases. No additional constructor immutability rule is inferred for directly constructed records. |
| 677 | exp-v1-java-generation-0482 | Criterion-positive bounded FIFO transitions validate supplied record state and detach returned message lists; the prompt specifically forbids null stored messages, not explicitly empty stored strings. |
| 678 | exp-v1-java-generation-0483 | Static contract/alias hold: valueAt returns the original mutable value (including explicitly supported byte arrays), contradicting the no-exposed-alias requirement. Arbitrary Object copying also needs a clarified contract. |
| 679 | exp-v1-java-generation-0485 | Non-triviality hold: directly transcribes two prescribed scalar formulas, finite checks and formatting without substantive algorithm or state transition. |
| 680 | exp-v1-java-generation-0486 | Criterion-positive nested subscription snapshots validate every registry entry and copy mutable topic lists on all read/write return paths. |
| 681 | exp-v1-java-repair-0322 | Criterion-positive validates forbidden path segments at every depth rather than only the leaf, while preserving empty-segment and complete input validation. Broad Unicode case equivalence is not certified. |
| 682 | exp-v1-java-repair-0323 | Criterion-positive checked repeated-key accumulation preserves first occurrence order and translates overflow to the required exception. |
| 683 | exp-v1-java-repair-0324 | Non-triviality hold: adds the explicitly specified boolean guard around one already supplied acknowledgement append. |
| 684 | exp-v1-java-generation-0487 | Non-triviality hold: four-operator wrapper delegates exact arithmetic and directly transcribes the two division error cases. |
| 685 | exp-v1-java-generation-0488 | Static hold: U+2003-only device serial or label passes required nonblank-after-trimming validation. |
| 686 | exp-v1-java-generation-0490 | Non-triviality hold: stateless switch transcribes the supplied four-stage transition/message table. |
| 687 | exp-v1-java-generation-0491 | Static hold: U+2003-only line is not ignored as blank; trim preserves it and parseInt throws. |
| 688 | exp-v1-java-generation-0492 | Criterion-positive versioned binary framing validates lengths, strict UTF-8 decoding, optional long marker, truncation and trailing bytes without retaining input arrays. |
| 689 | exp-v1-java-repair-0326 | Static hold: children.contains(null) rejects valid null-free List.of child lists with NullPointerException on the pinned Java runtime; this candidate was not separately executed. |
| 690 | exp-v1-java-repair-0328 | Static hold: handlers.contains(null) rejects valid List.of handler lists with NullPointerException before dispatch; this candidate was not separately executed. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

