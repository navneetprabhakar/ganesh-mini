# R12 Java independent quality review — 2026-09-08

Gate 2; isolated static review of eight derived generation candidates, no execution, admission, new original coverage, central edits or cloud activity. Full original and derived prompts/references/tests/mutants read. Scope follows the R12 plan, RECOVERY_R12_SELECTION_20260908.md and RECOVERY_NEXT_GO_JAVA_20_20260908.md. Result: **2 scoped positives, 6 holds**. Static reference correctness is not an executed pass; main owns sandbox directionality and admission.

## Individual dispositions

| Java suffix | Decision | Substantive basis and blocking findings |
| --- | --- | --- |
| 0028 | HOLD: invalid oracle | The immutable OperationOutcome now snapshots links with a LinkedHashMap and unmodifiable wrapper, retaining null maps/entries until buildTransfer can throw the required checked PaymentException. Method/destination snapshots and opaque destination semantics are intact. Caller-map mutation followed by outcome getter inspection genuinely detects the original alias. However testImmutableSnapshots insists getter put must throw UnsupportedOperationException. A fresh defensive getter copy is expressly allowed by approved scope and satisfies immutability. Accept either rejection or harmless copy mutation, then recheck the outcome. Also move a source mutation before buildTransfer to directly test that boundary. Do not change the sound reference to satisfy or expand this oracle. |
| 0030 | HOLD: missing repaired witness | Reference element iteration correctly accepts null-query-hostile immutable lists and preserves nullable scalar strings, arbitrary integer age, duplicate order, defensive emails and unmodifiable output. Tests exercise ArrayList email sources but never List.of. These valid fixtures do not distinguish the original contains(null) mutant. Add valid List.of(), List.of("a@b") and duplicate immutable emails, retaining mutable-null rejection and scalar preservation. |
| 0131 | HOLD: missing repaired witness | Ordered callbacks, list snapshot, empty identity, null-stage/null-return checks, trim and Locale.ROOT uppercasing remain coherent; test restores locale in finally. All valid stage collections are Arrays.asList, ArrayList or Collections.emptyList, never List.of. Add List.of() and List.of(stage) to distinguish original contains(null). Do not broaden trimming or arbitrary callback exception semantics. |
| 0138 | HOLD: missing repaired witnesses | Reference traverses enabled modules and every recipe list rather than querying null; complete nested validation precedes filtering, sorted recipes retain duplicates, resource iteration and language behavior remain intact, outputs deeply copied/unmodifiable. Tests use LinkedHashSet/Collections sets and Arrays/Collections/ArrayList recipe lists; no Set.of or List.of. Add separate empty/nonempty Set.of and List.of cases, including disabled recipe lists so both repaired sites are witnessed. Existing ownership and invalid-disabled-input assertions are sound. |
| 0160 | HOLD: concurrency test gap | Reference synchronizes all ledger operations and emits TreeMap key order directly. Explicit A/A0 oracle genuinely detects rendered-string sorting, with values containing equals and first-equals parsing correct. Eight workers write/read distinct keys, joined final state checks 800 entries. But no snapshot runs until every worker joins: coherent in-flight snapshots are untested despite approved scope. Worker AssertionErrors are uncaptured; a read failure on the last write can leave the final state complete while main succeeds. Capture worker failures and rethrow after joining; add bounded concurrent snapshots with key-only order/uniqueness and feasible per-writer prefix/value checks. Use a start barrier and finite loops; do not demand specific scheduling, cross-call transactions or concurrent clear behavior. |
| 0334 | HOLD: missing witness and invalid exception oracle | Reference iterable validation and immutable Value/list ownership support all-part/all-value eligibility, false-template and nonempty-expression rejection; custom/null parts remain false. Tests contain no List.of values and therefore do not distinguish original null query. Add empty/nonempty List.of construction and canExpand. Constructors promise rejection but not IllegalArgumentException specifically; test helper expectIllegalArgument adds the exact subtype expressly excluded by approved scope. Permit legitimate null rejection such as NPE, without catching assertion failures as successful rejection. |
| 0514 | SCOPED POSITIVE | Full Boolean traversal now rejects [false,null]; the independent test uses that exact small witness and verifies no input mutation. Mutable card input cannot alias state, returned cards are unmodifiable, repeated close creates a new closed state while old state stays open, and a nonempty whitespace card is correctly accepted. Removed original unsupported distinct-card-list identity assertions. Empty/all-true/mixed-false coverage remains sound. [true,false,null] is a useful additional variant, not necessary to distinguish this mutation given the exact [false,null] witness. |
| 0794 | SCOPED POSITIVE | Shrinking left-to-right descending bubble passes now continue through the final no-swap pass, including the exact [1,2] two-snapshot witness. End bound stays at one for final comparison; no subtraction overflow. Empty/singleton, already sorted, duplicate, integer extrema, input isolation, accessor-array copies and unmodifiable pass list are tested. Complete target is trace lifecycle plus nested ownership, not merely an elementary comparison replacement. |

