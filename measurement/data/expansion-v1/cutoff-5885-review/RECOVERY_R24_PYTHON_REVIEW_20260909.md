# R24 Python full quality review — 2026-09-09

Gate 2. Exactly seven R24 Python generation candidates were reviewed statically
in full: 0047, 0130, 0143, 0153, 0159, 0588 and 0738. The frozen plan and run
contract, complete candidate specifications/references/known-bad
implementations/tests, immutable parents, parent holds and batch-3 selection
evidence were read. No generated code was executed, no candidate was changed,
and no admission, correction, cloud action or original-review credit is claimed.

**Result: one static seven-criterion positive (0159) and six test-quality holds
(0047, 0130, 0143, 0153, 0588, 0738).** The six held references are statically
correct and remain within their approved reference-fix scopes, but their tests
do not distinguish the supplied realistic known-bad. Candidate 0143 additionally
contains test oracles that contradict the frozen specification and approved
selection: they preserve the old tuple-scalar fallback and incorrectly treat
creation of an empty absent bucket as leaving `dirty` false.

This report is static quality evidence only. It does not claim executed
directionality or admission. All original parent holds remain immutable.

## Per-candidate decisions

### exp-v1-recovery-r24-python-generation-0047 — test-only hold

The prompt and API are clear. Sequential add/change/remove behavior, exact
schemas, position preservation, validation, caller atomicity and deep ownership
form a substantive full target. The replacement reference validates change and
remove IDs as nonempty strings before dictionary membership and stays within the
approved scope. The known-bad is a realistic predecessor whose membership lookup
raises `TypeError` for an unhashable ID.

The independent suite checks malformed scalar ID `4`, missing IDs, ordered
interleavings, duplicate IDs, schemas and input/output isolation. It never uses
`id=[]` or `id={}` in a change or remove operation. A hashable integer is rejected
by both implementations before exposing the defect, so the known-bad remains
indistinguishable.

Minimal specification-only feedback: for both change and remove, use list and
dictionary IDs in otherwise exact operations and require `ValueError`. Include
each after a valid prior operation and compare both caller inputs after failure.
Retain order, remove-and-readd, duplicate/missing IDs and deep-copy controls.

### exp-v1-recovery-r24-python-generation-0130 — test-only hold

The two ordered projections, duplicate reservation preservation, complete event
labels, validation and deep ownership are substantive. The replacement reference
validates `event_code` as a nonempty string before membership and otherwise
preserves the original implementation. Python integers remain unbounded as the
contract requires. The unhashable-membership predecessor is realistic.

The suite covers output order, duplicate reservations, unreserved events, large
fees, allocation, malformed records and atomicity. Its only wrong-type event code
is integer `1`, which is hashable and therefore rejected by both reference and
known-bad as `ValueError`. It lacks list/dictionary event-code witnesses and does
not expose the held exception mismatch.

Minimal specification-only feedback: use `event_code=[]` and `event_code={}` in
otherwise valid reservations, require `ValueError`, and verify inputs remain
unchanged, including a later malformed reservation after a valid one. Preserve
the two ordering rules, duplicates, unreserved labels, large integers and fresh
projected rows.

### exp-v1-recovery-r24-python-generation-0143 — test-only hold with invalid oracles

The reference correctly implements the approved prompt reading. A tuple is one
hashable scalar, so it normalizes to a one-element tuple containing that tuple;
it must not fall back to the distinct normalized key produced from a list or
set. Also, `add(key, [])` on an absent key creates a bucket and sets `dirty=True`
but returns `False`, because creation occurred while membership did not change.
Stateful normalization, membership, dirty tracking, hashability, immutable
snapshots and deterministic rendering are substantive and standard-library only.

The independent tests directly contradict both requirements:

- after `add(["a", "b"], [1, 2])`, they expect `get(("a", "b"))` to retrieve
  the list-normalized bucket, preserving the supplied known-bad fallback;
