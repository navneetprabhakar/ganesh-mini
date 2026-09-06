import unittest
from solution import installation_order


class ReviewProbe(unittest.TestCase):
    def test_finite_acyclic_chain(self):
        names = [f'p{i:04d}' for i in range(1100)]
        graph = {name: names[i+1:i+2] for i, name in enumerate(names)}
        error = None
        try:
            order = installation_order(graph)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(order, list(reversed(names)))


if __name__ == '__main__':
    unittest.main()