## Seven criteria

Prompt clarity and public API are adequate within the approved scopes; 0160's new text only makes original-key order and equals-containing values explicit, as approved. Tests must not convert unspecified constructor exception subtype (0334) or harmless getter-copy mutation (0028) into public requirements. Independent test origin passes for all eight. Entire-target non-triviality is supported by interacting validation/ownership, nested mapping/filtering, callbacks, concurrent state or trace lifecycle; small repair size alone is not the basis. References are idiomatic standard-library Java and dependency-isolated. Each mutant is the exact original reference and represents a realistic identified defect; realistic-failure qualification is blocked for 0030/0131/0138/0334 because the distinguishing immutable-collection fixture is absent. 0160 has a real ordering witness but lacks the promised concurrency verification. No additional static reference defect found in this bounded review.

## Exact provenance checks

For all eight, canonical original parent hashes match plan records; plan parent source and rights match originals; derived source retains dataset, URI, license, license URI, revision, record ID and source-record hash, with the versioned recovery transformation appended. Rights remain unchanged with answer/model_training/prompt/redistribution/tests all true. This preserves existing approval, not a new external rights determination.

Shared source: Multilingual-Multimodal-NLP/McEval-Instruct, CC-BY-SA-4.0; revision 57bd46727e49ac3e2890218a146d35c2454a8496. URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct ; license URI https://creativecommons.org/licenses/by-sa/4.0/ .

Seven reference-fix specifications are byte-identical to their originals. 0160 is the approved oracle-rebuild clarification. All eight derived mutants are byte-identical to original references. Architect output problem/reference_code/known_bad_code exactly matches emitted fields. Independent author receives only eight id/problem objects plus generic Java test instructions, no reference, mutant, source tests or architect context. Each emitted test equals author test_code plus exactly one trailing LF, not arbitrary post-author editing. Architect and independent-author prompt/output hashes recomputed successfully; both returncode 0, timed_out false, disallowed_tool_item_types empty. Provenance does not cure deficient oracles.

Paths relative to repository root; SHA-256 hashes:
- measurement/data/expansion-v1/recovery-plans/r12/plan.json: 0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121
- Plan logical plan_sha256: 3edbe358f89bc7396eb1ae1c694acf685213164bda40030cf54c5c033467f78d
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_SELECTION_20260908.md: 58b6a5cb6646e03ba4ae0d103b51ff638ea4e3f6b847711c232f09dec8424916
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_20_20260908.md: 986b3dba391e9903b743d680f6b5b94071a3292c37c00a4930a998a00d6b586d
- r12/java-recovery-architect-evidence.json: e48e6a40e11c8aa70c141ca3455a0d14277c187c5332bfc5bf8b2275cd2dd8c4
- Architect prompt/output: 08fab10d9e831b932839dfc21d1f3237dc1808a3a42addda4bb68cfc6df84bdf / 0702fb718d45e75cf40f28103af4615f984fb7d771636f53e9b280401356f2d9
- r12/java-recovery-independent-tests-evidence.json: e7ecf97e1f74309b2fe1b45a949b0828279935f6a1c72a9e9206700e155711d5
- Independent prompt/output: 7062bb4145c9354c97cf54d8c15fc8eb49aa1c82f05d16bdb356b851ad7c1e1c / 9eefd352372a06d0cc9f4a85a004e77f5eb127da0456acc8f1e8cc679dc3fb5c

