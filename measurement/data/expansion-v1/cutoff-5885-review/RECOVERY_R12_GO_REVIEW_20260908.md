# R12 Go independent recovery review — 2026-09-08

**Result: 10 reviewed, 10 test-qualification holds, 0 admission-ready/static overall positives.** References have scoped static-positive correction assessments; the independent test layer is not sufficient. Eight suites lack the exact held-defect witness. Two (0326,0360) do expose the held defect, but contain invalid/unsupported oracles. No generated code was executed. No cloud, teacher, central ledger or candidate mutation occurred. Zero new original-row coverage.

All ten complete derived prompts/references/tests/mutants were read, together with original test files. Original prompts and references were byte-compared: all ten prompts equal their originals, and all ten mutants equal the fully read original references. Approved R12 plan records and Go sections of RECOVERY_NEXT_GO_JAVA_20_20260908.md were reconciled. No original test is treated as permission to narrow the prompt.

IDs below use prefix `exp-v1-recovery-r12-go-generation-`.

## Per-candidate dispositions

### 0072 — HOLD: missing control-character witness; JSON oracle overconstraint

Reference correctly uses encoding/json for JSON strings and strconv.Quote only for FormatLines; keys are bytewise sorted, full key/format errors return empty output, nil/empty behavior matches. The current JSON suite contains newline, quote, slash and Unicode but not bell U+0007, vertical tab U+000B or NUL, where Go quoting is not valid JSON. Thus it does not expose the original defect.

TestRenderBindingsJSONSortedValidAndCompact compares an entire JSON string requiring literal 雪 and selected equivalent escapes. The specification promises valid JSON quoting, not that spelling; a compact ordered JSON value using a Unicode escape is valid. Replace the exact-value-escape oracle with JSON decoding equality plus independently checked ordered keys, separator compactness and final newline. Keep FormatLines exact Go-quoting checks. Add tiny control-character values and no new UTF-8/domain restrictions.

### 0084 — HOLD: false ordinary-case oracle; missing ASCII-only folding witness

Reference folds ASCII bytes only, preserves Unicode bytes, uses parsed struct field types, suppresses only eligible source-name ambiguity and maintains destination declaration order. In TestInspectFieldMatchesOrderTypesAndEligibility, destination URL must match source Url: source lowercase url is ineligible and does not create ambiguity. Correct result begins {Destination:"URL", Source:"Url"}, then Name/NAME, Count/COUNT, Meta/META. Current want omits URL, incorrectly rejecting correct code and mutant alike.

No Aİ/Ai case tests the held Unicode overfolding defect. Add nonmatch for destination Aİ vs source Ai with equal types, self-match Aİ vs Aİ, ordinary ASCII controls and genuine eligible ambiguity. Continue parsing-only—not type-checking—tests; unresolved pkg.T in source strings is legitimate parser input.

### 0133 — HOLD: missing structural-key collision; extra nonnil policy

Structural componentKey{scope,name} fixes Create/Get/Delete identity coherently; scoped listing, Quota64 and returned values remain correct. Tests use ordinary scope/name pairs, never the old delimiter collision. Require both (scope "a\\x00b", name "c") and (scope "a", name "b\\x00c"), distinct releases, exact Get/List and independent deletion.

TestRegistryEmptyInputsAndEmptyLists requires nonnil for both empty scope and nonempty missing scope. The prompt explicitly requires nonnil for empty scope only. Preserve that check for ""; use length/content for "missing". Do not prohibit NUL, trim identifiers, introduce nil-receiver behavior or change registry concurrency requirements.

### 0149 — HOLD: missing structural-route collision; constructor error representation

Reference routeIdentity{method,pattern} fixes duplicate checking without altering first-match ordering, parsing or copied routes. Current tests never use colliding concatenations. Add routes ("GET\\x00/x","/y") and ("GET","/x\\x00/y") and require construction plus both exact resolutions. Preserve true duplicate rejection.

TestRouterRejectsInvalidRoutes requires both an error and nil Router. Constructor failure return value is not specified; only Resolve has the explicit "",nil,false tuple. Remove constructor nil-value demand, retain nonnil fresh maps on successful resolution and exact Resolve failure tuple. No URL decoding, identifier grammar or nil receiver promise is warranted.

### 0204 — HOLD: missing bounded-allocation witness

