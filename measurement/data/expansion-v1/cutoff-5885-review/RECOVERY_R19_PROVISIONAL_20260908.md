# R19 provisional architecture recovery — 2026-09-08

Status: **PROVISIONAL**, exactly two original held parents; main approval required. No reservation, generation, execution, teacher/cloud calls, new selections, ledger changes or admissions. This is fresh architecture recovery, not an oracle-only attempt to evade reference defects or another critic round.

Complete original and R12 contracts/references/tests/mutants were inspected (Python original full read carried from its R12 review; the R12 fields and original-reference mutant were reread here), alongside the main-read R12 reviews and approved scopes. Neither existing R12 candidate is admission-ready.

## Python generation0717 — retain reference-fix

Original parent `exp-v1-python-generation-0717`; required fresh ID `exp-v1-recovery-r19-python-generation-0717`.

R12 fixed outer MappingProxy copying but introduced TypeError for non-string kind, contradicting the approved invalid-kind ValueError distinction. None/1 are tiny direct witnesses; original tests and approved scope retain ValueError. R12 tests also lack a MappingProxy witness. Neither weakening the error test nor adding only Mapping tests fixes the reference regression.

Minimum reference correction: preserve outer Mapping normalization followed by deep copy; restore ValueError for invalid kind, with the ordinary type guard returning that error rather than TypeError (so unhashable invalid ordinary kinds do not fail accidentally in a set membership check). Keep the original problem bytes and all field/schema/ownership behavior. This is enforcement of the already-approved invalid-kind rule, not a new custom-object exception policy.

The new single-defect known-bad should retain correct invalid-kind behavior and reintroduce only direct outer-Mapping deepcopy. Independent tests must exercise both corrected requirements: MappingProxy reply/job snapshots and ordinary invalid kinds with exact ValueError. Existing field TypeError, key/value ValueError, raw nonempty text, priority bounds/bool exclusion, unique list tags, read-only properties and independent returned nested copies remain.

No private-field layout, hostile noncopyable descendants or concrete copied wrapper requirement. Full request rationale below is controlling proposal, subject to main approval.

## Rust generation0487 — retain oracle-rebuild scope with actual reference repair

Original parent `exp-v1-rust-generation-0487`; required fresh ID `exp-v1-recovery-r19-rust-generation-0487`.

Original and R12 specifications require Debug/Clone/PartialEq/Eq where applicable. ObservationStore's BTreeMap of cloneable/equatable observations supports all four; R12 omits them. Different-query-arity fallback is already correct and its mixed query test is valid. Passing current tests does not satisfy the missing public traits.

Minimum reference correction: add the four traits to ObservationStore, preserve all existing applicable traits on Observation/ModelError, and retain the approved R12 derived constructor/API/query-arity wording. Do not remove “where applicable” or deliberately choose an opaque storage design to evade the requirement. No Default, ordering trait or exact Debug rendering is required.

New known-bad must also supply all required traits and retain only the realistic query-arity rejection bug. Otherwise a compile failure could masquerade as the intended semantic witness. Tests should use generic public trait bounds and cloned-store independence without touching private fields; retain two-feature10/20 observations queried with one feature returning15, query-order, i128 extremes/truncation, updates/rollback and empty/unknown-model controls. An unmodified clone should compare equal; no new canonical internal representation across differently constructed stores is imposed.

Class remains oracle-rebuild against the immutable original parent because the approved derived contract clarifies constructor locations and corrects original query-arity tests. This is not invoking correct_recovery_tests.py: actual reference generation is required.

## Complete proposed scopes

### Python

PROVISIONAL fresh r19 architecture recovery, not test-only correction. Return exact ID exp-v1-recovery-r19-python-generation-0717. Preserve original/R12 problem byte-for-byte and all WorkMessage APIs. Retain valid Mapping support by snapshotting validated outer fields to a standard container before deep-copying; do not deepcopy an outer MappingProxyType directly. Restore the approved invalid-kind ValueError behavior, including None and integer1, rather than the R12 non-string-kind TypeError regression. Non-job/reply ordinary kinds are invalid kinds; avoid relying on hashing an unhashable invalid kind. Malformed fields remain TypeError, invalid keys/values remain ValueError. Preserve exact job/reply schemas, nonempty raw ID/tags, integer priority0..9 excluding bool, unique list tags, exactly boolean accepted, read-only kind/fields properties, fresh deep fields copies, and is_consistent nonraising validation without private-layout tests. New known-bad must preserve corrected invalid-kind handling and all other behavior and retain only direct outer-Mapping deepcopy as the plausible defect. Independently authored tests must include MappingProxy reply and job with mutable backing tags, UserDict and dict controls, input/property mutation isolation, invalid kinds None/1 and ordinary unhashable invalid values returning ValueError, malformed field TypeError and existing value/key controls. Do not narrow Mapping classes, demand wrapper preservation, add hostile descendant-copy policies or broaden a numeric domain. Both the actual reference regression and original Mapping defect must be corrected; weaker tests cannot substitute.

