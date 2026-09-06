import unittest
from solution import attach_labels


class BoundedDeepHierarchyTests(unittest.TestCase):
    def test_finite_acyclic_chain(self):
        root = {"name": "leaf", "children": []}
        for _ in range(1200):
            root = {"name": None, "children": [root]}
        failure = None
        try:
            attach_labels(root, {})
        except Exception as exc:
            failure = type(exc).__name__
        self.assertIsNone(failure, "Finite depth-1200 hierarchy raised " + str(failure))


if __name__ == "__main__":
    unittest.main()
