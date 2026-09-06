from solution import check_allocation

value = 10 ** 400
assert check_allocation([{"id": "a", "m": value}], [{"source_id": "a", "m": value}], "m") is None
