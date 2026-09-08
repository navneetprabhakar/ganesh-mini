# Python/Rust next recovery selection — 2026-09-08

## Recommendation and boundary

Recommend **17 held parents: 8 Python and 9 Rust**, a shortfall of3 against the requested10+10. All20 shortlisted prompts, complete references and supplied test files were read; repair prompts include their full original known-bad source. Exact hold reasons and their per-ID review evidence were reconciled. All17 are currently held and exclude every one of the12 r1 parents. This is selection advice only: no generation, candidate execution, cloud, admission, central edits or new original inspection credit. Main approves the eventual tranche.

The candidates retain substantive algorithm/state/ownership interactions rather than padding elementary tasks. Each needs a new immutable derived candidate, fresh specification-only independent tests and actual reference-pass/realistic-mutant-fail evidence. Source hashes below are binding, not approval of unseen derived output. Do not silently lift original holds.

## Python8

All numeric repairs must retain exact int values: do not call float or math.isfinite on arbitrary-sized integers merely to validate finiteness. Do not add global integer-digit-limit changes. Where native mixed numeric arithmetic has an unrepresentable result, do not invent a finite-output guarantee; the explicit decisions below must be frozen if needed before generation.

| Parent ID | Change class / minimal correction | Substantive target and specification-grounded independent tests / contract decisions |
| --- | --- | --- |
| exp-v1-python-generation-0355 | reference-fix: remove the unstated string-only batch-key guard; retain permitted Mapping keys unchanged. | Four byte-descriptor algorithms interact with one-shot batch materialization, first scheme order and duplicate-record position. Test integer/tuple batch keys (no invented coercion), multiple schemes over one-shot records, duplicate replacement, odd/partial blocks and mutable payload isolation. Keep inner record names nonempty strings. No new batch-key restriction. |
| exp-v1-python-generation-0445 | reference-fix plus fresh oracle: normalize each selected outer notice Mapping before deep-copying its contents. | Authentication-before-selection, complete notice validation, optional filters, duplicates and deep ownership. Test matching MappingProxyType notices/principal with ordinary nested data, detached values and rejected unpublished rows. Correct the original malformed-scalar tests' extra list wrappers so a malformed field, not a wrong outer shape, is actually tested. Do not require a concrete copied Mapping subclass; preserve contents/independence. No unsupported filter-type expansion. |
| exp-v1-python-generation-0298 | reference-fix: accept finite integers without float coercion; retain float nonfinite rejection. | Fuzzy/casefold matching, filtering, three-key ranking and pagination interact. Test rank10**500 and adjacent huge ranks with tied titles/IDs, ordinary float rank, NaN/inf/bool rejection, fuzzy boundary and snapshots. No float output is required and no new range decision is needed. |
| exp-v1-python-generation-0314 | contract-clarification plus reference fix: int-aware finiteness; explicitly retain Python numeric addition semantics, with OverflowError allowed for unrepresentable mixed int/float arithmetic rather than an impossible finite guarantee. | Composite-key join, validation of unmatched corrections, ordered output and copied tags. Test huge integer primary with no correction and huge cancelling integer offset, duplicate keys, unrelated correction validation and tag isolation. Preserve ordinary float results. The mixed-result policy is a proposed explicit derived decision requiring main acceptance, not a claim it was specified originally. |
| exp-v1-python-generation-0319 | contract-clarification plus reference fix: int-aware coordinate/limit validation; make native numeric advancement overflow behavior explicit without capping valid integer coordinates/speed. | Reusable fire/advance/inactive lifecycle, no-op active fire and boundary deactivation. Test fire(10**500,0), huge integer limits, exact huge integer speed/y movement, refire after deactivation and snapshot isolation. Validate inputs before lifecycle shortcuts as existing behavior; no promise against direct user corruption of public fields. Proposed derived policy: unrepresentable mixed addition raises OverflowError before movement; no implicit float conversion for integer paths. |
| exp-v1-python-generation-0269 | reference-fix: finite-real predicate must recognize exact integer/rational values without float conversion; preserve ordinary float finiteness check. | Complete metric-schema validation, unique IDs, threshold order and per-bucket input order. Test threshold/value10**500 equality and nearby integers, Fraction controls, MappingProxy inputs, malformed schemas, NaN/bool, fresh nested outputs. Arithmetic is comparison only: no output-range restriction or concrete input-Mapping type restriction needed. |
| exp-v1-python-generation-0672 | reference-fix: validate every attributes key is str before copying, raising TypeError for non-string keys. | Frozen dataclass contract, whitespace normalization, post-trim duplicate tags, exact output-key order and nested ownership. Test an integer attribute key directly, empty string key as valid (not forbidden), ordinary nested values, duplicate normalized tags and frozen fields. Do not require arbitrary opaque noncopyable values to clone; retain ordinary deep-copy-supported envelope. |
| exp-v1-python-repair-0138 | contract-clarification plus reference fix: finite Real validation without lossy float coercion; preserve accepted-only grouping and first-accepted order. | Whole repair has validation of rejected events, group ordering and numeric aggregation. Test huge integer accepted amount and integer cancellation, Fraction controls, rejected huge amount, late malformed rejected event, count/order and fresh results. Explicit derived arithmetic policy retains native numeric sum including normal float behavior; mixed-operation OverflowError is not reclassified as malformed input. Keep the original accepted/rejected predicate corrected. |

