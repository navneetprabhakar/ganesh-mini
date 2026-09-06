import unittest

from solution import resolve_encounter


class FirstTargetTests(unittest.TestCase):
    def test_fire_changes_only_first_target_occurrence(self):
        target = {"x": 1, "y": 8, "health": 2, "points": 1}
        state = {"player": {"x": 1, "y": 1, "health": 3, "lives": 1},
                 "targets": [target, target], "score": 0, "boosts": [], "ended": False}
        result = resolve_encounter(state, {"dx": 0, "dy": 0, "fire": True})
        self.assertEqual([item["health"] for item in result["targets"]], [1, 2])
        self.assertEqual(target["health"], 2)


if __name__ == "__main__":
    unittest.main()
