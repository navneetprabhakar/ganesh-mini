# R24 Java independent static quality review — 2026-09-08

Gate 2. Exactly ten R24 Java candidates were reviewed against the complete
request, plan, run contract, original parents, held evidence, architect output,
independent-test output, emitted problems, references, mutants and tests. This
is static evidence only: no generated code was executed, no candidate was
changed, and no admission or cloud action occurred.

## Result

**One unconditional static positive and nine holds.** Generation-0512 is the
only unconditional positive. Generation-0123/0140/0196/0427/0513/0643 have
test-oracle or recovery-discrimination holds. Repair-0326/0328/0359 are
substantive reference-and-test positives, but all three exact artifacts exceed
their approved source-only/neutral-diagnosis prompt-edit scope and therefore
remain overall holds. Original parent holds remain unchanged.

| Candidate suffix | Seven-criterion result | Prompt scope | Overall |
| --- | --- | --- | --- |
| generation-0123 | Hold: defining NUL-pair collision absent | Exact parent problem | Hold |
| generation-0140 | Hold: opposite-sign finite maxima break the reference; extreme-average witnesses absent | Exact parent problem | Hold |
| generation-0196 | Hold: both overflow witnesses absent | Exact parent problem | Hold |
| generation-0427 | Hold: existing duplicate-list witness absent; unsupported element-identity assertions | Exact parent problem | Hold |
| generation-0512 | Positive | Exact parent problem | Positive |
| generation-0513 | Hold: hostile maximum count/length witnesses absent; unsupported deterministic-GZIP oracle | Exact parent problem | Hold |
| generation-0643 | Hold: tests call nonexistent `getMax()`; numeric witnesses absent; opposite-sign maxima break reference average | Exact parent problem | Hold |
| repair-0326 | Substantive positive | Hold: behavioral/implementation prose added | Hold |
| repair-0328 | Substantive positive | Hold: behavioral/implementation prose added | Hold |
| repair-0359 | Substantive positive | Hold: code-point behavioral prose added | Hold |

## Common immutable and author bindings

All ten planned parent canonical hashes reproduce exactly. Candidate IDs and
lanes match the plan. Parent rights objects are byte-equivalent as JSON, and
candidate source objects equal the parent source plus only the exact versioned
recovery transformation suffix. The seven generation problems equal their
parent problems byte-for-byte. Architect output problem/reference/mutant fields
equal the emitted candidates; independent-author output equals each emitted
test after the generator's documented strip-plus-newline normalization. Stored
reference, mutant and test hashes reproduce from their UTF-8 content.

Both teacher calls returned zero, did not time out, have no event parse error
and list no disallowed tool item types. The independent-author prompt contains
task IDs and complete derived specifications, not separate reference, mutant,
source-test or architect context. For repair records, the derived specification
necessarily embeds the complete proposed broken source, so this is
specification-origin independence rather than blindness to that embedded code.

The parent corpus SHA-256 is
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`;
the frozen hold ledger SHA-256 is
`9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.
All generation records retain McEval-Instruct CC-BY-SA-4.0 revision
`57bd46727e49ac3e2890218a146d35c2454a8496`; all repair records retain
MdEval-Instruct MIT revision
`38c9197e3add996fae624eb198ebd06155b2101e`. All five rights flags remain true.

## Seven-criterion adjudication

The seven criteria are prompt clarity, API consistency, independent test
origin, whole-target non-triviality, idiomatic reference implementation,
dependency isolation, and realistic known-bad discrimination. A positive here
is static and still requires main's pinned sandbox directionality, deduplication
and evaluation-separation checks.

### generation-0123 — hold

Clarity/API, independent origin, non-trivial invitation lifecycle, idiomatic
record-based collision-free reference and standard-library isolation are
positive. The delimiter-key mutant is realistic. The suite never creates the
required distinct unordered pairs `(a, b+NUL+c)` and `(a+NUL+b, c)`, so it does
not exercise the held collision and can allow the supplied mutant to pass.
Add the exact independent invitation/acceptance/clear controls without banning
interior NUL or changing normalization.

