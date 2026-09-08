# R12 Rust independent static quality review — 2026-09-08

## Result and boundary

Gate 2: exactly ten derived Rust generation candidates. **Two static positives (0092, 0509), eight derived quality holds (0099, 0141, 0177, 0364, 0449, 0487, 0630, 0697).** Seven holds concern tests/oracles/discrimination; 0487 has a reference public-trait omission. References for the other nine are statically consistent with their scoped contracts.

No candidate executed, generated, admitted or mutated. Zero new original-row coverage; originals remain held. R13 and other lanes are untouched. Main owns sandbox results and subsequent decisions.

Read complete original prompts/references/tests and mutants (unchanged source plus complete diffs where appropriate), complete derived prompts/references/tests/mutants, approved R12 plan/selection and the prior Python/Rust proposal. Original evidence is bound below. Static expected compile/failure behavior is not reported as executed evidence.

## Integrity and independent provenance

All ten canonical parent hashes equal approved plan records. Original source and rights objects match plan parent bindings, and derived source preserves every field except the explicit lineage transformation. All five rights flags remain true. Authorized source: Multilingual-Multimodal-NLP/McEval-Instruct revision 57bd46727e49ac3e2890218a146d35c2454a8496, license CC-BY-SA-4.0; no ownership decision reopened.

For every ID, architect problem/reference/mutant equals emitted candidate content; independent test output equals solution_test.rs. Independent test-author task objects contain only id/problem and exactly match the emitted specification. These generation prompts expose no reference or mutant. Separate architect/test calls have return code zero, no timeout/disallowed tool item, and valid prompt/final-output SHA256 bindings. Provenance does not certify oracle correctness.

All four strict reference-fix problem strings (0099/0177/0449/0630) are byte-identical to their original problems. Other derived changes follow the explicit approved grammar/API/arithmetic scopes rather than silently narrowing the domain.

## Seven-criterion assessment

All ten whole targets are substantive interactions, not elementary padding: delimiter validation/selection, transactional registry ordering, conserved ledger atomicity, label decoding plus ragged-table totals, tree validation/path arithmetic, allocation/error priority, model updates/prediction, ordered rule evaluation, exhaustive graph tours and multilevel descriptor parsing. All use only the standard library, with no external dependencies or hidden services. Idiomatic structures are generally appropriate; no universal allocation/runtime guarantees are invented. Independent provenance is satisfied for all; remaining API, oracle and realistic-defect obligations are resolved individually below.

### exp-v1-recovery-r12-rust-generation-0092 — static positive

Explicit extended delimiter-name grammar and Malformed-before-Duplicate precedence make the parser coherent. Reference preserves exact text, nonnested matching and whole-input validation; ASCII delimiter slicing stays on UTF-8 boundaries. Required FieldError traits are present. Hyphenated item-name and slash-containing a/b witnesses are legitimate under the explicitly broadened name grammar, not invented nested fields. Duplicate-then-malformed suffix, empty content, ordinary brackets, case distinctions and mismatches exercise the required interactions. The supplied original-reference mutant wrongly restricts names and returns Duplicate early; tests directly distinguish both. No concrete unsupported oracle found.

### exp-v1-recovery-r12-rust-generation-0099 — hold: test trait overconstraint and missing sorting witness

Reference correctly sorts complete qualified strings after constructing them, preserves cloneable ownership and atomic enabled batches, and ignores disabled malformed input. It need not derive Debug for RegistryError; prompt requires no such trait. Yet multiple successful setup calls use Result::unwrap, which requires the error type to implement Debug. The reference does not, so these tests are statically compile-incompatible. Use matching or is_ok where appropriate rather than changing the contract for test convenience.

The sorting test uses disjoint A and z_scope names: component traversal and full-string sorting coincide. No a versus a0 prefix-scope witness is present, so after fixing compilation the intended component-order mutant is not distinguished by the current ordering assertions. Required tiny witness: both scopes with tag x produce a0::x before a::x. Existing batch rollback/name checks remain valid; detached string and clone-isolation controls may be retained without a new private-state oracle.

### exp-v1-recovery-r12-rust-generation-0141 — hold: unsupported error Debug requirement

Reference correctly permits a destination exactly u64::MAX, conserves supply, validates transfers and rolls batches back. Full-supply transfer to an empty destination is a direct, sufficient witness of the actual mutant's artificial maximum rejection; lack of the separate one-unit return witness is not itself a blocker. No unreachable overflow state is fabricated.

