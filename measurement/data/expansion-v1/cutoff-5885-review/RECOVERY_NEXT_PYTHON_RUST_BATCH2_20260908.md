# Next Python/Rust recovery selection, batch 2 — 2026-09-08

## Recommendation

Recommend **11 new held generation parents: four Python and seven Rust** from 20 freshly inspected parents (10 per language). Explicit shortfall against 10+10: **six Python and three Rust**. This is a bounded selection result, not a claim that no further recoverable parents exist.

Gate 2. Only this isolated proposal is written. No reservation, generation, candidate execution, cloud action, admission, central ledger change or new original-row coverage credit. Complete original prompts, references and tests were read for all 20 inspected parents; exact per-ID held evidence was reconciled for every recommendation. Small patch size was not used as a triviality proxy.

Exclusion scanned every currently present r1–r20/plan.json: **120 distinct original parents**. None of the 11 proposed IDs overlaps. All 11 remain in additional-holds.json; snapshot SHA256 9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee. Repeat exclusion before reservation because concurrent plans may change.

Original corpus: datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl; SHA256 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec. Canonical hashes below use sorted compact UTF-8 JSON.

## Seven-criterion and generation conditions

The selected scopes retain complete API/contract objectives, language-idiomatic standard-library implementations and substantive interacting behavior. Fresh independent tests must be written from the approved specification without corrected-reference or mutant exposure, and must exercise each stated decisive witness. Use one realistic mutant reproducing the held defect, keeping other corrected objectives intact. Original tests are evidence, not authoritative oracles. Source/rights must be copied in full, including original transformation history plus explicit new lineage. No selection is admission: derived full-quality review and sandbox reference/mutant evidence remain mandatory.

Ten scopes are reference-fix, preserving original problem bytes. Rust0071 is explicitly contract-clarification because the previous diagnostic accepted either rejection or CR preservation; this proposal chooses the exact-value LF framing interpretation openly. All use authorized McEval source revision 57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0. Recorded rights answer/model_training/prompt/redistribution/tests are all true for every recommendation.

## exp-v1-python-generation-0063

**Change class:** reference-fix.

**Concrete request / minimum correction:** Treat a valueless rel attribute as absent/empty before tokenization; preserve standard HTMLParser recovery, trimmed URLs, case-insensitive complete preload tokens and stable exact deduplication.

**Contract-derived decisive tests:** The literal document <img src="a"><link rel href="ignored"><img src="b"> must yield ["a","b"]. Add valueless src/href controls, repeated URLs across tag kinds and incomplete markup with later recoverable links.

**Contract decisions and whole-task quality:** Do not impose a new HTML grammar, URL resolution, duplicate-attribute policy or custom parser. This is interacting parser recovery, token classification and ordered collection, not only a string wrapper.

**Exact existing hold:** Valueless rel attribute aborts recoverable markup with AttributeError and loses later image links.

- Parent canonical SHA256: b064d4aec3a7de115990eab9116edbb5f8d63ab16722a01381ea7be991ba83ff.
- Prompt SHA256: d08e2c87d1765592c39b0d92d7fcccf71e0e84ab53a5f8c60760e8951f779337.
- Reference SHA256: bd7e11039e02a86ac3715e3ff1e4b63b1c6ce8f42cb3ae8afa567a41f5605198.
- Original test content SHA256: 937e3b0191eed70102940275686b1fd0d6ddf085900ad02a0e619430a5994516.
- Source row-08307, source-record SHA256: eee4b16d4bcac7bda70cfaa52ef1df926cab8afa15fe4bfec6997ea37fdb0372.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-08307","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"eee4b16d4bcac7bda70cfaa52ef1df926cab8afa15fe4bfec6997ea37fdb0372","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/preload-valueless-rel-result.json; SHA256 df9fb7b2ad70d1d83bedac6443cea24b6f42719101e8f6351409dfe79e4972b2.

## exp-v1-python-generation-0017

**Change class:** reference-fix.

**Concrete request / minimum correction:** Drain/wait every submitted ticket before re-raising the first failure in submission order; do not let the first failed Future terminate gather early. Retain copied submission arguments, stable result identities and idempotent shutdown.

