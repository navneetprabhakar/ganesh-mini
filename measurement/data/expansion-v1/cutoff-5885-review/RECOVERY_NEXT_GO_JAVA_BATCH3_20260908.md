# Next Go/Java recovery selection — batch 3 — 2026-09-08

## Disposition and scope

Gate 2; selection only. Recommend **18 fresh held original parents: 7 Go generation, 7 Java generation, 4 Java repair**. Target was up to 30, ideally 15 per lane; shortfall is **12 (8 Go, 4 Java)**. This is a bounded shortlist, not a claim that every remaining held parent is unsuitable.

Complete original prompt/reference/test reads were performed for 30 parents (12 Go, 18 Java), together with source/rights fields and exact per-ID hold evidence. No candidate was executed, generated, admitted or changed. No plan/request/version was reserved, no GCloud action occurred, and no original-review coverage credit is added. Existing historical execution claims below are quoted ledger provenance, not new runs.

All 23 reserved plans r1–r23 were checked: **153 unique original parent IDs**, zero overlap with the 18 proposals. Historical explicit deferrals from RECOVERY_NEXT_GO_JAVA_20_20260908.md and RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md were respected. Main must revalidate reservations and live ledger hashes before approving any future request.

Corpus: `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`, SHA-256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Hold ledger: `measurement/data/expansion-v1/cutoff-5885-review/additional-holds.json`, SHA-256 `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.
Canonical hashes use UTF-8 JSON with sorted keys, compact separators and ensure_ascii=false. Prompt/reference/test hashes are UTF-8 field-content hashes; evidence/plan hashes are raw file hashes. Original source_record_sha256 binds the approved drafting stimulus. Rights values are recorded provenance, not a new independent license ruling or release admission.

## Seven-criterion selection assessment

The individual scopes below assess complete targets, not patch size. Each selected target has a clear behavioral obligation and declared API sufficient for its distinguishing witness; coupled state, validation, numeric, ownership, framing or grammar behavior supplies substantive work beyond elementary padding. Standard-library-only recovery is appropriate. Retain declared public types/traits and use ordinary accepted inputs, not hostile object behavior, reflection or private-layout checks.

Independent tests must be authored from the unchanged behavioral specification and approved scope, not reference implementation text. Original independent-test origin does not validate every original oracle: exclusions below must be respected. The proposed known-bad is one realistic current defect, not an uncompilable stub or deliberately unrelated failure. These are selection-level conclusions; only full emitted-artifact review plus sandbox directionality/provenance checks can support later admission.

The 14 generation parents propose reference-fix with **byte-preserved problem text** and a realistic defect mutant. The four repairs propose **oracle-rebuild**, explicitly allowing embedded complete known-bad replacement and neutral diagnosis edits only, while retaining behavioral prose, corrected objectives and APIs. Do not apply a reference-fix problem byte guard to those source replacements, and do not use this permission to add algorithm mandates or behavioral paragraphs. No broad contract clarification is being silently adopted.

## Ordered proposals

| Order | Parent | Class | Behavioral focus |
| --- | --- | --- | --- |
| 1 | exp-v1-go-generation-0102 | reference-fix | Go AccountStore token spelling |
| 2 | exp-v1-go-generation-0160 | reference-fix | Go PassService token spelling |
| 3 | exp-v1-go-generation-0276 | reference-fix | Go session credentials token spelling |
| 4 | exp-v1-go-generation-0327 | reference-fix | Go concurrent Ledger finite mean |
| 5 | exp-v1-go-generation-0382 | reference-fix | Go MintSession/VerifySession token spelling |
| 6 | exp-v1-go-generation-0542 | reference-fix | Go Resource nil-kind acceptance |
| 7 | exp-v1-go-generation-0791 | reference-fix | Go DeviceConfig exact JSON keys |
| 8 | exp-v1-java-generation-0123 | reference-fix | Java InvitationRegistry pair collision |
| 9 | exp-v1-java-generation-0140 | reference-fix | Java NumberBook finite decimal average |
| 10 | exp-v1-java-generation-0196 | reference-fix | Java buffered sink integer overflow |
| 11 | exp-v1-java-generation-0427 | reference-fix | Java inventory global uniqueness |
| 12 | exp-v1-java-generation-0512 | reference-fix | Java text pipeline unbounded take count |
| 13 | exp-v1-java-generation-0513 | reference-fix | Java GZIP frame premature allocation |
| 14 | exp-v1-java-generation-0643 | reference-fix | Java Snapshot norm and mean |
| 15 | exp-v1-java-repair-0326 | oracle-rebuild | Java repair tree valid immutable children |
| 16 | exp-v1-java-repair-0328 | oracle-rebuild | Java repair dispatcher immutable handler list |
| 17 | exp-v1-java-repair-0359 | oracle-rebuild | Java repair supplementary identifier usage |
| 18 | exp-v1-java-repair-0409 | oracle-rebuild | Java repair allowed-key Set contract |

### 1. exp-v1-go-generation-0102 — Go AccountStore token spelling

**Proposed class:** reference-fix. Original remains held.

The complete target combines normalized account creation, deterministic IDs, password digests, authentication, verification and sorted queries. The reference permits CR/LF in the raw-base64url signature. Register a valid account, authenticate, confirm the canonical token succeeds, then require appended newline/CR and an embedded signature newline to fail without changing store state. Enforce the specified raw URL-safe unpadded representation in both segments without redesigning token layout: its MAC covers the encoded payload segment. Retain secret copying, failed-registration ID behavior, normalization and ordinary tamper/unknown-account controls. Do not inherit tests demanding nil constructor output on error, private counter access, or unpromised capacity behavior; assert the promised error. No prompt change or new domain restriction.

Exact immutable bindings:

- Parent canonical SHA-256: `4377988fa835ef619986b4d073426242af17e62bd9b98746682359517ddc27b7`
- Prompt SHA-256: `d3038d4c26b833ab95c0bb140b49c248462019dd6f28203397ce43d1078204e4`
- Reference SHA-256: `44031e579da404885b1691eea8730b9b05538f72bcc4e63bf85f3e24b497d97c`
- Original file `go.mod`: `96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905`
- Original file `solution_test.go`: `d43ec6f12f16da4a51194d7650df3a3225f8ee14c1e0df777f4a5b6e9fa005c4`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-28029",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "9b17377e4e10c0b37fbeaae4388c126879259d3f189c23b70f09d0b69e7fc863",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Executed altered token acceptance: appended newline is ignored.
- Canonical hold-object SHA-256: `b677e5669867db05c951558aff2397fed34e7ac5f53b5266013ecfe6f1f7f70d`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_9.md`
- Evidence file SHA-256: `8a660a9738cfca73baf7c7509f94ec0b8c42cd5d5c6403d3b6293d239d845aaa`

