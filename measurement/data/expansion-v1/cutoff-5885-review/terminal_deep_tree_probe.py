import unittest

from solution import collect_terminals


class DeepTreeTests(unittest.TestCase):
    def test_finite_valid_deep_tree(self):
        node = {"name": "leaf", "details": {"category": "c", "region": "r"}, "children": []}
        for _ in range(1500):
            node = {"name": "branch", "details": None, "children": [node]}
        self.assertEqual(collect_terminals(node), [{"name": "leaf", "category": "c", "region": "r"}])


if __name__ == "__main__":
    unittest.main()
