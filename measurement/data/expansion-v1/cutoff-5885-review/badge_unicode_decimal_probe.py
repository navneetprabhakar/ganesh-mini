from solution import BadgeCodePolicy

digit = "١"
assert digit.isdecimal()
actual = BadgeCodePolicy().assess("Aa" + digit + "@")
assert actual == {"level": "weak", "missing": ()}, repr(actual)
