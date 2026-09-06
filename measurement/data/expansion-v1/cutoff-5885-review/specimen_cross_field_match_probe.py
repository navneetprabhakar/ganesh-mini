from solution import query_specimens

record = {"id": 1, "name": "alpha", "collector": "beta", "notes": "gamma", "habitat": "h", "year": 2020}
actual = query_specimens([record], text="alpha\nbeta")
assert actual == {"items": [], "total": 0, "pages": 0}, repr(actual)
