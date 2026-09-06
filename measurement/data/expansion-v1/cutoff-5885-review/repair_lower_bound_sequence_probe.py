import unittest
from solution import lower_bound


class Probe(unittest.TestCase):
    def test_set_is_not_sequence(self):
        with self.assertRaises(ValueError):
            lower_bound({1}, 1)


if __name__ == '__main__':
    unittest.main()