### Rust

PROVISIONAL fresh r19 architecture recovery, not test-only correction. Return exact ID exp-v1-recovery-r19-rust-generation-0487. Retain the approved R12 derived contract including ObservationStore::new, update and predict methods plus free new wrapper, and explicit nonempty different-arity query fallback; preserve unrelated original semantics. Fulfill the existing Debug, Clone, PartialEq and Eq requirement on ObservationStore as well as Observation and ModelError: all four traits apply to the supported store state. Add these actual reference implementations/derives, do not remove or weaken the contract. Keep atomic whole-batch validation, common observation arity per model across updates, empty update no-op without model creation, nonempty names/features, existing-model requirement even for empty query lists, exact-match averaging otherwise model-wide fallback, i128 sums and truncation toward zero, query order and no store mutation. New known-bad must also have all required traits and constructor surface, and retain only the original erroneous different-query-arity rejection; do not use missing-trait compilation failure as its semantic defect. Independent tests must instantiate public Debug+Clone+PartialEq+Eq bounds for all three exported types without asserting Debug text or private layout, clone a populated store and mutate one copy via update while the other retains predictions, and retain exact equality of an unmodified clone. Include two-feature observations outcomes10/20 with nonempty one-feature query returning15; mixed nonempty query arities preserve order; empty features error, unknown model with empty queries error, empty updates no creation, failed update rollback and extreme i64/i128 truncation controls. Do not restore original query-arity rejection assertions, add Eq ordering policy, Default or a new trait beyond the original four.

## Approval and future gates

Main must validate the current frozen corpus/hold ledger and review bindings before reserving R19. Preserve the original parent identities, source/rights and R12 failure artifacts. Fresh architecture and independently authored tests must use exact R19 IDs and pass quality plus network-disabled resource-limited sandbox checks; code-generation completion alone is not admission. Trait satisfaction and behavioral mutant directionality are separate obligations. No automated further correction loop is proposed.

## Exact bindings

Hashes are SHA-256. Canonical candidates use sorted compact UTF-8 JSON, ensure_ascii=false. R12 files reside in `datasets/cache/expansion-v1/versioned-recovery/r12/`; original parents remain in cutoff-5885/final.candidates.jsonl. R12 plan hash `0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121`. Full source/rights and original hold evidence bindings are preserved below, distinct from R12 quality evidence.

Reviewed notes (under measurement/data/expansion-v1/cutoff-5885-review):

```json
{
  "RECOVERY_R12_PYTHON_REVIEW_20260908.md": "4aa736c5fa48090c3a2c45b3798492231d61363f1ff8ffae0756f290a2b4dc4b",
  "RECOVERY_R12_RUST_REVIEW_20260908.md": "e8fafe162d914b4726b5ddab87ed1a4cb6d3542156eb6000756ff47a9997e625"
}
```

