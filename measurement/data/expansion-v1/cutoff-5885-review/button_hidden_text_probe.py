import unittest
from solution import collect_button_actions


class VisibleButtonTests(unittest.TestCase):
    def test_script_text_not_visible_button_label(self):
        self.assertEqual(collect_button_actions('<button data-action="save">Save<script>hidden()</script></button>'), {"Save": "save"})


if __name__ == "__main__":
    unittest.main()
