import unittest
from decimal import Decimal, localcontext
from solution import apply_growth

class GrowthZeroProbe(unittest.TestCase):
    def test_minus_hundred_percent_zero_period_is_identity(self):
        self.assertEqual(apply_growth(Decimal('10'), Decimal('-100'), Decimal(0), 'compound'), Decimal('10'))

    def test_zero_period_preserves_principal_beyond_context_precision(self):
        with localcontext() as context:
            context.prec = 5
            principal = Decimal('123456789.123456789')
            self.assertEqual(apply_growth(principal, Decimal('25'), Decimal(0), 'compound'), principal)

if __name__ == '__main__':
    unittest.main()
