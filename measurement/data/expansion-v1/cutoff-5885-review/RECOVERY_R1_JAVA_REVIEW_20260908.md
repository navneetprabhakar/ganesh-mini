# Recovery r1 Java static quality review — 2026-09-08

Scope: `exp-v1-recovery-r1-java-generation-0781` and `exp-v1-recovery-r1-java-generation-0788`, exact original parents, recovery request/plan and Java teacher evidence. Full derived and original prompt/reference/test/known-bad content was inspected. No candidate execution, cloud access, candidate edits or ledger changes. Zero additional unique-original-row coverage.

**Decision: both recoveries are scoped static quality-positive and suitable for the next sandbox verification gate.** This is not executed correctness, admission, training authorization evidence or release approval. Original records remain held; only the hash-bound derived artifacts below are assessed.

## 0781 — monetary intermediate overflow

The derived prompt is byte-identical to the original. The approved reference-fix request requires exact safe percentage intermediates, preserving half-up rounding, discounted tax/gratuity bases, final overflow rejection and deterministic participant distribution. The reference uses `(BigInteger(cents) * basisPoints + 5000) / 10000` and `longValueExact`, followed by exact subtraction/addition. All validated quantities are nonnegative: discount cannot exceed subtotal, required percentage results fit when mathematically representable, and final nonnegative additions cannot overflow transiently and then recover. This removes the implementation-induced product/rounding-addition overflow without weakening real total-overflow behavior.

The decisive independent witness is `Long.MAX_VALUE` with 10000 discount basis points: required discount is exactly `Long.MAX_VALUE`, discounted subtotal/tax/gratuity/total are zero. Reference supports this; supplied known-bad is the original reference and throws at `multiplyExact`. This is meaningful rejection of the recovery defect, not an unrelated test error. Genuine total overflow is separately expected for maximum subtotal without discount, with and without full-rate tax.

Other tests substantively cover independent rounding (101 subtotal, 50% discount -> 51 discount, 1 tax, 3 gratuity, 54 total), all five service levels, normal discounted tax, zero, invalid inputs/indexes, stable immutable results, and remainder allocation. The 10,000/825/1000/20% example correctly yields 1000 discount, 743 tax, 1800 gratuity, 11543 total and shares 3848/3848/3847. `Integer.MAX_VALUE` participant count is exercised without proportional allocation. Reference computes individual shares in constant space; adding a remainder cent cannot overflow because a positive remainder implies the floor share is below the total.

No static correctness or oracle blocker found. Partial-large-discount and near-total-limit probes could broaden confidence but are not a newly required gate: the general BigInteger formula and the existing maximum/full-discount witness address the identified mechanism.

## 0788 — Unicode blank validation and XML structure

The approved contract clarification explicitly retains `String.trim()` normalization, adds `String.isBlank()` rejection after normalization, and says comments are ignored and cannot provide required children. The derived prompt contains these requested changes without changing the direct-child schema, integer parsing contract, ordered duplicate messages, defensive immutable output or XML access restrictions. The older broad comments phrase remains in its invalid-input list, but the new explicit comment rule and missing-child fixtures resolve it: a comment is not a substitute for a required element; harmless comments alongside real required elements are allowed.

The reference uses `getTextContent().trim()` followed by `isBlank()` in the common leaf helper. U+2003-only Category and Message are therefore rejected while nonblank values retain trim—not strip—normalization. Independent tests contain separate U+2003 category/message witnesses. Supplied known-bad is the original reference with `isEmpty()`, so it accepts these values; rejection distinguishes the actual correction. The number remains the named `Integer.parseInt` domain plus nonnegative check; no new ASCII-only grammar or ban on otherwise parseable signs is inferred.

DOM traversal accepts exactly one direct Number/Category/Messages, rejects unexpected/duplicate children, disallows element children in leaves and requires actual Message children. Tests cover missing/duplicate/nested substitutes, comments pretending to supply Number or Message, reordered valid elements with harmless comments, CDATA, duplicate/message order, malformed XML, integer maximum/overflow and empty/blank leaves. The reference's copied unmodifiable list supports the mutation/stability tests.

DOCTYPE declarations are disabled; general/parameter external entities are disabled, external DTD/schema access attributes are empty, and XInclude/entity expansion are disabled before parsing. Unsupported configuration fails before parse and is wrapped as a nonempty `IllegalArgumentException`. Tests require rejection of internal/external entities and a bare DOCTYPE. These assertions alone do not prove no access occurred; the static fail-closed setup plus network-disabled execution remains the relevant protection. No candidate was executed or network/file entity target accessed in this review.

No static correctness or oracle blocker found. Null-input, nested leaf-element and nonblank Unicode trim-preservation probes would be additive coverage, not evidence of a discovered defect; the reference handles those paths directly. Do not turn optional coverage improvements into blanket re-review.

## Seven criteria