### 2. exp-v1-go-generation-0160 — Go PassService token spelling

**Proposed class:** reference-fix. Original remains held.

Claims, HMAC, expiry and validation interact nontrivially. Issue valid claims with expiry 20; the canonical token verifies at 0 but token plus newline/CR must fail. Include padding, extra segment, tampering and temporal boundary controls. Enforce raw-base64url segment spelling while preserving HMAC over the encoded payload, constant-time comparison, claims validation, unknown-field and EOF handling. Do not mandate zero claims/empty token/nil service secondary outputs on errors unless the frozen specification explicitly requires them. No JSON serialization canonicalization policy beyond the existing contract.

Exact immutable bindings:

- Parent canonical SHA-256: `e71c6bf13e826999d47ca6b1c7e113ddebc97924f45ae0496d629c35c8f6605a`
- Prompt SHA-256: `f5e850694c91a9ed83a5eab94954024ec88d93c30858af2ea27e97fa4462e2a7`
- Reference SHA-256: `5a1b6ddab0bcce7230dfef8e34f6184669945515734def9a0b3e626f02d41550`
- Original file `go.mod`: `96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905`
- Original file `solution_test.go`: `c22e357e59bd822ade2c67f3c2afe39cd8b65afe712a671f0a8dcd09f9b75c0d`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-16261",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "9d171379ff74b9d76867c37990a38abb93b0617a0feb31d5c3dd2eb9ee0b3063",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Executed acceptance of newline outside specified base64url token representation.
- Canonical hold-object SHA-256: `dfe4e038299d8a9153eebdd3e7203145b443709b0679d27a003124d7df312653`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_13.md`
- Evidence file SHA-256: `d3583742ab9cb63f101f2aad34bedf5edac212872130f77328fbfb0048b982ed`

### 3. exp-v1-go-generation-0276 — Go session credentials token spelling

**Proposed class:** reference-fix. Original remains held.

The complete target signs structured claims, checks issuance and checked 86400-second expiry arithmetic, and copies the key. A token generated at 10 must verify at 10; appending CR/LF must fail. Keep future-issued, expiry equality, padding, tampering and issuance-overflow controls. Preserve HMAC over the encoded payload segment, not decoded JSON, and the stated time window. Fix only encoded-segment acceptance; do not add JSON-key, error-secondary-output or resource policies.

Exact immutable bindings:

- Parent canonical SHA-256: `1b101834ee8390d3b845e09023ce6ee3c1b6a439f146b889b5fb2c5025d00fda`
- Prompt SHA-256: `84f806be6720e7e6a4acd309cd6991ec881a86f5daf3e187ff959c301ae02172`
- Reference SHA-256: `d673ab0804e539f327f374ae192254b22df82c0501a5c4c9287f7316032aeee1`
- Original file `go.mod`: `96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905`
- Original file `solution_test.go`: `8bc409363b1be30efec15f5552f8b59a796fd2ec060933f1aaf206cbc50462d4`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-27535",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "daf674758d1e7848b9b061d9546069822129f55e249518fc7655b13dbbd43913",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Criterion-positive signed claims and temporal boundaries; executed behavioral hold: appended newline accepted outside specified base64url format.
- Canonical hold-object SHA-256: `d39f48f417c929ede0fd4e2a9817697672da7584ddf376b8c5dcb82dc24c282d`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_22.md`
- Evidence file SHA-256: `25bf51489804d0121f218c29c990be0119fa7d5961012fd54072c15ec7434cb1`

### 4. exp-v1-go-generation-0327 — Go concurrent Ledger finite mean

**Proposed class:** reference-fix. Original remains held.

History ownership, ordered ticks, validation, concurrency and aggregations make the whole target substantive. Append two Double/Go MaxFloat64-equivalent observations at successive valid ticks: Mean must return that same finite value and true, not infinity. Include two negative maxima, cancelling opposite maxima, ordinary values and rejected-invalid-append state preservation. Correct arithmetic so intermediate accumulation does not overflow a representable mean; preserve missing-key behavior, sorted/independent history and min/max. Use exact expectations for the decisive equal-input witness and sensible tolerance for general fractions, not an invented bit-exact summation algorithm. No new allocation or nil-receiver policy.

Exact immutable bindings:

