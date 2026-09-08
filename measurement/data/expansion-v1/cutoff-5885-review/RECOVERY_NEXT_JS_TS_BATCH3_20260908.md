# Next JavaScript/TypeScript recovery selection — batch 3 — 2026-09-08

## Result and boundaries

Propose **18 fresh held originals:9 JavaScript +9 TypeScript**. Shortfall against15+15 target:6 per lane,12 total. This bounded accelerated selection does not assert that the remaining pool contains no other recoverable records. No reservation, request/plan creation, teacher call, execution, admission, GCloud or central mutation. Originals remain unchanged and all holds remain in force. Zero new original-review coverage.

The r1–r23 plan exclusion join contains **153 unique original parent IDs**; all18 proposals are disjoint. Main must repeat the join immediately before any reservation. Corpus bytes SHA256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`; additional-holds.json bytes `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`. Each historical diagnostic's candidate canonical and complete original_task match the original candidate/verification_task, verified directly. Historical JavaScript failures have exit[1]; TypeScript probes compiled before runtime exit[0,0,1]. These are archived witness evidence, not newly executed tests.

## Seven-criterion selection policy

Complete prompts, references and original tests were read for every proposal, together with source/rights records and the exact historical hold test/output evidence. Targets below have substantive interacting validation/state/order/ownership/grammar behavior. A small repair is not evidence of nontriviality; per-target rationale follows. Coherent API and minimal semantic correction are required. No elementary hold, compile-only defect, private-representation probe, unsupported extra-field guarantee or unresolved broad contract is used to fill quota.

Future corrected artifacts still require all seven quality criteria: clear prompt, consistent API, independently authored tests, nontrivial target, idiomatic reference, isolated dependencies and a realistic semantic mutant rejected by valid tests. Original tests are reference material, not future independent author context. Standard-library-only scope is preserved. Proposed recovery is not an admission or rights reassessment.

**Request-class discipline:** every repair proposal uses oracle-rebuild because a fresh isolated mutant changes the embedded broken source. Preserve all behavioral prose/API/domain/error/ownership rules, replace ONLY the complete embedded source with the exact returned mutant, and update stale nonbehavioral diagnosis if necessary. Never pair frozen original repair prompt with a different unembedded mutant. Generation reference-fix preserves prompt bytes. TS0382 uses oracle-rebuild because original oracle accommodation must also be removed; its behavioral specification remains unchanged. Do not add algorithm mandates to prompts.

For sparse witnesses, reject genuinely absent slots whose accessed value is undefined under the stated element validation. Do not demand rejection of a valid inherited numeric array value unless the contract expressly requires own slots. For property witnesses, preserve named or explicitly required keys; do not infer arbitrary extra-field deep copying or descriptor/prototype identity.

## Ordered proposals

### 1. exp-v1-javascript-repair-0015

Change class: **oracle-rebuild**. Substantive target: Whole-graph validation and cyclic reachability with side-effect roots.

Minimum correction and decisive witness: selectModules({unused:{imports:new Array(1),sideEffect:false}},[]) must throw TypeError even though unused is unreachable. Validate every imports slot before traversal; retain corrected sideEffect:true inclusion, cycle termination, lexical order and dependency closure. Validate sparse entries as well without changing valid name grammar.

Independent-test requirements and contract limits: No new own-property-only graph policy or plain-object prototype restriction: preserve source domain. Whole-graph malformed checks must not be deferred to reachable traversal. Independent controls: empty graph, unused valid module, side-effect dependency chain, duplicate entries, missing imports and cycles.

Realistic new mutant: Reintroduce skipped sparse imports validation only, with original side-effect correction intact.

Historical hold: Sparse imports in unreachable module bypass required whole-graph validation.

- Parent canonical: `71df1c6b0aca82937922d83679fa3c7826e9a44610a5d83a28d1db08a31b45a9`
- Prompt: `8262068bdb1fb3cb7252eccf39296bbecda3815d6f7ebd65b303122b580b7b81`
- Reference: `57b6c557e36aaa6ce2a06a5848346288cf71717aa9a95dcac6991fd3a23a0a31`
- Original test: solution.test.js `e834d14997077216eb7328e5fc31f04b72eaa43c6dd92f43d294b4a043843911`
- Source object canonical: `4a196ba7b4e1c2c2faa5c76004a64156e92b12cfe7bcf7a2dbd44f40bf1e452c`; source record: `d60d443cecaee2fef8b62a983d03989c6276f5b5ca9bb472b602c9366583173d`
- Source: m-a-p/MdEval-Instruct, revision `38c9197e3add996fae624eb198ebd06155b2101e`, row-14196, license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `a3e396228fad34ca5f403ae971301e372d1d682d604120bf8579ef116d4f2c58`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/module-unused-sparse-result.json; file SHA256 `c6e7b2860be8bd42522015b14b0165b9d231ec80dd1b2979b055fe548941eb73`; diagnostic test SHA256 `8a64d8294d8c38d3111d23efdc06f177f1f264e208620ca00dca94e1be63fefd`; archived exit codes [1].

### 2. exp-v1-javascript-repair-0048

Change class: **oracle-rebuild**. Substantive target: Sequential asynchronous dispatch, stop-on-handled semantics and preflight atomicity.

Minimum correction and decisive witness: handlers=[()=>{calls++;return 'handled'}]; handlers.length=2. Returned promise must reject TypeError with calls===0. Validate all indexed elements before any callback; keep await, first non-undefined result and exact thrown/rejected error propagation.

Independent-test requirements and contract limits: Preserve original async promise behavior; do not demand synchronous throw from an async function. Controls include false/0/null results, awaited undefined, rejection stopping later handlers and nonmutation; no callback scheduling guarantees beyond sequential awaiting.

Realistic new mutant: Restore some()-based sparse preflight while keeping awaiting fixed.

Historical hold: Sparse handler array bypasses atomic validation and invokes earlier handler.

- Parent canonical: `f5544deae2ef298ee0543374315fba07322d8144baaac5d641e7128b9fb7ec60`
- Prompt: `d23cbf7bfad6a3dbcd3e524bd153de0ab308724b3a4808e047cb1774a0c5e674`
- Reference: `fece1b918f7f8e3abd733f311763eab8f629acb01052b7131b000bb652295d79`
- Original test: solution.test.js `fb0d2f4b70299a98465de30884394d3d27bbe5d9a3c80def63822df0f63b5f98`
- Source object canonical: `686b68c5fd0fdda5d722d00d907fb619d8b1a5575a8e6c36d70cb9c6a449fe9f`; source record: `dec4f717ab2f2b7980192118ea0ae48ed8018014770c87a36f774ead95a42391`
- Source: m-a-p/MdEval-Instruct, revision `38c9197e3add996fae624eb198ebd06155b2101e`, row-09237, license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `bc62cc3f7798f9c5ccf9e896ed2fceff453189e6e387b036514a82a3e9b66e6b`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/dispatch-sparse-atomic-result.json; file SHA256 `afae89f0f87678cb1f7cc9456aae2e9d183a85b8262f0271fbba88cf87819f4e`; diagnostic test SHA256 `49ba09eaad68570ffa2f7359b30baff50e409a0fefb695cec9d8103bc44fe62c`; archived exit codes [1].

### 3. exp-v1-javascript-repair-0051

Change class: **oracle-rebuild**. Substantive target: Thenable pipeline ordering, propagation and validation-before-effects.

Minimum correction and decisive witness: steps=[x=>{calls++;return x}]; steps.length=2. runPipeline must reject TypeError without incrementing calls. Perform complete slot validation before invoking any step, retaining awaited fulfilled value flow and original seed for empty input.

Independent-test requirements and contract limits: Original async source establishes rejected-promise error delivery despite prose shorthand 'throws'; preserve it and native Promise return. Keep identity of thrown/rejected errors, thenables and array nonmutation. Do not introduce snapshot semantics for caller mutations during execution.

Realistic new mutant: Restore skipped hole validation with sequential await still correct.

Historical hold: Sparse pipeline step causes validation error only after an earlier step has already run.

- Parent canonical: `5ecf48de78e5bdc267bf7f0ff3de2b164614291491a1de990752d9360c833406`
- Prompt: `a1f32341eaf9f55a0d69cfde46f865a4df9468441f63a347b143c000acac662b`
- Reference: `a347c81786d0a072a047c3a0786d0c2d1e6b0afc9ae0fc79c0e9ed4378f86d48`
- Original test: solution.test.js `0160f4e41c39cff337d8e73ce3459cb7f2018aa9fbc6bdd3f8787aa2e624e3c0`
- Source object canonical: `1e327e487c447b9a567e571fc2af11053776010ebf745eb1b4761e2dfbf282fc`; source record: `d41f8a55afb2015b36bbfdcc688b148ca7bcbfacb489d51f81aced3a622fc120`
- Source: m-a-p/MdEval-Instruct, revision `38c9197e3add996fae624eb198ebd06155b2101e`, row-03174, license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `39b9ef4ef65d9ba8af0829a695b49cc8bdb5f9e7b3f800fd762180065487290e`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/pipeline-sparse-atomic-result.json; file SHA256 `145add563b56b702debe566365c8561d6ead11462181bca7efcbf53040b6d13f`; diagnostic test SHA256 `71dcb0c3a83ed65ea46bdfabcd2509e9f3a2fed9e3936dd65a1d3aceac29ba6f`; archived exit codes [1].

### 4. exp-v1-javascript-repair-0240

Change class: **oracle-rebuild**. Substantive target: Routing priority, first-match stability and independent descriptor snapshots.

Minimum correction and decisive witness: createRouteTable(new Array(1)) must throw TypeError at construction. Validate every slot, not map-skipped slots. Keep exact method/path matches ahead of earlier wildcard and first among same-class matches; copy named fields directly.

Independent-test requirements and contract limits: Handler value may be undefined/null/anything and must not be deep-cloned; it must be an own property as specified. Preserve source method grammar (nonempty uppercase comparison), not a new alphabetic-only restriction. Test sparse singleton/mixed descriptors, required hidden handler, input descriptor mutation, wildcard fallback and no-match null.

Realistic new mutant: Restore hole-skipping descriptor construction; original exact-over-wildcard correction stays fixed.

Historical hold: Sparse route array is accepted during construction instead of malformed-descriptor rejection.

- Parent canonical: `844f40ede452ad2f8dcb1bdc1b60dbfd655c431a38bfdbde5e2e5411ab45e47f`
- Prompt: `fa59ff63baefc132cab66e024f67115f948e18b03ed61480a178747d0b056931`
- Reference: `06995474e0bc96a7f2940e2d2b684295afc2d346ed17c58fabc6d30f30342073`
- Original test: solution.test.js `f9d88e1aaad2dc1a098db6c4edda6e20adc74af5ef9706946a975ac468809762`
- Source object canonical: `51f53daf52ff74d678d8c82cffa3deceb2177cdd0b94c8ddc893ba1e13fff2a6`; source record: `f6a023ce95c1f33f82aa797745aa97cb2586e6d6be28f666d7d9515ef05b3797`
- Source: m-a-p/MdEval-Instruct, revision `38c9197e3add996fae624eb198ebd06155b2101e`, row-03266, license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `6d67e665a27ca4ebf0b4735855aba4f57e1376568e5e5366a8d8225380b14456`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/routes-sparse-result.json; file SHA256 `6fcbbc166aa551fbba87fc38527721f0563136fa749db2debf759d07f070921a`; diagnostic test SHA256 `5596439f066f31395a08ef0ebe8c1051437adf7f1f208cd2dcd33ebaa269f53a`; archived exit codes [1].

### 5. exp-v1-javascript-repair-0043

Change class: **oracle-rebuild**. Substantive target: LRU recency/eviction, key identity and payload ownership.

Minimum correction and decisive witness: touchAssetCache({order:[],entries:{}},'__proto__','asset',1) must yield order ['__proto__'] and an own entries key with value 'asset'. Create own data properties without invoking inherited setters; retain least-recent shift eviction, touching/replacement and payload reference reuse.

Independent-test requirements and contract limits: Also reconcile explicitly required own string keys independent of enumerability: a non-enumerable own a with order ['a'] is valid; unknown non-enumerable string key outside order is malformed. Copy required keyed values by order and validate full own-string-key membership. Do not require a particular result prototype/descriptors or cloning payloads. No unsupported symbol-key policy added. Test proto key insertion, retouch, survival/eviction and capacity zero.

Realistic new mutant: Restore unsafe ordinary-object assignment for __proto__ while preserving correct eviction.

Historical hold: LRU cache loses valid __proto__ key through Object.assign to ordinary object.

- Parent canonical: `3822324e93b766c419edd046ca664a44c8278c202ef4621f250c709c5e6b45a1`
- Prompt: `7d7a7d8916aac80c7cb5a3c855c5ff50b50ea8252db83a231fc4737e4ce90dfd`
- Reference: `90bfe76e94acbb9a2df26122951c1142e4739c69e1565a9619e7e3a0e501e917`
- Original test: solution.test.js `1c98b775cff2a53e2abe7b8c8bba7f46c8683abd805a69480f00640527418154`
- Source object canonical: `34f74fb990bd081c6d087bb70540cf86755cd01273cd8e655810c117b5592b5f`; source record: `6234809bced4c502d0467a8e4728f106d94d0f6c52fc9c39343ebc3431ee0243`
- Source: m-a-p/MdEval-Instruct, revision `38c9197e3add996fae624eb198ebd06155b2101e`, row-07988, license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `2958f96fd018d71eeeb7437f3a2ff99fa683d98a5437258b532bcc16aea45602`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/cache-proto-key-result.json; file SHA256 `ad7ba7aa688066f207426e4b5dc2066e1b6db4faa2c8e184fa19407c81f58972`; diagnostic test SHA256 `302d5b139ccbde1d5bfead5270d061485c94d6060894551e5be323ec17bcaf91`; archived exit codes [1].

### 6. exp-v1-javascript-generation-0292

Change class: **reference-fix**. Substantive target: Whole rectangular-grid validation interacting with bounded movement and detached positions.

Minimum correction and decisive witness: moveRobot([[0]],{row:0,column:0},new String('N')) must throw TypeError, not treat boxed text as exact command N. Require primitive exact membership before dictionary access; retain full-grid validation and movement logic.

Independent-test requirements and contract limits: Do not add safe-integer position bounds beyond actual grid/index validity, or new position fields. Test boxed command and coercible object, all four primitive commands, blocked/outside stay with fresh object, malformed distant cell, sparse rows/cells and nonmutation. Avoid asserting Object.keys insertion order merely because result contains exactly the two named fields.

Realistic new mutant: Allow property-key coercion again while all other movement and validation behavior is corrected.

Historical hold: Reference coerces boxed command strings rather than enforcing exact primitive command values.

- Parent canonical: `62963b6c604808fa36f01def4b09190c5fbab0f997d2a191face5321f477bc38`
- Prompt: `f52acc2ad2f434986b92081c1d3d94e9c94554346dd78acaa25d09a6bec7a88e`
- Reference: `852e81d0a5128243d2a06fbe00de3c384d4e20576d266a8999609c380d5130f6`
- Original test: solution.test.js `7ac0874e168becb5703fd73118718929c9535e97c9798bfb40ef18d2c77a321a`
- Source object canonical: `a8a4f95b3c066ab1fffc2bba73d8346753db8b9450779894e5ef4801e8975173`; source record: `ccefb7d9983b1c6a9c0ff788151ed0f947772372e767b324f5dc87474ffa2320`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-26721, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `bd78fe400dec9594cc354f865283a40caee72c286ea703fff8fd90ea9e6be21d`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/robot-command-type-result.json; file SHA256 `2613728e58ad543a404048e38677c5c9532e1262808a6130ab8bb87aaaeb08e5`; diagnostic test SHA256 `51c82577d87b6c63c770766c5c684f90c6b960522f2c9b4433d58585377b5eb3`; archived exit codes [1].

### 7. exp-v1-javascript-generation-0120

Change class: **reference-fix**. Substantive target: Candidate normalization, complete validation, filter composition and stable multi-key ordering.

Minimum correction and decisive witness: selectCandidates(new Array(1),{}) must throw TypeError. Fully visit candidate slots and nested candidate.skills/criteria.requiredSkills slots before filtering; a single missing skill must be a TypeError, not accepted undefined or mislabeled duplicate RangeError.

Independent-test requirements and contract limits: Preserve trim-based IDs/names/skills, score0..100, after-trim duplicate RangeErrors, default optional fields, case-sensitive required skill membership, stable equal sort keys and fresh skills arrays. Include malformed candidate that would otherwise be filtered out and sparse requiredSkills even with no selected candidates. No new extra-field or inherited-option restriction.

Realistic new mutant: Restore sparse candidate skip only; keep nested validation and existing sorting correction sound.

Historical hold: Sparse candidates bypass object validation.

- Parent canonical: `264d5b2a8d304128c06308afed6d8de3be2250ba7690f4531cac83f4b238705d`
- Prompt: `fbd7759157b096cf29a3e26792567a8740c488379f1d8f137550ced6378fd1a5`
- Reference: `d198d4ea13deaef1285d7682255f353697df6c14b80706ef6c8df2250301a842`
- Original test: solution.test.js `79fc3112008e2eb4cef03203e02e85ebb06924ba7cdf110f7850d0f5f167f38d`
- Source object canonical: `32b19b39964321ab3face50aa377481c54c750f66928e916ae6262ead0a74591`; source record: `69c6cfffad19490be61a88c476d533da295ec04d364fe78a0011f976745c23a3`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-06678, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `4ce4257a43f7a579d89837c61bacd44ae3e57b5dbe5cea664683594a9a396bc1`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/candidates-sparse-result.json; file SHA256 `09174d481b2a55c4d3159eb7c87fa9c56d7c198a585349c794bf77db80b00cc5`; diagnostic test SHA256 `bde2f88099c394ce6162925825066f613df1be220d730d4223798e010f950d39`; archived exit codes [1].

### 8. exp-v1-javascript-repair-0132

Change class: **oracle-rebuild**. Substantive target: Ordered formula neutralization followed by CSV escaping, preserving literal text.

Minimum correction and decisive witness: serializeSafeRow(new Array(1)) must throw TypeError. Validate all cells rather than every()-skipping holes, retaining all four formula prefixes and neutralization before quote-doubling/wrapping.

Independent-test requirements and contract limits: Keep precisely spaces/TAB/CR/LF for formula-prefix whitespace; no broad Unicode whitespace expansion. Independent expected literal outputs for quoted formulas, embedded quotes/comma/newlines, leading apostrophe, harmless text, empty cells/array, and nonmutation. This is composition of two distinct transformation stages, not only a regex-character patch.

Realistic new mutant: Restore hole-skipping string validation with all four formula prefixes correctly covered.

Historical hold: Sparse cell array bypasses string validation.

- Parent canonical: `465586f80d03674e2729e059ebc486a4ed5713cb636e84bbba9dbd26c11aa34f`
- Prompt: `a1811ecb849550923639f9cfee7fadda1d6652e134b034b175241841616df6d9`
- Reference: `4ce7eddb034e44e970e8c5dee14feefd5e08bc4220244c20753c17b176167de8`
- Original test: solution.test.js `4aac19d7326ff2f8d83170f9ef08b0f7c435741ec3e721b1fd3f2e43f7323cf1`
- Source object canonical: `1d579bb664253b3c4cb9ce25069806cb2433d6d07f3104db3458413a737484a4`; source record: `624685d8208b0057afa1bdff2293f40d6b6cdce44373368ce4c40dae2891436f`
- Source: m-a-p/MdEval-Instruct, revision `38c9197e3add996fae624eb198ebd06155b2101e`, row-02750, license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `532ed09dcb298a7618075fd0c64f1bcad34382bfe58ae21b051a4b4a56c40800`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/csv-sparse-result.json; file SHA256 `6877afe79da531543f95540112f34348e719844c976d283b048a4f0609713c41`; diagnostic test SHA256 `6344eb1c05480d790c898ffbe2e3d0547ac13e3d3892ea137381fc120efdb46f`; archived exit codes [1].

### 9. exp-v1-javascript-repair-0003

Change class: **oracle-rebuild**. Substantive target: Validated manifest lookup, duplicate/missing classifications, requested order and independent records.

Minimum correction and decisive witness: selectBuildPages([],new Array(1)) must throw TypeError rather than return a sparse array. Validate requested slots fully; retain duplicate/missing RangeErrors and copying correction.

Independent-test requirements and contract limits: Required slug/revision/content fields must survive valid ordinary property access even when non-enumerable: reconstruct them explicitly in returned record rather than relying only on spread. This is named-field preservation, not a demand to deep-copy arbitrary extras. Keep whole manifest validation even for empty request, exact nonempty strings including whitespace, safe revision bounds, requested order and empty-input behavior.

Realistic new mutant: Restore requested.map hole skip while preserving required-field copying and original independent-result correction.

Historical hold: Sparse requested slugs bypass required shape validation.

- Parent canonical: `add930de98c1fa45c4b693faeefdbbb7862eef5b110f3532a548c668c2c391e4`
- Prompt: `a8e68e4539b60660f04151bca79c2140c8a42ff116af57fe5aa890c595f385bb`
- Reference: `a9d28626576934f2978f77e56793ea9b4ec5d51bc499c2c102f23d1a8cd80865`
- Original test: solution.test.js `ee17f315593088acc502a962f35b825968e44efdcae5eb079396e4859e16a29b`
- Source object canonical: `b148efb8660b5da1f4d5dddb4313213b796a5b9adcb559c56389134762624b4f`; source record: `487febb53bff29e747d438fae3d8688ecb1f956cc5194ae150f75a5cef571c33`
- Source: m-a-p/MdEval-Instruct, revision `38c9197e3add996fae624eb198ebd06155b2101e`, row-06064, license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `b479fcc9929f91764886416898160643f9e008cc1689b2c696587808427fd7b4`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/build-pages-sparse-result.json; file SHA256 `8203e6d66f4ccf9e81a43ee7074d3b939b5e578cefb70cbcce4235b051c80bde`; diagnostic test SHA256 `a343b90ee98931230cc423c0afae62c1af9a8331808924f1b7170752f0ac222a`; archived exit codes [1].

### 10. exp-v1-typescript-generation-0294

Change class: **reference-fix**. Substantive target: Observable replacement atomicity, per-registration lifetime and defensive notification copies.

Minimum correction and decisive witness: Register A,B,A then unsubscribe the last A twice; replace must notify A,B in that order. Use distinct registration identities, not callback indexOf. Also replace with title 'new',tags:new Array<string>(1) must throw TypeError, leave prior state intact and notify nobody; constructor must reject same malformed tags.

Independent-test requirements and contract limits: Keep trimmed title/tags, valid empty tags/duplicates, snapshot listener timing, per-listener fresh copies, no initial notification and nonfunction rejection. No added callback-exception isolation. A single correcting reference must address BOTH ledger defects; independent tests cover both.

Realistic new mutant: Restore incorrect callback identity removal only, with sparse tag validation fixed.

Historical hold: Final duplicate unsubscribe removes wrong registration; separate sparse-tag probe also accepts malformed replacement and notifies.

- Parent canonical: `5b3f759e01ed5df9ac801d7dc639963f09568820de828828051e5a461072fb4f`
- Prompt: `cd5ca15648adb86896b25b15026017f2e97dedaf223e7138853ad2d5112e02ea`
- Reference: `6b624b7771202f601aa0ac4a8d9b7cbbc2ec43ca0428d5745cb22b9be8cb02ca`
- Original test: solution.test.ts `7fe45c5eab574d4e3df313bf44894efd7964befcb5b7228acae61a77140f887e`
- Source object canonical: `ecda63c22ecaf4019324f34eac44ee8776279944a9e1f0db7717d17fdd7ff775`; source record: `91c45d3dda6eef386f52513c5b4891329f5311810d4555c71a6d7495a098f89d`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-32734, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `51960363968c81badad90ccbcd985930869f88c740cfa9684109625dc6cd75eb`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/document-duplicate-result.json; file SHA256 `c6d94e6538dbe6cde768340ec39b090e9f2b1b99a20b04be9ff16cc522e7ecb4`; diagnostic test SHA256 `7446c48b30c7bd47911fd0d473ef2eac9d35c792768f038ac5b440c912d59581`; archived exit codes [0,0,1].
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/document-sparse-result.json; file SHA256 `d50e53603e0c9950fd7e937ea590d513bbdbd6f5fa387be52a8ed5a24b490a61`; diagnostic test SHA256 `60172d367929f9093df0f363d9409202bda2e17869dc590c58eb04cf1976253f`; archived exit codes [0,0,1].

### 11. exp-v1-typescript-generation-0366

Change class: **reference-fix**. Substantive target: Multi-event subscription identity, insertion ordering, snapshot changes and immediate exception propagation.

Minimum correction and decisive witness: Register A,B,A on create, unsubscribe last A, emit: expect A,B. The closure must own a registration token and remove only it, idempotently. Repeat on another event to ensure buckets remain isolated.

Independent-test requirements and contract limits: Keep exact event names, current unchanged title, blank/nonfunction TypeErrors and snapshot changes applying only later. Listener exceptions stop immediately and propagate unchanged. Do not add per-listener event-object copies; that is not promised. Public event carries the corresponding name/title as existing API; no extra field is introduced.

Realistic new mutant: Restore callback indexOf deletion with duplicate registrations otherwise supported.

Historical hold: Unsubscribing last of A,B,A removes first A registration and changes order to B,A rather than A,B.

- Parent canonical: `f7c2a72a9d9031d3ffad9c48d1b3a6f82219afb4677bfe3515cba44ef42efa64`
- Prompt: `cbccd01987d29e94683586f1f6cec54cc7836c0b4086ac311a58283af641a4f9`
- Reference: `b2685366f7f516d3ddfd342f806359d742562b161673dedfed8f5df8543b8167`
- Original test: solution.test.ts `657b097417ce4d02abbb4377905c2c95eb64877fed2338f7314d340896832fb6`
- Source object canonical: `4b2a0cd317b510184fb182c0fa13fd817182f9f4f367b80226c6b994a768a26b`; source record: `f2abb47eda2e3a2d3a2062d239d15f84ab6f0b01d6bb32155210d9f9b7c9f383`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-33158, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `9edc9ec5cf0375268091bd4fa6ec9789e7756578e3abefcf13eed959a88dced0`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/header_0366_registration_probe-result.json; file SHA256 `54e8ef3280eeaeb8f988f82e3a314972d2c20ce2b0bb428898d2d1bf1d032ff6`; diagnostic test SHA256 `0b8be4922042e3bfa888365542739de41d718f7c7b43efd05a659319dc91d3a7`; archived exit codes [0,0,1].

### 12. exp-v1-typescript-repair-0211

Change class: **oracle-rebuild**. Substantive target: Survey state machine, required-answer gate, resubscription lifetime and defensive answers.

Minimum correction and decisive witness: Subscribe callback A, invoke old unsubscribe, resubscribe A, invoke old unsubscribe again; after valid draft->review->sent transition A must run once. Add an active guard on each returned closure, keeping source Set-based duplicate behavior and all stage transitions.

Independent-test requirements and contract limits: Do not enlarge into duplicate-registration multiplicity or snapshot iteration policy not specified by the repair. Preserve Incomplete survey and source Answers are locked errors, answer trimming, no-op transitions, reset retaining current subscribers, per-listener answer copies. Existing invalid-one-answer fix remains intact.

Realistic new mutant: Remove the per-closure active guard, retaining required-answer and copy corrections.

Historical hold: Repeated old unsubscribe removes a later subscription of the same callback, violating idempotence.

- Parent canonical: `a0f31f22a8d704c068cf3b5ce3673fd2fc5c977c83534fd3b208f98ca18db16c`
- Prompt: `c62997224d2c85bb33daa30e3fad606aa00ea495d0d9da99a9ec14c65f8fa999`
- Reference: `8f8c487159adf6ac45237063b0a5687ef458813cd13004996c484b9a6737a6ce`
- Original test: solution.test.ts `4a6a237dbfc418adade2643ae68c5ba146c453cc9b11ad11bd8a595975662324`
- Source object canonical: `322e44ae6c495ad312ea2cb167e4b4fdeb23aafc2a7105604fa12ebfa4809cb9`; source record: `714834166c1c38cf7b0b9d5103f7d216c7b65eee56163dd9b5c7e16ad144fed3`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-32788, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `e145a56ec89590d9c93445693c3eabedb2860f87880fc5e997a95f33a030015a`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/survey_0211_unsubscribe_probe-result.json; file SHA256 `24874d89366cb5c6f8056c77f9f2387fa22543c31f9926c890d8265083b56d06`; diagnostic test SHA256 `7530cf3527280d660a4f761b9f2c6c09c5ea53d77639531cc6df42d6be9430ca`; archived exit codes [0,0,1].

### 13. exp-v1-typescript-generation-0382

Change class: **oracle-rebuild**. Substantive target: Shared service/controller event semantics, snapshot mutation and individual subscription lifetimes.

Minimum correction and decisive witness: During one notification register child A and child B; after it finishes unsubscribe only A, then next state change must notify B. Apply same witness to controller dismiss listeners. Remove owner-group deletion; closures target only their own registration.

Independent-test requirements and contract limits: Original tests overwrite the newest child unsubscribe after creating a child on each emission, then wrongly expect no older child to remain. Rebuild those expectations: the older independent registration survives until its own unsubscribe. Keep unchanged-state no-notification, toggling/delegation, dismissal true without drawer mutation, insertion snapshots and idempotence. No new callback exception policy.

Realistic new mutant: Restore owner-group sibling deletion; source/API and all other state behavior unchanged.

Historical hold: Unsubscribing one child registration removes sibling registrations; reference owner-grouping accommodates contradictory original listener test.

- Parent canonical: `27f80e5b3c491d542f41cebaf0d3b8c72fed443b8ee3f753e153c8cde4fae8e1`
- Prompt: `2615b3aad94195c05b55dc8ef02d36f7a2535d2377781b2de0ba6ab2d8229eb0`
- Reference: `a0a60c6976b1636d74d96672aed75f5585cba4e71aa7a7b43772599119061138`
- Original test: solution.test.ts `42bd77528eeffe3df8268ec0393fbc3f15f697600bbd63b1f557b6911b8cf0f5`
- Source object canonical: `2c1733be3571026c8f92c0fe8fee386381228234f7bf029455f60572946066db`; source record: `17bdb274dfe14eb642def96744e12dbcb7971e849cedabe3ce2cf52a04914c16`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-33391, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `80534e4f00602ebbcc51c4dcafbbc76b2347155c3106c69a198ca9b31c016499`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/drawer-subscription-result.json; file SHA256 `e35c96eb8202b225202bd2790e3b9a331fc49f70bf679711c5af31e609e99b4f`; diagnostic test SHA256 `69671e1d7aa66c159cdd039ec7d8657c2fa4637424a7a8bbd66f068345f318b6`; archived exit codes [0,0,1].

### 14. exp-v1-typescript-repair-0190

Change class: **oracle-rebuild**. Substantive target: Recursive deep merge, overwrite precedence, enumerable symbol/string keys and nested ownership.

Minimum correction and decisive witness: mergePreferences([JSON.parse('{"__proto__":{"kept":true}}')]) must retain an own __proto__ data key and independently cloned nested object. Use safe own-property writes and avoid consulting inherited result properties as prior merge values; preserve recursive record merge and arrays-as-replacements.

Independent-test requirements and contract limits: Contract explicitly preserves enumerable own string/symbol keys and ignores inherited/non-enumerable properties. Test two sources merging nested __proto__ records, primitive/undefined override, symbols, arrays inside arrays and bidirectional independence. Do not broaden nonplain-object or cyclic domains; no new arbitrary-extra-field rule.

Realistic new mutant: Restore assignment through inherited __proto__ setter, keeping deep array copying correct.

Historical hold: Own enumerable __proto__ key lost during deep merge.

- Parent canonical: `3af1da2539951774d0e5a64a8b0d1499b765b6b823c0bc3c59a7f2bd8c8e9179`
- Prompt: `e5f845453d03a808670df618e4bc553864c5d5bd04d4758e5f3fc99698c234ad`
- Reference: `505b08dd4a34b16e4361e953bd662aceedb2471fb73df0a3db91a14d840783c7`
- Original test: solution.test.ts `47a7e3c9df495df6114127ebb76b7916ab43e6dfac1b798a7a69604b11e2120a`
- Source object canonical: `51fc95263918df12bfa0dbb98693a5f152550c18fb721dc8d7bb435f93c2c5ff`; source record: `eb627c743dc8089df585abb47bea11abde5cb3819513d9edd2377ce2590b7e26`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-33467, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `9a6a03deb48e3586b924fe22ce29de49433463ebad76744f37b875fd0d9bff84`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/merged-preferences-proto-key-result.json; file SHA256 `7c5baf71ea824c882d1ac31c0f49fdc21bc6ab101e896857db549aef0f2afabe`; diagnostic test SHA256 `90a270fa245569732df9ad19806f897681ca983f4ab19a23d0d871e9c81f7ebf`; archived exit codes [0,0,1].

### 15. exp-v1-typescript-repair-0158

Change class: **oracle-rebuild**. Substantive target: Feature validation before fallback selection and translated-key resolution.

Minimum correction and decisive witness: resolvePanel([{id:'x',titleKey:'toString',detailKey:'d',altKey:'a'}],undefined,{}) must return title 'toString', not inherited Object.prototype function. Resolve usable string translations; inherited non-string built-ins are absent translations.

Independent-test requirements and contract limits: Do not ban inherited valid string translations without a contract rule: preserve them if available as strings. Test explicit own toString string, empty-string translation, constructor key, absent/unknown selected ID falling back to first, selected feature, whole feature validation, duplicates and fresh output. No new exact error messages beyond existing API.

Realistic new mutant: Restore unchecked dictionary lookup fallback, retaining unknown-selection fix.

Historical hold: Inherited method returned instead of missing-message key fallback.

- Parent canonical: `9b773881d015a560ed807faf980b227bd0cefa2b3c62c8a3bfc99a6220bb51cb`
- Prompt: `0eeac3f25c460cac281a14380417e92c4e83bc12f71e9209803b4169c9926bd7`
- Reference: `e70de3b0f77674960e60badcf6ac4223c220f16c266b9777f801113a3c86e6a8`
- Original test: solution.test.ts `d0ddf813810f2cd22df57892dcd60bb72ac04d3f549f22816aed28a9003926b1`
- Source object canonical: `5846316621b62d4e72f2716663abffd44dd58ff0f6cf2b9b1962db31125b3410`; source record: `394aa58aecdb3da5e23cb6421f5db58c3edec8edb2914e2f382619e5b09712d3`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-32837, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `3c8c04b467672686d4303090ce52dd82c264835af81e24258eacefd32daf9fb8`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/panel-inherited-translation-result.json; file SHA256 `9e552652ee51af660d2d54776016e0ced7cd83e98cc8400f5bda4324fbbdb93a`; diagnostic test SHA256 `e6fceb501aa3ea728b87938c6784d8cf33861d69928975ab712716fa87463042`; archived exit codes [0,0,1].

### 16. exp-v1-typescript-repair-0030

Change class: **oracle-rebuild**. Substantive target: Cyclic graph traversal, root exclusion and deterministic depth-first discovery.

Minimum correction and decisive witness: collectDependencies({},['constructor']) must return []; {root:['constructor']} with roots['root'] returns ['constructor'] as a leaf, not throw on inherited function. Use a dependency-array-aware lookup so absent built-in property names behave as leaves.

Independent-test requirements and contract limits: Retain real supplied array entries (including valid inherited arrays if accessible under existing source domain), input-order DFS, duplicates, cycles, empty-string root and root dependencies. Test own constructor array as a positive control. No new global graph-shape validation or depth/resource promise.

Realistic new mutant: Restore unguarded property lookup with transitive DFS otherwise corrected.

Historical hold: Absent graph root constructor resolves inherited function and throws TypeError instead of behaving as a leaf.

- Parent canonical: `1507fddcff8bd1ddd40dc51bc5b592e1b455a42bc179b2567a7750c642429920`
- Prompt: `fb4f5170b80f729b547f08fee6c14b6e13451114314a4e0530d265731dc7ae78`
- Reference: `436f1affce75bb3feb8b05c84276d2766a8196292b6d95c6df1add70aafda1f2`
- Original test: solution.test.ts `b22c1e1c2f6883af108cd10d61811d4a2ac8d78700a6ba896ca8c7a27c3fd0f3`
- Source object canonical: `abd52cbe262f3536e31dee7b0fd9e2a240a83aa8c6c068f7f2aab6b9df139232`; source record: `bc2dc0700653b32df5fa9cd629ee07350e648b10dac5335e471c3a0ed419e502`
- Source: m-a-p/MdEval-Instruct, revision `38c9197e3add996fae624eb198ebd06155b2101e`, row-02537, license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `1e99928e9a078f702463ab95419616e00323b9d1fbc9bd93e32d3720c211f71b`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/residual-dependencies-0030-result.json; file SHA256 `109873e8f59fb08da308c16d45a13dbed75cfc203c46964636a2ceee39532970`; diagnostic test SHA256 `0de4b622315b2372612d6c819596676f05145fedd1e394475e277239e2c6b635`; archived exit codes [0,0,1].

### 17. exp-v1-typescript-generation-0368

Change class: **reference-fix**. Substantive target: Cross-field normalization, Gregorian dates and ordered unique validation errors.

Minimum correction and decisive witness: Valid nonblank draft closing0099-01-01 with earliest0099-01-01 must succeed. Correct date validation without Date.UTC's 0..99 remapping, preserving exact four-digit syntax and real calendar checks.

Independent-test requirements and contract limits: Test early positive years0096 leap/0099 common, modern1900/2000 century controls, bad day/month, equal/preceding dates, invalid earliest reported last, email exact-one-@ and online venue normalization. Do not invent exact error strings: compare consistent per-field identities/order. Do not enlarge into an unresolved year-zero policy or new email grammar.

Realistic new mutant: Restore Date.UTC year remapping for early years while unrelated validation stays correct.

Historical hold: Valid Gregorian year 0099 rejected through Date.UTC year remapping.

- Parent canonical: `43e7ee667f90b4114ca95e22c9285b47ef45665412de87fd76c7f23fc762b9a0`
- Prompt: `23910463ceac6581da65a37806a63b1120762f6429793c3384a83cd6c003c4c3`
- Reference: `2163414e32cce1677952064fe35c40474f02364920e82a3253ca5ad63baf23dc`
- Original test: solution.test.ts `e1eda4d9dd69fc4baa816887ac1b0de53226eba8826cf1a612821e411024cd46`
- Source object canonical: `a3177420adcee444654e962be1d2427367c8853580616ac41472bb334ac9c6b7`; source record: `8cc7bc1f483937bc4a3c629ab2a27146064eff63ce575e798cf399a4f1b63751`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-33254, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `b29614069f1b0bbea2442d2d0ac1f4f3add9f29ecd395a1e2fbaaa0632b61292`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/workshop-early-year-result.json; file SHA256 `6e0517b692c7351625612ef7730320d99e824c5f7a73a79cb30480972ca2be3c`; diagnostic test SHA256 `f0470f2e903c13f05be3f857c4dc0edeee6b60890454012cd4b3e43c76ca9264`; archived exit codes [0,0,1].

### 18. exp-v1-typescript-repair-0063

Change class: **oracle-rebuild**. Substantive target: Kind-isolated snapshot storage, cycle detection, stable replacement order and deep copy.

Minimum correction and decisive witness: WorkspaceStore put/get of JSON.parse('{"__proto__":1}') must retain own key/value. put of new Array<Snapshot>(1) must throw TypeError. Fix safe own key creation and full indexed array validation in the shared clone path; both held defects must be repaired.

Independent-test requirements and contract limits: Retain original plain-object prototype policy (null-prototype input rejected by supplied source), fixed typed kinds, ID normalization/error asymmetry, primitive validation, cycle rejection, repeated acyclic sharing allowed, insertion/replacement order and fresh nested copies. Test malformed replacement preserves prior record/order; nested proto keys and sparse arrays; get twice independent. No extra symbol-key/descriptor or unbounded-depth policy.

Realistic new mutant: Restore unsafe __proto__ assignment only with sparse validation and original get-copy correction retained.

Historical hold: JSON-like snapshot cloning loses valid __proto__ object key and accepts undefined sparse slots.

- Parent canonical: `0c8ed1c572c9f30b9d708b9d0aff4765d86a6c778f691e09eb2d13d528fa89c5`
- Prompt: `e94bf578530cecbcdc8578c31aa66db06ae75ea940ec6e567294de8d9647f9ec`
- Reference: `c924f72217c95a5c6805f9cd93016eae14110ec7392f58b8b81f34e9acba0052`
- Original test: solution.test.ts `b91d5d6caad8782743b256b61965ef5ab71a22074608fea5333025e8d747d7d3`
- Source object canonical: `c16ce37d9a399d134a6eb3bc9b9581e3f7c95650f1b6cfbf2ae447413c00c348`; source record: `98ccd131f49c74bc70ae6088bb5396b50cb0d71ef59b6dcb69ebe4690f7466c5`
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-32777, license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct
- Rights object canonical: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`; prompt/answer/tests/model_training/redistribution all true in original record.
- Exact hold object canonical: `37d27cb0840d629cf673cc45cc84b9dfa2addeac4076864d267e7d990074ae17`
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/workspace-proto-key-result.json; file SHA256 `d1eed3932d75d0e277df91a2baad0681216e8525060f6bcc27811ddb07abd938`; diagnostic test SHA256 `28105bd47832ed888a84fa92035493f832422465d5eeb4bba2df67f56103492c`; archived exit codes [0,0,1].
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/workspace-sparse-result.json; file SHA256 `658beaae404f90fea261e5fd7f36713f9f1fa93f43cfae4ba7d0e1a622228d3b`; diagnostic test SHA256 `b2e1070d19313079c3f5e6152ad84b4180eac0e0d5b13e8b4d7528e740699e9a`; archived exit codes [0,0,1].

