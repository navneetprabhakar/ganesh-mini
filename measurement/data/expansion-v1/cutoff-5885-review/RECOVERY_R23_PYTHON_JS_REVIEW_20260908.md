# R23 Python and JavaScript terminal quality review — 2026-09-08

Gate 2. Exactly seven terminal test-only corrections reviewed: Python0017/0063/0156/0781 and JavaScript0034/0061/0119. **Seven static quality positives; zero newly identified quality holds.** No candidate execution, generation, admission, GCloud, central edits or further retry. One correction has been consumed; this report does not request another. Original coverage is unchanged.

Complete derived specifications, references, corrected tests and mutants were read, and reconciled with full prior R21 reviews and the exact main-approved R23 feedback/request. Prior test-quality holds are closed for these exact derived artifacts on static evidence. Runtime qualification remains main's separate sandbox work, not an executed claim in this report.

## Immutability and independent origin

For all seven, R23 problem, rendered problem, reference code, known-bad validation objects and user/assistant messages are byte-for-byte equal to R21. Only tests and expected versioned identity/lineage metadata change. The approved feedback previous_candidate_sha256 equals the canonical R21 artifact. Source fields except explicit versioned transformation and all rights booleans equal R21 and original parents.

Each correction author input has exactly id/problem/test_code, with problem equal to the frozen R21 problem and test_code equal to the complete R21 test. The separately appended specification-derived review equals the approved feedback text exactly. No reference, mutant or original-source code is supplied to either correction author. Each corrected test equals its archived author output after the generator's strip-plus-newline normalization. Both author runs returned zero, no timeout, no disallowed tool events and no event parse error. Prompt/output hashes were recomputed. Independent provenance is established; the individual oracle assessments below are separate.

## Seven-criterion decisions

| Candidate | Clarity/API | Independent test contract | Complete-target substance | Idiom/dependencies | Realistic mutant witness | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Python0017 | Frozen concurrency and ownership API | Controller/observer, ordered failures, public outcomes | Work drain, error ordering, argument/result ownership and lifecycle | Standard threading/futures/copy; bounded test cleanup | Short-circuit gather observed before released second completion | Static positive |
| Python0063 | Frozen parser recovery/link rules | Actual valueless rel, src and href | Parser recovery, normalization, stable deduplication | HTMLParser and unittest only | None rel lookup no longer crashes extraction | Static positive |
| Python0156 | Frozen hooks, logger and state API | Falsey Logger behavior; private-layout oracle removed | Hook order, failed transitions, logging and snapshots | logging/unittest; bounded subprocess import check | Truthiness fallback loses supplied falsey logger | Static positive |
| Python0781 | Frozen matrix placement/type/ownership rules | Repeated same-row overlay and mutable transparency | Topology, placement, transparency and nested ownership | copy/unittest only | Whole-base deepcopy preserves repeated-row alias and changes wrong row | Static positive |
| JS0034 | Frozen glossary and review API | Sparse category/token arrays, no new trim/casefold rules | Validation, normalized identity, ordering and snapshots | CommonJS Map/arrays and node:assert | some/map skips holes | Static positive |
| JS0061 | Frozen protocol/generator/numeric API | First-next sparse rejection before prefix yield | Protocol selection, complete validation and exact BigInt decomposition | Standard CommonJS and Node assertions | Array.map skips holes, yielding invalid sparse results | Static positive |
| JS0119 | Frozen normalized CRUD and atomic changes | Sparse constructor/add/update; unsupported extra-field oracle removed | Normalization, duplicates, atomic updates and detached ordered state | Standard Map/CommonJS and Node assertions | Sparse ingredients skip validation | Static positive |

These assess all seven criteria: clarity, API consistency, independent tests, full-target nontriviality, idiomatic implementation, dependency isolation, and realistic known-bad. The repair delta's size is not the substance criterion.

### Python0017

The reference drains every submitted Ticket, records the first BaseException in submission order, and raises only after draining all; the unchanged mutant returns a short-circuit result comprehension. Argument deep copies occur at submit time, result references remain stable across fresh gather outer lists, and shutdown/context cleanup remain coherent.

