from solution import advance_cart

actual = advance_cart({'x': 5.0, 'y': 5.0, 'heading': 0.0}, (1e308, 1e308), (10.0, 10.0))
print(repr(actual))
assert actual == {'x': 10.0, 'y': 5.0, 'heading': 0.0}, 'straight motion must not change y'
