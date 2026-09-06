import unittest
from solution import collect_entries

class Probe(unittest.TestCase):
    def test_valid_void_markup_does_not_unclose_article(self):
        html = '<article data-rank="1" data-score="2"><h2>Title</h2><br><span class="contributor">Ada</span></article>'
        self.assertEqual(collect_entries([html]), [dict(rank=1, title='Title', contributors=['Ada'], score=2.0)])

if __name__ == '__main__':
    unittest.main()