However the frozen derived public API does not require LedgerError: Debug, while multiple Result::unwrap setup calls require it. The supplied reference happens to derive Debug, so the tests may run against it, but they reject an otherwise conforming non-Debug implementation. This is a test-only API overconstraint, not a reference defect. Use trait-neutral success extraction; do not add a new trait demand to the problem. Existing error matching, conservation and rollback oracles are otherwise justified.

### exp-v1-recovery-r12-rust-generation-0177 — hold: missing exact maximum-index witness

Reference's zero-based recurrence (26 times previous index plus 26 plus next zero-based digit) avoids the overflowing one-based temporary. All intermediate additions are nonnegative, so checked steps do not falsely reject a representable final index. Whole-label syntax validation precedes conversion; ragged presence, numeric-only summation, ordering and original f64 semantics remain intact. Required public traits are present.

Tests cover small columns and a vastly oversized label but never the label for zero-based usize::MAX. Both reference and supplied one-based mutant behave identically on those cases. Add an independent u128-derived short label for the exact maximum, checking empty/tiny tables without huge allocation, and the next index as overflow. Existing invalid labels and numeric-cell controls are valid; no float-finiteness policy should be invented.

### exp-v1-recovery-r12-rust-generation-0364 — hold: missing hidden-route arithmetic witness

Reference correctly implements the approved iterative root-prefix checked arithmetic, verifies tree topology/reachability and retains negative leaf sums. No recursive-depth dependence or unintended numeric cap remains. Current two-edge overflow/underflow and one_bad_branch tests are valid but are also detected by the supplied subtree-max mutant.

The distinctive shared-ancestor underflow is absent: edges [(0,1,-1),(1,2,i64::MIN),(1,3,0)] require None, whereas the subtree-max mutant selects zero at node 1 and returns Some(-1), hiding the other route. This tiny semantic witness is required. A 20,000-node depth test is allowed by the explicit iterative contract, but a potential recursive stack failure does not independently demonstrate the lost nonwinning-route arithmetic defect. Keep any valid depth test separate from claims about the arithmetic witness; no executed stack result is claimed.

### exp-v1-recovery-r12-rust-generation-0449 — hold: test compile overconstraint and missing late validation witness

Reference validates the entire allocation sequence before total/fee arithmetic, then preserves arithmetic-before-capacity ordering and exact funding boundaries. The contract does not require DistributionError: Debug. The empty allocation test uses build_transfers(&[]).unwrap(), so the emitted reference lacking Debug cannot compile with this test; use trait-neutral extraction, not new derives.

The validation-before-arithmetic test puts an invalid recipient first, which the old interleaved mutant also rejects first. It does not test overflow before a later invalid allocation. Add [('a',MAX),('b',1),('',1)] => EmptyRecipient and the analogous late zero allocation => ZeroAllocation; all-valid MAX+1 must remain ArithmeticOverflow. Current order/duplicates/fee boundary assertions are otherwise legitimate. No additional cross-error precedence is required.

### exp-v1-recovery-r12-rust-generation-0487 — hold: explicit public trait contract omitted by reference

Different-arity nonempty query fallback is correctly implemented and directly witnessed by the mixed query batch yielding [-9,15,7,7]. Atomic updates, empty-update noncreation, existing-model requirement and i128/truncating averages are coherent. Constructors and free wrapper match the approved clarification. Existing tests do not impose an unrelated numerical domain.

But the derived problem explicitly says to derive Debug, Clone, PartialEq and Eq where applicable after listing Observation, ModelError and ObservationStore. The store consists entirely of a BTreeMap<String, Vec<Observation>> whose contents support all four; all are applicable. Reference provides none on ObservationStore. This is a concrete inherited contract omission, not a demand for private-layout access or an invented trait. The tests also never check it. A test-only correction cannot supply missing reference traits; main should preserve this reference hold rather than declaring passage of current behavioral tests sufficient.

### exp-v1-recovery-r12-rust-generation-0509 — static positive

