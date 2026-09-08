# R26 Go and Java independent static quality review — 2026-09-09

## Decision

This is a bounded, static Gate 2 review of the six Go and four Java R26
test-correction candidates. Nine candidates are unconditional seven-criterion
positives. `exp-v1-recovery-r26-java-generation-0123` remains held because its
new collision scenario does not distinguish the supplied delimiter-key mutant.

| lane | reviewed | unconditional positive | hold |
|---|---:|---:|---:|
| Go | 6 | 6 | 0 |
| Java | 4 | 3 | 1 |
| total | 10 | 9 | 1 |

No generated candidate was executed. This review did not admit data, mutate a
candidate, inspect or mutate cloud resources, or supply an admission seal. A
static positive remains subject to fresh pinned, resource-limited,
network-disabled reference/known-bad directionality and the separate admission
gate.

## Frozen scope and evidence

The review used the required project plan, decisions, state, primary-source and
handoff documents, the R26 request/feedback/plan/run contract/generation
registries, both lane correction transcripts, the R24 Go and Java reviews, all
ten R24/R26 candidate pairs, and the ten immutable original source candidates.

- R26 request file SHA-256:
  `1dc3ec0d046bc5beca47b72d2a5c3d37cd1e2cf86f39c275947b445622000677`
- R26 feedback file SHA-256:
  `dc8ecab5c4911bc85b92f90d1392af7db49750e1dc080fdeb9f8345367bb4dc7`
- R26 plan logical SHA-256:
  `11dce4e35cb0afa717cc966b9540f541caf5f6258b967f260ade7131df0f0293`
  (raw file SHA-256
  `48d7a05990b0882f209c78a0942b8e21ae44a103e1cad192241ec33c6c8d4071`)
- R26 run-contract raw SHA-256:
  `bd94fcb8b81d1efb14380d496d5f5dcdc8715c3b47678d1865e2488c3b8c9448`
- R26 generation registry raw SHA-256:
  `2045083c185c671803a717a81df41eeb8edd176523a3736401455a4a59330478`;
  its 25-candidate aggregate is
  `51eaef24706eb6031cd6205ef81b20f4509e2c624b9ccbbaa8f94240611b457c`
  and its status is `generated-not-verified-not-admitted`.
- R24 Go review SHA-256:
  `9e4c20764d3406d1af2bc2f34c58983c9fb34138349a9e496121c6603d2b965c`
- R24 Java review SHA-256:
  `64fb3f7692ab61471926c3f498401927bea1ebaca64b7b57acf08aab1bdb302a`

The seven criteria are: prompt clarity, API consistency, independent test
origin, whole-target non-triviality, idiomatic/plausible reference,
dependency isolation, and realistic known-bad discrimination.

## Immutable binding reconciliation

For every row below, the R26 prompt and rendered-prompt bytes equal R24; the
reference and sole known-bad code bytes equal R24; the user/assistant messages
equal the task prompt/reference; source metadata and rights equal the immutable
original parent except for the mechanically required R26 transformation suffix;
and task ID, lane and task type bind the candidate record. The R24 and R26
candidate columns are canonical-JSON SHA-256 values. `source` is the immutable
source-record SHA-256.

