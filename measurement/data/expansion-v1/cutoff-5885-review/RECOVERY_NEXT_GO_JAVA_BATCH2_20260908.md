# Next Go/Java recovery selection, batch2 — 2026-09-08

## Provisional result

Recommend **15 new held parents:8 Go +7 Java**, from full reads of20 original triples (10 per lane). Shortfall against20:2 Go,3 Java. Selection only, pending main approval. No reservation, generation, execution, cloud, admission or central edit; zero new original-row coverage. All currently reserved r1–r20 plans exclude120 unique parents; selected overlap is zero.

Gate: recovery selection/quality, not training. Full original prompts, references and complete tests were read, mutant differences reconciled against complete references, and exact per-ID evidence inspected. Prior executed claims belong to archives, not this turn. No licensing/evaluation-overlap or elementary-padding selections.

## Per-parent scopes and seven criteria

Criteria: prompt clarity, API consistency, independent test origin, nontriviality, idiomatic code, dependency isolation and realistic known-bad failure. All selected records have independent_teacher origin and standard-library dependencies. Each target's substantive interaction and required clarity/API/test correction is below. Idiomatic safe arithmetic, ownership and native decoding behavior must be retained; original tests are not authority for identified conflicting oracles. New tests must be independently authored from approved derived specifications, with no reference/mutant leakage. Narrow recoverability is not an all-gates positive or admission.

### exp-v1-java-generation-0026 — reference-fix

Substantive target: Canonical lexical numbers interacting with iterative tree-slot completion.

Minimum correction, independent semantic witness and explicit caveats: Remove machine-int conversion/bound. Trees2147483648,*,* and a100-digit positive node label pass; remove contradictory original bound oracle. Retain ASCII decimal grammar, no signs/leadingzeros/whitespace, '*', complete child slots, deep iterative input and malformed false-not-throw. Values need not be numerically stored. Mutant restores int restriction with slot completion correct.

### exp-v1-go-generation-0027 — reference-fix

Substantive target: Whole-input validation before exact matches, bracket selection and finite interpolation.

Minimum correction, independent semantic witness and explicit caveats: Use overflow-safe convex interpolation, preserving exact stored matches. [(0,-MaxFloat64),(2,MaxFloat64)] at1 must be finite zero; reversed signs likewise. Retain same-sign large controls, fractional ordinary interpolation, minute0..1439 and malformed later observation after early exact match. Use sensible relative tolerance for non-exact results, not arbitrary bitwise floating equality. Mutant restores endpoint subtraction overflow with fraction division correct.

### exp-v1-java-repair-0065 — reference-fix

Substantive target: Exact limiting ratio, floor and minimum-one interaction over positive int dimensions.

Minimum correction, independent semantic witness and explicit caveats: Use exact rational comparison/products, which fit long for positive int pairs. fitSize(100,100,29,29) =>[29,29]. Retain width/height limits, minimum-one, no enlargement, asymmetric fractions and Integer.MAX_VALUE. Independent BigInteger rational oracle on small cases avoids repeating floating error. All nonpositive dimensions IAE; fresh arrays. No alternative aspect-ratio optimization. Mutant restores floating floor rather than merely integer-scale collapse.

### exp-v1-java-repair-0075 — reference-fix

Substantive target: Nested immutable snapshots, source iteration order and complete null validation.

Minimum correction, independent semantic witness and explicit caveats: Replace list contains(null) with element iteration before copying. Map.of(x,List.of(1)) and empty immutable list succeed. LinkedHashMap controls order; mutable lists/map changes must not alter snapshot. Null map/key/list/element remains IAE, including late entries. Require unmodifiable map/lists without exact wrapper identity. New mutant restores null-query validation with original deep-copy fix intact; no concurrent mutation guarantee.

### exp-v1-go-repair-0048 — reference-fix

Substantive target: Sorted adjacent spans, full-width distance comparison, lexical ties and nonmutation.

Minimum correction, independent semantic witness and explicit caveats: Represent ordered distances without signed overflow; ordered native unsigned subtraction is sufficient. [MinInt,0,1] must return (0,1,true); [MinInt,MaxInt] must return that pair. Preserve strict replacement only for smaller widths, duplicate zero ties and short-input tuple. Independent oracle can use math/big, not overflowing signed subtraction. New mutant may restore signed widths with original tie repair intact.

### exp-v1-go-generation-0095 — reference-fix

Substantive target: Concurrent timestamp/sequence state, bit layout, exhaustion and atomic errors.

