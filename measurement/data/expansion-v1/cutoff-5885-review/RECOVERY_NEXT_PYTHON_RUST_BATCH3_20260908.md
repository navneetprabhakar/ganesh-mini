# Next Python/Rust recovery selection, batch 3 — 2026-09-08

## Recommendation and boundary

Recommend **13 fresh held generation parents: seven Python and six Rust**, in the order below. Explicit shortfall against the requested 15+15 ceiling: **eight Python and nine Rust (17 total)**. This is a bounded accelerated screen, not a claim that the remaining corpus contains no recoverable candidates. No elementary padding or compile-only controls are proposed.

Gate 2. Only this isolated proposal is written. No requests, reservations, generation, candidate execution, admission, cloud operations or central state changes. ZERO new original-row coverage credit. Complete original prompt/reference/test/source/rights reads and exact held diagnostic reads support every recommendation. Existing diagnostics are historical evidence, not fresh runs.

Original corpus: datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl; SHA256 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
Hold ledger: measurement/data/expansion-v1/cutoff-5885-review/additional-holds.json; SHA256 9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee.
Exclusion: all present r1–r23 plans contain **153 distinct reserved original parents**, none overlaps these 13. All 13 remain held; each evidence candidate hash equals the freshly computed canonical parent hash. Repeat exclusion immediately before reservation because concurrent work can add plans.

## Seven-criterion conditions

All recommendations use reference-fix with byte-unchanged original prompts; independent tests must be rebuilt from the approved specification, never from corrected-reference or mutant code. Python0143 also removes a demonstrably unsupported original test oracle; Python0588 includes a second concrete per-ID isolation correction, explicitly disclosed below. Source/rights are copied intact with new versioned lineage, never inferred from an answer. Original mutants/tests are not sufficient admission evidence: derived full-quality review, valid whole-contract tests, resource-limited network-disabled reference passes and behavioral control failures remain required.

The seven criteria remain: independent tests, appropriate language/standard-library use, complete specification, no test accommodation, substantive whole target, correct reference, and meaningful non-overconstrained verification. Current original references fail correctness by design of this proposal; no original is declared admission-positive. Proposed witnesses are contract-derived, input-bounded and compile-compatible. There is no score/coverage credit for simply finding a small patch.

All selected source records are from McEval-Instruct revision 57bd46727e49ac3e2890218a146d35c2454a8496 with recorded CC-BY-SA-4.0 license and all five recorded rights true. Full binding objects below preserve transformation histories. Canonical object hashes use sorted compact UTF-8 JSON; content/file hashes cover actual bytes.

## 1. exp-v1-python-generation-0047

Change class: reference-fix.

Minimum scope: Validate change/remove IDs before dictionary lookup; preserve exact schemas, sequential position-preserving edits and caller atomicity. This is a reference-fix, with original prompt bytes unchanged.

Specification-grounded tests: For each of change and remove, supply id=[] and id={} in otherwise correctly shaped operations and require ValueError, including after a valid prior operation; compare both input snapshots after failure. Retain add/change/remove interleavings, duplicate and missing IDs, order and independent output rows.

Contract and quality decisions: Ordered state transitions, validation and ownership interact; this is not a fixed CRUD output template. No private positions/index representation or new exception priority is required.

Exact held reason: Unhashable change/remove IDs raise TypeError instead of ValueError for malformed operations.

- Parent canonical SHA256: 2cb4ead62e781964c6e88bddaf9b8fb1715a12462cf54b85b15971177469a32d.
- Prompt content SHA256: d6892f718c3336700d57051d877bff74ea26c7b8185aa9a562d8b8b7129dcf1a.
- Reference content SHA256: e90e60a7da71a87aff54d21c0e8bf4bf6863a74726aa59af962ae65588e23674.
- Test test_solution.py content SHA256: 6d037bcb686128efa3440f5d2c0175d5405d96de6ccbb2ce1b51232191ab1605.
- Source object canonical SHA256: 469f8f56e0895552f2dec88684f6de1747a2114710cc6b5eae14a477e67d09a2.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-04253","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"be82bf2e5d67d65b36948ac33d203957c88358b6f978a94cc634d28c4faf6f45","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; independent tests strengthened after rejection","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: cf6718000ea9f81dec34ed96afc7a9b2a462f9675a53688ac110aad18491daa3; evidence measurement/data/expansion-v1/cutoff-5885-review/registry-id-validation-result.json; file SHA256 df05b4c2b6eaad38345ae1da0e1e979978af04e9a2abc621f9f60bbd413796c8.