- Parent canonical SHA-256: `9243974513083f41dc16e1ba30f135bd76a34c1f3bec416aaa358d3e2c488aab`
- Prompt SHA-256: `8f3fdc51e6cca5ac33f0911819ed4392687ad4e80e28552f66dff0fae7d470a1`
- Reference SHA-256: `9326449e3ea77c8a28ba3d4cf99c9abec609c79c2b3203fd9eb4dcebdc28baa4`
- Original file `go.mod`: `96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905`
- Original file `solution_test.go`: `c2b8c9fefe35a03dccf4a579b718957d193c13bede863691cf3973b62942b669`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-15986",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "626c2a9e229c3a197b21bf952ac1749f324048265bb042133ca74eb885c32b75",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Criterion-positive concurrent ledger; executed behavioral hold: mean of identical finite observations overflows to infinity.
- Canonical hold-object SHA-256: `5e27e995c93f6a9c2dcc08e8f83d9e14ef80eb0a983b31a9e7accf2537e44e22`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_26.md`
- Evidence file SHA-256: `0635874594f827dc82736b76ab44bd29ec7c102f5e0224fb899a831185df1b48`

### 5. exp-v1-go-generation-0382 — Go MintSession/VerifySession token spelling

**Proposed class:** reference-fix. Original remains held.

The authentication task combines canonical JSON, MAC and temporal checks. Canonical token succeeds; appended/embedded signature CR/LF and noncanonical payload spelling must fail. Unlike the preceding token tasks, this contract MACs raw JSON bytes: preserve that fact, canonical JSON checking and constant-time comparison. Preserve acceptance when now precedes issued time if expiry is still valid; do not import the other token tasks' now >= issued restriction. Malformed segments, padding, bad claims and expiry controls must accompany the defect witness.

Exact immutable bindings:

- Parent canonical SHA-256: `fa94df20b2555700b767d35154cfff4b52c4f888374d96cc9c5e893e0767b99b`
- Prompt SHA-256: `7fe8a3247abfd0aa2fb3f4d5b12e6c4505653cd0364b819a98ad1b5eb3c12754`
- Reference SHA-256: `c3721cfcbe75daaf3af5650daec9954e0dbed54f5314fd246ce02e5801bed933`
- Original file `go.mod`: `96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905`
- Original file `solution_test.go`: `dc4cd14466fff7b270bbff4cc757763d5597cea3a8c836fc7b1b8bc2715831f2`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-16139",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "f2871dbb809c89434ed469db95e0d5a42ea7588c4a3d2c5066ef36194b1cb772",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Criterion-positive authentication task; static behavioral hold: raw-base64 signature decoding accepts appended CR/LF without canonical encoding check. Canonical JSON comparison does not validate encoded signature spelling.
- Canonical hold-object SHA-256: `3b4a3d0d4b414474690e49d7a3b58072c85eb7c214e2608ade67c3cee0287efe`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_30.md`
- Evidence file SHA-256: `eb274356879e5fde32267e6aab0639bb3c662695d945172ce684ed085bd51ed7`

### 6. exp-v1-go-generation-0542 — Go Resource nil-kind acceptance

**Proposed class:** reference-fix. Original remains held.

Polymorphic aggregation must support custom Resource implementations, ordered calls and input preservation. Only nil interfaces and typed nil pointers are excluded. A named nil map implementing Metrics and returning (2,3) is a nonnil interface value and must yield UsageSummary{2,3,1}, nil. Optional ordinary named nil slice/function/channel implementations exercise the same distinction; a typed nil pointer remains rejected. Narrow the reflection nil check rather than banning valid implementations. Preserve per-resource finite/nonnegative validation, zero-summary/error-index behavior and ordering. Do not add panic shielding or an aggregate-overflow error policy: the prompt defines invalid individual metrics, not a global finite-total guarantee.

Exact immutable bindings:

- Parent canonical SHA-256: `c183cc2df0bccc34a4ba71a6c9f144b92756fbc8862032111f47886ae3058a66`
- Prompt SHA-256: `001dc417ffe707a206143bca902760995c989a5e81e353fcb6b2ed860096632e`
- Reference SHA-256: `b6c9ddb8b4207e26e28a60f9cc289895685497a4e0ba17dada4626c4e80dbf2a`
- Original file `go.mod`: `96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905`
- Original file `solution_test.go`: `3f5dd716af41acac212de74b7a8a97fc8d8318f2d19dbbb49baf30c4a5395a1a`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-27722",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "711b143e103d3a12419ee699cb176532ba9c6608e27ad951a552ed30038cac64",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Criterion-positive polymorphic aggregation; static behavioral hold: rejects nil map/slice/function/channel resource values even though only nil interfaces and typed nil pointers are forbidden.
- Canonical hold-object SHA-256: `b629cfaa66c352a69c1f344a4e9b22b88a1987a7d301c279cb6dbb254c4eafb4`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_42.md`
- Evidence file SHA-256: `62a0c20c885211d942f51b4dc91128dcd3151b798e148c591274af0c398010c9`

### 7. exp-v1-go-generation-0791 — Go DeviceConfig exact JSON keys

**Proposed class:** reference-fix. Original remains held.

The target combines strict typed custom JSON, hidden token state and generic object decoding. Canonical lowercase label/level succeeds; {"Label":"x","level":1} and {"label":"x","Level":1} must fail. Validate exact decoded key names rather than relying on encoding/json's case-insensitive struct matching. Preserve missing/duplicate/wrong-type/unknown rejection and token exclusion. Escaped JSON spelling that decodes to label is the same key, not grounds for a new raw-lexeme rejection. Keep generic DecodeJSONObject's duplicate-last and UseNumber behavior separate. Inspect emitted keys, not an unsupported blanket ban on the substring token inside legitimate label values.

Exact immutable bindings:

- Parent canonical SHA-256: `baedc50e12510a76ed553b3cdfdf92189a02b67c1ea41f534813cafd1be75675`
- Prompt SHA-256: `a0f50420a08bd018cd47099551381fa974c9b0d1d191b2349eb29ae87d0d6e96`
- Reference SHA-256: `f047728069a0556a60c55e0ae707665190fea58485dfd7f1f8ea3983460c1ee0`
- Original file `go.mod`: `96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905`
- Original file `solution_test.go`: `afe258f0b64dfc19c47fb7fdbe444b301f8713b49d414077abab248eaf450532`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-16256",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "89fd81ac61ddad0ff958d721cf65b66f8c97a60bc4c6cf75b7f23d5c869202fa",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Reference accepts differently cased JSON keys despite exact-key contract.
- Canonical hold-object SHA-256: `f63bbb4ae335f91a4778f49237b338e607317a5f4911361e1c6e7b22a6e37a5d`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/device-exact-keys-result.json`
- Evidence file SHA-256: `7ae9cb1ab14321dbe5a9606cacb4e04dc7cbdcb289c801f9764a363a7fbf64e4`

### 8. exp-v1-java-generation-0123 — Java InvitationRegistry pair collision

**Proposed class:** reference-fix. Original remains held.

