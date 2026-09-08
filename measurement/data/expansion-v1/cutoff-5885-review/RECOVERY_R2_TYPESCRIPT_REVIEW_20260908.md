# Recovery r2 TypeScript0064 static review — 2026-09-08

**Static quality positive for exp-v1-recovery-r2-typescript-generation-0064.** The single bounded test correction resolves the three r1 blockers. No new unsupported expectation was identified. No compilation, candidate execution, cloud/teacher calls, central changes or admission occurred in this review; main owns fresh sandbox results and admission checks. No additional critic loop is requested.

## Complete-test findings

The complete corrected solution.test.ts was read against the unchanged r1 specification, reference and known-bad.

- Ownership tests now use explicit mapped mutable views, removing readonly with `-readonly` before assignment. Imported Performance/Reservation types are not directly mutated through readonly references. Local assertion helpers and type-only imports require no Node declarations. This resolves the predicted r1 compile incompatibility statically; an actual strict-compiler pass is still main-owned evidence.
- The unfinished placeholder assertion is gone. A patch containing only extra id/active fields now returns an unchanged reservation; supported seat updates coexist with ignored extras. This agrees with the clarified supported-field/ID-retention contract rather than asking the reference to throw an unpromised error.
- Object.defineProperty now supplies **non-enumerable seat='B9'**, in addition to hidden customerId/performanceId. The assertion checks all expected fields and retained ID. The unchanged mutant still gates seat on propertyIsEnumerable and would leave the earlier seat='A9', so this exact test distinguishes the intended bug. It does not merely test unrelated hidden fields that the mutant handles correctly.
- Ordinary constructor malformed/duplicate validation, empty storage, malformed drafts, explicit-ID collision, generated-ID collision skipping, query order, failed-operation atomicity, direct/undefined/empty patch behavior, ownership, deletion and remaining-result order are covered with bounded fixtures.
- Fieldwise reservation comparisons replace JSON-string equality, avoiding an incidental object-property insertion-order requirement. Generic malformed draft/update checks use generic throw assertions where the prose does not specify the exact error class. Explicit constructor TypeError and unknown-performance RangeError checks retain their contract basis.

The final state/order expectations are consistent: r1 changes to customer c3/performance p2; reservation-1 is removed; reservation-3 remains p2. Therefore customer c1 has no remaining rows and the p2 query yields r1 followed by reservation-3. This is actual insertion-order reasoning, not an inferred sort requirement.

No reference change is requested. Explicit direct-read field reconstruction and precommit validation remain correct for the scoped correction. No hostile getters, inaccessible counters, arbitrary allocation guarantees or descriptor-preservation rules were introduced.

## Seven criteria and lineage

Prompt clarity and API consistency retain the explicit r1 clarification; the corrected suite now agrees. Independent test origin is supported by the archived specification/proposed-test/feedback-only critic request, which does not provide reference or mutant code. Whole-target non-triviality remains the coupled reservation lifecycle, foreign keys, collision handling, query order and ownership. Reference idiom and standard-library dependency isolation remain positive. The realistic hidden-seat mutant now has a meaningful independent distinguishing assertion. These are static seven-criterion judgments, not executed pass/fail measurements.

The r2 prompt object and full validation object compare exactly equal to r1, preserving both reference and known-bad. The new test content matches the critic's final output for the exact derived ID and its stored SHA-256. Critic prompt/output hashes recompute. Archived events contain only thread/turn/agent-message records and no tools. The request feedback specifically identifies readonly-compatible ownership tests, removal of the unsupported placeholder, hidden-seat coverage and ordinary API breadth; it supplies no implementation source.

Original parent lineage remains exp-v1-typescript-generation-0064 with canonical SHA-256 `b282271869c48b1390be6822cad7841c19d1ae211a3f378ea186e65c197d9f39`. This is one derived quality review, zero new original unique coverage. Original and r1 holds/evidence are not erased or relabeled as passes.

## SHA-256 bindings

Paths are under datasets/cache/expansion-v1/versioned-recovery/r2 unless noted.

| Object | SHA-256 |
| --- | --- |
| exp-v1-recovery-r2-typescript-generation-0064.candidate.json file bytes | 28e1eb8c09ebdc27acd80b3086a0c508a55f8c51bac61c7849933c15f90633bb |
| Corrected solution.test.ts content | 2e82afa7ccc2e5a30771d54b1dffe3bab08579b6d68df772a1e6811336f57fc0 |
| typescript-recovery-test-correction-evidence.json file bytes | 88385e55daa83eaac218735a31810374178795bc9301e30ac7e672616b115f4d |
| Unchanged prompt | 2f3b045934241f6f9324d27ad37a61083d00374be73c40ffb875093d77520750 |
| Unchanged reference | 7097938eae44473878cd0ef2ad01544fcaf2da9f86620df80a48ad793b010f96 |
| Unchanged known-bad | 3ddea3ecf89890379bae413771ae7c00e5512f715ce1a036400fe0973ee99768 |

Recommendation: carry this exact immutable candidate to main's serial reference-pass/mutant-fail verification and remaining admission checks. No automatic extra correction is needed on the reviewed evidence.