### generation-0140 — hold

Clarity/API, staged replacement, exact integer overflow, dependency isolation
and independent origin are positive. The online-average reference handles two
same-sign maxima, but it is not generally overflow-safe: after a first
`Double.MAX_VALUE`, adding `-Double.MAX_VALUE` evaluates `value - average` as
negative infinity and returns negative infinity instead of the representable
average zero. This is a static reference-correctness hold under the declared
finite-double domain and approved cancellation control. The tests contain no
`Double.MAX_VALUE` average at all; they omit positive maxima, negative maxima
and cancellation, so realistic mutant discrimination is also not established.
Do not introduce a private-capacity or arbitrary fraction bit-pattern oracle.

### generation-0196 — hold

The sink API, state transitions, atomic list validation, snapshots and close
behavior make a non-trivial standard-library target, and the long accumulator
and widened threshold are idiomatic. The supplied int-overflow mutant is
realistic. The tests stop at capacities five and two: neither capacity
`Integer.MAX_VALUE` threshold overflow nor buffered-weight overflow at
`Integer.MAX_VALUE - 1` is exercised. Both approved tiny physical witnesses are
required before discrimination is positive.

### generation-0427 — hold

The complete ledger is clear, API-consistent, substantive and isolated; the
global duplicate-ID check in the reference is straightforward and idiomatic.
The suite checks only duplicate insertion into an already valid list. It never
supplies an existing two-entry list whose IDs already collide to `find`, a
missing lookup, removal/update, grouping or aggregation, so it misses the exact
mutant defect. It also repeatedly requires unchanged immutable `Entry` objects
by Java reference identity (`==`), although the public contract requires values,
order and nonmutation rather than element identity. Use public fields for value
comparisons and add whole-input duplicate validation witnesses.

### generation-0512 — positive

All seven criteria are positive. The exact command grammar and UTF-16 behavior
are clear and API-consistent; ordered transforms plus unbounded decimal parsing
are substantive. The reference validates every decimal character while using a
bounded comparison against the current string length, avoiding integer parse
overflow without narrowing valid counts. It is standard-library-only and
idiomatic. The independent suite includes an arbitrarily long valid count,
leading zeros, UTF-16 truncation, ordered transforms, a `take:12x` case that is
validated after the numeric prefix already exceeds the short input, malformed
grammar and input-list preservation. The supplied `Integer.parseInt` mutant is
realistically and directly distinguished by the long valid-count case.

### generation-0513 — hold

The typed framing API, compression, codec failures, ownership and incremental
reference decoder are substantive, coherent, idiomatic and dependency-isolated.
The eager-allocation mutant is realistic. Tests exercise only count two and
length four truncation; they never use the bounded compressed frames containing
count `Integer.MAX_VALUE` or length `Integer.MAX_VALUE`, so the selected resource
defect is not discriminated. The suite additionally requires two independently
packed GZIP byte arrays to be identical, a canonical-compressed-byte promise the
specification does not make. Remove that oracle and add both maximum-field
truncation witnesses; later execution must classify resource failure honestly.

### generation-0643 — hold

The matrix/vector target is clear and non-trivial, and the reference uses
`Math.hypot` plus defensive deep copies with no external dependency. However
the problem explicitly names getters only for sorted vector and transpose; the
reference exposes `getMaximum()`, while the test calls nonexistent `getMax()`.
The suite therefore cannot compile against this emitted reference. It also
lacks `[1e200]`, `[1e-200]` and two-`Double.MAX_VALUE` witnesses, so neither
re-squared-hypot nor naive-average discrimination is established. Separately,
the same online mean formula returns an infinity rather than zero for opposing
finite maxima, a reference-correctness defect under the unrestricted finite
vector domain. Keep scalar observation aligned with the emitted API or the
specified `toString()` contract and replace the average with genuinely
overflow-safe arithmetic before adding the approved numeric boundaries.

### repair-0326 — substantive positive, prompt-scope hold

