# Gate 2 repair-delta V5 result — 2026-09-17

Status: `qualification-failed`

Contract: `capability-stratified-v5-interface-replay/v1`

Frozen plan SHA-256:
`132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b`

Terminal qualification report SHA-256:
`f169894cc32557388ec7812180d1524502af1ae35c310e8f31f3c4177e5452e5`

## Decision

V5 is a terminal corpus-construction no-go. The complete ordered first pass
accounted for all 60 candidates: 29 were admitted, 31 were rejected, and none
remained unresolved. The frozen aggregate and distribution gates failed, so
V5 reserves are forbidden and none may be generated.

This is not a training failure and does not measure Ganesh Mini model quality.
V5 reran the repair-data construction interface. It performed no model
training, untouched evaluation, merge, quantization, laptop certification, or
release evaluation.

## Preserved execution history

The final V3 execution followed two interrupted, non-qualifying attempts whose
evidence remains immutable:

- V1 interruption accounting seal:
  `f939b138bc8be963c709c1550231218a782905335632aef4ca37136806d2cad9`;
- V2 interruption accounting seal:
  `4d739a334ce3df4cc9feca6fbbbe291d93f53a1d896fb457f8caba93720d5c69`;
- V2 exposed a live API schema incompatibility with `uniqueItems`; its 11
  schema-rejected test-author calls and one interrupted semantic call produced
  no candidate disposition and contribute no qualification metric;
- the corrected exact test-author schema is SHA-256
  `e099481a27e5d40923778098eb3c02126ca40e0116565bcd8a224396baf077cc`;
- the content-free live schema-admission smoke passed at report seal
  `5fbb4f0551f42742b31b99ddf19a5e07dce2df69d7cf405c1d3daa8a7b0f230d`;
- the schema-correction manifest passed at seal
  `7b492491f41711692d99d12e53e4cf05d76d2f3b1779a365b9658347e8adb812`;
- the exact two valid V2 semantic carries are sealed at
  `f8a158319e08b822d29b3074061e06e04a45b1a1ba453fadefdec8ba96845ac8`;
- the final V3 attempt manifest is sealed at
  `b8013bcf65b0b520347c682fcf83e933a9bc9d89ee77f8ea5407aa13e885303a`.

The final attempt carried 42 exact semantic outcomes and made 18 new semantic
calls. It made all 60 test-author calls under the corrected schema. All final
attempt model invocations completed successfully at the transport/runtime
layer. Candidate-local contract or executable failures were recorded as
terminal rejections rather than campaign infrastructure failures.

## Ordered terminal accounting

The V3 two-phase controller emitted exactly 60 ordered terminal artifacts:

- 60 generated or immutably carried;
- 46 advanced beyond the strict test-author contract;
- 29 ready for admission;
- 31 terminally rejected; and
- 0 unresolved.

The canonical terminal artifact file is
`measurement/gate2/capability-stratified-v5-interface-replay/primary-two-phase-v3/terminal-artifacts.jsonl`,
SHA-256
`5ab70923a54311db8942fa7210c7689e0418ed09f7065d5b8d035a19bcbcdf70`.
The two-phase inventory report seal is
`6e1512cf01b00272120e041b74487bfc66105627d01db13e9f9a1b1bbe99796d`.

Canonical admission accepted 29, rejected 31, and retained 0 unresolved. Its
report seal is
`3b112519be6c3f122499d137983a58288bdad16bdfaea8c7c83f34c45dc58b11`.

## Terminal outcome taxonomy

The outcomes divide exactly into 14 strict test-author rejects, 17 executable
final-admission rejects, and 29 admissions:

| Outcome | Total | Go | Java | JavaScript | TypeScript | Python | Rust |
|---|---:|---:|---:|---:|---:|---:|---:|
| Test-author contract rejection | 14 | 2 | 5 | 2 | 0 | 0 | 5 |
| Final-admission executable rejection | 17 | 0 | 0 | 7 | 6 | 0 | 4 |
| Admitted | 29 | 8 | 5 | 1 | 4 | 10 | 1 |
| **Total** | **60** | **10** | **10** | **10** | **10** | **10** | **10** |

