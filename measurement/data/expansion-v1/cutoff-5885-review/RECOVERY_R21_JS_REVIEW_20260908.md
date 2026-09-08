# R21 JavaScript full quality review — 2026-09-08

Gate 2. Exactly five derived candidates reviewed in full: 0034, 0061, 0090, 0097, 0119. Original full prompt/reference/test evidence and approved batch-2 scopes were reconciled with complete derived prompts/references/tests/mutants. Saved diagnostics were read, not rerun.

**One complete scoped positive: 0090. Three test-only quality holds: 0034, 0061, 0119. One reference/domain plus test hold: 0097.** No admission, execution, generation, critic invocation, retry reservation or central edits. Originals remain unchanged; zero new original coverage.

## Per-candidate decisions and minimal feedback

### 0034 — test-only hold

Reference correctly visits all categories and review-token indexes, preserving normalization, case-insensitive term uniqueness, canonical spelling and independently copied result categories. Submitted tests never construct a sparse category/token array. The mutant retains the old some/map behavior and skips holes in both paths.

Minimal specification-only feedback: add constructor categories=new Array(1) and review(new Array(1)) TypeError assertions, plus valid-prefix/trailing-hole forms for both. Preserve input nonmutation and known/unknown/empty token controls, exact duplicate-term message, category order and repeated-output isolation. Do not add trimming of review tokens or broader Unicode casefold semantics.

Saved diagnostics: reference, known-bad and original-parent reference all passed. This is inadequate defect discrimination, not a reason to admit.

### 0061 — test-only hold

Reference validates all measurements before its first yield, rejects sparse packets, maintains protocol selection and exact BigInt quotient/remainder, and emits new result/timestamp objects. The tests cover only dense arrays. Array.from on a dense partially invalid packet does not establish that rejection occurs before any result is yielded.

Minimal specification-only feedback: for a one-hole plural packet require canHandle=false and first iterator.next() to throw TypeError. Repeat with valid first measurement and trailing hole: first next must reject without a successful prefix yield. Retain both protocol kinds, empty plural success, ordered topics, exact nanosecond boundaries, sequence validation and detached outputs. No eager-call generator exception requirement, timing policy or unpromised concurrent caller-mutation snapshot rule.

Saved diagnostics: all three controls passed. No defining sparse witness exists in the submitted suite.

### 0090 — scoped positive

Approved contract clarification explicitly covers every own patch key, including hidden strings and symbols, applies recognized hidden string fields, ignores inherited fields, and validates before lookup. The reference uses Reflect.ownKeys and ordinary required-field copying.

Tests meaningfully apply a hidden title, ignore inherited title while applying own pages, reject an own symbol with otherwise valid title, and reject a hidden unknown property even for an absent ID. Atomic failures, exact field snapshots, sorted list, monotonic IDs and exhaustion after deleting the largest ID remain covered. No descriptor preservation, prototype copying or extra numeric cap is imposed. The original function-name reflection assertion is absent.

Saved reference passed; known-bad and original-parent reference both failed at test line87, the own-symbol patch rejection. This is a genuine required behavioral failure under the approved derived contract. The hidden-unknown test separately exercises pre-lookup validation. No test correction is required by this review.

### 0097 — reference/domain hold and missing-witness hold; not test-only

The indexed loop fixes sparse construction, and ordinary search behavior is sound. However the derived reference adds Array.isArray(entry) rejection. The unchanged prompt describes records shaped as code/title without non-array/plain qualification, and the original bound reference accepted a decorated array with those valid fields. A standard array with code='a' and title='A' therefore moves from accepted input to TypeError solely due to a new representation restriction. This was not part of the approved reference-fix scope, which preserved accepted record domains.

Concrete static witness: create an empty array, assign code='a' and title='A', supply it as the sole entry; the original returns the declared record through get('a'), whereas the derived reference rejects construction. This witness was not executed. It does not rely on getters, hostile prototypes or fabricated object behavior.

Tests also omit one-hole/valid-prefix-hole construction, so reference, known-bad and original-parent all pass the existing suite. A test-only correction cannot resolve the new reference restriction while preserving source. Main must disposition this source hold separately; do not silently narrow the contract, waive it, or include0097 in a test-only critic batch.

### 0119 — test-only hold

