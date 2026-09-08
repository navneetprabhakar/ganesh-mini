# R12 Python independent recovery review — 2026-09-08

Status: static review only; **2 scoped positives, 7 holds**, all nine assigned generation candidates reviewed. No execution, admission, teacher calls, ledger changes or new original-row coverage. IDs below use prefix `exp-v1-recovery-r12-python-generation-`. Full original prompts/references/tests and complete derived prompts/references/tests/mutants were read. Approved R12 Python records and relevant nine Python scopes in RECOVERY_NEXT_PYTHON_RUST_20_20260908.md were reconciled.

## Dispositions

| ID | Disposition | Substantive finding |
|---|---|---|
| 0070 | STATIC POSITIVE | Assignment recognition now precedes header recognition, explicitly documented for significant lines containing '='. Existing test_normal_comments_blanks_replacement_and_order contains both value=[brackets] and tail=ends], which the original reference/mutant rejects as malformed headers. Split-first-equals, empty values, duplicate sections, late invalid types, replacement order and fresh dictionaries are covered. Bracket-free header-name rule is explicit rather than an unexplained restriction. |
| 0097 | HOLD — missing held-defect witness | Mapping acceptance is correctly changed while explicit list/dict/tuple inputs remain. Tests use only dict scoped_suffixes; neither UserDict nor MappingProxy is supplied. The dict-only mutant remains observationally equivalent on the current suite. Add valid non-dict scoped mapping {('src',):('.tmp',)} with src/a.tmp and independent dry-run copies. Existing union, order, prefix and nested ownership tests are useful and have no identified invalid oracle. |
| 0259 | HOLD — missing held-defect witness | SignalSpec normalizes the outer Mapping before deepcopy; catalog stores detached specifications, preserves insertion order and repeated-add construction. All tested labels are dict or invalid list. Add MappingProxy {'tags':['api']} and UserDict labels, mutate backing tags and returned find/all copies. Existing nested-copy tests do not reject the dict-only parent/mutant. Do not demand retention of concrete wrapper types or mutate public attributes into a newly invented validation domain. |
| 0399 | HOLD — missing held-defect witness | Reference now accepts the approved character-set grammar with [a-z0-9-]+; state edits stage before commit and returns are copied. All valid tested slugs satisfy the old stricter hyphen-placement regex. Add a--b, -a, a-, and nonempty all-hyphen controls through constructor/detail/edit/resolve. Current tests cannot reject the held grammar defect. Existing uppercase/underscore/non-ASCII rejections and failed-edit controls are valid. |
| 0400 | STATIC POSITIVE | Derived contract explicitly uses str.isidentifier and nonempty string target. Registration parses Unicode names once, retaining parsed wildcard/capture identity for resolution. test_unicode_identifier_and_fresh_parameters registers /users/{名字}, resolves /users/alice and checks exact Unicode key and independence; the ASCII-leading parent/mutant rejects registration. Specificity, ties, root, duplicate names, terminal wildcard, malformed paths and inventory routes are tested. A Unicode wildcard-specific control from selection advice is absent, but the exact held defect is exposed and the same inspected name parser handles both forms; this is not a missing-defect hold. |
| 0471 | HOLD — missing held-defect witness | Correct reference separates root-capable entry validation from non-root document validation and preserves profile-first then anchor fallback. Tests include root-level markers but never the root entry '/' itself. Those are different conditions: old _parts accepts /ember.lock. Add nearest_bundle('/a/doc','ember',{'/','/a','/a/ember.lock'}) == '/a', plus {'/'} fallback. No physical filesystem/type metadata oracle is warranted. |
| 0717 | HOLD — missing witness plus reference scope regression | Outer fields Mapping is correctly normalized before deepcopy, but tests never supply MappingProxyType, the exact held defect. More importantly, new _validate rejects non-string kind with TypeError. Approved scope expressly retains invalid-kind ValueError versus malformed-field TypeError; original None/1 controls expected ValueError. WorkMessage(None, {'id':'r','accepted':True}) now raises TypeError, a static scope conflict outside the allowed copy correction. This cannot be repaired with tests alone. |
| 0741 | HOLD — missing held-defect witness | Mapping records now accepted; Sequence matrix validation, bool rejection, bounded pixels, arbitrary-size stride and per-target deep copies are coherent. Current records are dicts only. Add UserDict and MappingProxy records containing [[0]], sector s, distance d; assert both targets and isolation. Tuple matrix control currently checks partition counts without asserting a concrete list wrapper, which is appropriate. |
| 0744 | HOLD — missing held-defect witness | Outer item/collection Mapping snapshots precede deepcopy; duplicate IDs, votes ordering, separate pages, repeated resolutions and copy boundaries are coherent. All tested items/collections are dicts. Add UserDict/MappingProxy item(s), repeated collection references and mutation checks. Negative integer votes remain allowed; add a valid negative vote control, not a rejection assertion. Huge page and vote controls do not replace the missing Mapping witness. |

