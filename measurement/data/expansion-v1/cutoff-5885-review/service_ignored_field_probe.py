import unittest
from solution import render_by_service


class IgnoredFieldTests(unittest.TestCase):
    def test_extra_field_need_not_be_copyable(self):
        row = {"carrier": "A", "number": 1, "destination": "X", "platform": "1", "departure": 0, "ignored": iter(x for x in ())}
        self.assertEqual(render_by_service([row], {}), "Service | Destination | Platform | Departure\nA1 | Unknown (X) | 1 | 00:00")


if __name__ == "__main__":
    unittest.main()
