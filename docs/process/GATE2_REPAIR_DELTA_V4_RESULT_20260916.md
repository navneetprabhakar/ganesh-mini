# Gate 2 repair-delta v4 result — 2026-09-16

Status: `qualification-failed`

Contract: `capability-stratified-v4-repair-delta/v1`

Frozen plan SHA-256:
`79849d2f8b70ba69572b4c3fa1761bdb413562c6f6d9a12537d93a1724812ef6`

Terminal qualification report SHA-256:
`af2ce7ea3cab939ea219eef840af9e42bcb379f0f5de7002bcdf7e688da8c2e5`

## Decision

The v4 repair-delta construction qualification failed. The complete ordered
60-candidate first pass admitted 5, rejected 55, and left 0 unresolved. The
frozen first-pass thresholds were not met, so reserves are forbidden and none
may be generated under this contract.

This is a failure of the v4 data-construction and qualification method. It is
not a training failure or a measured model-quality failure: no Ganesh Mini
training, untouched model evaluation, merge, quantization, laptop
certification, or release evaluation was performed by this campaign.

## Source ontology and queue

The fixed native CommitPackFT extension selected 3,000 records: 1,000 each for
Go, Python, and Rust. Its extension manifest is sealed at
`530aca0ee51ba65c703f1adbb97fecf16e129aa3a85920a1ce5601a0113a9bca`;
the selected extension JSONL SHA-256 is
`125b9f6f53180c3f74ad729adcb77e98eaa042a496e075f31beb274a12b977e4`.

The ontology wave sealed as `failed` at summary SHA-256
`1ca22c30b5b50d7e27b9632b60c97824444d010058a356714dab60bcd88fdb04`:
34 failed batches covered 170 of the 3,000 fixed records. No adaptive top-up
was performed. The aggregate nevertheless sealed `coverage-complete` by
combining the valid wave results with the compatible v3 carry-forward:

- aggregate SHA-256:
  `87c8dbb34e4570c7b87864675c7bae59aadd6be378ae3cad8306facdcc6003ec`;
- combined evidence SHA-256:
  `15d9a3c65a44110389d1a1d8cf042125c0df54a8dec120006990dbfd8e82d782`;
- source-union SHA-256:
  `82bc4df27d634885e48ff78643d34e38c238b92b283e1bdf66488b5e89a5f2e9`;
- 15,253 unique sources and 15,253 unique lineages;
- all 60 repair cells met the minimum of two sources; and
- evaluation artifacts read: 0.

The resulting queue contains 120 unique source identities: 60 ordered
primaries and 60 cell-bound reserves. Queue SHA-256 is
`f148208afa6015ed842d544f38fbdd6fd66653ae2623e61a8cd6560a8228f863`;
manifest seal is
`e99c52b6b33e0d447641e9836dbe86496bbac9bef71d11ffd83377cb6ef8d163`.
Primary sources comprise 22 McEval, 26 MdEval, and 12 CommitPackFT records;
reserves comprise 14 McEval, 27 MdEval, and 19 CommitPackFT records. The
manifest records 120 unique identities and zero evaluation reads.

## Tooling readiness and teacher identity

The production-tooling fixture report passed at seal
`22c2fe7717f6194fa0f67630ab9b4bb4f40cbe661c31ea6ce4a2501cb8345490`.
It admitted one fixture in each of Go, Java, JavaScript, TypeScript, Python,
and Rust, covered CommitPackFT, McEval, and MdEval provenance, demonstrated
the frozen four-suite outcome matrix, and rejected the deliberately broken
staging control. It read zero evaluation artifacts and emitted no training
records.

All six primary teacher batches used the same recorded identity:

- provider: `codex-cli`;
- CLI: `codex-cli 0.144.4`;
- model: `gpt-5.6-sol`;
- model snapshot: `provider-alias-not-exposed`;
- reasoning effort: `medium`;
- service tier: `priority`;
- isolated read-only execution, batch size 10, 1,800-second batch timeout.

Each lane requested and generated 10 candidates with no teacher-batch
failure. The sealed batch evidence and candidate-output SHA-256 values are:

