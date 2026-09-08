# Next JavaScript/TypeScript recovery selection, batch 2 — 2026-09-08

## Result and scope

Recommend **9 new held parents: 5 JavaScript + 4 TypeScript**. Explicit shortfall against the 10+10 ceiling: **5 JavaScript + 6 TypeScript = 11**. This is a conservative bounded selection, not a claim that no other recoverable parents remain.

Gate 2, proposal only. No reservation, generation, teacher call, candidate execution, cloud activity, admission or central mutation. Zero new original-record coverage. Full original prompt/reference/test reads were completed for every proposed parent, with original mutant differences inspected and exact historical diagnostic test/outcome evidence read. Historical failed diagnostics are not fresh executed evidence.

Exclusion join covers all currently present reserved plans r1–r20: 120 unique original parents. None of these nine is reserved. TS0241/0242 and prior explicit selection deferrals are excluded. Main must rerun this join before reservation. No elementary-held parent is proposed.

## Seven-criterion treatment and common limits

Each selected target has a coherent narrow defect, named API, standard-library-only implementation and tiny contract-derived witness below. Complete-target non-triviality is evaluated individually, not inferred from patch size. These are selection conclusions; independent test provenance, corrected prompt/API clarity, idiomatic complete reference, meaningful single-defect mutant, dependency isolation and sandbox qualification must still be established for each future artifact.

New independent tests must see only the approved derived specification, not original tests or the corrected reference. The original known-bad is not automatically suitable: it usually targets a different bug and shares the currently held defect. Build a one-defect mutant from otherwise corrected behavior. Carry every stated correction obligation rather than making a convenient partial fix.

Required-field preservation means copying values promised by the public record type; it does not mandate preserving input descriptors, prototypes, arbitrary metadata or accessors. Tests should compare required fields, not JSON property ordering, concrete object shape beyond the contract, method insertion order or unpromised exception names.

## Proposed parents

### exp-v1-javascript-generation-0034 — Validated glossary and detached review results

- Proposed change class: `reference-fix`.
- Request rationale / minimum correction: Validate every category and every review-token position, rejecting holes with TypeError before constructing results. Preserve trim normalization for glossary terms/categories, case-insensitive lookup and duplicate terms, token spelling/order and independent category arrays.
- Defining independent test requirements: createGlossary([{term:'valid',categories:new Array(1)}]) and createGlossary([]).review(new Array(1)) must each throw TypeError. Repeat with a valid prefix followed by a hole; require input nonmutation and ordinary known/unknown/empty-token behavior. Retain duplicate-case error and repeated-output mutation isolation.
- Contract decisions and hard limits: No new Unicode normalization, casefolding, input size or prototype policy. Use JavaScript case conversion consistent with the existing contract; do not introduce full Unicode casefold promises. A one-defect mutant may omit token-hole validation while category handling and ownership stay corrected.
- Whole-target substance: Persistent normalized unique-term index, dual input validation and per-result detached collections interact; not merely a string replacement.
- Parent canonical SHA-256: `4d16032d68bb2d5e5cf60535b0edf67c3b5a8e1397f8a44988a75c5fb6df80ff`.
- Prompt SHA-256: `45da4f03a13fd9c303d286b5852c1adbcb0286a298f6b3f5b6b0b103212b411b`.
- Reference SHA-256: `0b7473d86f3e8b4a3fb0d8c1ba49e0fb8c28b223ec2b6a58be78b98c8f7b563b`.
- Original test SHA-256: `1bc0cbbf56d8d3318d31c62f21b36bb65d87892e29fc94e2a911c9d55bbeaffd`.
- Exact held reason: Sparse categories and sparse review tokens both bypass required string validation.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/glossary-sparse-result.json`; raw SHA-256 `d764fb0633a1f83fbc20003af0d1c336cac8fea003cca4954be4e679d4246927`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, record `row-26941`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`; source-record SHA-256 `8a3af611be382bc79cb152e4ed5cfe8eeb4c4ad01e0c81319b00261034c8b184`.
- License: CC-BY-SA-4.0, https://creativecommons.org/licenses/by-sa/4.0/; source URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Rights (unchanged): `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`. Preserve the complete hash-bound source object and its transformation history in future lineage.

