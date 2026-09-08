# R16 Go terminal test-correction review — 2026-09-08

**9 STATIC POSITIVE; 1 HOLD (0084).** All ten assigned corrected suites fully read. No execution, generation, admission, central mutation or original coverage credit. Positive means scoped quality review only; main owns serial sandbox diagnostics and admission. This is the terminal one-correction review, not authorization for another critic round.

## Integrity and provenance

For all ten R16 candidates, exact comparisons against R12 passed for messages (including reference answer), prompt object, rendered prompt object and complete validation object (reference and mutant code/hashes). All original source fields except additive derived lineage remain equal, and rights are unchanged. Prior canonical hashes match the main-approved R16 feedback. Corrected test bytes match the recorded correction author's test_code after the workflow's strip-plus-final-newline normalization.

Main-approved feedback file: `measurement/data/expansion-v1/cutoff-5885-review/recovery-test-feedback-r16.json`, SHA-256 `5adbfe13ec77231b8fd45010b4b639c2ab0c89523a41bf16426e29ffae9816a4`. Its complete ten entries were reconciled. Prior quality report: `RECOVERY_R12_GO_REVIEW_20260908.md`, SHA-256 `adbf72043d37d718a1d05ac4c114c7bdd0f8c7a0ccc5ad3cce4f1311bc919b5b`.

R16 directory: `datasets/cache/expansion-v1/versioned-recovery/r16/`.

- plan.json file SHA-256: `efd902abc4ed3e00d6639c74f7d2ec95e6f153d1aa19a70a460aeb553dfb6844`.
- run-contract.json file SHA-256: `d8f24054febbb0ebe043109dcbf8c6b7cf2a3852322586e1784aa96214b2a482`; correction_attempt=1, unchanged specification/reference/known-bad.
- go-recovery-test-correction-evidence.json file SHA-256: `eacbcc37ef767e5d458c4e6d7a18011d250644867eb92cc2d322f8454b45ccc5`.
- Correction prompt SHA-256: `fdc9d01a4e1a1e1164d30361e2af794ad373a80f5f260dd40d5dda52816d9147`.
- Raw final output SHA-256: `c7afd52bf10a8ef275acc4297db45adc453839a28aa3c483eb0c99223059d3e6`.

The recorded correction uses a separate ephemeral gpt-5.6-sol/medium read-only process, exit0, no timeout, event parse error or disallowed tool items. Its ten prompt items have exactly id/problem/test_code, each byte-matched against prior specifications/tests; appended review is the approved specification-derived feedback. No reference/mutant implementation fields are present. This establishes recorded author separation, not executed test correctness.

## Per-ID seven-criterion dispositions

ID prefix: `exp-v1-recovery-r16-go-generation-`.