- after `add("k", [])`, they expect `False` and `dirty=False`, then expect
  `add_empty("k")` to create the bucket, although the first call already created
  it under the frozen contract;
- the same tuple-fallback error recurs when a normalized set key is queried as
  its tuple representation.

The reference is not to be changed to accommodate these tests. A future test-only
version must assert that the list key and tuple-scalar key remain independently
addressable/removable, and must assert `add(absent, empty) == False`, `dirty is
True`, empty snapshot present, and subsequent `add_empty` returns `False` without
new state change. Preserve atomic unhashable failures, membership no-ops, frozen
snapshots and deterministic rendering. Do not invent ordering for equal `repr`
values.

### exp-v1-recovery-r24-python-generation-0153 — test-only hold

Route schema/order, cross-origin path and generated-name uniqueness, immutable
values, callable identity and mapping support are substantive. The reference
validates every asset key and handler before sorting validated string-key pairs,
which cleanly fixes the selected mixed-key exception defect. `Mapping` and frozen
dataclasses are idiomatic standard-library choices. The predecessor that sorts
raw keys first is realistic.

The suite tests an all-integer-key mapping, but a single integer key reaches the
known-bad's later validation and raises `ValueError`; it does not make sorting
compare unlike types. No mapping contains a valid string key and invalid integer
key together. Therefore the known-bad can satisfy every submitted assertion.

Minimal specification-only feedback: use both insertion orders of
`{"/x": handler, 1: handler}` and require `ValueError`, not the sorting
`TypeError`. Retain `UserDict`/mapping acceptance, sorted valid assets, ordinary
route order, name/path collisions, callable identity, immutable `Route` values
and input preservation.

### exp-v1-recovery-r24-python-generation-0159 — static positive

The corrected reference uses `lstrip()` followed by `split(None, 1)`, so the
first token is split on Python whitespace while the remaining argument keeps
its internal text and loses only surrounding whitespace. Lowercase dynamic
method dispatch, dependency identity, exact connection tuple objects, unknown
command silence and repeat behavior remain consistent and substantive. The
literal-space `partition` mutant is realistic.

The generic `ProbeModule` test sends `"  !PrObE\t  alpha beta  \n"` and requires
successful dispatch with argument `"alpha beta"`. The known-bad includes the tab
in its method name and cannot find the handler. The no-argument repeat test also
uses newline after the command, while ordinary spaces, case normalization, plain
and unknown messages, full command-token matching, exact sender identity and no
side effects remain covered. Tests depend only on the declared public behavior
and impose no private-helper layout. All seven criteria are statically positive.

Fresh resource-limited, network-disabled reference-pass/known-bad-fail and
original-parent control execution is still required before admission.

### exp-v1-recovery-r24-python-generation-0588 — test-only hold

The library update task combines six ordered operations, cross-map integrity,
atomicity, sorted output and deep ownership. The reference validates the `op`
discriminator as a string before membership and detaches the selected book before
an ID-specific move. This is the approved coherent fix for both malformed
discriminator handling and shared-input book isolation. The combined known-bad
is realistic.

The tests cover unknown string operations, schemas, invalid IDs, all operations,
dependencies, large IDs, atomicity and ordinary deep copies. They never use
`op=[]` or `op={}`, and they never bind the same ordinary book dictionary under
two different book IDs before moving only one. Thus neither component of the
known-bad is behaviorally separated.

Minimal specification-only feedback: require `ValueError` for list/dictionary
operation discriminators without caller mutation, including after a valid
operation. Separately bind one book dictionary under IDs 10 and 11, move only 10,
and require 11 plus the caller object to retain the original category. Preserve
all six operations, dependency rejection, later-failure atomicity, sorting and
deep output isolation.

### exp-v1-recovery-r24-python-generation-0738 — test-only hold

