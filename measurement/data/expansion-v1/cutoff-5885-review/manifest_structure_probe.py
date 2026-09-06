import unittest
from solution import validate_manifest


class ReviewProbe(unittest.TestCase):
    def test_unexpected_nested_locator(self):
        self.assertFalse(validate_manifest('<manifest name="m"><source name="s" kind="tiles" profile="plain"><locator>x<extra/></locator></source></manifest>'))

    def test_unexpected_source_text(self):
        self.assertFalse(validate_manifest('<manifest name="m"><source name="s" kind="tiles" profile="plain">extra<locator>x</locator></source></manifest>'))

    def test_unexpected_source_tail(self):
        self.assertFalse(validate_manifest('<manifest name="m"><source name="s" kind="tiles" profile="plain"><locator>x</locator></source>extra</manifest>'))


if __name__ == '__main__':
    unittest.main()