| ID suffix | original parent | R24 candidate | R26 candidate | prompt | reference | known-bad | corrected test | source |
|---|---|---|---|---|---|---|---|---|
| go-0102 | `4377988fa835ef619986b4d073426242af17e62bd9b98746682359517ddc27b7` | `c55a1a04b100b0c6ed79ac44c483d9e4269bed317aa2c7686db7d2fec21fb753` | `d1ce768c5e6a3f4ced0294156597530a4b4a0fcb4cd1caac81112fed25022788` | `d3038d4c26b833ab95c0bb140b49c248462019dd6f28203397ce43d1078204e4` | `ba63f7acf6955c219fb93bb65244bc318f2b5bdeb9515115152e82f41729a3ad` | `44031e579da404885b1691eea8730b9b05538f72bcc4e63bf85f3e24b497d97c` | `405f25b6c8bb899ff947fb789db38394e5960d9fa6a6070d23657a7d9a3c47f3` | `9b17377e4e10c0b37fbeaae4388c126879259d3f189c23b70f09d0b69e7fc863` |
| go-0160 | `e71c6bf13e826999d47ca6b1c7e113ddebc97924f45ae0496d629c35c8f6605a` | `6e46ef94c05af07b278379cd10f21201da53b857e36e96eb3319943851223347` | `6706bf819ad1cd47bf1d7fd72fd0349d2d12f7f735fc153b5047e62e56cef670` | `f5e850694c91a9ed83a5eab94954024ec88d93c30858af2ea27e97fa4462e2a7` | `48b2fe71c0c31ebf0c79855fe34981f28372dfcb9f3c9e4e367c7e85637b65e5` | `5a1b6ddab0bcce7230dfef8e34f6184669945515734def9a0b3e626f02d41550` | `22d83669f608694e3cbaffd0794013ea4f58aaf703f77790b41d16f92e2d072e` | `9d171379ff74b9d76867c37990a38abb93b0617a0feb31d5c3dd2eb9ee0b3063` |
| go-0276 | `1b101834ee8390d3b845e09023ce6ee3c1b6a439f146b889b5fb2c5025d00fda` | `1fed776fceb6b2c67e52b5299ef4c65997d6a94cffdf1012fc045ce910676279` | `d929cc225b54479bf3b1d4df8d42354f6255db0bdef9ed8ca9f081d20b4de613` | `84f806be6720e7e6a4acd309cd6991ec881a86f5daf3e187ff959c301ae02172` | `31c72cc1ae87f8c37ade0e808df25c0fdbc156edaf9a7bf38448879a3d6ea2e0` | `d673ab0804e539f327f374ae192254b22df82c0501a5c4c9287f7316032aeee1` | `841ecad1635ed143e10036f34647a9908b459dbe92584278eb03a223663b4774` | `daf674758d1e7848b9b061d9546069822129f55e249518fc7655b13dbbd43913` |
| go-0382 | `fa94df20b2555700b767d35154cfff4b52c4f888374d96cc9c5e893e0767b99b` | `921df4a4a294738d50c8299cdd36217751e765e9612d219432779bee50384124` | `4d5971c72bed158010c2c98ffce4c7bd28e4b368d3de0776467d2db18afa39bc` | `7fe8a3247abfd0aa2fb3f4d5b12e6c4505653cd0364b819a98ad1b5eb3c12754` | `e3a31e638e423e14abc940a306151511b3c98e954a8b28396488abadfa1a6e0a` | `c3721cfcbe75daaf3af5650daec9954e0dbed54f5314fd246ce02e5801bed933` | `b0c2b37819c8504fd1e5c620c2f6b1a5e05e5a33f89942ab611313bdd2b0f34f` | `f2871dbb809c89434ed469db95e0d5a42ea7588c4a3d2c5066ef36194b1cb772` |
| go-0542 | `c183cc2df0bccc34a4ba71a6c9f144b92756fbc8862032111f47886ae3058a66` | `e5fa21dbe209de543e5519a10393273472106f472f85a9a63b68773aef09c776` | `5ca924a2ac558ac9887bd873dce53d89c91f04307de3b468189b9ee44072e817` | `001dc417ffe707a206143bca902760995c989a5e81e353fcb6b2ed860096632e` | `f5eb9f180b1e1a329a2526fafd44130d19eeaca41bb66e44580866d01de4ec26` | `b6c9ddb8b4207e26e28a60f9cc289895685497a4e0ba17dada4626c4e80dbf2a` | `fcbf14f96256af2513ae83a613e401b4829c444e127858baf8cf2f914f442a73` | `711b143e103d3a12419ee699cb176532ba9c6608e27ad951a552ed30038cac64` |
| go-0791 | `baedc50e12510a76ed553b3cdfdf92189a02b67c1ea41f534813cafd1be75675` | `173b31e9a25c578827b89c1db3546b39e6a927c462fb97bea58b7ce7bba945aa` | `acf03b31e3ab5edf7b65533abb1449ebc285c7ce0d8d2505d6a4a87aae717e88` | `a0f50420a08bd018cd47099551381fa974c9b0d1d191b2349eb29ae87d0d6e96` | `b75ef2b0df09536dbd734c996cc944bd7162b09ecc7de9f2a522c6815bffdf53` | `f047728069a0556a60c55e0ae707665190fea58485dfd7f1f8ea3983460c1ee0` | `a9aa65453918b78623bb572dbea467b2196127c1a615ed6c59cd4de729575b11` | `89fd81ac61ddad0ff958d721cf65b66f8c97a60bc4c6cf75b7f23d5c869202fa` |
| java-0123 | `8f23c06357bc9e5422f9849fcd12ee7764b3c71ddb90654d2fa9bf2fdbc11b2f` | `a2f307ced55abd6f34f66084b17b0333f7eb2d1b7b035c65e0a41af8a1793b7b` | `6a6aa28631ccee2d854f4c66237ea7a9a56c3506ade69817dfd34ba1703d3b66` | `549b56d62328e9d6c9022a26e8c16aae073dda4223153c89ecb4f5e57cefa0d0` | `dc3872f3895cf12f88fb3621b23d3bf7943d8e8d1856ecebde473ecd21499349` | `dcdf4bee21158dbbf0c6920245120b2fad35d062e691b72cfe9893178d2d7506` | `5900b8ee6929144302344b74c41213c12304d99eb706dde5a8569b22b19cda04` | `3ab75cb53bbb3e5afc119f686f8c49d549bff31db6fc204ae266f6eb7f71fb8e` |
| java-0196 | `cf7d82bbc4fc796c951fab429f522607eb8e0847c3a293b636c16d2c4d37b216` | `0e890f32f4cb595318043a89a7f4ce48d5e30cc0aaa4678cdc775b398c65d04c` | `a47ddace0baccc97b9eb92b0570bd5d1db7c9e1b4df84867b1a63181f2fb3fa0` | `82a9037d40938d0d2020278439656a0daff4a0e2d4f00f07ce4df3b1653263ee` | `c5df08296786d230c0b78907a3ed2ff23ae614c313e0d9fb311ffca7621809fd` | `9b99f3f70d8e1c9272c93a882dcb8f04be9d05a6da15c4b689980d87fe6963dc` | `1ffa185f65b4a89f21bbe2dc5e516448103616b8a6f16f2bf133ad5be96db006` | `46f6521d6e29115c03648c59b7a4cd3bfc7b20e460e558fdee4992f668289f63` |
| java-0427 | `0667dd7c4bd4913f0886ed1c031961871b89687065479ad125756b731a35ac7b` | `aa393a0f4ca6eb7558827a137ed852fc246408536f26a35272396b2937c7b6ef` | `e0008f1383a29a24990ea1f6554d2519b0d134eb74155b47ba2b511c7a5b124b` | `8fef9391ee8bfcd656393f7e81d377efe497b2cf258d50172c74fa3c88d042a6` | `3a2e547e4d11bf0c539ebf3f77cf52915750d03cf29134df298ad0bf7b9f0fa2` | `9e4f416431e58a6ed9c48c3f05e4cfacd1acc8f49697e8d5408102b4df635a08` | `7c010d6879d082d92101226462e0d8a2bc324174e60951742f16200ed81798e6` | `3d997a96d05c39524df81378a068c7e16a4519c8b1a3771d7e48edecb58f7e9f` |
| java-0513 | `79d21d7bc51051e5e40ecd5c20263a634bbc4752a9ea2d96600b29d4858696b6` | `7eb1d85bed548949d28ca7a8fb10a267cd03d8ea177b1dd34b29185d95e7e97e` | `7447c16bef348aa4ca818e7f7ae785c6a66e39b7b619ad6cb3237d54d06b7657` | `317203991ca46103bdef0505ca0f5e47b7bc1665ae1b90d082af75c60b8cba08` | `f297f9492aa8888a420567b9af434e1d60792e12280eedc443857be5398a407e` | `9a6e575ab6593e02fe4dd34910ab55edbd828bf77ba2ac298458f1614ae510ce` | `0864e20171b9686f38fcc92c77613cd8c6db48c85def2df62c7ed8c258ec52d6` | `d1efe09a382e868d0b7be2f5fe00892e06eebff6b25f75c9cdbb40836a4daaf7` |

