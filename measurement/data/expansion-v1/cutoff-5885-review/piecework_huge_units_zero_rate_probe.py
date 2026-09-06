from solution import render_piecework_badge

actual = render_piecework_badge(1, 10 ** 400, 0.0)
assert actual == "WORKER = 1\nPAY = CR 0.00", repr(actual)
