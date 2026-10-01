# Gate 2 repair-delta V8 two-role correction plan — 2026-09-17

Status: prospective local contract; readiness next

Contract: `capability-stratified-v8-two-role-correction/v1`

## 1. Boundary

V7 is terminally sealed as `qualification-failed`: 58 candidates admitted,
two rejected, and zero unresolved. V8 does not relabel or edit either V7
disposition. It is a prospective correction of exactly two invalid authored
test roles demonstrated by the final executable matrix:

1. `cap-v4-associative_aggregation-rust-repair-primary` — replace only
   `primary_discrimination`. The V7 test required the literal internal key
   `kind.audited`, although the specification requires behavioral consistency
   and the reference consistently uses `kind.audit`.
2. `cap-v4-binary_and_bitwise-python-repair-primary` — replace only
   `cross_cutting`. The V7 cross test mocked SHA-256 and asserted primary
   payload dataflow, so it necessarily failed the known-bad instead of
   isolating immutability/aliasing.

The other 58 complete V7 admissions and the passing role in each corrected
candidate are carried byte-for-byte. No other role, candidate, semantic result,
or disposition is eligible for change. A V8 pass qualifies corpus construction
only; it does not authorize training, evaluation opening, publication, or a
release claim.

## 2. Immutable inputs

Before any V8 model call, bind the V7 plan, readiness, first-pass, delta,
separation, admission, terminal artifacts, and qualification summary at report
seal `1bbdd82b8558542547f0476e8b753089a0c93e73221f4db4c6b6b9787dde3f06`.
Bind the exact V5 teacher/proof/semantic carries and V2 generation equivalence.

V8 carries:

- 58 exact V7 admitted envelopes and executable outcomes;
- the V7 passing `cross_cutting` role for the Rust candidate; and
- the V7 passing `primary_discrimination` role for the Python candidate.

It carries neither failed role nor its failed executable result into a V8
decision. Candidate reference code, known-bad code, specification, assignment,
teacher proof, and semantic evidence remain byte-identical for all 60 cells.

## 3. Two fresh independent role authors

Run exactly two fresh model calls, in the order listed in section 1. Each author
sees only the specification, embedded known-bad, lane, assigned capability or
dimension definition, canonical filenames/command/binding, its single role,
and this response object:

`{"content": <non-empty complete test source>, "case_ids": <unique non-empty strings>}`

Rust primary requires at least two cases and must test externally observable
`mark_audit`/`is_audit` behavior. It must not assert a literal metadata key
unless the specification uniquely names that key.

Python cross requires at least one case and must pass the visible known-bad. It
may test only input non-mutation/alias isolation. It must not mock, intercept,
or assert the value passed to SHA-256 and must not assert the returned digest.

Authors never see the reference, V7 tests or outcomes, verifier output, proof,
semantic review, source data, evaluation content, or one another. There is no
correction, retry after structured response, reserve, or third author call.

## 4. Readiness

Before the two calls, seal:

1. the exact two-cell/role correction manifest and the 58+2 carry accounting;
2. unit fixtures for the single-role schemas, case-ID rules, Rust/Python static
   interface rules, and forbidden semantic patterns above;
3. one content-free live provider admission smoke for the single-role schema;
4. one synthetic Rust-primary and one synthetic Python-cross canary under the
   final prompts, each compiling and satisfying its applicable executable
   matrix; and
5. a composite readiness report with zero evaluation reads and `status: passed`.

Readiness artifacts never enter training or qualification.

## 5. Final adjudication

After both fresh roles pass schema/static checks:

- reconstruct the two candidate test pairs with their carried passing roles;
- run a fresh blind delta audit for each changed candidate;
- rerun content-free global separation for the complete reconstructed 60;
- execute all four suites for each changed candidate under canonical staging;
- require reference primary/cross pass, known-bad primary fail, and known-bad
  cross pass; and
- revalidate byte identity and seals for the 58 carried admissions.

V8 passes only with exact 60/60 final admissions, zero unresolved, clean
lineage/separation, V2 generation equivalence still passing, and combined
120/120 generation/repair coverage. Any schema, static, delta, separation,
execution, identity, or accounting failure seals V8 failed. No post-hoc edit or
additional author call is allowed.

## 6. Scope and hard stops

Local readiness, two model calls, two delta audits, separation, sandbox
execution, and sealing are authorized under standing non-GCloud scope. This
plan authorizes no GCloud action. Stop on any V8 readiness or final gate
failure, ambiguous destructive action, or goal-alignment `DIVERGENCE`.