Clarified associated constructors, exact allowed-character grammar (including dot/hyphen only), suffix-boundary rule, kind filter and first-match ordering are consistent. Reference removes only the unsupported alphanumeric-presence requirement and keeps validation/ordering. Required enum Copy/equality traits are present. Tests use equality without Debug on enums; Policy::new returns String errors, so unwrap introduces no unpromised custom-error trait. Dot and hyphen policies directly distinguish the supplied old-reference mutant. Invalid host, valid subdomain versus bare tail, kind/order and borrowed-string controls have sound oracles. No private layout or DNS-domain restriction added.

### exp-v1-recovery-r12-rust-generation-0630 — hold: missing overflowing dead-end witness

Reference tracks overflow as state while continuing topology exploration, marks it fatal only at complete tours, and retains validation-before-traversal, exact names, oriented enumeration and lexical sorting. Public traits are fulfilled. This is appropriate exhaustive behavior, not a promise of scalable unrestricted graph enumeration.

Tests distinguish ordinary valid versus overflowing complete tours but omit an overflowing incomplete path. The disconnected case has only small weights and cannot expose the defect. Add A-B MAX, B-C 1 plus disconnected D-E 1 => Ok(empty); retaining the connected counterpart as CostOverflow prevents pruning overflowed complete tours. A bounded graph with an overflowing dead-end alongside a valid complete route can further check topology discrimination. Current mutant returns CostOverflow too early, but existing small disconnected/complete-overflow tests do not distinguish it. Current numerical and tour-cost arrays are otherwise correct.

### exp-v1-recovery-r12-rust-generation-0697 — hold: incorrect two-field tag-error oracle

Reference correctly uses comma field count and InvalidEnabled for a colon-containing enabled field. The a,on:off, assertion directly witnesses the intended fix; no custom Debug requirement is imposed. Ordered/duplicate tags, trimmed fields and empty tag field follow the contract.

One item in rejects_empty_or_invalid_tags_in_nonempty_lists is a,on::, containing only ONE comma and therefore TWO fields. The test incorrectly requires InvalidTag. Frozen specification explicitly requires WrongFieldCount whenever comma splitting does not yield three fields. This is not a choice of unspecified simultaneous-error priority. Correct that expected class or use a proper three-field empty-tag-list example such as a,on,::; do not change reference to accommodate the malformed oracle. Other listed invalid-tag examples are proper three-field cases.

## Summary for main

- Static positives: 0092, 0509.
- Test-only quality holds: 0099, 0141, 0177, 0364, 0449, 0630, 0697.
- Reference/API hold: 0487.
- No automatic critic, generation, sandbox or further selection performed. Compile and mutant outcomes above are static expectations only; main must attach actual diagnostics independently.

## Evidence hashes

- datasets/cache/expansion-v1/versioned-recovery/r12/plan.json: 0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121.
- datasets/cache/expansion-v1/versioned-recovery/r12/rust-recovery-architect-evidence.json: d361ff8a8f7693b55695ce3e5d52579520cdd6dc925aee999b486e70b9820a53.
- datasets/cache/expansion-v1/versioned-recovery/r12/rust-recovery-independent-tests-evidence.json: ac2c5a1a30c14f8ce5ef53e851a2840a61069ce1cd1e8d4aea9e5bf1ef2f6a90.
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_SELECTION_20260908.md: 58b6a5cb6646e03ba4ae0d103b51ff638ea4e3f6b847711c232f09dec8424916.
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_PYTHON_RUST_20_20260908.md: bfd5af2666f35a2d67bb6babba881b76149794de7ede6ba714e0720c57a18181.

## Exact candidate bindings

Canonical SHA256 uses sorted compact UTF-8 JSON; file SHA256 uses original candidate-file bytes. All candidate files are under datasets/cache/expansion-v1/versioned-recovery/r12.

### exp-v1-recovery-r12-rust-generation-0697

- Change class: oracle-rebuild.
- exp-v1-recovery-r12-rust-generation-0697.candidate.json file: d10dbdc858dcbc7ec1a11d5330b9e579c1ebef2f55dfa7fbf7e4d10a609102c0.
- Candidate canonical: e1d8d32c6c4306e1b590af66ff4e7302f9807b73262ffd8ca93c813b91f44717.
- Parent canonical: 04dca4f26c1e805166c1ff4269bd8f0eed217af59e5200cd703dfb3e5631bff5.
- Source row-03261: a038d115ff090b5cea8442037b5f81548d8c36a95436debb75ac25040593a43d.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/RUST_FINAL_CONTRACT_ADJUDICATION_20260908.md: b7d4190075a713f3fe4bf5aed9574b9a97dfe93b0384cb049173dafaf1ec9fc5.
- Problem: 70cd434632c4ac3a6e4701a77bc5c8dbac8aa1f345738e4cf51407e4bad03c61.
- Reference: d25800634e8dee7f01f5575f56acc81e0c734a99a4c8a7911ec08530b5105c8b.
- Supplied mutant: d5e0dc4f32729ea3561cd4814f8e79c36264c4214cdcdcfb5d8e644c4482ab94.
- Independent solution_test.rs: 25cbb426e993b5056b15111dc4e445f6c968882f491cfa4111e9728496f1b761.