## Rust9

Repair generation must embed a coherent complete known-bad source reflecting one selected realistic defect while preserving all other required corrections. Do not merely apply the original advertised one-line repair and leave the later held defect intact.

| Parent ID | Change class / minimal correction | Substantive target and specification-grounded independent tests / contract decisions |
| --- | --- | --- |
| exp-v1-rust-repair-0343 | reference-fix: reject forbidden ] in extracted kind and value before accepting any output. | Full restricted-grammar parse must continue after first match. Test forbidden bracket in matching value, forbidden kind after an earlier valid match, empty matching value, Unicode/newlines and valid-first then malformed suffix. Existing bad-kind-only None test does not discriminate the defect. Preserve exact allowed grammar rather than broadly reject UTF-8. |
| exp-v1-rust-repair-0361 | reference-fix under pinned64-bit runtime: compute elapsed+remainder in u128 (or equivalent quotient/remainder decomposition), keep exact remainder; avoid saturation loss. | Time carry, directional cancellation and clamped movement interact. Test step=u64::MAX on1x1 grid with elapsed MAX-1,MAX,1 giving0,1,1; exact/partial/zero intervals, independent axes and error precedence. At most one step per witness. Return usize representability depends on64-bit pinned runtime; no inferred32-bit portability promise. Computing clamped repeated movement in bulk may avoid enormous loops but must equal per-step semantics. Preserve existing exclusive width/height bounds and validate no invented private state. |
| exp-v1-rust-repair-0113 | reference-fix: previous uses zero-wrap or decrement instead of index+len-1; retain correct next modulo. | Logical ring resizing/clamping plus orthogonal page/overlay/focus state. Test usize::MAX logical ring after one next then previous, zero-to-last wrap, len0/1, shrink/grow and UI isolation. No large allocation or private-field injection is needed. |
| exp-v1-rust-repair-0102 | reference-fix: trim only ASCII whitespace in project_slug, retaining exactly-one .git suffix removal. | Slug grammar and stable cross-category tracked-ref deduplication. Test U+2003 prefix/suffix preserved, ASCII tabs/newlines trimmed, repo.git.git retains one .git, invalid refs skipped and branch/tag identities kept distinct. No URL parser or general Unicode whitespace semantics added. |
| exp-v1-rust-repair-0095 | reference-fix: custom Default delegates to new so first public default-constructed ID is1. | Book insertion atomicity, sequential success-only IDs and same-entry authentication. Test Default and new first IDs, invalid/duplicate add no ID consumption, case-sensitive address/secret mismatch and observers. Retain AND authentication repair. No inaccessible lifetime-exhaustion witness or new public error variant needed. |
| exp-v1-rust-generation-0558 | reference-fix: trim and reject empty Zone lookup before map access, returning Invalid. | Dispatcher maintains linked tool/zone indexes, cascaded removal, insertion order and failed-command atomicity. Test Zone(empty/ASCII/Unicode blank) Invalid versus nonblank missing NotFound, no mutation, normal trimmed lookup and tool/zone cascade. Preserve explicit enums/signatures; do not infer behavior for manually inconsistent public maps beyond the stated command workflow. |
| exp-v1-rust-generation-0778 | reference/oracle correction: use ASCII whitespace trimming around bracketed records, not spaces-only; replace contradictory tab-rejection assertion. | Percent-byte codec, UTF-8 validation, two grammars, duplicates and canonical sort/rendering. Test tabs/CR/LF around whole bracketed records and empty interior, forbid whitespace inside keys/encoded values, preserve Lines CR rejection, uppercase escapes and invalid UTF-8 distinction. Prompt already states the correct rule; no contract weakening. |
| exp-v1-rust-generation-0757 | reference-fix: complete ordered kind validation before checked summation. | Validation/error precedence interacts with bounded arithmetic; not merely a sum wrapper. Test MAX matching,1 matching,later mismatching kind returns the first UnexpectedKind, while all matching MAX+1 returns Overflow; exactMAX, empty kinds and borrowed-input preservation. Check fields/variants without requiring unpromised trait derives. |
| exp-v1-rust-generation-0704 | reference-fix with explicit allocation-error mapping if needed: check representable Vec byte length and use fallible reserve mapped to Overflow before zero-fill; retain checked dimensions/indexes. | Pixel tiling, partial-row zero fill, lowest invalid index and dimension checks. Test one1x1 tile/usize::MAX columns returns Overflow without allocation, ordinary non-square tile layout, zero-area controls and validation order. Avoid ceil-add overflow with quotient/remainder row computation where dimensions/output remain representable. Do not execute huge feasible allocations; clarify that allocation/capacity failure maps to existing Overflow rather than claiming all memory exhaustion can be made successful. |

