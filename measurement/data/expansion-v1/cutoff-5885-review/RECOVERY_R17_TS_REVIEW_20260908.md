# R17 TypeScript independent static review — 2026-09-08

## Result and scope

Gate 2. Exactly six corrected derived generation candidates: 0036, 0078, 0148, 0228, 0300 and 0345. **Six scoped static positives; zero holds.** Full current specifications, references, independent tests and supplied mutants were read against the R12 review and approved R17 feedback. This is derived-artifact quality review, not new original-row coverage, execution evidence or admission. No candidate execution, critic call, cloud operation or central mutation was performed.

## Preservation and provenance

For every row, R17 problem, reference code and complete known-bad objects are byte-identical to R12. Each R12 canonical candidate hash equals the approved feedback's previous_candidate_sha256. The critic received exactly id/problem/test_code per item: problem equals the current specification and test_code equals the previous R12 test. Its separate specification-review text equals approved feedback exactly. There is no separate reference or mutant field in that input. All six are generation tasks, so no embedded repair implementation is exposed. Normalized critic output equals the stored test content for each candidate.

Stored correction prompt/output hashes recompute correctly; returncode is 0, timed_out is false and disallowed_tool_item_types is empty. Those are author-process checks, not verifier results. All approved source fields except explicit versioned transformation are preserved, and rights equal both the approved plan and prior candidate. All five rights flags remain true. Dataset: Multilingual-Multimodal-NLP/McEval-Instruct, revision 57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0. Each plan-bound prior review hash matches the current evidence file.

## Seven-criterion assessment

All six retain clear self-contained specifications and named APIs; independent behavioral tests now exercise the scoped defect without the earlier unsupported oracles; whole tasks remain substantive, not elementary solely because their repair is small; references use ordinary typed TypeScript and standard-library mechanisms; no external dependency, network, filesystem or environmental fixture is required; and each mutant is a realistic single behavioral regression against the retained contract. These are static assessments. Runtime compilation, passing reference tests, meaningful mutant failure and final admission remain main's separate gates.

| Candidate suffix | Disposition | Whole-target substance and decisive correction |
| --- | --- | --- |
| 0036 | Scoped positive | Token localization, frozen snapshots and conditional asynchronous loading; invalid metadata with a valid address must reject through the returned Promise. |
| 0078 | Scoped positive | Closed enumerable-own schema and deterministic validation reporting; each required field is individually hidden and must yield its own issue. |
| 0148 | Scoped positive | CREATE/UPDATE ownership, format checks, normalized uniqueness and ordering; malformed accessLevel precedes the appended duplicate-email issue. |
| 0228 | Scoped positive | Recursive validation/storage/getter isolation; actual own __proto__ values and hidden own nested values survive copying. |
| 0300 | Scoped positive | Gregorian validation, whole-input validation and detached range filtering; year0099 acceptance distinguishes native Date.UTC remapping. |
| 0345 | Scoped positive | Normalized catalog lifecycle, patch semantics and snapshots; blank amend/drop use the invalid-code error without mutation. |

### 0036 — Promise settlement and integer domain

The corrected test directly captures loadLocalizedResource with valid address and blank metadata key, rejects any synchronous throw, checks a returned Promise and awaits TypeError. Invalid language cases independently check Promise rejection; synchronous localizeMeta validation is retained. Number.MAX_SAFE_INTEGER+1 is now accepted on the missing-address path, consistent with non-negative integer rather than safe-integer language semantics. Missing, blank and nonstring address paths bypass bad metadata. Repeated/unmatched tokens, exact address preservation, freezing and nonmutation remain covered. No async-constructor reflection or extra numeric cap remains. The unchanged synchronous-validation mutant violates these settlement witnesses.

### 0078 — Enumerable required fields, not a hidden-extra ban

Each of recipientCode, crateCount and priority is independently defined as a valid but non-enumerable own value on an otherwise valid ordinary object. Its field issue and undefined result are required. A non-enumerable extra remains accepted, correctly distinguishing the required-field membership contract from an invented ban on all hidden properties. Boundary values, sorted unknown-key then field issue ordering, prototype restrictions and copy isolation remain tested without exact generic-message requirements. The mutant's direct property reads incorrectly accept hidden required values.

