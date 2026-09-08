from scripts.train.prepare_expansion import canonical_digest


def test_canonical_digest_is_key_order_independent():
    assert canonical_digest({"a": 1, "b": 2}) == canonical_digest({"b": 2, "a": 1})
