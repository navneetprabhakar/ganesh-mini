import unittest
from solution import relax


class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(relax([1e308, 1e308, 1e308], 1), [1e308, 1e308, 1e308])


if __name__ == '__main__':
    unittest.main()
