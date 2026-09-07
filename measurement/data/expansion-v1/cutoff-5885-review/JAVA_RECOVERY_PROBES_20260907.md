# Executed recovery probes — Java batch overflow and negative zero

2026-09-07. Frozen references only; no candidate edits or admission changes.

- exp-v1-java-generation-0710: a two-line catalog and Integer.MAX_VALUE batchSize produce IndexOutOfBoundsException, index -2147483648 / size2. Compile/runtime exit codes [0,1], no timeout,3121ms. See java-generation0710-batch-overflow.java and java-generation0710-batch-overflow-result.json.
- exp-v1-java-repair-0460: decodeLongs("-0") returns [0] despite explicit rejection requirement. Compile/runtime exit codes [0,1], no timeout,3090ms. See java-repair0460-negative-zero.java and java-repair0460-negative-zero-result.json.

Both ran in pinned java-21.0.11 image ganesh-mini-java-verify@sha256:fcfc6b2e2a658d43427d7f51adcdd3c557de2159d53b10da5afca41e05fa8440 under the network-disabled resource-limited verifier. Result JSON preserves original task, candidate hash, probe task, image identity, commands and raw output. These confirm existing static holds in batches67/65, not new unique holds.
