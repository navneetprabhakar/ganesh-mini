# R24 Rust independent static quality review — 2026-09-09

Gate 2. Exactly six R24 Rust generation candidates were reviewed against the
complete request, plan, run contract, original parents and holds, architect
output, independent-test output, emitted problems, references, mutants and
tests. This is static evidence only: no generated code was executed, no
candidate was changed, and no admission or cloud action occurred.

## Result

**Zero unconditional static positives; six holds.** Every independent suite
omits the exact recovery witness selected for its parent. Generation-0465 and
0553 additionally have a static reference-compilation defect. Generation-0635
also contains independent-test expectations that conflict with its emitted
reference and are not fixed by the stated contract. Original parent holds
remain unchanged.

| Candidate suffix | Reference | Independent tests | Overall |
| --- | --- | --- | --- |
| generation-0465 | Hold: incorrect predicate function type for `trim_matches` | Hold: no U+2003 field/capability witness | Hold |
| generation-0553 | Hold: incorrect predicate function type for `trim_matches` | Hold: no U+2003 repository/authorization witness | Hold |
| generation-0595 | Positive statically | Hold: no NUL/backspace/form-feed/other-control witness | Hold |
| generation-0606 | Positive statically | Hold: no NUL/backspace/form-feed witness | Hold |
| generation-0634 | Positive statically | Hold: no command-position `--unknown` witness | Hold |
| generation-0635 | Positive statically | Hold: defining priority witness absent; unsupported/inconsistent error oracles | Hold |

## Immutable lineage and independent author

All six planned parent canonical hashes reproduce exactly. Candidate IDs,
lanes and task types match the plan. Every candidate problem equals its
reference-fix parent problem byte-for-byte. Rights objects equal the parents,
and source objects equal the parent source plus only the exact versioned
recovery transformation suffix. Architect output problem/reference/mutant
fields equal the candidates; independent-author output equals each stored test
after the generator's documented strip-plus-newline normalization. Stored
reference, mutant and test hashes reproduce from their UTF-8 content.

Both teacher calls returned zero, did not time out, have no event parse error
and list no disallowed tool item types. The independent author received IDs and
complete specifications, not references, mutants, source tests or architect
context. All six retain McEval-Instruct revision
`57bd46727e49ac3e2890218a146d35c2454a8496`, CC-BY-SA-4.0, with all five
rights flags true.

The parent corpus SHA-256 is
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`;
the frozen hold-ledger SHA-256 is
`9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.
No prompt-scope drift was found: all six are reference-fix records and their
problems are exact parent copies.

## Seven-criterion adjudication

The seven criteria are prompt clarity, API consistency, independent test
origin, whole-target non-triviality, idiomatic reference implementation,
dependency isolation, and realistic known-bad discrimination. A static
positive would still require main's pinned sandbox directionality,
deduplication and evaluation-separation checks.

### generation-0465 — hold

The catalog/factory contract is clear and API-consistent; record parsing,
duplicate domains, descriptor ownership and independent serial state make the
whole target substantive. Test provenance and standard-library isolation are
positive, and Unicode trimming is a realistic defect.

The reference is not valid idiomatic Rust under the pinned toolchain: it passes
`char::is_ascii_whitespace` directly to `str::trim_matches`, whose predicate
must accept a `char`, while the method has signature `fn(&char) -> bool` (the
local Rust 1.96.1 core source declares it at `char/methods.rs:1978`). The
required form is a closure such as `|c: char| c.is_ascii_whitespace()`. This is
a static compilation hold, not an executed result. The tests also contain no
U+2003 around ID/title/revision, no U+2003-only capability and no distinction
between `read` and U+2003+`read`; the supplied Unicode-`trim` mutant can satisfy
the suite. Do not add private serial-state or overflow probes.

### generation-0553 — hold

The normalization/policy/decision chain is clear, API-consistent, substantive
and dependency-isolated. The Unicode-trimming mutant is realistic, and the
tests cover ordinary ASCII aliases, invalid shapes, organization/repository
authorization and Once/Remember/Reject mutation behavior.

The emitted reference repeats the same uncompilable direct
`trim_matches(char::is_ascii_whitespace)` use for the full input and both
components. Separately, the suite never tests U+2003-prefixed `Org/Repo`, its
literal normalized identity, non-authorization by an `org/repo` policy, or
Remember versus Once for that distinct identity. The internal `ÄBC/RÉPO`
case-conversion check is not a Unicode-whitespace boundary and does not
distinguish the mutant.

### generation-0595 — hold

