# Java combined quality follow-up — batch 12

Positions166–180 of v14 Java queue1112, full prompt/reference read.
Nine new holds: five non-triviality, three static behavioral, one executed behavioral.
1530 total holds (1527 additive+3),3867 unique outside inspections. Resume181.

| Position | ID | Finding |
| --- | --- | --- |
| 166 | exp-v1-java-repair-0077 | Non-triviality hold: substitutes the direct calendar-date library operation into the supplied branch; validation and elapsed-duration behavior are already supplied. |
| 167 | exp-v1-java-repair-0080 | Non-triviality hold: flips the supplied priority comparator. Static behavioral finding: U+2003-only Handler name/type also pass trim-based validation despite required nonblank text. |
| 168 | exp-v1-java-generation-0118 | Criterion-positive nested immutable snapshots and ordered rendering; static hold: U+2003-only table/column names pass nonblank validation, and a U+2003-only label is emitted instead of the required fallback. |
| 169 | exp-v1-java-generation-0119 | Criterion-positive atomic catalog replacement, bounded pagination and ordered snapshots; static hold: U+2003-only names/modes pass nonblank validation, and blank optional filters are applied rather than disabled. |
| 170 | exp-v1-java-generation-0120 | Criterion-positive deep ownership at input and snapshot boundaries; static hold: U+2003-only member names pass nonblank validation in constructor and setter. |
| 171 | exp-v1-java-generation-0121 | Criterion-positive normalized immutable state, create/replace preconditions, ordered snapshots and exact quote multiplication. Explicit trimmed-nonempty label contract is respected; no new constructor validation rule. |
| 172 | exp-v1-java-generation-0122 | Criterion-positive staged sequential exact updates, intermediate balance validation, normalized duplicate detection and unmodifiable sorted result without external mutation. |
| 173 | exp-v1-java-generation-0123 | Executed behavioral hold: accepting (a,b+NUL+c) makes unrelated (a+NUL+b,c) appear connected because the canonical pair delimiter encoding collides. Interior NUL is not prohibited or removed by trimming. |
| 174 | exp-v1-java-generation-0124 | Criterion-positive widened Manhattan distance covers both MIN_VALUE coordinates, comparator tie ordering agrees with equality, and sorted snapshots preserve duplicates. |
| 175 | exp-v1-java-generation-0125 | Criterion-positive normalized immutable catalog state with distinct create/update preconditions and fresh ordered snapshots. Contract explicitly says trimmed nonempty text. |
| 176 | exp-v1-java-generation-0126 | Non-triviality hold: direct temporary-variable swap with two index checks; no substantive algorithm, ownership graph or state transition beyond elementary array assignment. |
| 177 | exp-v1-java-repair-0081 | Criterion-positive delimiter endpoint repair preserves complete argument grammar checks and immutable parsed output. Prompt prohibits parentheses inside the argument, not an additional unstated command-name grammar. |
| 178 | exp-v1-java-repair-0082 | Non-triviality hold: replaces reference identity with String.equals under an already supplied null guard. |
| 179 | exp-v1-java-repair-0083 | Criterion-positive rectangular shape repair aligns output allocation with transposed indexing, including zero-column matrices, while preserving independent row storage. |
| 180 | exp-v1-java-repair-0084 | Non-triviality hold: negates the supplied membership predicate; normalization, deduplication, sorting and snapshot construction are already provided. |

Generation0123 probe: java_0123_pair_collision_probe.java and its -result.json
preserve original task, reference, hashes and sandbox output. Pinned Java21.0.11,
network disabled, one CPU,512MiB,64 PIDs,60-second timeout: compile/run [0,1],
2977ms, no timeout. The assertion confirms a false connection for distinct pairs.
All other new findings are static; no additional executions are claimed.
Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