Directed invitations, symmetric connections, normalization and immutable sorted views form the complete target. Accept the pair (a, b+NUL+c); connected(a+NUL+b, c) must remain false and that unrelated pair must still be independently invitable/acceptable. Both original and second pair should work symmetrically, then clear independently. Replace delimiter-concatenated identity with a collision-free structural unordered pair. Interior NUL is valid here; do not ban it or change trimming/Locale.ROOT semantics. Do not introduce a new null-decision oracle.

Exact immutable bindings:

- Parent canonical SHA-256: `8f23c06357bc9e5422f9849fcd12ee7764b3c71ddb90654d2fa9bf2fdbc11b2f`
- Prompt SHA-256: `549b56d62328e9d6c9022a26e8c16aae073dda4223153c89ecb4f5e57cefa0d0`
- Reference SHA-256: `dcdf4bee21158dbbf0c6920245120b2fad35d062e691b72cfe9893178d2d7506`
- Original file `SolutionTest.java`: `ea7f302a0219df0da5e98104cef7f799cdf7cc50ca3ab0af0a5914e73248d20a`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-28109",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "3ab75cb53bbb3e5afc119f686f8c49d549bff31db6fc204ae266f6eb7f71fb8e",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Executed behavioral hold: accepting (a,b+NUL+c) makes unrelated (a+NUL+b,c) appear connected because the canonical pair delimiter encoding collides. Interior NUL is not prohibited or removed by trimming.
- Canonical hold-object SHA-256: `82da136e6882102a216056760b86520ee861d742ff42d6943ac66a233c19cffd`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_12.md`
- Evidence file SHA-256: `3f43451a28cf719cb36bc0517678ebc3cf9546f377a36420ea281f6cc06639b9`

### 9. exp-v1-java-generation-0140 — Java NumberBook finite decimal average

**Proposed class:** reference-fix. Original remains held.

Staged integer replacement, exact integer overflow and decimal statistics are separate interacting obligations. Two Double.MAX_VALUE decimals must average to Double.MAX_VALUE, not infinity; include negative maxima, cancellation and ordinary decimal controls. Use overflow-safe average arithmetic while retaining finite-input checks and empty NaN. Preserve the explicit integer overflow contract; do not add a new cancellation/intermediate-overflow policy. Do not inspect private backing capacity to test the specified initial capacity, or require a particular arithmetic implementation/bit result for arbitrary fractions.

Exact immutable bindings:

- Parent canonical SHA-256: `2031b142e7dae804a91e64da72e41708cb558ab54b6022e1422d5ff1a399b12e`
- Prompt SHA-256: `9bcb65cf81587e561816324658f18ceafe396b240086db5b5cd5b5c2cd9a9730`
- Reference SHA-256: `69f7e92c58252187573882aad397d2ea22816b35804687884adeaa9a6402d30c`
- Original file `SolutionTest.java`: `c2277bdb659c5db63a2918ab1b83961e2070fe8d0b988c9ed8a38d9841953c3d`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-12965",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "326d583509768c707a9a176d8c26ffb577e3f7b29946fb864d7f969851ba7162",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Criterion-positive staged replacement and exact integer accumulation; static hold: two Double.MAX_VALUE decimals overflow the sum so decimalAverage returns infinity instead of the representable Double.MAX_VALUE average. Integer overflow policy is explicit and not newly held.
- Canonical hold-object SHA-256: `f9a0fdff9b1e7c9415c1b0a96009bb945dbf637bd9c4a1b869a49b89278f19ba`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_14.md`
- Evidence file SHA-256: `0be82513eff60ea85795fcf79a04527be1634fcca99a374cc2f0dbeb13a0bdbb`

### 10. exp-v1-java-generation-0196 — Java buffered sink integer overflow

**Proposed class:** reference-fix. Original remains held.

Configuration, prevalidated ordered batches, buffering, threshold commit, snapshots and close transitions are substantive. Fix both capacity+1 threshold overflow and bufferedWeight overflow. With capacity Integer.MAX_VALUE, adding weight 1 must not commit; adding a valid maximum-weight command then commits both. Independently, capacity MAX_VALUE-1 has threshold 1073741823: first weight 1073741822 stays buffered; then weight MAX_VALUE-1 must commit the two commands despite the sum exceeding int. Use wider/intermediate-safe arithmetic without changing accepted capacities or weights. Keep batch atomic validation, copying, flush/close behavior and declared worker configuration; do not invent worker scheduling/concurrency semantics.

Exact immutable bindings:

