import unittest
from solution import find_nodes


class Probe(unittest.TestCase):
    def test_finite_tree(self):
        tree = {'id': 'leaf', 'tag': 'x', 'children': []}
        for i in range(1100):
            tree = {'id': str(i), 'tag': 'x', 'children': [tree]}
        error = None
        try:
            result = find_nodes(tree, '1099', 'absent')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
