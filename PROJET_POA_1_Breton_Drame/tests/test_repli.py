import unittest
from src.armoire import Armoire
from src import reconfort_io as rio

#La fonction fouiller a en argument 2 fonctions, pour les tests on passe une fonction vide
def fct_vide(*args, **kwargs):
            #args n'importe quel nombre argument position
            #kwargs n'importe quel nombre argument nommé
            pass


class TestSelecteur(unittest.TestCase):

    def setUp(self):
        self.armoire_json = rio.charger_armoire("tests/donnees/armoire_test.json")
        self.armoire_obj = Armoire(self.armoire_json)
        self.armoire_obj.selecteur = [0, 0]
        

    def test_garni(self):
        retour = list(self.armoire_obj.fouillerCasier([2,0],self.armoire_json.get("casiers"),fct_vide,fct_vide))
        self.assertEqual(retour[0], "guirlande lumineuse")
        self.assertEqual(retour[2],"aucun")

    def test_repli_intensite(self):
        retour = list(self.armoire_obj.fouillerCasier([2,1],self.armoire_json.get("casiers"),fct_vide,fct_vide))
        self.assertEqual(retour[0], "coussin")
        self.assertEqual(retour[2],"intensite")

    def test_repli_voisine(self):
        retour = list(self.armoire_obj.fouillerCasier([2,2],self.armoire_json.get("casiers"),fct_vide,fct_vide))
        self.assertEqual(retour[0], "coussin")
        self.assertEqual(retour[2],"voisine_1")

    def test_vide(self):
        retour = list(self.armoire_obj.fouillerCasier([2,4],self.armoire_json.get("casiers"),fct_vide,fct_vide))
        self.assertEqual(retour[0], None)
        self.assertEqual(retour[2],"vide")

if __name__ == "__main__":
    unittest.main()