import unittest
from solution import is_well_nested


class Probe(unittest.TestCase):
    def test_invalid_character_after_mismatch(self):
        for text in (')a', '(]a'):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    is_well_nested(text)


if __name__ == '__main__':
    unittest.main()
