# Gate 2 V5 budget clarification addendum — 2026-09-16

Status: sealed pre-execution clarification

Applies to: `capability-stratified-v5-interface-replay/v1`

Base plan SHA-256:
`132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b`

Source-feasibility addendum SHA-256:
`01a8415fa9122f163aa58f5cf6578bb1ff2502346cb197a11af14b373d922da3`

## Conflict

The source-feasibility addendum prospectively lowers the absolute terminal
candidate budget from 66 to 65 and the absolute new V5 teacher-generation
budget from eight to seven, but one sentence retains the earlier allowance of
up to six generated reserves. With an ordered 60-candidate first pass and two
fresh primary teacher generations, six reserves would require 66 terminal
candidates and eight new teacher generations. Those statements cannot all be
satisfied.

No V5 model call occurred before this conflict was detected.

## Binding clarification

The stricter absolute budgets control. Replace every effective V5 allowance of
up to six generated reserves with **up to five generated reserves**.

The resulting exact budgets are:

- ordered first pass: exactly 60 candidates, comprising 58 immutable carries
  and two fresh primary teacher generations;
- prebound conditional reserve sources: exactly 59;
- generated reserves: 0–5, only for rejected cells after every first-pass
  threshold passes;
- absolute terminal candidate budget: 65; and
- absolute new V5 teacher-generation budget: seven, comprising two fresh
  primaries plus at most five reserves.

If six or more first-pass cells are rejected, V5 fails even if the aggregate
threshold arithmetic would otherwise pass. No sixth reserve may be generated.
The first-pass-only `graph_and_tree/java/repair` rule and every other source-
feasibility addendum constraint remain unchanged.

## Precedence and hard stop

This clarification takes precedence only where the base plan or source-
feasibility addendum says six reserves, 66 terminal candidates, or eight new
teacher generations. All other frozen requirements remain unchanged.

Stop before any V5 model call unless the cohort, readiness, generation,
terminal-accounting, admission, and qualification paths bind this file and
enforce the 60 + 5 = 65 terminal ceiling and 2 + 5 = 7 new-teacher ceiling.
This addendum authorizes no GCloud action, training, evaluation opening,
publication, or release claim.
