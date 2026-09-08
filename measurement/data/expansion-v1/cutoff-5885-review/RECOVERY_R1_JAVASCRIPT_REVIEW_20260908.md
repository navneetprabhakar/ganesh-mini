# Recovery r1 JavaScript independent static review — 2026-09-08

Scope: only `exp-v1-recovery-r1-javascript-generation-0014` and `exp-v1-recovery-r1-javascript-generation-0270`, their exact original parents, request/plan bindings and archived JavaScript architect/test-author evidence. Full prompts, references, independent tests and known-bad implementations were read, together with the original equivalents. No candidate code was executed; all failure predictions below are static. No original hold is cleared and no new unique-original-row coverage is claimed.

## Decision

**Both current recovery artifacts are blocked from a positive quality decision.** Their references implement the targeted preservation corrections, but the new test files contain reference-conflicting assertions and lack witnesses distinguishing the correction from the supplied known-bad. Independent origin is supported; independent origin alone does not establish oracle correctness or meaningful mutant rejection.

| Recovery suffix | Correction completeness, statically | Blocking test finding | Disposition |
| --- | --- | --- | --- |
| 0014 | Explicit required-field materialization in constructor/add/edit preserves directly readable required strings that object spread alone omits. Absent-key edit returns the original registry before irrelevant changes validation. | Existing-key `changes: []` is required to throw by the test, while the reference accepts it as an object with no applicable changes. No hidden/inherited required-field fixture or absent-key malformed-changes fixture distinguishes the recovery from the original implementation. | Blocked: unsupported/narrowed oracle and correction-specific test adequacy. |
| 0270 | `Reflect.ownKeys` copies every own dictionary entry into null-prototype output; unaffected record identities and order are retained. Required affected-record fields are materialized explicitly. | Replacement tests demand `metadata` and `note` extras retained, while reference and known-bad reconstruct required fields only. Neither test creates a non-enumerable dictionary entry, so the original required-entry-loss defect is not witnessed. | Blocked: oracle/contract mismatch and correction-specific test adequacy. |

## 0014 detailed assessment

The unchanged specification requires four usable string fields, immutable copied entries, duplicate rejection, selective editing, sharing of unaffected entries, absent-key identity and reference-preserving search. Extra fields **may** be retained; retaining every extra is not mandatory. The reference validates ordinary property access and then explicitly sets `key`, `code`, `owner` and `openedOn` after spreading the entry. This repairs hidden-own and inherited required-field loss for constructor/add and retained fields on edit without imposing universal deep copying. Whole-target non-triviality remains supported by interacting lifecycle, validation, copying and identity rules.

The new test iterates malformed changes including `[]` for an existing key and expects `TypeError`. The reference's non-null object guard accepts an array; its allowed-field loop sees no own changes, producing a copied entry and registry. The prompt does not expressly prohibit array-valued `changes` and says other properties are ignored, so this assertion is not a supported reason to change the reference merely to satisfy the oracle. Tests also require retention of an entry's extra fields despite the permissive wording; current reference retains ordinary enumerable extras, but the assertion still overconstrains otherwise valid alternatives.

The known-bad preserves the original spread-only copy and validates changes before checking absent-key identity. Current tests supply neither non-enumerable/inherited required fields nor malformed changes on an absent key. Ordinary constructor/add/edit cases do not distinguish those differences. Removing the array assertion would not by itself make this a correction-specific suite. No executed pass/fail is claimed.

Required next test work: specification-derived fixtures for directly readable hidden-own/inherited required entry fields through construction and addition; a valid registry with hidden required fields through edit; preserved unaffected identities; and absent-key malformed changes returning the identical registry. Own non-enumerable allowed changes are also a useful explicit property-access boundary. Do not invent an inherited-patch guarantee or deep-copy obligation. If using multiple known-bad differences, each should have a meaningful witness rather than relying on an unrelated oracle failure.

## 0270 detailed assessment

The unchanged normalized-state contract requires new dictionary/root and only affected-record replacement for pin/unpin, preserved order and unaffected entries, validated atomic replacement, and no input part-object retention. A valid external null-prototype dictionary can contain a non-enumerable own entry. The replacement of `Object.assign` with a `Reflect.ownKeys` copy resolves that entry loss; explicit affected `id`, `label`, `hours` fields resolve required-field spread loss. `__proto__` remains a data key. Whole-target non-triviality is supported by normalization, validation, transactional replacement and identity rules.

The new replacement test constructs parts with `metadata` and `note` and demands those extras in `deepStrictEqual`, including metadata reference identity. The reference returns only `id`, `label`, `hours`, `pinned`; the original known-bad does the same. The exact approved recovery request explicitly excludes arbitrary extra part-field preservation as the held defect. Thus this test cannot establish success or meaningful mutant rejection: reference and mutant both fail its extra-field expectation before any recovery witness. Resolve the oracle against the approved required-field contract; do not silently broaden recovery to arbitrary extra-property semantics. The phrase “copy each part” should not be used to override the already bounded parent adjudication without an explicit derived-contract decision.

Current special-key tests are useful but use enumerable generated entries; they do not exercise the difference between `Object.assign` and all-own-key copying. Required next witness: externally construct null-prototype `byId` with non-enumerable `engine`, enumerable `wing`, and order `["engine", "wing"]`; pin/unpin `wing` must retain `engine` and its identity while only the affected record/root/dictionary change. Add directly readable hidden/inherited required part fields at replacement/affected-copy boundaries. Continue ordinary null-prototype, `__proto__`, atomic replacement and identity tests. Do not demand property descriptors or arbitrary extras beyond the actual contract.

