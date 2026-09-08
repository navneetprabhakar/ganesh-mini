# R15 Java terminal correction quality review — 2026-09-08

Gate 2, isolated static review of exactly six derived Java generation candidates: 0028, 0030, 0131, 0138, 0160 and 0334. Full derived prompts, references, tests and known-bad implementations were read; unchanged R12 contracts and prior review evidence were reconciled. No candidate execution, generation, admission, cloud activity or central mutation occurred. Zero new original-record coverage.

## Decision

Five scoped seven-criterion positives: 0028, 0030, 0131, 0138, 0160.
One terminal derived test-quality hold: 0334. No reference defect found in these six. Originals remain held; this is not admission or a sandbox result. The one correction has been consumed; do not schedule another automatic critic.

| Derived candidate (prefix exp-v1-recovery-r15-java-generation-) | Disposition | Defining evidence and remaining issue |
| --- | --- | --- |
| 0028 | Scoped positive | Caller links mutate and clear after outcome construction, before transfer construction. Fresh getter and subsequent build retain the original payment. Getter mutation may either throw UnsupportedOperationException or harmlessly modify a defensive copy; the prior representation overconstraint is removed. Alias-retaining mutant is directly distinguished by the construction snapshot. Malformed null outcome/directive/method/links/payment remains a checked PaymentException obligation, with opaque destinations preserved. |
| 0030 | Scoped positive | Actual List.of() and singleton/duplicate immutable email lists now succeed, preserve order/duplicates, and distinguish the contains(null) mutant. Mutable null-element rejection, nullable scalar strings, min/max integer ages, nested address mapping, caller isolation and explicitly unmodifiable output remain covered. No email grammar or concrete internal-list requirement is added. |
| 0131 | Scoped positive | Workflow(List.of()) and Workflow(List.of(stage)) succeed with empty identity and singleton callback behavior. These directly distinguish immutable-list contains(null). Ordered callback composition, defensive stage snapshots, null list/stage/input/callback-result errors and locale-independent uppercase remain covered; Turkish default locale is restored in finally. No callback exception or broader trim policy is imposed. |
| 0138 | Scoped positive | Actual Set.of() and Set.of("m") inputs, empty/nonempty List.of recipe lists and disabled-module immutable recipes are accepted. Filtering preserves resource iteration order; module/recipe sorting retains duplicates; all nested inputs are validated even when disabled/server-side. Deep snapshots and every explicitly unmodifiable output level remain tested. Both immutable set/list null-probe failure paths are represented, without requiring unsupported private layout. |
| 0160 | Scoped positive | A/A0 exact key-order fixture still distinguishes sorting rendered key=value strings. Eight coordinated finite writers use unique keys and exact values containing equals; main samples snapshots while workers run, parses first equals, checks unique sorted keys and each writer's prefix closure, then joins and checks every final entry. Every worker Throwable is captured and propagated. No cross-call transaction or particular interleaving is assumed. Runtime/scheduler liveness is not statically proven; the external sandbox timeout remains authoritative, not a new timing oracle. |
| 0334 | Hold: oracle narrows unspecified exception class | Real List.of empty/singleton value and immutable part-list witnesses now distinguish contains(null); false flags, nonempty expressions, custom/null parts and defensive list ownership remain meaningful. However expectNullRejection catches only IllegalArgumentException and NullPointerException. The frozen prompt says only constructors reject null arguments; the approved correction explicitly says no subtype is named. A constructor rejecting a null expression with an ordinary RuntimeException satisfies that rejection wording yet is rejected by this helper. AssertionError is correctly not swallowed, but the subtype whitelist remains unsupported. Reference itself is consistent; this is a test-oracle hold, not a claimed execution failure. |

## Seven criteria

Prompt clarity and API consistency: complete public contracts and reference signatures remain as approved in R12; R15 changed neither. The sole residual inconsistency is 0334's test-only exception whitelist, not an implementation/API defect. No public traits/accessors or private layouts were invented.

Independent test origin: all six are independent_teacher. The archived correction prompt's six Items contain exactly id, problem and prior test_code. Each problem equals the frozen derived prompt and each prior test equals R12's test bytes. There are no reference or known-bad fields in these generation-task author items. The specification feedback is bound separately; independent provenance does not excuse the 0334 oracle.

Non-triviality: the complete targets combine checked validation with immutable ownership (0028), nested DTO/domain mapping and collection validation (0030), callback composition and stage ownership (0131), globally validated filtering/sorting/deep copying (0138), coherent synchronized mutable state and output ordering (0160), and nested predicate/type dispatch with construction ownership (0334). Small null-probe corrections do not turn these complete targets into elementary padding.

Idiomatic code: standard collection iteration, defensive copies, unmodifiable wrappers where explicitly required, Locale.ROOT and synchronized ledger methods are appropriate to the stated APIs. All references were read, not inferred correct from their patch size.

