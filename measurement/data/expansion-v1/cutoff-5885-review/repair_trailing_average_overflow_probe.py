import unittest
from solution import trailing_average


class Probe(unittest.TestCase):
    def test_representable_average(self):
        self.assertEqual(trailing_average([1e308, 1e308], 2), [None, 1e308])


if __name__ == '__main__':
    unittest.main()
