# Next Go/Java recovery selection — 2026-09-08

## Provisional result

Recommend **18 new held parents: 10 Go + 8 Java**. Shortfall against the 20-row ceiling: **0 Go, 2 Java**. This is selection only, pending main approval; no reservation, teacher call, candidate execution, cloud operation, admission or central mutation. Zero new original-row coverage credit. All selected original prompts, references and complete original test files were read; exact per-ID hold evidence was reconciled. No keyword-only selection or new executed finding is claimed.

Exclusions were joined against all reserved r1–r11 plan records, including r11: **69 unique parent IDs**, with zero selected overlap. This current exact union supersedes the informal previous57 count. All18 are present in the additive hold ledger, have preserved approved source rights, and none was selected from elementary, licensing or evaluation-overlap holds.

## Per-parent scope, witness and contract decisions

### exp-v1-java-generation-0028 — reference-fix

Substantive target: Immutable outcome/request boundaries, checked failure routing and exact uninterpreted destination.

Minimal correction / independent tests / explicit limits: Snapshot the outcome links map at construction and prevent mutation through getLinks (unmodifiable snapshot or fresh defensive copy); retain null map/null entries so malformed data is rejected by buildTransfer as PaymentException, not a new Map.copyOf constructor NPE. Mutate original payment entry after constructing outcome but before buildTransfer: original destination must be used. Attempt getter-map mutation and verify outcome stays unchanged, accepting either rejection or harmless copy mutation. Preserve null directive/method tests, no URI interpretation and current character whitespace semantics. No new constructor-validation rule.

### exp-v1-java-generation-0030 — reference-fix

Substantive target: Nested DTO mapping with no scalar normalization, full null validation, duplicate order and immutable email snapshot.

Minimal correction / independent tests / explicit limits: Validate email elements by iteration, not contains(null). Map valid List.of(a@b), List.of(), and duplicated immutable emails; preserve order/duplicates, nullable scalar strings and arbitrary age. Mutable list with a null element must still produce IllegalArgumentException. Verify caller mutation cannot change profile and returned list is unmodifiable. No new email syntax/age/name rules.

### exp-v1-java-generation-0131 — reference-fix

Substantive target: Ordered user callback pipeline, null-return failure, list snapshots and locale-independent case conversion.

Minimal correction / independent tests / explicit limits: Validate stages by iteration before copying, accepting List.of() and List.of(stage). Empty workflow returns original string; callbacks remain ordered, null-return rejection and later caller-list mutation isolation stay tested. Keep Locale.ROOT uppercase and existing TrimStage behavior; do not substitute a wider whitespace-strip contract. No new exception policy for arbitrary stage-thrown exceptions.

### exp-v1-java-generation-0138 — reference-fix

Substantive target: Full nested validation, enabled filtering, resource order, sorted duplicate-preserving recipes and deep unmodifiable outputs.

Minimal correction / independent tests / explicit limits: Replace contains(null) checks with element traversal for enabledModules and every recipe list. Test Set.of() and Set.of(m), List.of() and nonempty List.of recipes, including disabled recipe lists that must still validate. Retain malformed nested maps/lists rejection before filtering, resource iteration order, recipe module/string ordering, duplicates, client/server language and deep immutability. No new collection implementation or normalization restriction.

### exp-v1-go-generation-0072 — reference-fix

Substantive target: Deterministic dual-format serialization with key grammar, ordering, format-specific quoting and atomic errors.

Minimal correction / independent tests / explicit limits: Use JSON string encoding for JSON values/keys, keeping strconv.Quote semantics only for FormatLines. Tiny value containing U+0007 (bell), U+000B and NUL must round-trip through encoding/json; assert compact ordered object and final newline, without demanding one equivalent JSON escape spelling. Preserve exact Go-quoted lines, valid UTF-8 values, nil/empty maps and invalid-key/format empty-output errors. No contract expansion.

### exp-v1-java-generation-0160 — oracle-rebuild

Substantive target: Thread-safe atomic ledger with coherent ordered snapshots, length/ASCII validation and no aliases.