### exp-v1-javascript-generation-0061 — Protocol mapper with exact epoch splitting and complete generator validation

- Proposed change class: `reference-fix`.
- Request rationale / minimum correction: Replace hole-skipping measurement preparation in map with complete packet validation before the first yield. Keep canHandle nonthrowing, legacy/modern kinds, ordered topic deduplication, BigInt timestamp quotient/remainder and the existing numeric domains.
- Defining independent test requirements: For modern samples with data=new Array(1), canHandle must be false and iterator.next() must throw TypeError. Repeat [validMeasurement,hole]: the very first next() must reject rather than yield the prefix. Preserve empty packets, singular/plural protocol controls, nanosecond maximum and complete detached timestamps.
- Contract decisions and hard limits: No silent sequence/error-class changes or numeric caps. Do not change the generator contract to an eager array. For splitEpochNanos malformed inputs allow the specification's stated TypeError/RangeError latitude unless separately frozen. A single mutant should skip holes, not also alter nanosecond modulus.
- Whole-target substance: Exact-width conversion, protocol discrimination, complete pre-yield validation and independent generated objects form a substantive target.
- Parent canonical SHA-256: `08071ad6a6a8e77b4cddf1b6fcfd34268f384a12eda00a0396a58bbfeba6e80f`.
- Prompt SHA-256: `74c2f55d8b0f39db80a343db6f00100c4e0433054d0952a3eb82e44c28ab0100`.
- Reference SHA-256: `72dd01601a3aa71f6c828c2e679980141e924430d6c81ed91dc89b219d14bbb6`.
- Original test SHA-256: `efaabbe212383236a962e0d1d08a3388d4a00d632dab469e0e9ed7bf8991a7bf`.
- Exact held reason: Telemetry map accepts sparse plural packet that canHandle correctly rejects.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/feed-sparse-result.json`; raw SHA-256 `e5203afd4cf2c936c274d2f640b4e790ec6ca76fb8308184803048766a5b3206`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, record `row-00458`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`; source-record SHA-256 `1d9b1ce15dea8656592b52316ea3a0fec2cd723ec394a85aef6423b32d4d8b8c`.
- License: CC-BY-SA-4.0, https://creativecommons.org/licenses/by-sa/4.0/; source URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Rights (unchanged): `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`. Preserve the complete hash-bound source object and its transformation history in future lineage.

### exp-v1-javascript-generation-0090 — Monotonic-ID reading shelf and atomic patch validation

- Proposed change class: `contract-clarification`.
- Request rationale / minimum correction: Make the existing only-title/pages/status patch rule explicitly cover all own keys, including non-enumerable string keys and symbols; recognized own fields are read regardless of enumerability, inherited fields are ignored. Then validate those keys and fields before lookup/mutation. Preserve all ID allocation/exhaustion, statuses, sorting and copying.
- Defining independent test requirements: Patch an existing book with a non-enumerable own unexpected key: TypeError and unchanged list. Repeat with valid title plus hidden unknown key; known non-enumerable title must update. Also reject unknown own symbol under the proposed explicit policy. Preserve empty patch, missing-ID valid patch null, highest-ID removal/nonreuse and safe-ID exhaustion.
- Contract decisions and hard limits: This property-boundary clarification must be approved, not silently inferred into a reference-fix request. No whole-prototype scan or hostile accessor requirements. Pages remain positive integers, not newly safe-only. Tests compare fields/behavior, not constructor/function reflection. Single mutant can validate only Object.keys while all other behavior is corrected.
- Whole-target substance: CRUD, monotonic allocation, error atomicity and strict patch schema are substantive interactions.
- Parent canonical SHA-256: `b42fa2345b2535ea180cc08fd6a38a2ea408f7a563832b7ecc318ad5799a968e`.
- Prompt SHA-256: `4d81b15fbe24c10668f804bb826c2433ce2d3ff29e2db75c9a64689139eb5eee`.
- Reference SHA-256: `06f810c757102638181e0648b7159216c8387934da2555adef16d4f93bb71ac6`.
- Original test SHA-256: `0483a67c37bb9dce4a7c8ff7a2ef16e3e2fd47755358795cc82c8519edc1b391`.
- Exact held reason: Unknown non-enumerable patch field bypasses explicit only-title/pages/status validation.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/shelf-hidden-patch-result.json`; raw SHA-256 `969e4cb05f5690a749ca2a9532d5e663fa56fc0c958bce81043aa5971b1eb4a6`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, record `row-10914`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`; source-record SHA-256 `f748cd2f99d921b0a4015e3697bd832d50cbb10eb9f17b9244b9ae6378b4403e`.
- License: CC-BY-SA-4.0, https://creativecommons.org/licenses/by-sa/4.0/; source URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Rights (unchanged): `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`. Preserve the complete hash-bound source object and its transformation history in future lineage.

