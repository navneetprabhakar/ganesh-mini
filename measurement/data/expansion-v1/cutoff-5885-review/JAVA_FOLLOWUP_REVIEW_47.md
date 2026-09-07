# Java combined quality follow-up — batch 47

Positions691–705 of v14 Java queue1112, full prompt/reference read.
Four new holds: three non-triviality and one static behavioral finding.
1814 total holds (1811 additive+3),4392 unique outside inspections. Resume706.

| Position | ID | Finding |
| --- | --- | --- |
| 691 | exp-v1-java-generation-0489 | Static hold: U+2003-only Unit label passes nonblank validation. Ancestor traversal can additionally dereference an unchecked dangling parent before that later unit's own link-validation turn. |
| 692 | exp-v1-java-generation-0494 | Criterion-positive complete registry validation distinguishes first-match save/find from all-match removal while preserving detached ordering and exception types. |
| 693 | exp-v1-java-generation-0495 | Criterion-positive complete uniqueness validation and immutable ordered create/update/delete snapshots, with isBlank text checks. |
| 694 | exp-v1-java-generation-0496 | Criterion-positive reminder identity/range validation precedes immutable schedule/cancel transitions and absent/duplicate rejection. |
| 695 | exp-v1-java-generation-0497 | Criterion-positive complete unique-SKU validation precedes index-based removal and detached rendering; invalid later entries cannot be bypassed. |
| 696 | exp-v1-java-generation-0498 | Criterion-positive validates complete port identity state before ordered replacement, rejecting missing targets without input mutation. |
| 697 | exp-v1-java-repair-0329 | Non-triviality hold: changes the supplied upper-bound comparison from > to >=. |
| 698 | exp-v1-java-generation-0499 | Non-triviality hold: direct parallel-array inequality filter with independent range/null guards. |
| 699 | exp-v1-java-generation-0500 | Criterion-positive strict record parsing, initial uniqueness and ordered upsert/delete reduction produce deterministic sorted output. |
| 700 | exp-v1-java-generation-0501 | Criterion-positive canonical undirected edge encoding deduplicates reversed pairs, sorts packed endpoints and widens output-size arithmetic. |
| 701 | exp-v1-java-generation-0502 | Criterion-positive two-pass bounded half-open expansion validates shapes/endpoints and widened aggregate size before allocating output. |
| 702 | exp-v1-java-generation-0503 | Criterion-positive heterogeneous encoding preserves typed scalar formatting and nullable length-prefixed nested-string boundaries without mutable aliases. |
| 703 | exp-v1-java-repair-0334 | Criterion-positive stack rollback on parent components restores normalized-path state and subsequent above-root rejection. |
| 704 | exp-v1-java-repair-0335 | Non-triviality hold: reverses loop direction to match the explicitly prescribed earliest-layer priority in a supplied fully validated search. |
| 705 | exp-v1-java-repair-0336 | Criterion-positive exact repeated-key accumulation replaces last-write-wins behavior while preserving first-occurrence order and overflow exceptions. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

