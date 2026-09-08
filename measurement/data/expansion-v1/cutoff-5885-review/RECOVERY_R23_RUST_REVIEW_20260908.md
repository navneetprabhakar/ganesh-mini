# R23 Rust terminal test-correction review — 2026-09-08

Gate 2. Scope exactly Rust generation0012/0064/0071/0111/0342/0414. Full corrected tests and complete unchanged specifications/references were read, and complete mutant differences reconciled. R21 full review carries original-parent adjudication; parent hashes, approved R23 requests and critic feedback were independently rebound. No code execution, generation, admission, GCloud use, new original-review credit or central mutation.

## Result

Six scoped quality positives; zero terminal quality holds. The one bounded critic is consumed. This is static quality closure, not a claim of executed reference/mutant directionality or admission. Main owns sandbox results and integration.

All six preserve problem and answer bytes exactly against R21; entire validation object, including reference and known-bad source/hash, is exactly equal. Tests are the only behavioral artifact changed. Derived IDs and lineage metadata are separately versioned.

| R23 Rust generation suffix | Defining corrected witness | Disposition |
| --- | --- | --- |
|0012|Balanced parenthesized extra tokens: offsets3/4/3, distinct from actual EOF missing close|Positive|
|0064|Earlier property/nested-reference errors beat later model errors; malformed absent name only requires rejection|Positive|
|0071|CR before a nonfinal attribute LF preserved by both parsers; trait-neutral success extraction|Positive|
|0111|Invalid public id/channels/prefix rejected atomically; clearing invalid optional fields succeeds|Positive|
|0342|U+2003 label preserved and prefixed code remains distinct unknown, including duplicate tracking|Positive|
|0414|Padding TAB accepted after trim; interior controls rejected; malformed suffix beats earlier conflict|Positive|

## Per-record seven-criterion adjudication

### 0012 — positive

Prompt/API remain consistent with checked i64 parsing and first offending byte diagnostics. Recursive-descent precedence, unary chains, checked operations and error distinctions are substantively nontrivial, not an elementary padded loop. The unchanged reference uses standard-library checked arithmetic and byte positions idiomatically. New evaluate("(1 2)") -> UnexpectedToken(3), "((1 2))" -> UnexpectedToken(4), and "(1 a)" -> UnexpectedToken(3) are decisive against the realistic mutant that treats every failed close consumption as MissingClosingParen. Existing actual missing-close, empty operand, Unicode byte-offset, precedence, overflow and MIN/-1 cases remain valid. Declared Debug/PartialEq traits support assertions. No new depth guarantee or invalid oversized positive literal is introduced.

### 0064 — positive, with explicit feedback reconciliation

Malformed absent Named("Not.Valid") now uses is_err instead of forcing an unspecified error category. Valid absent Missing still requires UnknownModel; declared invalid model/property identifiers retain their specified error variants. Earlier nested unknown references now beat both a later invalid model and later duplicate model; earlier invalid property before duplicate model is retained. Forward references, every type mapping, outer Option, exact formatting, duplicate properties, immutability and lexical keyword/underscore acceptance remain.

The literal suggested bad-property-before-"2Later" vector was not added separately: coverage instead contains bad-property-before-duplicate and nested-unknown-before-invalid/duplicate. This is accepted as substantive coverage of the ordered per-model/property validation versus premature model preflight defect, not falsely reported as literal completion of every suggested vector. No remaining criterion gap was established from that redundant cross-product omission.

The full target combines ordered validation, recursive type traversal and exact text rendering. BTreeSet precollection without early failure preserves forward names and input-order diagnostics; standard-library rendering is idiomatic. Declared model/error traits support clone/equality/unwrap here, unlike the unpromised traits in0071/0111. The realistic preflight mutant is rejected by explicit ordering witnesses. Generation output need not compile when the specified lexical grammar permits keywords; no new keyword restriction imposed.

### 0071 — positive

The unchanged approved LF-only contract clearly preserves CR data. Both binary and text tests now place key:value CR LF before next:kept LF LF body, assert both attributes and exact body, and therefore distinguish split-LF framing from the realistic lines()-normalization mutant. Success helpers use match with fixed panic text, removing unpromised ParseError Debug requirements; enum matches do not require Eq/Copy. Tests preserve duplicates/empty/colon values, exact space-separated start-line validation, first separator, non-UTF8 binary body acceptance/text rejection, and independent output after input mutation. No CRLF alternative framing or extra control ban appears.

Framing, binary/text validation and owned extraction interact substantively. Reference is idiomatic standard-library window search, exact separator slicing, UTF8 validation and owned fields. Origin/contract/API/dependency criteria remain positive.

### 0111 — positive

