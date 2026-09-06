from solution import collect_readings

snapshot = {'offers': [(1, 1e308), (2, 1e308)], 'requests': [(1, 1e308), (2, 1e308)], 'value': 1}
actual = collect_readings([snapshot], 1, 1)
print(repr(actual))
assert len(actual) == 1 and actual[0].imbalance == 0.0, 'identical sides must have zero imbalance'