## 2. exp-v1-python-generation-0130

Change class: reference-fix.

Minimum scope: Validate reservation event_code before membership lookup so malformed unhashable values raise the specified ValueError, without altering dual ordered projections.

Specification-grounded tests: Use one valid event and an otherwise valid reservation with event_code=[] or {}; require ValueError and unchanged inputs. Keep duplicate reservation retention, unreserved labels, first-contact order and independently allocated projected rows. A valid fee and party_size above machine integer ranges remain valid integers; do not add float conversion or arbitrary caps.

Contract and quality decisions: The two differently grouped, differently ordered projections and duplicate preservation are substantive. No error-message or simultaneous-error priority contract is invented.

Exact held reason: Unhashable reservation event code raises TypeError rather than malformed-input ValueError.

- Parent canonical SHA256: 167118c9169c84eef1c6639a2dca6da947188164e24dc42f821bac7413591faa.
- Prompt content SHA256: b2c698eb76869a72dc6d6f6d57e02f3cc7d2e01f7527201795cd76435ace8610.
- Reference content SHA256: e23a6f2c4ccd553132e395fe0c6c4799e3423e84458065dfbebcad67b8fb690b.
- Test test_solution.py content SHA256: 40c01e93605442ffd22bbdd096087c0be6d9eabc5e2cf48297014fae92c37c0a.
- Source object canonical SHA256: bf247d5511be53865a925cee500382269201d744151fce41ffb994aefe9a8cab.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-08412","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"7825b6147e1ac20d4a4478dd90f700f6f7db7e73bfa5f60406af89750ad8b4c8","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: a9d2ed3d36c2c8fab01fcc8e2bde7adb0a7680b14894aa29f80f2be5cf0f1bbb; evidence measurement/data/expansion-v1/cutoff-5885-review/reservation-code-result.json; file SHA256 bdf229df7f731c2423182a34aa979d37e4ca8086c8e96a8579668ac7a299c335.

## 3. exp-v1-python-generation-0143

Change class: reference-fix.

Minimum scope: Remove tuple-scalar get fallback into the distinct list/set normalized key. Also honor the explicit membership-change return contract: adding an empty collection to an absent key creates the bucket and marks dirty but changes no membership, so returns False. Keep add_empty's separately specified creation boolean.

Specification-grounded tests: After add(['a','b'],1), get(('a','b')) must be empty; then add(('a','b'),2) and prove both buckets remain independently addressable/removable with dirty/no-op semantics. Replace the original invalid assertion get((10,2)) after adding {2,10} with get({2,10}) or get([10,2]); a tuple is a scalar, not a normalized-key escape hatch. Add the absent-bucket empty-add False/dirty=True case and subsequent add_empty False.

Contract and quality decisions: Reference-fix with unchanged prompt. The original tests are not authority over normalization. Stateful membership, atomic hashability validation, dirty tracking and immutable snapshots remain substantive. Tie ordering of distinct equal-repr objects is not newly specified; use ordinary distinct repr values.

Exact held reason: Tuple scalar lookup falls back to distinct list-key bucket contrary to normalization contract.

- Parent canonical SHA256: fe8de50d87bfa45afc0930c7ebc31f161fc235701345dc539925c5ab3230cc76.
- Prompt content SHA256: f7a9e5b7b8460420d9ea23391d90a858f0632c2b53355ef9b319c6c443e870e4.
- Reference content SHA256: 11d205fa55d32730ef1ca228af1696f3a9858e0886444f5fef52c10004d83521.
- Test test_solution.py content SHA256: 613cb1a52e3004bcea6cf05abc9da31354443390a7577e2a2f7b67a00d6c43b0.
- Source object canonical SHA256: 884d63d0741640100c1a704f20e50f0c60ccceaca0fffb7e52d9641e74dc7144.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-04154","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"f28f6e822fd9d6809694e0302ce62f2ff740545d6e285a2f314f1630cdd1f655","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: ed0f37e93190bcba0c808156b9f3cae1008e87e39260c7235866a9065dc90b63; evidence measurement/data/expansion-v1/cutoff-5885-review/relation-tuple-key-result.json; file SHA256 669e6212d84f0dc72b72cd451031cbf4a311d8bfab2acc567f5d6eeef218ef3a.

