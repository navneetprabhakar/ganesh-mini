# Python repair review, batch 9 working notes

Uncheckpointed continuation after batch 8. Positions 121–126 fully read
(prompt, known-bad source, corrected source, original tests); do not add these
to the checkpointed inspection count until the batch reconciliation.

- 121 / 0145: inclusive comparisons repair shelf boundaries; ordinary exact
  and integer-subclass rules agree. No new hold.
- 122 / 0146: row slicing repairs width/left and structural independence;
  cell identity intentionally shared. Invalid grid-container policy unspecified;
  no invented validation requirement or new hold.
- 123 / 0147: removal of inserted space repairs single-hyphen joining, but
  double hyphen also removed. Probe repair_reflow_double_hyphen_probe.py and
  repair-reflow-double-hyphen-result.json: pinned isolated exit 1, no timeout,
  531 ms; 'word-next' instead of 'word-- next'. Pending additive hold entry.
  Blank-line precedence also needs disposition, not guessed.
- 124 / 0148: inclusive delay repairs wait boundary/zero budget; delay/index
  sort and intentional payload identity agree. Non-iterable outer input error
  wording remains unspecified; no new hold.
- 125 / 0149: half factor repairs energy formula. Probe still needed for float
  conversion collapsing adjacent large integer positions and intermediate
  overflow. No execution claim yet.
- 126 / 0150: empty-count guard repairs absent-value mean. Probe still needed
  for [1e308, 1e308] overflow. No execution claim yet.

Resume probes for 0149/0150, then position 127. No seven-criterion approval.
These working notes and the 0147 probe are later than the verified 791-hold
GCS archive. Frozen candidates unchanged.
