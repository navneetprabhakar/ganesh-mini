import unittest
from solution import MembershipBoard


class TeamRoleCollisionTests(unittest.TestCase):
    def test_pending_team_does_not_allow_reverification(self):
        board = MembershipBoard(["pending"])
        board.add_member("m")
        board.verify("m")
        board.choose_team("m", "pending")
        with self.assertRaises(ValueError):
            board.verify("m")


if __name__ == "__main__":
    unittest.main()