Reference visits every ingredient index across constructor/add/update, normalizes stored strings and preserves atomic partial updates and nested ownership. Tests omit sparse ingredients and impose TypeError for update('bread',{other:true}) at line96. The approved scope explicitly avoided a new unknown-extra-field policy beyond the id prohibition and validation of supplied title/ingredients; the frozen wording does not support this newly asserted universal rejection. Remove that assertion rather than replacing it with a new acceptance/rejection policy.

Minimal specification-only feedback: preserve the stated id-update prohibition, empty update, unknown-ID valid update null, and supplied-field validation. Add constructor one-hole ingredients TypeError, sparse add storing nothing, and existing-record update with valid title plus valid-prefix/trailing-hole ingredients rejecting TypeError while both prior title and ingredients remain unchanged. Keep empty ingredients success, trimmed duplicate IDs, order and deep copies. Do not infer a general patch-key policy from0090's distinct clarified contract.

Saved reference, known-bad and original-parent all fail at line96 with missing expected TypeError. This is the same unsupported oracle across all three, not semantic mutant discrimination. Correcting the oracle without adding sparse witnesses would still leave the intended defect untested.

## Seven-criterion assessment

1. Prompt clarity: four reference-fix prompts remain identical to their originals.0090's own-key boundary is the approved explicit clarification.0097 introduces an unapproved source-domain restriction;0119's test adds an unsupported patch rejection.
2. API consistency: CommonJS exports, function/method signatures, error/status behavior and result fields were read in full. No new descriptor/type/schema requirement is needed. Ordinary number and string domains are retained; no extra safe-integer cap is invented.
3. Independent test origin: archived author Tasks contain only id/problem, exactly matching derived prompts. Tests match archived independent output after prescribed strip-plus-newline normalization. Reference, mutant and original tests were not task fields. This establishes provenance, not adequate coverage or valid oracles.
4. Non-triviality: glossary indexed normalization and detached result collections; telemetry protocol/generator validation and exact numeric decomposition; shelf monotonic allocation/atomic patches; directory uniqueness/stable retrieval/ownership; recipe normalized CRUD/atomic nested updates are substantive complete targets. Patch size is not the criterion.
5. Idiomatic code: indexed validation appropriately rejects absent elements; Map/Set, explicit record construction and generator prevalidation fit the contracts.0097's new input exclusion remains a real scope defect despite otherwise idiomatic code.
6. Dependency isolation: standard JavaScript/CommonJS and Node built-in assertions only, no external packages or I/O dependencies. No generated code was executed in this review.
7. Realistic known-bad: sparse-skipping validation is meaningful in0034/0061/0097/0119; enumerable-only patch-key validation is meaningful in0090. Only0090's current suite demonstrates its defect. The others require the distinctions above, not blanket approval based on reference pass.

The0061 generator keeps validated measurement references until yielding, but the frozen contract promises detached returned objects, not snapshot isolation from caller mutation between iterator advances. No new concurrency guarantee is imposed. Likewise no universal descriptor/prototype guarantee is used beyond the concrete accepted-input regression in0097.

## Diagnostics and integrity

Diagnostics directory: artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js. All cited receipt candidate_sha256 bindings equal the canonical candidate inspected here. Each diagnostic control is classified from its actual result/exit/stderr, not the summary's directionality flag alone. All observed failures here are assertions, not compile errors/timeouts.

Plan parent hashes match immutable originals; rights and all source fields except versioned transformation remain original. Source is McEval-Instruct revision57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0. Candidate canonical hashes use sorted compact UTF-8 JSON, ensure_ascii=False; file/evidence hashes use raw bytes. Files reside in datasets/cache/expansion-v1/versioned-recovery/r21/<full ID>.candidate.json.

### exp-v1-recovery-r21-javascript-generation-0034

- file SHA-256: `9c283edf5361684292ebd8cccd5bc94cc6f01002ab510b341025fd4c3d496592`
- canonical SHA-256: `4f0cbf133323325866dfc807ef3f3f399b3127f0ca2f2b889ccf80d2744e9e85`
- parent SHA-256: `4d16032d68bb2d5e5cf60535b0edf67c3b5a8e1397f8a44988a75c5fb6df80ff`
- prompt SHA-256: `45da4f03a13fd9c303d286b5852c1adbcb0286a298f6b3f5b6b0b103212b411b`
- reference SHA-256: `f603a5c0729b15a0a5d8e95882c974e8b3c7c2f71008a4dc75ab9c97d088748f`
- test SHA-256: `16632fa6a29a9ca69fdb31df97b587fe55bceb51606cc651389cfc32c78098c7`
- mutant SHA-256: `ab8f5ab2391a7882c2eacb707c100df32c06b22778662c3c2dae489c721cecd4`
- Source record `row-26941`, SHA-256 `8a3af611be382bc79cb152e4ed5cfe8eeb4c4ad01e0c81319b00261034c8b184`; rights `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0034-reference.json`: passed, exit [0]; file SHA-256 `1b67bc06ab5faac37bea6db8d79efcfc7991c685367884b33b388825c739794e`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0034-known-bad-0.json`: passed, exit [0]; file SHA-256 `bab6bc5f1d3a5f249d6bea857525eaf4d442a2ad9ec8b701610f7a8c3b41d064`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0034-original-parent-reference.json`: passed, exit [0]; file SHA-256 `ba30db3a12aa18bf55d6ac6cb0d61cdd5300a445841fbc095e814fb416e95651`.

