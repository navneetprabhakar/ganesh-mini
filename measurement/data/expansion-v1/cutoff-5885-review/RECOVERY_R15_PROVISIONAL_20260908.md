# R15 provisional test-only correction — 2026-09-08

Gate 2. **Draft only, not approved, reserved, generated, executed or admitted.** Exactly 19 R12 derived generation holds: Java 6, Python 6, Rust 7. No original coverage credit or central mutation. R12 active teacher lanes are untouched.

Read all three R12 lane review reports, the correction implementation and R10/R13 request/feedback examples; rechecked the Python/Rust specifications governing the proposed witnesses. Java scope carries the completed full independent review. Requests use original parent canonical bindings from the R12 plan; feedback separately binds each exact previous R12 derived candidate by canonical SHA-256. These are distinct hashes and must not be interchanged.

Files:
- recovery-requests-r15-PROVISIONAL.json: planner request schema, tentative version r15; all selections oracle-rebuild.
- recovery-test-feedback-r15-PROVISIONAL.json: exact proposed r15 IDs mapped to previous_candidate_sha256 and specification_review.
- Neither file is a plan or registry reservation. Main must inspect/approve and revalidate before any activation; do not launch automatically.

## Scope

| Lane | Exact suffixes | Correction |
| --- | --- | --- |
| Java | 0028,0030,0131,0138,0160,0334 | Harmless getter-copy oracle; List.of/Set.of witnesses; in-flight coherent snapshots and propagated worker failures; unspecified constructor exception subtype. |
| Python | 0097,0259,0399,0471,0741,0744 | Non-dict Mapping witnesses, accepted hyphen grammar, root entry acceptance and deep ownership; negative votes remain valid. |
| Rust | 0099,0141,0177,0364,0449,0630,0697 | Trait-neutral tests, full qualified-string ordering, maximum index, hidden-route arithmetic, validation priority, overflowed incomplete tour and correct comma field count. |

Explicit exclusions: Python0717 invalid-kind reference regression and Rust0487 missing explicitly promised reference traits. A test-only correction cannot resolve those reference holds. Existing positives are also excluded.

All R12 specification/reference/mutant bytes must remain unchanged. The critic receives only current specification, prior tests and specification-derived feedback, never corrected reference or mutant source. No repeat critic loop: correct_recovery_tests.py rejects a prior run already marked correction_attempt. Lane counts 6/6/7 stay within its ten-row batch guard. Runtime execution, independent quality re-review, directionality, deduplication and evaluation separation remain required after any approved emission.

Rust0364: the four-node hidden-route witness must execute and assert inside each test function/path BEFORE reaching a deep-tree call. A separately named test or single-thread assumption is insufficient because Rust tests can run concurrently and a stack abort elsewhere can obscure semantic failure. The existing valid 20,000-node iterative-depth coverage stays; no stack tweaking, expected abort or timing oracle is proposed. Rust tests may use only the public traits actually promised. Python0744 includes negative votes as accepted data, never an invented rejection.

## Review bindings

- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_JAVA_REVIEW_20260908.md: `e07eba34ce78be5557421eabc5b53afce22fb0ad3b92be30be71d279083ef85c`
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_PYTHON_REVIEW_20260908.md: `4aa736c5fa48090c3a2c45b3798492231d61363f1ff8ffae0756f290a2b4dc4b`
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_RUST_REVIEW_20260908.md: `e8fafe162d914b4726b5ddab87ed1a4cb6d3542156eb6000756ff47a9997e625`
- Frozen parent corpus: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`
- Frozen hold ledger: `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`

## Exact previous candidate and unchanged-content bindings

Paths are datasets/cache/expansion-v1/versioned-recovery/r12/<full R12 ID>.candidate.json. Canonical hashes use recursively sorted compact UTF-8 JSON; file hashes cover raw bytes. Parent hashes in the request refer to the original corpus, not these derived files.

### exp-v1-recovery-r12-java-generation-0028

- Previous canonical: `97d1366f3983a8b567fadfea631d0a945aec34e350105f83134e63a2c76412bf`
- Candidate file: `57f5cc2470db4ed7fa275fbc59baa5507edb356825b53f82345d61569afd8f35`
- Immutable specification: `c7fadf3cb0fc2d3e88f7a7536dfd9f2ca2e9d784cc17aef614dbc08d2f8a68a9`
- Immutable reference: `28d74955d709023ea486cf9357d1fdc6172ed9662adf8279796410a28b8066a7`
- Immutable known-bad: `d0673124d68e8d04c8f29cc36ca387d9787bb91e8f21c4b4cb663a449e3b7082`

### exp-v1-recovery-r12-java-generation-0030

- Previous canonical: `828d277e11cec1345055ad831bdf2a35524c6306d9add9f5f3e7a8c101a8cc73`
- Candidate file: `1838895c1799b697fd643cabb41d4bfc12f4c4fc35a0ff0baa6fb310bcf89d00`
- Immutable specification: `0b898e179321d692abbbcfb08ea3084e78094d6671a1eba959d991defb1a3296`
- Immutable reference: `0093352549231fdbbc04028644ad76611ca7fbb47a474ee9d6809a7dafea9227`
- Immutable known-bad: `3de5ea06234b92fbe695f70f794ad92fb07258d03ca198d642230f6cde69130e`

### exp-v1-recovery-r12-java-generation-0131

- Previous canonical: `5a9829cb8aac0db3486d051fa2bd039734fb3fcbb8e9e75a158fad9638626828`
- Candidate file: `6c5cb01bbbd24606f3b41f06b4c134f72265b5cfa9969c0a77733afe9376ec94`
- Immutable specification: `48613f74c4278d960f81a77a0b3057d0c6b5e30fb6b60298b09cc53653846233`
- Immutable reference: `604bc8a45d2585ad162c5be4864c5019efa3e4338331a0cbcb61888082f29e16`
- Immutable known-bad: `3306b56d80a2b40515868a80426aa42a7ba00940ce2db28cdd8f2a1f89af576c`

### exp-v1-recovery-r12-java-generation-0138

- Previous canonical: `87c16276a6d38343ac2a7127a77da978aeac3c8b1ec36a0d038431cb6f2ec2ab`
- Candidate file: `323df69c9451064d9e507ba2323d92c800d35041f06bc67328078b170449b9e4`
- Immutable specification: `1febe7197851c92cc08a9be775c0c308143382127d4e40a9ca3f75d916e0db42`
- Immutable reference: `26fdb37459d0f33d32fab79c27e56f0df409e887ccc647b71df7b85074bb7799`
- Immutable known-bad: `78b7790fd43c551d3f840625a3a6607df98e22b0f29f744c2be41e9b206ae585`

### exp-v1-recovery-r12-java-generation-0160

- Previous canonical: `88c8f12b881679e8b6821b06008dff4104a299aea7190d29691e2bca42888c33`
- Candidate file: `de65d17791fca742c7b00c9a433e6857306e9b4f15dc1afe21c6b002e4ed4850`
- Immutable specification: `4124fced52ca68bcb817ae63ad62a41a663289e89353b79e8cad2714539caede`
- Immutable reference: `9074e92c141e44be3613cba122bd8c72c70481a2a3d88a998e785a3ce4a0944d`
- Immutable known-bad: `12c7fd6af703cbf551a20c8551a4953956a23784343bfe5ba66a1a391e37ffa3`

### exp-v1-recovery-r12-java-generation-0334

- Previous canonical: `7bb65b2e32cecd8b10dc3823457cabf0628e8f66607c28828a5f84c67edf7e8c`
- Candidate file: `2c30b40acd7d47d03340ba08d2c214086c3e0b2b326397df19a6c8f1a4c18a8d`
- Immutable specification: `1361c6803cc1b519191634c0c3869c65ec3de58c10d73205f49b7e6c43c922aa`
- Immutable reference: `b621094918c9e1f58f2aa748c1eda4df07fa30b2dd6658da21924c6fb4770260`
- Immutable known-bad: `06c415f96ae36c0633123ce9f5285bd294d8087efbfcb4c4dff648d8c85fe868`

### exp-v1-recovery-r12-python-generation-0097

- Previous canonical: `a7ef3302a392362628beb273701bcfc9b16f7ce206c4c1a145d9987670a885f0`
- Candidate file: `a4f90a76897c995b957f645b9a0c4e801e580404659609321a6ee18e9dd17ccc`
- Immutable specification: `fc4a97bec60e3c1bf4b564e3b3cf4c8a04711f809a7170c5699e2b11c999d522`
- Immutable reference: `91b3d679428d4f1388e12a28ede303e0b4cb30362be98c71edc1485b5ee39743`
- Immutable known-bad: `3b9048e541eff229e17381086a065ac61987dc82473fae9546b794ca2d2f8c30`

### exp-v1-recovery-r12-python-generation-0259

- Previous canonical: `0c61dc5d92a1d4c30a91592b1759ebcf5d9e0b59146c59e596cfa92ae416dd88`
- Candidate file: `bbac7e8dceea45d1977ae61cceba64e32b839b2d845b68597907136110433e1d`
- Immutable specification: `c20049bb4562fad3ae085104b2e9c5c3d78fa880a5c7f1ef7559811f38e5caa2`
- Immutable reference: `4659f3bfa280e64b93b882e271f9ec1101c728899d39c80306e670d1e40241c1`
- Immutable known-bad: `0ee27b5b502cea284a4e44eb1fcb96c894a3271f8a5872eb376e9981a1fa3e82`

### exp-v1-recovery-r12-python-generation-0399

- Previous canonical: `692828d94f580bcb292b10f88a57f6d23549a3769f8e7deeb4d8856c354468b3`
- Candidate file: `f81d392ca66e1f7ac781ac409b473a7d3d47a89b417dbfdfd552b94f0ad4833b`
- Immutable specification: `9644fdf70f8fed6169e9c6100e70b36bc2e973bc1e9bc942a0da511ff6d34585`
- Immutable reference: `b2af6cf002d908ba4f87d575c4e01d970a0551afd0824fb6a90e5268b666bed0`
- Immutable known-bad: `36f1f6dd199a2c0a2b990b4064a023078292ab3e4bbdbc19aca6f901a6961a34`

### exp-v1-recovery-r12-python-generation-0471

- Previous canonical: `4dfb8be99c9b246b3989f126d970cad0590ad0150001a21fa5d23acab87ae8dc`
- Candidate file: `eeb133d1c4b36879aa54c3eeb06d1e0b877ae6ce6078f9c4fe86c64b94ea170c`
- Immutable specification: `ce5355943765d4cc29aa73396eb131bf456f339222799677ab7381a104ed1956`
- Immutable reference: `67a22d1fc9e556936b90e527b5aaf03cd785e7b4160579abb67806968f37ddbe`
- Immutable known-bad: `cf6b85867afd14a13ca09ddbdbf7722037de56b716f130c3f183593391815bae`

### exp-v1-recovery-r12-python-generation-0741

- Previous canonical: `727cce89478bf7a7e45876b1c0de145bdb5f47735d06fc7934ac9942f231e047`
- Candidate file: `be87d213067062c9d55c918d239d743efcfef7c25c67b0889474261e659fd0eb`
- Immutable specification: `36957cd7be2a735650abab3571506d4c2e2177577e5de0576e0a71b4ffefbaa8`
- Immutable reference: `6ed08b6d38339aa4c5d083168505d7a08b9e60b0a299b68994d7f5320ff14cd0`
- Immutable known-bad: `0654fb10b11f2165d1a9a655d14ae10da7b755f57f1efe8ea718f76ea9069915`

### exp-v1-recovery-r12-python-generation-0744

- Previous canonical: `ab2daf94f57723d3e226e6844819fada728e0d180bdddc333a217ad2b5845a18`
- Candidate file: `643a3652023ad952a26693103e482f504d4831977fc630ff72e3a24492675b33`
- Immutable specification: `2fc177499dea298ce295e6bdb25374f0751ef2b2260f30535cf35c30d033e232`
- Immutable reference: `19ae7b3adbf4e1b13eaf142f7931dfa2b08565efd764e23e97963363b43623ef`
- Immutable known-bad: `48c5864cc2ac0b98047f402e8930f6ee55f6db510a7b5f968fc7470f860dcf27`

### exp-v1-recovery-r12-rust-generation-0099

- Previous canonical: `bda4cff745d3406bbdfbe6bcdddff264700be040963c1e6a3947533b6677e698`
- Candidate file: `7f88ae0ee308fb0c02c016348baa4b6c723843cb47e53e44ad062a37a2d67363`
- Immutable specification: `7dd2093524df44c2e1652379b094a7b1f09272273d84aa99bf8beecb80278bc8`
- Immutable reference: `8622cda78491c35444bff2c2db427deeb3ff55b556acdf01c6d8761808a8d568`
- Immutable known-bad: `0e24a33412199403e6ef0e7d766ecf276c4213d509adf4cef73257735d3a8922`

### exp-v1-recovery-r12-rust-generation-0141

- Previous canonical: `2ab42198145460387c9227a93ed83feeb1e45312a1602fd4d6eb3069c61beeb2`
- Candidate file: `33082579d7d7d5abcfb25a01c7efbc1c14bc3ceacd0858e22f60428f3df38616`
- Immutable specification: `a58d0fbc8b1c7dc2e7cf842bd069245566a82ee6392569d4e5cb50ecdfd16bf8`
- Immutable reference: `2315a74ec80dc374d52c36886024b5b93f60416bcd4412a7752b6dce2c8be42d`
- Immutable known-bad: `0e11b5f4972fe25c713e9a846c5f2130fb47c7c0d33448e3720ca0550784b66f`

### exp-v1-recovery-r12-rust-generation-0177

- Previous canonical: `99b77896fb0a1c15a9193a215cbc8f3abbb9dbc62a085b4b1184aac963911ade`
- Candidate file: `1abf6cf30a487e23182319aafd9e2c574fe24143ee719977ac7eeedeef8d450b`
- Immutable specification: `f505cc84a989305c7c3a8089efb586bf071ad1a27d394b764f79fdb9c8f41efb`
- Immutable reference: `77cf66c9ef6d25d383fb64cd0b09c031317fbd1c674bc0912cef20085dfc0d4d`
- Immutable known-bad: `d8bdc9b7e38a996abd8b6c8acefa453be934179665c5af22aa881b80252e6996`

### exp-v1-recovery-r12-rust-generation-0364

- Previous canonical: `2f4ddad80bf1944922827cb9fc06916eb08fbcf344f4b3653abef43d54dcdf12`
- Candidate file: `59ee230c63afbb4e07ec1ccb748ef9864bf18d5ddc45d772fe3913f7ad2b0be5`
- Immutable specification: `62edca8f8853ebcbc019cbb9b8e4beaab63cd8359347484b1386a7a66e4b2bd8`
- Immutable reference: `af7ad1df261f6ff0399b9faf7ff4b9d36f94ad096ad3816f5ec1c41a8052532f`
- Immutable known-bad: `e6689b45014153e9705114f0de5fda6cc802e44e13904ccdb3866c09894b7aeb`

### exp-v1-recovery-r12-rust-generation-0449

- Previous canonical: `7819626127384db5815257819edb3df0ab660979c19dc1e58cba0ba2145c6189`
- Candidate file: `66299b929e2c7faf2353da35d22522ad89f193a1243b42aaf45e691d8bf603d8`
- Immutable specification: `6d7a70dacc0a6117f4ed17d992a32009c6cd2dc0cfd249aa490b8199166147bb`
- Immutable reference: `ebf0b3831ebe025ee19583c5008adbcd7bf9550f3632f0e92a10b97962055b8d`
- Immutable known-bad: `11098d7f7895a2ab90f9d7bbf31cc169976d72dffd0df361b98cd5f3339cf5a2`

### exp-v1-recovery-r12-rust-generation-0630

- Previous canonical: `3288a8b44e34153fe140d9e00744dc3e6c667bcffd74ddf35241ba892a603afd`
- Candidate file: `df68b99d3f716adef1447e1f6b148746c975e84a68c14d267f6498d013e5b90a`
- Immutable specification: `0a623f4f9c63280d98e219fa50b678b8f7923d5c7cb6d0cb04003f0ed9a258e1`
- Immutable reference: `3d5b9d95aeb1418eff1d2a50f5cbc62261ca8ce1b3f3ff98968eaa759c5b4da3`
- Immutable known-bad: `4754d79523abf7673544be78997e882f8056c41bcac3ab8cd1a0ae125ac65f30`

### exp-v1-recovery-r12-rust-generation-0697

- Previous canonical: `e1d8d32c6c4306e1b590af66ff4e7302f9807b73262ffd8ca93c813b91f44717`
- Candidate file: `d10dbdc858dcbc7ec1a11d5330b9e579c1ebef2f55dfa7fbf7e4d10a609102c0`
- Immutable specification: `70cd434632c4ac3a6e4701a77bc5c8dbac8aa1f345738e4cf51407e4bad03c61`
- Immutable reference: `d25800634e8dee7f01f5575f56acc81e0c734a99a4c8a7911ec08530b5105c8b`
- Immutable known-bad: `d5e0dc4f32729ea3561cd4814f8e79c36264c4214cdcdcfb5d8e644c4482ab94`


