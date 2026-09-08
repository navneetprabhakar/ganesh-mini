# R10 Java test-only correction review — 2026-09-08

Gate 2; exactly four complete corrected suites reviewed against their frozen R8 prompts, references and mutants. **Four static positives; zero new holds.** No execution, cloud use, admission, central mutation or repeated critic. Zero original unique-row review credit.

Every prompt object and complete validation object equals R8 exactly. The previously fully read reference/mutant assessments carry forward; no implementation was silently substituted. The four historical R8 quality holds remain evidence about R8, not these corrected hashes.

| Exact candidate ID | Static disposition and distinguishing evidence |
|---|---|
| exp-v1-recovery-r10-java-generation-0641 | Positive. Two-row exactBoundary fixture excludes `(Integer.MAX_VALUE,1)` and includes `(Integer.MAX_VALUE,0)` from origin at radius Integer.MAX_VALUE. Squared distances differ by one, so the double-rounding mutant incorrectly includes the first row. No epsilon or floating oracle is used. Existing full-range coordinates/radius, zero radius, palette, invalid input and matrix ownership tests remain. |
| exp-v1-recovery-r10-java-generation-0617 | Positive. Set.of() is tested against empty and nonempty assets, Set.of("g2") filters, and TreeSet selects valid groups. These standard accepted sets distinguish the null-query mutant. Returned lists are independently mutable; later-null asset validation precedes first-match return; duplicate ID identity and case sensitivity remain. No private-field reflection or extra immutable-layout requirements. |
| exp-v1-recovery-r10-java-generation-0687 | Positive. Invalid DELETE permission collections containing zero, negative and null now enclose construction plus apply against an existing group. Reference rejects during apply; mutant wrongly deletes. Null, empty and valid-positive DELETE controls succeed and initial contents remain unchanged. Malformed REPLACE permission assertion also encloses apply. No earlier constructor stage is demanded for permission elements; fixed constructor checks for null kind, zero group and forbidden null CREATE permissions remain consistent with the unchanged API. |
| exp-v1-recovery-r10-java-generation-0762 | Positive. Standalone-newline assertion is removed without adding its opposite. Extra-pipe rejection directly distinguishes the mutant; one trailing newline on actual records remains accepted. Empty feed, duplicates/order, two trailing newlines, blank/interior malformed records, CR and Unicode edge whitespace remain covered. Added percent-looking opaque URL is retained literally, as required; no decoding or scheme-validation policy added. |

## Seven-criterion adjudication

1. **Clarity:** frozen specifications unchanged. The 0762 ambiguous standalone-newline case is not converted into a new contract; the test only omits that unsupported expectation.
2. **API consistency:** required names, parameter types, return shapes, mutable versus immutable results, field accessors and exceptions retained. 0687 no longer forces invalid permission elements to fail before apply.
3. **Independent tests:** critic sees only exact specifications, prior tests and specification-derived feedback. Provenance and output bindings below pass; oracle adequacy was separately assessed by complete reading.
4. **Whole-target nontriviality:** exact geometry/validation/color/ownership, full-list validation/selection/identity, sequential transactional permission updates with sorted deep snapshots, and restricted feed grammar with opaque values remain the same substantive targets. No elementary padding was added.
5. **Idiomatic implementation:** R8 references remain appropriate: exact BigInteger comparison, element iteration instead of unsupported null queries, copied transaction state and standard deterministic parsing. Corrected tests use small public-domain fixtures rather than private state or invented limits.
6. **Dependency isolation:** standard-library Java only with executable SolutionTest mains. No unbounded resources, external services or concurrency requirements added. No execution/compilation claimed here.
7. **Realistic failure:** each corrected suite now reaches the intended current mutant. Shared invalid oracle failures no longer substitute for the intended defect witness. Static review found no new unjustified expectation.

## Exact provenance and hashes

Paths below are relative to `datasets/cache/expansion-v1/versioned-recovery/r10/` unless stated otherwise.

- `plan.json` file SHA256: `728e70ee23ad46f8a4a8aec64a34d74b48c073a5382849fc52ce449154f2afb5`.
- `java-recovery-test-correction-evidence.json`: `1d9bbd318103b3aa50688eef0ae2b4299f55e4cd07a730d0a6dea4d07ed0e1f8`.
- Review-root `recovery-requests-r10.json`: `2a9a76b9baa61ee4de2794c4d0bd75225407ffebb454a6166cf80793e2551221`.
- Review-root `recovery-test-feedback-r10.json`: `4ac15446964c97884986ad218d56fd0b3c92186a594a517657c4f5b52f3ef40d`.

Evidence prompt and final-output hashes recompute correctly and disallowed-tool list is empty. Parsed critic items have exactly id/problem/test_code; each problem and previous test equals its R8 counterpart. All four feedback previous_candidate_sha256 canonical bindings match R8. Corrected final-output tests equal installed R10 files. All four prompt and full reference/mutant validation objects match R8 exactly. Full immutable parent/source lineage is inherited through the unchanged R8 bindings documented in RECOVERY_R8_JAVA_REVIEW_20260908.md; no ownership decision or original candidate is altered.

| Suffix | Candidate file SHA256 | Corrected test content SHA256 |
|---|---|---|
| 0641 | ca3696211cbf83e34263931b373a41fad3eb844d67b9c66ecaf895e7ca1d20f6 | 884fc16a2048dd1336cf0eb0f3db456785401ac675f13f078b3d04573d06c65b |
| 0617 | 4778f64672bc3d624b58e8ef138bfbc91dc0b5dadb00607c6e23cbc501704df9 | f4949d5228de42e30ca2ecd496f8d16b381dd691c39183b87bb78f625f5e9877 |
| 0687 | bba446c2301a3c6f26c66f535d82fe731692046cd29d32a5c7db663131ab06e7 | 737e9a38c5e15388075887c8884d0c0a84df46b51f34cca99528d99e585b0d0b |
| 0762 | 9400b182c758d03edf7b46990bbf41c3fca1d6444fea5c41f99944d96f889a94 | be0988a378476805a8fc8b99a760b59e4d1b531309fab9f5dea033421bfc1b05 |

Main owns serial sandbox verification and admission. These decisions are static quality findings only, not executed pass/fail counts or release certification.