## Seven-criterion accounting

| Criterion | 0014 | 0270 |
| --- | --- | --- |
| Prompt clarity | Required lifecycle/copy contract supported; test-only array prohibition and mandatory extras are not supported. | Required normalization/copy contract supported under approved bounded adjudication; new extras oracle requires correction/explicit contract resolution. |
| API consistency | CommonJS exports and reference operations match; test/reference changes-array mismatch blocks current artifact. | CommonJS reducer and required state transitions match; extras oracle/reference mismatch blocks current artifact. |
| Independent test origin | Supported by archived specification-only test-author prompt and exact output binding. | Same. |
| Non-triviality | Positive: complete immutable registry and interacting identities/validation/search. | Positive: normalized reducer, transactional replacement and structural sharing. |
| Idiomatic code | Scoped static positive: standard object/array operations, explicit required-field copy. | Scoped static positive: null-prototype dictionary and all-own-key copy. |
| Dependency isolation | Static standard-library/CommonJS positive; sandbox execution still required. | Same. |
| Realistic known-bad failure | Mutation is realistic, but current suite lacks a correction-specific rejecting witness. Blocked. | Mutation is realistic; extras failure shared by reference is not meaningful rejection. Blocked. |

## Lineage and immutable bindings

Both candidate prompts equal their exact original prompts. Original canonical record hashes below reproduce the plan bindings; rights match the parents, and source revision/record hashes are preserved with derived recovery lineage. No ownership decision is reopened. Architect output `problem`/`reference_code` equal candidate prompt/answer, and independent output `test_code` equals candidate `solution.test.js`. The independent author prompt was read in full: it contains only exact derived IDs/specifications plus runtime/test instructions, not reference, known-bad or original tests. Both evidence records report return code 0, no timeout, no event parse error and no disallowed tool item types; those are author-run metadata, not candidate execution evidence.

SHA-256 values are exact file bytes unless marked canonical/content.

| Binding | SHA-256 |
| --- | --- |
| Original `cutoff-5885/final.candidates.jsonl` | `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec` |
| `recovery-requests-r1.json` (matches plan request hash) | `c7fed0810f7fa42b2b0e5c56ccf9e0afe2c0b239db8aa529c5c0744f58e6b37d` |
| r1 `plan.json` file | `a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1` |
| Plan embedded canonical plan hash | `ff64db89a09b39d0ca9b19f2b7231ded79cbff17823b21be51d36ea4c0647fdb` |
| Bound recommendation evidence | `adc9832180fda515790272be9305841a4b9da4356b336cafaa0843bbe3ba0b3f` |
| r1 `run-contract.json` | `359ed51b2db8f6e4e169b352435a822670d35376fb5d1d705999a2ba310839ce` |
| JavaScript architect evidence file | `68fb4438d1c08bf39494b034929dfb99001fca3d547d8468ae1a7174815ff6c7` |
| JavaScript independent-tests evidence file | `f593ecf2501bdd3449520223de5588c7975425a845b54cb68ae8117c17cefe1c` |
| Architect prompt content | `cfdd8c5b69163529bd30f43e6feee4ed4b4b6bccb6bd76b990efcfd6e7e0db68` |
| Independent-test prompt content | `db8b966476b0b544315d75881936bc60e9f780eed341bce9914149d2be1e9fd0` |

| Content binding | 0014 | 0270 |
| --- | --- | --- |
| Original parent canonical JSON | `e545f4c21fb6f2b5cbbd468b700b96f652be2cc4c7cb3a1a7b0e36678e3931e8` | `a7b809fba05e9a23cf9977b895faa05a982b73cf871ff9bcc8e70f99b42820cd` |
| Recovery candidate file | `8628a0772a479aa4ad8c7a12fe549b2d514837245aba596ca9c99452811dbc24` | `0ccf369943db8df30106032524abb8e53f2b7c3bfbacf59f51c91c3b189fcdfe` |
| Prompt content | `6365dfb0f4ff6941ebe8b2cd2aa6a255224f600c5151f16b2976823f1878cacc` | `e1f5f3610d02b4c5ac79babb64c6862da58b21af8b6f333f63feff086c57097a` |
| Reference content | `d179ac45d8be8f63af8e742704a2ad8704b4880312d35de41f2544db74ed3551` | `c47477ae5bbe2f2abde5006f3e7700ca5124247b9fd652bb8d27da6bfa02e464` |
| Test content | `bf8dfb0afb40eec53a4dbbd814778e3bd5bbc10863994ee40f32c1898d89b2d7` | `80cb408ebddcf45a7c2ba89ae3d421879fad6309a7bd0f8b2493b8ddbc426d23` |
| Known-bad content | `f00baa13dd4a65cf6adb69e89c4b41f317c7abe27a8933f109fe344146f980e9` | `d72c38f3d309f37d2b9d402e69b911759c131b4042149727bfcc489a061aa8cc` |

Runtime declared for both: `javascript-node-22.23.2`, 1 CPU, 512 MiB, 64 PIDs, 65,536 output bytes, 60 seconds. Main owns any execution, regenerated immutable artifacts, sandbox evidence, separation/admission gates and ledger updates. Counts: 2 reviewed recovery artifacts; 2 blocked current artifacts; 0 admission recommendations; 0 candidate executions; 0 new original-row coverage.