### 0148 — Combined format and duplicate ordering

UPDATE with email a@b.com already present and empty accessLevel requires fields accessLevel then email and the exact promised duplicate message. A second combined case puts an unrelated account before the match; separate existing tests reverse the account order. The second combined fixture is not a literal reversal of the first array, but together these supply the intended deterministic-order control and a direct distinguishing witness; that syntactic difference is not a quality hold. Own-property update behavior, current-ID exclusion, trimmed/case-folded uniqueness, fresh issues and CREATE validation remain intact. No new email grammar or exact generic format-message oracle is imposed.

### 0228 — Real property witnesses and recursive isolation

Tests construct real own __proto__ data properties with defineProperty on null-prototype input, both at palette and nested-rule levels, rather than relying on object-literal prototype syntax. They require own membership and exact values after storage, after original mutation, and after getter-copy mutation. A non-enumerable hiddenBranch containing a non-enumerable concealed value exercises readable own values recursively. Normal nested copy controls, insertion order and unsupported recursive values remain. Tests do not require returned prototypes, descriptor layout or freezing; symbols stay outside copied string-property semantics. Assignment-based copying loses the bounded __proto__ witness.

### 0300 — Early year, required-field copy and trailing hole

Both an empty range and a matching charge in year0099 are accepted. The matching result checks all four fields and detached identity. A valid non-enumerable own id must be copied; a genuine trailing hole after a valid charge must throw TypeError while preserving input length, contents and hole membership. Unrelated malformed charges are validated too. Leap-year controls, raw nonempty IDs, finite MAX_VALUE amount, negative zero and inclusive ordering are retained. No year0000 success/failure oracle or new calendar convention is introduced; the inherited unresolved convention is not expanded by this bounded correction. The unchanged Date.UTC-based mutant rejects year0099.

### 0345 — Exact blank-code semantics on both operations

After insertion, amend with a space-only code and drop with a real U+0009 tab require the promised Feature code must not be empty message and unchanged snapshot. The source test uses a JavaScript tab escape producing a tab, not a literal backslash-plus-t value. Nonblank missing codes still require Feature not found. Normalization, duplicate insertion, default true, false patches, absent-field retention, ordinary sort and snapshot detachment remain. There is no out-of-type patch or explicit-undefined deletion oracle. The mutant reports the missing-code error for blank amend/drop, directly violating the test.

## Evidence bindings

All hashes below are SHA256. Canonical hashes use sorted compact UTF-8 JSON. Candidate file paths are under datasets/cache/expansion-v1/versioned-recovery/r17/.

- datasets/cache/expansion-v1/versioned-recovery/r17/plan.json: 60c02db8869c80c1515e2216205ac11a45b357206563f62f499d8b67b3ee02ee.
- datasets/cache/expansion-v1/versioned-recovery/r17/run-contract.json: 1df6b4c2dedcd278281f61b6594be0f2303cc047eff1dd91722b1925d6364f27.
- measurement/data/expansion-v1/cutoff-5885-review/recovery-test-feedback-r17.json: adb48971f9f414d4feb1603c7143aa15723aeccee52fb20df7eafafb0489a068.
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_JS_TS_REVIEW_20260908.md: 835852a52c537556c37389b692902bb8a48e2552a80d6d01e6baad2a7ae2cefa.
- typescript-recovery-test-correction-evidence.json file: 56d42fe76bc1b4a8bb2329d75224b0e1f43fac57db96b9d3cadbceaf1ce8fafa.
- Correction prompt: 73daa39dd33ac77192ddabfa23d60d8eae5b81c757d716da764d3e33429d9e36.
- Correction final output: a6aa40b7a3f60d84578c6f10f463c38478af9d4a4e5f6f1fa7cab4608a4c8266.

### exp-v1-recovery-r17-typescript-generation-0036