All seven substantive criteria are positive: the immutable tree/preorder API is
clear and non-trivial; element-wise validation/copying is idiomatic and isolated;
the suite uses valid `List.of()`/`List.of(left,right)`, right-branch traversal,
first-preorder duplicates, defensive copying and explicit null elements; the
`contains(null)` mutant is realistic and directly distinguished.

The approved oracle-rebuild scope nevertheless required preserving behavioral
prose/API exactly, replacing embedded source and neutralizing only the stale
first-child diagnosis. R24 additionally states that `List.of` inputs must not be
queried in a way that throws, which is new implementation-directed behavioral
prose. It therefore fails the same fail-closed source-only binding boundary used
for R22 repairs. This exact artifact is not an unconditional positive.

### repair-0328 — substantive positive, prompt-scope hold

All seven substantive criteria are positive. Tests cover multiple and empty
`List.of` handler lists, ordered exactly-once invocation, null results, full
prevalidation before callbacks, propagation and stopping after a thrown handler,
unrelated invalid entries and immutable snapshots. The copied-list reference is
idiomatic standard Java and the `contains(null)` mutant is realistic.

The emitted problem adds implementation-directed `List.of`/null-query prose and
an explicit validate-entire-list-before-invocation sentence beyond replacing
the embedded source and stale first-handler diagnosis. Those requirements agree
with the intended behavior but exceed the approved source-only edit operation.
The exact artifact remains held absent an explicit main scope disposition.

### repair-0359 — substantive positive, prompt-scope hold

All seven substantive criteria are positive. The reference validates identifiers
and boundaries by code point, retains exact case-sensitive search/comment/order
behavior and uses only ordinary Java APIs. The independent tests exercise a
supplementary U+10400 query and supplementary identifier characters adjoining
`foo`; the UTF-16-char mutant is realistic and directly distinguished. The
whole target remains identifier validation, token-boundary scanning, comments,
ordering and ownership rather than a padded one-line patch.

The approved request nevertheless labels this oracle-rebuild and says only the
embedded source/neutral diagnosis changes. R24 adds explicit code-point and
surrogate-pair behavioral prose and changes the boundary wording from characters
to code points. That is substantively appropriate to define the selected fix,
but it is not the frozen source-only edit that was authorized. Main must resolve
that contract contradiction explicitly; this review does not waive it.

## Exact evidence bindings

Raw file SHA-256 values:

- R24 plan: `1f89608807b00559e993952c6d0a1936baccae882322c3315ae7efe3dd37d9fb`.
- R24 run contract: `a455daccb7e85a30c3cc86d4c328ee44be8e6fd166afef6fe685bba9c8225be4`.
- R24 request: `2e881ce718f8509655f0a894daddc305c869bc787deb6672a9b68d6e0d416451`.
- Approved selection report: `b3a392016df6e9d2b8edf521cec466ad7d454c5753f3c4f735e77da51fcfb0f5`.
- Java architect evidence: `42fb8cf69bf0ee5a46de96f5da1be2ac5c4ce3e9f8dccc567b79c2f8a9b631b1`;
  prompt `9c3ed4b4e74229a6b33ece968c1a5b0e04ca7a8057331d021c35d29f9dd053ec`;
  final output `c72b8a7ddd322f456e3109b5a4de7b6a381b1aa22c3165b4e3ae603e54ccb598`.
- Java independent-test evidence: `602355c09917b2a735d4f43798fd15caa2c8fa0afb7f8a3c1fa2a864c706a143`;
  prompt `c5477502e5e3e4bd612ddfd963b362ce9305e2dc24f18ea616f940c198767d97`;
  final output `78dc84979cef4d23fca807825283168af16c9a4f57f77df4d4819d6354034f70`.

Candidate raw-file and canonical-JSON hashes:

