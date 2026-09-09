# Capacity-probe transition audit — 2026-09-10

## Scope

This is a read-only comparison of the exact frozen base evidence and the
capacity-probe terminal canary. It does not reinterpret verifier outcomes and
does not admit any evaluation task into training.

## Exact transitions

Four tasks changed from fail to pass:

- Go `bounded-prefix-sum`: the base returned the wrong failure sentinel; the
  candidate returned the specified sentinel and added the negative-bound guard.
- Java `collapse-runs`: the base omitted required imports; the candidate
  supplied a compilable implementation.
- Python `collapse-runs`: the base incremented the run value; the candidate
  retained one value per adjacent run.
- Rust `collapse-runs`: the base made the same run-value error; the candidate
  retained one value per adjacent run.

Three tasks changed from pass to fail:

- Python `clamp-window`: the candidate stopped clamping `start` into
  `[0, length]` and therefore returned invalid windows.
- TypeScript `bounded-prefix-sum`: the candidate tested `sum < bound` instead
  of `sum < -bound` and omitted the negative-bound guard. It compiled but
  failed behavioral verification.
- TypeScript `collapse-runs`: the candidate compared index zero with index
  minus one, then advanced the cursor twice. It compiled but failed behavioral
  verification.

The headline +1 is therefore four gains minus three losses, not one isolated
new capability. Three of the four gains are the same elementary
`collapse-runs` product across languages. Python merely swaps one passing task
for another, and TypeScript loses both of its base passes. The evidence is
consistent with narrow pattern transfer plus cross-lane interference; it is
not evidence of broadly stronger coding behavior.

## Prefix-mixture finding

The 468,601-token probe used the first 624 prepared records. Its weighted
objective allocation by lane was:

| Lane | Rows | Input tokens | Objective share |
| --- | ---: | ---: | ---: |
| Go | 168 | 143,554 | 20.27% |
| Java | 119 | 73,324 | 20.31% |
| JavaScript | 48 | 33,931 | 11.15% |
| Python | 113 | 69,101 | 21.95% |
| Rust | 134 | 119,431 | 19.14% |
| TypeScript | 42 | 29,260 | 7.17% |

The frozen preflight balanced five product families, combining JavaScript and
TypeScript into one family. That family received 18.32%, but TypeScript alone
received only 7.17%, despite the promotion rule enforcing zero regression on
each of six lanes. This is a contract mismatch: the training prefix was
family-balanced while the safety condition was lane-balanced. It does not
prove that underweighting caused the regressions, but it is the first mechanism
defect that must be removed before interpreting another capacity experiment.

## Recommendation

Do not increase rank, tokens, or runtime again. The next bounded recipe should
first make the optimization and promotion units agree:

1. Construct the probe prefix with explicit six-lane objective targets rather
   than a combined JavaScript/TypeScript family target.
2. Use stratified optimizer groups so every short training window contains all
   six lanes; report realized lane weights per checkpoint.
3. Add a non-evaluation retention slice for language-specific boundary
   semantics and require no degradation on it before the private canary.
4. Keep the same small continuation screen and stop on any lane regression.

This recommendation is a new mechanism, not a waiver of the failed result. It
needs a sealed local design and a fresh approval before any GCloud execution.