The old automatically releasing Timer witness has been replaced. A first worker signals failure path, a second signals startup and blocks on a controller-owned Event. A separate observer signals entry, calls gather, records the error plus the second-finished marker and signals settlement. The controller checks no settlement while the second gate remains held, releases it, joins and checks the first submitted ValueError only after second completion. A separate pair reverses failure completion order and requires the first submitted exception. Observer outcomes are propagated to unittest; all gates are released and joins/shutdown occur in finally. Shutdown waiting is also observed through a controlled gate.

The 0.1-second nonsettlement observation is a bounded scheduling probe, not a required gather latency or proof against every possible starved scheduler. Worker “failed” markers occur immediately before raising, rather than through an independently completed Future acknowledgment. Under pathological scheduling, markers alone cannot prove exact exception completion order. This does not reopen the generic timing caveat: the controller/observer design and reverse-error pair implement the explicitly approved finite witness, avoid the previous Timer-only automatic release, and include post-settlement outcome checks. Main must evaluate actual sandbox directionality. No executed mutant failure is claimed here.

Validation, deep-copied positional/keyword arguments, repeated gather result identity, empty results, exception propagation, idempotent shutdown and normal/exceptional context exit remain tested. No concurrent-submit snapshot or cross-args/kwargs alias policy was added. sys.maxsize workers are instantiated without any jobs in that test; it is not evidence of mass thread allocation.

### Python0063

Reference uses attributes.get("rel") or "" and leaves HTMLParser recovery, URL trimming, exact deduplication and first-document order intact. Tests now contain a genuine valueless rel between valid img/preload links, plus valueless src/href controls and later successful recovery. These are materially different from only missing rel or rel="". Expected ["a","b","c"] follows the markup; the mutant calls lower on None at the valueless rel. Normal mixed-case complete preload tokens, relative URL preservation, exact case-sensitive URL deduplication, incomplete trailing markup, fresh results and nonstring TypeError remain. No URL resolution, new HTML grammar or duplicate-attribute policy is invented.

### Python0156

Reference uses the supplied logger whenever it is not None. Tests define an actual logging.Logger subclass whose bool is False and whose debug records messages. Both BaseUnit stages and AuditUnit base-before-audit pairs are observed through messages/public state/events. No private _logger assertion remains. This directly distinguishes the unchanged truthiness-fallback mutant.

Default None fallback is observed through a temporary handler on logging.getLogger(solution.__name__), restoring handlers, level and propagation in finally. Read-only properties, immutable snapshots, invalid transitions without effects, hook exceptions before state advance and load() effects remain. Fresh-process import checks the specified absence of global logging reconfiguration with a ten-second subprocess timeout; no external packages or network dependency. No new transition return-value or private storage constraint.

### Python0781

The defining fixture uses the *same* row object twice: row=[0], base=[row,row], patch=[[1]], coordinates0,0 => [[1],[0]], with input row untouched. A second repeated mutable row fixture overlays a replacement in one row and leaves a transparent position in the other. Nested retained/replacement output cells are mutated and both inputs remain unchanged. This exercises placement independence, not merely equal separately allocated rows.

Reference deep-copies rows independently before overlay; mutant deep-copies the entire matrix and preserves repeated-row aliasing, so one overlay affects both output rows. Existing equality transparency, ragged/type/coordinate rejection even for empty patch, empty/zero-width cases, exact boundaries and nested input detachment remain. No hostile noncopyable values, deliberately throwing equality, or blanket mutual output-cell unaliasing requirement was added.

### JavaScript0034

Tests now reject categories=new Array(1), valid-prefix/trailing-hole categories, review(new Array(1)) and review(['alpha', ,]). These reach both skip-hole validation paths in the unchanged some/map mutant. Reference indexed loops reject missing entries. Existing canonical spelling, category trimming, exact duplicate-term message, case-insensitive matching, empty/unknown tokens, category order and source/result copy isolation remain. Review tokens are not newly trimmed and no universal Unicode folding contract is asserted. Export checks match the explicitly exact CommonJS export contract.

