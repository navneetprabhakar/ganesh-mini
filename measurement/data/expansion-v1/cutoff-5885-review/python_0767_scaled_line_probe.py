import math
from solution import LineDiagnostics

intercept, slope = LineDiagnostics([1e200, 2e200, 3e200], [1.0, 2.0, 3.0]).coefficients()
assert math.isclose(intercept, 0.0, abs_tol=1e-12)
assert math.isclose(slope, 1e-200, rel_tol=1e-12)