- File exp-v1-recovery-r17-typescript-generation-0036.candidate.json: bde83a4642d589ffedcbdd7e22e78a3cc37a9491b556262f920dffff736261f3.
- Current canonical: 325358dc4d1d9ea54240d755ba980cf6c389e5d438c37472c5f246d9d8add321.
- Previous R12 canonical: 1e5b726e348eaf8e03e6a94d40bccd462cd437fed21bad801afaf82d6963c081.
- Original parent canonical: 8972e476c5337d9d93eea39c6398d1678e1563b23fc3db4c6696fcc2867ae185.
- Source row-33246: 57c4ad08ebf11a051480a1d8cab74af0fab92c508e7ed50a723fc7c632263e29.
- Problem: 585548abc47e31309c840476ff91e73b438bf26c5fc5f0f056df63f45250cca1.
- Reference: b88e54a7821c4eb976c59de1fd4a0dfff0ecbea08e0bf2c4660dd0ab0bc63e4e.
- Supplied mutant: d3e839802541d9bf12fbe98ceadaf422753c5f963183442e4d89d7321ff252b2.
- Corrected test content: 20aeb3ecc43f31c86746678d9e15529af8d042e02fced56938a36879c7ee6580.

### exp-v1-recovery-r17-typescript-generation-0078

- File exp-v1-recovery-r17-typescript-generation-0078.candidate.json: 3aa05df73384bf843d7092d35dce53ad793ab1fe6c5a890cafac9dc7f8b3a1c3.
- Current canonical: 5e00c78bd376b9fcc064c848e2025c4fdb40f3723b1cbc777790a1d882e2749e.
- Previous R12 canonical: 4a51c3ffc5a78dc90ed56b95c9bbcc692142f7e8c38f39826c382d54d8a5ba11.
- Original parent canonical: bc13b1006c2e4895e294d759248d64dedf1b02618c6aa5228fa1cda2efe34843.
- Source row-33239: 1865f38162eecee1a51da8527676f9dc6e9da94e9d3cc75ee65cc00f7b1aba43.
- Problem: e3bc968f548a031e362185edf570d63a7f440a9f09c7d94d644fc411029f0406.
- Reference: 361f8a99debb2696133ccca0c7636dd3864a6c90b20b40ba04c75cdb570cd9cb.
- Supplied mutant: a1fb1ac7325854469d6f4350af649949e5874edf5bff8b97b7792dd2f122deb8.
- Corrected test content: 9f100cd0eda95dc4b9202c4a90ccdf50513e301da2300308a2258e75268e12c6.

### exp-v1-recovery-r17-typescript-generation-0148

- File exp-v1-recovery-r17-typescript-generation-0148.candidate.json: aaf7fa7e494831aeac47af61966465d303d5ccac8d61c42f3079df6e04a240e0.
- Current canonical: d43a408a0c707efb8af4082f3463257620b6a89776dafcf75f0ca1dfa0cd53c8.
- Previous R12 canonical: c16a29e263fdd74eddff40899c7d4840a9087b2af32e53563c969c45433ecf19.
- Original parent canonical: c98c452f81d3b7cf707118e7ae6fca5dc56bf18f91d2d3d817358d678dc53c4e.
- Source row-33221: 4110f601042fc712d8c1a357da880b6dacbfb9c4c591e5fe1699f07b27ebbcef.
- Problem: 29bb13be4a80ce2740873569511d61a836f5c957210ff179dabfe1d3e2321308.
- Reference: 9e2b8422c37e474b6215930c33819797c407900a97654a6100bedb70c7bc4e11.
- Supplied mutant: 97c48cbda4736d192e366eec734a838f94cf9bb20c4e728ea97ae1016c718133.
- Corrected test content: f7f60c5ce2f7a0b7b27032a36c2b506ddb376fd6924f9afc0b7c2db450bd0e1a.

### exp-v1-recovery-r17-typescript-generation-0228