### exp-v1-javascript-generation-0097 — Validated directory with stable search and independent snapshots

- Proposed change class: `reference-fix`.
- Request rationale / minimum correction: Validate every entry position before retaining a dense copied directory. Keep unique raw nonempty codes/titles, case-insensitive substring matching, default/nonnegative integer limit, zero-limit behavior and fresh get/search results.
- Defining independent test requirements: makeDirectory(new Array(1)) must throw TypeError during construction, as must a valid entry followed by a hole. Preserve ordinary valid substring search in input order, case controls, bounded/default/zero limits, duplicate rejection and mutation isolation.
- Contract decisions and hard limits: Do not trim raw nonempty strings, add safe-integer caps to limit, reject decorated records solely for descriptors, or introduce a new search ordering. This request addresses the held missing-element validation, not an unrestricted object clone. Single mutant skips entry holes with otherwise correct lookup/search.
- Whole-target substance: Construction-time uniqueness and ownership interact with two independent retrieval paths and stable capped search; retained as a bounded stateful target, not a new pagination template.
- Parent canonical SHA-256: `bb5f15cd9c13402bb76132464f96fedc08e95f446849d93a289655da4d60830a`.
- Prompt SHA-256: `25253e6ad0f560a0c45c9ce198439c104a729558ed173045a431475e267e4df0`.
- Reference SHA-256: `8d981862b909645ae39af5b273f6552b85e602ccc3d2a15971da21a1a990311b`.
- Original test SHA-256: `17a8c077d5cb6b3a230581965f82489615ca540d7be23ebd3c564d6a2c09c550`.
- Exact held reason: Sparse directory entries bypass required record validation.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/directory-entries-sparse-result.json`; raw SHA-256 `a442ed629fe837edc78be73bb5ffe647f7304d290500029c8976d4a87a9a09c2`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, record `row-10886`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`; source-record SHA-256 `e9945de7d5ebae9e6b8214b3d12bb1d628b913a02c66b3ee2f0f71fd2a951aaf`.
- License: CC-BY-SA-4.0, https://creativecommons.org/licenses/by-sa/4.0/; source URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Rights (unchanged): `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`. Preserve the complete hash-bound source object and its transformation history in future lineage.

### exp-v1-javascript-generation-0119 — Normalized recipe CRUD with atomic ingredient updates