- Parent canonical SHA-256: `cf7d82bbc4fc796c951fab429f522607eb8e0847c3a293b636c16d2c4d37b216`
- Prompt SHA-256: `82a9037d40938d0d2020278439656a0daff4a0e2d4f00f07ce4df3b1653263ee`
- Reference SHA-256: `9b99f3f70d8e1c9272c93a882dcb8f04be9d05a6da15c4b689980d87fe6963dc`
- Original file `SolutionTest.java`: `102819fb996e287715d062a546880021543d4711076110cd6761451da48b901e`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-12803",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "46f6521d6e29115c03648c59b7a4cd3bfc7b20e460e558fdee4992f668289f63",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Executed behavioral hold: capacity Integer.MAX_VALUE overflows capacity+1; adding weight 1 commits immediately despite mathematical threshold 1073741824. Static secondary defect: bufferedWeight can overflow when a large valid command follows a partial buffer.
- Canonical hold-object SHA-256: `9911332a7b756b865167653440fd63b1037d3a52da857c8cc3efe8d15398eeaf`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_19.md`
- Evidence file SHA-256: `f64077ec47ec18fd153960fe3718575b7888e77c887cdcb5a21385e06f704be1`

### 11. exp-v1-java-generation-0427 — Java inventory global uniqueness

**Proposed class:** reference-fix. Original remains held.

The ledger supports multiple ordered immutable transformations and aggregates with global unique-ID validation. A two-entry input with repeated ID is invalid for every operation, including a missing lookup, an early matching lookup, and adding a distinct new ID. Validate the entire existing list before an operation can return. Preserve field validation, ordering, nonmutation and long-valued sums. Also honor explicitly independent returned outer lists, including empty results, rather than relying on List.copyOf identity reuse. Tests should compare public Entry fields, not require element reference identity. The prompt only calls invalid input invalid: do not strengthen it to an unpromised exception subclass.

Exact immutable bindings:

- Parent canonical SHA-256: `0667dd7c4bd4913f0886ed1c031961871b89687065479ad125756b731a35ac7b`
- Prompt SHA-256: `8fef9391ee8bfcd656393f7e81d377efe497b2cf258d50172c74fa3c88d042a6`
- Reference SHA-256: `9e4f416431e58a6ed9c48c3f05e4cfacd1acc8f49697e8d5408102b4df635a08`
- Original file `SolutionTest.java`: `48286a6cbee455cb16028bf3092adb7b0b26457a203e24e328b5995c2c197bdc`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-12804",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "3d997a96d05c39524df81378a068c7e16a4519c8b1a3771d7e48edecb58f7e9f",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Static hold: existing lists with duplicate IDs are accepted by check and propagated by operations despite the unique-ID requirement. Add only compares the new ID against existing ones.
- Canonical hold-object SHA-256: `9e1358804eecadb1819103f473faf7557c156fe0f36904286c8b05919e4e0790`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_40.md`
- Evidence file SHA-256: `44c4c2d8dc6b61f800b3e1090978687f5bcb3b9b4b1b7bd11228405d998e4e89`

### 12. exp-v1-java-generation-0512 — Java text pipeline unbounded take count

**Proposed class:** reference-fix. Original remains held.

Ordered text transformations, ASCII-decimal grammar and UTF-16 truncation interact. take:2147483648 applied to abc must return abc; a 100-digit positive count likewise retains it; arbitrarily many leading zeros followed by 2 returns ab. Validate all characters even after the numeric value exceeds the current string length, so a huge count followed by x remains invalid. Remove the original unsupported int-upper-bound rejection oracle. Avoid int parsing overflow by bounded comparison/saturation or arbitrary precision while preserving the specified grammar, operation order and UTF-16 take semantics. No new whitespace, casing or reversal policy.

Exact immutable bindings:

- Parent canonical SHA-256: `a9a891a7be5be58373edc5504c9370876dc45f8c23718a4b80053e710af1d022`
- Prompt SHA-256: `e52b65227e5d388c1253a11030269c7259beb3445f69fd7e8b5a353dfc19d22f`
- Reference SHA-256: `ce7e7a0df9d425b6fe9c0df5e8d061408ed55a1770a15221814680a70ae16faa`
- Original file `SolutionTest.java`: `5570a24434f56ec428ee865db939bf2c2985e7474ae1e86a8c162f569a46e21d`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-12928",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "208ca8497caf09307cc4ccf69d3c3d1eb14e8f9deff2945ae482102d871f47e7",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Static hold: take:2147483648 is a valid nonnegative decimal count larger than any current string but parseInt rejects it instead of retaining the string. Prompt supplies no int upper bound.
- Canonical hold-object SHA-256: `5f766a169f871e22e47bb1700015ecb420b227152e1e4fd6126bb14994f6f22e`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_48.md`
- Evidence file SHA-256: `1f7dae9d24d80c688f272b0d01fb6e399d3d9abe597a4b559ac8d2cc39771e1a`

### 13. exp-v1-java-generation-0513 — Java GZIP frame premature allocation

**Proposed class:** reference-fix. Original remains held.

Typed codec calls, exact binary framing, compression, malformed-input validation and ordered mutable output are substantive. Independently construct tiny GZIP frames whose decompressed bytes contain only count=MAX_VALUE, or count=1 and length=MAX_VALUE with no item bytes. They are truncated and require IllegalArgumentException before enormous preallocation. Decode incrementally/validate available input rather than allocating solely from hostile counts or lengths. Do not impose a fixed valid-message size cap, new strict UTF-8 policy, canonical gzip bytes or Error-catching codec contract. Preserve mutable ArrayList output, trailing-decompressed-byte rejection and codec RuntimeException handling. These witnesses are bounded malformed inputs, not demands to allocate huge valid payloads; original behavior may be resource failure and must be classified honestly by the later sandbox.

Exact immutable bindings:

- Parent canonical SHA-256: `79d21d7bc51051e5e40ecd5c20263a634bbc4752a9ea2d96600b29d4858696b6`
- Prompt SHA-256: `317203991ca46103bdef0505ca0f5e47b7bc1665ae1b90d082af75c60b8cba08`
- Reference SHA-256: `9a6e575ab6593e02fe4dd34910ab55edbd828bf77ba2ac298458f1614ae510ce`
- Original file `SolutionTest.java`: `530c082b2194d9d67d2385a560c972fd1357e671f34e83811f574d167ca434a6`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-28224",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "d1efe09a382e868d0b7be2f5fe00892e06eebff6b25f75c9cdbb40836a4daaf7",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Static hold: truncated GZIP frame declaring count MAX_VALUE triggers eager ArrayList allocation before truncation validation, yielding resource failure rather than required IllegalArgumentException. Untrusted item length is likewise allocated before reading; not executed.
- Canonical hold-object SHA-256: `7b24f55c7cd2e8eeb3db4141559cf1c515c1cc4cf1092498bbf4d07bd7c9bc61`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_48.md`
- Evidence file SHA-256: `1f7dae9d24d80c688f272b0d01fb6e399d3d9abe597a4b559ac8d2cc39771e1a`

### 14. exp-v1-java-generation-0643 — Java Snapshot norm and mean

**Proposed class:** reference-fix. Original remains held.