The deeper evidence audit changes the interpretation without changing any V5
disposition. Ten test-author rejects were false positives from the
`_v5_cross_depends_on_primary` syntax heuristic: all ten suites targeted the
assigned secondary dimension and were designed to pass the embedded known-
bad. Four Java rejects used `SolutionTest.java` for both role objects, a path
collision encouraged by the undisclosed cross-object uniqueness rule and the
required Java entry point. None of these 14 establishes a candidate or test
semantic failure. Five of the ten Rust outputs also contained a latent
`../solution.rs` staging mismatch.

All 17 executable rejects were authored-test/runtime binding failures, not bad
references: 14 used parent-relative candidate paths after the controller
flattened tests to the canonical root, one JavaScript suite imported the wrong
`../index.js`, one JavaScript suite required an unset `TARGET_MODULE` or argv
target, and one Rust suite required Cargo's `CARGO_MANIFEST_DIR` although the
runtime invokes `rustc` directly. Reference and known-bad executions failed
identically before assertions in every case. One TypeScript suite also had a
strict-null typing defect. The evidence demonstrates 31 test-author/validator/
staging interface failures, 0 bad-reference findings, and 0 unresolved runtime
failures.

## Frozen first-pass gates

| Requirement | Executed result | Decision |
|---|---:|---|
| All 60 candidates terminally accounted | 60/60 | Pass |
| Zero unresolved after bounded replay | 0 | Pass |
| At least 54 final-validator admissions | 29/60 | Fail |
| At least 9 admissions in every lane | Go 8, Java 5, JavaScript 1, TypeScript 4, Python 10, Rust 1 | Fail |
| At least 5 admissions per capability | Range 1–4 | Fail |
| At least 10 admissions per cross-cutting dimension | Range 4–8 | Fail |
| Unreserved graph/tree Java primary passes | Admitted | Pass |
| Zero evaluation reads outside content-free boundary | 0 | Pass |

V2 generation equivalence remains passed: all 60 generation cells remain
covered. The bound V2 qualification, admission, and envelope seals are
`293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139`,
`c576ef4f5b0f137edac829703eae6d7c4a63cae513544d36471f7ffcf81b7cb7`,
and
`4b9427262b2c9645bf2a0edbddba5772340298d6d4554bd4b2f7bce1641d44bf`.

The global separation report passed for all 46 post-test candidates at report
SHA-256
`89546c8ec233ff3a042deb33c0db2e23ef88fc05d3bcca0ffeaf6bf28426757c`.
The separation contract remained
`4c480fbb7ea1177afb0f4a840efe81e6acdf62f2bd2a41d7da03032abe733a8e`,
and the campaign recorded zero evaluation artifacts read outside that
content-free boundary.

## Interpretation and next action

V5 materially improved recorded construction yield over V4, from 5/60 to
29/60, and removed unresolved infrastructure outcomes. It still missed the
predeclared 54/60 threshold by 25 admissions. The concentration is diagnostic:
Python passed 10/10 while JavaScript and Rust passed 1/10 each because the
test-author validator and canonical staging contract were not aligned with
authored suite paths and imports. The executed evidence does not show a bad
reference among the 31 rejects.

Do not generate V5 reserves, promote the 29 rows as a qualified full repair
surface, start main training from this result, or make a public-release claim.
Any successor must be a new prospective contract. It must make test paths
controller-owned, replace syntax heuristics with the exact executable outcome
matrix, and prove final canonical staging before another complete 60-cell
campaign. The adopted successor is
`docs/plans/GATE2_REPAIR_DELTA_V6_CANONICAL_TEST_REPLAY_PLAN_20260917.md`,
file SHA-256
`4fe6a1374c01a0a682bf256c91a141b36b26680bdb5279049070f4f143418ec1`.
Relabeling or rerunning V5 is forbidden.
