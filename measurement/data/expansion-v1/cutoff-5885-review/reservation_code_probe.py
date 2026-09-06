import unittest
from solution import compile_reservation_views


class ReservationCodeTests(unittest.TestCase):
    def test_unhashable_code_raises_value_error(self):
        events = [{"code": "a", "label": "A", "fee": 0}]
        rows = [{"event_code": [], "party_size": 1, "customer": "C", "contact": "X"}]
        with self.assertRaises(ValueError):
            compile_reservation_views(events, rows)


if __name__ == "__main__":
    unittest.main()
