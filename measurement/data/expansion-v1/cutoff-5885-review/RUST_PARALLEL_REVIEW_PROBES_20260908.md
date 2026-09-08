# Parallel-review numeric probes

2026-09-08. Main-agent follow-up to static holds in batches22/23. Original
candidate corpus and tests remain unchanged; separate diagnostic tests ran
against the frozen references in the pinned Rust1.85.0 sandbox.

| Candidate | Result | Evidence |
| --- | --- | --- |
| exp-v1-rust-repair-0361 | Compiled0, test101; elapsed MAX−1,MAX,1 with interval MAX returns0,1,0 instead of0,1,1.1504ms; no timeout. | rust-repair0361-carried-time-result.json |
| exp-v1-rust-repair-0382 | Compiled0, test101; finite samples2e200 and1e200 with query0 select farther outcome2 instead of1.1740ms; no timeout. | rust-repair0382-finite-nearest-result.json |

Both holds already existed; these executions add corroboration, not new holds
or inspection counts. Full JSON preserves original/diagnostic tasks, candidate
and output hashes, raw outputs, commands and exact runtime identity.
Network disabled,1CPU,512MiB,64PIDs,60s limits; image manifest
f7a845c048ec8b96df961b9b1b754dcfcf5e2f824401e59cca0a1c42d64c2192;
sandbox contract b64089f9f047e0b6b0a475e6c2f19ea9451d2480109ad08abb1b2561f7070e6e.
No training, admission or release result is implied.
