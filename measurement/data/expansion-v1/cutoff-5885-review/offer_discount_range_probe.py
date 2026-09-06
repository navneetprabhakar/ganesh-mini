import unittest
from solution import OfferDirectory


class OfferDiscountTests(unittest.TestCase):
    def test_out_of_range_integer_discount_raises_value_error(self):
        offer = {"id": 1, "code": "x", "starts_at": 0, "ends_at": 0, "discount": 10**400, "active": True, "metadata": {}}
        with self.assertRaises(ValueError):
            OfferDirectory([offer])


if __name__ == "__main__":
    unittest.main()
