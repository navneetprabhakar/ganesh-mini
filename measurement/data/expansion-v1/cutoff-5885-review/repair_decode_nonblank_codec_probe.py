import unittest
from solution import decode_nonblank


class Probe(unittest.TestCase):
    def test_non_text_codec_validation(self):
        with self.assertRaises(ValueError):
            decode_nonblank(b'x', ('base64_codec',))


if __name__ == '__main__':
    unittest.main()
