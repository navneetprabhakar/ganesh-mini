import math
from solution import build_station_view

station = {"id": "x", "name": "X", "current_c": 2e307, "forecast_c": []}
actual = build_station_view([station], "", "F")
assert math.isclose(actual[0]["current"], 3.6e307, rel_tol=1e-15), repr(actual)
