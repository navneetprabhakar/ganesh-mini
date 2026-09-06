import unittest
from solution import extract_guide_links


class GuideHostTests(unittest.TestCase):
    def test_base_requires_host_not_only_netloc(self):
        with self.assertRaises(ValueError):
            extract_guide_links("", "https://user@:80/path")

    def test_resolved_link_without_host_is_filtered(self):
        html = '<article data-kind="guide"><a href="https://user@:80/path">x</a></article>'
        self.assertEqual(extract_guide_links(html, "https://valid.test/"), [])


if __name__ == "__main__":
    unittest.main()
