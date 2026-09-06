import unittest
from solution import extract_resource_links


class Probe(unittest.TestCase):
    def test_malformed_ports_ignored(self):
        for url in ('https://example.com:abc/file.seg', 'https://example.com:65536/file.seg'):
            with self.subTest(url=url):
                self.assertEqual(extract_resource_links(url), [])


if __name__ == '__main__':
    unittest.main()
