# R20 provisional test-only correction — 2026-09-08

Current gate: recovery quality qualification, not admission or training. Main accepted the two R19 test-scope holds. These drafts propose exactly one bounded test correction for those same original parents. No reservation, teacher call, generated-code execution, central edit or new selection was performed.

Only intended implementation artifacts are recovery-requests-r20-PROVISIONAL.json, recovery-test-feedback-r20-PROVISIONAL.json and this note. Main must validate/finalize before use. The prior run is datasets/cache/expansion-v1/versioned-recovery/r19, not R12. This is the first test-only correction from the fresh R19 architecture; no repeated critic loop is authorized.

## Scope

| Original parent | R20 derived ID | Correction |
| --- | --- | --- |
| exp-v1-python-generation-0717 | exp-v1-recovery-r20-python-generation-0717 | Add []/{} invalid-kind ValueError and MappingProxy reply ownership witnesses, retaining all valid R19 controls. |
| exp-v1-rust-generation-0487 | exp-v1-recovery-r20-rust-generation-0487 | Instantiate Debug+Clone+PartialEq+Eq for all three public types; remove Debug-text assertions; retain existing semantic witnesses and make the approved tiny 10/20 ->15 different-query-arity fallback explicit. |

R19 references are statically positive. The Python unhashable test excludes a hashing-based invalid-kind regression even when None/1 pass. The reply MappingProxy test closes the specifically approved second schema branch; it imposes no wrapper-retention requirement. Rust assert_eq only checks PartialEq/Debug, not Eq. Actual generic bound instantiation establishes the required marker trait without layout/output assertions. Existing mixed-arity 3/9 ->6 witness was already semantically sufficient; the additional 10/20 ->15 example is an approved tiny redundant control, not a new domain. No reference/mutant implementation code appears in critic feedback.

Both selections use oracle-rebuild as required by scripts/data/correct_recovery_tests.py. That script was fully read. Its feedback keys are the exact R20 IDs and previous_candidate_sha256 binds canonical R19 candidates. It copies prior candidates and replaces the independent test file, rebinding IDs/source lineage while preserving specification/reference/known-bad bytes. A prior correction_attempt triggers the one-correction guard. Main must check the current immutable prior contract before launch.

## Exact bindings

- Review: measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R19_REVIEW_20260908.md; SHA-256 7ea6c5727474ee9ce80c4f5e8241dcac48881082253f0554d68f7e0433ff6f72.
- Approved R19 request SHA-256 c174093a3eb792c57d0940c656ae0e8cef1447702bd9afeff5e9ed1733279886.
- R19 plan file SHA-256 401d56a11f2ca2929eb42be7ffb36fe694cfded2500ed56a96759560b8b65f62; embedded plan seal ef6c38e0eadab9fa90f94dcfcec012c01160c8b9d1c5ff1adfc33b3b94b087e2.
- R19 run-contract file SHA-256 a0b4a39242bee4710967f7d01a0d6031bf4a81401f3aca98bcab09c80b80c6a8.
- Original corpus SHA-256 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec; frozen hold ledger SHA-256 9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee.

| Binding | Python0717 | Rust0487 |
| --- | --- | --- |
| Original canonical | 4432a25372e0cd1ef3da2401dbab9b82886ecdeb5d0a791dbf22d3fb4768e3e4 | 9ee8d243d8728a71c43c64ab9122fceb8e0db37aabc8e8e1f055ff82fb726ad4 |
| Previous R19 canonical | b624bad0311feff0e19e0ded806618f78f56d6d6515dfd516c990d7093e1794a | 047f9334346c3c5711dfa3577f23decd78373b5f3e819fb86c98645c40711179 |
| Previous R19 candidate file | 7cf1a28c74d1a2f171775e95889039a4fecb3332a145914797762def3cf57b20 | bdb6610f5848b885ee103e6aa96b6ef0ca2c39f2dd12af23e72c7ceecc9b5c09 |
| Unchanged prompt | 49701ab781d8b5d856d109aab003eefd3548095d2471b20e8975195434763be5 | 0a5e39e8643655c11636eef891770f507145c632582fb12b94fb7ee405b62db2 |
| Unchanged reference/answer | 7c76f2a9375c1b67da0e3b45de6a0f1aebb6abab43376c6afcb2e486bcd13eb5 | 241b3cf5acdeb01cca500b0e50abadf8179bdaee62128608b46d9a71f570633a |
| Unchanged mutant | 4d7a5924ea9389791e9eae3edf56150c753281cd4df093b610daa4ca5eace301 | 90f5aa84e99e7a1c4b4da8a4bb6df028b51ef2b6a3603b5a10970017931c6b85 |
| Previous tests | e1e8d8bff3c458df78e943b52f9e0ec2be5c5c097afdc0792753c3733758640e | 345a1a02f5bf633b9cd766f2a04df3e796e12a67a1919133cb1b1c8ea23a5df1 |

Full source, rights, architect and independent-author evidence hashes remain bound by the R19 review; preserve original McEval row-04048 / row-05991, revision 57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0 and recorded rights. No new provenance decision.

## Required downstream checks and hard stops

Main must validate exact two-parent selection and previous hashes, finalize requests, and use one test-correction attempt. After generation, separately verify byte preservation for both user/rendered prompts, answers/references and all mutants; verify new test provenance and test quality. Fresh pinned network-disabled sandbox reference success and realistic mutant rejection remain required, together with deduplication/evaluation separation and the separate admission seal. No source change or revised contract is authorized by this draft. A mismatch or second-critic request is a stop, not permission to silently regenerate architecture.

