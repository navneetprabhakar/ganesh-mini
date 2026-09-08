# R15 Python/Rust corrected-test review — 2026-09-08

Gate 2; bounded static review of exactly 13 corrected generation candidates (Python6, Rust7). **11 scoped positives, 2 oracle holds**: Python0741 and Rust0449. No candidate execution, generation, admission, central edits or new original coverage. R15 Java is outside scope.

Full corrected tests, unchanged reference and mutant read; specifications reconciled against the R12 review and approved R15 feedback. All 13 specifications, references and mutants are byte-identical to R12. Every defining held-defect witness is now present. Two remaining oracle restrictions must not be excused merely because the supplied reference passes them.

## Individual decisions

| Lane / suffix | Decision | Exact basis |
| --- | --- | --- |
| Python0097 | SCOPED POSITIVE | Both UserDict and MappingProxyType scoped suffix mappings select src/a.tmp and preserve a nonmatching path. Normal and dry-run outputs assert correct order and independent nested metadata across input/removed/remaining. The dict-only mutant is now directly distinguished. Explicit list/dict/tuple domains elsewhere are preserved. |
| Python0259 | SCOPED POSITIVE | MappingProxy labels with nested tags and UserDict labels are accepted; backing mutations and independent find/all results cannot alter stored catalog. No concrete wrapper type asserted. Insertion order, repeated-add constructor and duplicate/type validation retained. The dict-only mutant rejects these valid wrappers. |
| Python0399 | SCOPED POSITIVE | a--b, -a, a-, and - are accepted across construction/add/detail and edit/resolve. Lexical order [-,-a,a-,a--b] is correct; no invented hyphen-placement or URL-decoding rule. Prior stricter regex rejects this fixture. Staged edit failure and payload ownership retained. |
| Python0471 | SCOPED POSITIVE | Entries contains '/' itself, separately from a root marker; nearest_bundle('/a/doc','ember',{'/','/a','/a/ember.lock'}) is '/a', and {'/'} fallback is '/a'. Mutant rejects root entry. Profile-before-anchor search, direct-child hierarchy, malformed paths and nonmutation retained without filesystem assumptions. |
| Python0741 | HOLD: new output-wrapper oracle | MappingProxy/UserDict records now directly witness Mapping acceptance, with stride-two train/validation and cross-target isolation. However test_empty_and_large_stride newly requires returned pixels to compare equal to ((0,255),), thereby rejecting an otherwise correct copied list-of-lists matrix with the same cells. The public contract specifies a sequence matrix and independent deep copies, not preservation of the concrete tuple/list wrapper. The R12 review explicitly accepted this case with count-only checks and no concrete wrapper assertion. Compare row/cell contents after sequence normalization, or omit this new equality; do not alter reference/specification. |
| Python0744 | SCOPED POSITIVE | MappingProxy item and collection plus UserDict item fixtures preserve totals, repeated resolved IDs and detached copies. Negative votes are correctly accepted and sorted 0,-1,-5. Independent slices, huge pages, duplicate IDs, references and bool restrictions retained. Missing UserDict collection variant is not a fresh hold: the exact non-dict collection boundary is already witnessed by MappingProxy and the same Mapping branch is inspected. |
| Rust0099 | SCOPED POSITIVE | All custom-error unwrap/Debug requirements removed in favor of is_ok/match/matches. Scopes a/a0 with x require a0::x before a::x, distinguishing complete-string order from component iteration. Clone isolation, name validation, duplicates and enabled-batch atomicity/disabled ignore remain. |
| Rust0141 | SCOPED POSITIVE | Trait-neutral setup and errors; full u64::MAX supply transfer into zero destination succeeds with exact balances/total, directly rejecting artificial maximum exclusion. Reachable ordinary rollback, zero supply and ordered batches retained; no private balance fabrication. |
| Rust0177 | SCOPED POSITIVE | Independent u128 one-based encoder produces label for zero-based usize::MAX, tested against empty input and tiny ragged table with absent/0.0 output. Next index produces LabelOverflow. This distinguishes overflowing one-based temporary without huge allocation. Public traits are explicit, ordinary label/ragged/numeric semantics remain sound. |
| Rust0364 | SCOPED POSITIVE | Exact four-node hidden underflow [(0,1,-1),(1,2,MIN),(1,3,0)] now yields None. The helper runs inside the deep-tree test BEFORE constructing the 20,000-node chain, so the subtree-max mutant fails semantically before a recursive depth abort, independent of parallel test ordering. Existing iterative depth, topology and negative/overflow cases retained. |
| Rust0449 | HOLD: retained intra-validation priority oracle | Trait-neutral extraction fixes compile constraints. Late EmptyRecipient/ZeroAllocation after valid MAX+1 prefix now each decisively test allocation-validation-before-arithmetic, with all-valid overflow control. But allocation_validation_is_ordered_and_shared_by_both_functions retains [Allocation('',1), Allocation('later',0)] and demands EmptyRecipient from both APIs. The prose prioritizes allocation errors over arithmetic/capacity but does not order EmptyRecipient versus ZeroAllocation across malformed entries. A zero-validation pass before recipient validation conforms to the specified categories yet fails this assertion. Approved feedback explicitly forbids adding priority between simultaneous allocation errors. Use one invalid category per fixture or accept either justified allocation error; keep the decisive late-validation fixtures unchanged. This refines the earlier R12 note's overly broad statement that current order assertions were legitimate. |
| Rust0630 | SCOPED POSITIVE | Disconnected A-B MAX/B-C1/D-E1 returns Ok(empty), exposing premature incomplete-path overflow. Existing connected triangle contains overflowing complete routes and still requires CostOverflow; exact-max edge accepted. Oriented lexical tours, cost arrays, input-order validation and copies retained. No need for the precise connected-line variant when the existing complete-tour control already distinguishes that rule. |
| Rust0697 | SCOPED POSITIVE | Exact approved distinctions now tested: a,on:: (two fields) => WrongFieldCount; a,on::, (three fields, bad enabled) => InvalidEnabled; a,on,:: => InvalidTag. a,on:off, also witnesses incorrect colon/field-count mutant. Empty tags, trim, order/duplicates and trait-neutral errors remain correct. This uses main's corrected approved feedback, not the provisional punctuation misclassification. |