## Seven-criterion accounting

1. **Clarity/domain:** Scoped contracts remain self-contained. Seven reference-fix prompts are byte-identical to originals; only 0070/0400 have approved clarification changes. 0070 explicitly prioritizes assignment lines containing '='; it must not be reinterpreted by reintroducing header-first recognition. 0400 names Python identifier semantics, without URL decoding or keyword exclusions. 0717's approved error distinction is the exception identified above.
2. **API/correct reference:** Eight have a scoped static-positive reference assessment, subject to normal execution. 0717 needs reference correction or a separately approved contract decision; do not let its current tests redefine the approved error behavior. Generic hostile descendants, unlimited resource guarantees and wrapper preservation are not imposed.
3. **Independent tests / valid oracle:** Provenance is verified below. No concrete unsupported oracle found in current derived tests. Seven suites miss their defining held witness, so independent origin alone is insufficient. Some validation tests allow TypeError or ValueError where the prompt specifies one; this reduces discrimination, not an unsupported demand. No tests access implementation-private fields.
4. **Whole-target nontriviality:** All nine retain substantive interactions: parser grammar plus ordered replacement; union/filter plus deep ownership; catalog insertion/identity/copy; transactional editing plus routing; route specificity and matching; two-pass hierarchy search; schema-dependent immutable view; cross-target partitioning; cross-list resolution and pagination. Small Mapping/regex corrections do not make these entire targets elementary.
5. **Python idiom:** Standard Mapping/Sequence checks, dict/list ordering, deepcopy and explicit parsers are reasonable within the stated standard-container domains. 0717's issue is behavioral scope, not style.
6. **Isolation/self-containment:** Sources/tests use standard-library imports and solution.py, no filesystem/network/environment dependency, private-layout coupling, clocks or random oracles. Actual pinned sandbox execution remains main's responsibility.
7. **Realistic known-bad failure:** All nine mutants are exact original parent references, preserving realistic original defects. Two have concrete suite witnesses identified above. Seven need test strengthening before directionality can be claimed. 0717 additionally changes error behavior beyond the targeted defect; its mutant is not a perfectly isolated diff against the new reference, which must be resolved rather than silently ignored.

## Recommended next boundary

Main may combine the two static positives with independent execution/separation gates; these are not admissions. Six holds (0097,0259,0399,0471,0741,0744) are suitable for one bounded test-only correction if authorized, preserving prompt/reference/mutant bytes. 0717 is **not** test-only: first resolve the reference's invalid-kind regression within the approved scope, then require a decisive MappingProxy witness and normal gates. No further correction or teacher work was launched here.

## Lineage and independent-author binding

R12 plan: `datasets/cache/expansion-v1/versioned-recovery/r12/plan.json`, file SHA-256 `0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121`.
Approved selection scope: `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_PYTHON_RUST_20_20260908.md`, file SHA-256 `bfd5af2666f35a2d67bb6babba881b76149794de7ede6ba714e0720c57a18181`.