Minimum correction, independent semantic witness and explicit caveats: Validate mathematical delta across int64 without signed subtraction overflow, before narrowing to41 bits. Fresh epoch MinInt64, Next(MaxInt64) must error; Next(MinInt64) must then have sequence zero. Also reject huge timestamp after a valid call without consuming sequence. Retain max delta, pre-epoch, node1023/1024,4096 same-ms values, exhaustion/new-ms reset. Bounded concurrent same-ms calls require a unique contiguous set, not scheduling-specific IDs; actual race qualification remains separate. No zero-ID-on-error oracle. Mutant can restore overflowing delta while zero initial sequence remains corrected.

### exp-v1-go-generation-0121 — reference-fix

Substantive target: Tuple identity, URI ambiguity, replacement lifecycle, ordered pagination and snapshots.

Minimum correction, independent semantic witness and explicit caveats: Correct both held defects: structural tuple keys and page length bounded by remaining items before offset addition. Insert (a+NUL+b,c,d) and (a,b,c+NUL+d) with distinct fields; independent Get/List/Delete and replacement must retain both. Two ordinary items, List(1,MaxInt) returns second only with tiny memory. Retain raw strings, URI ambiguity, nil behavior and specified nonnil empty pages. No new concurrency/error secondary-value rules. Mutant isolates collision or page-end overflow; tests cover both plus original offset semantics.

### exp-v1-java-repair-0270 — oracle-rebuild

Substantive target: Full task validation/uniqueness, stable ready ordering and output ownership.

Minimum correction, independent semantic witness and explicit caveats: Remove private-field reflection and mandatory returned Task identity: immutable references are allowed, not required. Compare public key/due values in order; fresh array/nonmutation remains. Preserve source constructor behavior so invalid Task values reach ready validation. Test boundary inclusion, equal-time stability, duplicates in excluded future rows, late malformed entries, Long.MAX_VALUE and empty output. Keep immutable public Task API without private representation oracle. Original < versus <= mutant remains substantive; reference behavior can remain unchanged.

### exp-v1-go-generation-0218 — contract-clarification

Substantive target: Multimethod state transitions and independent reviewer-map boundaries.

Minimum correction, independent semantic witness and explicit caveats: Explicitly clarify RequestRemoval from removal-pending as successful idempotent retention, consistent with any-nonremoved wording. Test two requests then one finish, rejection after removed, and each reachable nonremoved starting state. Preserve publish success/failure, ready-only suspension, raw nonblank IDs, existing public typed constants, scopes/reviewers, absent-ID errors and copied maps. Do not add nil/zero-value/error-map representation guarantees. This sole state-boundary decision needs main approval. Mutant rejects second request with other transitions correct.

### exp-v1-java-repair-0401 — reference-fix

Substantive target: Full key validation before fast paths, positional rename and detached mutable results.

Minimum correction, independent semantic witness and explicit caveats: Validate all existing row keys for null/empty before same-key or absent-source return. Tiny LinkedHashMap null/empty key cases must IAE without mutation for no-op, absent-source and actual rename paths. Preserve nonempty raw keys including blanks, null values, insertion position, mutable LinkedHashMap copy and collision error. Compare ordered key lists rather than comma-joined strings. Mutant skips full-row validation with collision repair intact; no new value restriction.

### exp-v1-java-repair-0460 — reference-fix

Substantive target: Canonical token grammar, exact full-long codec and ordered duplicates.

Minimum correction, independent semantic witness and explicit caveats: Reject -0 while retaining Long.parseLong exactness. Both -0 and0,-0,-9 throw IAE; remove original contradictory accepted-negative-zero oracle. Retain MIN/MAX, >2^53 precision,0, negative nonzero, empty/duplicate/order and malformed tokens/overflow. New mutant accepts-0 but retains exact integer decoding. No new exception message/cause demands.

### exp-v1-java-repair-0464 — reference-fix

Substantive target: Exact-marker section state, completed order, empty-line joining and full validation.

Minimum correction, independent semantic witness and explicit caveats: Track interior-line count separately from character length. [@@@L,empty,x,@@@] => newline+x; two empty interiors =>newline; zero interiors =>empty. Retain repeated empties, nested marker content, exact-not-prefix opener, unclosed discard, null even outside sections, fresh arrays and nonmutation. Nonempty blank labels remain allowed; no trim/newline restriction. Mutant restores character-length joining while exact opener fix remains.

### exp-v1-go-repair-0180 — reference-fix

Substantive target: Exact all-uint64 floor arithmetic, saturation and validation branch.

Minimum correction, independent semantic witness and explicit caveats: Replace remainder*100 with safe wide arithmetic; preserve zero-live and target<=live tuples. live2^63,targetMaxUint64 =>99; retain3->4 =>33 and clamp boundaries. Use independent big.Int formula on tiny full-width cases. New mutant can restore remainder overflow while original divide-first defect stays repaired. No new input bounds.