**Contract-derived decisive tests:** Use two workers, an immediately failing first job and a second job gated by threading.Event. Run gather in an observer thread, confirm it has entered and cannot settle while the second job remains blocked, then release and join; at failure observation the second completion marker must be set. Propagate observer exceptions, release in finally and bound waits. Also two failures completing in reverse order must re-raise the earlier submitted exception.

**Contract decisions and whole-task quality:** No new concurrent-submit/gather snapshot semantics or cross-positional/keyword shared-alias requirement. Prior alias caveat is not an established contract failure: both graphs must be detached, while alias preservation across independently copied args/kwargs is unstated. Use ordinary deepcopy-supported values. No sleeps as sole synchronization or timing-performance oracle. Lifecycle, futures, ordering and ownership are substantive.

**Exact existing hold:** Gather short-circuits on first exception rather than waiting for all submitted work.

- Parent canonical SHA256: 723dca54f596a0ba0fd3a1b0a8c6b18d3a32c03e18ed64336c26b73c5850043c.
- Prompt SHA256: 55a17cb9a4a7c87fad53d875234e74dd0ad3e786a378489843369482713ee5ea.
- Reference SHA256: cb22d8d8a79cf8ddd9797cc930076b8c565d40ebb6739702b008043f4c82e3f3.
- Original test content SHA256: 0690c4228a42f907cbc8d63a3f62b85d059f7429b621496a8be03620e0262665.
- Source row-08337, source-record SHA256: 264fc64f9bca86a567470ab99e8af285724d0562b4deff83bf96ab2c015bd22f.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-08337","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"264fc64f9bca86a567470ab99e8af285724d0562b4deff83bf96ab2c015bd22f","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/PYTHON_GENERATION_REVIEW_2.md; SHA256 360318ea41b4990ca61dbcb0d96ae1ed53ea557c3f17bc0b3586568806cc4bce.

## exp-v1-python-generation-0156

**Change class:** reference-fix.

**Concrete request / minimum correction:** Use the provided logging.Logger whenever it is not None; replace truthiness fallback with explicit None handling. Preserve lifecycle validation, superclass-first audit hooks and immutable event snapshots.

**Contract-derived decisive tests:** A logging.Logger subclass with __bool__ returning False and debug recording messages must receive base initialization/start/stop messages; AuditUnit must emit corresponding base/audit pairs. None fallback remains supported. Verify invalid transitions produce no new events and hooks that raise do not advance state.

**Contract decisions and whole-task quality:** Do not test private _logger layout or unspecified transition return values; original tests do both and must not be copied unquestioningly. Use public event/log behavior, no global logging reconfiguration. Hook dispatch, state transitions and logging dependency identity make the entire task substantive.

**Exact existing hold:** Truthiness fallback discards valid falsey supplied logger.

- Parent canonical SHA256: 0c23e909c2ebad68f8ede1a958275f2556a147199fbef166e3dc9c443e8e64b6.
- Prompt SHA256: dd53aabfb665ded9b96d502ac5ceb89e2f3a4ee44c82890b27cdfe4a9f917cba.
- Reference SHA256: 04601ba54b2a9d8c36b51dc0437bc1f85f4d2bc8591d7e6375e62d926115fa36.
- Original test content SHA256: 1f4ce125d98892eb55a33152a6b149bd821c0b0561eece0e75b23418cd55b84c.
- Source row-08157, source-record SHA256: 002be561d743d0b170192022d03dfe040e83c1d56c16e7d9c87f25d8e36bffdb.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-08157","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"002be561d743d0b170192022d03dfe040e83c1d56c16e7d9c87f25d8e36bffdb","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/lifecycle-falsey-logger-result.json; SHA256 c68951cde49cff4f928d06d4b0ab72518787be5073f8d891526f547977d0a5f6.

## exp-v1-python-generation-0781

**Change class:** reference-fix.

**Concrete request / minimum correction:** Detach row containers independently before applying the overlay so a shared base-row object cannot cause a write to an untargeted matrix row. Retain rectangular validation, transparency and deep isolation from both inputs.