## 4. exp-v1-python-generation-0153

Change class: reference-fix.

Minimum scope: Validate asset key types and nonempty values before lexicographic sorting; preserve mapping acceptance, handler identity, ordinary-route order, asset-name collision checks and immutable Route values.

Specification-grounded tests: Mixed asset keys {'/x': handler, 1: handler} must raise ValueError, not the sorting TypeError, in either insertion order. Include MappingProxyType assets with ordinary valid string keys, sorted after ordinary routes, and cross-origin name/path collisions. Check callable identity and input preservation.

Contract and quality decisions: This is interacting schema/order/identity validation. Do not impose a private route registry, undocumented constructor coercion or arbitrary callable signatures.

Exact held reason: Mixed asset key types sorted before validation raise wrong exception.

- Parent canonical SHA256: cfc2316132c8a8c1aaf44d55f7fb35c230384ef0e97262ad362d14101870c4a8.
- Prompt content SHA256: 26f58c6c7ab9feb13c4475da23cc5ea5de4ed3ada3f6b688deadd67e23f84117.
- Reference content SHA256: b6f08ce6fcffe4cc3af3484bf3c54c11228820f097aa5c3bf87e76882c5de3ae.
- Test test_solution.py content SHA256: 2a697f2e94f629bba72fe5fa4248f16d9655e946f8b0496755765ad7f216f1b7.
- Source object canonical SHA256: 541f35c44546a778844892e1f035c8260932afdbee2f66e5aa3253b53c46271d.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-08548","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"37eca3ee52c4b38bfbffe75acbc4f322ed6daeeb146e599e5fb1dda619d38eba","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: ed9ed155115cf8f7fd97d4092eaa9ddb950fdf1b0a41a2b2f96a0b03314e59c8; evidence measurement/data/expansion-v1/cutoff-5885-review/routes-mixed-asset-keys-result.json; file SHA256 20c31d8d74ed63e8b76e02a39ded3ef59ee73f6b235008e36b87905a1b481dda.

## 5. exp-v1-python-generation-0159

Change class: reference-fix.

Minimum scope: Parse the first whitespace-delimited command token rather than splitting on literal space only. Preserve the unmodified internal argument text except surrounding whitespace, lowercase handler name, dependency identity and no sends for unknown commands.

Specification-grounded tests: Dispatch '!repeat\thello' must return True and send ('user','hello'); also use newline-separated command text and mixed surrounding whitespace while preserving double spaces inside the argument. Test unknown command followed by a tab produces no send; a subclass public command handler verifies generic dispatch, not just a hardcoded repeat special case.

Contract and quality decisions: Dynamic method dispatch, dependency identity and handler/connection interaction survive the correction; not merely changing a canned reply. No requirement on private helper layout or implicit string coercion.

Exact held reason: Tab-delimited command not recognized by literal-space partition.

- Parent canonical SHA256: 7a332974a4a89fb69754960d860ca42f072c75c60ac17127257d1dbba7f03400.
- Prompt content SHA256: 1483d06381da41d4566c4d861fbb75003a4f59cce44c5bc547b3768009e0f7d7.
- Reference content SHA256: 3509d978faae9500b24c18a4d46197986e83a7ac839f3aa1cb9e71737feb07c8.
- Test test_solution.py content SHA256: cdbeec039d7bf58fbd81413ffd24e0cc4d21404d4e85fcb776018705d89cbb5c.
- Source object canonical SHA256: 7f6c859c35cf66694c96afd80d63e172382a0c15d7bf96ade856bf3486dbc571.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-04123","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"5a198c17ffea276c814341dfd02b99b2fff90b517b495d1fd911892822a6548d","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: 846d1742820dbfd25aeebe2c43309e438152d1a08e2696904806fdbd67bf269e; evidence measurement/data/expansion-v1/cutoff-5885-review/dispatch-whitespace-result.json; file SHA256 3087fef01cde9e42063409672ba84ad900600c793f87df64c9f62ea02006f361.

## 6. exp-v1-python-generation-0588

Change class: reference-fix.

Minimum scope: Validate operation discriminator type before hash lookup. In the same derived reference, detach each independently addressable book record before a move: one shared source dictionary bound under two book IDs must not move both. This closes the additional concrete ownership/operation interaction found in the full read.

