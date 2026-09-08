# Recovery r1 TypeScript static quality review — 2026-09-08

## Result

Exactly two derived candidates reviewed: exp-v1-recovery-r1-typescript-generation-0064 and exp-v1-recovery-r1-typescript-generation-0087. **0064 has a static test-harness/oracle quality hold;0087 receives a static seven-criterion positive, subject to fresh sandbox verification and admission checks.** Both reference corrections implement the requested semantic clarification. No candidate execution, cloud/teacher request, candidate mutation, ledger change or admission was performed by this reviewer.

All derived prompts, complete references, independent tests and known-bad sources were read. Parent prompt/reference differences and request semantic clarifications were checked against immutable original candidate records. Calibration follows SEVEN_CRITERIA_GO.md, SEVEN_CRITERIA_TYPESCRIPT.md and the earlier exact property adjudication. This is two derived reviews, not new unique original inspection coverage or two recovered admissions.

## Binding / scope

Both requests are contract-clarification, not byte-preserving reference-fix. The changed prompt passages explicitly define absent/undefined patch handling, supported non-enumerable fields, invalid-value atomicity, and preservation of unrelated behavior.0064 additionally freezes ID retention;0087 explicitly requires boolean active validation and preserves empty-patch notification. These changes match the plan request rationales; no unrelated broad domain restriction was introduced.

Canonical parent JSON SHA-256 values match plan records. Exact derived IDs join architect and independent-test outputs; prompt, reference, known-bad and test content all match those outputs byte-for-byte. Their stored content hashes recompute, and assistant training messages equal reference source. Architect/test prompt and final-output hashes recompute. Both archived streams contain only thread/turn and agent-message events, no tool events; disallowed-tool lists are empty. The independent request supplies only the two IDs/specifications and runtime contract, not reference, mutant, parent tests or architect context. Independence is supported, but does not guarantee correctness of the tests.

## 0064: reference corrected; packaged tests blocked

Reference explicitly reconstructs customerId/performanceId/seat from direct patch reads, preserves fields when undefined, and always retains current.id. Validation precedes map replacement. This fixes the held loss of a supplied hidden seat, honors the explicit extra-ID rule, preserves foreign-key validation, insertion order and detached outputs. Its Map/field-copy approach is idiomatic and standard-library-only. The whole reservation lifecycle, generated-ID collision skipping, foreign keys, failure atomicity and query ownership are substantive; the correction is not elementary because it is small.

Three separate problems prevent a positive packaged result:

1. **Compile incompatibility:** exported Performance and Reservation fields are readonly. The test directly assigns originalPerformances[0].id and venueId, first.customerId, fetchedA.seat, queryA[0].seat and updated.seat. These are statically invalid assignments to the imported readonly interfaces, predicted TS2540 errors. This is not an executed compiler result. The contract does not freeze mutable field declarations; readonly input-array typing also does not independently settle element typing. Test ownership via an explicit mutable local view/cast or another contract-compatible witness, rather than requiring the reference to remove reasonable readonly declarations solely for this test.
2. **Unsupported final oracle:** the last assertion is literally labeled `placeholder` and expects update('r1', {active:true}) to throw Error. Active is not a supported reservation patch field. The same suite accepts ignored extra `id` and `ignored` fields, and the clarified contract requires changes only to supported fields. There is no specified basis for this throw. Correct behavior is an unchanged detached reservation with no mutation; do not modify the reference to satisfy the placeholder.
3. **Mutant coverage gap:** hidden fields are tested only for customerId/performanceId. The supplied known-bad reads those correctly but gates **seat** on propertyIsEnumerable. All tested seat updates are enumerable literals, so this specific realistic mutant is not distinguished. Once compile/oracle issues are fixed, add a non-enumerable seat value and assert it changes the stored seat while retaining the ID. Merely obtaining any mutant failure from a broken common harness would not establish semantic discrimination.

Coverage also omits direct delete behavior and malformed/duplicate performance-constructor cases despite the task exposing those operations. These are ordinary breadth additions for the successor suite, not new reference defects. Preserve collision, detached-copy and atomic multi-field update checks already present. No reference change is requested on current evidence.

## 0087: static positive

Reference reads displayName and active directly, preserves either when absent/undefined, validates both before assignment and emits only after successful replacement. Explicit reconstruction prevents the original spread from dropping hidden false. Registration validates and trims IDs/names, checks boolean active, rejects duplicate IDs, and stores a fresh record. Find/authenticate/update/register and each callback get separate copies; removal emits undefined only after deletion.