**Contract-derived decisive tests:** With row=[0], base=[row,row], patch=[[1]], top=left=0, expect [[1],[0]], unchanged inputs. Repeat with mutable base cells, transparent patch cells and mutation of returned cell contents; verify both inputs remain detached. Cover zero-width/empty placement and ordinary boundary errors.

**Contract decisions and whole-task quality:** No guarantee to clone deliberately uncopyable objects or shield arbitrary throwing equality. No need to require all result cells mutually unaliased, only input detachment and independent row placement. Existing zero-width semantics remain. Matrix placement, shared topology and transparent ownership are substantive.

**Exact existing hold:** Shared base row references cause patch to overwrite untargeted row.

- Parent canonical SHA256: e38611dd9c5e9d79c0ae6264ad5445cab62cfbafee1f652cba9dfe8243607df3.
- Prompt SHA256: 22f0c818bc8d999d1776bd5447344bc136cb8bfc51f675aa69e5e58b308fca74.
- Reference SHA256: cca7111f939b953fce593f5e75e830ccffa4948f15bba553f93b683cdeb589c5.
- Original test content SHA256: aa27af0ad4331ec51dbdb5979867bbd210a0131457d6194fe2c4ce293a1b10ff.
- Source row-08398, source-record SHA256: 2397dd65af3b9e0d7927b07b721090b7be7c3c50ab170213e14fdfac188fad3d.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-08398","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"2397dd65af3b9e0d7927b07b721090b7be7c3c50ab170213e14fdfac188fad3d","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/stamp-shared-row-result.json; SHA256 0086f494cc695c5a4b7a8142fbf9e90932428247ecb5b2a3440e349f499154dd.

## exp-v1-rust-generation-0012

**Change class:** reference-fix.

**Concrete request / minimum correction:** Distinguish an actual unexpected token inside parentheses from end-of-input missing closing parenthesis. Preserve checked literals/arithmetic, unary chaining and byte offsets.

**Contract-derived decisive tests:** evaluate("(1 2)") must be UnexpectedToken(3), with nested and invalid-character equivalents. Preserve "(" and "(1 + 2" missing-close controls; empty parentheses, missing operand, precedence, division zero and i64 boundary controls.

**Contract decisions and whole-task quality:** Do not add arbitrary cross-error precedence for expressions containing several defects. Literal parsing remains checked nonnegative i64; do not introduce acceptance of out-of-range positive magnitude merely because a unary minus follows. No new fixed depth cap. Grammar, checked evaluation and exact diagnostics are substantive.

**Exact existing hold:** Balanced parenthesized expression with an extra operand reports MissingClosingParen instead of UnexpectedToken at the offending byte.

- Parent canonical SHA256: 45578ce324c41c8bee44f0b9bd48f5184c0022494f0ab67265cdac2053b02886.
- Prompt SHA256: e7c6e0f5675d424679743bc779608c1fedb756484877786d65bb9a5ccc2d8c7e.
- Reference SHA256: 5209df71dd4f4395536d3608c63cc1731e2a69ada15d5ccc05ae9aaa2376cdee.
- Original test content SHA256: 5c9f753ec12e9c610d6e9d4f259b60e80ada5b95178ff74312da531dde3c566d.
- Source row-23670, source-record SHA256: 74e0892178c4208a92529ad7ff121ff460e9234a8652f3b295de27d18e13a0cd.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23670","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"74e0892178c4208a92529ad7ff121ff460e9234a8652f3b295de27d18e13a0cd","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/expression-extra-token-result.json; SHA256 f044fa5b6e2bf7b048875b9aade607c2427c5afcf7be8fbd3494f018d2c119be.

## exp-v1-rust-generation-0064

**Change class:** reference-fix.

**Concrete request / minimum correction:** Precollect model names for forward-reference membership without reporting later-name errors early; then validate each model name and its properties in input order, preserving duplicate detection and recursive Named validation.

**Contract-derived decisive tests:** First model First with property bad-name, followed by invalid model 2Later, must report bad-name. Add earlier nested unknown reference versus later duplicate/invalid model, and a valid forward reference control. Retain exact ordered output, optional complete-type wrapping and nested dictionary/sequence types.

