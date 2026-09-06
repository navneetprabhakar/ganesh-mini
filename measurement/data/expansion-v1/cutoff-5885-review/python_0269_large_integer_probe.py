from solution import bucket_metrics

large = 10 ** 400
assert bucket_metrics([{"id": "a", "metrics": {"x": large}}], {"x": large}) == {
    "x": {"below": [], "at_or_above": ["a"]}
}