Dependency isolation: only Java standard-library imports, pinned Java 21 runtime, no external library/file/network dependencies. The tests are manual assertions under SolutionTest; no compilation/execution is claimed here.

Realistic known-bad failure: 0028 retains a caller map; 0030/0131/0138/0334 query null-rejecting immutable collections with contains(null); 0160 sorts rendered strings rather than original keys. The corrected suites contain tiny behavioral counterexamples to these actual mutants. For 0334, the meaningful mutant witness is present but does not cancel a separate invalid oracle.

## Exact lineage checks

All six R15 messages, verification prompt, rendered prompt and complete validation (reference plus known-bad bytes and metadata) equal R12. Feedback previous_candidate_sha256 equals the canonical R12 candidate hash for every row. Each test content equals the archived independent correction output test_code after the generator's strip-plus-newline normalization; its stored SHA-256 matches actual content. The correction archive returned zero, did not time out, and records no disallowed tool items or parse error. This describes teacher provenance, not candidate execution.

Source fields other than the versioned transformation string equal the immutable original parent. All retain McEval-Instruct revision 57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0 URI and record-specific hashes; prompt/answer/tests/model_training/redistribution rights equal the original all-true bindings. Original corpus SHA-256: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec. R15 run contract declares correction_attempt=1 and unchanged specification/reference/known-bad.

Canonical hashes use UTF-8 JSON with sorted keys, compact separators and ensure_ascii=False. Files are under datasets/cache/expansion-v1/versioned-recovery/r15/, named <full ID>.candidate.json.

### exp-v1-recovery-r15-java-generation-0028

- file SHA-256: `fa955c42a8e7bbbb9d92e3ac227e9a5dc17ce1054b3b2a62e60ce0142fc58e76`
- canonical SHA-256: `ca8e2f222ade25d03a75002769d51cea63b3d0d3c37da48405209323212b2b04`
- previous SHA-256: `97d1366f3983a8b567fadfea631d0a945aec34e350105f83134e63a2c76412bf`
- source SHA-256: `62288bccfb8c26aa64c38da947f52de916155ba6415a085132a17ccef891a807`
- prompt SHA-256: `c7fadf3cb0fc2d3e88f7a7536dfd9f2ca2e9d784cc17aef614dbc08d2f8a68a9`
- reference SHA-256: `28d74955d709023ea486cf9357d1fdc6172ed9662adf8279796410a28b8066a7`
- test SHA-256: `58cd7b6d8e944e89abad0038bb51c202b1a6a6f47a77667d6cb90bbffd5088a8`
- mutant SHA-256: `d0673124d68e8d04c8f29cc36ca387d9787bb91e8f21c4b4cb663a449e3b7082`

### exp-v1-recovery-r15-java-generation-0030

- file SHA-256: `a9a7fbb846cd69c49f3833140f19c6b9858f285d405c7ee7e5bc132376986ff0`
- canonical SHA-256: `e31237d7eef3db12142fd94464c1e1c5da99cc4eb935d9e9881e159c0467a7c2`
- previous SHA-256: `828d277e11cec1345055ad831bdf2a35524c6306d9add9f5f3e7a8c101a8cc73`
- source SHA-256: `da17191e8944081e6e9f4048c171068ce5654cc5d3cac4e40c3c858da721db73`
- prompt SHA-256: `0b898e179321d692abbbcfb08ea3084e78094d6671a1eba959d991defb1a3296`
- reference SHA-256: `0093352549231fdbbc04028644ad76611ca7fbb47a474ee9d6809a7dafea9227`
- test SHA-256: `1d89df9150f5c6beff6431248492b187b08771b002ce03baae57e9f958b32aa1`
- mutant SHA-256: `3de5ea06234b92fbe695f70f794ad92fb07258d03ca198d642230f6cde69130e`

### exp-v1-recovery-r15-java-generation-0131

- file SHA-256: `894253106a275ac1d671df42da4d9ca44104229812e326736d173b1434fbd849`
- canonical SHA-256: `af6ee9799d39bc48c9d6d81b4321d4b498a6429c5db316993e53454198551454`
- previous SHA-256: `5a9829cb8aac0db3486d051fa2bd039734fb3fcbb8e9e75a158fad9638626828`
- source SHA-256: `cbabfe95656672a309efaaeb658409285de2f95f4b7c46027bbf6fc8b18a6c46`
- prompt SHA-256: `48613f74c4278d960f81a77a0b3057d0c6b5e30fb6b60298b09cc53653846233`
- reference SHA-256: `604bc8a45d2585ad162c5be4864c5019efa3e4338331a0cbcb61888082f29e16`
- test SHA-256: `b969894ef30a2570c628d90ee14e3891c520bbc7c0c65b9600d41d56f7537858`
- mutant SHA-256: `3306b56d80a2b40515868a80426aa42a7ba00940ce2db28cdd8f2a1f89af576c`

