import unittest
from solution import Patron


class PatronTextTests(unittest.TestCase):
    def test_nonempty_strings_without_unspecified_trim_requirement(self):
        patron = Patron(" ", " ", " ", " ")
        self.assertEqual(patron.identifier, "Patron: ")


if __name__ == "__main__":
    unittest.main()