### exp-v1-go-generation-0280 — reference-fix

Substantive target: JSON shape/EOF validation, wrapped errors and exact allowed-level comparison.

Minimum correction, independent semantic witness and explicit caveats: Reject top-level null as zero Badge plus ErrMalformedBadge before semantics. Preserve native encoding/json field matching and duplicate last-value behavior; do not add exact-case or duplicate-rejection policy. Scope is top-level object only. Test whitespace-surrounded null, arrays/scalars, wrong types/trailing values, valid duplicates, blank/missing label ->ErrInvalidBadge, allowed empty level and nonmutation. New mutant restores null-as-zero-struct behavior while original trailing-JSON bug remains fixed.

### exp-v1-go-repair-0233 — reference-fix

Substantive target: Exact integer extrema and differences, stable order and normalized endpoints.

Minimum correction, independent semantic witness and explicit caveats: Compute nonnegative differences exactly before float conversion, avoiding signed overflow and endpoint collapse. On pinned64-bit, [2^53,2^53+1] =>[0,1]; also [MaxInt-1,MaxInt] and [MinInt,0,MaxInt], finite middle within[0,1]. Guard architecture-specific literals if testing portability. Retain negatives, duplicates, constant zeros, nonnil empty and independent output. Do not demand exact arbitrary fractions. Mutant restores float-before-subtraction with original denominator repaired.

## Excluded after full original prompt/reference/test reads

- Go generation0189: global duplicate-name defect is concrete, but Credential/Principal/AuthLog layout is incompletely specified and exact Basic/base64 spelling needs adjudication. Duplicate-only repair leaves scope questions.
- Go generation0270: package mutable map violates structural no-global-mutable-state requirement, but public API supplies no decisive semantic witness for that structural defect. Avoid private-map manipulation as invented behavior; separate structural qualification needed. Constructor tests additionally require unspecified nil on error.
- Java generation0080: original-configuration preservation conflict is concrete, but optional keys/values, task.index collisions and omitted return surfaces need separate contract decisions; do not silently preserve broad trim/rejection.
- Java generation0305: null exception mismatch is concrete, but whole target is mainly a fixed five-step rendering loop with boundary guard. Not a substantive count filler.
- Java generation0029: list contains(null) defect is concrete, but Room additionally rejects null student entries despite no stated element-null prohibition. Constructor domain needs adjudication; room-list-only fix is incomplete.

This bounded shortfall does not assert that no other defensible parents remain. No broad re-review or automatic selection occurred.

## Exact bindings

Canonical SHA uses sorted compact UTF-8 JSON, ensure_ascii=False. Corpus datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl SHA256680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec. Ledger measurement/data/expansion-v1/cutoff-5885-review/additional-holds.json SHA2569dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee. Source records and generated answers/tests are distinct artifacts; recorded rights are preserved, not a new legal conclusion.

### Binding exp-v1-java-generation-0026

- Canonical candidate SHA256: 0534a85b6da9497118cb55f2e8f05bbfba9aa4e4f0eb626cf714ea0e4c4d8884
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; revision 57bd46727e49ac3e2890218a146d35c2454a8496; row-28204; source SHA256 ca9c0668735ab216ff80d8c898379935316b6e9941594001b78d3d846ce98ed0; license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI https://creativecommons.org/licenses/by-sa/4.0/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests
- Prompt SHA256: 82a167b3147c36c0e7be0654e88ec6f2c9da27a85f62b7c689eb626fd1603bb9
- Reference/answer SHA256: f0da24edc8a2f7628889fe482b3c8305b1d582ab9e1c187249e3c2e94b94c985
- Original SolutionTest.java SHA256: f710d3f33ac2281d050ffe764d9279d299cff93b652a07279a588250600ac81e
- Original mutant SHA256: abd320723eeb9e6873b3173562790de449f0c1d94c1ddae6dffa0f4dd938e941; Accepts encodings that end with unfilled child slots because it checks for nonnegative slots instead of exactly zero.
- Exact held reason: Static hold: canonical numeric node tokens have no int bound in the prompt, but validToken rejects 2147483648; the valid tree 2147483648,*,* is rejected.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_4.md; SHA256 1719c893f2a73b7e0a9e90b919bb4db97e1c2ac3abc94fd2846e97632919585d.

### Binding exp-v1-go-generation-0027

