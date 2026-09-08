# R21 TypeScript quality review — 2026-09-08

Gate 2. Full candidate prompt/reference/tests/mutants reviewed for exactly 0072, 0086, 0097 and 0101, reconciled with the original full reads and approved R21 plan.

**Four derived test-quality holds; zero complete candidate positives. All four references are scoped-positive.** No candidate execution, admission, critic invocation, generation or central edits. Zero new original coverage.

## Individual decisions

| Candidate suffix (prefix exp-v1-recovery-r21-typescript-generation-) | Reference | Candidate decision and concrete reason |
| --- | --- | --- |
| 0072 | Scoped positive | Test hold: seed now explicitly copies id/name/email/active, while the mutant spreads seeded records. Every test fixture uses ordinary enumerable fields, so no test distinguishes the actual seed-copy defect. Require V1 and V2 seeds with valid non-enumerable id; verify listed ID and V2 update/remove by it. Also retain supplied hidden name/email/active values on add/update. Existing namespace isolation, duplicates, empty/raw IDs and detached output tests are sound but not substitutes for that witness. |
| 0086 | Scoped positive | Test hold: no hidden-width/height fixture distinguishes constructor copy from the spread mutant. Additionally invalids includes {width:Number.MAX_VALUE,height:0} and requires RangeError in constructor/resize. MAX_VALUE is finite, nonnegative and an integer-valued Number; the prompt requires no safe-integer cap. The reference correctly accepts it, so this is an unsupported oracle, not a reference numeric defect. Require hidden width constructor/current and resize/listener field checks; MAX_VALUE and MAX_SAFE_INTEGER+1 must remain valid controls. |
| 0097 | Scoped positive | Test hold: reference reconstructs all required Preset fields; mutant spreads them. Ordinary enumerable fixtures cannot distinguish the defect. Require a valid non-enumerable label plus multi-record code-unit sorting and hidden id/status preservation. Existing grouping, raw string preservation, blank rejection, duplicate IDs across groups, compound ordering and independent copies remain meaningful. |
| 0101 | Scoped positive | Test hold: reference explicitly reconstructs existing Book fields in success and failure branches, but every existing fixture is enumerable. Add an existing non-enumerable id and verify preservation in both branches; include the other declared fields. Keep error accumulation/order, trimmed new ID duplicate matching, year boundaries and book/array-entry independence. Branch narrowing is already valid and needs no public overload changes. |

These are missing-defect-witness holds, not executed claims that mutants pass. For0086 the invalid MAX_VALUE oracle is an additional concrete blocker. Any later main-authorized correction should be test-only and preserve these specifications/references/mutants; this review does not invoke or reserve one.

## Seven criteria

Prompt clarity and API consistency: all four derived problems equal original problems byte-for-byte under approved reference-fix scope. Required TypeScript field values are independent of enumerability. The fixed references use explicit property access/copying and preserve the original signatures and error/status behavior. No new descriptor/prototype requirement is necessary.

Independent test origin: archived author Tasks contain only id/problem and match candidate prompts. No source tests, reference or mutant is present in those task objects. Emitted test content exactly matches archived independent output after the generator's strip-plus-newline normalization. Archive returncode0, no timeout, no disallowed tool items, no parse error describe author provenance, not candidate verification. Provenance does not excuse missing witnesses or the invalid dimension oracle.

Non-triviality: 0072 combines version-separated state, uniqueness and ownership; 0086 combines validated state transitions, listener registration snapshots and per-listener copies; 0097 combines duplicate validation, two groups and explicit compound sorting; 0101 combines ordered accumulated errors, normalized duplicate checks and independent success/failure snapshots. These whole targets remain substantive even though corrections are small.

Idiomatic code: explicit fixed-schema copying, Map/Set/arrays, ordered listener snapshots and discriminated results fit the stated APIs. No implementation defect was found in these bounded scopes. Sparse/out-of-type values, arbitrary metadata and unspecified nested-resize/callback policies were not used to invent new requirements.

Dependency isolation: standard TypeScript/JavaScript only; manual assertion helpers need no Node type declarations or external packages. No candidate code was executed.

Realistic known-bad failure: every mutant reintroduces spread copying at one accepted-input boundary, dropping a non-enumerable required field. That is a genuine defect with a tiny standard-object witness, but none of the submitted tests constructs that witness. All four therefore remain held despite scoped-positive references.

## Oracle boundaries

New tests should assert required values and ownership, not retained descriptor flags, input prototype identity, arbitrary extra-field preservation or private representation. Use typed fixtures with Object.defineProperty changing enumerability, leaving all required values valid. For readonly listener values, ownership probes may use a local cast without changing the public type. No broader safe-number restriction is supported for Dimensions.

Existing JSON.stringify helper comparisons are used on ordinary fixed-schema fixtures; they should not be copied into a hidden-input oracle that accidentally omits the very required field being checked. Read the required output fields directly or compare explicitly assembled expected records. Do not rely on serialized input as the expected object for a non-enumerable fixture.

## Binding checks

For each row the approved plan parent hash matches the canonical immutable parent, candidate prompt equals original prompt, rights match originals, and every source field except versioned transformation matches original lineage. Test SHA was recomputed. Source remains McEval-Instruct revision57bd46727e49ac3e2890218a146d35c2454a8496 under CC-BY-SA-4.0. Original source tests and mutant differences were reviewed during the hash-bound batch-2 selection; fresh derived complete artifacts were read here.

Candidate files are datasets/cache/expansion-v1/versioned-recovery/r21/<full ID>.candidate.json. Canonical hashes use sorted compact UTF-8 JSON with ensure_ascii=False. File/evidence hashes use raw bytes.