Trait-neutral create/update helpers replace Result.unwrap; patches name both fields explicitly, no RulePatch Default or NoticeRule Clone/Eq assumption. Snapshot derives apply only to the test-owned Snapshot struct; field cloning uses specified String/Vec<String> types. Channel mapping uses variants without additional traits.

Independent invalid id=0, empty channels and blank prefix are each followed by otherwise-valid patches and corresponding error plus complete snapshot equality. Invalid existing expiry and tags can be cleared successfully, proving proposed-state rather than pre-state validation. Normal tri-state semantics, empty tag vectors, exact text, atomic multi-field errors and stable original-reference ordering remain. Pointer fields in failure snapshots are retained consistently with the explicit byte-for-byte unchanged contract and prior R21 adjudication; they are not a new success-allocation requirement. Each invalid input has one invalid field, avoiding invented error priority.

Transactional validation/commit, public mutable state and stable borrowing are substantive. Reference clones a proposed value, validates it, then commits; realistic mutant omits required-field revalidation. Code is idiomatic and isolated to standard library. All seven criteria positive.

### 0342 — positive

Corrected tests preserve U+2003 surrounding label and NBSP summary literally; a U+2003-prefixed code alone fails missing actual code, alongside actual code succeeds as a unique ignored key, and repeating the identical prefixed unknown fails. This separately closes key trimming and value trimming, rather than relying only on the earlier NBSP value witness. ASCII tabs/form feeds, empty required values, duplicate required/unknown keys, exactly-one-equals grammar, literal case-distinct keys and owned output remain. No error-string oracle, VT trimming assertion or new Unicode-only blank-line policy added.

The reference's explicit char closure uses ASCII whitespace, exact key tracking and owned strings. Whole parser validation/identity/ownership is substantive under frozen calibration. All API traits used are specified; realistic Unicode-trimming mutant has multiple concrete semantic witnesses. Standard-library dependency and independent-origin criteria positive.

### 0414 — positive

Leading-tab case now correctly finds first malformed empty key at index2; separate interior-tab-first case reports1 despite a later malformed key. Boundary-tab valid entry succeeds with trimmed value. Interior TAB/LF/NUL/DEL each fail. Earlier conflict followed by malformed DEL key still reports malformed index2, retaining the actual held ordering witness. Equal duplicates, valid-only conflict, no match, empty values, detached output and ASCII-only comparison remain.

This preserves main-approved trim-before-control interpretation without changing frozen specification or imposing allocation restrictions. Input-order complete validation before conflict resolution is substantive; reference's two passes are idiomatic. Declared LookupError Debug/Eq supports unwrap/assertions. Known-bad early conflict return is realistic and statically rejected by targeted test. All seven criteria positive.

## Provenance and exact checks

Correction author input Items contains exactly each R23 ID, its unchanged problem and the R21 test_code; parsed output test_code exactly matches each R23 candidate test. Specification-derived feedback is separate from source implementations. No reference or known-bad implementation was supplied as correction context. Previous canonical hashes match feedback bindings; original parent canonical hashes match approved request. Source identity fields and rights flags match originals; source transformation records derived lineage. All six source records are McEval-Instruct at revision57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0. This preserves recorded source/rights decisions, not new legal approval.

Author returncode0, timed_out false, no disallowed tool items. Raw prompt and final-output hashes recomputed. Full specification/reference/mutant immutability was compared, not inferred from labels. No execution result is claimed by this review.

