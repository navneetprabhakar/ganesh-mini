import unittest
from solution import ParcelLedger


class ParcelIntegerTests(unittest.TestCase):
    def test_finite_integer_coordinate(self):
        ledger = ParcelLedger()
        record = {"parcel_id": "p", "mass": 0, "position": {"x": 10 ** 400, "y": 0}, "labels": []}
        ledger.put(record)
        self.assertEqual(ledger.get("p"), record)


if __name__ == "__main__":
    unittest.main()
