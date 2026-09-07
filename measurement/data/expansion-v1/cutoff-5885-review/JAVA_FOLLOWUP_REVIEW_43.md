# Java combined quality follow-up — batch 43

Positions631–645 of v14 Java queue1112, full prompt/reference read.
Eight new holds: four non-triviality and four static behavioral findings.
1778 total holds (1775 additive+3),4332 unique outside inspections. Resume646.

| Position | ID | Finding |
| --- | --- | --- |
| 631 | exp-v1-java-repair-0298 | Criterion-positive per-tenant routing isolation repair resolves each job independently rather than leaking the first tenant destination to later jobs. |
| 632 | exp-v1-java-repair-0299 | Non-triviality hold: appends the already accumulated final partial page after a complete supplied pagination loop. |
| 633 | exp-v1-java-repair-0300 | Criterion-positive key lifecycle repair removes released keys from state so repeated UP and subsequent DOWN events remain correctly paired. |
| 634 | exp-v1-java-generation-0451 | Static hold: U+2003-only plan name passes blank validation. Exact mutable balance updates and immutable plan properties are otherwise substantive. |
| 635 | exp-v1-java-generation-0452 | Static hold: U+2003-only picture label passes blank validation. Copied cyclic navigator ordering is otherwise substantive; extreme index arithmetic is not executed. |
| 636 | exp-v1-java-generation-0454 | Criterion-positive stateful exact-decimal accumulation, numeric maximum and DECIMAL128 average preserve sample/collection ownership. Atomic rejection of a whole accept batch is not required or claimed. |
| 637 | exp-v1-java-generation-0455 | Static hold: U+2003-only category descriptions pass blank validation. Successful-registration sequencing and prior-list snapshot isolation are otherwise substantive. |
| 638 | exp-v1-java-generation-0456 | Static hold: U+2003-only reviewer passes nonblank-after-trimming validation. First-appearance grouped counting is otherwise substantive. |
| 639 | exp-v1-java-repair-0302 | Non-triviality hold: flips the supplied extrema comparison from < to >. |
| 640 | exp-v1-java-repair-0303 | Criterion-positive unsigned high-header-byte repair accepts the full16-bit payload length while retaining strict UTF-8 decoder and exception contract. |
| 641 | exp-v1-java-repair-0304 | Criterion-positive cache-miss fallback repair distinguishes available-but-missing values from unavailable-cache state and preserves the no-read-when-unavailable boundary. |
| 642 | exp-v1-java-generation-0453 | Criterion-positive bounded aliasing view implements independent cursor/close state, read-only ownership and all-or-nothing bulk bounds including overlapping array copies. |
| 643 | exp-v1-java-generation-0457 | Non-triviality hold: elementary count-and-copy filter transcribes one inequality predicate over an array. |
| 644 | exp-v1-java-generation-0459 | Criterion-positive full nested validation and cross-group distinct intersection handle undefined empty universe and empty groups without early validation bypass. |
| 645 | exp-v1-java-generation-0460 | Non-triviality hold: direct membership partition with independent null guards and list wrapping contains no substantive algorithm or state transition. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