## Independent correction and evaluation separation

The Go correction evidence raw SHA-256 is
`8552b03996e4acf6c7e51e6b195e3832673cbe6df6e9335d03aeab9214d4c4db`;
its prompt SHA-256 is
`4272b2562c6324977ddf21e3825c4402711f983b2f73d0c6e298e930f9e82285`
and stdout SHA-256 is
`dee934cec05efa990b555eae729cfd2e08a69d75ff8ab8621395aec42f5b5db1`.
The Java evidence raw SHA-256 is
`fe909bdf31bcef52cc762d2b2b7a4a66605a0e5a0b56de3f1b6afc833abb00b2`;
its prompt SHA-256 is
`533ee3bd3ba7c9ced6294a051d6f418cdb75fe3962812129e41eef16d7ca3278`
and stdout SHA-256 is
`20c540f08c231d19e21eec6655e069c5f8fa688ffeba739bb275c9a4b0c4fedd`.

Both transcripts bind a read-only, isolated, ephemeral Codex invocation. They
record no disallowed tool item, parse error or timeout. For all ten items, the
critic input contains exactly the R24 specification, R24 proposed test and
specification-derived correction feedback; it contains neither reference nor
known-bad code. Each returned ID and test body exactly equals its R26 candidate.
Thus the correction preserves the frozen prompt/source-only critic boundary.

