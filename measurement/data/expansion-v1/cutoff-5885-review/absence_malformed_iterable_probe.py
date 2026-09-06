import unittest

from solution import build_absence_report


class MalformedAbsenceTests(unittest.TestCase):
    def test_noniterable_absence_raises_value_error(self):
        with self.assertRaises(ValueError):
            build_absence_report({"a": "g"}, [
                {"day": 1, "absent": None, "unreported_groups": []}
            ], 1)


if __name__ == "__main__":
    unittest.main()
