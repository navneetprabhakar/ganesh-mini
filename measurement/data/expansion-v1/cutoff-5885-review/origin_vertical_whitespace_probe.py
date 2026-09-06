from solution import analyze_origins

# Vertical tab is whitespace after the prefix, not one of the specified endings.
actual = analyze_origins("Origin:\vAlpha")
assert actual == (["Alpha"], {"alpha": 1}, ("alpha", 1)), repr(actual)
