import unittest
from solution import SampleCatalog

class Probe(unittest.TestCase):
    def test_arbitrary_label_is_isolated(self):
        def label():
            pass
        label.items = [1]
        catalog = SampleCatalog([dict(values=[1], points=[], label=label)])
        catalog[0]['label'].items.append(2)
        self.assertEqual(catalog[0]['label'].items, [1])

if __name__ == '__main__':
    unittest.main()