Reference limits capacity to41, preserves generator independence and overflow-safe permanent exhaustion. Its fixed count bounds allocation only; the values still come from the checked generator, not a literal-answer table. Tests exercise generator exhaustion and PowersOfThree(1000), which the old allocate-n implementation handles. Add PowersOfThree(MaxInt) and require exactly41 values with final12157665459056928801, checking prefix recurrence. This has tiny correct output; do not iterate MaxInt generator calls. Existing nonpositive nonnil, fresh slices and post-exhaustion tests are valid.

### 0234 — HOLD: missing unbounded textual-ID witness

Reference validates canonical positive ASCII decimal text directly, removing machine-int parsing while preserving IDs verbatim and lexicographic order. Add/Get/Update/Delete and tags copying are otherwise coherent. All valid tested IDs are small. Require ID "18446744073709551616" through full lifecycle, with ordinary IDs for lexicographic ordering and replacement tag isolation. Existing malformed IDs and no-sign/no-leading-zero tests are valid; do not introduce a numeric cap or nil/empty tag representation demand.

### 0266 — HOLD: missing overflow witness; explicitly disallowed representation oracle

Reference computes remaining=len(rows)-offset, clamps pageLength before offset addition, so end cannot overflow. It preserves complete record validation, exact owner/label filters, inclusive time, sorted pagination and deep copies. Tests reject overflowing cursor text (a different rule) but never use PageSizeMaxInt with Cursor"1". Add one-record terminal-offset and two-record one-row-success cases with that page size.

Multiple tests demand nonnil empty success rows: TestListAssetsInclusiveDateAndExactFilters, TestListAssetsCursorValidationAndBoundaries and TestListAssetsEmptyInput. This is not in the prompt and was expressly excluded by approved selection scope. Check empty content/length and cursor without requiring nonnil. The exact nil/empty-cursor/error tuple is promised for malformed timestamps; tests also impose it on other failures (IDs, page size, cursors) where only rejection is stated. Avoid promoting those incidental reference outputs into a broader error-result contract. Do not strengthen RFC3339 beyond the existing time.Parse semantics.

### 0326 — HOLD: false suffix oracle despite real overflow witness

Reference checks each gap/span against remaining capacity before adding; used remains between0 and Capacity. This correctly handles MaxInt without overflow and preserves raw string interpolation, order, marks and final newline. TestEncodeLayoutRejectsArithmeticOverflow is a genuine tiny held witness: MaxInt plus another span and gap is mathematically overcapacity.

TestEncodeLayoutEmptySectionsAndGapOnlyBetweenSegments compares got[len(got)-20:] to "used=5\\nremaining=0\\n". That literal is18 bytes, so the comparison is always unequal for the correct full output. Use a spec-exact complete expected string or suffix length derived from the actual expected suffix. Current invalid-layout tests also require output "", whereas the prompt only requires rejection/error; remove that extra error-output demand unless separately approved. Retain/add independent span-overflow, gap-overflow and MaxInt exact-fit single-segment controls, with no unused-gap charge. A false ordinary oracle cannot qualify an otherwise useful overflow test.

### 0360 — HOLD: unsupported constant-number oracle despite real Unicode witness

Reference preserves whitespace trim and changes only ASCII folding. TestParseSeverityRejectsEverythingElse includes "İNFO" (U+0130) and therefore exposes the held Unicode-folding defect; ordinary ASCII and storage/order controls are useful. The same corrected ParseSeverity is used by FilterLogs; a direct Unicode-minimum filter control is still advisable.

However, TestFilterLogsValidatesAllEntriesBeforeReturning hardcodes Severity(-1) and Severity(5) as invalid. The generation prompt promises only increasing severity constants, not numeric0..4 or even a zero origin. A conforming assignment Debug=-2, Info=-1, Warn=0, Error=1, Fatal=5 makes both entries valid; the test would falsely demand nil/ErrInvalidLevel. Derive an invalid value relative to exported bounds (e.g. Fatal+1 within the supplied int runtime), or otherwise establish it differs from every exported valid constant. Do not require iota's incidental values. Keep nonnil empty output here because this prompt explicitly requires it.

### 0409 — HOLD: nil snapshot oracle error; missing existing-empty-key witness

Reference looks up the item before empty-code rejection, returns the original when present and never mutates on error; staged patch validation and pointer-value copying remain correct. Current empty-code test has only key "present", so it does not expose the original defect. Add a nonzero InventoryItem stored at key "" and require that original plus error with the map unchanged; no valid-key-only table precondition exists.