## Explicit deferrals from inspected alternatives

- JSgeneration0076: reentrant notification can reuse IDs, but nested-success/outer-failure rollback precedence needs a separate contract decision; excluded from this narrow tranche.
- TSgeneration0383: sibling unsubscription defect is concrete, but numeric cycle generation has a broader precision/resource domain and choice strings also narrow nonempty to nonblank. Do not select a partial listener-only fix.
- TSgeneration0352: modular arithmetic defect is concrete, but listWelcomes greeting semantics for middle names need separate contract reconciliation; not selected here.
- TSgeneration0026: repository/result interfaces are not fully specified by the generation prompt, and broad copying wording needs more than a sparse-tag-only patch.
- JSgeneration0098, JSrepair0077 and TSrepair0227: conservatively deferred for this accelerated tranche; grouping/projection/credential-filter targets are weaker nontriviality choices than the coupled state/graph/parser targets selected. No new holds or claim that these are unrecoverable.
- JSgeneration0005 was initially screened, but its broad whole-record alias wording and spread copying need additional domain reconciliation; not proposed and not claimed as a complete quality adjudication.

The eighteen positive selection decisions above are provisional and bounded. No automatic follow-on retry loop is proposed.

## Exclusion snapshot

Exact raw plan file hashes used for r1–r23 exclusion (some version directories contain only retry subsets; deduplicate by original parent ID):

