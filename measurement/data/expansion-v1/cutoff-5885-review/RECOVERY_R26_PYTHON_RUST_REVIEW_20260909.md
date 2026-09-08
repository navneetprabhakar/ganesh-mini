# R26 Python/Rust independent static quality review — 2026-09-09

Gate 2 remains open. This report reviews exactly the six Python and four Rust
test-correction candidates in R26. It is a static review of frozen artifacts:
no generated candidate or test was executed, no candidate was edited, no row
was admitted, and no cloud resource was inspected or changed.

## Result

**Nine unconditional static positives and one hold.** All six Python
candidates and Rust generation-0595, 0606 and 0634 satisfy the seven static
criteria and their explicit R26 correction scopes. Rust generation-0635 is
held because the suite still lacks the requested endpoint duplicate-before-
null-conversion witness. A static positive is not an admission and still needs
main-owned pinned sandbox directionality and final separation/admission.

| Candidate suffix | Immutable correction | Static decision | Exact reason |
| --- | --- | --- | --- |
| Python generation-0047 | Valid | Positive | List and dictionary IDs are used for both change and remove after a valid operation; each must raise `ValueError`, and caller records/operations are compared unchanged. |
| Python generation-0130 | Valid | Positive | List and dictionary `event_code` values are tested after a valid reservation; both require `ValueError` with unchanged caller input. |
| Python generation-0143 | Valid | Positive | Tuple fallback assertions are removed; list-normalized and tuple-scalar keys are proven independent; absent empty add creates an empty bucket and marks dirty, while later `add_empty` is false without new dirtiness. |
| Python generation-0153 | Valid | Positive | Both insertion orders of one valid string key and one integer asset key require `ValueError`, preventing incidental sort-order `TypeError`; ownership and ordering coverage remains. |
| Python generation-0588 | Valid | Positive | List/dictionary operation discriminators require `ValueError`; an aliased book under two IDs proves moving one detaches it without changing the other alias or caller inputs. |
| Python generation-0738 | Valid | Positive | One shared account dictionary under two keys is updated through one key only; the selected object is the returned object, while the other key and caller object remain unchanged and detached. |
| Rust generation-0595 | Valid | Positive | Exact-decoding controls cover NUL, backspace, form-feed and U+001F across string lists, string maps and list maps. The test-only canonicalizer accepts equivalent valid short/Unicode escape spellings while preserving decoded identity. |
| Rust generation-0606 | Valid | Positive | Exact-decoding checks place NUL in a document name, backspace in a key and form-feed in a value, accepting equivalent valid JSON escapes and rejecting the incomplete control encoder. |
| Rust generation-0634 | Valid | Positive | Command-position `--unknown` is checked both first and after a valid workspace pair as `Unexpected`; an ordinary unknown command remains `UnknownCommand`. |
| Rust generation-0635 | Valid binding; incomplete test correction | **Hold** | The priority, reverse-order and null-allowed cases are corrected, unsupported index-base assertions are removed, and earlier errors now outrank later duplicates. However, the explicit “duplicates fail before value conversion” endpoint/null edge remains absent: `endpoint=x;endpoint=null` should return `DuplicateKey("endpoint")`. The added `endpoint=null;endpoint=x` under strict settings returns immediately at the first segment and never reaches a duplicate, so it is not that control. Pool/tracing duplicate tests do not establish ordering for endpoint's special null conversion. |

## Immutable bindings and source scope

All ten R26 canonical records bind to the exact R24 canonical candidate hash
named by `recovery-feedback-r26.json`. For every record, the R26 problem,
assistant/reference bytes and known-bad bytes equal R24 byte-for-byte; the
behavioral test is the only substantive payload change. IDs, task IDs, lanes,
task types, prompt/reference copies inside the verification task, rights and
all stored content hashes reproduce. The R26 source object equals the planned
original-parent source plus the exact versioned-recovery transformation naming
the R26 ID, original parent ID and original parent canonical hash.

The ten original parents were independently recovered from
`datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`; their
canonical hashes equal the R26 plan's `parent_candidate_sha256` values. Their
problems equal the R26 prompts. All use McEval-Instruct revision
`57bd46727e49ac3e2890218a146d35c2454a8496`, CC-BY-SA-4.0, and all five
rights flags are true. The transformed specifications remain self-contained
and source-inspired only; no source answer or source test entered the emitted
prompt/reference/test contract.

