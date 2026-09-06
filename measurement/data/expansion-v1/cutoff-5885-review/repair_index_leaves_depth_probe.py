import unittest
from solution import index_leaves

class Probe(unittest.TestCase):
    def test_contract(self):
        value = {'leaf': 1}
        for _ in range(1200):
            value = {'branch': value}
        error = None
        try:
            index_leaves(value)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