## Seven-criterion conclusion

All thirteen retain clear bounded APIs, substantive complete targets, idiomatic standard-library references and dependency isolation. Non-triviality comes from nested ownership/filtering, ordered catalog state, hierarchical search, transactional mutation, checked numeric state, graph topology or structured parsing—not small patch size or added boilerplate. All thirteen have provenance-separated correction input and realistic original-reference mutants, now with genuine small witnesses. No additional static reference defect identified in this bounded correction review. Valid-oracle/API consistency remains blocked for the two exact rows above; the eleven positives are not admissions or executed passes.

No automatic further critic loop is requested. Preserve terminal correction artifacts and main's independent diagnostics. An executed supplied-reference pass cannot resolve an unsupported oracle that would reject other conforming implementations.

## Provenance and immutable-byte checks

For each row, previous_candidate_sha256 recomputed from canonical R12 JSON equals approved feedback. R15 prompt/reference/known-bad exactly equals R12. Plan source fields (except additive transformation) and rights match corrected candidate and previous rights, retaining all five approved flags. Individual source rows and hash-bound review origins are preserved; no rights decision reopened.

Both correction prompts contain exactly id/problem/prior-test items plus approved specification_review feedback, no reference/mutant code. Their item specifications and prior test files exactly match R12; returned test_code normalized only by strip plus terminal LF matches R15 test content. Both archived calls returncode0, timed_out=false, no disallowed tool items, with prompt/output hashes recomputed. These are generation tasks, so unlike embedded repair inputs their specifications do not contain known-bad code.

## Evidence files

