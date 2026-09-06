from fractions import Fraction
from solution import MonotoneRisk

score = Fraction(10 ** 30 + 1, 10 ** 30)
assert score > 1 and float(score) == 1.0
try:
    MonotoneRisk([score])
except ValueError:
    pass
else:
    raise AssertionError('out-of-range exact real accepted after float rounding')