- Canonical candidate SHA256: 3fca5e99057f8713a19a8bbe37827effe22c5ff22c04366cf98a656cb31dc0ac
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; revision 57bd46727e49ac3e2890218a146d35c2454a8496; row-16164; source SHA256 1a9ed05364034dc652c7173ba9e7edc1cae10da0379ad88a4e890126c67ecea2; license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI https://creativecommons.org/licenses/by-sa/4.0/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 96baab03bcc8a98fb487b72346b5bd9403d39830360085dedf711aa2273691d6
- Reference/answer SHA256: 28f492a8bab7648a3127dfa2c529b0e0a999b815ddc1ea6bd75d282eecba0af0
- Original go.mod SHA256: 96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905
- Original solution_test.go SHA256: ba3530e7f2783537f18854fc52cfd11ad6a31f92a82efe33a8858f8a9b2883d7
- Original mutant SHA256: 2f48d767cbb5b0148f49c45ffc432cdbe59bdc33cdb77fcaa8bbc82515771d10; The interpolation fraction is computed with integer division, causing every non-exact interior request to use the left value.
- Exact held reason: Executed finite opposite-endpoint interpolation returns infinity instead of zero midpoint.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_3.md; SHA256 030a1a1edb1f6b742f37f31b70dd86b0f8c1e12dc1bc6f8e644fb4b036bb3b74.

### Binding exp-v1-java-repair-0065

- Canonical candidate SHA256: c34d1c5d2b3f003ffea1c853e8dc04f86613d318364859a05b61f9b63688f065
- Source: m-a-p/MdEval-Instruct; revision 38c9197e3add996fae624eb198ebd06155b2101e; row-10884; source SHA256 a2ffe7305badc421b558e313f5945f22cf347d8d9e6181900d8b05b4a223277a; license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct; license URI https://opensource.org/license/mit/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 38ce365fd27849c957bec9fd8f1694a814f6f0f0a2b3f16b5b7a65a72f6825b0
- Reference/answer SHA256: 7f23bd6cfac60a7749e16d684a0064e2056882887bc88d558608a09b97b4a922
- Original SolutionTest.java SHA256: 315df41ce4a3af3097fe5a6f282074b7fcaeb66796b2f4ae27879a72db9e35be
- Original mutant SHA256: 407b72ef94e309006d3927c8d0c770c391634fc3ada5f1b6c995cdcc966fe629; Uses integer division for the scale factor, collapsing any required downscaling to a 1-by-1 result.
- Exact held reason: Executed hold: fitSize(100,100,29,29) returns [28,28], not the exact-floor [29,29]; binary floating rounding changes the required integer result.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/java_repair_0065_exact_floor_probe-result.json; SHA256 1957043fd89415ebf4dac32e7334fb378e7bb51c3386e59869ca33bc6c8bc80b.

### Binding exp-v1-java-repair-0075

- Canonical candidate SHA256: 7f843f49c9d9925480529ce3eac1047552fca5e2f28293d9e4403c3e3f617556
- Source: m-a-p/MdEval-Instruct; revision 38c9197e3add996fae624eb198ebd06155b2101e; row-09982; source SHA256 49a965fee739dffecbfccbfab49ef5a95cc5402a7bbeaa0db2200b47ae1ecb95; license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct; license URI https://opensource.org/license/mit/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: ce3949843d26efa4e066a9761c4940ec71439386b514bac373af6b3289e6f302
- Reference/answer SHA256: f3ad08a44303d5dc4bafae84a0ea25d07b3cdb8be6dd06b9505e5a4fefdfc3b5
- Original SolutionTest.java SHA256: 9364d5d7afb21671af7016910e524d45599b422ac119cd50c30053ff8f3a97ca
- Original mutant SHA256: 899b526b30f14830a02327a3d9d9dc3e77ee41d5aa69dedd80ef6c5738a3540e; Wraps each original list directly, so later source-list mutations leak into the supposedly immutable snapshot.
- Exact held reason: Criterion-positive nested-list snapshot repair; static hold: source Map.of("x",List.of(1)) throws from contains(null), rejecting valid immutable list input.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_11.md; SHA256 1b500abe97769c0068be828a91e9b09b574953a4c335f74b23484df6323aa09b.

### Binding exp-v1-go-repair-0048

