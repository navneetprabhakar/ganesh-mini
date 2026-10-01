# Gate 3 Go single-worker requalification — 2026-09-23

Status: prospective local execution contract after sealed first-pass matrix

The sealed 534-candidate first-pass matrix (`01ab1d4b460a922e81b61497a923e2ac0c577eceb607288f9734a5a7f951f5e3`)
contains 476 admissions, 24 rejections, and 34 unresolved outcomes. All 34
unresolved candidates are Go; their frozen 60-second suites timed out after the
one identical replay. The original results remain terminal evidence and are
not relabeled. A diagnostic-only isolated replay of one unresolved Go candidate
preserved the exact input SHA, completed each suite in about 26 seconds, and
revealed an ordinary reference-test rejection. It grants no admission credit.

Run a new, separate matrix campaign for **all 89** remaining-first-pass Go
candidates, not only the 34 timeouts. Select them deterministically from the
sealed merged teacher, test-author, attached-candidate, delta, and parent
matrix cohorts in their existing order. Preserve candidate, authored tests,
blind delta evidence, pinned image, commands, task limits, and 60-second
per-attempt timeout byte-for-byte. Change only host scheduling to one verifier
worker, eliminating the six concurrent amd64-emulated Go compiles on this
Apple Silicon host. Each suite retains at most one identical infrastructure
replay. Do not read any evaluation surface or use GCloud.

The new campaign is uniform and fail-closed: every new Go result, including a
regression from a prior admission, becomes the Go cohort's prospective
qualification outcome. It may replace the Go slice in a new derived aggregate
only if all 89 input SHA-256 values match the original matrix inputs, no result
is unresolved, no original admission regresses, and all report/artifact hashes
and zero-evaluation-read bindings verify. Otherwise stop and preserve both
campaigns; do not cherry-pick passing rows across versions. Non-Go first-pass
matrix results remain unchanged. This does not expand the 1,200-teacher-draft
budget, the source queue, the one-correction allowance, or any release gate.