## Three not recommended in this bounded tranche

- exp-v1-python-generation-0058: int-aware validation alone leaves a0.0 accumulator, huge integer conversion and tolerance multiplication/float boundary semantics. A full exact rational tolerance policy is a larger design choice than the held validation witness; defer rather than imply a one-guard repair completes it.
- exp-v1-python-generation-0343: constructor int-aware validation alone leaves mixed int/float multiply overflow and potentially partially applied adjustment. Numerical result/atomicity semantics need a fuller recovery specification; do not force it into a narrow reference-fix.
- exp-v1-rust-repair-0223: unsigned miss exponent correction is clear, but full reading exposes wider stars/product and cached-difficulty nonfinite semantics. Defer until those are deliberately specified instead of endorsing a single cast repair as complete.

This shortfall does not claim no other suitable parents exist. It records the result of this bounded20-record inspection without automatic expansion or generation.

## Source/rights and immutable bindings

All selected records have prompt/answer/tests/model_training/redistribution rights flags true in the frozen parent. These existing authorizations are preserved, not reopened. Most use McEval-Instruct CC-BY-SA-4.0; Python repair0138 uses MdEval-Instruct MIT. Exact revision, record ID, source record hash and license are below. Preserve full original source object and transformation lineage when deriving candidates; table shorthand is not a replacement for them. Parent canonical hashes use sorted-key compact UTF-8 JSON, not JSONL line bytes. Original corpus SHA-256:680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.


### exp-v1-python-generation-0355

- Parent canonical SHA-256: `ed9c9388c83fae7fb3b171fa6c584a67e1adfb82b4285b55d0aedf62ff3c3ba5`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/PYTHON_MAPPING_ENUM_CLOSURE_20260908.md`; file SHA-256 `6bfe636fd24282b350cfe3b21838400df202de6e9273edf5654d3c9adc2e46b2`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-08580`, source record SHA-256 `95f9c5485589d711a3d76fed2b6fa4793705a545aaadc217dd940d94e5e48be8`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `eee7633773233463861add808aeb885ac96f1b0e123610c18a2163359c59775a`; reference SHA-256: `9a9559c49aeb981b655c25834e2cefeafbad8cfce1c5c3b28afa14f6958a5500`; test content SHA-256: `1c842661ff00febdd088996f454ad3aa3f863252b999ec5f494065a209958868`.

### exp-v1-python-generation-0445

- Parent canonical SHA-256: `36207ebf9a306b6c60f8dce488e5fa5b9201590be6e5a599ee6799bcde1abd68`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/PYTHON_MAPPING_ENUM_CLOSURE_20260908.md`; file SHA-256 `6bfe636fd24282b350cfe3b21838400df202de6e9273edf5654d3c9adc2e46b2`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-01665`, source record SHA-256 `9258268b4254ce521f8473564bdf05866202ae705ceb4017c1e1b0fd87bff909`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `8187eea886aa094141dfc5caac2b1e15cb3c3fb80d30482318ba0c4392ffc3c5`; reference SHA-256: `4d4870713bdab37c4bc4f565014dac63c562385f455c6745ec2f98c8c1ae44d4`; test content SHA-256: `76ad7682e3168eb5bee8089f5e6d601a6da06f713352691a903d855476a94fc7`.