- Canonical candidate SHA256: 750c4daa922b861fd2013145a76364da01755ac8c61c1fa092e4c0cb950392b5
- Source: m-a-p/MdEval-Instruct; revision 38c9197e3add996fae624eb198ebd06155b2101e; row-00314; source SHA256 a359818cd6f9e35da3cb1d15ca4da60ed09578855a0c542c8606bb39c11ff9cd; license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct; license URI https://opensource.org/license/mit/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 9e74c345b7189df709173547e1520dc4d19f541fb8d69e29534a7636585ed71f
- Reference/answer SHA256: 3ce1f3020a7f2827e65ce864fbd79c0226aeae322db0012c769af26785e9d364
- Original go.mod SHA256: 96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905
- Original solution_test.go SHA256: c31b5db8baeba086b2f71600f5c32dc3dabdcd4d4611d5b25906eb147a5e875e
- Original mutant SHA256: 04b748ff5fb840bd9bb8f691cc0b590b18c1b1494740d86a9bdaf12045c45f93; Equal-width candidates replace the earlier lexicographically smaller span.
- Exact held reason: Executed signed span-width overflow selects the wrong closest pair.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_7.md; SHA256 d659c4ccda2f5e666390f4c6cd847efbd42e1342c228513625a4a743e037d38f.

### Binding exp-v1-go-generation-0095

- Canonical candidate SHA256: 179863828385f6d0259eb99b885c38820d13b3d8c6844f45620e3dc9cb03e573
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; revision 57bd46727e49ac3e2890218a146d35c2454a8496; row-27736; source SHA256 f5aa52ee5881c9450065352f784eac6d229abb418c6c0376d1071e089df5bdf2; license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI https://creativecommons.org/licenses/by-sa/4.0/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 2f7bf5287781a5534abc28810d82ad1a362684773c16c930bdd183720612fcce
- Reference/answer SHA256: 2a90c42f289d23776b99bc269be123dbc93c957f0707c06f92e6ae06b8a4f55e
- Original go.mod SHA256: 96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905
- Original solution_test.go SHA256: c557e257cf86e2f0434895c7840fac4946709a428052b2de16469aa12608e32e
- Original mutant SHA256: 8580d50227f17a993b7df644c19031b20d16c2ac90df88a87b39507053bccc68; The first identifier in every millisecond uses sequence 1 instead of sequence 0.
- Exact held reason: Executed signed delta overflow bypasses the timestamp bit limit.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_8.md; SHA256 edb07770501248434984db12f2f6d7911e2613d8061fbddca333b50bf4f15253.

### Binding exp-v1-go-generation-0121

- Canonical candidate SHA256: 748e3d3563c5167ffd6fcbec801b9191aa48a4b28d852a5dcd78b1c5ff6e721d
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; revision 57bd46727e49ac3e2890218a146d35c2454a8496; row-27755; source SHA256 7c070187bd90893cde5d662efe2f622ce5aff653ff3ebd40a2f4267fbacc8a6f; license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI https://creativecommons.org/licenses/by-sa/4.0/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: e289568f43c8807df18d1cb48eff6990c09fc769933c5aa58d1b4ee8b80fdd42
- Reference/answer SHA256: b8e6550c729c2ecf772d77cef1f5c224bd0373cbaf6e33bb5776dbe10d192dc0
- Original go.mod SHA256: 96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905
- Original solution_test.go SHA256: 5838b4f360f181db3f1f0c8ead0f26484725a6ea94432856363c8f800bad040e
- Original mutant SHA256: 5ec9413c5d9cfa6dd0f9a0f2dda8929534eea2cbd050222f44bf3bd55a6f9c24; List skips the artifact at the requested offset because it increments offset before slicing.
- Exact held reason: Executed NUL tuple collision and valid pagination overflow panic.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_10.md; SHA256 b803a2c4a2e6fdde021ec347ce01e104724af0e4cc9e9592d71fbaf120d3c3fa.

### Binding exp-v1-java-repair-0270

- Canonical candidate SHA256: 007c19454079cb3c64acad3dc00fcd99d55dc2a0a136a876376fae9db81317ae
- Source: m-a-p/MdEval-Instruct; revision 38c9197e3add996fae624eb198ebd06155b2101e; row-08071; source SHA256 3b8c3da9c55588b1520b83c54f91403e185640693fdb90239e7e7b9946290f3b; license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct; license URI https://opensource.org/license/mit/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 5ed565b9cf0623f1eda57de121f245a57ba426f52fd1765fe2497edb09bb23b8
- Reference/answer SHA256: a1aab818577ae581ac9133e72d901f6c8cf0e87641da4a5ce60794c4c9d6efcc
- Original SolutionTest.java SHA256: 66df309282d3e3fa16676006b2de428cdbb4d74c79fe372714161cef483bb662
- Original mutant SHA256: 4489b38b406750afdd06a70b33d1646560ab54a2c3717346f1255e7317a7232e; Excludes tasks due exactly at the current step.
- Exact held reason: Tests require private field names and modifiers beyond preserved public API.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/SEVEN_CRITERIA_JAVA.md; SHA256 847c40de6bab8129ec42420778b4c11b1f394b393b9fa0358b812360b99f88e6.