| Suffix | Disposition | Exact witness and oracle reconciliation |
|---|---|---|
| 0072 | STATIC POSITIVE | JSON test now includes bell, VT and NUL; json.Compact and json.Unmarshal reject the old Go-only escapes. Decoder tokens verify sorted key order, while decoding preserves string contents and Compact leaves spaces inside strings untouched. Equivalent Unicode/JSON escape spellings are allowed. Exact Go-quoted lines, nil/empty outputs, final newline, determinism and errors in both formats retained. |
| 0084 | HOLD — new unsupported nonnil oracle | URL→Url is restored and genuine Aİ/Ai folding/self-match cases are present. However the second call in TestInspectFieldMatchesUsesASCIICaseFoldingOnly tests two nonempty structs with no match, then rejects got==nil. The prompt promises nonnil empty slices for empty structs, not all zero-match cases. A conforming nil zero-match result is incorrectly rejected. Exact criterion below. |
| 0133 | STATIC POSITIVE | Creates (scope a+NUL+b,name c) and (scope a,name b+NUL+c), checks distinct Create/Get/List values and independent deletion; old delimiter key collides. Removed nonnil demand for nonempty missing scope, retained explicit empty-scope nonnil rule, ordering/Quota64/empty validation and returned-value isolation. |
| 0149 | STATIC POSITIVE | Constructs the exact two delimiter-colliding method/pattern pairs and resolves each with fresh maps. Invalid constructors require only error; failed Resolve retains its explicitly promised tuple. First match, method case, slash grammar, copied input and true duplicates remain tested. |
| 0204 | STATIC POSITIVE | PowersOfThree(MaxInt) requires exactly41 bounded results with correct endpoints, exposing original preallocation. Existing1000-prefix test verifies bounded recurrence; generator test validates sequence, eventual permanent exhaustion and independent state. Test input/output are tiny; no MaxInt iteration/allocation is authored into the oracle. |
| 0234 | STATIC POSITIVE | Text ID18446744073709551616 goes through Add/Get/Update/Delete and replacement-tag mutation isolation, rejecting old Atoi validation. Ordinary IDs still prove lexical ordering and explicit nonnil IDs/Snapshot; invalid textual grammar, sentinel errors, atomic replacement, snapshots and clear retained. |
| 0266 | STATIC POSITIVE | One/two records with Cursor1 and PageSizeMaxInt require empty/one-row terminal successes. Native cursor overflow remains separately invalid. Success-empty nonnil checks removed; only malformed timestamp errors require nil/empty-cursor tuple. Full excluded-ID/timestamp validation, exact/inclusive filters, sorted pages and deep-copy boundaries retained. |
| 0326 | STATIC POSITIVE | Erroneous20-byte suffix replaced by full exact output. MaxInt+1 span and MaxInt gap cases reject; single MaxInt span with unused MaxInt gap succeeds with exact totals. Error assertions no longer require empty output. Raw text interpolation, final newline, order, marks and nonmutation remain valid. |
| 0360 | STATIC POSITIVE | Both ParseSeverity and FilterLogs reject U+0130NFO while ordinary ASCII cases pass. Invalid severity is selected among0..5 by exclusion from all five exported constants, guaranteed without origin/gap/overflow assumptions. Full-list validation, increasing order, explicit nonnil empty results, duplicates, threshold and storage checks retained. |
| 0409 | STATIC POSITIVE | Nonzero original at key empty-string must be returned with error and map unchanged; old code returns zero. Nil snapshot oracle now handles wasNil separately. Missing/nil maps, existing key/Code mismatch, atomic complete patch validation, zero cost, notes clearing and pointer nonretention remain valid. |

### Exact remaining hold:0084

File `exp-v1-recovery-r16-go-generation-0084.candidate.json`, test `TestInspectFieldMatchesUsesASCIICaseFoldingOnly`, after destination `Aİ int` and source `Ai int`: `if got == nil || len(got) != 0` adds a nonnil condition absent for this input category. Both source structs contain a field; they are not the explicitly covered empty structs. The correctly scoped oracle is no error and zero matches, regardless of nil representation. The separate TestInspectFieldMatchesEmptyIsNonNil remains justified.

This is not failure of the ASCII reference correction: both exact semantic witnesses are present, and the inspected reference returns a nonnil slice. It is a test-validity gate. A sandbox pass of the supplied reference does not erase it. The feedback's shorthand “explicitly nonnil empty output” should have been kept anchored to the actual empty-struct promise; I do not treat my prior shorthand as permission to enlarge the contract. No further correction or manual candidate/test edit was made. Main must preserve this terminal hold or explicitly determine an authorized next action outside the completed one-critic workflow.

## Shared seven-criterion assessment

1. **Clear contract/domain:** R12 specifications are unchanged, and prior full original/spec/reference assessment carries forward. All ten defining semantic witnesses now exist. No hidden scalar/Unicode/identifier caps were introduced;0084's representation demand is the sole remaining concrete test-contract conflict found.
2. **API/reference correctness:** Byte-identical R12 references preserve the prior scoped-positive implementation findings. Structural identities, bounded arithmetic, ASCII-only folding, JSON quoting, textual IDs and original-on-error semantics remain intact. No executed correctness assertion.
3. **Independent valid tests:** Provenance comparisons pass10/10. Valid scoped suites9/10;0084 held as above. Prior concrete false oracles and unsupported error-result constraints have been removed.
4. **Entire-target nontriviality:** All retain their previously reviewed serialization/AST/lifecycle/routing/generator/inventory/pagination/layout/filter/transaction interactions. No new padding or elementary replacement.
5. **Idiomatic Go:** Standard-library parsing/encoding, comparable structural keys, safe bounded arithmetic and explicit value/slice/map copying preserved; tests derive expectations from public APIs, not private layouts.
6. **Isolation:** Standard library and package solution; no network/filesystem/clock/concurrency assumptions. The0204 generator-exhaustion loop terminates for the required finite generator and is sandbox-bounded for incorrect implementations; it is not a claimed guarantee of termination for arbitrary mutants.
7. **Realistic known-bad:** All original-reference mutants remain unchanged. Each now has a direct behavioral witness;0084 remains held despite that, because directionality alone is not the oracle-validity gate. No fabricated executed results.

