# R22 Java independent recovery quality review — 2026-09-08

Gate 2; static review only. Exactly six derived Java candidates were reviewed against complete original and derived prompts, references, tests and embedded mutants, the approved R22 request/plan, and existing completed r22-java diagnostics. No code was executed, no candidate or central record was changed, and no additional original-review credit is claimed.

## Decision

Zero unconditional candidate positives. Three substantive test holds: generation-0026, repair-0065, repair-0401. All five repair artifacts also have an approved-scope/prompt-binding hold. Repair-0075/0460/0464 are substantive reference-and-test positives conditional on resolving that binding discrepancy; this is not admission. No corrected-reference correctness defect was identified in the six complete references.

| Candidate suffix | Reference quality | Test quality | Approved prompt scope | Overall |
| --- | --- | --- | --- | --- |
| generation-0026 | Positive | Hold: valid tree rejected by oracle | Preserved exactly | Hold |
| repair-0065 | Positive | Hold: defining exact-floor witness absent | Hold: additional algorithmic requirement | Hold |
| repair-0075 | Positive | Positive | Hold: additional iteration requirement | Hold |
| repair-0401 | Positive | Hold: replacement String identity oracle | Hold: added behavioral prose | Hold |
| repair-0460 | Positive | Positive | Hold: behavioral elaborations beyond neutral diagnosis | Hold |
| repair-0464 | Positive | Positive | Hold: added behavioral elaborations | Hold |

## Binding discrepancy — do not silently waive

R22 repair requests are oracle-rebuild, not contract-clarification. They explicitly require preserving all original behavioral prose/APIs/domains/errors/ownership, replacing only the embedded complete known-bad source, and neutralizing stale diagnosis only when it describes the previous mutant. Each of the five emitted repair prompts contains the exact new known_bad_code.strip() substring, but that source guard does not establish preservation of the surrounding specification.

- 0065 adds: “The limiting scale and both floors must be computed as exact rational arithmetic; binary floating-point rounding must not change an integer result.” Correct exact output was already required, but prescribing the computational method is not neutral diagnosis and can exclude other correct methods.
- 0075 changes the empty-input paragraph to discuss immutable lists and adds: “Null elements must therefore be detected by iterating through the elements rather than by querying the list for null.” Accepting ordinary immutable lists follows the existing List domain; prescribing the iteration technique is new implementation-specific prose.
- 0401 adds explicit validation-before-return, whitespace-key and unrestricted-value sentences. These agree with the intended original semantics and approved correction rationale, but are behavioral prose additions rather than embedded-source replacement or neutral diagnosis.
- 0460 legitimately removes the stale floating-point decoder diagnosis, but also rewords the negative-zero requirement and adds negative-nonzero and beyond-floating-point-range behavioral statements. Those statements are entailed by the signed-long contract, not newly discovered reference failures; they nevertheless exceed the explicitly restricted prompt-edit operation.
- 0464 adds two empty-line examples and an explicit raw-whitespace label sentence. These are consistent with joining interior lines and exact label matching; they are still additions to the frozen behavioral prose.

These are finite, exact discrepancies, not a generic pending caveat. The reviewer has not authorized retrospective scope expansion or prompt rewriting. Main must explicitly disposition the binding issue before any of these exact repair artifacts can be admitted. Test-only correction alone cannot remove it. Do not claim all repair prompt changes were limited to source/neutral diagnosis.

## Individual seven-criterion review

### generation-0026 — test hold

Clarity/API: complete ordered binary preorder grammar, ASCII canonical nonnegative labels of unrestricted lexical length, complete slots, false rather than throw on malformed strings; public static Boolean-return API is consistent. Independent-origin evidence is bound below, but oracle correctness fails. Entire target is nontrivial: canonical token validation interacts with traversal-slot exhaustion, missing children and trailing tokens; it is not merely a one-line int-bound removal. Reference is idiomatic iterative Java, uses long slots, rejects malformed lexical tokens without integer parsing, and has no external dependencies. The known-bad preserves grammar/slots and realistically restores only the machine-int restriction.

The independent tests classify `1,2,*,*,3,*,*` as invalid. It is valid: root 1 has leaf children 2 and 3, each consuming its two empty children. The reference properly accepts it. The existing 36-digit positive-label tree is a genuine witness against the bounded mutant and original reference.

