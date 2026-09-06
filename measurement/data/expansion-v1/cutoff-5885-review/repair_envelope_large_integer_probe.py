import unittest
from solution import monotone_envelope


class ReviewProbe(unittest.TestCase):
    def test_finite_integer_value(self):
        value = 10 ** 400
        self.assertEqual(monotone_envelope([value], 'up'), [value])


if __name__ == '__main__':
    unittest.main()