Specification-grounded tests: Require ValueError for op=[] and op={} without caller mutation, including following a valid operation. With categories {1:'One',2:'Two'}, shared book {'title':'B','category_id':1} stored under IDs 10 and 11, move_book id10 to2 must leave id11 at1 and caller at1. Retain referenced-category deletion rejection, later-failure atomicity, sorted IDs and all six operations.

Contract and quality decisions: Minimum coherent reference-fix covers malformed discriminator and ID-targeted move isolation; this is not a claim of newly executed shared-book evidence. Do not require preservation of output internal aliases: per-ID operation semantics require divergence when only one ID moves. No extra category/title normalization.

Exact held reason: Malformed unhashable op raises TypeError instead of required ValueError.

- Parent canonical SHA256: ca29b3df2e7307a0f1ca72e4e4e57f89a9dcb8f0b589ae4c223bdae3f7b95fef.
- Prompt content SHA256: 0802b23ea3ad91689f33c1edb3bdbdd6d55109ef87c0cf4f1ab27ef1e2a4f08c.
- Reference content SHA256: 4bbc6639ad9e76b912b89d1e0c2117c4f1a8a15e6ee3ec9386f7e839dccf643b.
- Test test_solution.py content SHA256: 3b465a0efd2bca015eb2bfb2255b48d5f52f82997440cac96560267abbc815d8.
- Source object canonical SHA256: 1ca0a04c908a4eca20b6cc06e477bab2281e6be95e971aeb3417ab3ac3121a67.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-08414","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"11870823b72e93d6cfa893ae6a77d9d5a1eebf97b948d2d554edce85a8e89157","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: f1c8bb1125d020fc2a5182721c5a0e2942c8f66501e8b53eee5471f5916f8ba2; evidence measurement/data/expansion-v1/cutoff-5885-review/library-operation-result.json; file SHA256 3710be053de2a2720372dfb2e12e4ff966ca3f1b7c423c0a74c0421d4d48c0ea.

## 7. exp-v1-python-generation-0738

Change class: reference-fix.

Minimum scope: Detach the selected account before replacing its email so a shared account object at another directory key retains every original field. Keep output selected object identical to result[key] and deep detachment from caller values.

Specification-grounded tests: The same ordinary account dict under keys a and b, update a.email to new: result[a].email=new, result[b].email=old, input shared account unchanged, and selected is result[a]. Include nested lists and preservation of password/username/extra fields plus new-account control.

Contract and quality decisions: Targeted update isolation, branch behavior, deep ownership and exact return identity are the substantive interaction. No wholesale ban on ordinary shared inputs, no demand that unrelated output aliases preserve identity, and no custom deepcopy-hook domain.

Exact held reason: Shared account references cause selected email update to alter another directory key.

- Parent canonical SHA256: e23b7270f5b8e9988a062f204d40dae6d70a02e52b2f77b88bae0b6862b8c3e5.
- Prompt content SHA256: 826f1794e88ba7756095ab87917abe2d9f45239daf21d4630fb9dfcbb1e1fe45.
- Reference content SHA256: 69a358e79d9e0255ba5b6e55e568c3a5a5afc099e4048438f8ae2e582da43ae2.
- Test test_solution.py content SHA256: b70c916f920b45fdfe4ec67297fae5bb9062ef6199f2ef04036d469580cf3cca.
- Source object canonical SHA256: 96720a8cfb6d804e89e58cfa96dee10c7a0fac4b69beec97816e82a5c55c8c3d.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-04230","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"7d779fae999c6f2ca280fa6020b0acf0e751563c4c09dbfefe14e34350e22182","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: 146a59a3def3514529324408c7ab5f045a9bb85695faa050c03d5c9f3f96d2df; evidence measurement/data/expansion-v1/cutoff-5885-review/identity-shared-account-result.json; file SHA256 a42f85fb25ae4a1cc3d26706c7f57eddb445a2a13e4951d28c5752a914b767ed.

## 8. exp-v1-rust-generation-0465

Change class: reference-fix.

Minimum scope: Replace Unicode trimming with the explicitly required ASCII whitespace predicate for all four fields, capability names and the empty-capability-field check. Keep factory state and duplicate detection over corrected literal identities.

Specification-grounded tests: U+2003 around ID/title/revision must survive, and a capability field consisting of U+2003 is one nonempty capability. Distinguish 'read' and U+2003+'read'; duplicate exact capabilities/IDs still fail. Keep space/tab/CR/LF/FF trimming, order, descriptor ownership and independent serial sequences.

