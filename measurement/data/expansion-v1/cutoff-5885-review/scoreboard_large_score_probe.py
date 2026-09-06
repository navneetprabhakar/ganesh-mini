import unittest
from solution import render_scoreboard


class ScoreboardIntegerTests(unittest.TestCase):
    def test_large_score_fits_requested_width(self):
        score = 10**4500
        text = render_scoreboard((("x", score),), 4504)
        self.assertEqual(text.split("\n")[2], "x..1" + "0" * 4500)


if __name__ == "__main__":
    unittest.main()