The Python and Rust correction calls each returned code zero, did not time out,
have no event parse error, and list no disallowed tool item types. Their final
structured outputs contain exactly the expected six and four IDs respectively,
and every `test_code` is byte-identical to the corresponding stored R26 test.

## Evaluation separation

A read-only reconstruction of `scripts.data.admit_expansion.evaluation_index`
over `eval/` validated and indexed **546 evaluation task files**. Using the
frozen cutoff deduplication settings (minimum 12 tokens; SimHash Hamming limit
3), all ten candidates have:

- zero normalized exact prompt overlaps;
- zero qualifying fuzzy prompt overlaps;
- zero exact reference-code overlaps; and
- zero exact known-bad or behavioral-test overlaps.

This establishes static separation for the reviewed payloads. It does not
replace the admission tool's later sealed separation and execution pass.

## Seven-criterion adjudication

The criteria are prompt clarity, API consistency, independent test origin,
whole-target non-triviality, idiomatic reference implementation, dependency
isolation, and realistic known-bad discrimination.

### Python generation-0047 — positive

The record/operation API and error/atomicity contract are explicit. Registry ID
validation, create/change/remove behavior, ordering and nonmutation make the
target substantive without external dependencies. The reference validates
hashability through membership under its `ValueError` boundary and copies
records before mutation. The corrected matrix covers both operations, both
unhashable shapes and state after a valid operation, directly distinguishing
the realistic leaked-`TypeError` mutant.

### Python generation-0130 — positive

The inventory/reservation API is coherent and the contract clearly separates
malformed events, availability, conflicts and atomic ownership. The idiomatic
reference performs validation before copying and applying reservations. The
new list/dictionary event-code cases occur after a valid reservation and check
both exception class and unchanged input, closing the only identified oracle
gap against a realistic hashability mutant.

### Python generation-0143 — positive

The relation-store API precisely defines normalization, empty-bucket creation,
dirty state and copy isolation. The corrected assertions now follow that
contract: list keys normalize to set-derived tuples while tuple inputs remain
scalar keys, and empty add behavior distinguishes bucket creation from element
change. The reference is compact, idiomatic and standard-library-only; the
corrected suite retains broad lifecycle and ownership checks while removing
the unsupported tuple fallback.

### Python generation-0153 — positive

The manifest compiler has a clear mapping API, canonical path rules, collision
semantics, deterministic output and ownership requirements. The reference
validates all key/value shapes before sorting and copies returned structures.
Both mixed-key insertion orders now require the declared `ValueError`, so test
success cannot depend on Python's attempt to compare `str` and `int`. Existing
mapping, collision, ordering, identity and nonmutation checks remain intact.

### Python generation-0588 — positive

The catalog operation grammar, referential constraints and all-or-nothing
semantics are explicit. The reference deep-copies inputs before processing and
validates unhashable operation discriminators under `ValueError`. The corrected
suite adds both malformed discriminator shapes and a decisive shared-object
alias witness. It therefore covers the named error-normalization and shallow-
copy defects while retaining valid sequencing and rollback coverage.

### Python generation-0738 — positive

The directory/account API clearly defines canonical email handling, selected
object identity, detachment and input preservation. The reference validates
the whole directory, deep-copies it and returns the selected value from that
copy. The new two-key shared-dictionary witness proves both per-key isolation
and caller detachment after one update, directly discriminating a realistic
shallow-copy implementation.

### Rust generation-0595 — positive

The graph renderer exposes three related APIs with explicit locator and compact
JSON behavior, providing substantial nested behavior under the standard
library. The reference's encoder handles every U+0000..U+001F character. The
new test-only decoder/canonicalizer is bounded to the supplied JSON shapes and
normalizes valid escape alternatives; raw controls emitted by the known-bad
encoder remain different from the expected escaped canonical form. NUL,
backspace, form-feed and U+001F appear across every rendering API, closing the
selected discrimination gap.

### Rust generation-0606 — positive

The document compiler combines line parsing, replacement, sorting, u64 parsing,
nested JSON output and ownership into a coherent non-trivial target. The
reference has complete JSON control escaping. The corrected document puts the
three selected controls in distinct structural positions and compares decoded-
equivalent canonical JSON, avoiding an overfit to one legal escape spelling
while rejecting the realistic incomplete encoder.