Contract and quality decisions: Nontrivial parsing/duplicate domains plus stateful factories. Use Rust's named ASCII predicate correctly; VT is not included by char::is_ascii_whitespace. Do not mutate private serial state or impose unpromised Debug/Clone traits to reach u64 exhaustion; checked private overflow is static-review evidence only.

Exact held reason: Reference uses Unicode trim for fields and capabilities despite explicit ASCII-only trimming; diagnostic confirms literal U+2003 removal.

- Parent canonical SHA256: b173a6e93f316bebe8bf35cd4a78ce9823c8cee54bff10c80fd177d5341902b4.
- Prompt content SHA256: fd15aa529282bdcac026b22b4581ca27679c1527d6fab4d6a661b3156d0791d2.
- Reference content SHA256: b2281e93dd6e8b7728202ed38a8f63450590d51d96e89714eaadbfdd92985cb0.
- Test solution_test.rs content SHA256: 4f0e50a63a994de96275a21aede288845e5f84568cc3d9023e19ece87337812c.
- Source object canonical SHA256: fe3ca8fe2ca43e2f80051455e47f583188fd82f53149164a6d287a14315f8c22.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-05930","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"f0c1f04844801de4135c23227d857bea37573b97b2e9103da70c7fab30047306","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: 0b627d1878dc23a0fa4dc0fc98900ab6b5026d163f185e8677c33e2a5d3372e0; evidence measurement/data/expansion-v1/cutoff-5885-review/extension-ascii-trim-result.json; file SHA256 edf21f1d20bce0faae2d4cb8443b08bf376d4043d824f5a116946ae25d5db281.

## 9. exp-v1-rust-generation-0553

Change class: reference-fix.

Minimum scope: Use ASCII-only trimming for the full repository and each component. Preserve ASCII-only case conversion and the normalization-to-authorization decision chain.

Specification-grounded tests: U+2003+'Org/Repo' normalizes to U+2003+'org/repo', and a policy authorizing 'org/repo' does not authorize the Unicode-prefixed spelling. Test Remember stores the literal distinct repository, Once does not mutate, already-authorized bypasses Reject, and ASCII aliases still deduplicate.

Contract and quality decisions: Identity normalization, policy mutation and decision precedence are substantive. No URL/Git hostname grammar, Unicode casefold, or production-security guarantee is added. Keep the stated exactly-two-components rule and correct Rust ASCII predicate.

Exact held reason: Unicode trimming changes repository identity and authorizes distinct identifiers despite ASCII-only normalization contract.

- Parent canonical SHA256: 31a9d66e2b3e01423477aba5a5caba8d2bd3d34092a03b0b5886224b3dff009e.
- Prompt content SHA256: 0b58ae63839af0126727137b81d0de54eed33318a7dcad5db3ae3b65185aeb94.
- Reference content SHA256: b33728d423a41be7e33b059dfb7cd928c0f2ebc6eab6abb197e5403bd6d1a8b0.
- Test solution_test.rs content SHA256: 7dd634e574dc4fa967ea1ddedb6ccd0131126634f9ed2daea3c4603d88d6eab8.
- Source object canonical SHA256: 6ae2a970da8e722c509a4b5e4f0c26cc0aeb42e0486793ac7234b135f696ca40.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-06079","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"40fab23acb6a83c25c5c3b4907d2920fc35535017a31aa90ada12404d799d8f8","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: 140eeca030d10486548bfdc7383260279beec824b74f52f8d6c8d2f81e7e195a; evidence measurement/data/expansion-v1/cutoff-5885-review/repository-ascii-trim-result.json; file SHA256 be002053a57922f019b5ffe7735488bf6fa1be029a795419afaba9009e5bfe26.

## 10. exp-v1-rust-generation-0595

Change class: reference-fix.

Minimum scope: Complete JSON string escaping for U+0000 through U+001F in all three rendering APIs while preserving map/vector ordering, locator grammar and source-node behavior. The existing explicit common-escape list is not permission to emit invalid JSON.

Specification-grounded tests: Use NUL/backspace/form-feed and another unnamed control in string list values, string-map keys/values, and list-map keys/nested values. Require compact valid JSON with exact decoded original strings and no raw controls; allow valid equivalent short or Unicode escapes rather than inventing one spelling for previously unspecified escapes. Preserve ordinary quote/backslash/newline/tab tests, external incoming edges, self edges and stable source-node deduplication.