Minimal correction / independent tests / explicit limits: Order by original keys, not rendered key=value strings; do not re-sort rendered entries. Exact witness keys A and A0 with values x,y requires [A=x,A0=y]. Original concurrent tests compare entire rendered strings and would incorrectly reject a key-sorted implementation for prefix keys; replace those assertions by parsing at first '=' and comparing keys only. Values may themselves contain '='. Preserve synchronized snapshot coherence, valid empty values and ASCII key rules. Bounded concurrent writes/reads/snapshots with per-writer keys and joined exact final state; clear only at controlled boundaries unless oracle accounts for it. No new scheduling assumptions or promised cross-call transaction.

### exp-v1-go-generation-0084 — reference-fix

Substantive target: Go AST parsing, structural type rendering, ambiguity suppression and destination declaration order.

Minimal correction / independent tests / explicit limits: Fold only ASCII A–Z in eligible field names, not Unicode letters elsewhere in an identifier. Destination Aİ and source Ai of identical type must not match; Aİ should still match itself. Include an ordinary ASCII case match and an ambiguity case so matching and suppression remain correct. Preserve parsing-only scope (not type checking), exact rendered types, embedded/unexported exclusion and multi-name order. No contract decision needed.

### exp-v1-java-generation-0334 — reference-fix

Substantive target: Immutable nested value/list ownership and polymorphic all-part/all-value eligibility.

Minimal correction / independent tests / explicit limits: Validate TemplateField values by iteration before defensive copy; List.of() must construct and canExpand(List.of(field)) must return true. Also valid nonempty immutable Value list, false-template/nonempty-expression rejection, custom Part/null-part false and caller-list mutations. Constructor prose promises rejection but does not name a subtype; do not turn original tests' IAE preference into a newly required subtype. No new rule for empty expression or aliasing immutable Value objects.

### exp-v1-go-generation-0133 — reference-fix

Substantive target: Scoped component lifecycle, uniqueness, sorted filtering and detached output.

Minimal correction / independent tests / explicit limits: Use a structural (scope,name) key consistently in Create/Get/Delete. Create scope a+NUL+b/name c and scope a/name b+NUL+c with different releases; both must exist, list only in their scopes, and delete independently. Keep Quota64, exact strings and empty-field rules. Do not prohibit NUL, trim names, add nil-receiver requirements or change list semantics.

### exp-v1-go-generation-0149 — reference-fix

Substantive target: Pattern parsing, placeholder uniqueness, first-match resolution, exact methods and fresh parameter maps.

Minimal correction / independent tests / explicit limits: Use a structural method/pattern identity. Routes (method GET+NUL+/x, pattern /y) and (method GET, pattern /x+NUL+/y) have the same old concatenation but are distinct valid pairs; construction and both exact resolutions must succeed. Retain true duplicate rejection, slash/placeholder grammar, first-registration priority and copied inputs. No nil-receiver guarantee or identifier restriction added.

### exp-v1-java-generation-0514 — reference-fix

Substantive target: Immutable open/close lifecycle, fresh state, deep list boundary and full-input visibility validation.

Minimal correction / independent tests / explicit limits: Validate every Boolean entry even after a false; [false,null] and [true,false,null] must throw IllegalArgumentException, while false-only returns false and empty returns true. Preserve card validation, unmodifiable snapshot and new close-state identity even when already closed. Original tests require different getCards list identities; immutable list sharing is not prohibited by no-mutable-alias wording, so avoid that extra identity requirement in new oracle. Do not change nonempty cards to nonblank.

### exp-v1-go-generation-0204 — reference-fix

Substantive target: Independent checked generator state, finite exhaustion and detached prefix collection.

Minimal correction / independent tests / explicit limits: Bound allocation by the finite output or grow incrementally. PowersOfThree(MaxInt) must return exactly41 values ending12157665459056928801 with tiny memory; never attempt MaxInt generator outputs. Retain multiple independent generators, permanent zero/false after exhaustion, positive prefixes and explicitly nonnil empty for nonpositive n. No unlimited-memory guarantee inferred.

### exp-v1-go-generation-0234 — reference-fix

Substantive target: Inventory CRUD, canonical textual identity, lexicographic ordering and nested slice ownership.

Minimal correction / independent tests / explicit limits: Validate canonical positive ASCII decimal ID text directly rather than parsing to machine int. Add/get/update/delete ID18446744073709551616; preserve full string and lexicographic order. Keep rejected signs/leading zero/zero/nondigits, no normalization, tag snapshots and explicit empty collection behavior. ID is text with no numeric upper bound; do not add one.

### exp-v1-go-generation-0266 — reference-fix