Existing diagnostic evidence: reference compiled then failed at SolutionTest.java:28 on the invalid valid-tree oracle; mutant and original reference compiled then failed earlier at line 7 rejecting the valid 36-digit node. None timed out. Their failures have different causes; do not label the reference failure as a semantic defect.

Specification-only test feedback: classify that complete two-leaf tree as valid; retain separate missing-child and extra-token invalid cases. Add the approved `2147483648,*,*` and 100-digit positive-node valid cases and a bounded deep iterative tree (the original suite had depth 2000). Do not introduce a numeric capacity limit or permit signed/leading-zero labels. The current huge-label witness already distinguishes the defect; its presence must not be erased when fixing the bad oracle.

### repair-0065 — test hold plus prompt-scope hold

Clarity/API: positive int dimensions, exact uniform limiting scale capped at one, floor each dimension with minimum one, fresh int[2], IllegalArgumentException for nonpositive dimensions. Reference chooses a rational limiting ratio with long cross-products and floors exact long products. All products of positive int dimensions fit signed long; no new dimension cap is needed. Idiomatic standard-library-only Java. The complete target is nontrivial numeric/validation/ownership interaction despite a narrowly recoverable rounding defect. Independent author provenance is present; tests are not sufficient for the declared held defect. The embedded mutant realistically uses double scale/floor while preserving the earlier repaired integer-division objective.

Tests cover width/height limits, fractional cases, extreme ints, non-enlargement, fresh arrays and malformed dimensions. They omit `fitSize(100,100,29,29)` => `{29,29}`, the decisive tiny exact-floor regression. Existing diagnostic reference, mutant and original reference all compile and pass, without timeout. Thus mutant qualification fails, not reference correctness.

Specification-only feedback: add the exact 100/100/29/29 => 29/29 result, retain both limiting axes, minimum-one and maximum-int checks, and use an independently derived exact rational/BigInteger oracle for a bounded set if adding breadth. Never use binary floating floor as the expected-value oracle. Preserve current reference/mutant for any authorized test-only correction, subject to the separate frozen-prompt disposition.

### repair-0075 — substantive positive; prompt-scope hold

Clarity/API: Map<String,List<Integer>> snapshot, ordered entries and elements/duplicates, deep nonmutation, unmodifiable map and nested lists, malformed nulls => IAE, empty and ordinary immutable inputs valid. The complete target combines generic accepted inputs, validation, order, two-level ownership and unmodifiable results; not elementary padding. Reference performs element inspection before ArrayList copies and unmodifiable wrappers in a LinkedHashMap. Standard Java only, idiomatic and coherent. The embedded mutant restores contains(null), while the original deep-copy objective stays corrected.

The tests use actual List.of(1,2) and immutable empty lists, not fabricated hostile custom objects; retain source/nested mutation isolation, key order, duplicates, null rejection and mutation attempts on map/list/entry views. The defining valid immutable-list witness reaches the query defect. Existing reference passes; mutant and original reference fail via ImmutableCollections List12.contains -> NullPointerException at test line 47, all after successful compilation, without timeout. This is meaningful input-domain discrimination, not a required exception subclass oracle for valid input.

No substantive test-only correction is required. The new prompt instruction prescribing element iteration is separately outside the approved source-only edit scope.

### repair-0401 — test hold plus prompt-scope hold

Clarity/API: mutable LinkedHashMap copy in encounter order, replacement position, preserved values including null, no mutation, equal copies for no-op/absent source, collision and malformed-key IAE. Reference validates every existing key before early return, then preserves position and values. Complete target combines validation order, collision/no-op state and ordered ownership; standard Java and idiomatic. The mutant realistically omits only existing-key validation, retaining repaired collision logic. Tests have independent author provenance and substantive null/empty existing-key no-op and absent-key witnesses. Existing reference passes; mutant/original fail malformed null-key no-op at test line 63 after compiling. This is a valid witness.

However tests assert `identityResult.keySet().iterator().next() == replacement` for a newly allocated String argument. Neither original nor derived prose mandates Java object identity for an equal String key. A correct map implementation may preserve the requested key value and ordering using a distinct equal String; the public equals-based String-key contract does not require this identity. This is a concrete unsupported oracle despite the current reference passing.