**Contract decisions and whole-task quality:** The declared lexical identifier grammar is authoritative; do not add keyword rejection, compile-generated-text guarantees or recursive-model size rules. This task emits text according to the supplied grammar. Fresh tests must not demand more traits than explicitly declared. Ordered validation plus forward references and recursive rendering are substantive.

**Exact existing hold:** Validates later model names before earlier model properties, violating input-order validation error contract.

- Parent canonical SHA256: 3b3050e4e3e301fdadaaf3fd2d92ce3ce57b0e8e0067cb32112ed88a58adb9dc.
- Prompt SHA256: 77072b4f93d931a0ea22ed6b5bb574ebb5ac1c0a859f0418b3f929610f026d13.
- Reference SHA256: ab4afb2c071d0c87293586117951727fbba81ceaba47005de23f74c8159bc0f9.
- Original test content SHA256: 22780e873ca86b5212bfe3f9b96bdb6895801414260be1d162783deb1b00bd43.
- Source row-23794, source-record SHA256: 87494f452d3efe2333a2407b843683deaf960d7ad7a38585c5244925f2e26c17.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23794","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"87494f452d3efe2333a2407b843683deaf960d7ad7a38585c5244925f2e26c17","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/model-validation-input-order-result.json; SHA256 4e0428c358338868da344cf8ebbd45157900225fd56d317f60ba677518b3cf10.

## exp-v1-rust-generation-0071

**Change class:** contract-clarification.

**Concrete request / minimum correction:** Explicitly clarify that LF alone is framing and CR within an attribute value is literal data, then split headers on LF without CR stripping. Preserve the same public API, verb parsing, first-empty-line separator and independent binary/text bodies.

**Contract-derived decisive tests:** READ / followed by LF, key:value plus CR plus LF, next:kept then LF LF body must successfully preserve value followed by CR, not merely avoid failure through unconditional rejection. Test both parsers, duplicate/empty attributes, colon-containing values, binary invalid UTF-8 body and owned copies.

**Contract decisions and whole-task quality:** The old probe allowed either rejection or preservation; this proposal deliberately selects literal CR preservation, grounded in exact values and LF framing, and requires explicit approval rather than silently calling it immutable reference-fix. No CRLF alternate framing or extra general control-character ban. Use trait-neutral match assertions where traits were not promised. Framing, ownership and separate UTF-8 domains are substantive.

**Exact existing hold:** Accepted LF-delimited packet silently removes a carriage return from an attribute value instead of preserving it or rejecting the packet.

- Parent canonical SHA256: e2ceb1e16802116fff5a7b828b4a01b13ac7c996d841f293fdca978b0186610d.
- Prompt SHA256: 9f6d489d7630112bf92b57bbb50b74a2c328fee9f91c04e1669f918be077663a.
- Reference SHA256: 796201a2fa2a8e706ceb32add9d0c607149d7c2b860cf1cd5a875c331d4c64e0.
- Original test content SHA256: 9236b44d291f84bc7a523d043a63a935f867d52935ee3bdf982fe66d52a9e41a.
- Source row-05827, source-record SHA256: 70cd4c936746caf3958edcd46ad96d982d28dcb01f575a5b63799969bdef7680.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-05827","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"70cd4c936746caf3958edcd46ad96d982d28dcb01f575a5b63799969bdef7680","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/packet-attribute-cr-preservation-result.json; SHA256 6c7bb50d5be8d8273028a45a4df0811a91843a7bcf8c25ea3465888f74223779.

## exp-v1-rust-generation-0111

**Change class:** reference-fix.

**Concrete request / minimum correction:** Validate all proposed NoticeRule fields before assignment, including public id, channels and subject_prefix, not only patched optional fields. Preserve tri-state set/clear/retain behavior and stable borrowed ordering.

**Contract-derived decisive tests:** Create a valid rule, set public id=0, apply otherwise-valid expiry patch: InvalidId and unchanged public-field snapshot. Independently repeat empty channels and whitespace prefix; also an invalid existing optional value that a valid patch clears must succeed because the proposed result is what is validated.

**Contract decisions and whole-task quality:** Do not require RuleError Debug, RulePatch Default or NoticeRule Clone/Eq just because old tests use unwrap/clone. Use matches and public-field snapshots. No imposed priority for multiple simultaneous invalid fields. Transactionality, three-state patches and borrowed stable ordering are substantive.

