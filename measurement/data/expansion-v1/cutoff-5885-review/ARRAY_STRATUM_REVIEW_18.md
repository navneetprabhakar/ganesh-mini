# Array-validation follow-up, batch 18

Completed positions 256–270: 15 new / 279 unique outside-sample inspections.
Nine new holds: **206 additive / 209 including historical three**.

| ID suffix | Finding | Result prefix |
| --- | --- | --- |
| typescript-repair-0114 | A single missing image bypasses validation. | gallery-single-missing-image |
| javascript-generation-0199 | Missing pattern bypasses pattern validation. | queue-summary-missing-pattern |
| javascript-generation-0200 | Finite dimensions yield infinite top despite representable centered coordinate. | label-stack-finite-center |
| javascript-generation-0201 | Positive angle already within range is erased to zero by normalization. | reading-positive-angle |
| javascript-repair-0136 | Missing dependency bypasses dependency validation. | stage-dependency-missing |
| javascript-generation-0204 | Reference proxy hides inherited methods to accommodate incorrect prototype tests. | crate-inheritance-contract |
| typescript-generation-0175 | Missing track bypasses playlist validation. | playlist-store-missing-track |
| typescript-repair-0117 | Required equipment code lost during defensive copy. | loan-equipment-required-code |
| typescript-generation-0176 | Missing allowed kind bypasses constructor validation. | submission-allowed-kind-missing |

All result prefixes refer to sibling -result.json files. All nine runtime
diagnostics failed without timeout in pinned network-disabled/resource-limited
sandboxes; all TypeScript compilations succeeded.

Crate tests explicitly expect undefined from EqualCrate.prototype.volume and
surfaceArea, contrary to ordinary inherited property lookup. The reference proxy
special-cases that lookup. This is another test-accommodation hold, not approval
of an implementation that happens to satisfy original tests.
Label centering uses only two labels: an overflowing intermediate sum turns the
representable first top coordinate into -Infinity. Angle normalization changes
1e-20 to zero despite it already lying within the requested range.

Scoped negative findings: TS repair0113 validates points with for-of (unbounded
spread argument counts and unrepresentable rectangle extents are not new holds);
TS repair0115 and generation0170 copy internally created dense records; JS
generation0202 checks items again in add, so missing items are rejected despite
initial some; JS generation0203 validates with for-of and copies explicit fields;
JS repair0134 maps dense whitespace splits with own-key token lookup.
None is a seven-criterion approval. No training seal or revised partition.

Continue position 271. GCS verified through 200 holds / batch 17, not this batch.
