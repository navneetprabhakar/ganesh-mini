from solution import build_report

actual = build_report(2 ** 53 + 1, 2, [0, 0, 0], [0, 0, 0], 0)
assert actual["remainder"] == 1, repr(actual)