### exp-v1-recovery-r21-typescript-generation-0072

- file SHA-256: `92aa8cd6580f3888ae438c19d0bb1fa0eea24b68e23c903c62dbfd47cf5150a1`
- canonical SHA-256: `260fa15fccc2fa53e29fe064790953755c18d14166d23e1b39085a1a5aad796e`
- original SHA-256: `4a4a6d0f9bf22025ea247abac34a73fd21f2896e07725f7ee77f6c4dda5d2729`
- prompt SHA-256: `d60440f4bce9496322ea76e09ba8f648fca3be78f10050c8a6c2ada2c37a906d`
- reference SHA-256: `bbc19c1465c2b617813bf9138477470b71db2f90f39a0f8ff865161d65704ce4`
- test SHA-256: `1b1b541054709b380b787cdbb9f6b21fca5a2b70f782b462b47aa5a12ad11da5`
- mutant SHA-256: `1db0438e6990e0e68aae91890ae01e7432653a72ec364b2094b8e9127e7d955b`
- source SHA-256: `c15a4be7ab0853e9e49ed916afa276f9ad1756559ae785b5e413f0e9f5c7b1ea`
- Source record: `row-33323`; rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

### exp-v1-recovery-r21-typescript-generation-0086

- file SHA-256: `e4119fedca000396c72dcbea05afe258aa9da8c8757e9c05a9e9c6c343bd8ea4`
- canonical SHA-256: `d93e39bb8d457ff8dfa5592aa545dafd83419ddbcb3528a39bbef49250a4b6bb`
- original SHA-256: `c0c1b1b9b53b42b12de2ca9a4bb6ddca4bdd61c0d024b6a726a16c840e28f168`
- prompt SHA-256: `d4b09434518cb86b853ed58b90c424262238c7c6c7af1f48f24a686976472379`
- reference SHA-256: `16f81c80ca23422ef9c5a921e08ca3a179fda35963902e62fd5d4e49e89e23ac`
- test SHA-256: `f44c68aa3120961c2c72d6d6219fb922809121030cb41338634794a6c6d5fd91`
- mutant SHA-256: `415d6fb1c5f8164f9023ac64bce044b529d6c3d21e0f9856fdd66d5f975b28b2`
- source SHA-256: `68eca6df8bf1c06a2ddcfae60c74b8ac930c50b230a39348986e1cdd83176482`
- Source record: `row-32635`; rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

### exp-v1-recovery-r21-typescript-generation-0097

- file SHA-256: `ac8b388ee07b2ae704f0c2789ee3ab32ae337a5d9a3634c7cf198da5624c010d`
- canonical SHA-256: `81e16b093bc1f4fc543fcce61451336f83403d1fd293af0a4c44500a67fe6bea`
- original SHA-256: `76fe2c6d594e702af13675a235223ee8e0cb2aca33dc47fbfae5f69f95e872a4`
- prompt SHA-256: `39080ea5e89f7034dc30a827a4e4dc64a0b20f0209e33074284151d14964bb35`
- reference SHA-256: `b4a724c8bc200764c9a3c6731446208044bd5848cf558e8aa56c555f19911d6e`
- test SHA-256: `a90201c7cf9b69c65107b3246d870a366765bfb4d23d13e48532a10652897399`
- mutant SHA-256: `419d455d6ed23d54308943fc50296ff4dcbb2e52ab8a74e9b29af77880c3cc1d`
- source SHA-256: `ade5c72d02aff6d873b0b45911d178b80a55202ee9dc2f015fd7adc90c2a783b`
- Source record: `row-32889`; rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

### exp-v1-recovery-r21-typescript-generation-0101

- file SHA-256: `f9d1735279d0853d922b6441b414353c9710f80ece67071602d8d9f69811e564`
- canonical SHA-256: `c096c0c789f1664782b60c4701bc8843c24e23566fb55e8f2858dd9170af45c4`
- original SHA-256: `59af9f01c3c8a5b5e026a24a6ecfaa2e3450b37b124101b1e11aa23227cffe90`
- prompt SHA-256: `5a5de0dab5e6453a590aa6817ae5b519858d324a23d64a517d99bf3a88fd4215`
- reference SHA-256: `f11acc43a2b18e2a23e16d4db572c4b2b0dff73d2855ca677a759ae0bb8380d7`
- test SHA-256: `335c42aa3fb0c8cecf93dd333dfebdb1e10ef2a387d59108c46ad58b22a132cb`
- mutant SHA-256: `62dfe8aa75b1ef51ea80b9fa1808fc5d3ffec26188c88964f57ce6a152d87af4`
- source SHA-256: `b424d77a41dc28adabb96e2238c848ba6719014f78af15d3365a6a22c9b271af`
- Source record: `row-02270`; rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

## Shared evidence hashes

- measurement/data/expansion-v1/recovery-plans/r21/plan.json: `a5fe5bbb1cffe149091f626ed317a0e79c39985c10c883acd8f83df3c04582ca`
- datasets/cache/expansion-v1/versioned-recovery/r21/run-contract.json: `a455daccb7e85a30c3cc86d4c328ee44be8e6fd166afef6fe685bba9c8225be4`
- datasets/cache/expansion-v1/versioned-recovery/r21/typescript-recovery-independent-tests-evidence.json: `97fc9d46aa0d3f8ef1a8ccb4fab08879379ac4a98c8611dc5544537fb18fd0b7`
- datasets/cache/expansion-v1/versioned-recovery/r21/typescript-recovery-architect-evidence.json: `0e2a61256686b9048af802fbba01e0b97a89523f9db591a74b2772dabe413b02`

