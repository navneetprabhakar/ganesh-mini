# Python generation review, batch 7

Positions 91–105 of 684, v6 outside-sample Python generation queue. Fifteen full
prompt/reference/original-test inspections. Ten additive holds: eight reproduced
and two static contract contradictions. 520 additive plus historical three =
523 holds; 1,338 unique outside-sample inspections. No admission approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 91 | 0100 | Exact ASCII tracking grammar, validated string subclass and frozen Parcel conversion agree. Explicit max_length=9 is retained, not inferred as a separate length check. No new hold. |
| 92 | 0101 | Lower-middle balanced construction, distinct duplicate nodes and inorder generator agree. Integer-subclass acceptance and arbitrary deep external trees remain pending; no new hold. |
| 93 | 0102 | Hold: accepted finite integer query 10**400 overflows math.isfinite despite zero coefficient and exact forecast 7.0. |
| 94 | 0099 | Hold: 4,501-digit nonnegative score that fits a 4,504-character row is rejected by pinned integer conversion limit. Exact-int subclasses and Unicode newline scope remain pending. |
| 95 | 0104 | ASCII key grammar, first separator, line-number errors and replacement order agree. No new hold. |
| 96 | 0105 | Static hold: prompt permits nonempty names without a stripping rule; original tests and reference reject whitespace-only names. Copy-failure name reservation and side-effectful equality remain separate pending concerns. |
| 97 | 0106 | Hold: unhashable environment raises TypeError instead of ValueError for any unsupported environment. Whitespace-only database URL restriction remains a separate wording question. |
| 98 | 0108 | Hold: valid limit=1500,width=5000 raises ValueError at final integer-to-string conversion. Modular powers themselves complete; no timeout. |
| 99 | 0103 | Static hold: accept says preserve application order, report says registration order; original test accepts Bob before Alice but expects Alice before Bob. Conflicting order contract needs resolution, not a guessed canonical ordering. |
| 100 | 0107 | Hold: special-case +3 bonus for the nine unique pairs matches incorrect original (60,60) expectation; per-rule sum and individual calls give (57,57). |
| 101 | 0109 | Hold: premature float conversion loses one before integer offset cancellation, exporting V 0 0 0 instead of V 1 0 0. |
| 102 | 0111 | Hold: equal finite halves overflow sums and yield NaN turn rather than zero. Validation-before-false-start and ordinary action ordering agree. |
| 103 | 0112 | Active-path cycle detection permits shared noncyclic children, sorted DFS and name checks agree. Recursion-depth envelope pending; no new hold. |
| 104 | 0113 | Byte-length framing, strict decoding and incomplete-frame handling agree. Lone-surrogate encode-domain wording and enormous frame boundary remain pending; no new hold. |
| 105 | 0114 | Hold: nonempty netloc with no hostname is accepted as base and retained as resolved link. Malformed URL recovery remains a separate scope question. |

Eight probes ran in pinned Python 3.11.15, network disabled and resource limited;
each exited 1 without timeout. Static contradictions are not executed results.
Original candidates/tests remain frozen; all probe/task/runtime hashes retained.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0102 | forecast_integer_probe.py / forecast-integer-result.json | 464 | OverflowError in finite integer validation. |
| 0099 | scoreboard_large_score_probe.py / scoreboard-large-score-result.json | 465 | 4,300-digit conversion limit rejects valid fitting score. |
| 0106 | web_config_environment_probe.py / web-config-environment-result.json | 397 | TypeError for environment=[]. |
| 0108 | self_power_wide_suffix_probe.py / self-power-wide-suffix-result.json | 546 | ValueError converting completed modular sum; subsequent assertions not reached. |
| 0107 | gesture_additivity_probe.py / gesture-additivity-result.json | 463 | Individual-round sum assertion passes at 57; combined result is 60. |
| 0109 | model_offset_exactness_probe.py / model-offset-exactness-result.json | 426 | Offset cancellation exports zero rather than one. |
| 0111 | rescue_equal_finite_probe.py / rescue-equal-finite-result.json | 409 | TURN is NaN for four equal 1e308 readings. |
| 0114 | guide_missing_host_probe.py / guide-missing-host-result.json | 516 | Both missing-host base rejection and link filtering assertions fail. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 106. No changed frozen sample, partition, VM or training seal.
