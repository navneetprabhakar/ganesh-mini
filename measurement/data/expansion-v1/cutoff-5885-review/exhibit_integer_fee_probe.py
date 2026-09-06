import unittest
from solution import compile_exhibits, ExhibitKind, ViewingMode


class ExhibitIntegerFeeTests(unittest.TestCase):
    def test_preserve_numeric_fee_value(self):
        fee = 2 ** 53 + 1
        item = dict(code='x', label='X', creator='A', fees={'list': fee, 'current': 1})
        result = compile_exhibits([[item]], ExhibitKind.PHYSICAL, ViewingMode.ONSITE)
        self.assertEqual(result[0].list_fee, fee)


if __name__ == '__main__':
    unittest.main()
