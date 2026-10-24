import unittest
import io                               # Permet de récupérer les erreurs affichées
from contextlib import redirect_stderr  # Redirige les erreurs vers un autre flux
import os                               # Permet la gestion de fichier
from main import main


class TestFichiers(unittest.TestCase):
    def test_fichier_inexistant(self):
        erreur = io.StringIO()                          # Création du flux
        chemin_trace = "tests/sortie/trace_test.json"   
        if os.path.exists(chemin_trace):
            os.remove(chemin_trace)                     # Supprime la trace si elle existe déjà

        with redirect_stderr(erreur):                   # Redirige la sortie erreur vers notre flux
            argv = [
                "main.py",
                "fichier_inexistant.json",
                "tests/donnees/scenario_01.json",
                "donnees",
                chemin_trace
            ]
            retour = main(argv)

        self.assertNotEqual(retour, 0)
        self.assertNotEqual(erreur.getvalue(),"")
        self.assertFalse(os.path.exists(chemin_trace))
        

    def test_fichier_malformate(self):
        erreur = io.StringIO()
        chemin_trace = "tests/sortie/trace_test.json"
        if os.path.exists(chemin_trace):
            os.remove(chemin_trace)
        with redirect_stderr(erreur):
            argv = [
                "main.py",
                "tests/donnees/appartement_errone.json",
                "tests/donnees/scenario_errone.json",
                "donnees",
                chemin_trace
            ]
            retour = main(argv)
            
        self.assertNotEqual(retour, 0)
        self.assertNotEqual(erreur.getvalue(),"")
        self.assertFalse(os.path.exists(chemin_trace))


if __name__ == "__main__":
    unittest.main()