Substantive target: Whole-input validation before filters, timestamps, sorted cursor pagination and nested copies.

Minimal correction / independent tests / explicit limits: Compute page length bounded by remaining matches before adding to offset. One/two valid records, Cursor1 and PageSizeMaxInt must yield respectively empty/one-row success without overflow. Preserve native-int canonical cursor overflow rejection, full validation of excluded records, inclusive date filtering and copies. Do not strengthen RFC3339 beyond existing time.Parse behavior. Original tests demand nonnil empty rows although prompt only says empty input valid: new tests should assert content/length unless that representation is separately approved; no need to change reference's existing representation.

### exp-v1-java-generation-0794 — reference-fix

Substantive target: Algorithm trace lifecycle, termination pass and nested defensive snapshots.

Minimal correction / independent tests / explicit limits: Record the final no-swap pass even if the last possible comparison pass swapped. [1,2] must yield two [2,1] snapshots; already descending length2 yields one; empty/singleton yield none. Preserve descending numeric comparison without subtraction overflow, input copy and defensive arrays on every accessor plus unmodifiable pass list. For longer cases preserve existing shrinking left-to-right bubble schedule rather than introducing a new trace algorithm; require completion/no-swap evidence without unspecified alternative-schedule oracles.

### exp-v1-go-generation-0326 — reference-fix

Substantive target: Layout validation, consumed-capacity arithmetic, ordered sections and exact serialized totals.

Minimal correction / independent tests / explicit limits: Before adding each positive span and inter-segment gap, compare against remaining capacity; reject mathematical overcapacity even if int addition would wrap. CapacityMaxInt with spansMaxInt and1 must fail; spans1,1 with GapMaxInt fail; single spanMaxInt exact-fit succeeds and ignores unused gap. Preserve raw material/code interpolation (do not invent escaping), order, exact final newline and existing marks rules. No new overflow policy: overcapacity is already error.

### exp-v1-go-generation-0360 — reference-fix

Substantive target: Severity parsing plus full-list validation, stable threshold filtering and copy boundaries.

Minimal correction / independent tests / explicit limits: After existing whitespace trimming, fold ASCII letters only. ParseSeverity(U+0130NFO) and FilterLogs with that minimum must return ErrInvalidLevel (nil filter result), while mixed ASCII INFO passes. Keep empty messages, duplicates, all-entry validation including excluded levels and nonnil empty outputs. Do not narrow whitespace trimming itself or alter severity ordering.

### exp-v1-go-generation-0409 — reference-fix

Substantive target: Optional-field updates, transaction atomicity, original-on-error semantics and pointer ownership.

Minimal correction / independent tests / explicit limits: Look up original value before rejecting an empty code, while still rejecting it and never changing table. A table with key empty-string mapped to a nonzero InventoryItem must return that original item plus error; nil/missing maps return zero. Retain full-patch validation, zero allowed cost, notes clearing, nonblank name/group and no retained patch pointers. No contract decision needed; input table has no valid-key-only precondition.

## Excluded after full read

Four other original prompt/reference/test triples were read but not selected: Go0174 has underspecified AccessEvent/AccessTrail layouts and case-colliding header selection beyond the simple user-ID trim defect; Go0422's cross-field sentinel match is concrete but Unicode case-insensitive substring semantics require separate scope adjudication; Java0400 mixes signed-literal versus unary NEG output conventions and whitespace/numeric parsing that deserve explicit scope before a narrow minimum-literal fix; Java0029's Room student-list null-element policy is not specified although reference adds rejection. These are omitted, not newly held or declared unrecoverable. No additional Java parent is approved merely to fill the two slots.

## Quality and recovery discipline

Small corrective patches do not make the complete selected targets elementary. Each row above names actual interaction/ownership/state/validation behavior rather than padding. All remain standard-library and deterministic-domain tasks; Java0160 additionally needs bounded concurrency verification. Preserve original IDs/hashes and source attribution in separate derived versions. Independent test author sees only frozen specification, not original reference or mutants. Include the exact tiny witness from each row; never count a false oracle or compile error as semantic mutant qualification. Original tests are evidence to inspect, not a license to add missing domain restrictions. Reference-fix leaves unrelated specification bytes unchanged; Java0160 oracle-rebuild fixes both implementation ordering and incompatible test expectations without changing the public promise. Main must resolve any newly discovered contract issue before reserving that row.