- Proposed change class: `reference-fix`.
- Request rationale / minimum correction: Validate each ingredient position before trimming/storing during constructor, add and update. Retain trimmed unique IDs, title/ingredient normalization, empty ingredient success, update partial-field behavior, id-update prohibition, insertion order and deep snapshots.
- Defining independent test requirements: Constructor ingredients=new Array(1) throws TypeError. On an existing book, update with a valid title and ingredients=['ok',hole] throws TypeError and leaves the old title/ingredients unchanged. Sparse add must store nothing. Preserve duplicate trimmed IDs, empty ingredients, unknown get/update/remove and copy isolation.
- Contract decisions and hard limits: No new unknown-extra-field policy: additional recipe fields are ignored as stated; do not silently expand patch rejection beyond the existing id prohibition and supplied title/ingredients validation. Do not require method property order; test exact method set as a set. Single mutant may skip ingredient holes but retain all other corrected behavior.
- Whole-target substance: Normalized keyed state, transactional partial update, ordering and nested ownership are substantive, although related recipe/CRUD families need composition accounting.
- Parent canonical SHA-256: `74e1d6caa1a6ffbb6faec18c7dcdb39b7eb2290c4cb8a8724eb6148370c04715`.
- Prompt SHA-256: `343ae18119a895d6712bde36bcb1780712952a8c3af9d444cbd68da07e4ce4f0`.
- Reference SHA-256: `7905c995d1ab009229a61a313ba945b2309c8185c35bd651eec64793cc477efe`.
- Original test SHA-256: `f59592963c4c69c472cbe79952cb7a4928be2beef5ace7cc6e32c9cae8735cd0`.
- Exact held reason: Sparse initial ingredients bypass string validation.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/recipe-initial-sparse-result.json`; raw SHA-256 `783f1995ab9c5c95b3f49f90a833e0a7b446a5500ad971d646165093c2543735`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, record `row-06759`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`; source-record SHA-256 `b994176cea0b1ef8ac7450227ae93824318fea927afcce78ae14aef1084bc0a2`.
- License: CC-BY-SA-4.0, https://creativecommons.org/licenses/by-sa/4.0/; source URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Rights (unchanged): `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`. Preserve the complete hash-bound source object and its transformation history in future lineage.

### exp-v1-typescript-generation-0072 — Version-separated subscriber repository

- Proposed change class: `reference-fix`.
- Request rationale / minimum correction: Replace spread copying of supplied Subscriber values with explicit copying of id/name/email/active throughout constructor/add/update and snapshots. Preserve distinct V1 list and V2 mutation namespaces, duplicates, update position and raw strings.
- Defining independent test requirements: Constructor V1 subscriber with own non-enumerable id='a' must list that id. Seed V2 similarly, then update/remove by the retained id; add/update supplied hidden name/email/active fields must survive. Mutate caller/output objects and confirm namespace/state isolation.
- Contract decisions and hard limits: The declared Subscriber type establishes required fields independent of enumeration. No extra-property preservation, descriptor preservation, new string validation, or out-of-type sparse-array policy is added. Error messages stay exact; fields may be ordinary copied data properties. Single mutant should spread only a supplied source copy.
- Whole-target substance: Namespace isolation plus constructor/CRUD uniqueness and defensive ownership distinguish this from a simple projection.
- Parent canonical SHA-256: `4a4a6d0f9bf22025ea247abac34a73fd21f2896e07725f7ee77f6c4dda5d2729`.
- Prompt SHA-256: `d60440f4bce9496322ea76e09ba8f648fca3be78f10050c8a6c2ada2c37a906d`.
- Reference SHA-256: `c3ea85ca920bd9d9bdea47481ad2e1d627e0a2318c34680e5543d6db02fecb7f`.
- Original test SHA-256: `bbba50f13169cd379ac58f359e6ade4ee4aa4d183f360e2e707076680008496a`.
- Exact held reason: Constructor spread copy loses a valid non-enumerable required subscriber ID.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/subscriber-hidden-id-result.json`; raw SHA-256 `0265f46ddb32179a0fbaf11cef728f9f4432d86289fcd14dd4a673f7e06de00f`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, record `row-33323`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`; source-record SHA-256 `c15a4be7ab0853e9e49ed916afa276f9ad1756559ae785b5e413f0e9f5c7b1ea`.
- License: CC-BY-SA-4.0, https://creativecommons.org/licenses/by-sa/4.0/; source URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Rights (unchanged): `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`. Preserve the complete hash-bound source object and its transformation history in future lineage.

### exp-v1-typescript-generation-0086 — Dimension state with independent listener snapshots

