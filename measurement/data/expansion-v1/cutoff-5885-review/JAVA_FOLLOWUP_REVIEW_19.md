# Java combined quality follow-up — batch 19

Positions271–285 of v14 Java queue1112, full prompt/reference read.
Five new holds: four non-triviality and one executed behavioral finding.
1589 total holds (1586 additive+3),3972 unique outside inspections. Resume286.

| Position | ID | Finding |
| --- | --- | --- |
| 271 | exp-v1-java-repair-0125 | Criterion-positive nested ownership repair copies rows before wrapping while preserving explicitly valid null cells. |
| 272 | exp-v1-java-repair-0126 | Non-triviality hold: deletes the unconditional COMPLETED overwrite after the fully supplied failure branch. |
| 273 | exp-v1-java-repair-0127 | Criterion-positive signed-magnitude repair widens before abs so MIN_VALUE does not introduce a minus sign into digit counting. |
| 274 | exp-v1-java-repair-0128 | Non-triviality hold: replaces the self-overwriting postincrement expression with the direct next-index modulo formula. |
| 275 | exp-v1-java-generation-0189 | Criterion-positive full-list validation before append/replace, bounded maximum-ID allocation, first-match revision and immutable creation/revision lineage. |
| 276 | exp-v1-java-generation-0193 | Criterion-positive validated duplicate admission and insertion-ordered immutable snapshots; only registry methods can place values into stored state. |
| 277 | exp-v1-java-generation-0194 | Criterion-positive inactive/active session transitions, defensive channel deduplication and independent event snapshots. Already-active versus malformed-start precedence is ambiguous and not newly held. |
| 278 | exp-v1-java-generation-0195 | Criterion-positive multiset count transitions remove zero entries, use checked increments/products and preserve enum-ordered detached snapshots. |
| 279 | exp-v1-java-generation-0198 | Criterion-positive unique sequence admission and position-preserving immutable replacement keep prior journal snapshots unchanged. |
| 280 | exp-v1-java-repair-0129 | Non-triviality hold: adds the omitted remaining-- to a complete bounded fixed-point loop. |
| 281 | exp-v1-java-repair-0131 | Criterion-positive hierarchy ownership repair attaches new root peers to ROOT rather than the validated source node, preserving global identity checks and root-child order. |
| 282 | exp-v1-java-repair-0132 | Non-triviality hold: replaces floor division with a standard widened ceiling-division formula under supplied validation and cap. |
| 283 | exp-v1-java-generation-0196 | Executed behavioral hold: capacity Integer.MAX_VALUE overflows capacity+1; adding weight 1 commits immediately despite mathematical threshold 1073741824. Static secondary defect: bufferedWeight can overflow when a large valid command follows a partial buffer. |
| 284 | exp-v1-java-generation-0197 | Criterion-positive fully staged unique-ID load, detached filtered/sorted views and filter-independent lookup. |
| 285 | exp-v1-java-generation-0201 | Criterion-positive complete finite-coordinate and star validation before the single intentional append, preserving exact successful-site identity and immutable fields. |

java_0196_threshold_overflow_probe.java and matching -result.json preserve the
original record/reference, hashes and output. Pinned Java21.0.11, network disabled,
1CPU,512MiB,64PIDs,60-second timeout: compile/run [0,1],2408ms,no timeout.
Only the threshold counterexample was executed; buffered-sum overflow is static.
Focused positives are not admission. No new constructor, concurrency or precedence
requirements were imposed. Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
