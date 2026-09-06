# Array-validation follow-up, batch 17

Coverage reconciliation 2026-09-07: the result-prefix list below binds to these
IDs through each preserved receipt's `id`, not a new inspection:
session-render-missing = javascript-generation-0187;
agenda-bullet-missing = javascript-generation-0193;
facet-value-missing = javascript-generation-0195;
catalog-alias-missing = javascript-generation-0197;
interval-missing-endpoints = javascript-repair-0129;
book-tags-missing = javascript-repair-0131;
roster-required-id-copy = javascript-generation-0194;
responsive-menu-missing = typescript-generation-0172;
biography-key-collision = typescript-generation-0173.

Completed positions 241–255: 15 new / 264 unique outside-sample inspections.
Eleven new holds in batch: **197 additive / 200 including historical three**.
Later diagnostics: session-render-missing, agenda-bullet-missing,
facet-value-missing, catalog-alias-missing, interval-missing-endpoints,
book-tags-missing, roster-required-id-copy, responsive-menu-missing,
biography-key-collision (each suffixed -result.json). All runtime assertions
failed without timeout; both later TypeScript compilations succeeded.

The biography finding is a contradictory task contract, not merely a reference
implementation error: required keys for ['A','A','A#2'] are ['A','A#2','A#2'],
which cannot also be unique. No new naming convention is imposed by the probe.
JS repair0125 uses dense string segments and BigInt comparison; no new hold.
Continue position 256. Earlier partial checkpoint follows.

Partial: positions 241–245 inspected; five new / 254 unique outside-sample
inspections. Two new holds: **188 additive / 191 including historical three**.

- TS generation0163 drops a valid required non-enumerable banner ID during an
  unmatched dismissal. banner-required-id-copy-result.json: [0,0,1], 2277 ms.
- JS generation0188 skips a missing flag and serializes it as null instead of
  rejecting the invalid flag. feature-manifest-missing-flag-result.json:
  [1], 464 ms.

Both diagnostic assertions failed without timeout in pinned network-disabled,
resource-limited sandboxes; TypeScript compiled successfully.
TS generation0168 validates a dense fixed numeric tuple and allocates frozen
positions; fractional breakpoint wording is underspecified below 769 and is
not an executed hold. TS repair0109 uses internal dense notice objects.
JS repair0128 checks dense string splits; root double-slash interpretation is
an unresolved wording question, not a confirmed defect. No blanket approvals.

Continue position 246. GCS verified through 189 holds / completed batch 16;
these five inspections postdate it. Frozen sample/partition unchanged.