### Rust generation-0634 — positive

The invocation parser specifies global/local option placement, five command
grammars, duplicate flags, repeated tags and operand rules. The reference's
command-position option guard is an idiomatic minimal correction. The new
start-position and post-workspace `--unknown` cases exercise that exact branch,
while the retained ordinary word verifies the separate `UnknownCommand`
classification. The known-bad parser is decisively and realistically covered.

### Rust generation-0635 — hold

The settings parser remains clear, API-consistent, substantive, idiomatic and
standard-library-only. Its immediate null rejection correctly implements the
left-to-right rule, and the deferred-null mutant is now decisively rejected by
`endpoint=null;tracing=bad`. Reverse-order and null-allowed cases correctly
bound that priority. The corrected suite also removes the unsupported numeric
segment-index oracle and fixes the former global duplicate-pre-scan mistake.

Test quality is nevertheless incomplete against the frozen correction request.
Endpoint has special value conversion (`null`), and the contract explicitly
says duplicates fail before conversion. Neither `endpoint=x;endpoint=null` nor
an equivalent repeated-endpoint special-value case exists. The present strict
`endpoint=null;endpoint=x` assertion terminates on the first null and cannot
observe duplicate handling. This leaves a realistic alternate implementation
that checks the second endpoint's null value before its duplicate identity
unrejected. Add the exact witness expecting `DuplicateKey("endpoint")`; do not
change the frozen specification, reference or known-bad bytes.

## Exact evidence hashes

