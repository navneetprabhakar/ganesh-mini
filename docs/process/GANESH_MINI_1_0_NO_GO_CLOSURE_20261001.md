# Ganesh Mini 1.0 — no-go project closure

Historical record: later on 2026-10-01 IST, Navneet directed work to
continue despite the failure. The no-go quality finding and incomplete-gate
facts below remain valid; the stop-work request is superseded. See the top of
`docs/process/PROJECT_STATE.md` for current operational status.

Date: 2026-10-01 IST. Decision: close this iteration without publishing a
Ganesh Mini model. Navneet directed improvement work to stop today. This is
a terminal **no-go release decision**, not a claim that Gate 3 or Gate 8
passed.

## Frozen-gate disposition

| Gate | Disposition at closure |
|---|---|
| 0/0B | Upstream/runtime qualification evidence retained; historical 0B raw-report recovery gap remains a release hold. |
| 1 | Frozen private evaluation and correctly served upstream baseline retained. |
| 2 | Authorized seed lineage and admitted 720-capability plus 180-replay Gate 3 data package retained. |
| 3 | **Failed quality.** Both full-epoch learning-rate runs and the canary completed; selected `1e-5` adapter failed the frozen 180-task development criteria. |
| 4–5 | Not run; no main joint SFT or failure-targeted correction. |
| 6 | Not run; the 360 private decision tasks remain unopened and Ganesh v0.1 was not compared on that surface. |
| 7 | Not run; no merged/quantized laptop-certified release artifacts. |
| 8 | **NO-GO** for model release because required earlier gates and release conditions are unmet. |

The sealed 180-task adjudication is
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T020646Z/development-adjudication.json`,
report seal `4177c8e5782481877d0de5e20b861e46886a3c93138bf2d3a8037e4cfe088cd3`.
Upstream passed 20/180 and the selected adapter passed 19/180: 3 paired wins,
4 losses, and 173 ties. Only Python improved at the product-family level
(four of five required); Java and TypeScript each lost one pass (zero lane
regression required). Save/reload passed and output-quality failures did not
increase, but neither overrides the failed checks. The canary tied upstream
at 5/30 for both candidates. These are executed results, not release claims.

## Evidence and resource custody

- The selected development attempt is
  `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T020646Z`.
  It has evaluation exit 0, 375 independently verified terminal GCS objects,
  167 verified local control-mirror objects, and exact VM/disk/network/subnet
  absence checked twice after backup. Its `finalization.json` status is
  `terminal-backup-verified-and-exact-resources-absent-twice`.
- Both full-epoch candidate training runs, the canary, failed startup and
  capacity attempts, frozen data package, and baseline remain immutable
  historical evidence. Do not delete or overwrite them as part of closure.
- The approved Gate 3 GCloud plan SHA is
  `d4659d3b503d4eb0a0a38d5af6129f668ccef7994a7f678e920ced1a5e55dd09`,
  with a $15 absolute incremental ceiling. The last evaluation card's
  conservative combined bound was $13.263870928 including the $5 prior
  allocated reserve and staging/support allowances; this is **not an
  invoice**. Repeated pre-allocation transfer/operation charges are not
  independently reconciled here. Exact run resources are absent, but this
  record does not certify that every account-wide billable item is absent.
- Existing local working-tree changes and untracked evidence are preserved;
  closure does not silently commit, publish, or discard them.

## Publication boundary

Do not upload the model, adapter, GGUF, or a `ganesh-mini-1.0` model card to
Hugging Face as a successful release. Do not claim improvement, laptop
certification, or decision-set performance. An accurate internal no-go report
may cite the sealed aggregate metrics without exposing private prompts or
tests. Any future public sharing of failed-experiment artifacts needs its own
scope and privacy review; it is not the approved Gate 8 model publication.

## If the project is reopened

Resume only after Navneet explicitly reopens improvement work. Preserve the
frozen failure, choose a prospective non-evaluation data or mechanism change,
reconcile cumulative GCloud costs and obtain scope-specific GCloud authority,
pass a new bounded Gate 3 pilot, complete Gates 4–7 as applicable, recover the
Gate 0B raw report, and make a fresh Gate 8 release decision. Do not open the
untouched private decision set to work around the present failed development
result.
