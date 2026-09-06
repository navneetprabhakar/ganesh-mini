import unittest
from solution import encode_flash_message


class MorseNonASCIIExpansionTests(unittest.TestCase):
    def test_nonascii_letters_are_unsupported(self):
        with self.assertRaises(ValueError):
            encode_flash_message('ß')


if __name__ == '__main__':
    unittest.main()