Both author evidence files reside in the R12 candidate directory. Architect file `python-recovery-architect-evidence.json` SHA-256 `6b065649bf750ec41be3500d8add5cf0c08ce8c4984e350c3cc3965875c664e4`, prompt SHA `04292a311227ea415ca0a0c6016e7337831a5db199e33205f5286fa6f4d1a5f3`, raw final SHA `4006af5e4d39311097a3e1cf0eb24a273f82dd9ef722443412f3d6fdef312ac6`.
Independent tests file `python-recovery-independent-tests-evidence.json` SHA-256 `2659288427a6ea8ffbac5f5c5bfe3c037d7bb717e82d9a57387ed4dccdca17d6`, prompt SHA `44a7e9c095fa4209e2a2a4579b6f87b7521c6d4544c96002950725522ca71539`, raw final SHA `13cb05ebf323b51d180f5a4776fcafdf7174c1ea4494d3e0ec5056ac7f7964aa`.

Recorded author calls are separate ephemeral gpt-5.6-sol/medium processes, read-only with tool prohibition. Both returned 0, no timeout, no event parse error and no disallowed tool items. The complete independent-test prompt contains IDs/specifications and generic testing directions, not reference/mutant/source tests/architect context. Exact emitted test_code was compared with each candidate test file; architect problem/reference_code/known_bad_code were likewise compared with candidate bytes for all nine. This establishes the recorded separation, not execution correctness.

Every original canonical hash was recomputed and matched the plan. All nine preserve original source fields except the additive versioned recovery transformation, and all five rights flags (prompt, answer, tests, model_training, redistribution) remain true. Source data are McEval-Instruct revision 57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0; preserve attribution/share-alike metadata. These bindings are not a fresh legal opinion or publication decision.

## Exact per-candidate bindings

Candidate paths: `datasets/cache/expansion-v1/versioned-recovery/r12/<id>.candidate.json`. Canonical hashes use sorted compact UTF-8 JSON, ensure_ascii=false. Other hashes are file bytes or exact content UTF-8 as labeled. The full source transformation is included to separate source provenance from recovery author evidence.

