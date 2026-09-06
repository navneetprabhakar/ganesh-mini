import math
from solution import RoverController

rover = RoverController(1, 1e308, captured=True)
rover.update([], 2.0)
direction = rover.get_direction()
assert all(math.isfinite(value) for value in direction), repr(direction)
assert math.isclose(math.hypot(*direction), 1.0), repr(direction)
