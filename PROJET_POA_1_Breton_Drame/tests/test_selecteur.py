import unittest
from src.armoire import Armoire
from src import reconfort_io as rio

class TestSelecteur(unittest.TestCase):

    def setUp(self):
        armoire_json = rio.charger_armoire("tests/donnees/armoire_test.json")
        self.armoire_obj = Armoire(armoire_json)
        self.armoire_obj.selecteur = [0, 0]

    def test_bouclage_Ouest(self):
        self.armoire_obj.selecteur = self.armoire_obj.moveCursor("O")
        self.assertEqual(self.armoire_obj.selecteur, [0, 7])

    def test_bouclage_Est(self):
        self.armoire_obj.selecteur = [0, 7]
        self.armoire_obj.selecteur = self.armoire_obj.moveCursor("E")
        self.assertEqual(self.armoire_obj.selecteur, [0, 0])

    def test_limite_Nord(self):
        self.armoire_obj.selecteur = self.armoire_obj.moveCursor("N")
        self.assertEqual(self.armoire_obj.selecteur, [0, 0])

    def test_limite_Sud(self):
        self.armoire_obj.selecteur = [2, 0]
        self.armoire_obj.selecteur = self.armoire_obj.moveCursor("S")
        self.assertEqual(self.armoire_obj.selecteur, [2, 0])

if __name__ == "__main__":
    unittest.main()