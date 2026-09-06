from solution import SignalGate

gate = SignalGate([1e308, -1e308], "balanced")
actual = gate.evaluate([200.0, 200.0])
assert actual == 0.5, f"equal opposite terms must cancel: {actual!r}"