Matrix validation/transpose/maximum, vector statistics/sort and defensive Snapshot ownership make the whole target nontrivial. With an empty square matrix and vector [1e200], norm and average are 1e200; [1e-200] must not lose its representable norm to re-squaring; [MAX_VALUE,MAX_VALUE] has average MAX_VALUE, with an unrepresentable norm permitted to be infinity. Retain stable hypot accumulation instead of squaring it again, and prevent mean intermediate overflow. Observe scalar results through the explicitly specified Snapshot.toString format if getter names are not declared; do not invent new API requirements. Preserve deep copies, sorting and null/nonfinite/matrix validation, and avoid arbitrary fraction bit-exactness or new overflow exceptions.

Exact immutable bindings:

- Parent canonical SHA-256: `841935ccc0374818e4da3a3700cd09caaecaf195925fedcc6bef5c958a0ea7cb`
- Prompt SHA-256: `9624dc748309a837244edf8badd5e8aae8607cb5210973d24a2355af4574cb5e`
- Reference SHA-256: `efe823bb6395a21e8617954a37ee315cdfad68a576b0f8029384fbf1e02e3f7c`
- Original file `SolutionTest.java`: `f085fb6f3620787a1e0cf5739d16097e87d0f72e93c30041e2746f68a74c41b0`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "license": "CC-BY-SA-4.0",
    "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    "record_id": "row-28147",
    "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
    "source_record_sha256": "495a24de967fe834fc6e78bd51db5d6fde9af5eaeb5e6381d2dbb524007b5523",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Static hold: squaring each hypot result reintroduces overflow; vector [1e200] produces infinite norm although 1e200 is representable. [Double.MAX_VALUE,Double.MAX_VALUE] also overflows the sum before averaging. Not executed.
- Canonical hold-object SHA-256: `fba8c07f9048abf61361c1a720dacb6e6e909916d060aa018c91eb701a89de7c`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_60.md`
- Evidence file SHA-256: `c0034c9d1c06b6b828b248c8e22cb4d694387c59e5f11d1f85a699d386e93766`

### 15. exp-v1-java-repair-0326 — Java repair tree valid immutable children

**Proposed class:** oracle-rebuild. Original remains held.

Replace unsafe children.contains(null) with element-wise validation/copying, preserving full preorder DFS and immutable Node behavior. Node(leaf,v,List.of()) must construct successfully; a root with List.of(left,right) must find a right-branch match, retain first-preorder duplicate behavior and resist mutation of the original child list. Explicit null elements still reject. The fresh complete known-bad should restore only the unsafe null query while retaining the originally corrected first-child traversal. Preserve original behavioral prose and API exactly; only replace embedded source and neutralize stale diagnosis about repeatedly visiting the first child. Do not require a particular recursion strategy or unbounded-depth guarantee.

Exact immutable bindings:

- Parent canonical SHA-256: `c1c90b1936ebc21d0f4209dfce3c51e6007cd57b48b59e037af6e89975e5b7ba`
- Prompt SHA-256: `425aeec6a790260ddab3f34a011560850f3a0a6aec54f8c28974382f72f2c6b9`
- Reference SHA-256: `eee4cbd587aadebacf8ab3a60f795bde9ae919b4736b6413bc622671d66640c4`
- Original file `SolutionTest.java`: `3b01a3a2aa5594315a0105128d174987a6f39e40fd55a2f07d696d97d96a0f2e`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "m-a-p/MdEval-Instruct",
    "license": "MIT",
    "license_uri": "https://opensource.org/license/mit/",
    "record_id": "row-03695",
    "revision": "38c9197e3add996fae624eb198ebd06155b2101e",
    "source_record_sha256": "c3c4b4ae0115585f67ea0af41f3d987c1222031b0dee3e3d76d63e7f6f8a400e",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/m-a-p/MdEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Static hold: children.contains(null) rejects valid null-free List.of child lists with NullPointerException on the pinned Java runtime; this candidate was not separately executed.
- Canonical hold-object SHA-256: `c4a3bf359556a05050c6f0bd39b83d917eeb45cb6f3a004d9321e82e3dce6ff0`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_46.md`
- Evidence file SHA-256: `2c2e902a67a71312d097dda179f6d8ffee9a34864cbe35c1b77e83ce208862c4`

### 16. exp-v1-java-repair-0328 — Java repair dispatcher immutable handler list

**Proposed class:** oracle-rebuild. Original remains held.

Replace handlers.contains(null) with element validation before dispatch; preserve ordered exactly-once calls, null result acceptance, immutable result list and immediate exception propagation. Map.of(action,List.of(h1,h2)) must call both handlers and collect results; empty List.of succeeds. Use a late-null mutable-list control to verify validation before any callback, and a throwing handler to show later handlers are not called. Unrelated invalid action entries need not be validated. Fresh known-bad restores only contains(null), not the old first-handler break. Preserve behavior/API prose; change embedded source and stale diagnosis only.

Exact immutable bindings:

- Parent canonical SHA-256: `1b21652c330e32d28a910161952f672e7d9309d4ea46fc084bddc5550e91f0f2`
- Prompt SHA-256: `a8e4e9944d90f0033611055e5f6520ecab2eb71787b32c507376e58490b49530`
- Reference SHA-256: `3baec0bbf32b0dcf9a742ec339aa483cabdfe97627d8e686218757c670af9876`
- Original file `SolutionTest.java`: `14a1614dd7874a56dedcd285c183744ca11cf0a20af53cdba6236109e7f7e55f`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "m-a-p/MdEval-Instruct",
    "license": "MIT",
    "license_uri": "https://opensource.org/license/mit/",
    "record_id": "row-13165",
    "revision": "38c9197e3add996fae624eb198ebd06155b2101e",
    "source_record_sha256": "4091f9074f3db24b03ab39edf486ef142040ff84695b8b0c292210e12f242e2f",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/m-a-p/MdEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Static hold: handlers.contains(null) rejects valid List.of handler lists with NullPointerException before dispatch; this candidate was not separately executed.