**Exact existing hold:** Update accepts an invalid public ID rather than validating the entire proposed result before mutation.

- Parent canonical SHA256: 42d67460786da429421d42ac674375082c1cedd18823e1e323eb0b9a903eaed2.
- Prompt SHA256: 1060062f0cd123e7e9ffc62f6fa76fb5893539e1aacb621da2fd3a0859f8b502.
- Reference SHA256: 720420c227e306f3c319b1d00daa9e23657b6a07e5ae10596c48682134e1a448.
- Original test content SHA256: 57217b37fc4a6f17aac323c35af526bd31c75b1386ee57d3ed5dd6b40daadda3.
- Source row-05889, source-record SHA256: 9634d380340030a875384b7bb095738072a6fb2940c7d961b227f25e00f67e4d.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-05889","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"9634d380340030a875384b7bb095738072a6fb2940c7d961b227f25e00f67e4d","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/notice-entire-result-result.json; SHA256 3f8a4011d4bbcc4f99891401fd90f222dcc98eb460a2f93b28386235fdbe02ec.

## exp-v1-rust-generation-0133

**Change class:** reference-fix.

**Concrete request / minimum correction:** Remove the extra Self: Sized bound from ByteSource::read_until while retaining the specified generic FnMut contract and streaming state.

**Contract-derived decisive tests:** A helper fn with S: ByteSource + ?Sized must call read_until; invoke it on SliceSource(b"aa") and require Ok(2). This is a legitimate API compile witness, not a source-text inspection. Retain pair callback order, previous-output exclusion, partial bytes preserved on exhaustion and untouched destination tail.

**Contract decisions and whole-task quality:** Do not require dyn ByteSource object safety: a generic method is not object-safe, and that is unrelated. No new SliceSource traits or offset fields. Generic trait usability plus streaming state/exhaustion are substantive.

**Exact existing hold:** Adds Self: Sized restriction absent from the declared generic ByteSource read_until contract, breaking a ?Sized generic caller.

- Parent canonical SHA256: a5d5a5f77d58df7ba21dfecff01cad4d33b51dfb5c3071c1b5244cc1f4fdf531.
- Prompt SHA256: 1d5915fa31f27d85dcb89ca7cd602d16d1b7a58562ca9e2a1ef6e0517c445631.
- Reference SHA256: f26c51aec3309f6e951180aad686c92cd8fada591ffd01421602e6a79d565d7d.
- Original test content SHA256: ed1d9221193fc2b6af0afaecf3b1050cbeb65ea5e9dc15e802e37ce1b5a7e137.
- Source row-24062, source-record SHA256: d24006f2762b121aefa557c9d27062901fb424490625908062d9e4d96f22f9c0.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-24062","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"d24006f2762b121aefa557c9d27062901fb424490625908062d9e4d96f22f9c0","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/byte-source-unsized-result.json; SHA256 19a774438feb115a99c549b7030dfdd05669056444b67373408ee603fdd422f3.

## exp-v1-rust-generation-0342

**Change class:** reference-fix.

**Concrete request / minimum correction:** Replace Unicode trimming on key/value-bearing paths with the named char::is_ascii_whitespace predicate. Preserve exact-one-equals parsing, required/unknown key handling, duplicate detection and owned literal values.

**Contract-derived decisive tests:** U+2003 around label value must remain in the returned String; U+2003-prefixed code is an unknown key and cannot satisfy missing code. A valid code plus that unknown key is accepted; duplicate unknown keys still reject. Keep ASCII tab/FF padding controls and literal values.

**Contract decisions and whole-task quality:** Do not accidentally include VT in Rust char::is_ascii_whitespace; use the named predicate consistently. Do not add a new rule for Unicode-only blank lines because blank-line scope is not needed for the witness. Exact error strings remain unspecified. Interacting lexical normalization, duplicate tracking and required-field validation are substantive.

**Exact existing hold:** Unicode trim removes literal non-ASCII whitespace and treats a non-ASCII-prefixed unknown key as required code despite ASCII-only trimming contract.

