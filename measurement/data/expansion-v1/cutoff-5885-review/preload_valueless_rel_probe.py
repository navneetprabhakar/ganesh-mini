import unittest
from solution import extract_preload_and_image_links


class PreloadRecoveryTests(unittest.TestCase):
    def test_valueless_rel_does_not_abort_recoverable_document(self):
        self.assertEqual(
            extract_preload_and_image_links('<img src="a"><link rel href="ignored"><img src="b">'),
            ["a", "b"],
        )


if __name__ == "__main__":
    unittest.main()