## Per-artifact bindings

Candidate and author paths use datasets/cache/expansion-v1/versioned-recovery/r12/. Candidate filename is the full ID followed by .candidate.json. Prompt/reference/test/mutant hashes below cover exact emitted text; parent_canonical uses recursively sorted compact JSON. Source IDs/hashes bind individual stimulus rows.

### exp-v1-recovery-r12-java-generation-0028

- candidate_file: `57f5cc2470db4ed7fa275fbc59baa5507edb356825b53f82345d61569afd8f35`
- parent_canonical: `c2548783cf8bb819c5755c51766c243e6cde7bd67abb64cf2b897dba58c273be`
- prompt: `c7fadf3cb0fc2d3e88f7a7536dfd9f2ca2e9d784cc17aef614dbc08d2f8a68a9`
- reference: `28d74955d709023ea486cf9357d1fdc6172ed9662adf8279796410a28b8066a7`
- test: `bcfedfae5ef225ef71eee8b7b0988947484b17ce31607c7298b5c6571a092beb`
- mutant: `d0673124d68e8d04c8f29cc36ca387d9787bb91e8f21c4b4cb663a449e3b7082`
- source_row: `row-12801`
- source_record_sha256: `62288bccfb8c26aa64c38da947f52de916155ba6415a085132a17ccef891a807`

### exp-v1-recovery-r12-java-generation-0030

- candidate_file: `1838895c1799b697fd643cabb41d4bfc12f4c4fc35a0ff0baa6fb310bcf89d00`
- parent_canonical: `c40952607491e068206876e006721cddc0a911788062ab205e8dd13f3a7c8c8d`
- prompt: `0b898e179321d692abbbcfb08ea3084e78094d6671a1eba959d991defb1a3296`
- reference: `0093352549231fdbbc04028644ad76611ca7fbb47a474ee9d6809a7dafea9227`
- test: `208a13e3f3a5c3a69c5619eeb308778148d2276c8272be4070a5fc2d74d49414`
- mutant: `3de5ea06234b92fbe695f70f794ad92fb07258d03ca198d642230f6cde69130e`
- source_row: `row-12706`
- source_record_sha256: `da17191e8944081e6e9f4048c171068ce5654cc5d3cac4e40c3c858da721db73`

### exp-v1-recovery-r12-java-generation-0131

- candidate_file: `6c5cb01bbbd24606f3b41f06b4c134f72265b5cfa9969c0a77733afe9376ec94`
- parent_canonical: `c3d11a95db108914e880e5ce258454deab5ca5d6a2566fe9641fdfecbfd90c93`
- prompt: `48613f74c4278d960f81a77a0b3057d0c6b5e30fb6b60298b09cc53653846233`
- reference: `604bc8a45d2585ad162c5be4864c5019efa3e4338331a0cbcb61888082f29e16`
- test: `06ad5cea332e210dbe2d32149e4038da1e8f91051a3d839a1efbc6f7f476816c`
- mutant: `3306b56d80a2b40515868a80426aa42a7ba00940ce2db28cdd8f2a1f89af576c`
- source_row: `row-28116`
- source_record_sha256: `cbabfe95656672a309efaaeb658409285de2f95f4b7c46027bbf6fc8b18a6c46`

### exp-v1-recovery-r12-java-generation-0138

- candidate_file: `323df69c9451064d9e507ba2323d92c800d35041f06bc67328078b170449b9e4`
- parent_canonical: `3379b991c05d86cb5c52636aec64b3e6ba5888517c1c66730e4861cab1122ac6`
- prompt: `1febe7197851c92cc08a9be775c0c308143382127d4e40a9ca3f75d916e0db42`
- reference: `26fdb37459d0f33d32fab79c27e56f0df409e887ccc647b71df7b85074bb7799`
- test: `19b14e6f565ebdb9116b29db117691763bd140aab81279e05397df6ef0b33c32`
- mutant: `78b7790fd43c551d3f840625a3a6607df98e22b0f29f744c2be41e9b206ae585`
- source_row: `row-05775`
- source_record_sha256: `5ddfd21fa077ad8dd28ed37c3399b9e06c1001fc1da24011e61eedb11a712608`

