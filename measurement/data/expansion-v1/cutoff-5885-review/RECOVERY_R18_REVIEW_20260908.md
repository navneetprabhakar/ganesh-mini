# R18 independent corrected-test review — 2026-09-08

Gate 2; exactly Python repair0138 and Rust repair0102. **Two scoped static positives, zero holds.** Full current specifications/references/tests/mutants read against R14 and approved R18 feedback. No candidate execution, generation, admission, central mutation or new original-row coverage. Main owns fresh qualification and admission.

## Python repair0138 — scoped positive

ExplodingFloat and the custom validation-before-aggregation priority test are removed, with no substitute custom-number oracle. Ordinary later rejected nonfinite event still raises ValueError before a result can be returned. New accepted integers 10**500, -10**500, 7 yield count3/exact integer7; a rejected huge integer contributes nothing, and a rejected huge value followed by a malformed rejected category still produces the specified validation error. These use ordinary numeric values and do not impose a custom arithmetic/validation precedence.

Accepted huge integers remain a decisive witness of the retained lossy float-finiteness mutant. Fraction exact totals, native mixed Fraction/float OverflowError, accepted-event addition order, finite floats summing to infinity, bool/nonfinite validation, UserDict/MappingProxy and iterable acceptance, accepted-only category order/counts, no input mutation and fresh list/dictionaries are retained and contract-grounded.

Reference is unchanged: explicit float nonfiniteness validation avoids converting exact integers/Fraction; native addition is not reclassified or given an extra output-finiteness requirement. No cap, global digit-limit mutation, private layout or new numeric class behavior introduced. The original accepted-only correction remains fixed in the embedded mutant, leaving the realistic finiteness-validation defect. No remaining concrete unsupported oracle found.

## Rust repair0102 — scoped positive

VT is removed from the whitespace rejection loop and is now tested as permitted qualified_ref content. Rejection covers precisely the named predicate's space/HT/LF/CR/FF set; no new whitespace definition. FF is also added to surrounding slug padding and empty-result controls. U+2003 slug prefix/suffix preservation remains the decisive Unicode-trim witness.

Exact-one .git stripping, operation ordering, trailing slashes, last slash/colon component, empty/malformed cases, stable primary/supporting/tag ordering, deduplication and branch/tag identity separation remain valid. Tests use only shown public traits and API; no URL parsing or private-state assumptions. Reference retains the correct trim_matches(|c: char| c.is_ascii_whitespace()) adapter, avoiding the earlier signature error without broadening semantics. Embedded mutant retains the corrected single-suffix behavior and only overbroad Unicode trimming. No remaining concrete unsupported oracle found.

## Seven criteria and boundary

Both have self-contained clarified contracts and consistent public APIs. Corrected tests have independent specification/test/feedback provenance, valid ordinary boundary witnesses and no unsupported oracle found in this bounded read. Complete targets combine numeric validation/ordered aggregation/ownership and reference parsing/normalization/stable category deduplication, respectively; neither decision relies on patch size alone. References/tests are idiomatic standard-library-only, deterministic and isolated from external services. Known-bad defects are realistic and distinguishable by the explicit small witnesses above. These are seven-criterion static positives, not executed results or admissions.

## Immutable bytes, source, rights and critic provenance

Both R18 specifications, references and mutants exactly equal R14 bytes. Previous R14 canonical hashes match approved feedback; source fields excluding appended transformation match plan parent source; rights match both R14 and plan parent rights, retaining all five approved flags. Embedded broken source exactly equals supplied known-bad code. Original canonical parent bindings are carried from the already verified R14 review; no source/rights decision reopened.

Each correction prompt has exactly one id/problem/prior-test object and approved specification_review text, matched to R14 and feedback. Emitted tests equal exact critic output after strip plus terminal-LF normalization. Prompt and raw output hashes verified; both calls returncode0, timed_out=false and no disallowed tool items. No separately corrected reference is exposed. Repair specification includes the complete broken input, so generic critic boilerplate claiming it has never seen known-bad source is not literally accurate; evidence establishes separation from the corrected reference, not blindness to the embedded repair input.

## Evidence hashes

