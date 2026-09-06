import math
from solution import AffineTrainer

trainer = AffineTrainer([(0, 0)], [(0, 1e154), (0, 1e154)], 1, 1)
actual = trainer.evaluate()
assert math.isclose(actual, 1e308, rel_tol=1e-15), f"representable mean squared error: {actual!r}"