## Candidate, source and evidence hashes

Canonical candidate SHA-256 uses sorted compact UTF-8 JSON, ensure_ascii=False, allow_nan=False. Source dataset for all18: Multilingual-Multimodal-NLP/McEval-Instruct, revision57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0, URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct and license URI https://creativecommons.org/licenses/by-sa/4.0/. Every selected candidate has answer/model_training/prompt/redistribution/tests rights=true. Preserve each source transformation plus derived-parent lineage; this does not reopen authorized rights or certify release packaging.

### Binding exp-v1-java-generation-0028

- Candidate canonical SHA-256: `c2548783cf8bb819c5755c51766c243e6cde7bd67abb64cf2b897dba58c273be`
- Source row-12801, SHA-256: `62288bccfb8c26aa64c38da947f52de916155ba6415a085132a17ccef891a807`
- Prompt SHA-256: `c7fadf3cb0fc2d3e88f7a7536dfd9f2ca2e9d784cc17aef614dbc08d2f8a68a9`
- Reference SHA-256: `d0673124d68e8d04c8f29cc36ca387d9787bb91e8f21c4b4cb663a449e3b7082`
- Original SolutionTest.java SHA-256: `775568c0b2c5254f6d65f86d1703268a1f725f2c8239205ab6f145454fb222dc`
- Exact hold: Static hold: the required immutable OperationOutcome retains and exposes its caller-owned mutable links map; final reference fields do not make that object immutable.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_3.md`, SHA-256 `419a273520545d62234e37b05667abd67a042a451792be2eac0f0c8229680f57`.

### Binding exp-v1-java-generation-0030

- Candidate canonical SHA-256: `c40952607491e068206876e006721cddc0a911788062ab205e8dd13f3a7c8c8d`
- Source row-12706, SHA-256: `da17191e8944081e6e9f4048c171068ce5654cc5d3cac4e40c3c858da721db73`
- Prompt SHA-256: `0b898e179321d692abbbcfb08ea3084e78094d6671a1eba959d991defb1a3296`
- Reference SHA-256: `3de5ea06234b92fbe695f70f794ad92fb07258d03ca198d642230f6cde69130e`
- Original SolutionTest.java SHA-256: `83cc3d8fdd8e89476301bfd79099b40ac1bd75f30f73dcce6be01b1a2575a302`
- Exact hold: Executed hold: valid List.of("a@b") emails throws NullPointerException from contains(null), rather than mapping the profile.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/java_0030_immutable_list_probe-result.json`, SHA-256 `3ea879fa98f40b4d51a30bb40e75de78972c2e9a0862ce062432571605f2a607`.

### Binding exp-v1-java-generation-0131

- Candidate canonical SHA-256: `c3d11a95db108914e880e5ce258454deab5ca5d6a2566fe9641fdfecbfd90c93`
- Source row-28116, SHA-256: `cbabfe95656672a309efaaeb658409285de2f95f4b7c46027bbf6fc8b18a6c46`
- Prompt SHA-256: `48613f74c4278d960f81a77a0b3057d0c6b5e30fb6b60298b09cc53653846233`
- Reference SHA-256: `3306b56d80a2b40515868a80426aa42a7ba00940ce2db28cdd8f2a1f89af576c`
- Original SolutionTest.java SHA-256: `610faa2001be7b2530e1f9fd389e589992c4231ba7f4021f5440abc3544803c1`
- Exact hold: Criterion-positive ordered callback pipeline and list ownership; static hold: Workflow(List.of()) throws from contains(null), rejecting the explicitly valid empty-stage workflow.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_13.md`, SHA-256 `4db89546e4622dff087e36bbdaaa16843e82862160b690853ed2278e6e032ff8`.

### Binding exp-v1-java-generation-0138

- Candidate canonical SHA-256: `3379b991c05d86cb5c52636aec64b3e6ba5888517c1c66730e4861cab1122ac6`
- Source row-05775, SHA-256: `5ddfd21fa077ad8dd28ed37c3399b9e06c1001fc1da24011e61eedb11a712608`
- Prompt SHA-256: `1febe7197851c92cc08a9be775c0c308143382127d4e40a9ca3f75d916e0db42`
- Reference SHA-256: `78b7790fd43c551d3f840625a3a6607df98e22b0f29f744c2be41e9b206ae585`
- Original SolutionTest.java SHA-256: `832162c5af0111427c5850e8609859fd06cddbbef9b29aa19f2ab564e1324966`
- Exact hold: Criterion-positive full nested validation, filtering, ordered duplicate-preserving recipes and deep snapshots; static hold: valid Set.of enabled modules and List.of recipe lists are queried with contains(null), which may throw rather than accept valid inputs.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_14.md`, SHA-256 `0be82513eff60ea85795fcf79a04527be1634fcca99a374cc2f0dbeb13a0bdbb`.

