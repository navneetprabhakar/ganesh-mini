# R24 JavaScript independent static quality review — 2026-09-08

Gate 2; static review only. Exactly nine derived JavaScript candidates were reviewed against the complete R24 plan and run contract, exact original parents and hold evidence, the batch-3 selection boundary, architect evidence, independent-test evidence, and every derived prompt, reference, known-bad implementation and test file. No generated code was executed, no candidate was changed, no admission was made, and no cloud resource was used.

## Decision

**Zero unconditional positives; nine holds.** Both generation candidates have test-quality defects. All seven repair candidates have an approved prompt-scope/binding hold because their surrounding behavioral prose changed despite the explicit instruction to replace only the embedded complete source and, if necessary, neutralize stale nonbehavioral diagnosis. This is the same fail-closed boundary recorded for R22; substantive correctness does not waive it.

| Candidate suffix | Reference quality | Test quality | Approved prompt scope | Overall |
| --- | --- | --- | --- | --- |
| generation-0120 | Hold: reference and suite disagree on extra criteria fields | Hold: unsupported extra-field rejection | Preserved exactly | Hold |
| generation-0292 | Positive | Hold: defining boxed/coercible-command witness absent | Preserved exactly | Hold |
| repair-0003 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0015 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0043 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0048 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0051 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0132 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0240 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |

These are artifact-level holds, not claims that the underlying targets are unrecoverable. None of the nine may be counted as admitted from this report.

## Binding discrepancy — all seven repairs

The controlling selection says every repair is `oracle-rebuild`: preserve all behavioral prose/API/domain/error/ownership rules, replace **only** the complete embedded source with the exact returned mutant, and update stale nonbehavioral diagnosis only if necessary. Removing the fenced source from original and derived prompts leaves unequal prose for all seven repairs. The differences are not limited to stale diagnosis:

- **0003:** adds whole-manifest validation before empty request, explicit every-index/sparse requested validation, non-enumerable named-field preservation, and an arbitrary-extra-field boundary.
- **0015:** adds every-index/sparse validation, whole-graph-before-traversal timing, and explicit prototype/own-property limits.
- **0043:** adds own-*string*-key and non-enumerable/symbol membership semantics, safe own-data-property creation, and output descriptor/prototype limits.
- **0048:** adds every-index/sparse semantics, native-promise rejection delivery, and explicit `false`/`0`/`null` handling; it also removes the prior diagnosis.
- **0051:** adds every-index/sparse and validation-before-effects semantics, same-error identity, native-promise rejection delivery, and caller-mutation limits; it removes the `Known-bad source:` label.
- **0132:** adds dense/every-index/sparse semantics and narrows the whitespace wording with “only”; it removes the `Known-bad source:` label.
- **0240:** adds every-index/sparse construction semantics, `undefined` handler, construction-time timing, descriptor snapshot mutation behavior, and handler-reference reuse.

These additions generally agree with the selection rationale and the derived reference, but agreement is not authorization to rewrite the frozen repair task. A new explicitly authorized contract-clarification version, or a source-only regeneration that can express the witness under the original prose, is required. A test-only retry cannot repair the prompt binding.

## Per-candidate review

### generation-0120 — reference/test-oracle hold

The unchanged generation prompt and selection rationale explicitly avoid a new extra-field policy for `criteria`. The submitted tests nevertheless require `selectCandidates([], { extra: true })` to throw `TypeError`. The derived reference ignores that field, so the reference and its own suite are statically inconsistent. This is not a subtle runtime question: that final assertion reaches no other validation and the reference returns `[]`.

The indexed loops correctly address sparse candidates and nested sparse skills; normalization, score bounds, duplicate classification, stable sorting and detached results are otherwise coherent. The sparse candidate/skills/required-skills witnesses meaningfully distinguish the intended defect. Remove the unsupported extra-field assertion; do not replace it with an inherited-option or exact-key policy. Fresh sandbox directionality is still required after any correction.

### generation-0292 — missing defining witness

The reference correctly requires a primitive string command before dictionary lookup, and otherwise retains whole-grid validation, bounded movement, plain-position validation and detached results. The mutant removes only that primitive-type guard and realistically accepts values that coerce to `N`, `S`, `E` or `W`.