- Proposed change class: `reference-fix`.
- Request rationale / minimum correction: Explicitly copy width and height on construction, resize and current/notification output; no spread-only copying of accepted input. Preserve finite nonnegative integer validation, no-op equality, registration snapshot, duplicate registration identity and idempotent removal.
- Defining independent test requirements: Hide required width=2 on {width:2,height:3}; constructor current().width must remain2. Resize with a hidden required width and verify committed values plus separate listener objects. Retain one-axis change, unchanged no-op, invalid nonmutation and subscription/removal during callbacks.
- Contract decisions and hard limits: Do not introduce safe-integer restriction or require descriptors/frozen output. Existing registration-snapshot behavior is in scope; no new callback-error or nested-resize scheduling policy is invented. Selection is for required-field preservation, not another duplicate-unsubscribe mutant. Single mutant loses the initial hidden width only.
- Whole-target substance: Validated state transitions, per-callback ownership and snapshot registration semantics are substantive; account for existing observer-family density before selection.
- Parent canonical SHA-256: `c0c1b1b9b53b42b12de2ca9a4bb6ddca4bdd61c0d024b6a726a16c840e28f168`.
- Prompt SHA-256: `d4b09434518cb86b853ed58b90c424262238c7c6c7af1f48f24a686976472379`.
- Reference SHA-256: `3dc9f95786a6073b8139c0b9dcda36475dbdb88f1290484e65ba96b03a1892a9`.
- Original test SHA-256: `f1767d8461e5df46db414728f526c8acf48846011c3d7695ddabb23c31e541f0`.
- Exact held reason: Required valid non-enumerable width is lost after successful dimension validation.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/dimensions-hidden-width-result.json`; raw SHA-256 `6b264ea951e4e6b4f57392c16a3a6c6c1cd3b9ebc498308161fcb520c9894d32`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, record `row-32635`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`; source-record SHA-256 `68eca6df8bf1c06a2ddcfae60c74b8ac930c50b230a39348986e1cdd83176482`.
- License: CC-BY-SA-4.0, https://creativecommons.org/licenses/by-sa/4.0/; source URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Rights (unchanged): `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`. Preserve the complete hash-bound source object and its transformation history in future lineage.

### exp-v1-typescript-generation-0097 — Validated grouping with compound code-unit ordering

- Proposed change class: `reference-fix`.
- Request rationale / minimum correction: Explicitly reconstruct all required Preset fields before grouping and sorting; hidden required labels/IDs/status must survive. Preserve raw string values, blank rejection, global duplicate IDs and label-then-ID code-unit order.
- Defining independent test requirements: A valid available preset with non-enumerable label='A' must return label A. Use two hidden-label records to verify actual ordering, equal-label IDs A/a for tie-breaking, and both statuses. Test source/output mutation independence and duplicates across groups.
- Contract decisions and hard limits: No localeCompare, trimming of retained values, extra-field/descriptor preservation or runtime enum expansion. Typed status remains available|withdrawn. Tests should use instanceof for TypeError/RangeError rather than require mutable error.name. Single mutant can spread source presets while grouping remains correct.
- Whole-target substance: Duplicate validation, two partitions, compound explicit ordering and detached required fields form a coherent target beyond an enum-to-literal template.
- Parent canonical SHA-256: `76fe2c6d594e702af13675a235223ee8e0cb2aca33dc47fbfae5f69f95e872a4`.
- Prompt SHA-256: `39080ea5e89f7034dc30a827a4e4dc64a0b20f0209e33074284151d14964bb35`.
- Reference SHA-256: `93d4f1c0a86868af57f93eabd4e17cdd15db43cbf386cdb98736973a3b94e017`.
- Original test SHA-256: `204cb5dd10a99f0c953171ef07a5512dd80601a13c33dbeba3e0f13ae9bee799`.
- Exact held reason: Non-enumerable required label lost on preset copy; property-domain disposition pending.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/preset_0097_hidden_field_probe-result.json`; raw SHA-256 `2f1ae0b50ab2aaf7fb64b3b8a67e689703061691c0b35d1af327bc78662a7417`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, record `row-32889`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`; source-record SHA-256 `ade5c72d02aff6d873b0b45911d178b80a55202ee9dc2f015fd7adc90c2a783b`.
- License: CC-BY-SA-4.0, https://creativecommons.org/licenses/by-sa/4.0/; source URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Rights (unchanged): `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`. Preserve the complete hash-bound source object and its transformation history in future lineage.

### exp-v1-typescript-generation-0101 — Immutable book insertion with ordered accumulated errors