```json
[
  {
    "id": "exp-v1-recovery-r12-python-generation-0741",
    "parent": "exp-v1-python-generation-0741",
    "parent_hash": "8be310442dba97d554be2561d473d8ca7934207a377c12d1db0c6d39e8440a82",
    "candidate_hash": "727cce89478bf7a7e45876b1c0de145bdb5f47735d06fc7934ac9942f231e047",
    "file_hash": "be87d213067062c9d55c918d239d743efcfef7c25c67b0889474261e659fd0eb",
    "prompt": "36957cd7be2a735650abab3571506d4c2e2177577e5de0576e0a71b4ffefbaa8",
    "reference": "6ed08b6d38339aa4c5d083168505d7a08b9e60b0a299b68994d7f5320ff14cd0",
    "tests": "1c5f3aaade605021ecbe16759a713256890f9093d7bec8c86c264a2416c209d7",
    "mutant": "0654fb10b11f2165d1a9a655d14ae10da7b755f57f1efe8ea718f76ea9069915",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-04018",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "08db021eb4b30cc79961f91e3fc9c6473c0cf6136c1462b771fd875f3e167d4e",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-python-generation-0741 from exp-v1-python-generation-0741 sha256=8be310442dba97d554be2561d473d8ca7934207a377c12d1db0c6d39e8440a82",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/examples-userdict-result.json",
    "hold_evidence_file_hash": "8c9810c932618a508841778e005ac9a5c91526e79573d8f1305270ca986360ef"
  },
  {
    "id": "exp-v1-recovery-r12-python-generation-0744",
    "parent": "exp-v1-python-generation-0744",
    "parent_hash": "efc1b28c3fe07967b43185a885b838fdfe1cd090e1f4c8816a7774c5bb25b126",
    "candidate_hash": "ab2daf94f57723d3e226e6844819fada728e0d180bdddc333a217ad2b5845a18",
    "file_hash": "643a3652023ad952a26693103e482f504d4831977fc630ff72e3a24492675b33",
    "prompt": "2fc177499dea298ce295e6bdb25374f0751ef2b2260f30535cf35c30d033e232",
    "reference": "19ae7b3adbf4e1b13eaf142f7931dfa2b08565efd764e23e97963363b43623ef",
    "tests": "69028583438ab4ec419b7520f90467ac9c3e8075150fc0b1c58be2e7cf419ed3",
    "mutant": "48c5864cc2ac0b98047f402e8930f6ee55f6db510a7b5f968fc7470f860dcf27",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-04056",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "1785299abb85e4f4b6199ba0b1c06e9ada6a32b36de8a19dab5bcb456a7d26b1",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-python-generation-0744 from exp-v1-python-generation-0744 sha256=efc1b28c3fe07967b43185a885b838fdfe1cd090e1f4c8816a7774c5bb25b126",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/catalog-userdict-result.json",
    "hold_evidence_file_hash": "06125f7223c88dff4d5bd36cade54fe463d60df5036f51f64549c14ed094a252"
  },
  {
    "id": "exp-v1-recovery-r12-python-generation-0717",
    "parent": "exp-v1-python-generation-0717",
    "parent_hash": "4432a25372e0cd1ef3da2401dbab9b82886ecdeb5d0a791dbf22d3fb4768e3e4",
    "candidate_hash": "068140f7cd0ffbab9afd76b9a283b20d223e306e83d784e9332c0114bda33114",
    "file_hash": "54f9409debe5782b15c9459a8843e65501394d7c3daa4b4d9ca2c8be92df3779",
    "prompt": "49701ab781d8b5d856d109aab003eefd3548095d2471b20e8975195434763be5",
    "reference": "ae154eeae0a17d6ac414a40f5e111d3c4846d50df8e6cc0a53164c8d31f38a91",
    "tests": "cbb2eee7037015dda9b7cd4e5d4603bfab5f281b749d3e00b5ed4d7b61193033",
    "mutant": "f91b9e8db5d9bed1193c2a386981e530ceb046e60c3da4635e5d6048f065b07b",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-04048",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "b8192424da7167dcfab7af8b53b2274881ef6bc31f775bd4c07e409ddb958cca",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests; versioned recovery exp-v1-recovery-r12-python-generation-0717 from exp-v1-python-generation-0717 sha256=4432a25372e0cd1ef3da2401dbab9b82886ecdeb5d0a791dbf22d3fb4768e3e4",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/work-message-mapping-proxy-result.json",
    "hold_evidence_file_hash": "948083cbc072008d4c6cfd23cd2ea910e38c0fe5a39818603c737d9b4c6f1a1a"
  },
  {
    "id": "exp-v1-recovery-r12-python-generation-0097",
    "parent": "exp-v1-python-generation-0097",
    "parent_hash": "87284237d18ef56e4228b6dfaaf25aca4f61c58d448072ed5eec64fe8f2b4552",
    "candidate_hash": "a7ef3302a392362628beb273701bcfc9b16f7ce206c4c1a145d9987670a885f0",
    "file_hash": "a4f90a76897c995b957f645b9a0c4e801e580404659609321a6ee18e9dd17ccc",
    "prompt": "fc4a97bec60e3c1bf4b564e3b3cf4c8a04711f809a7170c5699e2b11c999d522",
    "reference": "91b3d679428d4f1388e12a28ede303e0b4cb30362be98c71edc1485b5ee39743",
    "tests": "1759729460046aa815025c590a1b03199b70554733cb1faa57432b792851b043",
    "mutant": "3b9048e541eff229e17381086a065ac61987dc82473fae9546b794ca2d2f8c30",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-08189",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "5d6d19b5258187e638c8ed23b2cc38769a138404be070f463eb6d9f009825ff9",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-python-generation-0097 from exp-v1-python-generation-0097 sha256=87284237d18ef56e4228b6dfaaf25aca4f61c58d448072ed5eec64fe8f2b4552",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/catalog-mapping-result.json",
    "hold_evidence_file_hash": "d40c75d7fab8dc86a806095c2a7f848bbe6b47a293c9414a04f3439e7e906728"
  },
  {
    "id": "exp-v1-recovery-r12-python-generation-0259",
    "parent": "exp-v1-python-generation-0259",
    "parent_hash": "41895584e60c005b6ac53a2bb5072605e35aee52ab910a796f1c704f9b6a80e0",
    "candidate_hash": "0c61dc5d92a1d4c30a91592b1759ebcf5d9e0b59146c59e596cfa92ae416dd88",
    "file_hash": "bbac7e8dceea45d1977ae61cceba64e32b839b2d845b68597907136110433e1d",
    "prompt": "c20049bb4562fad3ae085104b2e9c5c3d78fa880a5c7f1ef7559811f38e5caa2",
    "reference": "4659f3bfa280e64b93b882e271f9ec1101c728899d39c80306e670d1e40241c1",
    "tests": "cca519d76f3944ffb8370c1332c751822f606b93f89680fd8634d8e36fed7815",
    "mutant": "0ee27b5b502cea284a4e44eb1fcb96c894a3271f8a5872eb376e9981a1fa3e82",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-04040",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "6e8f62dad9737a2e8c9774d5659f8eaebddbde363ea85456194fc0093994d35e",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-python-generation-0259 from exp-v1-python-generation-0259 sha256=41895584e60c005b6ac53a2bb5072605e35aee52ab910a796f1c704f9b6a80e0",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/THIRD_BATCH_REVIEW.md",
    "hold_evidence_file_hash": "79a4d72b8e77ae856cf2798cf48c7a8f4e8f6ba052a44ce183a8f86c4c0f03af"
  },
  {
    "id": "exp-v1-recovery-r12-python-generation-0471",
    "parent": "exp-v1-python-generation-0471",
    "parent_hash": "a563fb4850e489aa1a783828e5a96885e06401b33761b8224fb8636a7208234f",
    "candidate_hash": "4dfb8be99c9b246b3989f126d970cad0590ad0150001a21fa5d23acab87ae8dc",
    "file_hash": "eeb133d1c4b36879aa54c3eeb06d1e0b877ae6ce6078f9c4fe86c64b94ea170c",
    "prompt": "ce5355943765d4cc29aa73396eb131bf456f339222799677ab7381a104ed1956",
    "reference": "67a22d1fc9e556936b90e527b5aaf03cd785e7b4160579abb67806968f37ddbe",
    "tests": "7e1ef321a96dc332afcfaac2541d47c766e240e1c799a16f02532b3ff3d440ec",
    "mutant": "cf6b85867afd14a13ca09ddbdbf7722037de56b716f130c3f183593391815bae",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-08440",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "140dff21f72b0d2646c02cea8e67b9165977face0fce9e867f62b8175f5a8349",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-python-generation-0471 from exp-v1-python-generation-0471 sha256=a563fb4850e489aa1a783828e5a96885e06401b33761b8224fb8636a7208234f",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/bundle-root-entry-result.json",
    "hold_evidence_file_hash": "f4d05f662fdd01d987375d70de593def5887bfe01f00cb7bc2a72f568e2690cf"
  },
  {
    "id": "exp-v1-recovery-r12-python-generation-0399",
    "parent": "exp-v1-python-generation-0399",
    "parent_hash": "24f839845ad5637c73cf7736dc648be9887d8b60c01dceac99733d9bde1b91dd",
    "candidate_hash": "692828d94f580bcb292b10f88a57f6d23549a3769f8e7deeb4d8856c354468b3",
    "file_hash": "f81d392ca66e1f7ac781ac409b473a7d3d47a89b417dbfdfd552b94f0ad4833b",
    "prompt": "9644fdf70f8fed6169e9c6100e70b36bc2e973bc1e9bc942a0da511ff6d34585",
    "reference": "b2af6cf002d908ba4f87d575c4e01d970a0551afd0824fb6a90e5268b666bed0",
    "tests": "88e21eefe5101095e0ca4530c82444ea38706df7d1ba7d163efcce0112c59f97",
    "mutant": "36f1f6dd199a2c0a2b990b4064a023078292ab3e4bbdbc19aca6f901a6961a34",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-08535",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "140997ab57987ecdc4375c608136ce69ddcb21af6f5670ecb48a9ea9e16b52da",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests; versioned recovery exp-v1-recovery-r12-python-generation-0399 from exp-v1-python-generation-0399 sha256=24f839845ad5637c73cf7736dc648be9887d8b60c01dceac99733d9bde1b91dd",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/recipe-repeated-hyphen-result.json",
    "hold_evidence_file_hash": "d83a240883dd5a1905fbefbdf02d87630aad36e3633fb1b15cae4cc9e11e1aa1"
  },
  {
    "id": "exp-v1-recovery-r12-python-generation-0400",
    "parent": "exp-v1-python-generation-0400",
    "parent_hash": "08fe6f4c5794d1490ff040fd14e8354e41f0a397d0e824175ac00b44843785f0",
    "candidate_hash": "12adf7b5af0bf0b1a969adec0e485e10ee02f8f4ff988aa7699e8d1ec8bbc925",
    "file_hash": "2de1c954d490cc635af51631c3d36ec86c865018d625c92cb13f3b92bfeaeef2",
    "prompt": "a1076181090b68c8f3954f626734d860e50b9a979c97280a928117a2de27d477",
    "reference": "c81cf24df0f58eca5f438b93456379089a045827d4fa650ca19cad4f91dd06ef",
    "tests": "ea50d3d3fb55c3f0c01c50fa4de89529736d24362c0cf622d4c911b7199e92e5",
    "mutant": "2e3c3aabc7f7cb488442e198e73f46883c50b6d76625f966c3b5c53e77689459",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-04326",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "077c6a675c6c7dac24218ce7e85b0d38722cf76983ced57a33acf58a7e8bf0d1",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-python-generation-0400 from exp-v1-python-generation-0400 sha256=08fe6f4c5794d1490ff040fd14e8354e41f0a397d0e824175ac00b44843785f0",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/router-unicode-identifier-result.json",
    "hold_evidence_file_hash": "43be30118be2e88e4c6647c5bc73c82c6c043d0bd03fcaf6b73798f2c756bb3b"
  },
  {
    "id": "exp-v1-recovery-r12-python-generation-0070",
    "parent": "exp-v1-python-generation-0070",
    "parent_hash": "408af975a047e2c7c813c957335ff3c3f4b12b7efc3b003257943fed5edfe8fa",
    "candidate_hash": "0b50616ecbc7ae8389d59a98047975870416e4c17efc5dce2f67bdf9a37443c9",
    "file_hash": "75521bc62e8accd3820799b6bf4b7e648e6b1dcc10f5be9cc9821073a631a462",
    "prompt": "0afd10a6e25c89f74b37985692af96a58237101fcb7bf1bbe40b4e5cca73971b",
    "reference": "95ac0e2fffaa932a0d88625e037d2ccee0c3393f9ad03d338563cf13d77733f2",
    "tests": "cf6ed15f7b7fc690f70f3972b05b3a80a04c45d102559f145de89928af612200",
    "mutant": "f73bbe182ed1401f85a2c22fe373076e0639ffc9526ef2c505cf42ae7daa70ed",
    "source": {
      "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
      "license": "CC-BY-SA-4.0",
      "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
      "record_id": "row-08214",
      "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
      "source_record_sha256": "22415b1dcdc3ed70a3e1d8677ac43eb6813281f2e936bcf0878edb6706a69a22",
      "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r12-python-generation-0070 from exp-v1-python-generation-0070 sha256=408af975a047e2c7c813c957335ff3c3f4b12b7efc3b003257943fed5edfe8fa",
      "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
    },
    "hold_evidence": "measurement/data/expansion-v1/cutoff-5885-review/section-bracket-value-result.json",
    "hold_evidence_file_hash": "2cbe5b854f2a291c8c76a501d5ba47abead0d2552cdcdef5e3c4146e684544fa"
  }
]
```