| Suffix | File SHA-256 | Canonical JSON SHA-256 | Parent canonical SHA-256 |
| --- | --- | --- | --- |
| generation-0123 | `ed1b29f62249403ebd613bfe993ad46511d91aa68d0daa9e830e86a1dde470c7` | `a2f307ced55abd6f34f66084b17b0333f7eb2d1b7b035c65e0a41af8a1793b7b` | `8f23c06357bc9e5422f9849fcd12ee7764b3c71ddb90654d2fa9bf2fdbc11b2f` |
| generation-0140 | `1faa461f9de73792414997ac600e7bed236f4505dd5f16bd7db12d270d9a906c` | `4ceafdcdde2a82d5f717aef6de25492363d4065b57e3d84e88dfb3729db5d128` | `2031b142e7dae804a91e64da72e41708cb558ab54b6022e1422d5ff1a399b12e` |
| generation-0196 | `ac805745f7840da1e717a728234761abf3712fa5ce08eb19b37a9c67484c3b38` | `0e890f32f4cb595318043a89a7f4ce48d5e30cc0aaa4678cdc775b398c65d04c` | `cf7d82bbc4fc796c951fab429f522607eb8e0847c3a293b636c16d2c4d37b216` |
| generation-0427 | `f73680cb3d38d4dc11608de8a87318d5998bafeca334aba229279dbb958cb209` | `aa393a0f4ca6eb7558827a137ed852fc246408536f26a35272396b2937c7b6ef` | `0667dd7c4bd4913f0886ed1c031961871b89687065479ad125756b731a35ac7b` |
| generation-0512 | `8a1539331c0ec5f52139879a1b33947517e29baaa144cccad6e4c4daaff305cc` | `38aa8e7a1200ece461ad9f1c025f44a9e1dd9ee4f153f1d8005389eb6f61857e` | `a9a891a7be5be58373edc5504c9370876dc45f8c23718a4b80053e710af1d022` |
| generation-0513 | `acc54b276381b92873d2b033a17643dde3adc164b1d51d306e65bd9dca9993aa` | `7eb1d85bed548949d28ca7a8fb10a267cd03d8ea177b1dd34b29185d95e7e97e` | `79d21d7bc51051e5e40ecd5c20263a634bbc4752a9ea2d96600b29d4858696b6` |
| generation-0643 | `632c53c991c486e06a0a32c53e1c8f1eae91c825733c5d521ba9a2dcd322a218` | `15a08fbce4d1a848c5578ba31b58569f144092eb02a06503c856d1776598bbb4` | `841935ccc0374818e4da3a3700cd09caaecaf195925fedcc6bef5c958a0ea7cb` |
| repair-0326 | `077aeae6e00bf2fbf47cbaca74516b8d9b0852345d5ec073758c0277c75535a2` | `11f7d45ddbb43dbab42755d3ecbf1ce3fee07a9c28923a78b702d5600c1023b5` | `c1c90b1936ebc21d0f4209dfce3c51e6007cd57b48b59e037af6e89975e5b7ba` |
| repair-0328 | `e09812ecfecfd97dddbccb65e4cb11cbe7d486d1965f53e00061404ecc1b1c01` | `e0859f49ce5f579ea3f43183a412c3aaf25fe1b3ced31a17261d9a67b61fd3db` | `1b21652c330e32d28a910161952f672e7d9309d4ea46fc084bddc5550e91f0f2` |
| repair-0359 | `e6c9316f338ea5f86f6a359ff4a2cb31116d391a9a3910cd39f628b6d35c8c02` | `6150276ded930a38e1e1f41142487411115b8b98223fa478a248ae892ca2419e` | `5e1e5ac85bd3c5055185a1e9472b46e092dff0f9e1fa51d3d43a0a121b8462a1` |

## Handoff

Main may carry generation-0512 to pinned serial directionality and remaining
admission checks. The other nine exact artifacts must not be counted as static
quality positives. A single bounded test-only correction could address
generation-0123/0196/0427/0513 if main authorizes it under the frozen one-critic
rule. Generation-0140/0643 require reference as well as test correction in a
new version. The three repair prompt-scope holds cannot be cured by test-only
correction and require explicit scope disposition or a newly planned,
correctly bounded version. This report is not an admission decision.
