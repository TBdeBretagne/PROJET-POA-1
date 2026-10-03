import sys
import time
from pathlib import Path

from src import reconfort_io as rio
from src import agent
from src import affichage as af
from src import chemin
from src import test


def main(argv):
    print("\033[2J\033[H", end="")
    if len(argv) != 5:
        print(__doc__.strip())
        return 2
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

    test.Test_coherence(carte, scenario)
    
    A = agent.agent(carte["depart_robot"], carte['armoire']['position'], carte['dictionnaire']['position'], carte['dimensions'], carte['residents'])
    #Dans l'idée, on va retrouver ici une boucle, peut etre infini
    tour = 0
    destination = ""
    dest = ""
    case_arrive = []
    C = []
    #while A.numero <= len(scenario):
    while A.numero < len(scenario['demandes']):
        print("\033[2J\033[H", end="")
        
        A.Cartographie(carte)
        af.affichage(carte['grille'], carte['dimensions'], A.carte, tour, A.demande, A.numero, A.action, A.main, dest)

        if not A.en_charge():
            A.prise_en_charge(scenario["demandes"], carte)

        elif not A.consulte:
            case_arrive = chemin.Arriver(A.position_dictionnaire, carte)
            if A.position in case_arrive:
                A.Consulter()
            else:
                destination = A.position_dictionnaire
                dest = "Dictionnaire" 

        elif A.main == []:
            case_arrive = chemin.Arriver(A.position_armoire, carte)
            if A.position in case_arrive:
                A.Chercher()
            else:
                destination = A.position_armoire
                dest = "Armoire"

        else:
            case_arrive = chemin.Arriver(A.position_resident, carte)
            if A.position in case_arrive:
                A.Donner()
            else:
                destination = A.position_resident
                for num in carte['residents']:
                    if num['id'] == scenario['demandes'][A.numero]['resident']:
                        nom = num['nom']
                dest = "Résident " + scenario['demandes'][A.numero]['resident'] + " nom"

        if destination != "" :
            case_arrive = chemin.Arriver(destination, carte)
            C = chemin.plus_court_chemin(A.position, case_arrive, A.carte)  

        if C != "aucun chemin" and C != []:
            A.deplacement(C[0])
        elif C != []:
            if destination == A.position_resident:
                A.Suivant()
            else:
                print("Le robot ne peux pas acceder à sa destination. Fin du programme")
            return 1
    
        tour += 1
        time.sleep(0.5)
    
    
if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