### exp-v1-recovery-r21-javascript-generation-0061

- file SHA-256: `d21f15ea11e3ba6ae42490036deeba6ecee17b0cdfdc19639a8dbc2ba493c2b8`
- canonical SHA-256: `1e76cc969898ba2699092735cdf86a97eb35922d28751e2ef50511c1a2cc8332`
- parent SHA-256: `08071ad6a6a8e77b4cddf1b6fcfd34268f384a12eda00a0396a58bbfeba6e80f`
- prompt SHA-256: `74c2f55d8b0f39db80a343db6f00100c4e0433054d0952a3eb82e44c28ab0100`
- reference SHA-256: `90af16c128bd7f7a36e9b283b2604f7b436c0978809d098ffea80c1d0039daa7`
- test SHA-256: `92730acf7affaf08d5ab31294a037c4c3a35573690b3d7118d9845c5562fae8e`
- mutant SHA-256: `72dd01601a3aa71f6c828c2e679980141e924430d6c81ed91dc89b219d14bbb6`
- Source record `row-00458`, SHA-256 `1d9b1ce15dea8656592b52316ea3a0fec2cd723ec394a85aef6423b32d4d8b8c`; rights `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0061-reference.json`: passed, exit [0]; file SHA-256 `aebe6e5c04af0e6453d34aceff6ae302745b1ae14a92a46ace1073e07abb6e78`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0061-known-bad-0.json`: passed, exit [0]; file SHA-256 `308e6fa85daa3c22ee30731f6f70deeaba27126c4cbff619dfcc76458382c57f`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0061-original-parent-reference.json`: passed, exit [0]; file SHA-256 `346033795aebc48654813d20820878abdd4acf76290c1360b95d0b672512d102`.

### exp-v1-recovery-r21-javascript-generation-0090

- file SHA-256: `6f3872b4b5bb4c45c767f0f7f75d938107f09c82c10a8e56b825662e5cfea02d`
- canonical SHA-256: `ff503fefcbb93dda9536602522eab8616ed8d393af675dc0c7f02357631528c5`
- parent SHA-256: `b42fa2345b2535ea180cc08fd6a38a2ea408f7a563832b7ecc318ad5799a968e`
- prompt SHA-256: `d72673d2fd27caa099c1ae8ae86560bcb64bf43de05dec72ce22cd9126295265`
- reference SHA-256: `8350f2c58fd1df651ddc2b7125e993eccfe609692d68fc739ea932fc0e059659`
- test SHA-256: `fe9ae0ab6b5d7aee0107b71102588d48f0a543f2a898839f8c47e2071272be58`
- mutant SHA-256: `06f810c757102638181e0648b7159216c8387934da2555adef16d4f93bb71ac6`
- Source record `row-10914`, SHA-256 `f748cd2f99d921b0a4015e3697bd832d50cbb10eb9f17b9244b9ae6378b4403e`; rights `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0090-reference.json`: passed, exit [0]; file SHA-256 `3d88f7b3e50767d68e198ae532ce410500e8c1ae7cc9a74aa189d7b0b78fcd24`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0090-known-bad-0.json`: behavioral-failure-requires-review, exit [1]; file SHA-256 `49ec3d79f5a223316fbaba79286eaf576ab88a1c57e822da4d472c92df098306`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0090-original-parent-reference.json`: behavioral-failure-requires-review, exit [1]; file SHA-256 `c0564702a9f7874c1d03483e7f2cde0b8dd7c6e33b8d9d64cedb8858a54ba740`.

### exp-v1-recovery-r21-javascript-generation-0097