### Binding exp-v1-go-generation-0218

- Canonical candidate SHA256: 9e86e83b0e915ce72b597e18fa741ba566dc55109e2b1b951245c55ca4dfcfc7
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; revision 57bd46727e49ac3e2890218a146d35c2454a8496; row-16417; source SHA256 2bdf1e2757b3bb800b3caf52479e9585f8993d1fb6810215b1ee9c574b6ec4fb; license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI https://creativecommons.org/licenses/by-sa/4.0/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: ce131492c97996a38d96d2f0df4a6683fdac208f0a9bb7d31a655659a49195a9
- Reference/answer SHA256: 9bf53b08de206935c55faf56b824f67c0575a713e35391d32227be5392e35203
- Original go.mod SHA256: 96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905
- Original solution_test.go SHA256: cc0e62648d19866581ef7eab4b39ce1dc34c53abf78003a645b0c1297090a033
- Original mutant SHA256: 8c645a5cbec20d2de6479fdba75ac480e5623930658be3049f3fdb0269750da0; FinishPublish reverses the success and failure outcomes, marking successful publications failed and failed publications ready.
- Exact held reason: Static transition contract gap: any non-removed state includes removal-pending, which RequestRemoval rejects.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_18.md; SHA256 ea82b71ab587e81430903b03635a7ce107e4e4ed454d3be3ce00a324cea1077d.

### Binding exp-v1-java-repair-0401

- Canonical candidate SHA256: c4d8ddefa4859653bc409279ab5db7cc83cdb24d68f788d33b1ec930831dbf9f
- Source: m-a-p/MdEval-Instruct; revision 38c9197e3add996fae624eb198ebd06155b2101e; row-12432; source SHA256 450b4f119dd3fc8460d37ff6b217a516794ce24008c366c8f52b4a0f3dc8780a; license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct; license URI https://opensource.org/license/mit/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 227dec471d003144c6edc873631f595cd9f404ae5d4a355f00dc5400f84850b7
- Reference/answer SHA256: 5312cd105c1d1013057e9578e2b4b0ad7b578d368db6412d20bbda1733a8215b
- Original SolutionTest.java SHA256: 1ab08410b4ac0e465006421212544c1e15ed7e0fa411520ca4e53df210fb4b0a
- Original mutant SHA256: f61f20a5b31f2f3c12e4999673d758dd2675e8d2798e3f440fc39f9fa1143438; The implementation fails to reject a rename whose destination key already exists, causing one value to overwrite another.
- Exact held reason: Static hold: required validation of null/empty existing row keys is absent, including no-op/absent-source fast paths; actual rename can dereference a null key.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_57.md; SHA256 b7a96a52aa6ed4443bfde2d594654ba67e8e1997adae5b97fb7ac51baaa0176c.

### Binding exp-v1-java-repair-0460

- Canonical candidate SHA256: 1b7dccfae15207310d49be2af3b5916aff29f6c55ac89b64eeb614660ac41182
- Source: m-a-p/MdEval-Instruct; revision 38c9197e3add996fae624eb198ebd06155b2101e; row-11843; source SHA256 85fd71077decc1963d8b90e139f7aa5cc72987c0412f850ed0b2ad00a741a7ce; license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct; license URI https://opensource.org/license/mit/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: baf1dda0231a74b6d349e406d460485c2f0c7b507559c2a58b735b999c8f804f
- Reference/answer SHA256: 1b64ac4080f5521d34f36bfd998bd8bb6fe8651265cbed68a37878f41a73d55d
- Original SolutionTest.java SHA256: 66a734d9ad15ae67f77860f60418447bafd4ca3dd671e4af663e29091b4e3472
- Original mutant SHA256: 26439a379c4212ff708217e87fc137d5058404e84b6ea8b63c2598049c983dde; Decoding passes integer text through double precision, rounding large values and mishandling long boundaries.
- Exact held reason: Static hold: canonical predicate still accepts explicitly forbidden -0, which Long.parseLong decodes as zero. Not executed.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_65.md; SHA256 70a3e1686674edfae4e7ead52a900f8e3613c7abbde00bdc9c30e924e14d0447.

### Binding exp-v1-java-repair-0464

