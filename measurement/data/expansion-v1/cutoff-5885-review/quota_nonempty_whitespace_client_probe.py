from solution import QuotaLedger

ledger = QuotaLedger(1, 2)
# Prompt requires a nonempty string client, not a nonblank client.
assert ledger.observe(" ", 1, "query") == "accepted"