The independent suite tests primitive valid commands, lowercase and empty strings, but never supplies `new String('N')` or another coercible non-string object. Therefore the exact held defect is not exercised and the known-bad is expected to survive the submitted suite. Add the approved boxed-string and coercible-object rejection witnesses without introducing safe-integer position bounds or additional position fields. No reference change is indicated.

### repair-0003 — substantive positive conditional on prompt binding

The indexed requested loop rejects absent slots, while whole-manifest validation, requested ordering, duplicate/missing classification and fresh named-field reconstruction remain coherent. Tests cover sparse manifest/request arrays, hidden named fields, bounds, duplicate/missing slugs, late invalid manifest data and input/result independence. The mutant realistically restores `requested.map` hole skipping. No additional reference or test defect was found; the artifact remains held solely because the rewritten prose exceeds source-only scope.

### repair-0015 — substantive positive conditional on prompt binding

The reference validates every imports and entries index before graph traversal, then performs cycle-safe dependency and side-effect reachability with lexical output. Tests include an unreachable module with sparse imports, sparse entries, missing imports, cycles, side-effect roots and inherited graph properties. The mutant realistically restores `some`-based hole skipping. No additional reference or test defect was found; the artifact remains held by prompt scope.

### repair-0043 — substantive positive conditional on prompt binding

The reference enumerates own string keys with `Object.getOwnPropertyNames`, validates order membership, safely defines `__proto__` as an own data property, preserves payload references and LRU ordering, and handles capacity zero. Tests cover the proto key, non-enumerable keys, ignored symbols, retouch/add/eviction, malformed membership, sparse order and ownership. The mutant realistically restores unsafe ordinary-object assignment. No additional reference or test defect was found; the artifact remains held by prompt scope.

### repair-0048 — substantive positive conditional on prompt binding

The indexed preflight validates every handler before effects. The async API returns a native promise, awaits sequentially, treats all non-`undefined` values as handled, and propagates the same thrown/rejected error while stopping later handlers. Tests include sparse and later-invalid atomicity, an explicit await gate, falsy handled values, error identity and nonmutation. The mutant realistically restores sparse-skipping `some`. No additional reference or test defect was found; the artifact remains held by prompt scope.

### repair-0051 — substantive positive conditional on prompt binding

The indexed preflight rejects sparse/non-function steps before effects, then awaits values, promises and thenables sequentially. Tests cover the original-seed empty case, an explicit ordering gate, sparse and later-invalid atomicity, same-error propagation and nonmutation. The mutant realistically restores `some` hole skipping. No additional reference or test defect was found; the artifact remains held by prompt scope.

### repair-0132 — substantive positive conditional on prompt binding

The indexed preflight rejects sparse cells before the unchanged formula-neutralization and CSV-escaping pipeline. Tests cover all four formula prefixes, the exact ASCII whitespace set, quotes/commas/CR/LF, a harmless vertical tab, leading apostrophe, empty values, partial sparsity and nonmutation. The mutant realistically restores `every` hole skipping. No additional reference or test defect was found; the artifact remains held by prompt scope.

### repair-0240 — substantive positive conditional on prompt binding

The indexed construction loop rejects sparse route slots and snapshots named descriptor fields. Resolution preserves exact-over-wildcard precedence and first-match stability. Tests cover sparse input, own hidden `undefined` handler, inherited-handler rejection, descriptor mutation, falsy handler, malformed lookup and empty/no-match behavior. The mutant realistically restores `map` hole skipping. No additional reference or test defect was found; the artifact remains held by prompt scope.

## Seven-criterion assessment

1. **Prompt clarity:** generation prompts are byte-identical to their parents. The seven repair prompts are individually understandable but violate their narrower approved edit operation. Generation-0120's “exactly usable fields” wording does not authorize the suite's blanket extra-field rejection under the explicit selection boundary.
2. **API consistency:** CommonJS exports, sync/async delivery, method signatures, return values and documented error classes are coherent except the generation-0120 reference/test disagreement. No private representation assertion was used.
3. **Independent tests:** the independent author call returned zero, did not time out, reported no tool events or parse error, and its exact `test_code` for every ID equals the candidate test. The author received IDs and complete derived specifications only. For repairs, those specifications necessarily contained the embedded broken source; this is specification-origin independence, not blindness to that source.
4. **Non-triviality:** all nine targets combine multiple interacting concerns—validation with filtering/order/ownership, whole-graph traversal, async atomicity, LRU identity/eviction, CSV transformation order, or routing precedence. None is being held for patch size.
5. **Idiomatic reference:** indexed loops are the appropriate sparse-slot guard; Map/Set, async/await, own-property APIs and `Object.defineProperty` are standard JavaScript. Generation-0120's suite inconsistency and the repair binding issue prevent unconditional positives, not general code style.
6. **Dependency isolation:** all tasks use JavaScript/CommonJS and Node built-ins only, with no network, external package, filesystem or service dependency. No generated code was executed here.
7. **Realistic known-bad:** all mutants are narrow and semantic. Generation-0292 lacks a test that rejects its mutant; generation-0120's intended sparse mutant is exercised but the suite independently invalidates the reference. The seven repair mutants have meaningful witnesses, conditional on prompt-scope resolution.

