# Gate 2 V5 schema-compatibility correction — V3

Status: effective and sealed for exactly one content-free live schema-admission
smoke; V3 candidate dispatch remains blocked

Applies to: `capability-stratified-v5-interface-replay/v1`

## Preserved evidence

The exact ordered 60 cohort, 58 immutable V4 teacher carries, two fresh V5
TypeScript teachers, source bindings, evaluation separation, and all V5
budgets remain unchanged. `primary-two-phase-v1` and
`primary-two-phase-v2` remain immutable evidence directories. A successor must
write only to `primary-two-phase-v3`.

V2 produced no post-test cohort, separation result, executable result, final
admission, or qualification artifact. It therefore has no qualification
metrics. Twelve candidates have sealed attempt-local unresolved wrappers; 48
have no V2 pre-separation artifact. These facts are interruption accounting,
not candidate rejection and not a training/model result.

The controlling V2 interruption-accounting report seal is
`4d739a334ce3df4cc9feca6fbbbe291d93f53a1d896fb457f8caba93720d5c69`;
its file SHA-256 is
`0f6a288eb092fa5fab0c28a1ef32aa3f2bf5f1a378930af5665adc4740e9e826`.

## Exact V2 classification

V2 contains fourteen sealed stage-run artifacts and twelve sealed
pre-separation wrappers:

- two semantic-review calls completed with valid structured responses;
- eleven test-author requests were rejected by the provider with HTTP 400
  `invalid_json_schema` before inference, with no structured response and no
  usage;
- one `callbacks_and_events/javascript` semantic-review thread and turn
  started, then the controller was stopped with SIGINT; it has no error,
  structured response, completion event, or usage and is
  `uncommitted-at-operator-stop`; and
- no test-author response or delta-audit response completed.

The eleven schema rejections and the operator-stopped semantic call are
different failure classes. Neither creates a reusable stage response.

## Narrow schema correction

The rejected test-author schema used `uniqueItems` on both `case_ids` arrays.
The provider does not permit that JSON Schema keyword. V3 may remove only the
two `uniqueItems` declarations from the provider-facing V5 test-author schema.
The existing deterministic response validator must continue to reject
duplicate case IDs after generation, so the semantic constraint is not
weakened.

Before V3 dispatch, a sealed correction manifest must bind:

1. this document's final file SHA-256;
2. the V2 interruption-accounting report seal and file SHA-256;
3. the unchanged V5 base plan, source, budget, resilience, cohort, execution,
   semantic-equivalence, and readiness seals;
4. old V2 and corrected V3 controller/adapter hashes;
5. a canonical before/after test-author schema diff proving the only semantic
   change is removal of `uniqueItems`;
6. a local response-validation test proving duplicate case IDs still fail;
7. the exact V3 output root and ordered-candidate-ID hash; and
8. a complete inventory of all prior physical attempts.

The corrected provider-facing schema canonical SHA-256 must be
`e099481a27e5d40923778098eb3c02126ca40e0116565bcd8a224396baf077cc`.
The only authorized smoke harness is
`scripts/data/run_v5_live_schema_admission_smoke.py`, file SHA-256
`9ec1edbadc311c6afc158ba0707589fd506286856eb95d04eaff9de618bfabe1`.
Immediately before the campaign, V3 must perform exactly one content-free live
schema-admission smoke using that exact schema, production Codex configuration,
and pinned CLI identity. The harness must seal its raw command, events, output,
usage, schema hash, config hash, and tool identity. Success requires a
schema-conforming response and a completed turn. Failure hard-stops V3 and the
sealed smoke artifact must record the provider's next rejected keyword or
other exact error. The smoke may establish only that the provider accepts the
schema; its output is not a candidate artifact, cannot be reused as model
evidence, and does not change any call or candidate budget. Zero smokes, more
than one smoke, a different schema hash, or a smoke after candidate dispatch
is a hard stop.

Any other prompt, projection, schema, model, reasoning, service tier,
scheduler, verifier, or candidate-input drift is a hard stop and requires a
separate correction.

## V3 carry and call accounting

V3 may carry exactly 42 completed semantic results after exact-input
validation: 37 V4-equivalent semantics, three V1 completed V5 semantics, and
the two V2 completed semantics. The two V2 rows are
`binary_and_bitwise/javascript` and `binary_and_bitwise/rust`. Eighteen
semantic calls remain. The stopped `callbacks_and_events/javascript` call is
retried with byte-identical input as interruption recovery and its prior
physical attempt remains disclosed.

V3 carries zero test-author results. It must author tests for all 60 candidates.
The eleven prior provider rejections are disclosed physical attempts but not
completed logical calls because the evidence shows no inference response or
usage. Test-author output still passes the unchanged strict local validator.
Delta audit, global separation, executable verification, admission, and
qualification remain entirely pending.

The V3 startup gate must prove `42 + 18 = 60` semantic coverage and `0 + 60 =
60` test-author coverage without overlap. No reserve becomes eligible until a
complete exact-60 first-pass qualification independently satisfies every
frozen threshold.

## Authorization boundary

This correction authorizes exactly the one content-free live schema-admission
smoke above under the standing non-GCloud model-call scope. It does not
authorize V3 candidate dispatch by itself. Candidate dispatch remains blocked
until the smoke passes and sealed V3 carry/attempt manifests plus controller
integration validate through the production CLI. It changes no training,
GCloud, evaluation, publication, or release gate.