Common rights object canonical SHA256: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`.

- datasets/cache/expansion-v1/versioned-recovery/r23/plan.json: `d44918671d7a9350cc90e67ac7eede1ee4ab61e6ce6bae2f1eadaccbed367d92`
- datasets/cache/expansion-v1/versioned-recovery/r23/run-contract.json: `779dbb642d6651a9c7d7e0e4b9ea0c1802052ce5614c7ee96307f3555271d0b4`
- datasets/cache/expansion-v1/versioned-recovery/r23/rust-recovery-test-correction-evidence.json: `58eb71370e99bd0544d4ef770b2e4cdf62c56d904a05a09b0e9de1c320566de9`
- measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r23.json: `0be4170d2177912f8a1079d5e76c09131cf7d65e6e0340cbc91b2e72cf1bb752`
- measurement/data/expansion-v1/cutoff-5885-review/recovery-feedback-r23.json: `ac425fb14ad116ccd3af62dbc8d339ac760bb1e4d0f7f87b70a1f766fd4a6f76`
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R21_RUST_REVIEW_20260908.md: `c17859d0799d774ac7bcb92e42771f4ce2d4a592565a8b5ce2c3229ef63adafb`

Correction author prompt: `68ad83199a4e3871e3865e51d3bb55be87370b86a83ff7aa70fc70a3400182d1`; final output: `aec6225cfbe1e29948d30861df63d37ae8f4ec2af6595b39fe7a6ce77786909f`.

## Candidate hash manifest

Canonical JSON uses sorted keys, compact separators, ensure_ascii=False and UTF-8. File hashes bind raw candidate bytes. All candidate files are datasets/cache/expansion-v1/versioned-recovery/r23/<ID>.candidate.json. Answer equals reference byte-for-byte.

### exp-v1-recovery-r23-rust-generation-0012

- Candidate file: `82caa533ff21212ebf7cc6f1dff1d74d5096700cd3c0623ff4f222e710f07bfc`
- Candidate canonical: `9ab1e013d46c98485bec7d4fa60c9716c9cf07c3fdb368cce84d3bc9a12f958e`
- R21 previous canonical: `bf531b354b2d7e9c35d34792fa145056770daef4e30bfa39f5feee876e100ff7`
- Original parent canonical: `45578ce324c41c8bee44f0b9bd48f5184c0022494f0ab67265cdac2053b02886`
- Problem: `e7c6e0f5675d424679743bc779608c1fedb756484877786d65bb9a5ccc2d8c7e`
- Answer/reference: `825ab51d467e944d9a926ec136f417bf0604b38ce11fa5f512d458dc1440973c`
- Known-bad: `5209df71dd4f4395536d3608c63cc1731e2a69ada15d5ccc05ae9aaa2376cdee`
- Corrected test: `a96a07430ee0570f9633f7f85a68e5533b701bf74c6eadd06f2a5fb06ee2404b`
- R21 test: `f435298ff4de3f690876a1935934956840ae4f7b3e4548b087def93ecb2d8ba6`
- Source object canonical: `14ebcaa1e92106b5891b371141e041d4a4acb66e1060a95c6bcfd61e8acee19c`
- Source record: `74e0892178c4208a92529ad7ff121ff460e9234a8652f3b295de27d18e13a0cd`

### exp-v1-recovery-r23-rust-generation-0064

- Candidate file: `61f7e8501f3c293efa12bfe31f3be88c0fbc81165e03da87b1dc3030b850b6dd`
- Candidate canonical: `f7097c07c436cc249e04adeb970451abd453a1fe58cff13c95578c73a7e702c8`
- R21 previous canonical: `a15cc83ff8dadf1061389ff4dffa8d882605d8ab110b0ac9abfdfd59a45cce7e`
- Original parent canonical: `3b3050e4e3e301fdadaaf3fd2d92ce3ce57b0e8e0067cb32112ed88a58adb9dc`
- Problem: `77072b4f93d931a0ea22ed6b5bb574ebb5ac1c0a859f0418b3f929610f026d13`
- Answer/reference: `4350c496ca5b7d2339837cdbb164d50593aba86b472d8468da94160f624dad1f`
- Known-bad: `ab4afb2c071d0c87293586117951727fbba81ceaba47005de23f74c8159bc0f9`
- Corrected test: `2e1cfa2c3cf76464dfc539e7e1211cbd7d426a70d7dc415fa7e524b3a60c9a82`
- R21 test: `3de685ddfaad559c0f9ffec6a5c58fda5875ec4de62d4081ff707c3189d6d98a`
- Source object canonical: `d38768b0443443e48b985de216db784c4965602cd5f0a609b55a150a740b479d`
- Source record: `87494f452d3efe2333a2407b843683deaf960d7ad7a38585c5244925f2e26c17`

### exp-v1-recovery-r23-rust-generation-0071

- Candidate file: `5480be0dce4bf77bdf6f3ef46c7857b7e03d4f58e7f9460e3646e96623e94fae`
- Candidate canonical: `6d19d2a1be476e38128953884dcc980e29669a32610b76f304b6866ac272e37f`
- R21 previous canonical: `0dd61fcc0a99305c1099c38d9018b46bd473c4b81ef7bb85ff89740d8c264528`
- Original parent canonical: `e2ceb1e16802116fff5a7b828b4a01b13ac7c996d841f293fdca978b0186610d`
- Problem: `05eafc417f3fb179645df8c7d9d0a392da3960b35d150ebb725972c93036369f`
- Answer/reference: `ab92319cc02461717e1bbd067cc0d5223de949a2aa19d141bccd688b022922b2`
- Known-bad: `796201a2fa2a8e706ceb32add9d0c607149d7c2b860cf1cd5a875c331d4c64e0`
- Corrected test: `d57fcb11281b21177295bfb8622a7d02a87d05ae446615b1439154ad981dec7d`
- R21 test: `9179d07c12b2cb211b773dec8278ae18b6770a9aff973ebf22a1a3f5a1f571d3`
- Source object canonical: `59afb89b83cef5202af2ccb3555d64524e4418d6056389c29d92d26ceeacfcfe`
- Source record: `70cd4c936746caf3958edcd46ad96d982d28dcb01f575a5b63799969bdef7680`

### exp-v1-recovery-r23-rust-generation-0111

- Candidate file: `2a4e98867f2606132900aa8bb17133a1cb0c19aaaf090a8d5c16b7b62336a007`
- Candidate canonical: `6a725f7b79730a084e5295972c3137452ea18dd9a2006604580d35455f0c0cab`
- R21 previous canonical: `6c3941bee54dc25b3f559d856309d6341a8204f6199a467ef4e4768fe943c67d`
- Original parent canonical: `42d67460786da429421d42ac674375082c1cedd18823e1e323eb0b9a903eaed2`
- Problem: `1060062f0cd123e7e9ffc62f6fa76fb5893539e1aacb621da2fd3a0859f8b502`
- Answer/reference: `3c5f21f3a690b2ee300ef2064b223cd3210ee98aaac485276af90a26b165b32a`
- Known-bad: `720420c227e306f3c319b1d00daa9e23657b6a07e5ae10596c48682134e1a448`
- Corrected test: `a140d7cf5501b79a70068b2fdc7b0dd1e8a92657e3b3d826e79dc7ba956c03c3`
- R21 test: `6de83f003c6b05bab900ec6bc69eb6489ba1aa4887515231cca2285ddaaad231`
- Source object canonical: `f19455b09214c2f09841c695564917d92473764dab4586b5962ef80cf4c304f8`
- Source record: `9634d380340030a875384b7bb095738072a6fb2940c7d961b227f25e00f67e4d`

### exp-v1-recovery-r23-rust-generation-0342

- Candidate file: `3ced51ade207072b067c11fa8409c0221b3d4bb54188f54fd752802042d9bbcd`
- Candidate canonical: `76bcc42b2f9c9a2b74dde6457404a305440d91486ab232523448be027e972b18`
- R21 previous canonical: `23aef207a98b3291deafda2ec465dd4e2b8c7e45dfdaa880390d4bbd600aeffc`
- Original parent canonical: `9130d034eb347f9d19e8bc8c67f68b7c018b6f6e6d4ee2a3cdc22b4997652634`
- Problem: `cfc34b2f401dcb7dcac891b908e006ebf8d55ba67e56f6ce4985f7f7a9f9e716`
- Answer/reference: `59e3282678fefdd3753f8890ea09fb37dcb3ca08927c8b3b865079a3f5170015`
- Known-bad: `5d53db9ba1640224a23c2804951892debb2a8439130c2845d5db0b2f01a745a3`
- Corrected test: `b6dddeb592ffc2e59eda18b152aa5825db8c47b5fdcf8374404a48fea4df2b2c`
- R21 test: `02d7afad7c9410bce18f57af12637e204d89cf3b60592fc8df6ee14d24841ec7`
- Source object canonical: `f8f21d40a250fb7dfe9f322ed64e9098c31783531738b4a58b83fffb14d58518`
- Source record: `bd320d0d81e852d74fc42a3f595ccf4779d6532d470f21a9a9ae0a46daa3c4ac`

### exp-v1-recovery-r23-rust-generation-0414

- Candidate file: `e8c05b0b108d0fa7df8819e31b89b2683efad156cfc036eda01f247344a39795`
- Candidate canonical: `ac86515ab7d89d6ca8389115e91fcb2e43d6d047d565a65b2649947b13aea7a2`
- R21 previous canonical: `492c4ad2c31b9d5e55d864a005d810d4607e6c833bccb7ec778c715c824a4d88`
- Original parent canonical: `967630134b4366dd6f569a3c43333edca71f3912974b87248f183a157041d60b`
- Problem: `ff7e586ef0f78c6ffe5ea1a6ef4073cce4a295ceeb4baecf7b9e8ce371fd5124`
- Answer/reference: `3adc4edc1ef15018c39712948b7a8a27b9db9521e2322a24879df827cc7620b1`
- Known-bad: `fbc9d845901b84dccb0b79fc08537a565005edba6b996ca96e72ee3f2a5bb21d`
- Corrected test: `9eb859f5a76ef81d36a25977afc1d18ede185f2f65f67c72fba01bbff8bf3f03`
- R21 test: `6a0e5f47a7d83e25a17e8f14bb51b15efc61d95d547579bf2afad7db4838b3b9`
- Source object canonical: `5193cf1d2a551c50f9a2aa26ae988735aa3028d72c8d084f03d274a598bd02b4`
- Source record: `a3bd7801d03dd4ee5860d6223ca12f96388eb694a2b821f77e6e44493fb29417`