A separate read-only comparison used the admission normalizer and SimHash rule
(`NFKC + casefold + whitespace collapse`, minimum 12 tokens, maximum Hamming
distance 3) against all 546 task files below `eval/`. For every candidate there
was zero normalized exact prompt match, zero fuzzy prompt match, and zero exact
reference, known-bad, test or support-file hash match. This is static
evaluation-separation evidence, not admission and not a substitute for the
admission gate's rerun.

## Seven-criterion matrix

`P` means positive; `H` means the criterion holds the candidate.

| ID suffix | clarity | API | independent tests | non-trivial | reference | isolation | discrimination | decision |
|---|---|---|---|---|---|---|---|---|
| go-0102 | P | P | P | P | P | P | P | positive |
| go-0160 | P | P | P | P | P | P | P | positive |
| go-0276 | P | P | P | P | P | P | P | positive |
| go-0382 | P | P | P | P | P | P | P | positive |
| go-0542 | P | P | P | P | P | P | P | positive |
| go-0791 | P | P | P | P | P | P | P | positive |
| java-0123 | P | P | P | P | P | P | H | **hold** |
| java-0196 | P | P | P | P | P | P | P | positive |
| java-0427 | P | P | P | P | P | P | P | positive |
| java-0513 | P | P | P | P | P | P | P | positive |

## Per-candidate findings

### `exp-v1-recovery-r26-go-generation-0102` — unconditional positive

The account-store contract and public API remain clear and substantive. The
reference uses canonical raw-base64url re-encoding plus constant-time HMAC
comparison and remains plausible and standard-library-only. The correction
retains canonical success, account state, normalization, ownership and tamper
controls, and now rejects appended LF, appended CR, embedded signature LF and
embedded signature CR. Those concrete spellings distinguish the realistic Go
base64 decoder mutant that otherwise ignores CR/LF.

### `exp-v1-recovery-r26-go-generation-0160` — unconditional positive

The signed-pass lifecycle, exact JSON claims, signature and expiry boundaries
are coherent and non-trivial. The unchanged reference validates canonical
base64url spellings, JSON completeness, claims and HMAC. The corrected suite
first guards the issued two-segment shape, then covers appended LF/CR and
embedded LF/CR in both payload and signature segments while retaining padding,
signature, malformed JSON, claims and expiry cases. It directly discriminates
the supplied noncanonical-encoding mutant.

### `exp-v1-recovery-r26-go-generation-0276` — unconditional positive

The fixed-lifetime credential contract combines overflow-safe issuance,
authenticated serialization and precise active-time behavior. The reference
uses canonical raw-base64url checks, constant-time HMAC, strict JSON and safe
`int64` lifetime validation. The correction retains the whole earlier suite,
adds a canonical success label/segment guard, appended LF/CR and an embedded
signature LF witness. This is the exact approved minimum for the supplied
CR/LF-accepting mutant and introduces no new semantic oracle.

### `exp-v1-recovery-r26-go-generation-0382` — unconditional positive

The raw-JSON MAC semantics, canonical payload requirement, claim validation and
pre-issued-time acceptance remain explicit and substantive. The unchanged
reference signs raw payload bytes, re-marshals for canonical JSON equality and
uses canonical raw-base64url spellings. The suite now covers appended and
embedded CR/LF in both token segments, while retaining pre-issued time, unknown
fields, canonical JSON, lifetime, signature and secret ownership controls. The
realistic encoding mutant is directly exposed.

### `exp-v1-recovery-r26-go-generation-0542` — unconditional positive