- Parent canonical SHA256: 9130d034eb347f9d19e8bc8c67f68b7c018b6f6e6d4ee2a3cdc22b4997652634.
- Prompt SHA256: cfc34b2f401dcb7dcac891b908e006ebf8d55ba67e56f6ce4985f7f7a9f9e716.
- Reference SHA256: 5d53db9ba1640224a23c2804951892debb2a8439130c2845d5db0b2f01a745a3.
- Original test content SHA256: 4e269c6d7f5fa85d5839cfb8c27db49bc1b87eccfe764f510539a72e2c5a1c53.
- Source row-23810, source-record SHA256: bd320d0d81e852d74fc42a3f595ccf4779d6532d470f21a9a9ae0a46daa3c4ac.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23810","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"bd320d0d81e852d74fc42a3f595ccf4779d6532d470f21a9a9ae0a46daa3c4ac","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/profile-ascii-trim-result.json; SHA256 4dcf80b2b51d7d8b1b7d23a5b5b6b4cd7de87c9a378a0ddf13bb32dacd319b9d.

## exp-v1-rust-generation-0414

**Change class:** reference-fix.

**Concrete request / minimum correction:** Finish ordered entry validation before returning any conflict, either via a first validation pass or deferred conflict marker. Preserve EmptyKey priority, first malformed index and ASCII-only matching/value trimming.

**Contract-derived decisive tests:** Entries [("key","first"),("KEY","different"),("","bad")] queried by key must return MalformedEntry{index:2}. Add multiple malformed suffix entries requiring the first, valid-only conflict, repeated equal values, nonmatch and detached output controls.

**Contract decisions and whole-task quality:** Keep existing interpretation that surrounding ASCII padding is trimmed before interior control rejection; do not reopen raw-padding policy. No new Unicode casefold or exact allocation/algorithm restriction. Complete validation versus conflict resolution is the substantive interaction.

**Exact existing hold:** Early conflicting-value return skips later malformed entries despite instruction to validate every entry and report first malformed index.

- Parent canonical SHA256: 967630134b4366dd6f569a3c43333edca71f3912974b87248f183a157041d60b.
- Prompt SHA256: ff7e586ef0f78c6ffe5ea1a6ef4073cce4a295ceeb4baecf7b9e8ce371fd5124.
- Reference SHA256: fbc9d845901b84dccb0b79fc08537a565005edba6b996ca96e72ee3f2a5bb21d.
- Original test content SHA256: c790849598f1044ea54a6da41832be2df637f2da3b175769e27e207ac416d9a3.
- Source row-23808, source-record SHA256: a3bd7801d03dd4ee5860d6223ca12f96388eb694a2b821f77e6e44493fb29417.
- Source dataset URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI: https://creativecommons.org/licenses/by-sa/4.0/.
- Complete source object: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23808","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"a3bd7801d03dd4ee5860d6223ca12f96388eb694a2b821f77e6e44493fb29417","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights object: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold evidence: measurement/data/expansion-v1/cutoff-5885-review/lookup-full-validation-result.json; SHA256 04921800da0274e66e717c225d2053184da673ec83b45deba39b313efd68beec.

## Inspected but not proposed

These nine are not new dispositions and no central hold was changed:

- Python0073: mostly independent scalar validators/formatting helpers; locale-independent month parsing alone does not justify padding the substantive tranche, and numeric-season spelling remains loosely stated.
- Python0028: empty format-spec detection has a clear witness, but arbitrary integer rendering under the pinned decimal guard needs a separate exact contract reconciliation before a coherent narrow request.
- Python0666: leaf/text/tail checks are clear, but whole-task XML generation accepts unrestricted strings; XML-invalid characters and comment/processing-instruction treatment need an explicit cohesive scope rather than a leaf-only patch.
- Python0678: zero-length barrier is real, but finite Real validation and writable endpoint state add unresolved numeric/malformed-state boundaries.
- Python0774: range endpoint support is real, but finite arbitrary-size coordinates with required float cost introduce a separate numeric representability policy. A sequence-only patch would not close the task.
- Python0790: generated layers are predominantly a fixed tuple template and direct exponent formula; do not add elementary volume just to reach ten.
- Rust0087: macro expansion is primarily a fixed struct/impl template, and broadly forwarding arbitrary outer attributes to an impl is not a coherent blanket repair.
- Rust0142: removing the hard-coded path is necessary but insufficient: public i32 boundary cells make neighbor coordinate arithmetic unrepresentable without an explicit boundary policy.
- Rust0235: last-clone drop race is substantive, but a black-box bounded simultaneous-drop stress test does not deterministically schedule the exact strong_count window. Keep out of this tiny-decisive-witness tranche rather than infer success from a probabilistic pass; a separate concurrency scope may be worthwhile.

