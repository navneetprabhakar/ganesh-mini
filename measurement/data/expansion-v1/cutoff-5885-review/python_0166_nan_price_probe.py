from solution import replay_orders

event = {"sequence": 1, "symbol": "X", "side": "buy", "quantity": 1, "price": float("nan")}
try:
    replay_orders([event], 100)
except ValueError:
    pass
else:
    raise AssertionError("NaN is not a positive price but was accepted")