TestUpdateInventoryItemMissingAndEmptyCode creates before:=make(map...,len(tc.table)) even for the nil-table case, then reflect.DeepEqual(tc.table,before). Nil input remains nil, so this assertion is false for correct behavior. Preserve nilness in the snapshot or compare the explicitly relevant map state without equating nil to a made map. Existing lookup/key-Code mismatch test is valid and should remain.

## Seven criteria and proposed correction boundary

1. **Clarity/domain:** All reference-fix problem bytes are unchanged. Approved text, ASCII, integer, ownership and error policies were used; no numeric caps or new container representations inferred.
2. **API/reference correction:** All ten requested corrections have coherent scoped static-positive implementations. No new reference-side contract defect established in this review. This is not a compile/execution claim.
3. **Independent tests/valid oracle:** Separate recorded author provenance is verified below, but all ten remain held. Missing defining witness:0072/0084/0133/0149/0204/0234/0266/0409 (eight). Existing defining witness but other test defect:0326/0360 (two). Additional invalid/unsupported oracle issues are individually described above.
4. **Entire-target nontriviality:** Each retains meaningful interactions: dual-format serialization; AST/type/name matching; scoped CRUD; routing/identity/order; independent checked generator exhaustion; lexical-ID CRUD and nested copies; validation/filter/pagination; checked layout arithmetic plus serialization; severity parsing plus whole-list validation/order; transactional optional-field updates. Small fixes are not grounds for elementary rejection.
5. **Go idiom:** Structural comparable keys, sorted deterministic output, AST parser/formatter, checked remaining-capacity arithmetic and value/slice/map copies fit standard Go. No implementation relies on tests' erroneous expected values.
6. **Isolation:** Standard-library-only package solution; support go.mod is separate from test code. No filesystem/network/clock dependencies or private-layout tests. No concurrency guarantee added. Main owns resource-limited sandbox diagnostics.
7. **Realistic mutant:** Every known-bad equals its immutable original parent reference and retains the named realistic defect. Do not count failures caused by false oracles as held-defect directionality. 0326/0360 have inspected semantic witnesses; the other eight do not yet.

If main authorizes correction, all ten are candidates for **one bounded test-only correction**, preserving exact R12 problem/reference/mutant bytes. Fix invalid oracles and add only specification-derived witnesses. No correction request, critic call, generation or execution was made here.

## Source and author evidence

Plan path `datasets/cache/expansion-v1/versioned-recovery/r12/plan.json`, SHA-256 `0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121`.
Scope path `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_20_20260908.md`, SHA-256 `986b3dba391e9903b743d680f6b5b94071a3292c37c00a4930a998a00d6b586d`.

Each original canonical candidate hash was recomputed against the plan; all ten match. Candidate prompt/reference/mutant were byte-matched to the recorded architect output and tests to the independent author's raw final output. All original source fields except additive recovery transformation are retained; all five rights flags are unchanged true. Exact source rows/hashes and original hold evidence hashes are below, distinct from author evidence. Preserve CC-BY-SA-4.0 attribution; this is not release authorization.

The independent test prompt was read: it contains exact IDs/specifications and generic test directions only, no reference, original tests, mutants or architect context. Both author calls are separate ephemeral gpt-5.6-sol/medium processes; recorded exit0, no timeout, no disallowed tools, no parse error. These are generation-process facts, not sandbox correctness. Author files are `go-recovery-architect-evidence.json` and `go-recovery-independent-tests-evidence.json` in the R12 directory.