| Criterion | 0781 | 0788 |
| --- | --- | --- |
| Prompt clarity | Positive: exact monetary rounding/order, validation and sharing contract. | Positive: explicit derived trim/isBlank and comment semantics resolve parent ambiguity. |
| API consistency | Positive: required public nested API, return types and checked monetary behavior. | Positive: immutable Notice/getters and parseNotice exception contract. |
| Independent test origin | Positive: archived prompt contains only derived IDs/specifications and test/runtime instructions; exact output bound below. | Same. |
| Non-triviality | Positive: full monetary calculation, interacting rounding/overflow/discount and deterministic split; not judged by size of fix. | Positive: secure parser, schema traversal, normalization and immutable ordered results. |
| Idiomatic code | Positive: standard BigInteger and exact long arithmetic, constant-space share query. | Positive: JDK DOM parsing with explicit hardening and defensive collection copy. |
| Dependency isolation | Static positive: JDK-only; pinned sandbox execution pending main. | Static positive: JDK-only; XML external access fail-closed configuration inspected. |
| Realistic known-bad failure | Positive statically: original premature product overflow rejected by maximum/full-discount witness. | Positive statically: original Unicode-blank acceptance rejected by explicit U+2003 witnesses. |

## Bindings and hashes

Both parent canonical JSON hashes reproduce the frozen plan; rights are unchanged. Parent source revision is `57bd46727e49ac3e2890218a146d35c2454a8496`, McEval-Instruct, CC-BY-SA-4.0. Parent source records are row-28067 (0781) and row-28578 (0788), with original source hashes retained in candidate metadata and recovery transformation lineage. No provenance decision was reopened.

Architect output problem/reference/known-bad and independent output test code exactly match both candidates. Independent author prompt was read in full and exposes neither reference nor parent tests/known-bad. Both teacher evidence records report return code 0, timeout false, no disallowed tool items and no event parse error; prompt/final-output/stderr content hashes reproduce their declarations. These are author-run metadata, not verifier outcomes.

Shared request SHA-256: `c7fed0810f7fa42b2b0e5c56ccf9e0afe2c0b239db8aa529c5c0744f58e6b37d`; plan file: `a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1`; bound recommendation evidence: `adc9832180fda515790272be9305841a4b9da4356b336cafaa0843bbe3ba0b3f`. Shared paths are `measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r1.json`, `datasets/cache/expansion-v1/versioned-recovery/r1/plan.json`, and `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_TRANCHE_RECOMMENDATIONS_20260908.md`.

| SHA-256 binding | 0781 | 0788 |
| --- | --- | --- |
| Parent canonical JSON | `2fe9d28d7cc74ea034ab338a3c535100a5fe47cfd627268ca4544a8ad528ad27` | `4959a3daecf43d2ed70ec7221329d70c3ab760974b210815ab4d3c2d74ffa30e` |
| Derived candidate file | `5ba68b1d0b6e465c6cca811e14a1ce3869eb9908b50949d09c2237e641474010` | `622fa006994a243dc12a616e0a50efb8a3cf81566fc47e0aae31999b02bda03d` |
| Prompt content | `d3604ae7d6dd3673fb845b56820907546a9b8d5d72c1be75ddb44046194fecce` | `cc39fe9ed4a2b59d9558226729ada52eeca99707e3ec6119e21659a4ac0fda32` |
| Reference content | `b87dbb6ecffb5c7bafefef372675501ba2c0f734c7976f02e5e42ec6a16cd8ce` | `0aded3000145bd39bdb8b02e77883bd68f8497878acb32046a5a4cfb895b8bc8` |
| Independent test content | `a5bd5cca6c362f098984134a4380719094482f8cf5f0f5b10afbfe4ee7efef65` | `dcc5a76fb505015c6a3dd1d7934f11afb821b7daa68b4ce1529d3e6ff9f86840` |
| Known-bad content | `033427eca0b70e63f47e9776f417fe713f5010156a57f4caeb20a7d47bca0993` | `b52419b83cfac390cbdbc6965b0740876b083f22229003b8ccebb9447349ac6e` |

Under `datasets/cache/expansion-v1/versioned-recovery/r1/`, `java-recovery-architect-evidence.json` file SHA-256 is `0cecfa4525ca32d189a97124a6fe3f35ed7c9f9d515ad065d7469e8fb54ce9f0`; `java-recovery-independent-tests-evidence.json` is `024aabaf2f484fcfe2aa6b5f2ee8fdb2fc29a9867ff180047c4148916c27e7b0`. Candidate basenames are their exact derived IDs plus `.candidate.json`.

Both declare runtime `java-21.0.11` with 1 CPU, 512 MiB, 64 PIDs, 65,536 output bytes and 60 seconds. Main owns execution and remaining recovery gates. Counts: 2 scoped static positives, 0 new static holds, 0 unresolved contract questions, 0 executions, 0 admissions, 0 new unique-original-row coverage.
