import unittest
from solution import build_hierarchy

class Probe(unittest.TestCase):
    def test_missing_ancestor_has_required_error(self):
        rows = [{'id': 'child', 'parent_id': 'parent', 'label': '', 'metadata': {}}, {'id': 'parent', 'parent_id': 'missing', 'label': '', 'metadata': {}}]
        with self.assertRaises(ValueError):
            build_hierarchy(rows)

    def test_finite_nested_metadata(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            build_hierarchy([{'id': 'x', 'parent_id': None, 'label': '', 'metadata': {'value': value}}])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