### Binding exp-v1-go-generation-0072

- Candidate canonical SHA-256: `324059f2ab4588d324dd392c8a09206050c98db6a903c813c0449725896146a6`
- Source row-27650, SHA-256: `64e46612151581ffc599323902438ca8622ed940ead8971808a6ba8364ca56b9`
- Prompt SHA-256: `5aca25a54083279b9c717518b0231ccf1661514e9c98c0dfec6f448c8ad90635`
- Reference SHA-256: `a608bd32584a8a1e2b70f169adb678d1a721c34d08765019107f3bb7f47dc7ec`
- Original solution_test.go SHA-256: `06febc007c74f799754e594e786b4ea11edc0c80979724b3056f0c6725551a21`
- Exact hold: Executed Go-only string escape produces invalid JSON for valid control-character input.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_6.md`, SHA-256 `e8a87bbddde64727a5fa0e81504d19baff9b9dff8e6e442eb2097fee4349d0db`.

### Binding exp-v1-java-generation-0160

- Candidate canonical SHA-256: `e2711ff7dc04c71ddb43b6eb631c7d0f01c9be76c40d815ce30b150606739cd3`
- Source row-12743, SHA-256: `98e88de7a7b82b8b613ad0b16ea76adc2747ee5d32ae6a0ae6afe976a90a5426`
- Prompt SHA-256: `5b524a114301b0170e5a2417976159d11da7940c986f519dd10483721cd4ab81`
- Reference SHA-256: `12c7fd6af703cbf551a20c8551a4953956a23784343bfe5ba66a1a391e37ffa3`
- Original SolutionTest.java SHA-256: `e93da8d71bc74833d2bb2d2c752977b27e3bdee6fc42b9a7de0c8d2ca8a2ff2a`
- Exact hold: Executed behavioral hold: snapshot sorts rendered key=value strings and returns [A0=y,A=x] for keys A and A0, violating key order despite the underlying TreeMap being correctly ordered.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_16.md`, SHA-256 `275ca337a08b23d7d25b9635a4739717b3b42f7719f0d8dbf3dfc36e39588985`.

### Binding exp-v1-go-generation-0084

- Candidate canonical SHA-256: `4880da15d57b6cae3153e1410178ca61728e95848149fcf63cb1c0381b20bc29`
- Source row-16327, SHA-256: `b00b27a7643b1a45d9a443de7cf66eb52b5c6ac30a862c5dcaac41841158327a`
- Prompt SHA-256: `080bab2c76e72435702004e7df92370d69e029659bea30006a5666b3618b3dc7`
- Reference SHA-256: `c5f9a2c7f066d21033ebc8cdb20dfbfdce3c6d98be36a1dad6f2a55def4364d8`
- Original solution_test.go SHA-256: `89fea6b701a32bad4ac7875ccd9de25299dd5841c73d137f4bc4e7ffcbfd0e67`
- Exact hold: Executed Unicode folding contradicts the ASCII-only field matching contract.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_7.md`, SHA-256 `d659c4ccda2f5e666390f4c6cd847efbd42e1342c228513625a4a743e037d38f`.

### Binding exp-v1-java-generation-0334

- Candidate canonical SHA-256: `be6d2e7e2caae0d7d304468e62589d654ad0cba8d89c10aa040a7854512299d6`
- Source row-12788, SHA-256: `dd3e84f742a4a159843083d2bd2c4f485a38a54e6d7153bb2ed4e6e1d84e9e52`
- Prompt SHA-256: `1361c6803cc1b519191634c0c3869c65ec3de58c10d73205f49b7e6c43c922aa`
- Reference SHA-256: `06c415f96ae36c0633123ce9f5285bd294d8087efbfcb4c4dff648d8c85fe868`
- Original SolutionTest.java SHA-256: `8f1b09d46612f968440028cb0132ae2c21f608ef434b02651cdefadd689576d2`
- Exact hold: Static hold: TemplateField(List.of()) queries contains(null), which throws on valid empty immutable Java lists. Same candidate-bound defect family as the previously executed List.of null-query probes; this candidate was not executed.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_32.md`, SHA-256 `a6b054425c5dbf0b7e7d44238626a3cdc3125569cd2cce656d3cf54444663445`.