- datasets/cache/expansion-v1/versioned-recovery/r1/plan.json: `a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1`
- datasets/cache/expansion-v1/versioned-recovery/r2/plan.json: `5dae7eac34ac462f6173dc6b740364d5c4b68129950359f453f4038111ad1d29`
- datasets/cache/expansion-v1/versioned-recovery/r3/plan.json: `cbad9d14a504531e749b5eb3433f0bf4670e21f2a8e8d5f310d2e843e53c6231`
- datasets/cache/expansion-v1/versioned-recovery/r4/plan.json: `8a6137773e65e1a55e5eaceed9a8c2e40153b5759a46a5189ba6a488d530d58c`
- datasets/cache/expansion-v1/versioned-recovery/r5/plan.json: `778e0071bec56248081e741f4c742d522c75b4b006e069d8301b75440c2732ec`
- datasets/cache/expansion-v1/versioned-recovery/r6/plan.json: `803f0308b33b4b8a834347d5976a148bc66001d6fc8606a1e206fb0e2b4a6795`
- datasets/cache/expansion-v1/versioned-recovery/r7/plan.json: `f0a3b5d14eb983206ac83c99571c5522925feaf7ac0443ec3c59ad172d5f293e`
- datasets/cache/expansion-v1/versioned-recovery/r8/plan.json: `1a579af9da9d542d6bb4f03c8fbc030fd0b9d3102a31c347cd631bfc18b873de`
- datasets/cache/expansion-v1/versioned-recovery/r9/plan.json: `0f0d6e653bbabff308a912cc764d1373b20faf3f4cf68a4c7341c94f36b5ae79`
- datasets/cache/expansion-v1/versioned-recovery/r10/plan.json: `728e70ee23ad46f8a4a8aec64a34d74b48c073a5382849fc52ce449154f2afb5`
- datasets/cache/expansion-v1/versioned-recovery/r11/plan.json: `2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6`
- datasets/cache/expansion-v1/versioned-recovery/r12/plan.json: `0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121`
- datasets/cache/expansion-v1/versioned-recovery/r13/plan.json: `dead1489bb779934327bf3c8786d89c65b7604832829fa17129ea41ff1773217`
- datasets/cache/expansion-v1/versioned-recovery/r14/plan.json: `2d59789fea811ba7ebe844564ee4dc66569fe4719067dea6d6a1524b049ea51f`
- datasets/cache/expansion-v1/versioned-recovery/r15/plan.json: `d2e65ef33e2c70162a53315e3daec75ebe1e3fbc1a7098e8635eddacb348c100`
- datasets/cache/expansion-v1/versioned-recovery/r16/plan.json: `efd902abc4ed3e00d6639c74f7d2ec95e6f153d1aa19a70a460aeb553dfb6844`
- datasets/cache/expansion-v1/versioned-recovery/r17/plan.json: `60c02db8869c80c1515e2216205ac11a45b357206563f62f499d8b67b3ee02ee`
- datasets/cache/expansion-v1/versioned-recovery/r18/plan.json: `512e3219da55465742728f2c5116840498e4a41c5a2bfe8f5b0130d9a19690a0`
- datasets/cache/expansion-v1/versioned-recovery/r19/plan.json: `401d56a11f2ca2929eb42be7ffb36fe694cfded2500ed56a96759560b8b65f62`
- datasets/cache/expansion-v1/versioned-recovery/r20/plan.json: `879eb4184b49e09a171cbe35592096a296d9d2af6e1e52eea68315fb6b7eb224`
- datasets/cache/expansion-v1/versioned-recovery/r21/plan.json: `a5fe5bbb1cffe149091f626ed317a0e79c39985c10c883acd8f83df3c04582ca`
- datasets/cache/expansion-v1/versioned-recovery/r22/plan.json: `34b141407c111f6df7999027d57540860ccb3b47c0d10c2c5ce8ba105f8facc0`
- datasets/cache/expansion-v1/versioned-recovery/r23/plan.json: `d44918671d7a9350cc90e67ac7eede1ee4ab61e6ce6bae2f1eadaccbed367d92`