Contract and quality decisions: Graph membership/order plus nested serialization and locator validation retain substantive whole-target work. The independent test may include a small test-only JSON string decoder for equivalence; no external crates or matching a reference helper, and no lossy deletion-only oracle.

Exact held reason: Reference emits raw JSON control characters in rendered string list.

- Parent canonical SHA256: f3f8b4a41e9eaf9b22b1f99acd3e6959b113ab521f44623d200e30fada2af351.
- Prompt content SHA256: 0241b8139ff1d245c2bef482884d695f77accdf0f05f854cdb680b9d6cf178d3.
- Reference content SHA256: bbf04444ff8f1a3d08d914ba434348f7fd5a80ec421f69500c2dade0f310b6d7.
- Test solution_test.rs content SHA256: f83cf13a7a174777b4d89fb324388c6a53b57e746a2f3a3eae4d364650f21876.
- Source object canonical SHA256: 05b8d493679affbf5d39639f52224143b0a599688e19138b1b21c78f65a2435f.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-03350","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"1c10784234a8059c556b9f66c5ccfbd38f3009f3a6e14276acc6e3a36a0220f9","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: b169fb62c4f39ef5f4b237aa83cb4e3a73231180811748b80f9c97c780750b69; evidence measurement/data/expansion-v1/cutoff-5885-review/json-control-render-result.json; file SHA256 f5552c33da03790a8d67a5ecd85b56fbff77290310c65a8068b12a9c7e22db53.

## 11. exp-v1-rust-generation-0606

Change class: reference-fix.

Minimum scope: Complete JSON escaping for controls in document names, entry keys and values. Preserve line parsing, first '=' split, later duplicate-key replacement, sorted cache objects and sorted unique u64 IDs.

Specification-grounded tests: A document named 'doc'+NUL with body containing a key with backspace and value with form-feed must produce valid compact JSON decoding to the exact original name/key/value. Include control-free sorting/duplicate-key/extra-equals tests, malformed physical lines and u64 boundaries. Do not put newline inside a single entry key/value and then demand it survive line splitting.

Contract and quality decisions: Interacting nested document compilation, grammar validation and ID deduplication are substantive. Equivalent JSON escape spellings are accepted; do not just assert absence of raw controls, which would allow dropping data. No new cross-document error-priority or framing contract.

Exact held reason: Reference cache_json contains unescaped NUL/backspace in document names and values.

- Parent canonical SHA256: a6e10b1e0e7f74755c3681f5b12cfa5a3cc290aefa8d1fe6e0c25854bb5e5bd3.
- Prompt content SHA256: 302fd793da516d12d6ecceabf36622ed6a6b8198cede30683a3cdc8b2341d66b.
- Reference content SHA256: 45691d49f78917587298dcf7945a262459441f021415e7c3ef0e12f5aede4156.
- Test solution_test.rs content SHA256: 87fb0f8d496a0badc966af133934ea37268f342c93a05a5b35f863765ae9873e.
- Source object canonical SHA256: 8c94bb8ea2fabaa16744688368ece1d9d01ec850e9860a4d09cbaa9a81069e84.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23786","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"dc32b9a2fa6123a0cde397c4c947498cc484680b68c6ab2f9a498e27d1fe20aa","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: 0f0203c7271f7ee1b62ef078c3185c3a5e9b30645747bcc497be0213c65443e9; evidence measurement/data/expansion-v1/cutoff-5885-review/document-json-control-result.json; file SHA256 8f48641817d98f67eb8bb78c09469fbbc98f49f2365373761433193f9d8987f2.

## 12. exp-v1-rust-generation-0634

Change class: reference-fix.

Minimum scope: Classify an unknown/misplaced option in command position as Unexpected, not UnknownCommand; retain ordinary unknown command words and recognized global workspace handling.

Specification-grounded tests: parse_invocation(['--unknown']) must yield Unexpected('--unknown'); repeat after a valid --workspace pair. An ordinary unknown word must remain UnknownCommand. Keep all five commands, repeated tags/order, duplicate options, operand errors and jobs bounds. No probe should require private parser helpers.

Contract and quality decisions: Stateful token consumption, global/local option placement and command-specific shapes are substantive. Limit the witness to unambiguous '--' options; do not silently invent single-dash or option-looking operand precedence beyond the original grammar.