Specification-only feedback: replace identity comparison with String value equality plus expected key order/value and independent mutable-copy assertions. Retain malformed existing keys before both no-op and absent-key branches, null values, raw nonempty whitespace keys, and collision nonmutation. Do not add String interning/identity or descriptor-like requirements. Separate prompt-scope hold still applies.

### repair-0460 — substantive positive; prompt-scope hold

Clarity/API: exact signed-long comma codec, canonical grammar, -0 rejection, order/duplicates, empty and null behavior, input nonmutation. Reference validates ASCII grammar including -0 then uses Long.parseLong for full-width exactness and overflow rejection. The complete target combines encode/decode, grammar, numeric boundaries and validation; not elementary padding. No dependencies beyond the JDK, idiomatic and realistic mutant removing only negative-zero rejection while retaining exact-long parsing.

Tests retain Long.MIN/MAX, +/-9007199254740993, duplicates, empty arrays/strings, canonical encoding, nonmutation, signs/zero/whitespace/empty tokens and overflow. They explicitly reject -0 and do not carry the contradictory original `0,-0,-9` success oracle. Existing reference passes; mutant and original fail at test line 36 accepting -0; all compile and no timeout. No unsupported output/private-layout or exception-message oracle identified. A mixed-token -0 negative fixture would add breadth but the existing single-token fixture decisively covers the held defect; it is not a new quality hold.

Only the exact prompt-edit scope discrepancy prevents an unconditional positive.

### repair-0464 — substantive positive; prompt-scope hold

Clarity/API: exact opener and terminator, completed sections only, join every interior line with newline, nested opener content, raw nonempty label, all null lines invalid including outside sections, fresh arrays/nonmutation. Reference maintains a hasInteriorLine flag separate from character length and resets it across sections, preserving empty lines and section order. Nontrivial complete parsing/validation/state semantics; idiomatic standard-library-only Java. Realistic mutant restores character-length-based separator insertion with exact opener correction retained.

Tests include empty first line then x => newline+x, two empty lines => one newline, trailing empty line, empty section, multiple completed/unclosed sections, nested/marker-like content, raw blank label, outside null and fresh empty results. No unsupported trim or newline policy is introduced. Existing reference passes; mutant/original fail test line 10: expected newline+x, got x; all compile, no timeout. No substantive oracle defect found. Exact-prefix-with-suffix control from the original suite is useful optional retained breadth, not needed to invent a new hold when the reference correctly uses equality.

Only the prompt-scope discrepancy prevents an unconditional positive.

## Provenance and source/rights

Candidate user message, verification prompt and rendered prompt are checked against the same derived problem; assistant content is the reference. Each architect final problem and independent-author Tasks problem equals the emitted candidate problem; authored test text matches after the generator's strip-plus-newline normalization. Both calls return zero, are not timed out, have no parsed forbidden tool events or event parse errors. The independent author receives IDs and complete derived specifications, not the corrected reference or original test suite. For repair tasks those complete specifications themselves contain the known-bad source: do not repeat the prompt preamble's overly broad assertion that the author never saw any known-bad implementation. This is specification-origin testing, not implementation-blindness to embedded repair source.