## Exact candidate and source bindings

Paths are in the R16 directory with filename `<id>.candidate.json`. Canonical hashes use sorted compact UTF-8 JSON, ensure_ascii=false. Test hashes refer to the complete corrected solution_test.go. Source remains McEval-Instruct CC-BY-SA-4.0 with preserved original rows/rights and derived lineage; this is not release admission.

```json
[
  {
    "id": "exp-v1-recovery-r16-go-generation-0072",
    "canonical": "204074a5fc34b6dd3316487cb77346705540c20ac18fb6b3047dcedc6d2b1bea",
    "file_sha256": "3eaaa56e513aa52e93031eb0a373e68d143e91d58a68734cf128875cd06a39ec",
    "prior_canonical": "23b132e85571fd015604b0c918bcd0363069c0b4ddbc3fb098e310d8d6ee2c53",
    "prompt_sha256": "5aca25a54083279b9c717518b0231ccf1661514e9c98c0dfec6f448c8ad90635",
    "reference_sha256": "1c614ccbcebff35ea577179879e5ef11969c91cd6413fcc7893dd5867b0b34c5",
    "mutant_sha256": "a608bd32584a8a1e2b70f169adb678d1a721c34d08765019107f3bb7f47dc7ec",
    "tests_sha256": "692714904a62e2b607d97c3b0d46d142d6b37fcb2b389a4b559492bdd7311dc1",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27650",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "64e46612151581ffc599323902438ca8622ed940ead8971808a6ba8364ca56b9",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0072 from exp-v1-go-generation-0072 sha256=324059f2ab4588d324dd392c8a09206050c98db6a903c813c0449725896146a6",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  },
  {
    "id": "exp-v1-recovery-r16-go-generation-0084",
    "canonical": "477a9a247b65bb1ea8dfcf88f17865d70988e1e3b93df36f3d39a74d9fc39996",
    "file_sha256": "a3f9b21ff033dc1cd4ef18f11600cda9074738531d84e7fa61bb0934c236d6f2",
    "prior_canonical": "429f9aa02d85f993ab46394d3ae0ed5c29d3c0d271b87c916129aad569233743",
    "prompt_sha256": "080bab2c76e72435702004e7df92370d69e029659bea30006a5666b3618b3dc7",
    "reference_sha256": "9c60f8a7187bf16f6fa6c6ebc61360046bd47f69a7101c99177a05e8f0911de2",
    "mutant_sha256": "c5f9a2c7f066d21033ebc8cdb20dfbfdce3c6d98be36a1dad6f2a55def4364d8",
    "tests_sha256": "d885dea9cb2a04d63b3b01a677a74f378907e08454c453a63e9f9bec28773d42",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16327",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "b00b27a7643b1a45d9a443de7cf66eb52b5c6ac30a862c5dcaac41841158327a",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0084 from exp-v1-go-generation-0084 sha256=4880da15d57b6cae3153e1410178ca61728e95848149fcf63cb1c0381b20bc29",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  },
  {
    "id": "exp-v1-recovery-r16-go-generation-0133",
    "canonical": "502a4807becb033929c0923d41a2aff6412706f284b23145ff0c38d136415cf4",
    "file_sha256": "7a4dfc9d05996eff9f42a93ec8efd5ae73fb1ff45f3d53130decc16fe58851d2",
    "prior_canonical": "73982812c6677b8d04e08731e91ac05e5e5815e30b3106fb2c17d25aeccff016",
    "prompt_sha256": "278f1bd5158f697c67b03559b158b46ca65fbb400a22f0ca9998661e272ae767",
    "reference_sha256": "4d30927c9a4d33c6b9dfeccf6cb579e28ebd878dccd074508481634213c90c4b",
    "mutant_sha256": "67228f131faedcf77df5cd2c87877fb8406244865f7b08de3ea12615c470314e",
    "tests_sha256": "f171f81ed2291f98f451672de4cc7a10377107bad0865558679c7db1aca1207e",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16388",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "fb9276729b5cc80028d85ada36a2d26dfcd0c852c4d5196f79b38703d09e11ed",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0133 from exp-v1-go-generation-0133 sha256=001f7a5e4245bb8e664d489f74364def16276ca5bb674f1691e5cf6250f330c0",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  },
  {
    "id": "exp-v1-recovery-r16-go-generation-0149",
    "canonical": "784c2cc1d10d62d032c00b31a9d8c87817b0acd7d0bb97ed18986f2d591b0217",
    "file_sha256": "b0bd7aafd311a42935f7fe4946ce106478392ddee346b600b5b8a25852b8a128",
    "prior_canonical": "0115aca38d542c4ac729fdeb7237aac032c45d9b9819260c3f1fb9e15a9132f0",
    "prompt_sha256": "9a7c67bf984186e968d52f0a9de94082e766f111d20cc45cb483f78554cabc8f",
    "reference_sha256": "c76863f07148ea788093c3378306cdf0e983fe9d3fbabb196cfe085792a63b77",
    "mutant_sha256": "ebc162a56670da62521ae600a8f448452137acb403166dd064723f6f9d286a6b",
    "tests_sha256": "41687e33c9f8fec84d193d796b1fce851d747b523bad3e25950e081823eb0b12",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27558",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "7d861fa39ec26b881e4283babb0fe2b7ce13ba805b275778eebf9da2a507cc3e",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0149 from exp-v1-go-generation-0149 sha256=ced5e779da6d43dfa9e1cb49213bcbda6f2b6351f2e9063a742ac79537fb564c",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  },
  {
    "id": "exp-v1-recovery-r16-go-generation-0204",
    "canonical": "3d97937cf5465e48137a46acad8091f18c2f5b2560fd09de4032526ecda44491",
    "file_sha256": "d2e26f317a6c47bd128835a58c673eb3ad9ff91f64cdaf60684d93ddbe253047",
    "prior_canonical": "c70866696af5d51a3f0824fde9f9eff98b09f4bb7c77da39882352c2d1605a7f",
    "prompt_sha256": "e9e812bc007a21c737711dc24f594f97ada4b259f4255cf1a9bdb1ac8d48eba2",
    "reference_sha256": "2424122709a2ee8f2ad30f3e72ad765b84a3577c900137430ed86709fc82de77",
    "mutant_sha256": "a8c44ed562a5dfece2390acde8a50f0aaae05a4a652dba9f0786e3f6f97f3530",
    "tests_sha256": "0ecb20d944c1fdf6f30a8e73320dd59e1022aea8f2ef6a357d468a16540f8d87",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16354",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "09349138b994b5c18ab98cccc2c9c01ec0be86ef67bacfb114cf2e2eb8ded28f",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0204 from exp-v1-go-generation-0204 sha256=b0911cfea3b4bfeaa79feffc2e1ef1fee103e28aba5320515d0cbdaebcd6b5ce",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  },
  {
    "id": "exp-v1-recovery-r16-go-generation-0234",
    "canonical": "cf305e7e5bc61fe1d6dad18c1d96eaebd8c8934e0f0aa721b0f4484b16e364e5",
    "file_sha256": "ec2b795eec25f0ac105130ddb6394789974ca55499869edd306a4262cc6ad101",
    "prior_canonical": "958417d368d3c44592112e70ad6a93d2ae5203cea8b12b645b6e377ef631c5e2",
    "prompt_sha256": "08adeaf5405cac0c74c03549e6946a071f48af69f21612c9cd5f5db2e89bd8aa",
    "reference_sha256": "8f175c2570d309096148270362739b7ce5d3fc2ca93d0d0d3e46412ef16c472c",
    "mutant_sha256": "a6c39329331ac0019e4af76d6cc154016b1ab7854603052f6b96ab8ace15c6bc",
    "tests_sha256": "2bee1f70be5b1dda0b33a130effa25d32484d7b0488c851c78d06ef1ab62abee",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16024",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "ed2c415ddf87fc00c1fb1bff954cad48fba6f081ab5df1adfa8d0a70dd2fb508",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0234 from exp-v1-go-generation-0234 sha256=f743b378be9f7bcb536e86973669c1cbead45f0b1556d79cc8077f14c19682cb",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  },
  {
    "id": "exp-v1-recovery-r16-go-generation-0266",
    "canonical": "8fb5d807591356c90fe834d8b9fe19b185f6f812ef7c98f714924f2753398d75",
    "file_sha256": "297f082dd08ef68671e74efd623910302054d85389cbd93b13a65a863ac6d18a",
    "prior_canonical": "7168f5f04b9cbc6748e07eb6568d59d10a8c8143c7120b3248292ed4c768a0b9",
    "prompt_sha256": "25eec8015b99b6c362e7a4e00698f12668abe810cf7dcaacc4e46559dc0cbc9f",
    "reference_sha256": "97d3bff918944731aee4c936b757dfba8b8f54fe394c87326477956f68db8993",
    "mutant_sha256": "a1357433313a59a97eb96dd15c6a27a91bed22a4727cc400d06fdc95a9ce6f2c",
    "tests_sha256": "4e59d5e6425acb659fac938bc09c5eaee7e21786c7235f1acd7b703aa6dd622b",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27933",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "ab17b5ffffac705bf869be22178b87c4b871154953c844fad7a15ace67ab4574",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0266 from exp-v1-go-generation-0266 sha256=16aab2d4078c16d399336e6fba8bccb6c41a7162f2f2093fe95fc30c7428a122",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  },
  {
    "id": "exp-v1-recovery-r16-go-generation-0326",
    "canonical": "24f4a91a5409028aff5ea634fe9b0622ee678ae7545e1abe39517feafb097a29",
    "file_sha256": "cd143f4bdd1d4f9b06bff7934968d77a4a0a58783d4bda6c66ee4cf500a88582",
    "prior_canonical": "c5dc02ecff1a44e9665cf05135cc405a21dfbfa6d7db1e1d01f99530cd277c51",
    "prompt_sha256": "27b49d1da63279c5a563c33db59445f9b0a302ebb4520388f79629af6453be4d",
    "reference_sha256": "2e7ff20fa52c15f7ba6b6bb00ba666ba0847a65e80a63905f945bfd7ae3cf286",
    "mutant_sha256": "045ab73fd3bb5bdd5ce0b8bb74dff911df74137d342cde3df6bce77482c76ffd",
    "tests_sha256": "ceac3f5f0e70f28d855bdf64534ca92d47e4aadc0ccb306a3d5c79431be470e4",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27592",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "bac2bf7e045a0e74c24de49502e2f7b8e0d6c496852577d089e1033cc3e627ce",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0326 from exp-v1-go-generation-0326 sha256=643ed0c3f460d89800673636d0609ac2250861752908ecb56f713e0ed0737198",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  },
  {
    "id": "exp-v1-recovery-r16-go-generation-0360",
    "canonical": "7c0df1ec8e8689b24238ace112e6d083b754508e16bc78cdfd16afae3dd2ecd7",
    "file_sha256": "a7bfe5e346b53fdc0ef858e82c0b52773b7c5744a5b49346cc24086958013f63",
    "prior_canonical": "5fc2ec2a2e5543aa175c61779c41d466f654270f656112143b213164d8bf845b",
    "prompt_sha256": "5fc2df7593c4518ab20f0a229bce250148172018bf5ed9bc7ea494b6b888dc4b",
    "reference_sha256": "4271ddcd4d169a9109f5e3d2e17f7e06b6b27c1eebc052b53995316cb0a48286",
    "mutant_sha256": "27f0a0e4a2fcf194a8096273ae3d9c1c36674eda77da1830c6b323a023687397",
    "tests_sha256": "a281656ca986644c59b46780ccb8f930742d397412983f24867ff1a53773af33",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-16165",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "0f63b789406e6aa6a42aef17a260a48f94c7ba543cd0869e4f2055e55556190e",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0360 from exp-v1-go-generation-0360 sha256=64b45b8fc1a1ce9398a14fb2e1bee722871bd506168b02d7dc1f2a95efe05846",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  },
  {
    "id": "exp-v1-recovery-r16-go-generation-0409",
    "canonical": "ab20ac4fdb0acc5cf962bb64a28164aa293ab2a8772d970963f55e489e121b64",
    "file_sha256": "5485afba3913b14ef46a4756ce170d50ab2428eb978ed23d3f5839d0f235959b",
    "prior_canonical": "6266a732a2380a001bf495c6df15c060b461cce1453e633d0ebf7516a423e3a3",
    "prompt_sha256": "c828c29d44f4df3de7a6230a332aa3875208275ab9facd92c732851208b6c8ff",
    "reference_sha256": "0cb4b30809b79cc03d18710a82d51a2bf930744d03dc0a2847755b5bc98b604e",
    "mutant_sha256": "7444cadb0424c9163e99313a043a735cf4037436f92fcbf1ab6b400bebc43111",
    "tests_sha256": "01022c95a51d6de50efd37ad39684a721cb19c9ff148dbf762d57cf9aba44ffb",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-27838",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "8899c769f9ffec50841fee8bd2b11c552352f69d5cce428b0ab75ae0a41c8797",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r16-go-generation-0409 from exp-v1-go-generation-0409 sha256=a9adb8cd38d9b6a6d8c6217e807c6139a9cd7939785e1234255c9cbf581ed5a8",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    }
  }
]
```

