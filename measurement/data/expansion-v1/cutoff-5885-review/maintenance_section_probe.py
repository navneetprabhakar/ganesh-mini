import unittest
from solution import MaintenanceCard


class SectionValidationTests(unittest.TestCase):
    def test_unhashable_unknown_section(self):
        card = MaintenanceCard("asset")
        with self.assertRaises(ValueError):
            card.apply_section({}, [])


if __name__ == "__main__":
    unittest.main()