- Canonical candidate SHA256: fa8d34215fe2836c1f6e49d6fd40bdb900ed86ec10fd685f9ea760c1bada280c
- Source: m-a-p/MdEval-Instruct; revision 38c9197e3add996fae624eb198ebd06155b2101e; row-08055; source SHA256 dfac8640df86d1e6e84375ad183965c1906bb26b51980cd1025a9e96d85f1b46; license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct; license URI https://opensource.org/license/mit/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 0f014ce2059b52ee96ebb5b13115f108e22de864a137aca321952b4f8fc9f68d
- Reference/answer SHA256: 01c6047507caae39fc8afa21200db073ed6598d815b16e60034a338221fa6457
- Original SolutionTest.java SHA256: 525802c72c4fb99c680dd51a21d1d8e142307ac4fb3ff99c4ddd71552ae9144e
- Original mutant SHA256: 6fcbf1d9f8abc62052dfa134dad7837253191a6e2d3a7274afde227b38f97ac5; Treats lines with extra suffix text as valid section openers.
- Exact held reason: Static hold: newline joining uses character length as an interior-line counter, losing initial empty lines; opener, empty string, x, terminator yields x instead of newline+x. Not executed.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_65.md; SHA256 70a3e1686674edfae4e7ead52a900f8e3613c7abbde00bdc9c30e924e14d0447.

### Binding exp-v1-go-repair-0180

- Canonical candidate SHA256: 7b5faf2fe549940745ff9bab52fa3bc710b837ce12d956656ff511a5648e6112
- Source: m-a-p/MdEval-Instruct; revision 38c9197e3add996fae624eb198ebd06155b2101e; row-11216; source SHA256 ade965862f69231d186a52f7fe4929c39946818a77eee9b7e5718f779440ac86; license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct; license URI https://opensource.org/license/mit/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 1a91ee508c0b25058de5ae7b883cf7434ae3fb52a60a2d475fcba32a01d3a9b3
- Reference/answer SHA256: cf4fdbd2ea95fa927b5ae62d5b8ee7dc444ea509017e15c925f94fe67bb8cf69
- Original go.mod SHA256: 96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905
- Original solution_test.go SHA256: ab9223aacd30fda1f776b3674d1f6e11ed802b0f1d6a9cb6ab07010cf91be79c
- Original mutant SHA256: b1ba86681e2beceb5bb56ec08b09958fae3991576a90e1e458e32bb38ca19131; Performs integer division before multiplying by 100, discarding fractional percentages.
- Exact held reason: Criterion-positive exact uint64 arithmetic; executed behavioral hold: remainder times 100 still overflows.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_22.md; SHA256 25bf51489804d0121f218c29c990be0119fa7d5961012fd54072c15ec7434cb1.

### Binding exp-v1-go-generation-0280

- Canonical candidate SHA256: a3e286b919262fbae3b53571ec92273fb0df3a94d347c153277c09f0fff9d39a
- Source: Multilingual-Multimodal-NLP/McEval-Instruct; revision 57bd46727e49ac3e2890218a146d35c2454a8496; row-28009; source SHA256 bcab7a773879d76851c2be5e4d8092c6a9a4b84a70f04f92246616faf3d3bec7; license CC-BY-SA-4.0; URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct; license URI https://creativecommons.org/licenses/by-sa/4.0/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 4c13666bb4ca43e61f0ee911475426a911b30eb600029165d0467852bae067c0
- Reference/answer SHA256: daf0854bbc80ad5e57ba9be7155e2617cf1dc63eca2c87d96f36c5135d681297
- Original go.mod SHA256: 96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905
- Original solution_test.go SHA256: 5ba0548706f989e412c7df25527e252069b2a2f9bb642ef4a9d87978e570c66d
- Original mutant SHA256: abb134bb916ea7e45cac5e3fc232aab33ad2e0722edb73404396cac4050e3934; ParseBadge accepts additional JSON values after the first object.
- Exact held reason: Criterion-positive strict parser/error categories; executed behavioral hold: JSON null reaches semantic validation rather than malformed-object rejection.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_22.md; SHA256 25bf51489804d0121f218c29c990be0119fa7d5961012fd54072c15ec7434cb1.

### Binding exp-v1-go-repair-0233

