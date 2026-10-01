# Gate 0B passed-run raw-report recovery: local audit

Date: 2026-10-01 IST
Scope: read-only local repository, local staging, and Git-history checks. No GCloud call, evidence mutation, or new qualification was performed.

## Exact missing object

The admitted Gate 0B run is `20260824T180957Z`. Its sealed
`measurement/cuda/gcloud/20260824T180957Z/run-result.json` and
`backup-verification.json` bind the original raw report
`output/gate0b-l4-flex-east1-fused-v1/qualification-bf16-lora-primary-v1.json`
at GCS generation `1787598922015862`, size `97,283` bytes, SHA-256
`ac9d809739def7fb67838c77221681b1db5cb8a32f655e82ddfd95647ce94c1b`.
The canonical admitted summary is
`measurement/gate0/cuda_qualification.json`, but it is not the raw report.

## Checks and result

- A repository-wide exact-size search found no regular file of 97,283 bytes.
- Every local file named `qualification-bf16-lora-primary-v1.json` under the
  repository, including hidden `.gcloud-staging`, was SHA-256 checked. They are
  older failed/other-run reports; none matches the pinned digest.
- Git history for the Gate 0B evidence paths contains the sealed passed-run
  manifests and older raw reports, but not this passed-run raw-report path.
- The previously preserved read-only provider checks in
  `measurement/gate3/capability-scale-v1/hardware-floor-reconciliation-v1/`
  show the exact generation download, current object, historical prefix, and
  all-version lookup unavailable at the time checked. The recorded related
  archive-root searches did not supply a replacement.
- `tests/cuda/test_admit_gate0b.py` and
  `tests/cuda/test_gate0b_l4_v14_fused_result.py` pass (4 tests). This verifies
  the retained sealed summary/manifests, **not** present possession of the
  original raw bytes.

This is a bounded negative search, not proof that every backup copy is lost.
Do not reconstruct a report from the summary or relabel an older run as the
passed run. Gate 0B's historical admission can remain recorded, but the
raw-report recovery gap remains a final-release evidence hold.

## Fail-closed resolution

1. Search external local/system backups or a restored original object/version
   for the exact 97,283-byte report. Admit it only if SHA-256 matches the
   pinned digest, and preserve its retrieval provenance alongside the bytes.
2. If exact recovery is impossible, design and separately authorize a new
   bounded Gate 0B qualification that produces a new immutable raw report and
   complete backup/inventory/teardown evidence. Treat it as a prospective
   requalification, not a repair or reconstruction of the historical run.
3. Until either route is independently sealed and reviewed, do not claim that
   the raw-report release hold is cleared or publish the model on that basis.