Each watch has its own Entry rather than listener-identity deduplication. Emit filters active registrations once then dispatches the snapshot, so an unsubscribe during the first callback does not remove the second callback from the current notification, and newly added registrations apply to a later notification. Duplicate unsubscribe handles remain independent and idempotent. Inactive entries are retained internally, but the prompt does not mandate compaction or a lifetime allocation bound; this is not a new correctness hold.

The independent suite includes the exact regression: define non-enumerable active=false and displayName, update a previously active account, assert the false value, and assert authentication fails. The known-bad validates the directly read false but then decides stored active from a spread copy, retaining old true when the property is hidden. Thus this test statically distinguishes the intended mutant for its semantic defect. No execution claim is made.

Other tested obligations include normalized registration and lookup, input/result ownership, missing/inactive errors, undefined/empty patch notifications, atomic invalid multi-field update, duplicate watches, callback-order snapshots, current-dispatch unsubscribe/new-watch behavior, per-listener snapshot isolation, and removal/no-op emission. No contradictory oracle or compile incompatibility was identified. The suite does not prove every possible behavior, but there is no concrete missing gate obligation requiring a new universal test cycle.

## Seven criteria

| Criterion |0064 |0087 |
| --- | --- | --- |
| Prompt clarity | Scoped positive: explicit supported direct-read patch domain, ID retention and undefined rules. | Positive: full public schema, errors, normalization and dispatch rules. |
| API consistency | Reference coherent; test readonly assignments incompatible and placeholder error unsupported. | Positive: reference/test signatures and specified mutable Account fields agree. |
| Independent test origin | Verified request/output chain; oracle quality still blocked. | Verified request/output chain; static tests align with prose. |
| Non-triviality | Positive: coupled reservation state, foreign keys, collision/order and ownership. | Positive: normalized directory plus duplicate registrations and snapshot dispatch. |
| Idiomatic code | Positive static reference; direct field reconstruction and Map storage. | Positive static reference; typed helpers, Map state, per-registration entries. |
| Dependency isolation | Standard TypeScript/ECMAScript APIs and local assertions only. | Standard TypeScript/ECMAScript APIs and local assertions only. |
| Realistic known-bad failure | Plausible hidden-seat bug, but no distinguishing test and common harness failures. | Plausible hidden-active bug with a direct independent distinguishing assertion. |

Recommendation: preserve0064 as quality-held pending an immutable successor test correction/augmentation. Carry0087 to main's fresh pinned sandbox reference-pass/mutant-fail verification and remaining admission gates. Do not reopen original coverage or lift either immutable parent hold.

## Evidence hashes

Candidate files reside in datasets/cache/expansion-v1/versioned-recovery/r1. Hashes are SHA-256.

| Object |0064 |0087 |
| --- | --- | --- |
| Parent canonical candidate | b282271869c48b1390be6822cad7841c19d1ae211a3f378ea186e65c197d9f39 | ddaa661359f01faf3d8e72ad106469dbdeddc378af9923560d2cbe1a39bc4f27 |
| Derived candidate file bytes | 677cbeeea27fd339df663801504b2adb1c3a63cf64555868ead500c2c053d7e3 | 7bf68f2c077f442710ddf9836bee137b4d44423a812b88315fd25eef9ba6cd52 |
| Prompt | 2f3b045934241f6f9324d27ad37a61083d00374be73c40ffb875093d77520750 | df06575afe33210ee1bac247c7d84175eee961c4133735789000b77fd23013c8 |
| Reference | 7097938eae44473878cd0ef2ad01544fcaf2da9f86620df80a48ad793b010f96 | 6286c2e9490d7fb76d3a2376c938817c80ec3fab6b0ea2174b654332fe908b65 |
| Known-bad | 3ddea3ecf89890379bae413771ae7c00e5512f715ce1a036400fe0973ee99768 | 740d3dabd39f80dd0d348975c921d0d5d49973df70fc1ed97973f5a07da99417 |
| Independent solution.test.ts | 0d4b9199f5e75d798e5a6a1843ed93b7e20cee3c7c7528a785fcadf77cfb7ad5 | f05b730c30a61a6357f6ae2db408a12ce62167b6bffac9feb5b73088e2f1d330 |

- typescript-recovery-architect-evidence.json:6d9db20f8c4291fa4d483912f3f022e31aaff8c69ca61a15a551a7f58013e65b.
- typescript-recovery-independent-tests-evidence.json:d8b8a835cbd6148cf4df0c664895c0dda8d3f0d82f15fbd52e98fcdd8252e95e.
- Original corpus:680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
