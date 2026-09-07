# Java combined quality follow-up — batch 2

Positions16–30 of the frozen v13 Java combined queue (1112), full prompt/reference
read. Eleven non-triviality positives; four non-triviality holds and one static
Unicode-blank behavioral hold.1426 total holds (1423 additive+3),3717 unique
outside-sample inspections. Resume31. No new execution in this batch.

| Position | ID | Finding |
| --- | --- | --- |
| 16 | exp-v1-java-repair-0006 | Non-triviality hold: direct String identity-to-equals substitution with all validation supplied. |
| 17 | exp-v1-java-repair-0007 | Non-triviality hold: direct prescribed first-code-point predicate split; supplementary traversal is already present. |
| 18 | exp-v1-java-repair-0008 | Criterion-positive: normalization-before-block-validation repairs representation-dependent length checking and prevents substring failure. |
| 19 | exp-v1-java-generation-0013 | Criterion-positive: strict ASCII digit grammar, bounded nonzero conversion and uniform checked exception; String.trim scope is explicit. |
| 20 | exp-v1-java-generation-0015 | Criterion-positive: digit-adjacency state across successive decimal digits and bounded enumeration with detached ordered results. |
| 21 | exp-v1-java-repair-0009 | Criterion-positive: replaces mutating sort/search with a non-mutating order-independent scan, repairing caller ownership. |
| 22 | exp-v1-java-repair-0010 | Non-triviality hold: direct strict-to-inclusive lower-bound comparator replacement. |
| 23 | exp-v1-java-repair-0011 | Criterion-positive: getter copy closes the remaining array ownership boundary. |
| 24 | exp-v1-java-repair-0012 | Non-triviality hold: loop start literal 1-to-0 replacement; validation and pipeline accumulation are supplied. |
| 25 | exp-v1-java-generation-0014 | Criterion-positive: insertion-order-preserving updates, dual uniqueness constraints, dependent counts and detached snapshots; trimmed/nonempty fields and Locale.ROOT are explicit. |
| 26 | exp-v1-java-generation-0016 | Criterion-positive: create/update distinction and immutable asset snapshots with ID ordering; trimmed/nonempty rather than nonblank contract. |
| 27 | exp-v1-java-generation-0017 | Criterion-positive: dual uniqueness, ordered snapshots and iterator-safe bulk removal; trimmed/nonempty code contract. |
| 28 | exp-v1-java-generation-0018 | Criterion-positive: role-directed callbacks after stored registration, strict calendar parsing and normalized credential lookup. |
| 29 | exp-v1-java-generation-0020 | Criterion-positive: scheduling/credit state invariant, exact accumulation before commit and idempotent scheduling. |
| 30 | exp-v1-java-generation-0021 | Criterion-positive rational aggregation; static hold: U+2003-only key passes trim().isEmpty() despite explicit nonblank-key requirement. Wider rational intermediate representability is not newly adjudicated. |

The generation0021 constructor accepts new RationalTerm("\\u2003",1,1): trim
leaves U+2003 intact. This is static propagation of the already executed Java
nonblank defect, not a new runtime result. Explicit trim/nonempty contracts in
other tasks are not replaced with an invented nonblank rule.
Focused positives do not establish admission or full seven-criterion approval.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

