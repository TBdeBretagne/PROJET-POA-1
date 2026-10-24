import unittest
from src.dictionnaire import Dictionnaire 
from src import reconfort_io as rio

class TestLecture(unittest.TestCase):
    def test_emotion(self):
        phrase_joie = "La lune est belle ce soir, je suis content."
        phrase_confiance = "La lune est belle ce soir, je suis rassuré."
        phrase_peur = "La lune est rouge ce soir, je suis angoissé."
        phrase_surprise = "La lune est rouge ce soir, je suis surpris."
        phrase_tristesse = "La lune est pleine ce soir, je suis nostalgique."
        phrase_degout = "La lune n'est pas visible ce soir, je suis dégouté."
        phrase_colere = "La lune n'est pas visible ce soir, j'ai la rage."
        phrase_anticipation = "La lune est une super lune ce soir, je suis intrigué."
        phrase_deux_mots = "La lune est belle ce soir, je suis heureux et un peu surpris." 
        phrase_sans_mots = "La lune est belle ce soir."

        dico_obj = Dictionnaire()
        dico_json = rio.charger_dictionnaire("./donnees/dictionnaire.json")

        

        retour_joie = list(dico_obj.findEmotion(phrase_joie,dico_json.get("entrees")))
        retour_confiance = list(dico_obj.findEmotion(phrase_confiance,dico_json.get("entrees")))
        retour_peur = list(dico_obj.findEmotion(phrase_peur,dico_json.get("entrees")))
        retour_surprise = list(dico_obj.findEmotion(phrase_surprise,dico_json.get("entrees")))
        retour_tristesse = list(dico_obj.findEmotion(phrase_tristesse,dico_json.get("entrees")))
        retour_degout = list(dico_obj.findEmotion(phrase_degout,dico_json.get("entrees")))
        retour_colere = list(dico_obj.findEmotion(phrase_colere,dico_json.get("entrees")))
        retour_anticipation = list(dico_obj.findEmotion(phrase_anticipation,dico_json.get("entrees")))
        retour_deux_mots = list(dico_obj.findEmotion(phrase_deux_mots,dico_json.get("entrees")))
        retour_sans_mots = list(dico_obj.findEmotion(phrase_sans_mots,dico_json.get("entrees")))

        self.assertEqual(retour_joie[1],"joie")
        self.assertEqual(retour_joie[2],"faible")

        self.assertEqual(retour_confiance[1],"confiance")
        self.assertEqual(retour_confiance[2],"faible")

        self.assertEqual(retour_peur[1],"peur")
        self.assertEqual(retour_peur[2],"moyenne")

        self.assertEqual(retour_surprise[1],"surprise")
        self.assertEqual(retour_surprise[2],"moyenne")

        self.assertEqual(retour_tristesse[1],"tristesse")
        self.assertEqual(retour_tristesse[2],"faible")

        self.assertEqual(retour_degout[1],"degout")
        self.assertEqual(retour_degout[2],"moyenne")

        self.assertEqual(retour_colere[1],"colere")
        self.assertEqual(retour_colere[2],"forte")

        self.assertEqual(retour_anticipation[1],"anticipation")
        self.assertEqual(retour_anticipation[2],"faible")

        self.assertEqual(retour_deux_mots[1],"joie")
        self.assertEqual(retour_deux_mots[2],"moyenne")

        self.assertEqual(retour_sans_mots[1],None)
        self.assertEqual(retour_sans_mots[2],None)

        
        


if __name__ == "__main__":
    unittest.main()