### Binding exp-v1-go-generation-0133

- Candidate canonical SHA-256: `001f7a5e4245bb8e664d489f74364def16276ca5bb674f1691e5cf6250f330c0`
- Source row-16388, SHA-256: `fb9276729b5cc80028d85ada36a2d26dfcd0c852c4d5196f79b38703d09e11ed`
- Prompt SHA-256: `278f1bd5158f697c67b03559b158b46ca65fbb400a22f0ca9998661e272ae767`
- Reference SHA-256: `67228f131faedcf77df5cd2c87877fb8406244865f7b08de3ea12615c470314e`
- Original solution_test.go SHA-256: `9966d6f7d714186412deb9dfca3a9e3ac1313f7264324745ab1dc24ddd5b98f8`
- Exact hold: Executed collision of distinct scope/name tuples containing NUL.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_11.md`, SHA-256 `1c0222dce13bf4c2cbabe6c75545d4f4a9bcfdff6b1adf2d53ec72c99f54249f`.

### Binding exp-v1-go-generation-0149

- Candidate canonical SHA-256: `ced5e779da6d43dfa9e1cb49213bcbda6f2b6351f2e9063a742ac79537fb564c`
- Source row-27558, SHA-256: `7d861fa39ec26b881e4283babb0fe2b7ce13ba805b275778eebf9da2a507cc3e`
- Prompt SHA-256: `9a7c67bf984186e968d52f0a9de94082e766f111d20cc45cb483f78554cabc8f`
- Reference SHA-256: `ebc162a56670da62521ae600a8f448452137acb403166dd064723f6f9d286a6b`
- Original solution_test.go SHA-256: `74103c2badf0e7a20ffb7594b8bbc604b52c18fed1bade3b08187e58b3fe70c7`
- Exact hold: Static identity collision: distinct permitted method/pattern pairs share the NUL-delimited key.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_12.md`, SHA-256 `896f4eb07e7c576b210f6f3635aa8431e604d32883fa9a54656b5f8004311296`.

### Binding exp-v1-java-generation-0514

- Candidate canonical SHA-256: `5ef6a582d84ffca6da4e08f8b72b6d53050c19c2f39a2f79dff17d7ec70f49b5`
- Source row-12859, SHA-256: `f182b2fff4ccbef27000f803c14502595d13bf7b47a161970e6d148d04abc49d`
- Prompt SHA-256: `1307b9939bd0f1470c433e6cce5e33bfa904e091ecae87fd4783eb4f411c4461`
- Reference SHA-256: `848aee622f56fe766420e96445d3c1e7c0f4a596e42e983a9b5dca9afd52e6f0`
- Original SolutionTest.java SHA-256: `c311e5bde9db9a3b84a9a1f1dd09d04ccc84a35158cb0dd288592e1a854659db`
- Exact hold: Reference short-circuits false before validating a later null visibility entry.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/visibility-null-result.json`, SHA-256 `f6d4b023b9c1b6534f4a85d015f69fc90a8b1134a45b3070df16af4423841db7`.

### Binding exp-v1-go-generation-0204

- Candidate canonical SHA-256: `b0911cfea3b4bfeaa79feffc2e1ef1fee103e28aba5320515d0cbdaebcd6b5ce`
- Source row-16354, SHA-256: `09349138b994b5c18ab98cccc2c9c01ec0be86ef67bacfb114cf2e2eb8ded28f`
- Prompt SHA-256: `e9e812bc007a21c737711dc24f594f97ada4b259f4255cf1a9bdb1ac8d48eba2`
- Reference SHA-256: `a8c44ed562a5dfece2390acde8a50f0aaae05a4a652dba9f0786e3f6f97f3530`
- Original solution_test.go SHA-256: `be927faab716391609a320461a1c6252b5c53bcc0f1d98060e12c9758cca2d33`
- Exact hold: Executed unbounded allocation panic for a finite 41-value generator output.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_16.md`, SHA-256 `ed948ebecd69937b90d9a454a2971d2678e872fe81a6ef28ef40e62e62e3bd7f`.

