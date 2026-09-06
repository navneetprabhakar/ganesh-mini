import unittest
from solution import attach_labels


class DeepHierarchyTests(unittest.TestCase):
    def test_finite_acyclic_chain(self):
        root = {"name": "leaf", "children": []}
        for _ in range(1200):
            root = {"name": None, "children": [root]}
        result = attach_labels(root, {"leaf": {"x": "y"}})
        for _ in range(1200):
            result = result["children"][0]
        self.assertEqual(result["attributes"], {"x": "y"})


if __name__ == "__main__":
    unittest.main()
