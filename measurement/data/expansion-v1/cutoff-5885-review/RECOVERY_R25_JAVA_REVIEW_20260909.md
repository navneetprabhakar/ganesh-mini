# R25 Java independent static quality review — 2026-09-09

Gate 2. Main reviewed the single R25 artifact,
`exp-v1-recovery-r25-java-repair-0409`, against its plan, run contract,
immutable parent, hold and selection evidence, architect evidence,
independent-test evidence, derived prompt, reference, mutant and complete test.
No generated code was executed, no candidate was changed, and no admission or
cloud action occurred.

## Decision

**Overall hold: approved prompt-scope binding failed.** The reference, mutant
and tests are substantive seven-criterion positives conditional on prompt
scope, but this exact artifact is not eligible for execution-backed admission.

The selected `oracle-rebuild` operation explicitly allowed replacement of the
embedded complete source and neutralization of stale diagnosis while preserving
all behavioral prose. After replacing the fenced source with a placeholder,
the original and derived prompts are unequal. The derived prompt newly states
that null elements in `allowedKeys` are permitted and have no special effect.
That is a behavioral contract addition, not merely source replacement or
neutral diagnosis. The later explanatory paragraph is consistent with the
selection but does not authorize the earlier prose rewrite. This is the same
fail-closed source-only boundary already applied to R22 and R24 repairs.

Conditionally, the corrected reference removes the unsupported
`allowedKeys.contains(null)` precheck while preserving parsing, trimming,
ignored disallowed keys, duplicate-last insertion order and caller ownership.
The realistic mutant restores that check. The independently authored suite
uses `Set.of`/`TreeSet`, a `HashSet` containing null, and a custom set that
throws on null queries; it also covers normal, empty, malformed, ignored,
duplicate, ordering and nonmutation behavior. No separate reference or test
defect was found. A future correctly bounded source-only regeneration may reuse
the target, but this R25 artifact must remain held.

## Immutable evidence

- Parent canonical SHA-256:
  `754568be928f85a57f3f4d1210d60813641b8f033a82496b186aeeda2f67cea9`.
- Candidate file SHA-256:
  `0fd5210de10407db92e053633c3cf8fd9edf1f011a2787d8a3284acf1b11627f`.
- Candidate canonical SHA-256:
  `e8f3bf80736fca304116e35ac6d1e96c93381aebcf81667a00cb03d4b4a567a6`.
- Prompt/reference/test/mutant SHA-256:
  `d49f1e4804e8a8703e705755e3f1fabdcd97ae9036659c7a2f4d4e034f84ecd0`,
  `5a9006695d32d8d9ddbb8f9b8ca0580cbaa5409e7140d957db04285b9ed0a479`,
  `0639c6ef9b48e3f53422c806831051421eabf86685ba0d13586a59462cc9b6c6`,
  `4da9ce61966bb456148ee5e3f2215dfd063d848164ea5c7fe1bed376fe1a3182`.
- Plan raw/logical SHA-256:
  `a68376b219ed88a10c2750885374839444f3f139e43a96e42e92cecf6e13f04d` /
  `93c8e5340b15878b8f5f7bbc48713577527fd0a540f05571d0588ef0be0d805c`.
- Run contract SHA-256:
  `b4f970f572157f127481011b99a4c8056776a03f13ecdfb099455b974a183a27`.
- Architect and independent-test evidence SHA-256:
  `b5ab314771da25f2d00ec425dbb9f566696cd339c2110e45e55ed75ed057ddfd`,
  `45974fcc13d50023a6ed3d0c7e41a89bd1d95825123bf830c672f5dbd0285b2e`.
- Generated JSONL SHA-256:
  `c700ab2211f45cb48e22eb331ab446a8ca6871e2e2260844d948619d73a2e2fd`.

Source lineage remains MdEval-Instruct revision
`38c9197e3add996fae624eb198ebd06155b2101e`, MIT, with all five recorded
rights true and the exact R25 parent-binding suffix. This verifies provenance,
not admission. The original parent hold remains unchanged.
