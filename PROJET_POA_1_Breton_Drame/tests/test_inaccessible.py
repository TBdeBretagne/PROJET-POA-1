import unittest
import json
from main import main

class TestInaccessible(unittest.TestCase):

    def test_simulation(self):
        argv = [
            "main.py",
            "tests/donnees/appartement_inac.json",
            "tests/donnees/scenario_01.json",
            "donnees",
            "tests/sortie/trace_test.json"
        ]
        retour = main(argv)

        self.assertEqual(retour,0)

        with open("tests/sortie/trace_test.json","r", encoding="utf-8") as trace:
            donnees = json.load(trace)

        resume = donnees["resume"]
        livraisons = donnees["livraisons"]

        self.assertEqual(resume["demandes"],4)
        self.assertEqual(resume["reussies"],2)
        self.assertEqual(resume["echecs"],2)

        self.assertEqual(livraisons[0]["motif_echec"],"Résident inaccessible")
        self.assertEqual(livraisons[2]["motif_echec"],"Résident inaccessible")
        
        
        

    

if __name__ == "__main__":
    unittest.main()