```json
{
  "architect": {
    "file_sha": "94f6db06c130087271871beaf0c1fa5c085a1963271f24ba8b9c63c6f3ff26aa",
    "command_identity": [
      "/opt/homebrew/bin/codex",
      "exec",
      "--ephemeral",
      "--ignore-user-config",
      "--ignore-rules",
      "--sandbox",
      "read-only",
      "--skip-git-repo-check",
      "--json",
      "-m",
      "gpt-5.6-sol",
      "-c",
      "model_reasoning_effort=\"medium\"",
      "-c",
      "service_tier=\"priority\"",
      "--output-schema",
      "/Users/navneetprabhakar/Documents/git/ganesh-mini/schemas/data/codex-architect-output.schema.json",
      "-o",
      "/private/var/folders/05/gl6wkys51x7gncjcc8hmfbg00000gn/T/ganesh-codex-recovery-architect-go-cfyh73y0/final.json",
      "-C",
      "/private/var/folders/05/gl6wkys51x7gncjcc8hmfbg00000gn/T/ganesh-codex-recovery-architect-go-cfyh73y0"
    ],
    "disallowed_tool_item_types": [],
    "event_parse_error": null,
    "returncode": 0,
    "timed_out": false,
    "prompt_sha256": "107ae0f5a0042553089bfbd777d08915e2d5648246fcd2808da3261607006774",
    "final_output_sha256": "b25827ecf2678da0cc933c2e7af53a1a74f78a4d3632deb5133dbaf3ff1e60a5"
  },
  "independent-tests": {
    "file_sha": "1af84bbe0a0dbac8dcc7b9a3d501aaa8e30f6a2212d1f38b7d6094c11bc595e9",
    "command_identity": [
      "/opt/homebrew/bin/codex",
      "exec",
      "--ephemeral",
      "--ignore-user-config",
      "--ignore-rules",
      "--sandbox",
      "read-only",
      "--skip-git-repo-check",
      "--json",
      "-m",
      "gpt-5.6-sol",
      "-c",
      "model_reasoning_effort=\"medium\"",
      "-c",
      "service_tier=\"priority\"",
      "--output-schema",
      "/Users/navneetprabhakar/Documents/git/ganesh-mini/schemas/data/codex-test-output.schema.json",
      "-o",
      "/private/var/folders/05/gl6wkys51x7gncjcc8hmfbg00000gn/T/ganesh-codex-recovery-independent-tests-go-_98ikktf/final.json",
      "-C",
      "/private/var/folders/05/gl6wkys51x7gncjcc8hmfbg00000gn/T/ganesh-codex-recovery-independent-tests-go-_98ikktf"
    ],
    "disallowed_tool_item_types": [],
    "event_parse_error": null,
    "returncode": 0,
    "timed_out": false,
    "prompt_sha256": "56d90690566e83a7f09ccb0e753761a5b7256f9bc026cf435eb5843edd1767b5",
    "final_output_sha256": "189bef6cba4c59940bbb3ccb09efc683297b20af5fbca1dcc448fee98ceee2b3"
  }
}
```

## Exact candidate bindings

Paths: `datasets/cache/expansion-v1/versioned-recovery/r12/<id>.candidate.json`. Canonical hashes are sorted compact UTF-8 JSON (ensure_ascii=false); file/content hashes are SHA-256 of exact bytes. Test hashes refer to solution_test.go, not go.mod.