- Canonical candidate SHA256: 353fc94add0a23ae2f54cdee93f18fc3d68ca42b298cbb0e7239d595237cdf6f
- Source: m-a-p/MdEval-Instruct; revision 38c9197e3add996fae624eb198ebd06155b2101e; row-00779; source SHA256 b676eda5236fc21bceb7add437cb7f764b8a901279e1ef35caf5c6897b1fe096; license MIT; URI https://huggingface.co/datasets/m-a-p/MdEval-Instruct; license URI https://opensource.org/license/mit/.
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}; test origin independent_teacher.
- Original transformation: Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification
- Prompt SHA256: 2d41b1902e19fbb06df8a612b49ce7ed5de88408c4c666eadd354d04b0f98b67
- Reference/answer SHA256: 835f04dc3397ef829b5fa314e161e72086f2750be222f29ec5c15efe0ea0ac91
- Original go.mod SHA256: 96608ba4d2790dd50587db4a263b8eb3cec88a704fe4c3d57363e81e7bf58905
- Original solution_test.go SHA256: b0a5dee38096c4cd7eb2f5d16658bc5c95e96d61e1f74d76055fbfca7c652bcd
- Original mutant SHA256: 3f2331452a0c129ebaf7b454c8106825532cd58645ba115b81a3cc9f9c9a9327; The scaling denominator adds the extrema instead of subtracting the minimum from the maximum.
- Exact held reason: Criterion-positive numeric normalization; executed behavioral hold: adjacent large int endpoints collapse on float conversion and become NaN.
- Evidence: measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_28.md; SHA256 6a27a803269ffa76cf451506a2c2847939b34db1d6581cc88f27a1b84161a8b5.

## Frozen reservation exclusions

Exact plan files below yielded120 unique original parents. Recheck if new reservations appear before approval. Selected parents remain held originals; future derived versions require fresh artifact hashes, quality, pinned sandbox reference/mutant qualification, deduplication/evaluation separation and admission seals.

- datasets/cache/expansion-v1/versioned-recovery/r14/plan.json: 2d59789fea811ba7ebe844564ee4dc66569fe4719067dea6d6a1524b049ea51f
- datasets/cache/expansion-v1/versioned-recovery/r13/plan.json: dead1489bb779934327bf3c8786d89c65b7604832829fa17129ea41ff1773217
- datasets/cache/expansion-v1/versioned-recovery/r12/plan.json: 0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121
- datasets/cache/expansion-v1/versioned-recovery/r15/plan.json: d2e65ef33e2c70162a53315e3daec75ebe1e3fbc1a7098e8635eddacb348c100
- datasets/cache/expansion-v1/versioned-recovery/r7/plan.json: f0a3b5d14eb983206ac83c99571c5522925feaf7ac0443ec3c59ad172d5f293e
- datasets/cache/expansion-v1/versioned-recovery/r9/plan.json: 0f0d6e653bbabff308a912cc764d1373b20faf3f4cf68a4c7341c94f36b5ae79
- datasets/cache/expansion-v1/versioned-recovery/r8/plan.json: 1a579af9da9d542d6bb4f03c8fbc030fd0b9d3102a31c347cd631bfc18b873de
- datasets/cache/expansion-v1/versioned-recovery/r1/plan.json: a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1
- datasets/cache/expansion-v1/versioned-recovery/r6/plan.json: 803f0308b33b4b8a834347d5976a148bc66001d6fc8606a1e206fb0e2b4a6795
- datasets/cache/expansion-v1/versioned-recovery/r10/plan.json: 728e70ee23ad46f8a4a8aec64a34d74b48c073a5382849fc52ce449154f2afb5
- datasets/cache/expansion-v1/versioned-recovery/r17/plan.json: 60c02db8869c80c1515e2216205ac11a45b357206563f62f499d8b67b3ee02ee
- datasets/cache/expansion-v1/versioned-recovery/r19/plan.json: 401d56a11f2ca2929eb42be7ffb36fe694cfded2500ed56a96759560b8b65f62
- datasets/cache/expansion-v1/versioned-recovery/r18/plan.json: 512e3219da55465742728f2c5116840498e4a41c5a2bfe8f5b0130d9a19690a0
- datasets/cache/expansion-v1/versioned-recovery/r20/plan.json: 879eb4184b49e09a171cbe35592096a296d9d2af6e1e52eea68315fb6b7eb224
- datasets/cache/expansion-v1/versioned-recovery/r16/plan.json: efd902abc4ed3e00d6639c74f7d2ec95e6f153d1aa19a70a460aeb553dfb6844
- datasets/cache/expansion-v1/versioned-recovery/r11/plan.json: 2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6
- datasets/cache/expansion-v1/versioned-recovery/r3/plan.json: cbad9d14a504531e749b5eb3433f0bf4670e21f2a8e8d5f310d2e843e53c6231
- datasets/cache/expansion-v1/versioned-recovery/r4/plan.json: 8a6137773e65e1a55e5eaceed9a8c2e40153b5759a46a5189ba6a488d530d58c
- datasets/cache/expansion-v1/versioned-recovery/r5/plan.json: 778e0071bec56248081e741f4c742d522c75b4b006e069d8301b75440c2732ec
- datasets/cache/expansion-v1/versioned-recovery/r2/plan.json: 5dae7eac34ac462f6173dc6b740364d5c4b68129950359f453f4038111ad1d29