### JavaScript0061

Tests add both one-hole and valid-prefix/trailing-hole plural packets. canHandle returns false, and each first iterator.next() must throw TypeError; the latter proves no valid prefix can be emitted before complete validation. A dense later-invalid packet is also checked at first next rather than solely through Array.from. No eager generator-call exception is demanded.

The unchanged reference prevalidates all indexed measurements and emits fresh timestamp/result objects. The supplied mutant's canHandle already uses for-of, which encounters holes; therefore the canHandle sparse checks alone are controls, not the decisive mutant witness. Its map uses Array.map, skips missing entries and then yield* can emit undefined or a successful prefix. The first-next tests are the actual distinguishing witnesses. This corrects the overly broad prior shorthand that every mutant path skipped holes.

Both protocol selections, empty plural success, ordered topics, BigInt quotient/remainder at maximum safe millisecond boundary, exact sequence domain, malformed packets and output detachment remain. No unpromised caller mutation isolation between generator advances, timing, native function reflection or broader numeric cap is added.

### JavaScript0119

The unsupported update("bread",{other:true}) TypeError assertion is removed without replacement by a universal extra-key acceptance/rejection policy. Constructor one-hole ingredients, sparse add plus absent stored ID, trailing-hole add plus absent stored ID, and existing-record update with valid changed title plus trailing-hole ingredients are present. The latter verifies TypeError and unchanged prior title/ingredients, exercising atomicity rather than only validation.

The unchanged indexed reference validates all ingredients before mutation; map-based mutant skips holes. Valid empty ingredients, normalized IDs/title/ingredients, duplicate IDs, explicitly forbidden id patch, supplied-field validation before unknown-ID lookup, successful unknown-ID null, detached nested results, insertion order and delete/reinsert order remain. No property descriptor, new extra-key policy or implementation identity requirement.

## Exact hashes and lineage

Canonical JSON SHA256 uses sorted keys, compact separators and ensure_ascii=False. Other hashes are raw UTF-8 strings or file bytes as labeled. Candidate files are `datasets/cache/expansion-v1/versioned-recovery/r23/<full ID>.candidate.json`; previous files are the matching r21 paths. All seven inherit McEval-Instruct CC-BY-SA-4.0 at revision57bd46727e49ac3e2890218a146d35c2454a8496. All rights booleans (answer, model_training, prompt, redistribution, tests) remain true and exact; no ownership decision is reopened.

### exp-v1-recovery-r23-python-generation-0017

- file: `5d85b2c31485fe51009c9760927111e20631bb75f8fc34106108de6a56bc0077`
- canonical: `38a6c0f4b814bc0d317d3b11194d8281f838898d6a901039df8d73caa476fa89`
- previous_file: `398cde94c35d2c90e88d376b383702f5f8488cbe05822a005862568c9361473b`
- previous_canonical: `70f55aefb2559ae95ee6b3e8b21a86599adcdc7861d48e5434c3b4531f128b31`
- original_canonical: `723dca54f596a0ba0fd3a1b0a8c6b18d3a32c03e18ed64336c26b73c5850043c`
- problem: `55a17cb9a4a7c87fad53d875234e74dd0ad3e786a378489843369482713ee5ea`
- reference: `2c8a2aaca90d17e9f047ccd3baeefa124b9a2560349290b6aec4f03cd9a859d2`
- mutant: `cb22d8d8a79cf8ddd9797cc930076b8c565d40ebb6739702b008043f4c82e3f3`
- test: `3ca74313a71cb6d128b29102c21e350f2bff1269fd922f72d37cfc2e740d64df`
- previous_test: `67eb1e06051f46ac2cd21a2988763ee0a10157255004cbd1b225cd9cc799ad49`
- feedback_hash: `5da059df5a86ac2c2aaf9a12a69631f600ece2d59ed41550f210c9c52a616a5d`
- Source row-08337: `264fc64f9bca86a567470ab99e8af285724d0562b4deff83bf96ab2c015bd22f`.