### exp-v1-recovery-r12-rust-generation-0509

- Change class: oracle-rebuild.
- exp-v1-recovery-r12-rust-generation-0509.candidate.json file: 6a5f86e6818f3e5cf4d54a9b195b6ac211c97c6f232c35ff758f7c79685dbde9.
- Candidate canonical: 1b3d6efb189dbfd00d64b698374f2b340b10e32394c095915482b39b6843929d.
- Parent canonical: 24c0d7e6054219d46ac007b92128c647e01732ece3176c4b5b7c9b4fa1f4a9c0.
- Source row-03274: 5f54ee4314abfc38a164902a518af0ec7e1fe6842fe5a964e6eb5a55b8a08d9d.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/RUST_STRATUM_REVIEW_30.md: 442a830041ee154bd6f980a0270256d5ba08e632f44779a8b8d5b3f1a1571301.
- Problem: 174b05c6538f4a415eaf36f49ecb98bc0efedb91279ccf5972c02c94aaac7fa4.
- Reference: 70a751373cbccd30cfb414428e0932d97c4e5ec1bb7362b7ce16e3ac04f719ee.
- Supplied mutant: da82cdeda2e180a340e9fd7da70cb31ee1b6498ffec56766638ba604a43e9c88.
- Independent solution_test.rs: 1e4139a01ea3fcedd702c98cca931fa5cf0c027a82b0a67386b0402c6c66f5cb.

### exp-v1-recovery-r12-rust-generation-0487

- Change class: oracle-rebuild.
- exp-v1-recovery-r12-rust-generation-0487.candidate.json file: f97043d0db6566226dbbd6aac88aa04c681d114d1af0b6d84af59606d71aa93d.
- Candidate canonical: 8bd4fdde9168e90a56a025f0d7b3117ebfc0e872a1e30905361efc2b40ee264c.
- Parent canonical: 9ee8d243d8728a71c43c64ab9122fceb8e0db37aabc8e8e1f055ff82fb726ad4.
- Source row-05991: ff9d9a8308576f019c50bec2336ce85b8a7d1ca4ecacc6a08345cf7037ae633a.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/RUST_STRATUM_REVIEW_29.md: 05a4bac120af9b07505a3e628a582021e9a2503520eb4d79d11f4f99c9e22831.
- Problem: 07bf29038eeb2e6fc3a38360146a787863a01e38a00a3a19be9a858638df0155.
- Reference: f82da9e0e607a31880dd1c533e4c9d92c87aa2b870cc10b3e7a41e69565eb550.
- Supplied mutant: a1ad0530f1198a0a72dae70887c635ad81b06d97fef700161a1bcd9c28c580af.
- Independent solution_test.rs: ee3da12e6ee7c93abe4321ec159028d39b19fb05057f92cc69a08d6c1ea582fa.

### exp-v1-recovery-r12-rust-generation-0449

- Change class: reference-fix.
- exp-v1-recovery-r12-rust-generation-0449.candidate.json file: 66299b929e2c7faf2353da35d22522ad89f193a1243b42aaf45e691d8bf603d8.
- Candidate canonical: 7819626127384db5815257819edb3df0ab660979c19dc1e58cba0ba2145c6189.
- Parent canonical: def1e400f668b012b1a57a04089f1177895a6c4a38d228c4a126c70670d745f1.
- Source row-06257: 11f9f2c15cad2ee111b02f79d288a6c2521d25e75085b212b2cc0fbaf75d2869.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/allocation-validation-priority-result.json: bc6323c2be41413b5b1faa27601639f2b90a0da24c2535bfb6204517fe6f301e.
- Problem: 6d7a70dacc0a6117f4ed17d992a32009c6cd2dc0cfd249aa490b8199166147bb.
- Reference: ebf0b3831ebe025ee19583c5008adbcd7bf9550f3632f0e92a10b97962055b8d.
- Supplied mutant: 11098d7f7895a2ab90f9d7bbf31cc169976d72dffd0df361b98cd5f3339cf5a2.
- Independent solution_test.rs: 2f9b9772b9e370a7947bcc79a0c36461aed84a0472041f3da396c708fa4d6ebb.