```json
[
  {
    "id": "exp-v1-recovery-r12-go-generation-0072",
    "parent": "exp-v1-go-generation-0072",
    "parent_hash": "324059f2ab4588d324dd392c8a09206050c98db6a903c813c0449725896146a6",
    "canonical": "23b132e85571fd015604b0c918bcd0363069c0b4ddbc3fb098e310d8d6ee2c53",
    "file_hash": "e37c26edbdbdb3fb21c461c3e989d3c605ce2fe415a08ca6fcfd57bc26ef5d82",
    "prompt": "5aca25a54083279b9c717518b0231ccf1661514e9c98c0dfec6f448c8ad90635",
    "reference": "1c614ccbcebff35ea577179879e5ef11969c91cd6413fcc7893dd5867b0b34c5",
    "tests": "8e95cc37ede445a5759169ae41798d1fbbfbc18571e72515a1286a771f8370e7",
    "mutant": "a608bd32584a8a1e2b70f169adb678d1a721c34d08765019107f3bb7f47dc7ec",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27650",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "64e46612151581ffc599323902438ca8622ed940ead8971808a6ba8364ca56b9",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0072 from exp-v1-go-generation-0072 sha256=324059f2ab4588d324dd392c8a09206050c98db6a903c813c0449725896146a6",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_6.md",
    "hold_evidence_file_hash": "e8a87bbddde64727a5fa0e81504d19baff9b9dff8e6e442eb2097fee4349d0db"
  },
  {
    "id": "exp-v1-recovery-r12-go-generation-0084",
    "parent": "exp-v1-go-generation-0084",
    "parent_hash": "4880da15d57b6cae3153e1410178ca61728e95848149fcf63cb1c0381b20bc29",
    "canonical": "429f9aa02d85f993ab46394d3ae0ed5c29d3c0d271b87c916129aad569233743",
    "file_hash": "4f0536a27be8833138688c5ff0a04b56d78f16bc16494306974c0d32276c1713",
    "prompt": "080bab2c76e72435702004e7df92370d69e029659bea30006a5666b3618b3dc7",
    "reference": "9c60f8a7187bf16f6fa6c6ebc61360046bd47f69a7101c99177a05e8f0911de2",
    "tests": "dffa8332fa5b3a0da9e9232c68fffc9c9ecc5981c772ba28bf438946b855012d",
    "mutant": "c5f9a2c7f066d21033ebc8cdb20dfbfdce3c6d98be36a1dad6f2a55def4364d8",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16327",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "b00b27a7643b1a45d9a443de7cf66eb52b5c6ac30a862c5dcaac41841158327a",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0084 from exp-v1-go-generation-0084 sha256=4880da15d57b6cae3153e1410178ca61728e95848149fcf63cb1c0381b20bc29",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_7.md",
    "hold_evidence_file_hash": "d659c4ccda2f5e666390f4c6cd847efbd42e1342c228513625a4a743e037d38f"
  },
  {
    "id": "exp-v1-recovery-r12-go-generation-0133",
    "parent": "exp-v1-go-generation-0133",
    "parent_hash": "001f7a5e4245bb8e664d489f74364def16276ca5bb674f1691e5cf6250f330c0",
    "canonical": "73982812c6677b8d04e08731e91ac05e5e5815e30b3106fb2c17d25aeccff016",
    "file_hash": "b5303299c48c94b41c941e3661bf417117e9782c47307e062fe65eaaae2533a4",
    "prompt": "278f1bd5158f697c67b03559b158b46ca65fbb400a22f0ca9998661e272ae767",
    "reference": "4d30927c9a4d33c6b9dfeccf6cb579e28ebd878dccd074508481634213c90c4b",
    "tests": "67ed41f02211d7d6304bbc915cf44ba758d24b95d2e990456572175904f92fa0",
    "mutant": "67228f131faedcf77df5cd2c87877fb8406244865f7b08de3ea12615c470314e",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16388",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "fb9276729b5cc80028d85ada36a2d26dfcd0c852c4d5196f79b38703d09e11ed",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0133 from exp-v1-go-generation-0133 sha256=001f7a5e4245bb8e664d489f74364def16276ca5bb674f1691e5cf6250f330c0",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_11.md",
    "hold_evidence_file_hash": "1c0222dce13bf4c2cbabe6c75545d4f4a9bcfdff6b1adf2d53ec72c99f54249f"
  },
  {
    "id": "exp-v1-recovery-r12-go-generation-0149",
    "parent": "exp-v1-go-generation-0149",
    "parent_hash": "ced5e779da6d43dfa9e1cb49213bcbda6f2b6351f2e9063a742ac79537fb564c",
    "canonical": "0115aca38d542c4ac729fdeb7237aac032c45d9b9819260c3f1fb9e15a9132f0",
    "file_hash": "bbf1ae071aca7f928122abec544aa6da1c31b8b5bfc704390a1685468a09ebd4",
    "prompt": "9a7c67bf984186e968d52f0a9de94082e766f111d20cc45cb483f78554cabc8f",
    "reference": "c76863f07148ea788093c3378306cdf0e983fe9d3fbabb196cfe085792a63b77",
    "tests": "049dac6d735c21d715f2670784aca9c814dd362b80e9d6bcc1cbad77c2cdbfb0",
    "mutant": "ebc162a56670da62521ae600a8f448452137acb403166dd064723f6f9d286a6b",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27558",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "7d861fa39ec26b881e4283babb0fe2b7ce13ba805b275778eebf9da2a507cc3e",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0149 from exp-v1-go-generation-0149 sha256=ced5e779da6d43dfa9e1cb49213bcbda6f2b6351f2e9063a742ac79537fb564c",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_12.md",
    "hold_evidence_file_hash": "896f4eb07e7c576b210f6f3635aa8431e604d32883fa9a54656b5f8004311296"
  },
  {
    "id": "exp-v1-recovery-r12-go-generation-0204",
    "parent": "exp-v1-go-generation-0204",
    "parent_hash": "b0911cfea3b4bfeaa79feffc2e1ef1fee103e28aba5320515d0cbdaebcd6b5ce",
    "canonical": "c70866696af5d51a3f0824fde9f9eff98b09f4bb7c77da39882352c2d1605a7f",
    "file_hash": "3d13979e8cf93bbb20591f1d8062fd707d9af7b2cc784ce777847a5a6e08382b",
    "prompt": "e9e812bc007a21c737711dc24f594f97ada4b259f4255cf1a9bdb1ac8d48eba2",
    "reference": "2424122709a2ee8f2ad30f3e72ad765b84a3577c900137430ed86709fc82de77",
    "tests": "d30480f418866f2e7316707c0de4ae70936a29570a0c2a87b864ac7cd079cfe9",
    "mutant": "a8c44ed562a5dfece2390acde8a50f0aaae05a4a652dba9f0786e3f6f97f3530",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16354",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "09349138b994b5c18ab98cccc2c9c01ec0be86ef67bacfb114cf2e2eb8ded28f",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0204 from exp-v1-go-generation-0204 sha256=b0911cfea3b4bfeaa79feffc2e1ef1fee103e28aba5320515d0cbdaebcd6b5ce",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_16.md",
    "hold_evidence_file_hash": "ed948ebecd69937b90d9a454a2971d2678e872fe81a6ef28ef40e62e62e3bd7f"
  },
  {
    "id": "exp-v1-recovery-r12-go-generation-0234",
    "parent": "exp-v1-go-generation-0234",
    "parent_hash": "f743b378be9f7bcb536e86973669c1cbead45f0b1556d79cc8077f14c19682cb",
    "canonical": "958417d368d3c44592112e70ad6a93d2ae5203cea8b12b645b6e377ef631c5e2",
    "file_hash": "cb083aa94cb2f2e2dbb22bb7417cfc1deff7717772f2507216646b4156399607",
    "prompt": "08adeaf5405cac0c74c03549e6946a071f48af69f21612c9cd5f5db2e89bd8aa",
    "reference": "8f175c2570d309096148270362739b7ce5d3fc2ca93d0d0d3e46412ef16c472c",
    "tests": "4e646c5b34e22db81128e418d2ceb4ddf5ca51211dae5b01102c2d66a38f4936",
    "mutant": "a6c39329331ac0019e4af76d6cc154016b1ab7854603052f6b96ab8ace15c6bc",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16024",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "ed2c415ddf87fc00c1fb1bff954cad48fba6f081ab5df1adfa8d0a70dd2fb508",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0234 from exp-v1-go-generation-0234 sha256=f743b378be9f7bcb536e86973669c1cbead45f0b1556d79cc8077f14c19682cb",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_19.md",
    "hold_evidence_file_hash": "ab17bc6d7e0f3a144ffb29784ee1b78ce8d00e47431735fd7d3b806c1d7c210c"
  },
  {
    "id": "exp-v1-recovery-r12-go-generation-0266",
    "parent": "exp-v1-go-generation-0266",
    "parent_hash": "16aab2d4078c16d399336e6fba8bccb6c41a7162f2f2093fe95fc30c7428a122",
    "canonical": "7168f5f04b9cbc6748e07eb6568d59d10a8c8143c7120b3248292ed4c768a0b9",
    "file_hash": "92b0c7de69f6215a37777fb8079f2ddad78e47925a7dc91b9633ef4a0dd32854",
    "prompt": "25eec8015b99b6c362e7a4e00698f12668abe810cf7dcaacc4e46559dc0cbc9f",
    "reference": "97d3bff918944731aee4c936b757dfba8b8f54fe394c87326477956f68db8993",
    "tests": "0270b892ef0273bea09fda58a8af00a1bad526a224ec2e726783f342577e9eba",
    "mutant": "a1357433313a59a97eb96dd15c6a27a91bed22a4727cc400d06fdc95a9ce6f2c",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27933",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "ab17b5ffffac705bf869be22178b87c4b871154953c844fad7a15ace67ab4574",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0266 from exp-v1-go-generation-0266 sha256=16aab2d4078c16d399336e6fba8bccb6c41a7162f2f2093fe95fc30c7428a122",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_21.md",
    "hold_evidence_file_hash": "5e99953ccd76c1620a462ca4025f0ff81c27273eff33eeab5ae55dd42407a746"
  },
  {
    "id": "exp-v1-recovery-r12-go-generation-0326",
    "parent": "exp-v1-go-generation-0326",
    "parent_hash": "643ed0c3f460d89800673636d0609ac2250861752908ecb56f713e0ed0737198",
    "canonical": "c5dc02ecff1a44e9665cf05135cc405a21dfbfa6d7db1e1d01f99530cd277c51",
    "file_hash": "ce39d64b28284a8d0478145a605834445252035bb6d948d2720319b41d8f58cd",
    "prompt": "27b49d1da63279c5a563c33db59445f9b0a302ebb4520388f79629af6453be4d",
    "reference": "2e7ff20fa52c15f7ba6b6bb00ba666ba0847a65e80a63905f945bfd7ae3cf286",
    "tests": "270c85d5c1916c4bf0cbf42bc53c813f2f60cf4dbc1c96c39bed9fed698020bb",
    "mutant": "045ab73fd3bb5bdd5ce0b8bb74dff911df74137d342cde3df6bce77482c76ffd",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27592",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "bac2bf7e045a0e74c24de49502e2f7b8e0d6c496852577d089e1033cc3e627ce",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0326 from exp-v1-go-generation-0326 sha256=643ed0c3f460d89800673636d0609ac2250861752908ecb56f713e0ed0737198",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_26.md",
    "hold_evidence_file_hash": "0635874594f827dc82736b76ab44bd29ec7c102f5e0224fb899a831185df1b48"
  },
  {
    "id": "exp-v1-recovery-r12-go-generation-0360",
    "parent": "exp-v1-go-generation-0360",
    "parent_hash": "64b45b8fc1a1ce9398a14fb2e1bee722871bd506168b02d7dc1f2a95efe05846",
    "canonical": "5fc2ec2a2e5543aa175c61779c41d466f654270f656112143b213164d8bf845b",
    "file_hash": "06654a7b93d6e60e5fc8d4e3a7872f4555e034f2462dcae21d863d60afad8b44",
    "prompt": "5fc2df7593c4518ab20f0a229bce250148172018bf5ed9bc7ea494b6b888dc4b",
    "reference": "4271ddcd4d169a9109f5e3d2e17f7e06b6b27c1eebc052b53995316cb0a48286",
    "tests": "950f4b3657cf20f39196d108a212e89d1050053876d5cb742dc15f16bbe723d7",
    "mutant": "27f0a0e4a2fcf194a8096273ae3d9c1c36674eda77da1830c6b323a023687397",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16165",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "0f63b789406e6aa6a42aef17a260a48f94c7ba543cd0869e4f2055e55556190e",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0360 from exp-v1-go-generation-0360 sha256=64b45b8fc1a1ce9398a14fb2e1bee722871bd506168b02d7dc1f2a95efe05846",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_28.md",
    "hold_evidence_file_hash": "6a27a803269ffa76cf451506a2c2847939b34db1d6581cc88f27a1b84161a8b5"
  },
  {
    "id": "exp-v1-recovery-r12-go-generation-0409",
    "parent": "exp-v1-go-generation-0409",
    "parent_hash": "a9adb8cd38d9b6a6d8c6217e807c6139a9cd7939785e1234255c9cbf581ed5a8",
    "canonical": "6266a732a2380a001bf495c6df15c060b461cce1453e633d0ebf7516a423e3a3",
    "file_hash": "7ef70c158ba0c189bb7f7c80cf11244c8d7d271cfb124a072b3d9df47bfcda11",
    "prompt": "c828c29d44f4df3de7a6230a332aa3875208275ab9facd92c732851208b6c8ff",
    "reference": "0cb4b30809b79cc03d18710a82d51a2bf930744d03dc0a2847755b5bc98b604e",
    "tests": "7ea0c339e5e9792b0d71e19596be9b8aefaf04713c4639027301cffc98954312",
    "mutant": "7444cadb0424c9163e99313a043a735cf4037436f92fcbf1ab6b400bebc43111",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27838",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "8899c769f9ffec50841fee8bd2b11c552352f69d5cce428b0ab75ae0a41c8797",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-go-generation-0409 from exp-v1-go-generation-0409 sha256=a9adb8cd38d9b6a6d8c6217e807c6139a9cd7939785e1234255c9cbf581ed5a8",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_32.md",
    "hold_evidence_file_hash": "e6f9fedf7642193c6da0f81c377fdf70c89d6975e7b608a27524b49630f3c64d"
  }
]
```