- Proposed change class: `reference-fix`.
- Request rationale / minimum correction: Copy every declared Book field explicitly for existing rows in both success and failure branches, preserving required hidden fields. Keep ordered simultaneous errors, trimmed new strings, duplicate check against trimmed new ID, year bounds and separate returned book.
- Defining independent test requirements: Existing Book with own non-enumerable id='old' must retain old on successful add and on an invalid-input failure. Also test hidden required ownerId/title/author/genre/year, ordered combined errors and success book distinct from its appended entry.
- Contract decisions and hard limits: No new existing-record normalization, metadata deep-clone, out-of-type malformed-array rules, or public schema changes. Existing content/order must remain unchanged. Tests narrow result.ok before accessing branch fields, without invented overloads. Single mutant drops hidden fields in the existing-book copy.
- Whole-target substance: Accumulated error precedence, duplicate normalization and independent success/failure snapshots form the whole substantive target.
- Parent canonical SHA-256: `59af9f01c3c8a5b5e026a24a6ecfaa2e3450b37b124101b1e11aa23227cffe90`.
- Prompt SHA-256: `5a5de0dab5e6453a590aa6817ae5b519858d324a23d64a517d99bf3a88fd4215`.
- Reference SHA-256: `323f052602d04f8f5716d75b904f0fb8d3876c6ce0963ae7f9441ebfc05246d3`.
- Original test SHA-256: `20812b3dcb2e7c6d8c801eeec91ff2f6c6b6b4bcc0394fd0d3967156523b1b1f`.
- Exact held reason: Valid existing required book ID is lost during copying.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/book-existing-hidden-id-result.json`; raw SHA-256 `196cfec19ae380f6f6e506d203d53f8beb2952c192e326762ed91ed55550ef25`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct, record `row-02270`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`; source-record SHA-256 `b424d77a41dc28adabb96e2238c848ba6719014f78af15d3365a6a22c9b271af`.
- License: CC-BY-SA-4.0, https://creativecommons.org/licenses/by-sa/4.0/; source URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Rights (unchanged): `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`. Preserve the complete hash-bound source object and its transformation history in future lineage.

## Deferred alternatives and shortfall

The bounded screening deliberately did not fill the quota. These are selection deferrals, not newly recorded original holds:

- JS0092: full read shows sparse labels plus unstated trim/blank narrowing for IDs/summaries and labels, and property-key coercion of severity. A sparse-only request would not be complete.
- JS0120: sparse candidate/skills validation is real, but the phrase “exactly usable fields” for criteria leaves unknown-field handling insufficiently explicit for this narrow tranche.
- TS0012: full read reveals an unconstrained numeric monotonic ID counter and original test additionally asserting failed creates do not consume IDs. Do not silently invent an exhaustion cap or reuse/consumption policy.
- TS0026: prompt names repository and result exports without supplying their full public method/signature schemas; do not infer them solely from implementation/tests.
- TS0123: full read reveals optional schema choices, empty-versus-blank ignored-prefix mismatch, elapsed arithmetic and unbounded generated-ID concerns beyond the hidden-ID headline.
- TS0137: full read reveals unstated constructor-name trimming expectations and underspecified AccountUpdate alongside the hidden-secret defect.
- TS0161: full read reveals global malformed-ID wording versus remove/get behavior and optional patch rules needing decisions; not selected on hidden recipient alone.
- TS0023/0032/0061/0098/0108 and JS0084 were screened as less compelling whole-target diversity/substance for this tranche; no correctness hold or universal elementary conclusion is added here.
- JS0041/0091 were not advanced to a complete recovery proposal in this bounded pass; no readiness claim.
- Prior deferrals remain excluded, including JS0005/0044/0052/0113/0241/0319 and TS0031/0073/0187, and the explicitly named TS0241/0242.

The 9 proposals include related lookup/CRUD/observer families. Main should consider family-token composition when choosing a subset. Do not count narrow correction variants as unrelated training diversity.

## Exclusion and evidence seal