### Binding exp-v1-go-generation-0234

- Candidate canonical SHA-256: `f743b378be9f7bcb536e86973669c1cbead45f0b1556d79cc8077f14c19682cb`
- Source row-16024, SHA-256: `ed2c415ddf87fc00c1fb1bff954cad48fba6f081ab5df1adfa8d0a70dd2fb508`
- Prompt SHA-256: `08adeaf5405cac0c74c03549e6946a071f48af69f21612c9cd5f5db2e89bd8aa`
- Reference SHA-256: `a6c39329331ac0019e4af76d6cc154016b1ab7854603052f6b96ab8ace15c6bc`
- Original solution_test.go SHA-256: `5563d0beef3a0e28637b7ac78f23c6a8f5f5a063e178e985381c2957d37743f2`
- Exact hold: Executed canonical decimal string ID rejection outside unnecessary machine-int bound.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_19.md`, SHA-256 `ab17bc6d7e0f3a144ffb29784ee1b78ce8d00e47431735fd7d3b806c1d7c210c`.

### Binding exp-v1-go-generation-0266

- Candidate canonical SHA-256: `16aab2d4078c16d399336e6fba8bccb6c41a7162f2f2093fe95fc30c7428a122`
- Source row-27933, SHA-256: `ab17b5ffffac705bf869be22178b87c4b871154953c844fad7a15ace67ab4574`
- Prompt SHA-256: `25eec8015b99b6c362e7a4e00698f12668abe810cf7dcaacc4e46559dc0cbc9f`
- Reference SHA-256: `a1357433313a59a97eb96dd15c6a27a91bed22a4727cc400d06fdc95a9ce6f2c`
- Original solution_test.go SHA-256: `d14143c193fe0975a55437e5741e034f3bd74ac429192e3337124600a0ed7fd2`
- Exact hold: Criterion-positive pagination and validation task; executed behavioral hold for signed page-end overflow.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_21.md`, SHA-256 `5e99953ccd76c1620a462ca4025f0ff81c27273eff33eeab5ae55dd42407a746`.

### Binding exp-v1-java-generation-0794

- Candidate canonical SHA-256: `e132eff2265708d2eb48c495be45e4948895a01dfc993679cba70c0e9aa3e205`
- Source row-05778, SHA-256: `ff90f742a493df2c31740627ce0a0ce4066bc9042dc7bbba29c39f9dda07bcb7`
- Prompt SHA-256: `84e9d7721c3147a5aa78db5d14afd7e336b2bdb8fc4909339c04a496f5241456`
- Reference SHA-256: `a8715cd3a6ec2c5a844a8ef8e30874ca4467647b3340b0def2a0312d092212d9`
- Original SolutionTest.java SHA-256: `f1deb1a5b46ec5cc710ad27311d747aae9a7eabba59daa1489e10d9726fd62bc`
- Exact hold: Reference omits required final no-swap pass after last possible swap pass.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/sort-final-pass-result.json`, SHA-256 `24d7dcfc9e5e4e6e1ed17a8e8d28d9b9d6cbc0c3f39d049baef6f25ab6d2be51`.

### Binding exp-v1-go-generation-0326

- Candidate canonical SHA-256: `643ed0c3f460d89800673636d0609ac2250861752908ecb56f713e0ed0737198`
- Source row-27592, SHA-256: `bac2bf7e045a0e74c24de49502e2f7b8e0d6c496852577d089e1033cc3e627ce`
- Prompt SHA-256: `27b49d1da63279c5a563c33db59445f9b0a302ebb4520388f79629af6453be4d`
- Reference SHA-256: `045ab73fd3bb5bdd5ce0b8bb74dff911df74137d342cde3df6bce77482c76ffd`
- Original solution_test.go SHA-256: `b852e0b574ce2a71071a4d0c69327cb8134769384b545a45ac56c9f4f223fd02`
- Exact hold: Criterion-positive layout validation/serialization; executed behavioral hold: span sum wraps and bypasses capacity rejection.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_26.md`, SHA-256 `0635874594f827dc82736b76ab44bd29ec7c102f5e0224fb899a831185df1b48`.

### Binding exp-v1-go-generation-0360