The interface-based aggregation target requires ordered dynamic dispatch,
numeric-domain validation, zero-on-error and ownership behavior. The reference
rejects nil interfaces and typed nil pointers without incorrectly rejecting
other nil-capable concrete values. The new named nil map has a value-receiver
`Metrics` method and must produce `{Units:2, Cost:3, Count:1}`; it therefore
distinguishes the mutant's overbroad `reflect.Value.IsNil` policy. Typed nil
pointers, malformed returned metrics, ordering, empty input, zero summary and
input preservation remain covered.

### `exp-v1-recovery-r26-go-generation-0791` — unconditional positive

The task combines private-field JSON exclusion, exact decoded key grammar,
duplicate detection, type/range checks and generic object decoding with
`json.Number`. The token-based reference compares decoded strings exactly, so
escaped spellings of lowercase keys work while case substitutions do not. The
new canonical and escaped-lowercase successes plus `Label`, `Level` and all-caps
rejections directly distinguish Go struct decoding's default case-insensitive
field match. Escaped duplicate keys, missing/wrong fields, trailing data,
privacy, numeric precision and ownership remain covered. The simpler level-0
fixture also removes the R24 test's unnecessary rune construction.

### `exp-v1-recovery-r26-java-generation-0123` — hold

Clarity, API consistency, independent origin, lifecycle substance, reference
plausibility and standard-library isolation are positive. Interior NUL remains
allowed, as required. The decisive discrimination is still absent.

The supplied mutant represents an unordered pair as
`min + "\\u0000" + max`. Therefore `(a, b+NUL+c)` and `(a+NUL+b, c)` both map
to the same string. The corrected test sends **both** invitations before it
accepts either one. At that point the mutant has no link yet, so both sends
succeed. It then accepts both invitations into the same set key; both symmetric
`connected` checks succeed because they query that same key. The two added
cross-pair checks query different keys and also return false, and `clear`
removes the shared key. Consequently every new assertion is compatible with
the supplied mutant.

A discriminating test must establish one collision-prone connection before
attempting the other pair, then require the other invitation/connection to
remain independently creatable (and independently clearable only through the
available global `clear`). R26 is the sole bounded correction attempt, so this
candidate remains held rather than requesting another critic draft.

### `exp-v1-recovery-r26-java-generation-0196` — unconditional positive

The stateful sink contract, atomic batch validation, threshold commits,
snapshots, reconfiguration and close lifecycle are substantive. The unchanged
reference widens both buffered weight and threshold arithmetic to `long`. The
correction fixes the prior internally wrong committed-size/index oracle (five,
not six), adds explicit atomic-invalid-batch state checks, and adds tiny
physical witnesses at capacity `Integer.MAX_VALUE` and capacity
`Integer.MAX_VALUE-1`. The first exposes `(capacity+1)/2` overflow; the second
exposes `int` buffered-weight wraparound. Both are bounded in physical memory
and directly distinguish the supplied mutant.

### `exp-v1-recovery-r26-java-generation-0427` — unconditional positive

The immutable ledger operations, global ID uniqueness, ordered snapshots,
updates, filtering and long aggregation are clear and non-trivial. The
unchanged reference validates the complete input list before every operation.
The correction replaces unsupported object-identity assertions with exact
public-field comparisons and introduces an existing two-entry duplicate-ID
list across add, present/missing remove, present/missing update, present/missing
find, present/missing group and aggregation calls. These witnesses directly
distinguish the supplied mutant, whose input validator checks nulls but not
existing duplicate IDs.

### `exp-v1-recovery-r26-java-generation-0513` — unconditional positive

The typed codec, framed UTF-8 representation, GZIP transport, corruption
handling, ownership and mutable result contract are coherent and substantive.
The unchanged reference reads item data incrementally with an 8192-byte chunk,
so truncated maximum declarations fail before a giant allocation. The
correction removes deterministic equality of separately packed GZIP bytes,
which the specification never promised, and instead checks semantic
independence. Tiny compressed frames declaring count `Integer.MAX_VALUE` and
length `Integer.MAX_VALUE` now require bounded `IllegalArgumentException`.
These cases directly distinguish the eager-capacity/eager-item-allocation
mutant while retaining UTF-8, malformed/truncated/trailing data, codec failure,
null and non-aliasing controls.

## Handoff

The nine positive IDs may proceed to fresh serial reference-pass / known-bad-
fail diagnostics and the later separation/admission workflow. Java 0123 must
remain excluded. This report is review evidence only; it is not an admission
record and does not count any draft as training data.