Clarity/API, graph behavior, locator grammar, nested rendering, whole-target
substance, standard-library isolation and reference idiom are positive. The
reference correctly emits short escapes for backspace/form-feed and `\u00xx`
for other U+0000..U+001F controls. The mutant is a realistic incomplete JSON
string encoder.

The tests exercise only quote, backslash, newline, carriage return and tab—the
same cases implemented by the mutant. They never place NUL, backspace,
form-feed or another unnamed control in a list value, string-map key/value, or
list-map key/nested value. Therefore they neither establish valid compact JSON
nor preservation of exact decoded strings for the selected defect; the mutant
can pass. Equivalent valid short and Unicode escapes should remain acceptable.

### generation-0606 — hold

The nested document compiler, entry grammar, duplicate replacement, sorting,
u64 parsing and ownership form a substantive, coherent standard-library target.
The reference's complete JSON control escaping is statically positive, and the
mutant is realistic.

The suite's JSON fixture contains quote, backslash, newline, carriage return
and tab only, all already handled by the mutant. It omits the selected tiny
document named `doc`+NUL with backspace in a key and form-feed in a value, or
equivalent exact-decoding checks. Thus realistic mutant discrimination is not
established. The existing exact output assertion is acceptable only for the
explicitly specified common escapes; new control witnesses must allow
equivalent valid JSON escape spellings and prove values were not dropped.

### generation-0634 — hold

The five-command parser has clear declared types, stateful global/local option
placement, duplicate flags, repeated tags and command-specific operands. The
reference's command-position `--` guard is a minimal, idiomatic standard-library
fix, and the mutant is realistic. Existing tests cover broad ordinary grammar
and misplaced options inside commands.

No test calls `parse_invocation(&["--unknown"])` or repeats that call after a
valid `--workspace VALUE` pair. The only unknown option is after `send`, where
both reference and mutant return `Unexpected`; the ordinary `launch` case
correctly expects `UnknownCommand` from both. The defining command-position
classification is therefore untested and the mutant can pass.

### generation-0635 — hold

The typed settings parser is clear and substantive, with interacting flags,
left-to-right segments, duplicate priority, defaults and value domains. The
reference's immediate `NullEndpoint` return is a reasonable standard-library
implementation of the selected rule, and the deferred-null mutant is realistic.

The suite checks `endpoint=null` only in isolation, where both reference and
mutant return `NullEndpoint`. It omits `endpoint=null;tracing=bad` under both
`allow_missing_required` settings, the reverse-order control, null-allowed
continuation, duplicate endpoint-before-null conversion and later malformed or
unknown segments. The mutant can therefore pass the selected behavior.

Two additional test oracles prevent even reference qualification. Empty
segments are expected at one-based positions, while the emitted reference uses
the zero-based `enumerate()` index and the specification never declares an
index base. The suite also expects a later duplicate to outrank an invalid
value in an earlier segment (`pool_size=bad;pool_size=3` and the tracing
equivalent), while the stated left-to-right first-error contract and emitted
reference return the earlier `InvalidValue`. “Duplicates fail before value
conversion” supports checking a duplicate segment's key before converting that
same segment; it does not authorize a global key pre-scan over later segments.
These unsupported expectations must be removed or the contract explicitly
changed before any corrected suite is frozen.

## Exact evidence bindings

Raw file SHA-256 values:

- R24 plan: `1f89608807b00559e993952c6d0a1936baccae882322c3315ae7efe3dd37d9fb`.
- R24 run contract: `a455daccb7e85a30c3cc86d4c328ee44be8e6fd166afef6fe685bba9c8225be4`.
- R24 request: `2e881ce718f8509655f0a894daddc305c869bc787deb6672a9b68d6e0d416451`.
- Approved selection report: `d9c169ff6b54494708893a8028d7019e6ec6688499da24822a330b39ad51e349`.
- Rust architect evidence: `d6bb6d0dc228811c4b720812a2863a926bd6f204e2b1a4fd764f43044d4e7ae1`;
  prompt `3ac0928d175d36bd27457febe76173451535523b3f90f3673b363054213576e0`;
  final output `1cbdf55e792a845aa6b6abb544c6f27eeadd72c41b95b20d76168bcb9fd08000`.
- Rust independent-test evidence: `0a7f7653ee9250995dd363fa11d5b4e8daffeb45402bda8c193ac53aac8d5045`;
  prompt `6d39e5ae5c680c8004cc4cdc3d9ca02a6ae90202b0fa7d3873fb39769b0f83bb`;
  final output `d9bf0a9c5959c753b9e3e907110f820c1c0b2468fba6736a3517a12770863a7c`.