Original corpus SHA256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Frozen hold-ledger SHA256 in request: `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.
Source fields except the explicit recovery transformation and all five rights booleans are preserved against each exact parent. Generation0026 is McEval-Instruct CC-BY-SA-4.0 revision 57bd46727e49ac3e2890218a146d35c2454a8496. All five repairs are MdEval-Instruct MIT revision 38c9197e3add996fae624eb198ebd06155b2101e, not McEval. This is lineage preservation, not a new legal assessment.

### Exact artifact bindings

SHA256 values below are raw file bytes except explicitly labeled canonical JSON. Canonical JSON uses sorted keys, compact separators and ensure_ascii=False. Candidate directory is `datasets/cache/expansion-v1/versioned-recovery/r22`; each candidate filename is its full ID plus `.candidate.json`.

#### exp-v1-recovery-r22-java-generation-0026

- Candidate file: `8ed9f1cd803a8b1d8ad3419b049e39e89c4bf377acffbd4139daaf57de8415b1`
- Candidate canonical JSON: `88e5e0f459425821029fd4bde1361dcc699d5fc841fb01664278e25d7e217a61`
- Original parent canonical JSON: `0534a85b6da9497118cb55f2e8f05bbfba9aa4e4f0eb626cf714ea0e4c4d8884`
- Problem UTF-8: `82a167b3147c36c0e7be0654e88ec6f2c9da27a85f62b7c689eb626fd1603bb9`
- Reference UTF-8: `3b6a7f38d2bc0908a1522c055370363ef62a863924b10064f1a2550fe2af461a`
- Independent tests UTF-8: `6339a013b2ee7c5f0cafd870149d82c9d489eff02e1c5ca5d88643eb75e0c2e8`
- Known-bad UTF-8: `05698a373558bf9b027cc517683fcc6b903e80f4b6cb035df3a87558f1649866`
- Source record row-28204: `ca9c0668735ab216ff80d8c898379935316b6e9941594001b78d3d846ce98ed0`; Multilingual-Multimodal-NLP/McEval-Instruct, CC-BY-SA-4.0.

Diagnostic receipts (read existing artifacts; no execution by reviewer):

- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-generation-0026-known-bad-0.json`: `aa9d0fbec7a710a305f92cbce4296873041729bb12927774a298bcc13cebb10d`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-generation-0026-original-parent-reference.json`: `3fa33cffd12e488fa9336333424452ac6c825e3814ad67ad217203f635792e1e`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-generation-0026-reference.json`: `0d2f2cb4ba4bd2a8491e2e9df7656e5f0a59c25bf9bcf3594845e0b06ed2dbd4`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-generation-0026-summary.json`: `211a443d8a5134a5d9d7252660aaf0c4c2bcdf255f01abd24afb7c1c136932f7`.

#### exp-v1-recovery-r22-java-repair-0065

- Candidate file: `4103b306a1835b593fd9dd08962cea2e4e027039b2eb8c4b8d6f6ab1b7d421ed`
- Candidate canonical JSON: `d87f8d476035b783671411546c57b6677c3bb6f9bb73dcc640526400ed52059f`
- Original parent canonical JSON: `c34d1c5d2b3f003ffea1c853e8dc04f86613d318364859a05b61f9b63688f065`
- Problem UTF-8: `53f3ae31e9412f1912378f559947786417693888fd0e7cc7a1934a0fa778cf7b`
- Reference UTF-8: `416b16c75210b8c686ffb51797817c659fc30e50bd5870245acd7dc293af41ac`
- Independent tests UTF-8: `3e84995e78bde3a7c16161e6e66ce60459a23572309a59f060542cecfa70fbc7`
- Known-bad UTF-8: `7f23bd6cfac60a7749e16d684a0064e2056882887bc88d558608a09b97b4a922`
- Source record row-10884: `a2ffe7305badc421b558e313f5945f22cf347d8d9e6181900d8b05b4a223277a`; m-a-p/MdEval-Instruct, MIT.

Diagnostic receipts (read existing artifacts; no execution by reviewer):

- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0065-known-bad-0.json`: `b5f4b6bcad500d608cad039ca741ebfc232df0493e478edbf1c52c8b17accc55`; passed.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0065-original-parent-reference.json`: `20a8b48fc2200c0a83b6f113290000e5618401759c5b06ddb00f302c85e4cb10`; passed.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0065-reference.json`: `3ef63a8a7613066cb278460951a8637586788e18aa0cc44f8e948376067ec5bb`; passed.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0065-summary.json`: `7c09aef020f48123c302fdcec265e2ba93d0264b9c278df63a6ba3ff9ef4d1c0`.

#### exp-v1-recovery-r22-java-repair-0075

- Candidate file: `f18401b6fed908f106d356ddd475b80fb0c8d364bbd7420066c414a024306267`
- Candidate canonical JSON: `d0b2aa7eb4fe242445da6c79850c52f24ebe10363622ba6bdd0e8939aee81606`
- Original parent canonical JSON: `7f843f49c9d9925480529ce3eac1047552fca5e2f28293d9e4403c3e3f617556`
- Problem UTF-8: `a4c14c5ed2256fe12c994f9284be23e633891b01f15846e2d37e7f64c55c66da`
- Reference UTF-8: `a234db84a51301fce795556b04a9359c6e92218ba205b92cb6b8b84b48182610`
- Independent tests UTF-8: `f6081ffa8011a0d8eb986cbd24e3b854ec60c118acfbd9d42fcba7ea68ee446c`
- Known-bad UTF-8: `f3ad08a44303d5dc4bafae84a0ea25d07b3cdb8be6dd06b9505e5a4fefdfc3b5`
- Source record row-09982: `49a965fee739dffecbfccbfab49ef5a95cc5402a7bbeaa0db2200b47ae1ecb95`; m-a-p/MdEval-Instruct, MIT.

Diagnostic receipts (read existing artifacts; no execution by reviewer):

- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0075-known-bad-0.json`: `b430e15152cf372813196130acc682a97282439320dd460cd26a317cb4ffeb60`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0075-original-parent-reference.json`: `7eeada53f446da18d139c823794abbfe2773f5028a0399f83abb2130ff5392b7`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0075-reference.json`: `0ce76dcd7f060d8131ccbe6d83aa9422e7f861b09cf4e51c1dd9ecafe4988a10`; passed.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0075-summary.json`: `2498b9e3e95cb7ba713ec82fc7e47ae864f5eeb589e22b535766ab590d74594f`.

#### exp-v1-recovery-r22-java-repair-0401

- Candidate file: `cbedd2c47835955bdea1bffa02931f607493b3e9736ec6cc127f14f6203c6fd5`
- Candidate canonical JSON: `aa537d2aeeb61e608596dc924f3ee08c9763369f4fb829f7b58cc147efa72b2c`
- Original parent canonical JSON: `c4d8ddefa4859653bc409279ab5db7cc83cdb24d68f788d33b1ec930831dbf9f`
- Problem UTF-8: `59297cd7282f8e01a4f878d8c1ca84723030fe9a5040d01511a5b265070167b5`
- Reference UTF-8: `2af4900442b51bd2ce0505a49a3ddf5dc86f84282feda4c5b1e9cc672b2b22c0`
- Independent tests UTF-8: `6f04743cf8b3b2fc6717ca5d044c6d6ff2451b7c61cfd8ee7385f50bf5078a9e`
- Known-bad UTF-8: `5312cd105c1d1013057e9578e2b4b0ad7b578d368db6412d20bbda1733a8215b`
- Source record row-12432: `450b4f119dd3fc8460d37ff6b217a516794ce24008c366c8f52b4a0f3dc8780a`; m-a-p/MdEval-Instruct, MIT.

Diagnostic receipts (read existing artifacts; no execution by reviewer):

- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0401-known-bad-0.json`: `c39a8229b606692124ac76bda4adbe022b9d3e6dfb8703d88d87e0523ca0bf60`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0401-original-parent-reference.json`: `27c28908998e576ba2ca3a461b9a90619da211f5944939bdf8c860f81846ce3c`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0401-reference.json`: `e173119eacfad11684d506523093a236e1def101b500e7a953784ef0f8558827`; passed.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0401-summary.json`: `cf8f758bafbc921fe90509371f3bc16f734c264c23871e4aca718cc0a8bf2409`.

#### exp-v1-recovery-r22-java-repair-0460

- Candidate file: `7cdcd978e0d8bc78e7c55e8c57884caa488a14906c9c22a166ab1fabaa2dd337`
- Candidate canonical JSON: `79eda93f52902c0c8f4c28ec253244c8c0c99cdb3d817eb12561494e0f61f65f`
- Original parent canonical JSON: `1b7dccfae15207310d49be2af3b5916aff29f6c55ac89b64eeb614660ac41182`
- Problem UTF-8: `9c7b8c7fa3aabea8bc504d3978fb629ab3beea13d456aa4298d48e5b4dce2f2d`
- Reference UTF-8: `4877905dd225620430912f64b2b7b50a3a2508e178190b0953ff28f1e5ea2955`
- Independent tests UTF-8: `a5bd7d39e70d5b69681f6846cb0084321dedd327ca37f4a2f576ff83321727f5`
- Known-bad UTF-8: `1b64ac4080f5521d34f36bfd998bd8bb6fe8651265cbed68a37878f41a73d55d`
- Source record row-11843: `85fd71077decc1963d8b90e139f7aa5cc72987c0412f850ed0b2ad00a741a7ce`; m-a-p/MdEval-Instruct, MIT.

Diagnostic receipts (read existing artifacts; no execution by reviewer):

- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0460-known-bad-0.json`: `bf70387f00c8befbd54f91fd8f8d53a0fafff33b2167a8a196c872fb5583e112`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0460-original-parent-reference.json`: `de0b65d92dd4e87ea4144f3393faf0fb4694c0737b85be2b51512880d5a5adf2`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0460-reference.json`: `ad64fabf33775b0dc9c76ec77bd29ee27d5c1ec0e411380804c3081409b2c329`; passed.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0460-summary.json`: `68cce043e3ec9435f44423816a34340c9eb0ab74d3c063314f2c0a4be98ee28d`.

#### exp-v1-recovery-r22-java-repair-0464

- Candidate file: `7c925c55fd3cc511159d538d4b0d9fc74d09d41dd534d1cb5f76a6a0b53bc4f1`
- Candidate canonical JSON: `7f40aff493ed409ee76687c5a933123e15a617c1e5584f81fc62cb4af438f5f6`
- Original parent canonical JSON: `fa8d34215fe2836c1f6e49d6fd40bdb900ed86ec10fd685f9ea760c1bada280c`
- Problem UTF-8: `c79655f54907c305d60bfa6f4d6dd19b12ae0a71dc22faf80a87d055caed15a3`
- Reference UTF-8: `7ea4a8b6094010dbd7c1dfaa0b160f4c981a7feb7856793fb77d11a500988e3d`
- Independent tests UTF-8: `4037f524b684fc56f03bd221db7ff6a6269e1323eaa69d5221e06fff969a97b7`
- Known-bad UTF-8: `01c6047507caae39fc8afa21200db073ed6598d815b16e60034a338221fa6457`
- Source record row-08055: `dfac8640df86d1e6e84375ad183965c1906bb26b51980cd1025a9e96d85f1b46`; m-a-p/MdEval-Instruct, MIT.

Diagnostic receipts (read existing artifacts; no execution by reviewer):

- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0464-known-bad-0.json`: `70043def9b9ff9116076f47c5f7bc74f81f103e144b4aa6c3d617048f7625db4`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0464-original-parent-reference.json`: `271e364bc79cebd89c61f1e0f798e4870554f3bafe747eeac825a59893f85095`; behavioral-failure-requires-review.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0464-reference.json`: `d50d2770e6fde0f8adba4c6d07c7e28cbe7ed30fd052d2c6bd2c12d816d2f450`; passed.
- `artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-java/exp-v1-recovery-r22-java-repair-0464-summary.json`: `42f083b04bb123616ce95c72eb898b8ce9902fd8d4a1ea2ee8b7ddce26ba2928`.

