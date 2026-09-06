# Targeted follow-up outside the frozen sample

Date: 2026-09-06. This is ten additional contract/reference/original-test
inspections, not an enlarged random sample and not ten seven-criterion passes.
The frozen 300 remain unchanged. Selection comes from the non-array high-signal
hits in `stratum-followup-inventory-v1.json`; all 15 unique hits are now inspected
for those patterns (five were already in the frozen sample).

Every runtime diagnostic uses the unchanged pinned, network-disabled,
resource-limited verifier. `run_review_probe --population cutoff` binds selection
to the manifest's full candidate-file SHA-256, while separately preserving the
original sample SHA. Each result retains the exact original task, diagnostic
task, candidate hash, runtime identity and stdout/stderr. No candidate is edited.

## Confirmed follow-up findings

All ten TypeScript probes compiled successfully, then exited `[0, 0, 1]`
without timeout. Seven records have subscription defects; three sparse probes
overlap two of those and identify one additional record: **eight new holds**.

| ID suffix (all TypeScript) | Targeted finding | Result file | Duration ms |
| --- | --- | --- | ---: |
| repair-0096 | MessageRelay removes first A when the final A's unsubscribe is called; retained A/B becomes B/A | relay-duplicate-result.json | 2650 |
| repair-0100 | ExhibitController has the same registration identity defect | exhibit-duplicate-result.json | 3311 |
| generation-0195 | WorkshopToolbar has the same registration identity defect | toolbar-duplicate-result.json | 3103 |
| generation-0261 | PanelStateStore has the same registration identity defect | panel-duplicate-result.json | 3955 |
| generation-0270 | FixedScaleVault has the same defect, after discarding required immediate callbacks | vault-duplicate-result.json | 3729 |
| generation-0294 | DocumentSignal has the same registration identity defect | document-duplicate-result.json | 3271 |
| generation-0383 | Unsubscribing one child also removes its sibling, despite distinct handles | sequence-subscription-result.json | 3100 |
| generation-0026 | ArchiveService accepts sparse tags and calls repository once instead of invalid/no call | archive-sparse-result.json | 2994 |
| generation-0383 | SequenceChooser accepts sparse choices, allowing undefined cycle entries | sequence-sparse-result.json | 3594 |
| generation-0294 | DocumentSignal accepts sparse tags, changes state and notifies | document-sparse-result.json | 3272 |

0096 and 0100 explicitly promise independent duplicate subscriptions. The four
generation APIs promise registration order and per-subscription unsubscribe
handles without forbidding duplicate functions. All six tests register A/B/A,
invoke the final handle twice, then emit once. `indexOf(listener)` incorrectly
removes the first registration. This is observable without relying on timing,
external services, private fields or unspecified exception behavior.

0383's original test installs a late subscription on each callback and
overwrites its unsubscribe handle, then expects both late subscriptions gone.
The reference's `owner` grouping accommodates that incorrect test. The diagnostic
registers two distinct children once, removes the parent and one child, and
expects the other child to remain. Instead neither child runs. This repeats
the independently observed 0382 issue. The known-bad changes only the aligned
numeric endpoint condition; it retains the same faulty subscription grouping.

Sparse probes use ordinary typed `new Array<string>(1)`, not type assertions,
proxies or injected executable properties. Original dense-array cases do not
exercise holes. 0026 spreads its accepted hole to undefined and calls storage;
0383 spreads holes into its cycle; 0294 keeps holes in its stored/returned tags.

## Negative controls and false positives

- TypeScript generation-0026: the `find(...);` match is an ArchiveRepository
  interface declaration returning `ArchiveEntry | undefined`, not an unsound
  overload. No nullability hold; its separate sparse issue is held above.
- TypeScript repair-0250: DirectorySource interface returns `Record | null`.
  This is not the repair-0208 unsound overload. The reference guards stale
  rejection with generation identity, including reset invalidation; no defect
  established by this targeted review. This is not overall approval.
- TypeScript generation-0270: `owner` denotes an allowance account, not a parent
  subscription. Its owner-grouping heuristic is false positive; its duplicate
  unsubscribe defect is independently reproduced above.
- JavaScript repair-0235: `off(name, listener)` explicitly removes the first
  matching function. `indexOf` is correct for this API, unlike an independent
  unsubscribe closure. The original test also covers A/B/A -> B/A. A dedicated
  `signal_first_match_control.js` preserves this expected behavior separately:
  sandbox exit `[0]`, no timeout, 350 ms, result in
  `signal-first-match-control-result.json`. No hold.

## Boundaries and next review

The initial v1 scope remains 11 strata / 2,567 records, not a rejection count.
This targeted follow-up does not clear those strata or imply an unbiased defect
rate. There are now 50 additive holds, 53 including the historical three.
Known-bad provenance and all seven criteria have not been newly audited for
each outside-sample record. Next distinguish external array validation from
internal dense-array transformations, and resolve incomplete API, numeric
envelope and non-triviality findings. Preserve the original population and
reports; no generation restart, training seal, or new VM.