- datasets/cache/expansion-v1/versioned-recovery/r15/plan.json: `d2e65ef33e2c70162a53315e3daec75ebe1e3fbc1a7098e8635eddacb348c100`
- datasets/cache/expansion-v1/versioned-recovery/r15/run-contract.json: `9698ee3b6b7cf73427e080069dda922d0d5de7e44d14d83b119cff3027a342e0`
- measurement/data/expansion-v1/cutoff-5885-review/recovery-test-feedback-r15.json: `be176d78f3d57efc593b56895696cb74425280e234239be67c8efcc45cdf1ead`
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_PYTHON_REVIEW_20260908.md: `4aa736c5fa48090c3a2c45b3798492231d61363f1ff8ffae0756f290a2b4dc4b`
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_RUST_REVIEW_20260908.md: `e8fafe162d914b4726b5ddab87ed1a4cb6d3542156eb6000756ff47a9997e625`
- datasets/cache/expansion-v1/versioned-recovery/r15/python-recovery-test-correction-evidence.json: `f9a0d506e75bc90ccf48a2b95bf762cac28b1fbdca46bc44a38c4d56b0dcaa9e`; prompt `d453c86a252b037c12614c07e3686bb98f8b64df4740c4cb6db705cb8e77745d`; raw final `3ae6d8bf407907d6f374b1e91044e3b064dec5fe3bc9cd72c0438fe380a841a7`.
- datasets/cache/expansion-v1/versioned-recovery/r15/rust-recovery-test-correction-evidence.json: `d05cf3246324ddca6670db39c6d9a3347bfbe78c54b5b338004f07a9ffa0cbc4`; prompt `658ecfd2861ee5052a0847b16b5bded04acabfa0bb9c6b7e044120df1c6e1eee`; raw final `3ffab20523e50495ef3d739a3e888514af234a9d5a210dfb3043802a21434b39`.

## Exact candidate bindings

All candidate paths: datasets/cache/expansion-v1/versioned-recovery/r15/<full ID>.candidate.json. Canonical hashes use recursively sorted compact UTF-8 JSON; file and content hashes are exact bytes.

### exp-v1-recovery-r15-python-generation-0097

- file_hash: `914a7d59879024b27c6527df128dd9992a05ee34f4ab1aacf5fc0068fa6da1dc`
- canonical: `9ded5f25d71d9f89d3dafc1109d69e94cb1b31920f3c7c40c920c6735c643fd5`
- previous: `a7ef3302a392362628beb273701bcfc9b16f7ce206c4c1a145d9987670a885f0`
- parent: `87284237d18ef56e4228b6dfaaf25aca4f61c58d448072ed5eec64fe8f2b4552`
- prompt: `fc4a97bec60e3c1bf4b564e3b3cf4c8a04711f809a7170c5699e2b11c999d522`
- reference: `91b3d679428d4f1388e12a28ede303e0b4cb30362be98c71edc1485b5ee39743`
- mutant: `3b9048e541eff229e17381086a065ac61987dc82473fae9546b794ca2d2f8c30`
- test: `6b0a5286122094dbfbaad1e5f27edd0074915aca9ac9bb1f6ad05aee3f10844d`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-08189; source-record SHA `5d6d19b5258187e638c8ed23b2cc38769a138404be070f463eb6d9f009825ff9`.

### exp-v1-recovery-r15-python-generation-0259

- file_hash: `e13d5244d1d12a5f20aab4820955de49ba03c4c7dc1b3795e185b782bcad2264`
- canonical: `968a2b3ee54d72bde422d12b0c9b05aadc669ee546cab26d8c4240b13ffc2f4e`
- previous: `0c61dc5d92a1d4c30a91592b1759ebcf5d9e0b59146c59e596cfa92ae416dd88`
- parent: `41895584e60c005b6ac53a2bb5072605e35aee52ab910a796f1c704f9b6a80e0`
- prompt: `c20049bb4562fad3ae085104b2e9c5c3d78fa880a5c7f1ef7559811f38e5caa2`
- reference: `4659f3bfa280e64b93b882e271f9ec1101c728899d39c80306e670d1e40241c1`
- mutant: `0ee27b5b502cea284a4e44eb1fcb96c894a3271f8a5872eb376e9981a1fa3e82`
- test: `cf5264ca1600e127dd20a9dc1d77b6e243bba995dd1dfe6ec0813a2c92b48eff`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-04040; source-record SHA `6e8f62dad9737a2e8c9774d5659f8eaebddbde363ea85456194fc0093994d35e`.

### exp-v1-recovery-r15-python-generation-0399