### Common evidence file hashes

- `measurement/data/expansion-v1/recovery-plans/r22/plan.json`: `34b141407c111f6df7999027d57540860ccb3b47c0d10c2c5ce8ba105f8facc0`.
- `measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r22.json`: `f2d66783fc2c5877a4016585c40f0b279a4991c809d59d1757eda35c6238eb00`.
- `datasets/cache/expansion-v1/versioned-recovery/r22/java-recovery-architect-evidence.json`: `c3863a5ad1c921370144768b33d38a7c03c82240a25d5988ee57b93aaa247dd6`.
- `datasets/cache/expansion-v1/versioned-recovery/r22/java-recovery-independent-tests-evidence.json`: `b16f33310d3f83c3ec49879ab7101dfe6d0b36a2eb92af450403d18939a28957`.
- `datasets/cache/expansion-v1/versioned-recovery/r22/run-contract.json`: `a0b4a39242bee4710967f7d01a0d6031bf4a81401f3aca98bcab09c80b80c6a8`.
- recovery-architect prompt: `d0eed8be7b7ab46b61b5de3f9969aef75d558cb04450b76426c8d3f0b5c8bb69`; final output: `c8b5af078537a3534c7045c6749a0f461183d433f7b855d9947605f0fed51774`.
- recovery-independent-tests prompt: `e4dce8f70ee3d53895d7dc61c8e7d19eb305c5215423ce2182c875667391ac20`; final output: `7c20b330eb0c388961ccc198945a90c2c866ce99bde8c48ead97078e57ab87e6`.
Approved request evidence: `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R21_JAVA_FAILURE_20260908.md`, SHA256 `493ab0a73263481e6e54adacffcd1674e8b542a1fdaf0236900a0f14d268926d`.

No automatic retry, admission or scope waiver is proposed by this report. Main owns the exact binding disposition and any one permitted test correction. All original held parents remain unchanged.

