import sys
import os
import time
from pathlib import Path

from src import reconfort_io as rio

from src import agent
from src import affichage as af


def main(argv):
    if len(argv) != 5:
        print(__doc__.strip())
        return 2
    os.system("stty cols 150 rows 40")
    chemin_carte, chemin_scenario = Path(argv[1]), Path(argv[2])
    dossier_donnees, chemin_sortie = Path(argv[3]), Path(argv[4])

    try:
        carte = rio.charger_carte(chemin_carte)
        scenario = rio.charger_scenario(chemin_scenario)
        dictionnaire = rio.charger_dictionnaire(
            dossier_donnees / "dictionnaire.json")
        armoire = rio.charger_armoire(
            dossier_donnees / f"{scenario['armoire']}.json")
    except rio.ErreurFichier as err:
        print(f"erreur de chargement : {err}", file=sys.stderr)
        return 1

    A = agent.agent(carte["depart_robot"], carte['armoire']['position'], carte['dictionnaire']['position'], carte['dimensions'], carte['residents'])
    #Dans l'idée, on va retrouver ici une boucle, peut etre infini
    tour = 0
    #while A.numero <= len(scenario):
    while tour < 10:
        os.system("clear")
        if A.en_charge():
            A.prise_en_charge(scenario["demandes"])
            
        A.Cartographie(carte)
        af.affichage(carte['grille'], carte['dimensions'], A.carte, tour, A.demande, A.numero)

        tour += 1
        time.sleep(0.5)
    
    
if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
