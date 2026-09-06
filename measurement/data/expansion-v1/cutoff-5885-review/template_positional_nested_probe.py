import unittest
from solution import required_template_fields


class TemplatePositionalNestedTests(unittest.TestCase):
    def test_nested_fields_rejected_even_for_ignored_root(self):
        for template in ('{0:{width}}', '{:{width}}'):
            with self.subTest(template=template), self.assertRaises(ValueError):
                required_template_fields(template)


if __name__ == '__main__':
    unittest.main()
