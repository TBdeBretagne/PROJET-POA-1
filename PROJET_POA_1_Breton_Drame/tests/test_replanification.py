import unittest
from src.chemin import plus_court_chemin

class TestReplanification(unittest.TestCase):
    def test_chemin2(self):
        carte = [
            ["#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", "#", "#", "#", "#"],

        ]

        start  = (1,1)
        goal = [(1,3)]
        chemin = plus_court_chemin(start,goal,carte)

        carte[1][2] = "#"

        nouveauChemin = plus_court_chemin(start,goal,carte)

        
        self.assertNotIn((1,2),nouveauChemin)
        self.assertEqual(nouveauChemin[0],(2,1))
        self.assertEqual(nouveauChemin[-1],(1,3))

        self.assertGreater(len(nouveauChemin),len(chemin))
        


if __name__ == "__main__":
    unittest.main()