### exp-v1-recovery-r23-python-generation-0063

- file: `9a63e67d73307d06332f99cc2901d1f227901f0eeb7cbe28977ecdb0c9410688`
- canonical: `c0ef63d268f8cc29d227598d669718a1bde09ef203470b0e51cd883e66d06c46`
- previous_file: `aab52df3d7bdd4bc462d86272d8e833c56e19167df34813c4faeb251e6790b5a`
- previous_canonical: `ad2350f7f30aa0d8e2ae1e62b7c5ae25805b71296a319a982e0f8d02613b9a96`
- original_canonical: `b064d4aec3a7de115990eab9116edbb5f8d63ab16722a01381ea7be991ba83ff`
- problem: `d08e2c87d1765592c39b0d92d7fcccf71e0e84ab53a5f8c60760e8951f779337`
- reference: `dc5383b9ea1ca273a52c44ee27c50026f386a44d05d035559cb3dd58fb6e3a44`
- mutant: `bd7e11039e02a86ac3715e3ff1e4b63b1c6ce8f42cb3ae8afa567a41f5605198`
- test: `21a1354e87a99e8a3d403ad448fad2656ab5f25104f98b3e43efb679114006e2`
- previous_test: `5c4bbdf9bd34138c96848d2dfacea749fbce24336870b5b106bd9e1a86b69e94`
- feedback_hash: `c5d682466429d1d2b64568f1595d558246a9f23d05e62e85dbbd342304c7350b`
- Source row-08307: `eee4b16d4bcac7bda70cfaa52ef1df926cab8afa15fe4bfec6997ea37fdb0372`.

### exp-v1-recovery-r23-python-generation-0156

- file: `cdf5c065375da4659827cb7baf6f33bbaeb47c4990bda5de53a4aa30ef37a6b1`
- canonical: `848fe5cd48d382b8b8dd24123c32bf074a7e335ec74f5e92c1e828e62e65e101`
- previous_file: `5e29e1f4c95202d450fd542d02f9519686dc0c1c84a68083085edb403fc71d09`
- previous_canonical: `3bb4f63ee262a44bb403d626383b28d9776e88fa062564598776a3570d38c3a0`
- original_canonical: `0c23e909c2ebad68f8ede1a958275f2556a147199fbef166e3dc9c443e8e64b6`
- problem: `dd53aabfb665ded9b96d502ac5ceb89e2f3a4ee44c82890b27cdfe4a9f917cba`
- reference: `e72699b581817c88c09c6180ad5326de212ed1928d9b65d5275242700fd9285a`
- mutant: `04601ba54b2a9d8c36b51dc0437bc1f85f4d2bc8591d7e6375e62d926115fa36`
- test: `fbcd8cacadbffaadbd4702ebf27602add18b986fc5ac8ab75eada0b989479115`
- previous_test: `ebf51dee75160ce3fb63fb71323e32c92a7b217ac3e0089b4e37531e795b86e2`
- feedback_hash: `fa6bec20f5666c2004a32bd613dfa5fa2ff1edc9c8a920bfbf09075ee7b0aa12`
- Source row-08157: `002be561d743d0b170192022d03dfe040e83c1d56c16e7d9c87f25d8e36bffdb`.

### exp-v1-recovery-r23-python-generation-0781

