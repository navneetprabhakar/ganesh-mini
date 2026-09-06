import math
from solution import estimate_channel_delivery

actual = estimate_channel_delivery(1e308, 4.0, 0.5, 0.1)
assert math.isclose(actual["delivered_output"], 2e307, rel_tol=1e-15), repr(actual)
