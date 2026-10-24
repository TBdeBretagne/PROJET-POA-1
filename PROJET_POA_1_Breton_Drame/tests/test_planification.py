import unittest
from src.chemin import plus_court_chemin

class TestChemin(unittest.TestCase):
    def test_chemin(self):
        carte = [
            ["#", "#", "#", "#", "#"],
            ["#", ".", "#", "#", "#"],
            ["#", ".", "#", "#", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", "#", "#", "#", "#"],

        ]

        start  = (1,1)
        goal = [(3,3)]

        chemin = plus_court_chemin(start,goal,carte)

        self.assertEqual(len(chemin),4)
        self.assertEqual(chemin[0],(2,1))
        self.assertEqual(chemin[-1],(3,3))


if __name__ == "__main__":
    unittest.main()