```json
[
  {
    "record": {
      "change_class": "reference-fix",
      "id": "exp-v1-recovery-r12-python-generation-0717",
      "lane": "python",
      "parent_candidate_sha256": "4432a25372e0cd1ef3da2401dbab9b82886ecdeb5d0a791dbf22d3fb4768e3e4",
      "parent_hold": {
        "evidence": "measurement/data/expansion-v1/cutoff-5885-review/work-message-mapping-proxy-result.json",
        "id": "exp-v1-python-generation-0717",
        "reason": "Valid standard MappingProxyType fields fail constructor deepcopy despite mapping contract."
      },
      "parent_id": "exp-v1-python-generation-0717",
      "parent_rights": {
        "answer": true,
        "model_training": true,
        "prompt": true,
        "redistribution": true,
        "tests": true
      },
      "parent_source": {
        "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
        "license": "CC-BY-SA-4.0",
        "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
        "record_id": "row-04048",
        "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
        "source_record_sha256": "b8192424da7167dcfab7af8b53b2274881ef6bc31f775bd4c07e409ddb958cca",
        "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests",
        "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
      },
      "rationale": "**Change class:** reference-fix.\n\n**Minimal coherent correction:** Normalize validated outer fields Mapping into a detached standard container before deep-copying; preserve read-only properties, complete field validation and consistency checks.\n\n**Decisive test requirements:** MappingProxy reply fields followed by backing-map mutation must remain unchanged; MappingProxy job with mutable tags, UserDict controls, repeated property isolation and malformed fields exercise the repair.\n\n**Contract decisions / limits:** Do not require a concrete copied Mapping class or arbitrary hostile/noncopyable descendants. Invalid-kind ValueError versus malformed field TypeError remains the stated distinction; no private-field layout test.",
      "review_evidence": "measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_PYTHON_RUST_20_20260908.md",
      "review_evidence_sha256": "bfd5af2666f35a2d67bb6babba881b76149794de7ede6ba714e0720c57a18181",
      "status": "planned-not-generated-not-admitted",
      "task_type": "generation"
    },
    "prior_file_hash": "54f9409debe5782b15c9459a8843e65501394d7c3daa4b4d9ca2c8be92df3779",
    "prior_canonical": "068140f7cd0ffbab9afd76b9a283b20d223e306e83d784e9332c0114bda33114",
    "prompt_hash": "49701ab781d8b5d856d109aab003eefd3548095d2471b20e8975195434763be5",
    "reference_hash": "ae154eeae0a17d6ac414a40f5e111d3c4846d50df8e6cc0a53164c8d31f38a91",
    "test_hash": "cbb2eee7037015dda9b7cd4e5d4603bfab5f281b749d3e00b5ed4d7b61193033",
    "mutant_hash": "f91b9e8db5d9bed1193c2a386981e530ceb046e60c3da4635e5d6048f065b07b",
    "original_hold_evidence_hash": "948083cbc072008d4c6cfd23cd2ea910e38c0fe5a39818603c737d9b4c6f1a1a"
  },
  {
    "record": {
      "change_class": "oracle-rebuild",
      "id": "exp-v1-recovery-r12-rust-generation-0487",
      "lane": "rust",
      "parent_candidate_sha256": "9ee8d243d8728a71c43c64ab9122fceb8e0db37aabc8e8e1f055ff82fb726ad4",
      "parent_hold": {
        "evidence": "measurement/data/expansion-v1/cutoff-5885-review/RUST_STRATUM_REVIEW_29.md",
        "evidence_kind": "static-contract-test-comparison",
        "id": "exp-v1-rust-generation-0487",
        "reason": "Original tests require query arity rejection though prompt only constrains observation arity and specifies fallback for no exact feature match."
      },
      "parent_id": "exp-v1-rust-generation-0487",
      "parent_rights": {
        "answer": true,
        "model_training": true,
        "prompt": true,
        "redistribution": true,
        "tests": true
      },
      "parent_source": {
        "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
        "license": "CC-BY-SA-4.0",
        "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
        "record_id": "row-05991",
        "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
        "source_record_sha256": "ff9d9a8308576f019c50bec2336ce85b8a7d1ca4ecacc6a08345cf7037ae633a",
        "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; independent tests strengthened after rejection",
        "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
      },
      "rationale": "**Change class:** oracle-rebuild.\n\n**Minimal coherent correction:** Permit nonempty queries of different arity to fall back to model mean; retain equal observation arity and atomic updates. Rebuild original query-arity rejection assertions.\n\n**Decisive test requirements:** Model outcomes 10 and 20 with two features; query [9] has no exact match and returns15. Mixed-arity nonempty query batch preserves order; empty query still errors and empty queries still require known model.\n\n**Contract decisions / limits:** Freeze constructor locations explicitly (existing ObservationStore::new and free new wrapper) and only required public traits. i128 summation remains as specified; no float mean or new query arity constraint.",
      "review_evidence": "measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_PYTHON_RUST_20_20260908.md",
      "review_evidence_sha256": "bfd5af2666f35a2d67bb6babba881b76149794de7ede6ba714e0720c57a18181",
      "status": "planned-not-generated-not-admitted",
      "task_type": "generation"
    },
    "prior_file_hash": "f97043d0db6566226dbbd6aac88aa04c681d114d1af0b6d84af59606d71aa93d",
    "prior_canonical": "8bd4fdde9168e90a56a025f0d7b3117ebfc0e872a1e30905361efc2b40ee264c",
    "prompt_hash": "07bf29038eeb2e6fc3a38360146a787863a01e38a00a3a19be9a858638df0155",
    "reference_hash": "f82da9e0e607a31880dd1c533e4c9d92c87aa2b870cc10b3e7a41e69565eb550",
    "test_hash": "ee3da12e6ee7c93abe4321ec159028d39b19fb05057f92cc69a08d6c1ea582fa",
    "mutant_hash": "a1ad0530f1198a0a72dae70887c635ad81b06d97fef700161a1bcd9c28c580af",
    "original_hold_evidence_hash": "05a4bac120af9b07505a3e628a582021e9a2503520eb4d79d11f4f99c9e22831"
  }
]
```

