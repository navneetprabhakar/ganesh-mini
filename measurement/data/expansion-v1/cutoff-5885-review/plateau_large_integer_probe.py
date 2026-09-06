from solution import locate_plateaus

value = 10 ** 400
assert locate_plateaus([[value]], 0) == [{'row': 0, 'column': 0, 'value': value}]