## Immutability, provenance and evidence

All nine plan parent hashes equal canonical JSON hashes of the exact originals in `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`. Candidate rights equal parent and plan rights; all five booleans are true. Candidate source fields equal the exact parent fields except the explicit versioned-recovery transformation. Generation prompts equal parent prompts byte-for-byte. Candidate user/assistant messages equal their verification prompt/reference, and rendered prompts equal prompts. Architect output exactly supplies every derived problem/reference/mutant; independent output exactly supplies every test.

The two generation records retain McEval-Instruct CC-BY-SA-4.0 revision `57bd46727e49ac3e2890218a146d35c2454a8496`; the seven repairs retain MdEval-Instruct MIT revision `38c9197e3add996fae624eb198ebd06155b2101e`. This verifies lineage, not a new rights determination.

Shared bindings:

- Parent corpus SHA256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
- Hold ledger SHA256: `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.
- R24 plan raw file SHA256: `1f89608807b00559e993952c6d0a1936baccae882322c3315ae7efe3dd37d9fb`; declared plan SHA256: `d2816d2eaf52f5c8427808ec807f04439218bb6a502eb95f4bcee5df970d71bc`; request SHA256: `2e881ce718f8509655f0a894daddc305c869bc787deb6672a9b68d6e0d416451`.
- Run contract raw SHA256: `a455daccb7e85a30c3cc86d4c328ee44be8e6fd166afef6fe685bba9c8225be4`.
- Architect evidence raw SHA256: `16f04e54d75522ccba47610924fec3d9f32a16ad0410b410c1cb6c02dade248d`.
- Independent-test evidence raw SHA256: `69730c0257e77af4235cb708d1844fa106c4613549986a177ceb3b0fae140d2a`.
- Batch-3 selection report raw SHA256: `f5e59348f4d1a986c144629f43153e39d08492380d7066fa2d3a9fe8d0bab139`.

### Candidate content bindings

Hashes are raw file bytes or canonical JSON as labeled; prompt/reference/test/mutant hashes are raw UTF-8 content.

| Candidate | File | Canonical JSON | Prompt | Reference | Test | Mutant |
| --- | --- | --- | --- | --- | --- | --- |
| generation-0120 | `056f72ec8d73ad1dce775bcecaa9f19b7017d622dad32ca4a44b81b9ae3c4600` | `1a11364fe49009462761f69820a97111a5380354cad9b3868bedfb0670ccafe1` | `fbd7759157b096cf29a3e26792567a8740c488379f1d8f137550ced6378fd1a5` | `1ae983a81af46f2404706e50b55fb70a673b425611284c97b32241702fbe4dcd` | `b643505914313e83d0a427484f14fb2714ae081331612e6b9ff0cedc16ed51eb` | `d16e2693faa0cf08dc8f4f5baa99cb99160b5b5e9aaa830a1c382ca16f4793c6` |
| generation-0292 | `2e2ca85db5c85b7dc17d976940ab3c10c3612c41245d89e1e976d9e2b95f3bac` | `3d02098306ea9ce9854d70862e2cccebd989ee92ba44962ba57ee2009f194139` | `f52acc2ad2f434986b92081c1d3d94e9c94554346dd78acaa25d09a6bec7a88e` | `0428490cf58a6a878d428fdc343feea17d73f1954d6300ee3d0c258a62a4f4d7` | `a6847ea9a47bf38dd0897fe8b65675b25460d9e357ed410bd449e9fd627a9de1` | `818716c419f90dd5044d507fd786b86cbb04c8eb6f6aa381c949af3570166194` |
| repair-0003 | `b14d2a7f63776a63da031a5bbf6b2d5eef5ed79381f1a25900a0d04e31294d45` | `7cd3eba88f6684833954be4ec258834c0a82649726cb12658386cf84abfb97c2` | `c5854561d94e82af057b4b224ee6f92c0d076a0c430e827437f940a29bc95d68` | `a79ee2d2a9bf6ec5a19d981f1487a6846f44ccb4c40b419b17b75ee961ac24ee` | `d6101a3c09f0d2366d01d8638c5f4bfd3c1dcda9c05225cc2ba661ff65aa56cf` | `9a2d2300679829c07e4a21ba60f67a087e214bb55514ab2ea3aa1785cd3ebe55` |
| repair-0015 | `0c85eadffd1e68d3ef3a0c727f9adaac2f0da11eab8ef80b81d64497bcf0203d` | `f0914130a6b612bdccbecf7542a137e6a6a1676b24c7c66db28637b2a56e26ec` | `dd176b4e5484ea4ae34e711783c393936b64da6e697f0177ce85afb9dbf91a83` | `49ddb4bdc167e4ae396f82f1e016260243c8e842ea34689943f059da710c762b` | `33581c9ba773d32120bc6728d86e767da2ee73ab31a45dce7f17c07e36213507` | `8dcda3e943ba59456d200177690d36e5d059916b0ce7f4b3f4f31f1bdc54f2a4` |
| repair-0043 | `11dad4fd05edc6797168a5a6846324f3a32e09616609ce250e312c4ff5fde682` | `170f01ae7e20b1e60d535860d36076413315a4c6e0e34f394e2e2c58644f1aa5` | `f007b1e824ad9b185262d95ba86fb98bd250858bf2643beed5434e09c1e5fef5` | `e8b1893afb638a6fb7906376c7bb7926af28ef3c614efbff9e3c45cc52d2d079` | `f8178f3456a13f01e0243bf6980c0dcb942711796a6a18bb3d2d691480e7602b` | `1b99a8ad23fdef66ffa49387a7937e191bca73b7ceff48250ff03d3b27b381af` |
| repair-0048 | `57fe9864ca8839b346de0704fee7e976796402781cbfac3a1539f89ec67cdcf1` | `6462c531985992ac8115fefe222c9d24c3e9ff7baf3cef1cae4a7dd91490898b` | `8e3f6f391a4caf527933e68494a86d5ee126fde41eb065b8f5d5b0bbfa7be8b3` | `3aac3b5335da391672f1c6e39b8bdca891b693e320652049dcbaaadf74de7cf2` | `c3d907ca8eece30be6d3a9f48eae672cca30e71b0b9866bbf52b6038db766ef1` | `fece1b918f7f8e3abd733f311763eab8f629acb01052b7131b000bb652295d79` |
| repair-0051 | `ea67c9940c9fffa036fa0a28b7b77b927e515a679177f3cb3136ebef8b7ea75b` | `fff58b51cce45415d868ab1e2c1f46622caefb377564993a0bdab148d5baa49f` | `ca0f7ab70db3004bee7c1c99f141131abbaedd19c0306331b165082b165ea69f` | `60c8207a7cc9fa1dba6eae1809a973046080a9d0a783bfb182963d53b3938f24` | `0d80a430a960f46e85c6cbf2b79f85c5c42f4a4493a2fcc748f3e66e5ef30342` | `a347c81786d0a072a047c3a0786d0c2d1e6b0afc9ae0fc79c0e9ed4378f86d48` |
| repair-0132 | `6174616aa6a9e3daf34e42d70add2abb7edc088bdb6c09fa75f032e80a2b0dcd` | `45a10fa68ec17874bd99563f9179d8c73fea81fbee4131e339112d2fbea24d61` | `d74e9dabb08104cabf53f9c5ed135ef47f109b2b0c6a031a47e9ff07576cef6e` | `3bb67045efae6c66ec158331c35b5418d20d730d693c30a2cd4c3aca3853a041` | `2fee043bd7950648eb375d0e8354bc1ee439ad70de26ab56195248c5a4c01bb9` | `4ce7eddb034e44e970e8c5dee14feefd5e08bc4220244c20753c17b176167de8` |
| repair-0240 | `8ab617dc6953f68bb20b5f5e1e043d8586b5ca72e3ee6964841418684eee97b3` | `46599b38ab9c74013e9a4c484953bd3849c066ad3b36c8cc066f23a42a5d4a72` | `958b6379a2678d809bc4cb338341674502f494c33be5b53430b42af5a1f92eb5` | `fc5505962d3fb2314f938fbaa44406c641130aa77d97559a492dd216e98b2455` | `911a56257b58c0bd935424340e52642a42a8d195f637b4141ed4821577d1f5d3` | `06995474e0bc96a7f2940e2d2b684295afc2d346ed17c58fabc6d30f30342073` |

### Parent and hold bindings

| Candidate | Parent canonical JSON | Hold evidence file SHA256 | Source record |
| --- | --- | --- | --- |
| generation-0120 | `264d5b2a8d304128c06308afed6d8de3be2250ba7690f4531cac83f4b238705d` | candidates-sparse-result.json `09174d481b2a55c4d3159eb7c87fa9c56d7c198a585349c794bf77db80b00cc5` | row-06678 `69c6cfffad19490be61a88c476d533da295ec04d364fe78a0011f976745c23a3` |
| generation-0292 | `62963b6c604808fa36f01def4b09190c5fbab0f997d2a191face5321f477bc38` | robot-command-type-result.json `2613728e58ad543a404048e38677c5c9532e1262808a6130ab8bb87aaaeb08e5` | row-26721 `ccefb7d9983b1c6a9c0ff788151ed0f947772372e767b324f5dc87474ffa2320` |
| repair-0003 | `add930de98c1fa45c4b693faeefdbbb7862eef5b110f3532a548c668c2c391e4` | build-pages-sparse-result.json `8203e6d66f4ccf9e81a43ee7074d3b939b5e578cefb70cbcce4235b051c80bde` | row-06064 `487febb53bff29e747d438fae3d8688ecb1f956cc5194ae150f75a5cef571c33` |
| repair-0015 | `71df1c6b0aca82937922d83679fa3c7826e9a44610a5d83a28d1db08a31b45a9` | module-unused-sparse-result.json `c6e7b2860be8bd42522015b14b0165b9d231ec80dd1b2979b055fe548941eb73` | row-14196 `d60d443cecaee2fef8b62a983d03989c6276f5b5ca9bb472b602c9366583173d` |
| repair-0043 | `3822324e93b766c419edd046ca664a44c8278c202ef4621f250c709c5e6b45a1` | cache-proto-key-result.json `ad7ba7aa688066f207426e4b5dc2066e1b6db4faa2c8e184fa19407c81f58972` | row-07988 `6234809bced4c502d0467a8e4728f106d94d0f6c52fc9c39343ebc3431ee0243` |
| repair-0048 | `f5544deae2ef298ee0543374315fba07322d8144baaac5d641e7128b9fb7ec60` | dispatch-sparse-atomic-result.json `afae89f0f87678cb1f7cc9456aae2e9d183a85b8262f0271fbba88cf87819f4e` | row-09237 `dec4f717ab2f2b7980192118ea0ae48ed8018014770c87a36f774ead95a42391` |
| repair-0051 | `5ecf48de78e5bdc267bf7f0ff3de2b164614291491a1de990752d9360c833406` | pipeline-sparse-atomic-result.json `145add563b56b702debe566365c8561d6ead11462181bca7efcbf53040b6d13f` | row-03174 `d41f8a55afb2015b36bbfdcc688b148ca7bcbfacb489d51f81aced3a622fc120` |
| repair-0132 | `465586f80d03674e2729e059ebc486a4ed5713cb636e84bbba9dbd26c11aa34f` | csv-sparse-result.json `6877afe79da531543f95540112f34348e719844c976d283b048a4f0609713c41` | row-02750 `624685d8208b0057afa1bdff2293f40d6b6cdce44373368ce4c40dae2891436f` |
| repair-0240 | `844f40ede452ad2f8dcb1bdc1b60dbfd655c431a38bfdbde5e2e5411ab45e47f` | routes-sparse-result.json `6fcbbc166aa551fbba87fc38527721f0563136fa749db2debf759d07f070921a` | row-03266 `f6a023ce95c1f33f82aa797745aa97cb2586e6d6be28f666d7d9515ef05b3797` |

Main should preserve these exact artifacts and holds, reconcile the scope failure centrally, and avoid representing any of the nine as a seven-criterion positive or admission.