- file_hash: `ec0a083a954ef9977b3d8623932529448027429d4d7d260f0e497003e123d5c6`
- canonical: `4c98b92350b593dfcb71cd40b1277e3352e1b6ad1b272b828b94dbd78c8e1ec7`
- previous: `692828d94f580bcb292b10f88a57f6d23549a3769f8e7deeb4d8856c354468b3`
- parent: `24f839845ad5637c73cf7736dc648be9887d8b60c01dceac99733d9bde1b91dd`
- prompt: `9644fdf70f8fed6169e9c6100e70b36bc2e973bc1e9bc942a0da511ff6d34585`
- reference: `b2af6cf002d908ba4f87d575c4e01d970a0551afd0824fb6a90e5268b666bed0`
- mutant: `36f1f6dd199a2c0a2b990b4064a023078292ab3e4bbdbc19aca6f901a6961a34`
- test: `0efdcd7d327d0f7ab232a6a4bcdddbf6f6b358427c1388c890daa9e8278ac112`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-08535; source-record SHA `140997ab57987ecdc4375c608136ce69ddcb21af6f5670ecb48a9ea9e16b52da`.

### exp-v1-recovery-r15-python-generation-0471

- file_hash: `6c9e595e23a94bf71b749a94d52a39bf93ceb4292c453fbc19120ca671bc73d8`
- canonical: `1cb5a209b3206eb8c6a1a8cc442518f24855446f6f614fbfe8f95ff88b35afec`
- previous: `4dfb8be99c9b246b3989f126d970cad0590ad0150001a21fa5d23acab87ae8dc`
- parent: `a563fb4850e489aa1a783828e5a96885e06401b33761b8224fb8636a7208234f`
- prompt: `ce5355943765d4cc29aa73396eb131bf456f339222799677ab7381a104ed1956`
- reference: `67a22d1fc9e556936b90e527b5aaf03cd785e7b4160579abb67806968f37ddbe`
- mutant: `cf6b85867afd14a13ca09ddbdbf7722037de56b716f130c3f183593391815bae`
- test: `2d1884dbe2cf5ccc21ffa8aa66ebea90d84a8bbb79e99abf6d07680ea4b0e163`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-08440; source-record SHA `140dff21f72b0d2646c02cea8e67b9165977face0fce9e867f62b8175f5a8349`.

### exp-v1-recovery-r15-python-generation-0741

- file_hash: `66f41ea3c03e135b6cb32207ac2506234eb634ada27f57820133e6e2111790f0`
- canonical: `fd1ba55fb49ffa298e2d2095d6a91bad462ef837df3eb1c1f8cc84be5da69b78`
- previous: `727cce89478bf7a7e45876b1c0de145bdb5f47735d06fc7934ac9942f231e047`
- parent: `8be310442dba97d554be2561d473d8ca7934207a377c12d1db0c6d39e8440a82`
- prompt: `36957cd7be2a735650abab3571506d4c2e2177577e5de0576e0a71b4ffefbaa8`
- reference: `6ed08b6d38339aa4c5d083168505d7a08b9e60b0a299b68994d7f5320ff14cd0`
- mutant: `0654fb10b11f2165d1a9a655d14ae10da7b755f57f1efe8ea718f76ea9069915`
- test: `cce46332defcc427ea921d2a0914a9e109a13fdab20ae324edc4a40779a58dbb`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-04018; source-record SHA `08db021eb4b30cc79961f91e3fc9c6473c0cf6136c1462b771fd875f3e167d4e`.

### exp-v1-recovery-r15-python-generation-0744

- file_hash: `0922902fd8e5e1c2977c12972a5e95d4cfc52c52b2dc2f90e14e2b2e5aea74e7`
- canonical: `d9eafb391c34bd7b18210a615398dc7bc4910fbd295c4a04f3bccb250ad70640`
- previous: `ab2daf94f57723d3e226e6844819fada728e0d180bdddc333a217ad2b5845a18`
- parent: `efc1b28c3fe07967b43185a885b838fdfe1cd090e1f4c8816a7774c5bb25b126`
- prompt: `2fc177499dea298ce295e6bdb25374f0751ef2b2260f30535cf35c30d033e232`
- reference: `19ae7b3adbf4e1b13eaf142f7931dfa2b08565efd764e23e97963363b43623ef`
- mutant: `48c5864cc2ac0b98047f402e8930f6ee55f6db510a7b5f968fc7470f860dcf27`
- test: `ab102f7d6ff7e9ccb83ca15ac7d0bf68bf2d229d46c56424e3a6e992fc77dae8`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-04056; source-record SHA `1785299abb85e4f4b6199ba0b1c06e9ada6a32b36de8a19dab5bcb456a7d26b1`.

