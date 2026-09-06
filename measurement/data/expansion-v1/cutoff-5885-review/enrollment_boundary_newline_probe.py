import unittest
from solution import append_enrollment


class EnrollmentNewlineTests(unittest.TestCase):
    def test_forbidden_newline_not_silently_trimmed(self):
        records = []
        with self.assertRaises(ValueError):
            append_enrollment(records, 1, "A\n", 1, "C")
        self.assertEqual(records, [])


if __name__ == "__main__":
    unittest.main()