Targeted update versus creation, required-field validation, deep ownership and
the exact identity of the selected returned account form a substantive target.
Python `deepcopy` intentionally preserves shared-reference topology; the added
second copy of the selected account before email replacement is therefore the
correct scoped way to make a per-key update diverge from an ordinary account
object shared under another key. The original leaking implementation is a
realistic known-bad.

The suite thoroughly checks ordinary update/create behavior, nested deep copies,
selected-result identity, exact payload validation and malformed directories.
Its `target` and `other` accounts are distinct objects. It never stores the same
account dictionary under two keys, so both reference and known-bad produce the
same tested results.

Minimal specification-only feedback: store the same ordinary account dictionary
under keys `a` and `b`, update only `a.email`, and require `a` to have the new
email while `b` and the caller object retain the old email. Assert the selected
object is exactly `result["a"]`, and preserve username, password, extra fields and
nested-list detachment. Do not require unrelated output aliases to preserve
identity or invoke custom `deepcopy` hooks.

## Seven-criterion accounting

1. **Prompt clarity / complete specification:** every prompt is byte-identical
   to its immutable parent and sufficient to adjudicate the selected behavior.
   No generated prompt alteration or domain restriction occurred.
2. **API consistency:** top-level functions/classes, Python 3.11 runtime, exact
   shapes, ordering and exception boundaries remain consistent. No private state
   or undocumented coercion is inspected.
3. **Independent tests:** provenance is clean—the test author saw only IDs and
   specifications, and emitted tests equal candidate tests byte-for-byte. Only
   0159 has adequate defect discrimination. The other six fail behavioral
   sufficiency; 0143 also has explicit contract-conflicting oracles.
4. **Non-triviality / substantive whole target:** all seven complete tasks are
   substantive. Decisions do not rest on the small size of a repair delta.
5. **Correct, idiomatic reference / no test accommodation:** all seven references
   use ordinary standard-library Python and satisfy their approved scopes on
   static review. In particular, 0143's correct reference must not be regressed
   to satisfy invalid tests.
6. **Dependency isolation:** all artifacts use Python's standard library only,
   with no network, external package, service or filesystem dependency.
7. **Realistic known-bad and meaningful non-overconstrained verification:** all
   known-bads reproduce their bound original defect. 0159's tests reject its
   behavior through public API semantics. The other suites omit their defining
   witness rather than being credited for broad but nondiscriminating coverage.

## Provenance, scope and immutable bindings

All seven requests are `reference-fix`. Candidate problems equal parent problems,
verification prompts and architect outputs byte-for-byte. Candidate answers equal
validation and architect references; candidate known-bads equal architect
mutants; candidate tests equal independent-author outputs. Both author runs
returned zero, did not time out, had no parse error and reported no disallowed
tool item type. Each plan parent hash matches the canonical original. All
non-transformation source fields and rights equal the original parent; the
transformation suffix binds R24 ID and parent hash. This records lineage, not
admission or a new license ruling.