### exp-v1-recovery-r12-java-generation-0160

- candidate_file: `de65d17791fca742c7b00c9a433e6857306e9b4f15dc1afe21c6b002e4ed4850`
- parent_canonical: `e2711ff7dc04c71ddb43b6eb631c7d0f01c9be76c40d815ce30b150606739cd3`
- prompt: `4124fced52ca68bcb817ae63ad62a41a663289e89353b79e8cad2714539caede`
- reference: `9074e92c141e44be3613cba122bd8c72c70481a2a3d88a998e785a3ce4a0944d`
- test: `6cd3d79f35d8cc62c30dd80f5649ef9b08757356475780168eef396d78566c67`
- mutant: `12c7fd6af703cbf551a20c8551a4953956a23784343bfe5ba66a1a391e37ffa3`
- source_row: `row-12743`
- source_record_sha256: `98e88de7a7b82b8b613ad0b16ea76adc2747ee5d32ae6a0ae6afe976a90a5426`

### exp-v1-recovery-r12-java-generation-0334

- candidate_file: `2c30b40acd7d47d03340ba08d2c214086c3e0b2b326397df19a6c8f1a4c18a8d`
- parent_canonical: `be6d2e7e2caae0d7d304468e62589d654ad0cba8d89c10aa040a7854512299d6`
- prompt: `1361c6803cc1b519191634c0c3869c65ec3de58c10d73205f49b7e6c43c922aa`
- reference: `b621094918c9e1f58f2aa748c1eda4df07fa30b2dd6658da21924c6fb4770260`
- test: `46da479be8a50d130f3f2a995ec37fc586b2ff3cbfd495fb75cb0f58db232461`
- mutant: `06c415f96ae36c0633123ce9f5285bd294d8087efbfcb4c4dff648d8c85fe868`
- source_row: `row-12788`
- source_record_sha256: `dd3e84f742a4a159843083d2bd2c4f485a38a54e6d7153bb2ed4e6e1d84e9e52`

### exp-v1-recovery-r12-java-generation-0514

- candidate_file: `874dd746f094cfcfa15d5b7cc6a479c59a931260192bc6a648bd53001b8ddcd2`
- parent_canonical: `5ef6a582d84ffca6da4e08f8b72b6d53050c19c2f39a2f79dff17d7ec70f49b5`
- prompt: `1307b9939bd0f1470c433e6cce5e33bfa904e091ecae87fd4783eb4f411c4461`
- reference: `81105364c0f6efbf3971702ec957ebde78a6b4482ef5f8bdda2bfbd29373a315`
- test: `250e06d478942d829a58a3ec10dadedbc8be671875a21a529abea3679a48f31e`
- mutant: `848aee622f56fe766420e96445d3c1e7c0f4a596e42e983a9b5dca9afd52e6f0`
- source_row: `row-12859`
- source_record_sha256: `f182b2fff4ccbef27000f803c14502595d13bf7b47a161970e6d148d04abc49d`

### exp-v1-recovery-r12-java-generation-0794

- candidate_file: `0bb0dafcad947fa1c833992fec8a922d32b8b3002793365bf70cae7ddcb33d96`
- parent_canonical: `e132eff2265708d2eb48c495be45e4948895a01dfc993679cba70c0e9aa3e205`
- prompt: `84e9d7721c3147a5aa78db5d14afd7e336b2bdb8fc4909339c04a496f5241456`
- reference: `b21fd06bbb0096654d7c0c85c3f0833ee9c229b5bdaa1e126851f4a1c9880cb8`
- test: `1c3493dae0da2c000c97b2398fa7a7588db5682a5bfef2419f32dab584c48e2c`
- mutant: `a8715cd3a6ec2c5a844a8ef8e30874ca4467647b3340b0def2a0312d092212d9`
- source_row: `row-05778`
- source_record_sha256: `ff90f742a493df2c31740627ce0a0ce4066bc9042dc7bbba29c39f9dda07bcb7`
