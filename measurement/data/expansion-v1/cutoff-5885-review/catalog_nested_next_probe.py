import unittest
from solution import collect_entries


class CatalogNestedNextTests(unittest.TestCase):
    def test_next_link_inside_article_is_still_pagination(self):
        pages = {
            'root': '<article data-title="Root"><a class="detail" href="/r"></a><a rel="next" href="next">Next</a></article>',
            'next': '<article data-title="Next"><a class="detail" href="/n"></a></article>',
        }
        self.assertEqual([item['title'] for item in collect_entries(pages, 'root')], ['Root', 'Next'])


if __name__ == '__main__':
    unittest.main()