- Canonical hold-object SHA-256: `3029fcfc70afe9a1b52679bac80a973cb1d995d3c81c2932f976e8226b2ec4b7`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_46.md`
- Evidence file SHA-256: `2c2e902a67a71312d097dda179f6d8ffee9a34864cbe35c1b77e83ce208862c4`

### 17. exp-v1-java-repair-0359 — Java repair supplementary identifier usage

**Proposed class:** oracle-rebuild. Original remains held.

Use code-point identifier validation and codePointBefore/codePointAt boundary checks while retaining case-sensitive textual usage semantics. U+10400 is a Java identifier letter. For that query, lines [query+' = 1;', query+'x', '//'+query, '('+query+')'] must report [1,4]; a foo query adjoining the supplementary letter on either side is not a whole identifier match. Retain null/invalid-query handling, one-based output and immutable result. Fresh known-bad reintroduces UTF-16-char identifier/boundary handling while keeping the original case-sensitivity fix. Only embedded source/neutral diagnosis changes; no lexer, string-literal, extra comment grammar or keyword policy.

Exact immutable bindings:

- Parent canonical SHA-256: `5e1e5ac85bd3c5055185a1e9472b46e092dff0f9e1fa51d3d43a0a121b8462a1`
- Prompt SHA-256: `44df024a5279baa6cecd5128aa3b12d002e2e38a82f303ac6c6315709d7ee74a`
- Reference SHA-256: `024eebcc3084df2465659d5c447a549801133cd11e98102ecd1d0e9047f9feda`
- Original file `SolutionTest.java`: `28aa83882333c33272a6d297318454604eb2128a3997bdf0912d574c918386e2`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "m-a-p/MdEval-Instruct",
    "license": "MIT",
    "license_uri": "https://opensource.org/license/mit/",
    "record_id": "row-14852",
    "revision": "38c9197e3add996fae624eb198ebd06155b2101e",
    "source_record_sha256": "b8db51cca396d2c66a0afadaf2ff9b26f52d87a92c98ca0a10491529d232991a",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/m-a-p/MdEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Static hold: char-based identifier validation rejects valid supplementary Java identifier letters such as U+10400, and char-based boundary checks can split surrogate pairs.
- Canonical hold-object SHA-256: `820933063528f573ea9c79408879bdd581a1414e2cfe8b3a2d10053463cb73d8`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_51.md`
- Evidence file SHA-256: `2da5d0ebe515212a7572bd83521dc728940a84e741ed55b44cb2bbe7ed6ecd49`

### 18. exp-v1-java-repair-0409 — Java repair allowed-key Set contract

**Proposed class:** oracle-rebuild. Original remains held.

The prompt forbids null arguments, not null set members. Eliminate allowedKeys.contains(null), which rejects Set.of/TreeSet and introduces an extra member prohibition. decode('a=1;ignored=x;a=2',Set.of('a')) must return only a=2; TreeSet containing a is another ordinary accepted implementation, and HashSet containing null and a must also return a=2. Remove the original unsupported null-member rejection oracle. Preserve field trimming, exactly-one-equals grammar, empty-key rejection, ignored disallowed keys, duplicate-last stable LinkedHashMap order and null-argument rejection. Fresh known-bad restores the unsafe null-member check while retaining the old ignore-unknown correction. Preserve all behavioral prose, replacing only embedded source and neutral diagnosis.

Exact immutable bindings:

- Parent canonical SHA-256: `754568be928f85a57f3f4d1210d60813641b8f033a82496b186aeeda2f67cea9`
- Prompt SHA-256: `3385f4ce4b5c7c2baa9fdf8bfc6c86bf6a5a029e0f901c6053fb6c52148bad5b`
- Reference SHA-256: `4da9ce61966bb456148ee5e3f2215dfd063d848164ea5c7fe1bed376fe1a3182`
- Original file `SolutionTest.java`: `8d0abf3b7f36da9d0fe5a4cfcdb847c7da959ce0ca57d59301cff4f1358d0a1c`

Source and rights binding (verbatim fields):

```json
{
  "source": {
    "dataset": "m-a-p/MdEval-Instruct",
    "license": "MIT",
    "license_uri": "https://opensource.org/license/mit/",
    "record_id": "row-10592",
    "revision": "38c9197e3add996fae624eb198ebd06155b2101e",
    "source_record_sha256": "49f4325cee980e62ef7da7aaa7498ae3a45075ec8dc903493481e453926f9ee9",
    "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification",
    "uri": "https://huggingface.co/datasets/m-a-p/MdEval-Instruct"
  },
  "rights": {
    "answer": true,
    "model_training": true,
    "prompt": true,
    "redistribution": true,
    "tests": true
  }
}
```

Held evidence:

- Ledger reason: Static hold: allowedKeys.contains(null) can throw for valid null-free immutable sets; it also rejects null set elements although the prompt only prohibits null arguments. No new execution.
- Canonical hold-object SHA-256: `631e76fc1bb5c2a4da7aab80ff7f9ad2b9d0d76861551c41d0431325a3ae313f`
- Evidence: `measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_58.md`
- Evidence file SHA-256: `76cd604b18f0a5eadeff6ae80be40ba33b795fa74026d408057fc6a448cd2e3a`

## Full-read exclusions and shortfall

These are exclusions from this campaign, not new ledger mutations or universal irrecoverability claims.

