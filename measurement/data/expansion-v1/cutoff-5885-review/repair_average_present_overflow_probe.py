import unittest
from solution import average_present


class Probe(unittest.TestCase):
    def test_representable_mean(self):
        self.assertEqual(average_present(iter([1e308, None, 1e308])), 1e308)


if __name__ == '__main__':
    unittest.main()
