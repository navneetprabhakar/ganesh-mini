import unittest
from decimal import Decimal
from solution import evaluate_decimal

class Probe(unittest.TestCase):
    def test_hex_integer_literal_domain(self):
        # Integer literals are stated as supported; if hexadecimal is excluded,
        # unsupported syntax must instead raise ValueError, not InvalidOperation.
        try:
            result = evaluate_decimal('0x10')
        except ValueError:
            return
        self.assertEqual(result, Decimal(16))

if __name__ == '__main__':
    unittest.main()