## Reservation-exclusion evidence

- datasets/cache/expansion-v1/versioned-recovery/r1/plan.json: a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1.
- datasets/cache/expansion-v1/versioned-recovery/r10/plan.json: 728e70ee23ad46f8a4a8aec64a34d74b48c073a5382849fc52ce449154f2afb5.
- datasets/cache/expansion-v1/versioned-recovery/r11/plan.json: 2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6.
- datasets/cache/expansion-v1/versioned-recovery/r12/plan.json: 0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121.
- datasets/cache/expansion-v1/versioned-recovery/r13/plan.json: dead1489bb779934327bf3c8786d89c65b7604832829fa17129ea41ff1773217.
- datasets/cache/expansion-v1/versioned-recovery/r14/plan.json: 2d59789fea811ba7ebe844564ee4dc66569fe4719067dea6d6a1524b049ea51f.
- datasets/cache/expansion-v1/versioned-recovery/r15/plan.json: d2e65ef33e2c70162a53315e3daec75ebe1e3fbc1a7098e8635eddacb348c100.
- datasets/cache/expansion-v1/versioned-recovery/r16/plan.json: efd902abc4ed3e00d6639c74f7d2ec95e6f153d1aa19a70a460aeb553dfb6844.
- datasets/cache/expansion-v1/versioned-recovery/r17/plan.json: 60c02db8869c80c1515e2216205ac11a45b357206563f62f499d8b67b3ee02ee.
- datasets/cache/expansion-v1/versioned-recovery/r18/plan.json: 512e3219da55465742728f2c5116840498e4a41c5a2bfe8f5b0130d9a19690a0.
- datasets/cache/expansion-v1/versioned-recovery/r19/plan.json: 401d56a11f2ca2929eb42be7ffb36fe694cfded2500ed56a96759560b8b65f62.
- datasets/cache/expansion-v1/versioned-recovery/r2/plan.json: 5dae7eac34ac462f6173dc6b740364d5c4b68129950359f453f4038111ad1d29.
- datasets/cache/expansion-v1/versioned-recovery/r20/plan.json: 879eb4184b49e09a171cbe35592096a296d9d2af6e1e52eea68315fb6b7eb224.
- datasets/cache/expansion-v1/versioned-recovery/r3/plan.json: cbad9d14a504531e749b5eb3433f0bf4670e21f2a8e8d5f310d2e843e53c6231.
- datasets/cache/expansion-v1/versioned-recovery/r4/plan.json: 8a6137773e65e1a55e5eaceed9a8c2e40153b5759a46a5189ba6a488d530d58c.
- datasets/cache/expansion-v1/versioned-recovery/r5/plan.json: 778e0071bec56248081e741f4c742d522c75b4b006e069d8301b75440c2732ec.
- datasets/cache/expansion-v1/versioned-recovery/r6/plan.json: 803f0308b33b4b8a834347d5976a148bc66001d6fc8606a1e206fb0e2b4a6795.
- datasets/cache/expansion-v1/versioned-recovery/r7/plan.json: f0a3b5d14eb983206ac83c99571c5522925feaf7ac0443ec3c59ad172d5f293e.
- datasets/cache/expansion-v1/versioned-recovery/r8/plan.json: 1a579af9da9d542d6bb4f03c8fbc030fd0b9d3102a31c347cd631bfc18b873de.
- datasets/cache/expansion-v1/versioned-recovery/r9/plan.json: 0f0d6e653bbabff308a912cc764d1373b20faf3f4cf68a4c7341c94f36b5ae79.