- File exp-v1-recovery-r17-typescript-generation-0228.candidate.json: 266954f774e88f331c223b68fc61329e128efc43fd39686d072a6ce4c47b006e.
- Current canonical: 01c02be988582f45abe394dc0aab1f88c471b5fa3b62bf7941d015ab205fa9fa.
- Previous R12 canonical: 5cb90b8be179de7906a5fe1d9ab5f15d5268be8c2e8dfec604a0b0b353ac7f51.
- Original parent canonical: c823a5ec5608671e167047a4b6d9cd8c85c8f5a8c8506f3cd242e34c03e9736c.
- Source row-33160: f7820f1f83488c20c59a7935a0b6cfbc828f93dcc8b36a43863e39b5e11f8b41.
- Problem: 8c9b8d6ddbb4bd99d12d71d05147fa07cb79ce6277fabfcb3db6c7440af1d959.
- Reference: b2d8763043f63b15e62e1a273406bdfae05c52049a0f5ef2efea937205da3849.
- Supplied mutant: 4dcd87ff8abdec447442ffa6b424db5d370fb39e615bf6c0bdf94a9f1aaa095c.
- Corrected test content: 4a9080f3a252644cbce714a107aede9f3c99f12c566df028bd6bad658f90c218.

### exp-v1-recovery-r17-typescript-generation-0300

- File exp-v1-recovery-r17-typescript-generation-0300.candidate.json: 5051e6bd96c09808a48f2dae4b283e7464f23ad63ba3e314414218f880d9c176.
- Current canonical: b3850387bcdb7495f956757f2f2f3b26d1f1093d05022a23321679da45f119e4.
- Previous R12 canonical: fe47313e0a75fcb670be5727bbfce5e3bd8acd4b6671f680da48dda8e5af5083.
- Original parent canonical: f3cfdd59bbe0196a94c80a91a34f282f891a78519ffae45c448f154d35b60f37.
- Source row-33063: 448c07e56a7a368aceb9b094f845bffd840f275ea0bf042c8cbcfd8f4d138fe9.
- Problem: b299fbea0dd30181fb9546e50144b724a0906ff50172ba42602b76d67752d004.
- Reference: 70ef35f99d1820eb951a7b681bd4ed9c7d6f0a1f1f00bfd4fd4ddb4750d84165.
- Supplied mutant: 61eadef8a88b9e8022f5e83f11b0682006789ebefa17c8dcffbdfa6a6f1197c6.
- Corrected test content: 58130492ec553d50e45958e0c2e43ce5e5459910e109caea6b9544660a54ea2f.

### exp-v1-recovery-r17-typescript-generation-0345

- File exp-v1-recovery-r17-typescript-generation-0345.candidate.json: 3ee5419a54f31786028dae66d4caf377f729a9dfc15363cf1c7d713b5cb4fe41.
- Current canonical: 830eea29e999855502b32a3bfb231a390db2e7d430df753b4aef61ef7826ab3c.
- Previous R12 canonical: c4324b3e8808bd6abe72039396b84b3306cfe08c1617658fcc943a37d0a0d97f.
- Original parent canonical: 9b7562bc82f90801804afde0d3952e1768dcffcba1458746d4622798fa62d77a.
- Source row-32603: 22e9e47c211df8040779db53edf1e81b2f77230926f2b3db79e358287e7db4b7.
- Problem: 5eff049a5bfe40f537c3b57455d44dfedb927481e94f68e235aa888ebb34a558.
- Reference: f69c423b08b88c778e2bdbb754065bf25eb068239d2ff3a139c2caac72400335.
- Supplied mutant: 02b843f569f7d0df8720464c28f614be7286f1b0e4b015184e891a67609dbbc4.
- Corrected test content: e68ebceb4210374f0f50c7b11c1a242e30c8f3c3490dee4ce33ee16e1e9bb57d.

## Handoff

All six are supported scoped static positives. No remaining test-quality hold or automatic further correction is proposed. Main must attach its independent sandbox results and admission/lineage checks before any inclusion; original parents remain subject to the existing hold ledger until main's versioned process resolves derived admission.