| Lane | Evidence SHA-256 | Candidate output SHA-256 |
|---|---|---|
| Go | `16e5d290ebadf846d52cdd55e8b6a784af456cd21ac3af516e2d66aa640e65a7` | `118207e3f73e228f66cffb9abe5693736b6a4f4a195fbaf8b2b9695891f4ceec` |
| Java | `d280b7acc961ae5af458df66d4f5a6fd34330b83702835826280a94e62f0b5a9` | `5454d1696fd8ec0032f6a0c61361f355d069ea8acfd4505a4835ec6cdf5e9a6c` |
| JavaScript | `232db656e87d3c057f1700bc2a53121d53be9c69907d66bc106f98ab783a50b0` | `e2b4036f37a7a6a75092ce514238d210e04ec669064ab83d166688458f3660e0` |
| TypeScript | `733b4cae6f220439e2e55fa91189eb76f7d2f5615420fb3dabe932354c41bab4` | `27afc61de95bf25dd29856bb62909c333d65a0060c20c5f14292d9e1c286d458` |
| Python | `015f161feb88ef430c06f09e9d7bc0416d9623ae81b30a1b53f6ab78904a305e` | `6906db3265f2727b9dfb49e7af3b8cc15901b7eb030923faf8150ac545e78445` |
| Rust | `221efafb66f0f9b830dcd81ffa205788188b584aa35a912ca59d5ca75ac6f990` | `277e65c9b049fd08c91bd97937d1de053ee04844c18dd9c79e61f5f369ee4107` |

The batch evidence binds the v4 plan and queue-manifest seals above.

## Ordered terminal accounting and ledger correction

The primary cohort binding seals the exact queue order of all 60 primary IDs:

- binding SHA-256:
  `30dda8353abde52ba97de11795dc63f2e22048e57c7a92772b31de4fca19e258`;
- ordered-ID-list SHA-256:
  `c3c7d794444a69a3eb05f02cac3d8df7a20f0433a50fd46fb1c202121ef4a56d`;
- records: 60.

The controller initially emitted 60 ordered terminal artifacts at file
SHA-256
`aae89dfe89c47742f5400c31217b653e6cb6f2a4ec3f5e2ad7c2023d54b31e63`.
Two terminal `final_admission` wrappers omitted the retry ledgers already
sealed in their exact pre-final candidate-evidence artifacts. A bounded
evidence correction copied only those two existing ledgers into the wrappers,
preserved candidate order, and left all 58 non-target rows unchanged. The
affected IDs were:

- `cap-v4-numeric_reasoning-go-repair-primary`;
- `cap-v4-ordering_and_selection-typescript-repair-primary`.

Correction report seal is
`05cb34251ceaca6c3c4289779128e208ddd0d238ac2f8aa594253ff5cd1aee51`.
The corrected, canonical 60-record terminal artifact SHA-256 is
`db1ab2174685d865f7e5e34f3f3e28d425c312f079a867a4e6d839fe0b7074d9`.
This correction repaired copied evidence bindings; it did not rerun a
candidate, change candidate bytes, change a verifier result, or alter a
terminal disposition.

Final admission reconciled exactly 60 ordered primary candidates: 5 admitted,
55 rejected, and 0 unresolved. Admission report seal is
`bfc80e399b44fb350048ed459c2bb611801757fb2c73286389d5c4c98aca99d2`.

## Terminal outcome taxonomy

The 60 outcomes divide exactly into 30 + 23 + 2 + 5:

| Outcome | Total | Go | Java | JavaScript | TypeScript | Python | Rust |
|---|---:|---:|---:|---:|---:|---:|---:|
| Test-author contract rejection | 30 | 6 | 9 | 0 | 7 | 8 | 0 |
| Post-teacher preflight rejection | 23 | 0 | 1 | 10 | 2 | 0 | 10 |
| Final-admission executable rejection | 2 | 1 | 0 | 0 | 1 | 0 | 0 |
| Admitted | 5 | 3 | 0 | 0 | 0 | 2 | 0 |
| **Total** | **60** | **10** | **10** | **10** | **10** | **10** | **10** |

The 30 test-author rejects comprise 27 responses that did not return exactly
one file for each split role and 3 Java responses whose test content did not
expose the required `SolutionTest` entry point. All 23 preflight rejects report
that the reference failed the frozen known-bad cross-witness execution
contract. The two final-admission rejects were:

