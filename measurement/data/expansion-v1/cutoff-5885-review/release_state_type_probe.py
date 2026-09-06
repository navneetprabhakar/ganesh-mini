import unittest
from solution import ReleaseIndex, ReleaseDetail


class ReleaseStateTypeTests(unittest.TestCase):
    def test_malformed_state_raises_value_error(self):
        releases = [dict(slug='s', headline='H', body='', published_at=0, state=[])]
        for renderer in (lambda: ReleaseIndex().render(releases), lambda: ReleaseDetail().render(releases, 's')):
            with self.subTest(renderer=renderer), self.assertRaises(ValueError):
                renderer()


if __name__ == '__main__':
    unittest.main()
