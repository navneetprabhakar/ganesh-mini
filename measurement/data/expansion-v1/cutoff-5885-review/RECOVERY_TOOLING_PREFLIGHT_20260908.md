# Recovery tooling preflight

Read-only inspection of scripts/data/repair_expansion_rejections.py completed
2026-09-08. No teacher invocation or data replacement performed.

The existing tool is not directly suitable for the approved semantic recovery:

- It accepts only behavioral-reference failures and tests accepting known-bad
  implementations, not clarity, API, non-triviality or numeric-domain holds.
- Reference correction preserves prompt text exactly, while approved derived
  recovery may require explicit contract clarification in a new version.
- It retains original candidate IDs and writes output/evidence without
  create-only guards. Do not aim it at the frozen5885 or historical evidence.
- It preserves source transformation text but does not itself establish the
  required new-version parent-candidate hash/ID and independent admission seal.

After review completion, implement or adapt a separate versioned recovery path
with parent binding, immutable outputs, explicit change classification,
independent test lineage, fresh sandbox execution and evaluation separation.
Do not treat trivial held tasks as recovered merely by padding their prompts.
This is a tooling assessment, not a new blocker or an admission claim.