### exp-v1-recovery-r12-rust-generation-0177

- Change class: reference-fix.
- exp-v1-recovery-r12-rust-generation-0177.candidate.json file: 1abf6cf30a487e23182319aafd9e2c574fe24143ee719977ac7eeedeef8d450b.
- Candidate canonical: 99b77896fb0a1c15a9193a215cbc8f3abbb9dbc62a085b4b1184aac963911ade.
- Parent canonical: fbe703e80006ad2b3cbf191a47c994dc7c11742f59bf7b69da2d537d7e333d8a.
- Source row-03349: db900eef05b85c25f0bc20a7d0773a2c753f98775919bd6c7ff14631f93b1c1a.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/column-maximum-index-result.json: 85a9ad502a17b130ad70c27eb5fccac6493b2b1e52cf979266df1ab9afcea12c.
- Problem: f505cc84a989305c7c3a8089efb586bf071ad1a27d394b764f79fdb9c8f41efb.
- Reference: 77cf66c9ef6d25d383fb64cd0b09c031317fbd1c674bc0912cef20085dfc0d4d.
- Supplied mutant: d8bdc9b7e38a996abd8b6c8acefa453be934179665c5af22aa881b80252e6996.
- Independent solution_test.rs: a72cef6d3385cd23fe74bd60f8b56fe508c41309fdc61e24f788193f1d5c4ae2.

### exp-v1-recovery-r12-rust-generation-0141

- Change class: oracle-rebuild.
- exp-v1-recovery-r12-rust-generation-0141.candidate.json file: 33082579d7d7d5abcfb25a01c7efbc1c14bc3ceacd0858e22f60428f3df38616.
- Candidate canonical: 2ab42198145460387c9227a93ed83feeb1e45312a1602fd4d6eb3069c61beeb2.
- Parent canonical: bee540edb94df83bbc7fdec816b910309e7e289d5e92618552b865aeaffadf0d.
- Source row-23880: a9752a45a5241e36cc4a43beac551210efa017cee94aad2bbc4773adaf799ad8.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/ledger-maximum-balance-result.json: 74317f9a0c1b71b421034bf54133fa10c1bf705039b26567f2379689d72480d9.
- Problem: a58d0fbc8b1c7dc2e7cf842bd069245566a82ee6392569d4e5cb50ecdfd16bf8.
- Reference: 2315a74ec80dc374d52c36886024b5b93f60416bcd4412a7752b6dce2c8be42d.
- Supplied mutant: 0e11b5f4972fe25c713e9a846c5f2130fb47c7c0d33448e3720ca0550784b66f.
- Independent solution_test.rs: 4a9891ad3adab4a1b231e4f45a5ff1c65477ba1711f5fce8cd09935ee5f28c8d.

### exp-v1-recovery-r12-rust-generation-0099

- Change class: reference-fix.
- exp-v1-recovery-r12-rust-generation-0099.candidate.json file: 7f88ae0ee308fb0c02c016348baa4b6c723843cb47e53e44ad062a37a2d67363.
- Candidate canonical: bda4cff745d3406bbdfbe6bcdddff264700be040963c1e6a3947533b6677e698.
- Parent canonical: 9f1028f4c63a875a71fbc516e38096b59319eb4fda05df1527125f04a6f467ab.
- Source row-03301: 40618a89aca80b1c378b9a9bcdde380b57c48dabd937b610265cfe36b679453d.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/scoped-tag-lexicographic-result.json: a72ad9c736e331c84e4380e4080bb7e2ec6927aa113a9eb1098b8aad8ed45f89.
- Problem: 7dd2093524df44c2e1652379b094a7b1f09272273d84aa99bf8beecb80278bc8.
- Reference: 8622cda78491c35444bff2c2db427deeb3ff55b556acdf01c6d8761808a8d568.
- Supplied mutant: 0e24a33412199403e6ef0e7d766ecf276c4213d509adf4cef73257735d3a8922.
- Independent solution_test.rs: 427b65d0748c36eed3f31f7b410c59d8be665d5692e64ef8442a9ff61f70ff7f.

