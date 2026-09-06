from solution import aggregate_metrics

value = 10 ** 400
assert aggregate_metrics([{"category": "x", "amount": value, "accepted": True}]) == [
    {"category": "x", "count": 1, "total": value}
]