- file: `17f7e13d23a47136d485b4d157fd515809811aa91506d86b7144db4384475682`
- canonical: `d7d0239aa3c23296bf861ec0ab012aa2d48a6525dc2047ade6fa3d31f61d02cc`
- previous_file: `d21edb3cbb5d1c2cb6085d2092e6a58a68cf4730ab16560e6c4a8c2bf9e55911`
- previous_canonical: `0f41054b1abeeefbdd6ab057b349dbb9bb2f97e99ae5864d18eb4b4b3881d923`
- original_canonical: `e38611dd9c5e9d79c0ae6264ad5445cab62cfbafee1f652cba9dfe8243607df3`
- problem: `22f0c818bc8d999d1776bd5447344bc136cb8bfc51f675aa69e5e58b308fca74`
- reference: `a603c86b534e84c129da93df2a0efd6ae8199b0bc1693f01f71c9a2c94899a18`
- mutant: `cca7111f939b953fce593f5e75e830ccffa4948f15bba553f93b683cdeb589c5`
- test: `0aa9a397fc461c9725bf9f472c1f68303dab078ee199d022fe4cb069c7d57b7c`
- previous_test: `f3a3063c95ed4e946e6c41d5a593861eca903dfbd9acf2f81485527d21575a91`
- feedback_hash: `c05dd8c700049c6401048d12ee403c91fbbd8bb984a7b0697b4a2b19c83a6711`
- Source row-08398: `2397dd65af3b9e0d7927b07b721090b7be7c3c50ab170213e14fdfac188fad3d`.

### exp-v1-recovery-r23-javascript-generation-0034

- file: `48544674e651ce6002acb650fe784405aa32dffae19082c59b78a776d7e8214e`
- canonical: `bfd523c1af7160bb1689e021bd7bb21d3e59848e21ce9426ea13b7fcff016fef`
- previous_file: `9c283edf5361684292ebd8cccd5bc94cc6f01002ab510b341025fd4c3d496592`
- previous_canonical: `4f0cbf133323325866dfc807ef3f3f399b3127f0ca2f2b889ccf80d2744e9e85`
- original_canonical: `4d16032d68bb2d5e5cf60535b0edf67c3b5a8e1397f8a44988a75c5fb6df80ff`
- problem: `45da4f03a13fd9c303d286b5852c1adbcb0286a298f6b3f5b6b0b103212b411b`
- reference: `f603a5c0729b15a0a5d8e95882c974e8b3c7c2f71008a4dc75ab9c97d088748f`
- mutant: `ab8f5ab2391a7882c2eacb707c100df32c06b22778662c3c2dae489c721cecd4`
- test: `96998bab2d846f6b7dcb43f155a54ca3fad17895c7f5b772170669f46770226e`
- previous_test: `16632fa6a29a9ca69fdb31df97b587fe55bceb51606cc651389cfc32c78098c7`
- feedback_hash: `e344a3398999f35d86675662a100366326c703c013e698cadadc5d26605662cf`
- Source row-26941: `8a3af611be382bc79cb152e4ed5cfe8eeb4c4ad01e0c81319b00261034c8b184`.

### exp-v1-recovery-r23-javascript-generation-0061

- file: `9bb41ddb0641b74b9c0c80a418d7cf130d5e4ce1351f0d51dcd0093d642ed5ac`
- canonical: `649452510973fdd1452883b56d7a233d0c1e363a045c6d07068d49b1dce61620`
- previous_file: `d21f15ea11e3ba6ae42490036deeba6ecee17b0cdfdc19639a8dbc2ba493c2b8`
- previous_canonical: `1e76cc969898ba2699092735cdf86a97eb35922d28751e2ef50511c1a2cc8332`
- original_canonical: `08071ad6a6a8e77b4cddf1b6fcfd34268f384a12eda00a0396a58bbfeba6e80f`
- problem: `74c2f55d8b0f39db80a343db6f00100c4e0433054d0952a3eb82e44c28ab0100`
- reference: `90af16c128bd7f7a36e9b283b2604f7b436c0978809d098ffea80c1d0039daa7`
- mutant: `72dd01601a3aa71f6c828c2e679980141e924430d6c81ed91dc89b219d14bbb6`
- test: `f1ab9664f019001f8326bbee6d2741fe71de3ee65413c11db9ab86319a8b9a08`
- previous_test: `92730acf7affaf08d5ab31294a037c4c3a35573690b3d7118d9845c5562fae8e`
- feedback_hash: `a7efb3d0160824405841c69135d06b2d358edcec7cc1cb6effad6e08b7aa7022`
- Source row-00458: `1d9b1ce15dea8656592b52316ea3a0fec2cd723ec394a85aef6423b32d4d8b8c`.