- Candidate canonical SHA-256: `64b45b8fc1a1ce9398a14fb2e1bee722871bd506168b02d7dc1f2a95efe05846`
- Source row-16165, SHA-256: `0f63b789406e6aa6a42aef17a260a48f94c7ba543cd0869e4f2055e55556190e`
- Prompt SHA-256: `5fc2df7593c4518ab20f0a229bce250148172018bf5ed9bc7ea494b6b888dc4b`
- Reference SHA-256: `27f0a0e4a2fcf194a8096273ae3d9c1c36674eda77da1830c6b323a023687397`
- Original solution_test.go SHA-256: `0be0628557943604e305ffb78b07d9050f62f3214a7b53a0f588f1cf11c861ec`
- Exact hold: Criterion-positive full-input severity validation/filtering; executed behavioral hold: Unicode dotted-I accepted despite ASCII-only case-insensitive parsing.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_28.md`, SHA-256 `6a27a803269ffa76cf451506a2c2847939b34db1d6581cc88f27a1b84161a8b5`.

### Binding exp-v1-go-generation-0409

- Candidate canonical SHA-256: `a9adb8cd38d9b6a6d8c6217e807c6139a9cd7939785e1234255c9cbf581ed5a8`
- Source row-27838, SHA-256: `8899c769f9ffec50841fee8bd2b11c552352f69d5cce428b0ab75ae0a41c8797`
- Prompt SHA-256: `c828c29d44f4df3de7a6230a332aa3875208275ab9facd92c732851208b6c8ff`
- Reference SHA-256: `7444cadb0424c9163e99313a043a735cf4037436f92fcbf1ab6b400bebc43111`
- Original solution_test.go SHA-256: `2d6bb4cda63c596dea523e47faa96e83c5298ea637d061198fb785d9b3bcec03`
- Exact hold: Criterion-positive partial-update ownership/atomicity; static behavioral hold: empty code returns zero before lookup even when table contains that key, contrary to original-item-on-any-error requirement.
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_32.md`, SHA-256 `e6f9fedf7642193c6da0f81c377fdf70c89d6975e7b608a27524b49630f3c64d`.

## Frozen selection inputs

Original corpus: datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl, SHA-256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

Additive hold ledger file SHA-256 at selection: `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee` (measurement/data/expansion-v1/cutoff-5885-review/additional-holds.json).

Reserved plan exclusion manifests:

- `datasets/cache/expansion-v1/versioned-recovery/r1/plan.json`: `a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1`
- `datasets/cache/expansion-v1/versioned-recovery/r10/plan.json`: `728e70ee23ad46f8a4a8aec64a34d74b48c073a5382849fc52ce449154f2afb5`
- `datasets/cache/expansion-v1/versioned-recovery/r11/plan.json`: `2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6`
- `datasets/cache/expansion-v1/versioned-recovery/r2/plan.json`: `5dae7eac34ac462f6173dc6b740364d5c4b68129950359f453f4038111ad1d29`
- `datasets/cache/expansion-v1/versioned-recovery/r3/plan.json`: `cbad9d14a504531e749b5eb3433f0bf4670e21f2a8e8d5f310d2e843e53c6231`
- `datasets/cache/expansion-v1/versioned-recovery/r4/plan.json`: `8a6137773e65e1a55e5eaceed9a8c2e40153b5759a46a5189ba6a488d530d58c`
- `datasets/cache/expansion-v1/versioned-recovery/r5/plan.json`: `778e0071bec56248081e741f4c742d522c75b4b006e069d8301b75440c2732ec`
- `datasets/cache/expansion-v1/versioned-recovery/r6/plan.json`: `803f0308b33b4b8a834347d5976a148bc66001d6fc8606a1e206fb0e2b4a6795`
- `datasets/cache/expansion-v1/versioned-recovery/r7/plan.json`: `f0a3b5d14eb983206ac83c99571c5522925feaf7ac0443ec3c59ad172d5f293e`
- `datasets/cache/expansion-v1/versioned-recovery/r8/plan.json`: `1a579af9da9d542d6bb4f03c8fbc030fd0b9d3102a31c347cd631bfc18b873de`
- `datasets/cache/expansion-v1/versioned-recovery/r9/plan.json`: `0f0d6e653bbabff308a912cc764d1373b20faf3f4cf68a4c7341c94f36b5ae79`