Exact held reason: Reference classifies unknown option in command position as UnknownCommand instead of required Unexpected.

- Parent canonical SHA256: fc7ad7656ace9381dfd98259e12a29b9c7505aee600251e637aa771ce6d9c8fb.
- Prompt content SHA256: c0c66704aeaf066a23b751726625685416759d90c591d624b1b4b18982420d73.
- Reference content SHA256: 14646d276395d2924f54bf83c138a97b63bd9cb919fe36ebb8fd3ae81ff2cb58.
- Test solution_test.rs content SHA256: 3ba0251b0fb5f5ecb950d2cdcca6cdd09007d510b7ced43d9be2c9f10031fe75.
- Source object canonical SHA256: d4735da4cc3ebbecf0efeb1eef80647099a2151d7e1edc67b030d65806a2bf5c.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-24060","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"74d3dd78ce2e81e1ac44e844406d8b58e6c5e530408aca7ba125b9c73148ae33","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: e9e459eb52a54709a21a22e2de3412eab43f0f1e6d22e010eabeaa3c56957867; evidence measurement/data/expansion-v1/cutoff-5885-review/invocation-unknown-option-result.json; file SHA256 965ac51feb7cf3d31c9145b8f5336a93684acaf345ad373433e25861e83e2577.

## 13. exp-v1-rust-generation-0635

Change class: reference-fix.

Minimum scope: Reject forbidden explicit endpoint=null when that segment is processed, after duplicate-key check, not at finalization. MissingEndpoint stays an end-of-input absence check.

Specification-grounded tests: With reject_null_required=true, 'endpoint=null;tracing=bad' yields NullEndpoint for either allow_missing_required value. Reverse order yields tracing InvalidValue; with null allowed, the later bad tracing still errors. 'endpoint=x;endpoint=null' returns DuplicateKey before interpreting null. Include a later malformed/unknown segment and valid null/missing/default controls.

Contract and quality decisions: Left-to-right parsing, duplicate priority, flags and typed values interact. Do not infer that MissingEndpoint outranks an actual earlier segment error or invent stricter integer spelling than the existing u16 contract.

Exact held reason: Reference defers forbidden explicit null past a later invalid segment despite left-to-right first-error contract.

- Parent canonical SHA256: 08d9c25271dc3f0bcbc500625ba16b06e094c8f578a434799f5da6484e329fc9.
- Prompt content SHA256: 66ae5eae2ff9b726571c5a7391431a4284f86797e20257b76fe3f1a8d91c0bb6.
- Reference content SHA256: 20389ec9af36de68c053b00af30d33479e1a9a17179d23cd864f332329c4eb9c.
- Test solution_test.rs content SHA256: fdd23399e9bece9832856570c05ae7a15967a012f050f4819da283a73072c978.
- Source object canonical SHA256: 1e741033db6e697f1aca1811acff75241cc445de443893e425d41f6b37902c75.
- Rights object canonical SHA256: 8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b.
- Complete source: `{"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23725","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"e605bedf3c5f49d38d38e903c4f2190710fc95bdd36b1fc51270b41d9b5460a2","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}`.
- Complete rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.
- Hold entry canonical SHA256: 5b963fe75bf8af687514f9c2f7fdf339fc24cac69bc1c4af109ceeb58cb4615e; evidence measurement/data/expansion-v1/cutoff-5885-review/profile-null-priority-result.json; file SHA256 56e1513242dd91b5d6f2b02be82ee2bdfcabf7cc47d32925e470a45608381960.

## Explicitly not selected in this bounded screen

Fresh full reads also considered Python0368 (MappingProxy/deep-copy contract plus large epoch formatting scope), 0785 (fixed dispatch/format wrapper), 0665 (near-duplicate repeated-row migration already covered in reserved recovery and elementary concern), 0645 (fixed-path metadata toggle plus wider Mapping ownership domain), 0598 (recursive merge introduces alias/cycle and every-depth key-validation scope), 0756 (visible-text domain beyond script/style is not sufficiently closed), and 0737 (filename normalization plus blank-name/disabled-validation/CSV-CR questions). These are not new terminal dispositions; no blanket re-review or automatic expansion is authorized.