- Go numeric reasoning: known-bad cross-cutting suite did not pass;
- TypeScript ordering and selection: reference primary-discrimination suite
  did not pass.

The five admitted cells were binary/bitwise Go, graph/tree Go, string/Unicode
Go, numeric reasoning Python, and parsing/encoding Python.

## Frozen gates

| Requirement | Executed result | Decision |
|---|---:|---|
| All 60 first-pass candidates terminally accounted | 60/60 | Pass |
| Zero unresolved after bounded replay | 0 | Pass |
| At least 54 final-validator admissions | 5/60 | Fail |
| At least 9 admissions in every lane | Go 3, Python 2, other lanes 0 | Fail |
| At least 5 admissions per primary capability | Five capabilities had 1; five had 0 | Fail |
| At least 10 admissions per cross-cutting dimension | Maximum observed was 2 | Fail |
| Zero source collisions or lineage failures | 120 unique queue identities; no final-admission lineage rejection | Pass for executed evidence |
| Zero separation failures among admitted records | All 7 post-test candidates passed; admitted subset was 5 | Pass |
| Zero evaluation reads outside the content-free boundary | 0 | Pass |

Because the first-pass thresholds failed, the frozen plan forbids reserves.
The apparent `reserves_complete: true` in the summary means no reserves were
required after a passing first pass; it does not override the failed threshold
gate or authorize reserve generation.

## V2 equivalence, separation, lineage, and evaluation boundary

The unchanged v2 generation-equivalence evidence passed: 120/120 generation
candidates were generated, semantically passed, and dispositioned; 114 were
admitted and all 60 generation cells remained covered. Its bound seals are:

- v2 summary:
  `293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139`;
- v2 admission:
  `c576ef4f5b0f137edac829703eae6d7c4a63cae513544d36471f7ffcf81b7cb7`;
- v2 envelopes:
  `4b9427262b2c9645bf2a0edbddba5772340298d6d4554bd4b2f7bce1641d44bf`.

Seven v4 candidates survived pre-separation construction. Their global
content-free separation report passed exact, normalized, and fuzzy checks for
all seven, with report seal
`15c00e94388fc8769687d95ebc6df70bc76c36ecedd644d6d25095f71a904af8`
and separation-contract SHA-256
`4c480fbb7ea1177afb0f4a840efe81e6acdf62f2bd2a41d7da03032abe733a8e`.
The campaign inventory and final summary both record zero evaluation-artifact
reads outside the content-free comparison boundary. The five admitted records
passed the final validator's sealed lineage chain; no source-collision,
separation, provenance, or lineage rejection appears in the terminal failure
taxonomy. This does not assert lineage validity for the 53 candidates rejected
before those downstream checks.

## Go timeout-contract drift

The plan states a 120-second **per-candidate** Go execution envelope. The
executed candidate contract instead placed `timeout_seconds: 120` on each of
the four sequential suite calls. The three admitted Go candidates accumulated
recorded suite durations of 128,202 ms, 129,131 ms, and 127,431 ms respectively,
so the executed implementation did not enforce a 120-second cumulative
candidate wall-time ceiling.

No Go suite timed out and the final campaign had zero unresolved candidates,
so this drift did not cause or rescue the threshold failure. It is still a
contract-conformance defect and must be corrected or explicitly revised in
any future construction plan; these results must not be represented as proof
that the exact per-candidate timeout clause was implemented.

## Final scope and next action

The terminal v4 qualification covers 65/120 combined cells: all 60 carried
generation cells and 5 repair cells. It does not qualify the repair
construction method, a training corpus, a trained checkpoint, or a public
release.

Do not generate v4 reserves, promote these five repair records as a qualified
60-cell corpus, start training from this result, or claim model improvement.
The next permitted action is a new explicit construction decision: either
close this repair-data route as a documented no-go, or freeze a new plan that
addresses the observed teacher/test-author/preflight failure modes and the Go
timeout-contract drift before any fresh candidate generation. The executed
v4 evidence remains immutable and must not be relabeled as a retry under a new
contract.