Candidate raw-file, canonical-candidate and parent-canonical hashes:

| Suffix | File SHA-256 | Canonical candidate SHA-256 | Parent canonical SHA-256 |
| --- | --- | --- | --- |
| generation-0465 | `701d272870eca7e9ba70a342cfbb509c0ea777732b69973f3af73dc9b75c27e0` | `00e3b6bd41a013bb38d7ea769df91814ca4f0867181d04c30dcdacd926f9ba53` | `b173a6e93f316bebe8bf35cd4a78ce9823c8cee54bff10c80fd177d5341902b4` |
| generation-0553 | `8ae6eb780f0ec8d8551c943b9cc6a185d66d944acef17167230f9e93bc3d880b` | `29f5837323bd662bd5583c06191e416338b534d30b5c14cf15317fb5ae620c65` | `31a9d66e2b3e01423477aba5a5caba8d2bd3d34092a03b0b5886224b3dff009e` |
| generation-0595 | `22a5eb7bea810ba79589a7e19c61871e1b86c922b3ae9af674eff62623220502` | `a71ceaab3865375eee512930409e96f063a1e1abcf9485a96de0bad1326f73eb` | `f3f8b4a41e9eaf9b22b1f99acd3e6959b113ab521f44623d200e30fada2af351` |
| generation-0606 | `491a10295e863b9b43052a9b9331c2dc1a74876626b36272fc015ab257561d0b` | `c5b513761b3caafb0238289feb0f886fdcf0c75bae98786814c91a00b7db55da` | `a6e10b1e0e7f74755c3681f5b12cfa5a3cc290aefa8d1fe6e0c25854bb5e5bd3` |
| generation-0634 | `56f97280191f02ebd0d2b4b14abe9e05c8d0e86cf1c17818de679154f7c17e32` | `c99b04318ef656bafaaefacaee820bfe491e40139c3ffca43a88b88a775bb59f` | `fc7ad7656ace9381dfd98259e12a29b9c7505aee600251e637aa771ce6d9c8fb` |
| generation-0635 | `b5ecbadb9b49a5b189a33b4770a10affb55a7f647dc2736e405c71d8cbfcbbc2` | `9b57ec9845692379e6b367999c064a38601915fc146f83fef07543e8bf13bc09` | `08d9c25271dc3f0bcbc500625ba16b06e094c8f578a434799f5da6484e329fc9` |

Canonical parent-hold and raw held-evidence hashes:

| Suffix | Hold-object SHA-256 | Evidence-file SHA-256 |
| --- | --- | --- |
| generation-0465 | `0b627d1878dc23a0fa4dc0fc98900ab6b5026d163f185e8677c33e2a5d3372e0` | `edf21f1d20bce0faae2d4cb8443b08bf376d4043d824f5a116946ae25d5db281` |
| generation-0553 | `140eeca030d10486548bfdc7383260279beec824b74f52f8d6c8d2f81e7e195a` | `be002053a57922f019b5ffe7735488bf6fa1be029a795419afaba9009e5bfe26` |
| generation-0595 | `b169fb62c4f39ef5f4b237aa83cb4e3a73231180811748b80f9c97c780750b69` | `f5552c33da03790a8d67a5ecd85b56fbff77290310c65a8068b12a9c7e22db53` |
| generation-0606 | `0f0203c7271f7ee1b62ef078c3185c3a5e9b30645747bcc497be0213c65443e9` | `8f48641817d98f67eb8bb78c09469fbbc98f49f2365373761433193f9d8987f2` |
| generation-0634 | `e9e459eb52a54709a21a22e2de3412eab43f0f1e6d22e010eabeaa3c56957867` | `965ac51feb7cf3d31c9145b8f5336a93684acaf345ad373433e25861e83e2577` |
| generation-0635 | `5b963fe75bf8af687514f9c2f7fdf339fc24cac69bc1c4af109ceeb58cb4615e` | `56e1513242dd91b5d6f2b02be82ee2bdfcabf7cc47d32925e470a45608381960` |

## Handoff

None of the six exact R24 Rust artifacts should enter admission. A bounded new
reference-and-test version is required for 0465/0553. A single bounded
test-only correction may address 0595/0606/0634. Candidate 0635 needs a
test-only correction that both adds the selected priority controls and removes
the unsupported segment-index/global-duplicate oracles; its reference may stay
unchanged. Main owns any correction authorization and subsequent execution,
separation and admission decisions. This report is not admission.
