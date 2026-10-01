# Gate 2 V6 readiness result — 2026-09-17

Status: terminal pre-campaign readiness failure

Contract: `capability-stratified-v6-canonical-test-replay/v1`

## Result

V6 stopped at its content-free live provider schema-admission smoke and is
sealed `readiness-failed`. The reason is
`json-object-order-validator-impossible-contract`.

The provider accepted the no-path response schema and returned one terminal
structured response containing exactly the two required role objects. It
serialized `cross_cutting` before `primary_discrimination`. The frozen local
validator then raised exactly:

`ValueError: V6 response must contain the two ordered role objects exactly`

JSON object member order is not a semantic property and the provider schema
cannot guarantee it. Consequently, the V6 plan's ordered-object readiness
condition is not satisfiable as written. Section 10 requires V6 to stop and
seal failed on any readiness failure or ordering drift. The validator was not
changed in place and the frozen V6 plan was not edited.

This is a pre-campaign contract failure, not a candidate, corpus-quality,
training, or model-quality result.

## Frozen evidence

- V6 plan file SHA-256:
  `4fe6a1374c01a0a682bf256c91a141b36b26680bdb5279049070f4f143418ec1`
- immutable carry manifest file SHA-256:
  `9023396c74567921a3dcdec3a05e2a1b5aea2cd437b63e7f4d5927cea04f362b`
- immutable carry manifest seal:
  `f95270299363fe003e0f8b747f60071eb813d36b09c9c132198588625a2be8af`
- ordered cohort manifest file SHA-256:
  `2869dcb033bfcfecff6e4f919a78e1f8e754db5aad3e3845991557ce30b47654`
- ordered cohort manifest seal:
  `188d3b5b3e95f71556321dc1262251375d641d8e23b3961c713985b81eb7e9de`
- raw live-smoke artifact file SHA-256:
  `24a0749d8de8d16907c2fb7814169ef64048d76d03b3d248a8cdf92d8e9d305e`
- raw live-smoke artifact seal:
  `2582bfa6b9e1dd98ec7994e31ab129ee4b400fb2947bc1facfc85394b5f54730`
- provider response-schema SHA-256:
  `7faee5a48a1750563d1c47aaea77a488a97943bcba1bf1fac489274343a52822`
- terminal readiness-failure report file SHA-256:
  `71f464e2c0af6e1bc71be894fa28fccdfc14e4cc7cf30ff3f8e51c28034103ca`
- terminal readiness-failure report seal:
  `39a8264850aafb9c8b8db6ed9de4f8d6e0d46b4ad331329a4e2c21c6cce3f778`

The machine-readable report is
`measurement/gate2/capability-stratified-v6-canonical-test-replay/readiness-v1/readiness-failure-report.json`.
Its raw provider artifact is
`measurement/gate2/capability-stratified-v6-canonical-test-replay/readiness-v1/live-schema-runs/v6-live-schema-smoke.test_author.json`.

## Terminal accounting

The one content-free readiness smoke is the only V6 model invocation. Before
the stop:

- candidate test-author calls: 0;
- blind delta-audit calls: 0;
- structural reauthor calls: 0;
- candidate suite executions: 0;
- candidate dispositions: 0;
- V6 qualification metrics emitted: no; and
- evaluation artifacts read: 0.

No V6 candidate test output was admitted and no V6 candidate campaign began.
The 60 carried teacher/semantic rows remain immutable inputs, not V6
qualification outcomes.

## Successor boundary

V6 is terminal and must not be resumed, patched, reinterpreted, or reported as
a qualification result. Any successor must use a new prospective contract. It
may require the exact role-key set while treating JSON member order as
irrelevant, then process roles in a controller-owned canonical order. It must
rerun and pass readiness before any candidate call.