Rust0584 and 0419 are direct packing/divisibility targets despite real boundary defects; Rust0532 is largely fixed code-template generation with keyword/priority issues. Rust0485 has nested assignment versus arithmetic nonmutation contract tension, Rust0393 has an inverse-rotation defect but wider finite-float representation questions and a wrong original inverse oracle, and Rust0705 leaves its toy tag algorithm insufficiently fixed for broad inequality oracles. Do not select these merely to fill the lane target. Prior documented compile-only Rust0133 and Rust0487, and terminal Rust0704, are excluded; no gate weakening or original-control compile failure substitution.

## Reservation snapshot binding

- measurement/data/expansion-v1/recovery-plans/r1/plan.json: a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1
- measurement/data/expansion-v1/recovery-plans/r2/plan.json: 5dae7eac34ac462f6173dc6b740364d5c4b68129950359f453f4038111ad1d29
- measurement/data/expansion-v1/recovery-plans/r3/plan.json: cbad9d14a504531e749b5eb3433f0bf4670e21f2a8e8d5f310d2e843e53c6231
- measurement/data/expansion-v1/recovery-plans/r4/plan.json: 8a6137773e65e1a55e5eaceed9a8c2e40153b5759a46a5189ba6a488d530d58c
- measurement/data/expansion-v1/recovery-plans/r5/plan.json: 778e0071bec56248081e741f4c742d522c75b4b006e069d8301b75440c2732ec
- measurement/data/expansion-v1/recovery-plans/r6/plan.json: 803f0308b33b4b8a834347d5976a148bc66001d6fc8606a1e206fb0e2b4a6795
- measurement/data/expansion-v1/recovery-plans/r7/plan.json: f0a3b5d14eb983206ac83c99571c5522925feaf7ac0443ec3c59ad172d5f293e
- measurement/data/expansion-v1/recovery-plans/r8/plan.json: 1a579af9da9d542d6bb4f03c8fbc030fd0b9d3102a31c347cd631bfc18b873de
- measurement/data/expansion-v1/recovery-plans/r9/plan.json: 0f0d6e653bbabff308a912cc764d1373b20faf3f4cf68a4c7341c94f36b5ae79
- measurement/data/expansion-v1/recovery-plans/r10/plan.json: 728e70ee23ad46f8a4a8aec64a34d74b48c073a5382849fc52ce449154f2afb5
- measurement/data/expansion-v1/recovery-plans/r11/plan.json: 2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6
- measurement/data/expansion-v1/recovery-plans/r12/plan.json: 0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121
- measurement/data/expansion-v1/recovery-plans/r13/plan.json: dead1489bb779934327bf3c8786d89c65b7604832829fa17129ea41ff1773217
- measurement/data/expansion-v1/recovery-plans/r14/plan.json: 2d59789fea811ba7ebe844564ee4dc66569fe4719067dea6d6a1524b049ea51f
- measurement/data/expansion-v1/recovery-plans/r15/plan.json: d2e65ef33e2c70162a53315e3daec75ebe1e3fbc1a7098e8635eddacb348c100
- measurement/data/expansion-v1/recovery-plans/r16/plan.json: efd902abc4ed3e00d6639c74f7d2ec95e6f153d1aa19a70a460aeb553dfb6844
- measurement/data/expansion-v1/recovery-plans/r17/plan.json: 60c02db8869c80c1515e2216205ac11a45b357206563f62f499d8b67b3ee02ee
- measurement/data/expansion-v1/recovery-plans/r18/plan.json: 512e3219da55465742728f2c5116840498e4a41c5a2bfe8f5b0130d9a19690a0
- measurement/data/expansion-v1/recovery-plans/r19/plan.json: 401d56a11f2ca2929eb42be7ffb36fe694cfded2500ed56a96759560b8b65f62
- measurement/data/expansion-v1/recovery-plans/r20/plan.json: 879eb4184b49e09a171cbe35592096a296d9d2af6e1e52eea68315fb6b7eb224
- measurement/data/expansion-v1/recovery-plans/r21/plan.json: a5fe5bbb1cffe149091f626ed317a0e79c39985c10c883acd8f83df3c04582ca
- measurement/data/expansion-v1/recovery-plans/r22/plan.json: 34b141407c111f6df7999027d57540860ccb3b47c0d10c2c5ce8ba105f8facc0
- measurement/data/expansion-v1/recovery-plans/r23/plan.json: d44918671d7a9350cc90e67ac7eede1ee4ab61e6ce6bae2f1eadaccbed367d92