Parent corpus SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Hold ledger SHA-256:
`9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.
Common canonical rights SHA-256:
`8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`.

| R24 suffix | Decision | Candidate file SHA-256 | Candidate canonical SHA-256 | Parent canonical SHA-256 | Problem SHA-256 | Reference/answer SHA-256 | Test SHA-256 | Known-bad SHA-256 | Source record SHA-256 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|0047|Hold|`df907b90db18c6e937ffd9c851adf42e87f47d678049cc2bb65c9c24ec6e37ff`|`7bd74105bcb392a9056d746aff9eb4a48fcfffaf5b36b3bc6b2c824d19193953`|`2cb4ead62e781964c6e88bddaf9b8fb1715a12462cf54b85b15971177469a32d`|`d6892f718c3336700d57051d877bff74ea26c7b8185aa9a562d8b8b7129dcf1a`|`eebb8b2927d58c990f8727147924fd744e2ec53fc174ce88bf69c71285d90f94`|`8870407ac4255f9b7b816dc0fa8e6e116b2c2a6f8840d91c79946f1dffa0d577`|`e90e60a7da71a87aff54d21c0e8bf4bf6863a74726aa59af962ae65588e23674`|`be82bf2e5d67d65b36948ac33d203957c88358b6f978a94cc634d28c4faf6f45`|
|0130|Hold|`0e6d663b1003677e0cb469dc63f704d7360ffb57db0e9b526e11b7a38908f297`|`185cd41a212994e335e36c1342234022d075b310d2e7ccc81de83f3021b91430`|`167118c9169c84eef1c6639a2dca6da947188164e24dc42f821bac7413591faa`|`b2c698eb76869a72dc6d6f6d57e02f3cc7d2e01f7527201795cd76435ace8610`|`a143220da0fccc9d880f77b887886e4347e080934859163e672688690c4a53f8`|`90c439dab43b296c53c0b7f139fcab16d030a2eb4deca97aaa31ea6d68869146`|`e23a6f2c4ccd553132e395fe0c6c4799e3423e84458065dfbebcad67b8fb690b`|`7825b6147e1ac20d4a4478dd90f700f6f7db7e73bfa5f60406af89750ad8b4c8`|
|0143|Hold|`df53b712cc304b1e612f494d6d3176cb3cf1a07beb454244b67b115ca6d28299`|`1a0e498f636db06c16978c50749ea6ab9315871f1b8abe96554fc6360102166a`|`fe8de50d87bfa45afc0930c7ebc31f161fc235701345dc539925c5ab3230cc76`|`f7a9e5b7b8460420d9ea23391d90a858f0632c2b53355ef9b319c6c443e870e4`|`d2a7438d9c9674d27c7def3302662482878e852b9dddaaa15611c954d9b2b243`|`b343476f74b34f615e679b2e2bd57a921fd733cdf7ea7a1732d55dfc79a7ca2e`|`11d205fa55d32730ef1ca228af1696f3a9858e0886444f5fef52c10004d83521`|`f28f6e822fd9d6809694e0302ce62f2ff740545d6e285a2f314f1630cdd1f655`|
|0153|Hold|`e4cc2d13b31f7b1b8d220904ad93cd9ad8e0648f89a1263cd0634a2a8a01b932`|`b4a224768b890f77644293bd3953ca7669067fd663d9ed7712c27d127e294ae2`|`cfc2316132c8a8c1aaf44d55f7fb35c230384ef0e97262ad362d14101870c4a8`|`26f58c6c7ab9feb13c4475da23cc5ea5de4ed3ada3f6b688deadd67e23f84117`|`f5bdfb9c4c4147af970b9a9d1fc1838e7e09f171d5d36641e0d0df558e8e7286`|`e32b79ee397f6d8014929ee5f7a64de9e91dcdf618db3e01052569b3be48fbd4`|`b6f08ce6fcffe4cc3af3484bf3c54c11228820f097aa5c3bf87e76882c5de3ae`|`37eca3ee52c4b38bfbffe75acbc4f322ed6daeeb146e599e5fb1dda619d38eba`|
|0159|Positive|`ac7860a5e4a0a00faca31dbffa2f1de1590b3c00055d67ef01ea64671b8e45ee`|`4e7b4be4325fc310ddee7e3decda5787ea802c076142ffe42bc5d77619ef080e`|`7a332974a4a89fb69754960d860ca42f072c75c60ac17127257d1dbba7f03400`|`1483d06381da41d4566c4d861fbb75003a4f59cce44c5bc547b3768009e0f7d7`|`e02fda08ffcd81d07deb7da736eaeecda850055bd12a8945812be35ec0f9f4e2`|`f02011c38d32374588cb908686f7b15049beff426db92f39bd66d7236963907d`|`3509d978faae9500b24c18a4d46197986e83a7ac839f3aa1cb9e71737feb07c8`|`5a198c17ffea276c814341dfd02b99b2fff90b517b495d1fd911892822a6548d`|
|0588|Hold|`dca6a1c938542290788ecaab11b1c26b9e2691faae8843dbdd9847e14517f9fd`|`79838f3e2ae2b11fcaf4ed321ae63b60a38d65d7cfbabe7e37b3c923ec25b319`|`ca29b3df2e7307a0f1ca72e4e4e57f89a9dcb8f0b589ae4c223bdae3f7b95fef`|`0802b23ea3ad91689f33c1edb3bdbdd6d55109ef87c0cf4f1ab27ef1e2a4f08c`|`1eeaed8cf240f8b6cd15584b635cd66b3b379c352e490b0f54a131cdb9e25f3e`|`37178bf963a63cb93cb7b8a06c66b1ceb46a5149ecb74b1a5859934399de1419`|`4bbc6639ad9e76b912b89d1e0c2117c4f1a8a15e6ee3ec9386f7e839dccf643b`|`11870823b72e93d6cfa893ae6a77d9d5a1eebf97b948d2d554edce85a8e89157`|
|0738|Hold|`32f9b8b1c0eb956566c4393b5f88ddf97590079ba8eba89a875133800fb89bcd`|`0b8d5e705958dd7b1e1a8737020ce49e7492e8b3fae53f18a0389f30b1302a6d`|`e23b7270f5b8e9988a062f204d40dae6d70a02e52b2f77b88bae0b6862b8c3e5`|`826f1794e88ba7756095ab87917abe2d9f45239daf21d4630fb9dfcbb1e1fe45`|`77720c48593760cd822b228752d57315cc5975367a59f3f2d3a8a56461873ae3`|`8434d934a47dd859f58f183831235c26c99fc29de0edaa3e2def307bdb536877`|`69a358e79d9e0255ba5b6e55e568c3a5a5afc099e4048438f8ae2e582da43ae2`|`7d779fae999c6f2ca280fa6020b0acf0e751563c4c09dbfefe14e34350e22182`|

## Shared evidence hashes

- `measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r24.json`:
  `2e881ce718f8509655f0a894daddc305c869bc787deb6672a9b68d6e0d416451`
- `measurement/data/expansion-v1/recovery-plans/r24/plan.json` and copied
  registry plan:
  `1f89608807b00559e993952c6d0a1936baccae882322c3315ae7efe3dd37d9fb`
- Logical plan SHA-256:
  `d2816d2eaf52f5c8427808ec807f04439218bb6a502eb95f4bcee5df970d71bc`
- `datasets/cache/expansion-v1/versioned-recovery/r24/run-contract.json`:
  `a455daccb7e85a30c3cc86d4c328ee44be8e6fd166afef6fe685bba9c8225be4`
- `datasets/cache/expansion-v1/versioned-recovery/r24/python-recovery-architect-evidence.json`:
  `f2a452118198ad70718a2bccb9a99f7353d641f8078a02ccad818ceb2b5fd18a`
- Architect prompt / final output SHA-256:
  `9bcf23076ecede555e2e7e6b6307065b512731a6dd9bc6284c42a4d433d67823` /
  `759487a59f9c54c0f0cfc080bf77a5aa78c9606f9adbab6dc6c0a817e1ebe821`
- `datasets/cache/expansion-v1/versioned-recovery/r24/python-recovery-independent-tests-evidence.json`:
  `60aa7e91bf3fd7bf5d77170f73a38776e3f9606caf30dc7172d7d4eebbb5e45d`
- Test-author prompt / final output SHA-256:
  `c4d75d2e54bfb6224b89e3dea7b6ec07e503bfb7a4c510e80eb26cbc3b8299b6` /
  `b4de7451616caf3da6ea98a35875f2ab5f44d386bd34a72c38c84436467e64c2`
- `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_PYTHON_RUST_BATCH3_20260908.md`:
  `d9c169ff6b54494708893a8028d7019e6ec6688499da24822a330b39ad51e349`

No execution result, admission count, training seal or release claim follows
from this report.
