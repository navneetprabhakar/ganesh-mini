import unittest
from solution import bundle_order

class Probe(unittest.TestCase):
    def test_finite_acyclic_chain(self):
        graph = {str(i): [str(i+1)] if i < 1199 else [] for i in range(1200)}
        error = None
        try:
            bundle_order(graph, '0')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