### exp-v1-python-generation-0298

- Parent canonical SHA-256: `e2c534bf1c6c91ab58615e9bf378f93e983c48e24dbc05497c88d853847d6d74`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/PYTHON_CRITERIA_REVIEW_3.md`; file SHA-256 `c718ed10bc18d999264e2a9366dc21e19a328b159e5abae5848c868063da0caa`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-01613`, source record SHA-256 `fa2de74830d50616b4215b62768dd9017086762b0e8755ad059403385f34e09e`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `879c6fb43290e8a23967ce56bdf682263ee1d0643be61009c537d36e48ebcfce`; reference SHA-256: `eaaf114d1ac9e129bfe332f16312fae2a011b522031e570bb7237058de10d232`; test content SHA-256: `d94706be9821347f06b604f12f006feb0c0700f1315067a008cb2da5a3498226`.

### exp-v1-python-generation-0314

- Parent canonical SHA-256: `1a205c41c4b415a66b071e934a4589185fb2acce421368551a607bb54386444b`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/PYTHON_CRITERIA_REVIEW_3.md`; file SHA-256 `c718ed10bc18d999264e2a9366dc21e19a328b159e5abae5848c868063da0caa`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-08522`, source record SHA-256 `39d5a89b3a99632bb4824c92aefe0dc49bc1549a35db0cedf4a9932820119a49`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `9f4a81647da4891baf2db10f6f63a82d6800682e9eb35e265cc469728f9bc67b`; reference SHA-256: `d668259f31e4848941292f83bb1fcfadd20ef26589d05a304c2fca8c1f436d2b`; test content SHA-256: `366589bc1fb41217c59c2cd0feccbd0382b31240d01ee42e82653e963ecb5e04`.

### exp-v1-python-generation-0319

- Parent canonical SHA-256: `f3b5c7ada4a0a4a084d855651077552a9b32c69a87b784edf136b19d7df37c43`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/PYTHON_CRITERIA_REVIEW_3.md`; file SHA-256 `c718ed10bc18d999264e2a9366dc21e19a328b159e5abae5848c868063da0caa`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-04265`, source record SHA-256 `c7566374d93b309443a31d5c02a89c175339a4990d9f9c39d9cf1a9b9210e8df`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `6e20d59ad3ad2e4518a00ac8e913c651e33514e27e8144e72945afbe9770029c`; reference SHA-256: `57974ba23a13025d7247ce40e423666b88a405d38b6d5b921d9734f34c065083`; test content SHA-256: `706306142219164ce772bc86b0befb2119571c727eb29dce94ec926ee2822003`.

### exp-v1-python-generation-0269

- Parent canonical SHA-256: `331bed53d9cc5f83528fc6c80aa1e9a9bbd6cef6c69debee947eff470a659291`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/SEVEN_CRITERIA_PYTHON.md`; file SHA-256 `5760e665691c09509d0cf198bbbabc4447e35bc8da86306c6f5454992965173d`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-04053`, source record SHA-256 `10ede521237662c587f7eb6c80b27eec0b1c594263166aff191ab2a5fbd3e907`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `b4a25d8a13c663751fafb1cea6f3c35d914a0212969f64a8aaf2eb23168153af`; reference SHA-256: `bd69826d153ba212c170105bdf0f357b71d1efa1ec7aabb1048a158806b6429a`; test content SHA-256: `d0d69317e35cb76b8b520f8a441665a695c0f9c56e3a8c0b3102ce015bbdfcb8`.

### exp-v1-python-generation-0672

- Parent canonical SHA-256: `af888ea9cca48d7fc324a0c3b66d3dbbeab896e8baecf29cc0e5b1fb52b460e9`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/SEVEN_CRITERIA_PYTHON.md`; file SHA-256 `5760e665691c09509d0cf198bbbabc4447e35bc8da86306c6f5454992965173d`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-04090`, source record SHA-256 `140650457ba08b5c48c211c8e95de09e93e83ea4aa9c8a6f46f5cfe32aa1604e`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `b1031b1c96a8d866d71e60e2193f139cf27aa6c225de4cebe5d22bdd001061f7`; reference SHA-256: `bb77755d0d767dcbd911a4781e9b23aaa854a09df8d90e406f4ace8d1768c2d8`; test content SHA-256: `549ad68d75ed65511772cf4cbb63c784cbb34b8547528f579f6ef931764f6b20`.

### exp-v1-python-repair-0138

