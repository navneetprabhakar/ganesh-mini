# Lane-stratified probe transition audit — 2026-09-10

## Finding

The v3 lane rebalance did not improve the v2 total. Upstream, v2, and v3 score
5, 6, and 6 passes respectively on the same frozen 30-task screen. Relative to
v2, v3 restores `dev-t1-typescript-collapse-runs` but loses
`dev-t1-go-bounded-prefix-sum`: one pass moved between lanes with zero net
gain.

Relative to upstream, the v3 gains are Java, Python, and Rust versions of
`collapse-runs`. Its losses are Python `clamp-window` and TypeScript
`bounded-prefix-sum`. Those same three gains and two losses also occur in v2.
This is stable task-archetype transfer, not broad multilingual transfer.

The concrete errors reinforce that diagnosis. The Java gain repairs missing
imports. Python and Rust gains stop mutating the run value. The Python loss
drops lower-bound clamping. The TypeScript loss replaces an absolute-bound
check with the logically impossible `sum < bound || sum > bound` condition.
Lower held-out corpus loss in all lanes therefore did not translate into
reliable boundary-condition reasoning.

## Recommendation

Do not scale or rebalance this recipe again. The only defensible cheap question
left inside this mechanism is whether an earlier v3 checkpoint briefly held
the Java/Rust gains without the Python/TypeScript losses. That requires a new,
separately approved continuation-screen-only checkpoint sweep and grants no
promotion by itself. If that diagnostic is not run, retire this SFT mechanism
class and design a provenance-separated semantic-boundary supervision
mechanism without using private development tasks as training data.
