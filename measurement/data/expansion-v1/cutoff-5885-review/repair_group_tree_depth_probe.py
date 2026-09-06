import unittest
from solution import group_tree

class Probe(unittest.TestCase):
    def test_finite_chain(self):
        rows = [{'id': str(i), 'parent': str(i-1) if i else None, 'label': 'x'} for i in range(1200)]
        error = None
        try:
            group_tree(rows)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