- Parent canonical SHA-256: `097e1648410b0391b52875d213ea6a982c8d3418fe08bfd48153bf2c6da17c72`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/SEVEN_CRITERIA_PYTHON.md`; file SHA-256 `5760e665691c09509d0cf198bbbabc4447e35bc8da86306c6f5454992965173d`.
- Source: `m-a-p/MdEval-Instruct` @ `38c9197e3add996fae624eb198ebd06155b2101e`, record `row-01990`, source record SHA-256 `73599e4b3e0df122a094495051835c773da202b671b7dc60365f75a9854362de`; license `MIT` (https://opensource.org/license/mit/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `a0c41a600c6e8c8aa9c9e36cb3dd848c5feb11ff7c12254092a25a22395cb598`; reference SHA-256: `73863c0d4a7512b23d97468999075f0f08ec352f543d9d5d24f5790d94919779`; test content SHA-256: `d125c70adafa73e2f39c1f3b53ece5f904c25247d89c82e2ba05acc7bbb01720`.

### exp-v1-rust-repair-0343

- Parent canonical SHA-256: `c9dd3f8da96f17de8beb02fa7caa4db8b37bcc8ac5310049ba80d78352dc61dc`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_21.md`; file SHA-256 `079207144cccdb572f633febe23b60ed2a9c26bb42e395fb6cd124da2a1d038d`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-23662`, source record SHA-256 `69f046905718618b53c19cc17341846b06ede647a6a851c5dbf0d7922941a78a`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `be8c165563e346ddbabd3b4893940f8a1422ee04f3703f2cde2711ff7872b6f9`; reference SHA-256: `d41eed62c476eefb56b881ce9487aff9b1e561112fa555918da8835df2d8dd54`; test content SHA-256: `da9a35354a04e29773923d1fe7eda0e803a8a32be76b1cbf469d2389816845f2`.

### exp-v1-rust-repair-0361

- Parent canonical SHA-256: `7f4a1f8b5996c876c97df3b662c4198b0e58ea0420b219abf391399d3a6aa015`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_22.md`; file SHA-256 `556d8b77f2081976d98289781c3be970575497703a7b708d57d782761d3ee8ad`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-23923`, source record SHA-256 `69e904572e01dba6a53d62c34aff15a6a7af7dbbc934bdf50c1b14464c7a80db`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `a5d3d062ec36befc1327a26d8fd14d222b0f5e5a93e260aded9932aa86ecff17`; reference SHA-256: `3b87f6a3c1e515e6cf3e568016625dd897a0f497cdbca8ad311b08e7afaf6d78`; test content SHA-256: `3a5ed1ef1740a31430d109354af98b6f420a14abb44d0e0332af7fdfda5f1d6f`.

### exp-v1-rust-repair-0113

- Parent canonical SHA-256: `942bc20053c7f88bad642fef157e0cc411dd89b5b27ad9f5479166fe70e921f7`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_7.md`; file SHA-256 `f59c4574805967e005972ce8dfb22631d84d718b697fac03246865e592422e60`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-06274`, source record SHA-256 `8fcbdea35247717fcc566870d4b776765c99c868dff6533147fe2d90cf04f6fb`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `d584acab078711418093b921059f04200dab88811f5e83a45f3245bead43432f`; reference SHA-256: `f853812d47850d680a7677b8b30802e1f52a71d62178e44157420b166d49d919`; test content SHA-256: `123112aa273d6390614812aa05be1d95d0d785deead0d11985b909846f8ac956`.

### exp-v1-rust-repair-0102

- Parent canonical SHA-256: `8c2b016284660327c9d77e34b6ccf76585bcaf4e147c761ef4d9bfe7d4a923f0`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_7.md`; file SHA-256 `f59c4574805967e005972ce8dfb22631d84d718b697fac03246865e592422e60`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-03276`, source record SHA-256 `d11d77577758ac7332e12deb503c8cf60f1257cbd1c6e0fe66cc774fe35152b2`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `4757f3df1b2cb7e9f8606be69fdda43da0573ba4208d594df0092c9d21528326`; reference SHA-256: `6b2ec40b5b9a4653c04112c1490efe0704952f24c0bede3e1b95de727ea94637`; test content SHA-256: `d32ae989464bd0182c419686a5d9367ca83998ef565070475faae2072cd08bee`.

### exp-v1-rust-repair-0095

- Parent canonical SHA-256: `1f0349892f99919906a6a1150d189fdeb1404b3d04dc11a6db486c2478f36ad7`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_6.md`; file SHA-256 `2e5a33cf86973a29052f686083002293dc924375abc0a129ffa7d02f570c296f`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-23720`, source record SHA-256 `d8d862ca93eac78348575794a692db1cab7dfeca2f6ee7eba370ca9c88656da8`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `5292b3cb9936e6f2cd2093a9bc470564562da61574f0ffbd2f17a40c68377889`; reference SHA-256: `3b82c08fcf9e4bb271f792464fc0b8debd82afc43a6164b50efa79ad54400853`; test content SHA-256: `91d078b969a86021a522ffe4e91bfd8849e61a57bba647ac542cedf919012b87`.

### exp-v1-rust-generation-0558

- Parent canonical SHA-256: `aa56c6090a2bfa2124c29e7066c9d42c995b3c6cd4e026063007dfa8ce6786f5`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/SEVEN_CRITERIA_RUST.md`; file SHA-256 `63c0fc957ad7ea05fecf61daf7f25823e122ffd23a319aad075a22f93fb92ef6`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-23825`, source record SHA-256 `e3f1d50c3bf33512a51aad31899bfc92d6f7e0b0d6d418b6b1cbfb7dd1e240de`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `327b75f4cc99495529ae51b0007dafd9a898819ad735587127af14f1e6edc257`; reference SHA-256: `1102f4fb30a4ccb75a80112246414eaf39b5b6c6c5df6a66cf74c05cce805116`; test content SHA-256: `15258ad08c17380acb6a791ce2f32a6c2e6e7145cd218c4a208297a346cbc480`.

### exp-v1-rust-generation-0778

- Parent canonical SHA-256: `e37bd12235442df21853d1913997f065186671d0f5077ab950f00a6b0c44232d`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_STRATUM_REVIEW_45.md`; file SHA-256 `b989ab1c987f1bb7bf9584ef48c77172895bbdb0a30eec3765c6ba1fb74cd706`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-05920`, source record SHA-256 `cfe7fa0ee1917f6fd254bcb710d56ad9ca2a3a3387fc4553ebc098abe4568cc8`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `ff9c5303d9b7f7d5721a32bfc450d222b6234f62cd8328a2840b1d088119142e`; reference SHA-256: `28fd769b7714cfa448eb86aec061ce2a6b6d602a368de55eede7532ad16ca989`; test content SHA-256: `0381fed1c153912f9fbec5e1bf396e453a9c0825c0b976c0ddf6022344502f60`.

### exp-v1-rust-generation-0757

- Parent canonical SHA-256: `e4f39e83aa6be47b212b1ef506b86afe040a3222d17d0968decfbf9beaa90e0c`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/aggregate-kind-priority-result.json`; file SHA-256 `c2b4c69f96b50b2af5863cefba5aa81e9e82740775376bcb4793a93b4311ae36`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-03237`, source record SHA-256 `780529f1e9d418b3d3d121d7cc9c3ab31b8e44d5f40b1825a8aff73d4272c5c6`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `0cae7a9b90fb212cb21667ac2efd6d70760ddb38cb9f103900953f364d23961b`; reference SHA-256: `23c46242f185a0adcfed30ac02dfc0ea2017d9dca4fcd3e9cb654c2cee5a1672`; test content SHA-256: `595bc8bdf472669a823cd5615482092d71e7942c2c99a475a38d2a63491348ae`.

### exp-v1-rust-generation-0704

- Parent canonical SHA-256: `a31e3ea788faae40f14f0db4a78c0354ac049f306ae5ef7757d4084b51f3761d`.
- Hold/review evidence: `measurement/data/expansion-v1/cutoff-5885-review/atlas-capacity-overflow-result.json`; file SHA-256 `4d208e334c892ef7acf8fa172f3e0c152575cd8a38259086c33e2c718501dab4`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct` @ `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-03222`, source record SHA-256 `a5ca26bf3ea193deadab1d88a5f8aec2527f84ff7ed9cb1a6ad229fbc937130a`; license `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/). Rights: prompt/answer/tests/model_training/redistribution all true.
- Frozen prompt SHA-256: `be581397e6f26704505cd7cefaabd4ec5bf509585ff2b88ddb5b5acd2ab1a7c8`; reference SHA-256: `032a5ddecdb994baf3f53e709a36ef90962db01ff62ecd74dca05a9e90df8c47`; test content SHA-256: `fb189ca76a93faf3cfe0d50ec67b10db14fc5809665b1c418b5c380bab605e23`.