- datasets/cache/expansion-v1/versioned-recovery/r18/plan.json: `512e3219da55465742728f2c5116840498e4a41c5a2bfe8f5b0130d9a19690a0`
- datasets/cache/expansion-v1/versioned-recovery/r18/run-contract.json: `2f51b84529d1fc1a33301f7ae88a0628921aa72caa67d474655d915e550005d4`
- measurement/data/expansion-v1/cutoff-5885-review/recovery-test-feedback-r18.json: `b37dd72bdaf3363650dd5f72762f150d4117890f13d8faaf84d3564c0cdb39fe`
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R13_R14_REVIEW_20260908.md: `f4e7d9a8b06f5690334b76a81275f03fbb67761a0c8bcf6202b12b4b553ee409`
- datasets/cache/expansion-v1/versioned-recovery/r18/python-recovery-test-correction-evidence.json: `073ba7eb465c79426f8e2135dbc8bdf671517741d4ec7da8f0e6b4102de381bf`; prompt `69b6c90a41f7c2905d11dd138393c15b39dfca0f9d620cb43d8b180ce8e94756`; raw output `6b49822a9a46ed2bbd9fdc9cfb7ee24f6027a3944c519b75b561ce99ca03b47f`.
- datasets/cache/expansion-v1/versioned-recovery/r18/rust-recovery-test-correction-evidence.json: `44dc3fb8e710854313ccfff5339d8a71dde8ceb10bc00d1b9c38cfc45d051d2f`; prompt `b32e42b875895ba9dfe7fac641b5b1ad6395a6f40894779917cda6a87a5e97e3`; raw output `ff79176d46990d7fb620f68276d89401266067b0d953a6ba9fda050ece4df1f9`.

## Exact candidate bindings

Canonical hashes use sorted compact UTF-8 JSON; file/content hashes use exact bytes.

### exp-v1-recovery-r18-python-repair-0138

- file: `datasets/cache/expansion-v1/versioned-recovery/r18/exp-v1-recovery-r18-python-repair-0138.candidate.json`
- file_hash: `5bab2ab51b60ac7c7aeb1226ce48d246c11d9f4d3abf7b5b6af50611a49f88eb`
- canonical: `14bdfd447a5e1126794419cf7d1e59d0f6ac2bd39c2ab783b05c62f86e689dcd`
- previous: `d510f25bd5b259f24dcb32ad719a010f970fc8af350827526df2407b5fc926a9`
- parent: `097e1648410b0391b52875d213ea6a982c8d3418fe08bfd48153bf2c6da17c72`
- prompt: `3e9530f8fdd09d0ac73827fa5fa1987318f9efc6674002ebfa0934b0c1c16200`
- reference: `a343644ad08e3f93bd8f4a1e0f3f6af06a69ce2e46eedb388e4d474fa520a197`
- mutant: `73863c0d4a7512b23d97468999075f0f08ec352f543d9d5d24f5790d94919779`
- test: `636c93dad46e67b9452c4b320aac32157fcb07bb8b673ee8e1915c939fa23387`

Source binding:

```json
{
  "dataset": "m-a-p/MdEval-Instruct",
  "license": "MIT",
  "license_uri": "https://opensource.org/license/mit/",
  "record_id": "row-01990",
  "revision": "38c9197e3add996fae624eb198ebd06155b2101e",
  "source_record_sha256": "73599e4b3e0df122a094495051835c773da202b671b7dc60365f75a9854362de",
  "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r18-python-repair-0138 from exp-v1-python-repair-0138 sha256=097e1648410b0391b52875d213ea6a982c8d3418fe08bfd48153bf2c6da17c72",
  "uri": "https://huggingface.co/datasets/m-a-p/MdEval-Instruct"
}
```

### exp-v1-recovery-r18-rust-repair-0102

- file: `datasets/cache/expansion-v1/versioned-recovery/r18/exp-v1-recovery-r18-rust-repair-0102.candidate.json`
- file_hash: `2dcb6f026ad2479ef9583091ef576eb4f583e2ce7acf3c790fc5557a4451e59f`
- canonical: `d62414c000b4ecd8d1660e29066a65404316398f62aebfd6dc9ad0f1960833d5`
- previous: `4d58a05badc57e8b8cc24efec7263633d26e7eed2c88814c063455cb783a93ef`
- parent: `8c2b016284660327c9d77e34b6ccf76585bcaf4e147c761ef4d9bfe7d4a923f0`
- prompt: `43d8a017a339391d2af9944a758a6b8aee68964c2c4b7a6f6bcbc3e4fa32fce4`
- reference: `29be4e94463fd7b8c1aa670cb7c750e6db3d93cd71aaaab0412d6ccd61bf54b2`
- mutant: `6b2ec40b5b9a4653c04112c1490efe0704952f24c0bede3e1b95de727ea94637`
- test: `4a200c99d65d2674384f858c4de0d89649bd7adeb1e86fdc5960e19a3b6cf33e`

Source binding:

```json
{
  "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
  "license": "CC-BY-SA-4.0",
  "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
  "record_id": "row-03276",
  "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
  "source_record_sha256": "d11d77577758ac7332e12deb503c8cf60f1257cbd1c6e0fe66cc774fe35152b2",
  "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r18-rust-repair-0102 from exp-v1-rust-repair-0102 sha256=8c2b016284660327c9d77e34b6ccf76585bcaf4e147c761ef4d9bfe7d4a923f0",
  "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
}
```