### exp-v1-recovery-r15-rust-generation-0099

- file_hash: `42517ec553bfafc06e3d54274573fdf89145e735c8ba7d799fe96dfc7a41519a`
- canonical: `a305cf205e8e2f45073ef1cf779a922e06531d29c2c58583b01ab5b9e32bcb91`
- previous: `bda4cff745d3406bbdfbe6bcdddff264700be040963c1e6a3947533b6677e698`
- parent: `9f1028f4c63a875a71fbc516e38096b59319eb4fda05df1527125f04a6f467ab`
- prompt: `7dd2093524df44c2e1652379b094a7b1f09272273d84aa99bf8beecb80278bc8`
- reference: `8622cda78491c35444bff2c2db427deeb3ff55b556acdf01c6d8761808a8d568`
- mutant: `0e24a33412199403e6ef0e7d766ecf276c4213d509adf4cef73257735d3a8922`
- test: `67237fdce08d345249253aad4543bcb4c6c47162722e10a3bee75e245f9dc367`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-03301; source-record SHA `40618a89aca80b1c378b9a9bcdde380b57c48dabd937b610265cfe36b679453d`.

### exp-v1-recovery-r15-rust-generation-0141

- file_hash: `c897e02ebe25735daecb54d8a2dd8178df303a5c4098b7e696393d8fe0e789d2`
- canonical: `2619e1d201ae37152f858529dadb008e2c1c740a3d71e3e8929fab4292cfb228`
- previous: `2ab42198145460387c9227a93ed83feeb1e45312a1602fd4d6eb3069c61beeb2`
- parent: `bee540edb94df83bbc7fdec816b910309e7e289d5e92618552b865aeaffadf0d`
- prompt: `a58d0fbc8b1c7dc2e7cf842bd069245566a82ee6392569d4e5cb50ecdfd16bf8`
- reference: `2315a74ec80dc374d52c36886024b5b93f60416bcd4412a7752b6dce2c8be42d`
- mutant: `0e11b5f4972fe25c713e9a846c5f2130fb47c7c0d33448e3720ca0550784b66f`
- test: `f8573a4b01733c87ff1bfab485b66b1558a7dc854b91777c52c958214d500b99`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-23880; source-record SHA `a9752a45a5241e36cc4a43beac551210efa017cee94aad2bbc4773adaf799ad8`.

### exp-v1-recovery-r15-rust-generation-0177

- file_hash: `32c577d232c1a0f6e293f27fab85f2e28c2588afc892930a652846268bc9a19f`
- canonical: `eba539daeb6b5153db2de8cecebe674217535b97ec47415105c70a00c19795d6`
- previous: `99b77896fb0a1c15a9193a215cbc8f3abbb9dbc62a085b4b1184aac963911ade`
- parent: `fbe703e80006ad2b3cbf191a47c994dc7c11742f59bf7b69da2d537d7e333d8a`
- prompt: `f505cc84a989305c7c3a8089efb586bf071ad1a27d394b764f79fdb9c8f41efb`
- reference: `77cf66c9ef6d25d383fb64cd0b09c031317fbd1c674bc0912cef20085dfc0d4d`
- mutant: `d8bdc9b7e38a996abd8b6c8acefa453be934179665c5af22aa881b80252e6996`
- test: `1d12ae6215acadad2b2cb72a298f29786b98ef5adc4447048d938fd510e447e2`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-03349; source-record SHA `db900eef05b85c25f0bc20a7d0773a2c753f98775919bd6c7ff14631f93b1c1a`.

### exp-v1-recovery-r15-rust-generation-0364

- file_hash: `2e5a949d25b9febfa63f6df00d8a81caf70cb9f93046f1bb8b4dd3d063e3a5cf`
- canonical: `72702982ebf2dfa15eceb4510387e914372aa0ae6677febc0c6f4d774b7c754a`
- previous: `2f4ddad80bf1944922827cb9fc06916eb08fbcf344f4b3653abef43d54dcdf12`
- parent: `a4018ca869dde6a604b3403171e77d5cc73cc2cfb74e4cb707004b04f2c46131`
- prompt: `62edca8f8853ebcbc019cbb9b8e4beaab63cd8359347484b1386a7a66e4b2bd8`
- reference: `af7ad1df261f6ff0399b9faf7ff4b9d36f94ad096ad3816f5ec1c41a8052532f`
- mutant: `e6689b45014153e9705114f0de5fda6cc802e44e13904ccdb3866c09894b7aeb`
- test: `0a49f9998ff357de2fd22020bf66b9b8bff53ff2688ebd4fdd109cab0aff79bd`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-23678; source-record SHA `372906d106961e5144eb62df36a213755206b5d0aed1328ee5be91bd8752c646`.

