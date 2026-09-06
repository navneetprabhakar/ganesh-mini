import unittest
from solution import apply_catalog_commands


class CategoryIsolationTests(unittest.TestCase):
    def test_add_affects_only_named_category(self):
        items = []
        item = {"sku": "x", "label": "X", "price_cents": 0}
        result = apply_catalog_commands({"a": items, "b": items},
                                         [{"op": "add", "category": "a", "item": item}])
        self.assertEqual(result, {"a": [item], "b": []})


if __name__ == "__main__":
    unittest.main()
