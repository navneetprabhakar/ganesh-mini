# Main r7 bounded correction approval

Main fully read r4 Go review and both provisional r7 JSON files. Exact prior
canonical candidate and review file hashes validated; approve all9 for exactly
one test-only correction from r4. Final requests/feedback remove provisional
wording and explicitly distinguish an actual NUL character from a literal escape
sequence in0439. All original specs/references/mutants remain immutable.

Feedback derives witnesses from specified input domains, not reference code.
Remove unsupported empty-slice/invalid-destination boolean/skip-interleaving
oracles, retain explicit error/trace promises, and qualify mixed-method concurrency
with bounded per-key ownership and deterministic final checks. No assumed
scheduling, arbitrary allocation, unsafe pointer dereference or test-owned race.
Go0439/0522 still require actual additional pinned -race execution.

R4 ordinary diagnostics are ongoing at this selection checkpoint; report their
terminal outcomes separately, without replacing or reconstructing them. Current
static missing-witness findings alone justify bounded independent test correction.
No automatic second critic, admission, training or cloud claim.