### exp-v1-recovery-r15-rust-generation-0449

- file_hash: `5f359ac52fcaebfc93ac106932efb26fa5f6546e9607472ba59652d9fbf655e1`
- canonical: `60f077de986b609c9b72ce1ea537d69c42ee374f51c019a8363be040b5818257`
- previous: `7819626127384db5815257819edb3df0ab660979c19dc1e58cba0ba2145c6189`
- parent: `def1e400f668b012b1a57a04089f1177895a6c4a38d228c4a126c70670d745f1`
- prompt: `6d7a70dacc0a6117f4ed17d992a32009c6cd2dc0cfd249aa490b8199166147bb`
- reference: `ebf0b3831ebe025ee19583c5008adbcd7bf9550f3632f0e92a10b97962055b8d`
- mutant: `11098d7f7895a2ab90f9d7bbf31cc169976d72dffd0df361b98cd5f3339cf5a2`
- test: `3a2b20f2d11bd40cd7d0c53ec35933959d08882001b28968f2a013b736d3398c`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-06257; source-record SHA `11f9f2c15cad2ee111b02f79d288a6c2521d25e75085b212b2cc0fbaf75d2869`.

### exp-v1-recovery-r15-rust-generation-0630

- file_hash: `2aa4d28d52743331542b265552a5ad62ff8cb1bd8edb54d89e52d22e4876b1ca`
- canonical: `a6679a76671f1f11fc27b57b2d0c0915d56350651a8bc516282c08239c235417`
- previous: `3288a8b44e34153fe140d9e00744dc3e6c667bcffd74ddf35241ba892a603afd`
- parent: `0f7f14bb3f47c11b8ab120ef115c5cf5a75a764a93a09437e25c5a05b1b8dba1`
- prompt: `0a623f4f9c63280d98e219fa50b678b8f7923d5c7cb6d0cb04003f0ed9a258e1`
- reference: `3d5b9d95aeb1418eff1d2a50f5cbc62261ca8ce1b3f3ff98968eaa759c5b4da3`
- mutant: `4754d79523abf7673544be78997e882f8056c41bcac3ab8cd1a0ae125ac65f30`
- test: `ef786d63b2eb6350a171dd1c231fb74034be203bde4b03969e21e6f6217c26b0`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-03229; source-record SHA `803c0eedd31ce9d6987a1445ec9464b3551262b68ae8a16cd09b5850c013f6e1`.

### exp-v1-recovery-r15-rust-generation-0697

- file_hash: `89052b231ba64c136294c825c8153f869d9f87825853365714492222f1f9b072`
- canonical: `b6cd77f711deb2ab734ad697eac629e1318c9e63326673c20d551e42c6ce49e7`
- previous: `e1d8d32c6c4306e1b590af66ff4e7302f9807b73262ffd8ca93c813b91f44717`
- parent: `04dca4f26c1e805166c1ff4269bd8f0eed217af59e5200cd703dfb3e5631bff5`
- prompt: `70cd434632c4ac3a6e4701a77bc5c8dbac8aa1f345738e4cf51407e4bad03c61`
- reference: `d25800634e8dee7f01f5575f56acc81e0c734a99a4c8a7911ec08530b5105c8b`
- mutant: `d5e0dc4f32729ea3561cd4814f8e79c36264c4214cdcdcfb5d8e644c4482ab94`
- test: `02fe4eaec852b2f48f17ef6d2d55e726d903c51056bbd68f88ded7339bf8f338`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; CC-BY-SA-4.0; revision `57bd46727e49ac3e2890218a146d35c2454a8496`; row-03261; source-record SHA `a038d115ff090b5cea8442037b5f81548d8c36a95436debb75ac25040593a43d`.