### exp-v1-recovery-r12-rust-generation-0092

- Change class: contract-clarification.
- exp-v1-recovery-r12-rust-generation-0092.candidate.json file: ff5ed17be02d49d6c55a6f703619e5281c33515d29ed53c23f91bcf0119cd186.
- Candidate canonical: 8549f265d6d91500244b8e23750b1f2394e2b0dba5ae06a73d1fef1639ea6621.
- Parent canonical: fb599775c62d40ba3fba6a8ea9a454415ad1d7de70a66a78206526600f768935.
- Source row-05918: 95268211b196c1f97aae21abe72f64b22d6973031276ec59eed55e1f0a2b1cbb.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/tagged-field-hyphen-result.json: a2aaaca92ea5e94560cf0878c40be1ca3e1d661e3e544073b31f888d455b13fc.
- Problem: 5d9ec137d6d373deabe3feaa6a086d9060c460ea8a29ead851c91d3e2be15abc.
- Reference: a1dc6460a8a09dc8d719348bebfdd9a4ec5ac3f6277371f88bcd8aaf067aa332.
- Supplied mutant: 672bdbf5b8056a67737c004765959631be1b6f896c6fd6f669225c1fe1797144.
- Independent solution_test.rs: c7076488d0c246caf8ed467fdd85d7a36ad52e4b05448e638aae6c5f82fb8de9.

### exp-v1-recovery-r12-rust-generation-0364

- Change class: contract-clarification.
- exp-v1-recovery-r12-rust-generation-0364.candidate.json file: 59ee230c63afbb4e07ec1ccb748ef9864bf18d5ddc45d772fe3913f7ad2b0be5.
- Candidate canonical: 2f4ddad80bf1944922827cb9fc06916eb08fbcf344f4b3653abef43d54dcdf12.
- Parent canonical: a4018ca869dde6a604b3403171e77d5cc73cc2cfb74e4cb707004b04f2c46131.
- Source row-23678: 372906d106961e5144eb62df36a213755206b5d0aed1328ee5be91bd8752c646.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/heaviest-route-hidden-overflow-result.json: 5fb865f04e14e9f1415d3f5f762206423163d4151c807df27fb569cd547681cc.
- Problem: 62edca8f8853ebcbc019cbb9b8e4beaab63cd8359347484b1386a7a66e4b2bd8.
- Reference: af7ad1df261f6ff0399b9faf7ff4b9d36f94ad096ad3816f5ec1c41a8052532f.
- Supplied mutant: e6689b45014153e9705114f0de5fda6cc802e44e13904ccdb3866c09894b7aeb.
- Independent solution_test.rs: 5bc77472b5169e0be28ebdc0ff8b10622039081e85eca672f5f11f43f6a03293.

### exp-v1-recovery-r12-rust-generation-0630

- Change class: reference-fix.
- exp-v1-recovery-r12-rust-generation-0630.candidate.json file: df68b99d3f716adef1447e1f6b148746c975e84a68c14d267f6498d013e5b90a.
- Candidate canonical: 3288a8b44e34153fe140d9e00744dc3e6c667bcffd74ddf35241ba892a603afd.
- Parent canonical: 0f7f14bb3f47c11b8ab120ef115c5cf5a75a764a93a09437e25c5a05b1b8dba1.
- Source row-03229: 803c0eedd31ce9d6987a1445ec9464b3551262b68ae8a16cd09b5850c013f6e1.
- Original hold evidence measurement/data/expansion-v1/cutoff-5885-review/tour-dead-end-overflow-result.json: bfc6f26488b3d8d0bc7e4e57e5d603e60fa23370b70559f6c3e679b061481cd7.
- Problem: 0a623f4f9c63280d98e219fa50b678b8f7923d5c7cb6d0cb04003f0ed9a258e1.
- Reference: 3d5b9d95aeb1418eff1d2a50f5cbc62261ca8ce1b3f3ff98968eaa759c5b4da3.
- Supplied mutant: 4754d79523abf7673544be78997e882f8056c41bcac3ab8cd1a0ae125ac65f30.
- Independent solution_test.rs: 2fd27a0c3f37680e1c18452a7a11f2aaf85723e86bc5e46d6bd6f28ca3517cc1.

