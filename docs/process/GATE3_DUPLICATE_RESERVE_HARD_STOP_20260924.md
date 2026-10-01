# Gate 3 duplicate-reserve hard stop — 2026-09-24

Status: HARD STOP. No final 546/720/900-row admission or training claim.

The sealed 16-reserve matrix admitted 15 and rejected one; the one permitted
blind reauthor subsequently admitted that Go rejection. Those executable
outcomes are preserved. But the provisional 546-row assembly rejected the
cohort at 546 rows / only 545 unique candidate IDs. The identified duplicate
also shares its source identity, so there are at most 545 unique sources.
There is no output directory or corpus seal from that failed assembly.

The duplicate is
`cap-scale-associative_aggregation-python-repair-reserve-06`, source
`m-a-p/MdEval-Instruct` at revision
`38c9197e3add996fae624eb198ebd06155b2101e`, record `row-02462`, source
SHA-256 `f17e2f6bc73c231122e44dc0960b2c892b7ce87c721ac7c66d3376b47770191e`.
The canary-final admitted candidate is sealed by canary report
`dc239958fc66b793830a19c254c54cdfad316263cc0eb04607a0e76454a13ad3`
and has candidate content hash
`a1613bee30bf549f2d86d3ce5d1415f487679a499b729793dc2347ea3e028a6e`.
The later reserve attempt used the same queue request, ID, and source but
different candidate content hash
`8b23c4178d83ff0e5ba07432de51c55eedbf17b4192079d78bcc503edd7afb38`.
Neither may be counted as a second source-unique training row.

The cell `associative_aggregation/python/repair` has one retained training
entry row, one unique canary reserve admission, three first-pass admissions,
and one first-pass rejection:
`cap-scale-associative_aggregation-python-repair-first_pass-02`.
That rejection passed both reference suites and failed `known_bad.cross_cutting`;
it was not eligible for the frozen blind test-reauthor route. The sealed queue
allocates only reserve-06 to this cell, already consumed by the canary. Thus
the cell has five unique admissions against the frozen six-row target. The
reserve-chain ledger failed to account for canary-consumed reserves and must
not be reused for a final admission claim.

The 1,200 teacher-draft cap was not exceeded: counted usage is 1,058/1,200,
including the duplicated later draft. Evaluation content was not opened by
the failed assembly, and no GCloud action occurred. Further generation,
reserve activation, separation, packaging, or training under the current
queue is stopped. Preserve every prior artifact. A new prospective resolution
must explicitly handle the canary reserve ownership and this one-cell deficit
without retroactively rewriting the failed evidence or weakening uniqueness.