### exp-v1-recovery-r15-java-generation-0138

- file SHA-256: `ebadebe009dd9d05b8a2a5e2840f223cefa683b5f7e182769cf11dbe8b48bdf9`
- canonical SHA-256: `5b4c14d37bc911c4f00015712126e084de295c5db832fccda79a2ed03c3b0498`
- previous SHA-256: `87c16276a6d38343ac2a7127a77da978aeac3c8b1ec36a0d038431cb6f2ec2ab`
- source SHA-256: `5ddfd21fa077ad8dd28ed37c3399b9e06c1001fc1da24011e61eedb11a712608`
- prompt SHA-256: `1febe7197851c92cc08a9be775c0c308143382127d4e40a9ca3f75d916e0db42`
- reference SHA-256: `26fdb37459d0f33d32fab79c27e56f0df409e887ccc647b71df7b85074bb7799`
- test SHA-256: `ff618964d1c477a0216d645bcd85f467c1d60c7bd74825c9154709e4b3e032bb`
- mutant SHA-256: `78b7790fd43c551d3f840625a3a6607df98e22b0f29f744c2be41e9b206ae585`

### exp-v1-recovery-r15-java-generation-0160

- file SHA-256: `f68413c1fdab50f28988815f2edf1449aaeb3489b531ce97f416c3b0b45999ac`
- canonical SHA-256: `2e85989b005e6ce0d20ec9ac3adb8d4115f6c5c7703d05a5d632add3264da13b`
- previous SHA-256: `88c8f12b881679e8b6821b06008dff4104a299aea7190d29691e2bca42888c33`
- source SHA-256: `98e88de7a7b82b8b613ad0b16ea76adc2747ee5d32ae6a0ae6afe976a90a5426`
- prompt SHA-256: `4124fced52ca68bcb817ae63ad62a41a663289e89353b79e8cad2714539caede`
- reference SHA-256: `9074e92c141e44be3613cba122bd8c72c70481a2a3d88a998e785a3ce4a0944d`
- test SHA-256: `04eba82017d9ccc31cc333371db6882cfbbf27dfb4da44f08dba970d39fd82e4`
- mutant SHA-256: `12c7fd6af703cbf551a20c8551a4953956a23784343bfe5ba66a1a391e37ffa3`

### exp-v1-recovery-r15-java-generation-0334

- file SHA-256: `1f70bf1bde6668f53d713f5a285c8a414ec2fd9d71ce40fa6091c01fab365b2d`
- canonical SHA-256: `baa9710f6a1ee8e452cd814e883962eb86c33823e29c24cd97aee47c0e2f2c91`
- previous SHA-256: `7bb65b2e32cecd8b10dc3823457cabf0628e8f66607c28828a5f84c67edf7e8c`
- source SHA-256: `dd3e84f742a4a159843083d2bd2c4f485a38a54e6d7153bb2ed4e6e1d84e9e52`
- prompt SHA-256: `1361c6803cc1b519191634c0c3869c65ec3de58c10d73205f49b7e6c43c922aa`
- reference SHA-256: `b621094918c9e1f58f2aa748c1eda4df07fa30b2dd6658da21924c6fb4770260`
- test SHA-256: `8cabf7a9ae06ee3d7fdc9f57ec4862065b6ed46678b9d267b2f34b845026e5f9`
- mutant SHA-256: `06c415f96ae36c0633123ce9f5285bd294d8087efbfcb4c4dff648d8c85fe868`

## Shared evidence hashes

- datasets/cache/expansion-v1/versioned-recovery/r15/run-contract.json: `9698ee3b6b7cf73427e080069dda922d0d5de7e44d14d83b119cff3027a342e0`
- datasets/cache/expansion-v1/versioned-recovery/r15/java-recovery-test-correction-evidence.json: `a871cc4556f8b0038020d1860b424098c02f69e17674bd1829745f1f7965711a`
- measurement/data/expansion-v1/cutoff-5885-review/recovery-test-feedback-r15.json: `be176d78f3d57efc593b56895696cb74425280e234239be67c8efcc45cdf1ead`
- measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r15.json: `0f0e6811acfda0be820f60655b41f14e8e5b5e0eb183f587112b16bb1b742566`
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_JAVA_REVIEW_20260908.md: `e07eba34ce78be5557421eabc5b53afce22fb0ad3b92be30be71d279083ef85c`

Static dispositions belong to these exact bytes. Main owns serial sandbox diagnostics and any later admission decision; successful reference/mutant diagnostics cannot establish that an unsupported oracle is valid.

