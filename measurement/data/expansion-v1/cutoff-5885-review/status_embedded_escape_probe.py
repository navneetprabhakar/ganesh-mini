import unittest
from solution import render_status


class StatusEmbeddedEscapeTests(unittest.TestCase):
    def test_plain_mode_emits_no_escape_characters(self):
        fields = dict(machine='\x1b[31mx', account='', platform='', interpreter='')
        self.assertNotIn('\x1b', render_status(fields, use_color=False))


if __name__ == '__main__':
    unittest.main()