| Parent | Reason not proposed |
| --- | --- |
| exp-v1-go-generation-0008 | Tuple-delimiter collision is real, but dot identity/global-versus-key and causal conflict/cycle semantics need additional decisions; a narrow collision fix would not establish coherence. |
| exp-v1-go-generation-0174 | Historical explicit deferral. Missing AccessEvent/AccessTrail field definition and case-colliding header behavior outweigh the narrow trim witness. |
| exp-v1-go-generation-0195 | Exact-key defect is substantive, but patch value trimming and null-versus-missing policy introduce additional unresolved choices. |
| exp-v1-go-generation-0270 | Historical explicit deferral. Mutable package-level map concern has no adequate public behavioral witness without private mutation. |
| exp-v1-go-generation-0422 | Historical explicit deferral. Cross-field NUL search issue is real, but unqualified Unicode case-insensitive matching remains a separate contract decision. |
| exp-v1-java-generation-0029 | Historical explicit deferral: null student entries are rejected without a corresponding prompt requirement; immutable-list fix alone is incomplete. |
| exp-v1-java-generation-0060 | Narrow stationary wide-box witness does not settle the broader unrestricted finite motion/output representability policy. |
| exp-v1-java-generation-0607 | Present-null asset issue is real but fixed routing/status projection risks elementary padding; not selected to fill quota. |
| exp-v1-java-generation-0630 | Equal-maximum annulus witness is real; direct formulas plus wrapper are a borderline elementary recovery target. |
| exp-v1-java-generation-0170 | Final page arithmetic has a potential tiny-output witness, but faithful full list validation remains allocation/work-scale; no unverified inconsistent virtual-list witness is certified. |
| exp-v1-java-generation-0313 | Eager allocation before null validation is real, but nonpositive-ID scope across message/author IDs needs a separate decision. |
| exp-v1-java-repair-0482 | Repository-only receiver issue is substantive, but token-boundary/whitespace scope and simple regex-wrapper target make a narrow recovery insufficiently settled. |

Full-read Go set: 0008, 0102, 0160, 0174, 0195, 0270, 0276, 0327, 0382, 0422, 0542, 0791 (all generation).
Full-read Java generation set: 0029, 0060, 0123, 0140, 0170, 0196, 0313, 0427, 0512, 0513, 0607, 0630, 0643.
Full-read Java repair set: 0326, 0328, 0359, 0409, 0482.
Totals: 30 complete reads = 18 proposals + 12 exclusions; zero new unique-original review coverage.

## Frozen reservation evidence

The following plan-file snapshot supplied the 153-parent exclusion union:

| Plan file | SHA-256 |
| --- | --- |
| measurement/data/expansion-v1/recovery-plans/r1/plan.json | `a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1` |
| measurement/data/expansion-v1/recovery-plans/r2/plan.json | `5dae7eac34ac462f6173dc6b740364d5c4b68129950359f453f4038111ad1d29` |
| measurement/data/expansion-v1/recovery-plans/r3/plan.json | `cbad9d14a504531e749b5eb3433f0bf4670e21f2a8e8d5f310d2e843e53c6231` |
| measurement/data/expansion-v1/recovery-plans/r4/plan.json | `8a6137773e65e1a55e5eaceed9a8c2e40153b5759a46a5189ba6a488d530d58c` |
| measurement/data/expansion-v1/recovery-plans/r5/plan.json | `778e0071bec56248081e741f4c742d522c75b4b006e069d8301b75440c2732ec` |
| measurement/data/expansion-v1/recovery-plans/r6/plan.json | `803f0308b33b4b8a834347d5976a148bc66001d6fc8606a1e206fb0e2b4a6795` |
| measurement/data/expansion-v1/recovery-plans/r7/plan.json | `f0a3b5d14eb983206ac83c99571c5522925feaf7ac0443ec3c59ad172d5f293e` |
| measurement/data/expansion-v1/recovery-plans/r8/plan.json | `1a579af9da9d542d6bb4f03c8fbc030fd0b9d3102a31c347cd631bfc18b873de` |
| measurement/data/expansion-v1/recovery-plans/r9/plan.json | `0f0d6e653bbabff308a912cc764d1373b20faf3f4cf68a4c7341c94f36b5ae79` |
| measurement/data/expansion-v1/recovery-plans/r10/plan.json | `728e70ee23ad46f8a4a8aec64a34d74b48c073a5382849fc52ce449154f2afb5` |
| measurement/data/expansion-v1/recovery-plans/r11/plan.json | `2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6` |
| measurement/data/expansion-v1/recovery-plans/r12/plan.json | `0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121` |
| measurement/data/expansion-v1/recovery-plans/r13/plan.json | `dead1489bb779934327bf3c8786d89c65b7604832829fa17129ea41ff1773217` |
| measurement/data/expansion-v1/recovery-plans/r14/plan.json | `2d59789fea811ba7ebe844564ee4dc66569fe4719067dea6d6a1524b049ea51f` |
| measurement/data/expansion-v1/recovery-plans/r15/plan.json | `d2e65ef33e2c70162a53315e3daec75ebe1e3fbc1a7098e8635eddacb348c100` |
| measurement/data/expansion-v1/recovery-plans/r16/plan.json | `efd902abc4ed3e00d6639c74f7d2ec95e6f153d1aa19a70a460aeb553dfb6844` |
| measurement/data/expansion-v1/recovery-plans/r17/plan.json | `60c02db8869c80c1515e2216205ac11a45b357206563f62f499d8b67b3ee02ee` |
| measurement/data/expansion-v1/recovery-plans/r18/plan.json | `512e3219da55465742728f2c5116840498e4a41c5a2bfe8f5b0130d9a19690a0` |
| measurement/data/expansion-v1/recovery-plans/r19/plan.json | `401d56a11f2ca2929eb42be7ffb36fe694cfded2500ed56a96759560b8b65f62` |
| measurement/data/expansion-v1/recovery-plans/r20/plan.json | `879eb4184b49e09a171cbe35592096a296d9d2af6e1e52eea68315fb6b7eb224` |
| measurement/data/expansion-v1/recovery-plans/r21/plan.json | `a5fe5bbb1cffe149091f626ed317a0e79c39985c10c883acd8f83df3c04582ca` |
| measurement/data/expansion-v1/recovery-plans/r22/plan.json | `34b141407c111f6df7999027d57540860ccb3b47c0d10c2c5ce8ba105f8facc0` |
| measurement/data/expansion-v1/recovery-plans/r23/plan.json | `d44918671d7a9350cc90e67ac7eede1ee4ab61e6ce6bae2f1eadaccbed367d92` |

## Approval boundary and next action

Main may accept a subset after reading these scopes and rechecking current reservations. This report creates no request and authorizes no generation itself. Future independent tests need canonical accepted controls and the precise behavioral witnesses above; removal of an invalid oracle is not permission to weaken unrelated requirements. Preserve full source/rights lineage and all original evidence. All parents remain held until a distinct approved derived version completes the frozen admission process.