- R26 request: `1dc3ec0d046bc5beca47b72d2a5c3d37cd1e2cf86f39c275947b445622000677`.
- R26 feedback: `dc8ecab5c4911bc85b92f90d1392af7db49750e1dc080fdeb9f8345367bb4dc7`.
- R26 plan raw file (both copies): `48d7a05990b0882f209c78a0942b8e21ae44a103e1cad192241ec33c6c8d4071`.
- R26 logical plan: `11dce4e35cb0afa717cc966b9540f541caf5f6258b967f260ade7131df0f0293`.
- Parent corpus: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
- Hold ledger: `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.
- R26 run contract: `bd94fcb8b81d1efb14380d496d5f5dcdc8715c3b47678d1865e2488c3b8c9448`.
- R26 generation registry: `2045083c185c671803a717a81df41eeb8edd176523a3736401455a4a59330478`.
- R26 aggregate candidates file: `51eaef24706eb6031cd6205ef81b20f4509e2c624b9ccbbaa8f94240611b457c` (also the registry's candidate hash; 25 total records).
- R24 Python review: `a4d20728e8e3ba4a8902ca24a81e2b9b66f490479f71bd4aff48b892869e30fa`.
- R24 Rust review: `f48da5f2cca0c87ef3be62a37722b2f550461b9fd1335b51288637be8aacae4d`.
- Python correction evidence raw/prompt/final-output:
  `b70b299260bdc7a82c37f63e8e933134a9c13f7eb10e3d22f08ab2fd3c85463c`,
  `402286651b36f6f86fe31f05f10fa11494092e8ab2deacb64bfd3b3e36452cbe`,
  `b6af17adc9a5f5a001d76e000e22857049471e061e8d5da1cd365045471cef05`.
- Rust correction evidence raw/prompt/final-output:
  `706e0c90e034f6099d9e360525f1e61436512b23b50a838ead01b911da9481ca`,
  `c258c025256878f58d833ef39b29f0f270c12ebfae7554db8a8517b43b0b57cd`,
  `b8695bfcd1b9f48c789007aac99f93247bf6447c6e525e750eeca87bc7c4a1b0`.

Candidate bindings below give raw candidate-file SHA, canonical R26 record SHA,
canonical R24 record SHA named by feedback, original-parent canonical SHA, and
the corrected test SHA. Each stored test hash reproduces from its content.

| Suffix | R26 file SHA | R26 canonical | R24 canonical | Original parent canonical | Corrected test SHA |
| --- | --- | --- | --- | --- | --- |
| py-0047 | `2ee06b1d01b7799cf3a55a8cb7ff5a3728b9dab003e20b9b05ff6ad0665259d1` | `5515535b9f3f300fc7b1c46ac6e64d384e0c3c11d7a8f21d9d1d48bec0cd8f0a` | `7bd74105bcb392a9056d746aff9eb4a48fcfffaf5b36b3bc6b2c824d19193953` | `2cb4ead62e781964c6e88bddaf9b8fb1715a12462cf54b85b15971177469a32d` | `c5a7f30d62b7dfb52e98ab41d636d25fb74e50d23a6618db20e386483aa1846d` |
| py-0130 | `ce3db0dc8e5538616e8c5d718eb074d3bee041661ce8ed40ed227c5b64ab6c86` | `74d5eed5725adf03cb46034ee5dfa52fde2465179b3532690d3276c635b5f357` | `185cd41a212994e335e36c1342234022d075b310d2e7ccc81de83f3021b91430` | `167118c9169c84eef1c6639a2dca6da947188164e24dc42f821bac7413591faa` | `5744d048e83187625e876c313782fd188cfbba10435db4fb4059c71cbe9502c4` |
| py-0143 | `4e971869a697c35ff8f10c3f455e3eef490914b79ce51ffa12f10d36c8ec3e52` | `b9ac4e4336fa158c012d65757fde8780b4e6d80235f6520a5a576d4a3cdcd7ac` | `1a0e498f636db06c16978c50749ea6ab9315871f1b8abe96554fc6360102166a` | `fe8de50d87bfa45afc0930c7ebc31f161fc235701345dc539925c5ab3230cc76` | `a55df015a283668f1e66687b69ef0ad249f40f0ee122276d32e289ceef3af075` |
| py-0153 | `e9b0cfecc150a325bb5a5e46b6fe4d64dde81beeeb1fad66b6dc26cc335633f7` | `17a42a9403c09eb099cb606c44ce6d018eccba5fd5d6087a3fd0173279bfead4` | `b4a224768b890f77644293bd3953ca7669067fd663d9ed7712c27d127e294ae2` | `cfc2316132c8a8c1aaf44d55f7fb35c230384ef0e97262ad362d14101870c4a8` | `5d704010a8082962c1eff9177be1e0701e08397f935309c91b5ecd0ef492239e` |
| py-0588 | `6d43bae5c9a1eebbe8e116da9928da7256b4883ce07bae9195962811af7705e5` | `1a5acd47e936294530a99b06dc531a02013d77a6b097709c02de6cd6f819313c` | `79838f3e2ae2b11fcaf4ed321ae63b60a38d65d7cfbabe7e37b3c923ec25b319` | `ca29b3df2e7307a0f1ca72e4e4e57f89a9dcb8f0b589ae4c223bdae3f7b95fef` | `011142ba157573473857877b5f5c3019d75246fe5fd4976ef890101c9dc90175` |
| py-0738 | `409031d8603beeea43c845611189fac7b3c7b11c1799c7c9cccdba1adcba5174` | `bb76beea4ac709fc29549daf658e39bd048318b53f5c391744787cd3bdfbff9b` | `0b8d5e705958dd7b1e1a8737020ce49e7492e8b3fae53f18a0389f30b1302a6d` | `e23b7270f5b8e9988a062f204d40dae6d70a02e52b2f77b88bae0b6862b8c3e5` | `7d42aace4254be0c9824938c2b1993d8beaabd4c56274aff93a5f11e8578aa8e` |
| rs-0595 | `60de5a72c1e1b4ed716ce37bf51797290cb9bb6a35fd322b513e36e3ffa94840` | `b5c6dd37b528f3983b82bfb38ac3d829f51fc50965f3f9d489158ae4ae5610fb` | `a71ceaab3865375eee512930409e96f063a1e1abcf9485a96de0bad1326f73eb` | `f3f8b4a41e9eaf9b22b1f99acd3e6959b113ab521f44623d200e30fada2af351` | `feb4836f9e12f97f9102f702c58686dbea77d2c0b4e4b734bd7b591258d58b3e` |
| rs-0606 | `dba7859440665aa02df40f7179bc80122207dcceeacbc030f20d253f9a14989a` | `65082c67ab064796ae44d3dcb0f74abef019445dbca3796e63e8026bbabde44b` | `c5b513761b3caafb0238289feb0f886fdcf0c75bae98786814c91a00b7db55da` | `a6e10b1e0e7f74755c3681f5b12cfa5a3cc290aefa8d1fe6e0c25854bb5e5bd3` | `54187a0295c5d7a24391175902c341f6b1599d510d9ec5e372d0adde718da589` |
| rs-0634 | `751a577547b5d958bc8bc4800bd3d53db611a305b74337f41f6804b118f0190c` | `32f46c46e1ebcae55c30ebd2f4cc841ee8b236605ba5ae3812133828757d2d3f` | `c99b04318ef656bafaaefacaee820bfe491e40139c3ffca43a88b88a775bb59f` | `fc7ad7656ace9381dfd98259e12a29b9c7505aee600251e637aa771ce6d9c8fb` | `8bbfb38da0f49f935d8f44301f4c9a16026c238db9fb481cee28a5bc5536f189` |
| rs-0635 | `9533be5ed9da16410901f6adc7514c7522b0cecb0518ba4e21d5282701b8f337` | `a502e06a17523bae908f14f7b41147d1ff7c55df952b2b90e911c3636b6997a1` | `9b57ec9845692379e6b367999c064a38601915fc146f83fef07543e8bf13bc09` | `08d9c25271dc3f0bcbc500625ba16b06e094c8f578a434799f5da6484e329fc9` | `a50fb9ffecdae063a6b5ef4200fb9cf9d1fd53089302cb5665761954dd2ec48d` |

Reference and known-bad hashes, reproduced from UTF-8 content:

| Suffix | Reference SHA | Known-bad SHA |
| --- | --- | --- |
| py-0047 | `eebb8b2927d58c990f8727147924fd744e2ec53fc174ce88bf69c71285d90f94` | `e90e60a7da71a87aff54d21c0e8bf4bf6863a74726aa59af962ae65588e23674` |
| py-0130 | `a143220da0fccc9d880f77b887886e4347e080934859163e672688690c4a53f8` | `e23a6f2c4ccd553132e395fe0c6c4799e3423e84458065dfbebcad67b8fb690b` |
| py-0143 | `d2a7438d9c9674d27c7def3302662482878e852b9dddaaa15611c954d9b2b243` | `11d205fa55d32730ef1ca228af1696f3a9858e0886444f5fef52c10004d83521` |
| py-0153 | `f5bdfb9c4c4147af970b9a9d1fc1838e7e09f171d5d36641e0d0df558e8e7286` | `b6f08ce6fcffe4cc3af3484bf3c54c11228820f097aa5c3bf87e76882c5de3ae` |
| py-0588 | `1eeaed8cf240f8b6cd15584b635cd66b3b379c352e490b0f54a131cdb9e25f3e` | `4bbc6639ad9e76b912b89d1e0c2117c4f1a8a15e6ee3ec9386f7e839dccf643b` |
| py-0738 | `77720c48593760cd822b228752d57315cc5975367a59f3f2d3a8a56461873ae3` | `69a358e79d9e0255ba5b6e55e568c3a5a5afc099e4048438f8ae2e582da43ae2` |
| rs-0595 | `093400aa498d4e83ad4dddd65be9c48fc552069d4d8b9cd0972cc2387e395607` | `bbf04444ff8f1a3d08d914ba434348f7fd5a80ec421f69500c2dade0f310b6d7` |
| rs-0606 | `44557f2618c9f8d086d07f525deec58d2baf1095cb76a3a03d605c9d72b0ab5e` | `45691d49f78917587298dcf7945a262459441f021415e7c3ef0e12f5aede4156` |
| rs-0634 | `687eb2fde6d0902dde7c71c4c8cfc57506ffbf2301e59df2d9fccd6bdc7c5da9` | `14646d276395d2924f54bf83c138a97b63bd9cb919fe36ebb8fd3ae81ff2cb58` |
| rs-0635 | `c95523edb57431f4c9a5dffcedcb2941d0016f05234832efa40c011dd8f24149` | `20389ec9af36de68c053b00af30d33479e1a9a17179d23cd864f332329c4eb9c` |

## Handoff

Main may advance the nine unconditional positives to pinned, resource-limited,
network-disabled reference/known-bad/original directionality and then sealed
separation/admission. Rust generation-0635 must remain outside admission until
a new bounded test-only correction adds the endpoint duplicate-before-null
conversion witness and receives another independent review. This report does
not admit any record. The finalized raw-file SHA-256 is reported externally in
the reviewer handoff because a file cannot contain its own full-file digest.
