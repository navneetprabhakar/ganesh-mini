# Array-validation follow-up, batch 17

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