### exp-v1-recovery-r23-javascript-generation-0119

- file: `89704c7a7ea64ef87efeba0c72c5daf69c49a1f1358aa1561861ed53de15129e`
- canonical: `0e3b33a71a5374e912de0e8868780123a2d870d05ea29ce33d1b28379f8320a1`
- previous_file: `6d1d8be5b6a33ec4a50e69691be01942ef37200085088795d956b98515dc2b90`
- previous_canonical: `658d770a922455bbcaef9965b8c3c506787d4b2148d389c3027a1ea2d53568a5`
- original_canonical: `74e1d6caa1a6ffbb6faec18c7dcdb39b7eb2290c4cb8a8724eb6148370c04715`
- problem: `343ae18119a895d6712bde36bcb1780712952a8c3af9d444cbd68da07e4ce4f0`
- reference: `1830c84ebe9987d703c8a6745fbb8660d54760214dda8cd1a36292196fdc9d30`
- mutant: `7905c995d1ab009229a61a313ba945b2309c8185c35bd651eec64793cc477efe`
- test: `0c71f992667d185caed4674020b32bc4ffec99622941df90452811ef32ec147a`
- previous_test: `3defbc6e0dfd3e5654ac4d7129dbcfb8d4b1657d308ab1c10014f33d59a550c9`
- feedback_hash: `e28d5123085ca553193e0c0dfdf8cbc82cb398906c41d6853d9e1740247cba00`
- Source row-06759: `b994176cea0b1ef8ac7450227ae93824318fea927afcce78ae14aef1084bc0a2`.

## Bound shared evidence

- `measurement/data/expansion-v1/cutoff-5885-review/recovery-feedback-r23.json`: `ac425fb14ad116ccd3af62dbc8d339ac760bb1e4d0f7f87b70a1f766fd4a6f76`.
- `measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r23.json`: `0be4170d2177912f8a1079d5e76c09131cf7d65e6e0340cbc91b2e72cf1bb752`.
- `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R21_PYTHON_REVIEW_20260908.md`: `d264153dddcacbf867374465206a504453b00a1dfdd6d21b2c0604f5677d111d`.
- `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R21_JS_REVIEW_20260908.md`: `f7052164e82503b220c84ae6ce5c4379d3b55397b344207990779f52c082ae71`.
- `datasets/cache/expansion-v1/versioned-recovery/r23/plan.json`: `d44918671d7a9350cc90e67ac7eede1ee4ab61e6ce6bae2f1eadaccbed367d92`.
- `datasets/cache/expansion-v1/versioned-recovery/r23/run-contract.json`: `779dbb642d6651a9c7d7e0e4b9ea0c1802052ce5614c7ee96307f3555271d0b4`.
- `datasets/cache/expansion-v1/versioned-recovery/r23/python-recovery-test-correction-evidence.json`: file `50fc862ace68c93f6bb1f5e3d7a8a4d411d0679af104d377402ab420da753d32`; prompt `2755bec13228f4ddcb6cf5868f62896e2f655fa28ad87cf5b3ae533d487cb5dc`; final output `b425aab414e51b1d12888956f65296a840eb10231e085f0f0b8faf032e8f0ce0`.
- `datasets/cache/expansion-v1/versioned-recovery/r23/javascript-recovery-test-correction-evidence.json`: file `490907be30f6d6400a3389edff730ac4eb3a03ccd893c7dd27e77645a0bc6bbb`; prompt `159bf57506c19a69743eae034a9fc70b85fd9d12b5cd05fff784e48dc45956e6`; final output `9c4b857e8731047c8dc0abe358ee220a76baef0a221e954d26f338c8dedfe45d`.

Original corpus remains cutoff-5885 final.candidates.jsonl; neither original nor R21 holds are overwritten by these terminal derived conclusions. Seven static positives are ready for main's existing quality/separation and sandbox qualification workflow, not automatic admission. No further critic or retry is recommended or authorized by this report.