- file SHA-256: `08936f49c713221dfef86fc2a08e872f9d6f3fe80fa91ff45222680b610a88fd`
- canonical SHA-256: `bb1f6bb322941519e7becb48aa177b8b38d9b6a61edb732a4f69dbaa433be554`
- parent SHA-256: `bb5f15cd9c13402bb76132464f96fedc08e95f446849d93a289655da4d60830a`
- prompt SHA-256: `25253e6ad0f560a0c45c9ce198439c104a729558ed173045a431475e267e4df0`
- reference SHA-256: `9e1373abbda520b2d7c79590e9ec683da3ba53bc9cdcf5424e12efb736cc9f1e`
- test SHA-256: `b47bfac7354e5635562e299103223416f75cf04f7443c0b211f1a1719b39ae44`
- mutant SHA-256: `8d981862b909645ae39af5b273f6552b85e602ccc3d2a15971da21a1a990311b`
- Source record `row-10886`, SHA-256 `e9945de7d5ebae9e6b8214b3d12bb1d628b913a02c66b3ee2f0f71fd2a951aaf`; rights `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0097-reference.json`: passed, exit [0]; file SHA-256 `95fc302727f326fffa56975884dab7def89400814a0ad3bb259fedfdeaec42b4`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0097-known-bad-0.json`: passed, exit [0]; file SHA-256 `4ac3823b4aa9f9ee3c0d855c3af71d722ca2076e9d3835dcec0c8b46897f72f4`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0097-original-parent-reference.json`: passed, exit [0]; file SHA-256 `bafc2c000a647089aae024dbbdea76311f90602895f583e290287749b2b0f2b2`.

### exp-v1-recovery-r21-javascript-generation-0119

- file SHA-256: `6d1d8be5b6a33ec4a50e69691be01942ef37200085088795d956b98515dc2b90`
- canonical SHA-256: `658d770a922455bbcaef9965b8c3c506787d4b2148d389c3027a1ea2d53568a5`
- parent SHA-256: `74e1d6caa1a6ffbb6faec18c7dcdb39b7eb2290c4cb8a8724eb6148370c04715`
- prompt SHA-256: `343ae18119a895d6712bde36bcb1780712952a8c3af9d444cbd68da07e4ce4f0`
- reference SHA-256: `1830c84ebe9987d703c8a6745fbb8660d54760214dda8cd1a36292196fdc9d30`
- test SHA-256: `3defbc6e0dfd3e5654ac4d7129dbcfb8d4b1657d308ab1c10014f33d59a550c9`
- mutant SHA-256: `7905c995d1ab009229a61a313ba945b2309c8185c35bd651eec64793cc477efe`
- Source record `row-06759`, SHA-256 `b994176cea0b1ef8ac7450227ae93824318fea927afcce78ae14aef1084bc0a2`; rights `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0119-reference.json`: behavioral-failure-requires-review, exit [1]; file SHA-256 `3f3c0a7d3ddcedd3b0ffba3845add65f9578aeabd47fe4346263c2d9d15d88ab`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0119-known-bad-0.json`: behavioral-failure-requires-review, exit [1]; file SHA-256 `39a463622d1173e57330a5b643ef5ab4edb24033cd51fadfc7dc874ef36ad42d`.
- Diagnostic `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js/exp-v1-recovery-r21-javascript-generation-0119-original-parent-reference.json`: behavioral-failure-requires-review, exit [1]; file SHA-256 `7537d48c8b9891c4ba4fb6e27f47c0b7a5dcda2b0f59fb98db46469c12bd0e19`.

## Shared evidence hashes

- measurement/data/expansion-v1/recovery-plans/r21/plan.json: `a5fe5bbb1cffe149091f626ed317a0e79c39985c10c883acd8f83df3c04582ca`
- datasets/cache/expansion-v1/versioned-recovery/r21/javascript-recovery-independent-tests-evidence.json: `01f7b43cbf0bc3de7b23c62adc0e29895ef415f9eda8509f87aa28b295f8764b`
- datasets/cache/expansion-v1/versioned-recovery/r21/javascript-recovery-architect-evidence.json: `b33835a09bfd559fc837417836ec794a981e31b0754399bab29918c7f2d03119`
- datasets/cache/expansion-v1/versioned-recovery/r21/run-contract.json: `a455daccb7e85a30c3cc86d4c328ee44be8e6fd166afef6fe685bba9c8225be4`
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_JS_TS_BATCH2_20260908.md: `0889609953fc9e3ff7f43f76bf1e3030dbcad822805ea3a177d30d6253c71cea`