Original corpus: datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl, SHA-256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Hold ledger: measurement/data/expansion-v1/cutoff-5885-review/additional-holds.json, SHA-256 `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.

Canonical hashes use sorted compact UTF-8 JSON with ensure_ascii=False; evidence/plan hashes use raw file bytes. Source/rights are preserved, not reopened.

| Reserved plan | Rows including repeat recoveries | Raw SHA-256 |
| --- | ---: | --- |
| measurement/data/expansion-v1/recovery-plans/r1/plan.json | 12 | `a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1` |
| measurement/data/expansion-v1/recovery-plans/r2/plan.json | 7 | `5dae7eac34ac462f6173dc6b740364d5c4b68129950359f453f4038111ad1d29` |
| measurement/data/expansion-v1/recovery-plans/r3/plan.json | 14 | `cbad9d14a504531e749b5eb3433f0bf4670e21f2a8e8d5f310d2e843e53c6231` |
| measurement/data/expansion-v1/recovery-plans/r4/plan.json | 19 | `8a6137773e65e1a55e5eaceed9a8c2e40153b5759a46a5189ba6a488d530d58c` |
| measurement/data/expansion-v1/recovery-plans/r5/plan.json | 11 | `778e0071bec56248081e741f4c742d522c75b4b006e069d8301b75440c2732ec` |
| measurement/data/expansion-v1/recovery-plans/r6/plan.json | 11 | `803f0308b33b4b8a834347d5976a148bc66001d6fc8606a1e206fb0e2b4a6795` |
| measurement/data/expansion-v1/recovery-plans/r7/plan.json | 9 | `f0a3b5d14eb983206ac83c99571c5522925feaf7ac0443ec3c59ad172d5f293e` |
| measurement/data/expansion-v1/recovery-plans/r8/plan.json | 10 | `1a579af9da9d542d6bb4f03c8fbc030fd0b9d3102a31c347cd631bfc18b873de` |
| measurement/data/expansion-v1/recovery-plans/r9/plan.json | 6 | `0f0d6e653bbabff308a912cc764d1373b20faf3f4cf68a4c7341c94f36b5ae79` |
| measurement/data/expansion-v1/recovery-plans/r10/plan.json | 4 | `728e70ee23ad46f8a4a8aec64a34d74b48c073a5382849fc52ce449154f2afb5` |
| measurement/data/expansion-v1/recovery-plans/r11/plan.json | 13 | `2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6` |
| measurement/data/expansion-v1/recovery-plans/r12/plan.json | 51 | `0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121` |
| measurement/data/expansion-v1/recovery-plans/r13/plan.json | 1 | `dead1489bb779934327bf3c8786d89c65b7604832829fa17129ea41ff1773217` |
| measurement/data/expansion-v1/recovery-plans/r14/plan.json | 2 | `2d59789fea811ba7ebe844564ee4dc66569fe4719067dea6d6a1524b049ea51f` |
| measurement/data/expansion-v1/recovery-plans/r15/plan.json | 19 | `d2e65ef33e2c70162a53315e3daec75ebe1e3fbc1a7098e8635eddacb348c100` |
| measurement/data/expansion-v1/recovery-plans/r16/plan.json | 10 | `efd902abc4ed3e00d6639c74f7d2ec95e6f153d1aa19a70a460aeb553dfb6844` |
| measurement/data/expansion-v1/recovery-plans/r17/plan.json | 13 | `60c02db8869c80c1515e2216205ac11a45b357206563f62f499d8b67b3ee02ee` |
| measurement/data/expansion-v1/recovery-plans/r18/plan.json | 2 | `512e3219da55465742728f2c5116840498e4a41c5a2bfe8f5b0130d9a19690a0` |
| measurement/data/expansion-v1/recovery-plans/r19/plan.json | 2 | `401d56a11f2ca2929eb42be7ffb36fe694cfded2500ed56a96759560b8b65f62` |
| measurement/data/expansion-v1/recovery-plans/r20/plan.json | 2 | `879eb4184b49e09a171cbe35592096a296d9d2af6e1e52eea68315fb6b7eb224` |

Main approval of the exact subset and any explicit contract clarification is required before issuing a fresh versioned request. Fresh verification, evaluation separation, deduplication, composition/sufficiency and admission seals remain mandatory.

