from solution import polynomial_families_match

actual = polynomial_families_match([[2 ** 53]], [[2 ** 53 + 1]], [0], tolerance=0)
assert actual is False, 'distinct integer constants differ by one, not zero'
