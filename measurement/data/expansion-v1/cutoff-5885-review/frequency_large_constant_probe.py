from solution import frequency_profile

actual = frequency_profile([1e308, 1e308])
assert actual[0] == 1e308, f"constant signal DC magnitude: {actual[0]!r}"
