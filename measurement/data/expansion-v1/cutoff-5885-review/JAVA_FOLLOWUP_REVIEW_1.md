# Java combined quality follow-up — batch 1

Queue: v13 records in frozen order, Java, reopened stratum, outside the frozen
sample. 1112 records (684 generation, 428 repair). Positions1–15 fully read.
Focus: non-triviality and generation Unicode-blank/whitespace contracts, with
opportunistic semantic checks. Existing source-defined trimming is not silently
replaced with a different contract for repair tasks.

Ten new holds: six executed behavioral defects and four non-triviality findings.
1421 total holds (1418 additive+3);3702 unique outside-sample inspections.
Resume position16. No training admission, altered candidate, or new cloud compute.

| Position | ID | Finding |
| --- | --- | --- |
| 1 | exp-v1-java-generation-0001 | Criterion-positive widened mean; executed hold: U+2003 surrounding a valid integer is not removed by trim(). |
| 2 | exp-v1-java-generation-0002 | Criterion-positive: immutable row objects and unmodifiable ordered snapshots; trimming explicitly defines usable fields. |
| 3 | exp-v1-java-generation-0004 | Criterion-positive byte ownership; executed hold: leading U+2003 in a .png key is accepted despite no leading whitespace. |
| 4 | exp-v1-java-generation-0005 | Criterion-positive relationship/state snapshots; executed hold: U+2003-only given name accepted despite nonblank requirement. |
| 5 | exp-v1-java-generation-0006 | Criterion-positive immutable channel ownership; executed hold: U+2003-only handle accepted despite nonblank requirement. |
| 6 | exp-v1-java-repair-0001 | Criterion-positive: removing in-place sorting repairs both caller ownership and stable partition ordering. |
| 7 | exp-v1-java-repair-0002 | Non-triviality hold: one prescribed http-to-https literal replacement; validation is already supplied. |
| 8 | exp-v1-java-repair-0003 | Executed hold: integer multiplication before division returns -95 instead of 100 for 22,000,000 identical accepted names. |
| 9 | exp-v1-java-repair-0004 | Non-triviality hold: direct insertion of the explicitly prescribed TEXT-only predicate in an otherwise supplied implementation. |
| 10 | exp-v1-java-generation-0008 | Non-triviality hold: direct literal age-range decision table without a substantive algorithm or state invariant. |
| 11 | exp-v1-java-generation-0009 | Criterion-positive aggregation; executed hold: 500,000 full-score Integer.MAX_VALUE rows produce -7179 basis points instead of 10000 due to long multiplication overflow. |
| 12 | exp-v1-java-generation-0010 | Criterion-positive: ordered atomic local edit simulation and independent sorted rows; requires nonempty, not nonblank, strings. |
| 13 | exp-v1-java-generation-0011 | Criterion-positive: validates all edges and colors every disconnected graph component; rejects odd cycles. |
| 14 | exp-v1-java-generation-0012 | Criterion-positive: validates operation/existence rules and copies input/output rows through sorted catalog transitions. |
| 15 | exp-v1-java-repair-0005 | Non-triviality hold: direct boxed identity-to-primitive-value comparison replacement. |

## Executed evidence

All six probes compiled successfully and failed their semantic assertions with
exit codes [0,1], no timeout, pinned Java21.0.11 in the network-disabled,
resource-limited verifier. They replace the diagnostic test entry point only;
receipts preserve original tasks, source, hashes, exact runtime and raw output.

- java_0001_unicode_trim_probe-result.json: 2592 ms; generation-0001.
- java_0004_unicode_edge_probe-result.json: 3017 ms; generation-0004.
- java_0005_unicode_blank_probe-result.json: 3042 ms; generation-0005.
- java_0006_unicode_blank_probe-result.json: 3096 ms; generation-0006.
- java_repair_0003_percent_probe-result.json: 3515 ms; repair-0003.
- java_0009_basis_points_probe-result.json: 3076 ms; generation-0009.

U+2003 is the same whitespace/blank counterexample as the existing executed
sample findings; no universal case-folding or normalization requirement is added.
The numeric probes use small storage: repeated shared immutable rows for the
assessment array and Collections.nCopies for names. They do not modify frozen
candidates. Criterion-positive is not all-seven-criteria approval.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

