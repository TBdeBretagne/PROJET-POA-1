import sys
import time
from pathlib import Path

from src import reconfort_io as rio
from src import agent
from src import affichage as af
from src import chemin
from src import test
from src.trace import Trace




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

    if(test.Test_coherence(carte, scenario,armoire,dictionnaire) == 1):
        return 1

    # Redimensionne à 40 lignes et 100 colonnes
    sys.stdout.write("\x1b[8;40;100t")
    sys.stdout.flush()

    trace = Trace(carte["nom"],scenario["nom"])
    A = agent.agent(carte["depart_robot"], carte['armoire']['position'],armoire, carte['dictionnaire']['position'], carte['dimensions'], carte['residents'])

    destination = ""
    dest = ""
    case_arrive = []
    C = []


    emotion =""
    intensite =""
    casier_choisi = []
    repli = ""
    objet = ""

    Succed = []
    for i in range(len(scenario['demandes'])):
        Succed += ["_"]
        

    def afficher():                         #On declare la fonction ici afin de pouvoir la passer en argument pour l'appeler depuis l'armoire
        print("\033[2J\033[H", end="")
        af.affichage(
            carte['grille'],
            carte['dimensions'],
            A.carte,
            armoire,
            A.armoire.carteArmoire,
            A.armoire.selecteur,
            trace.t,
            A.demande,
            A.numero,
            A.action,
            A.main,
            dest,
            Succed
        )

    def ajouterTrace(selecteur, argument, contenu_casier,action):
        trace.ajouterPas(
            A.numero,
            A.position,
            selecteur,
            action,
            argument,
            A.perception(),
            contenu_casier,
            "Aucun"
        )

    num = 0
    while A.numero < len(scenario['demandes']):
        print("\033[2J\033[H", end="")
        
        A.Cartographie(carte)
        afficher()
        if not A.en_charge():
            A.prise_en_charge(scenario["demandes"], carte)

        elif not A.consulte:
            case_arrive = chemin.Arriver(A.position_dictionnaire, A.carte)
            if A.position in case_arrive:
                emotion, intensite = A.Consulter(dictionnaire.get("entrees"))
                trace.ajouterPas(A.numero,A.position,A.armoire.selecteur,A.action,None,A.perception(),None,"Le robot consulte le dictionnaire")
                if A.casier == None:
                    trace.ajouterLivraison(A.numero,scenario["demandes"][A.numero]["resident"],emotion,intensite,casier_choisi,repli,objet,False,"Emotion indéterminée")
                    Succed[A.numero] = "F"
                    A.Suivant()
                    continue
            
            else:
                destination = A.position_dictionnaire
                dest = "Dictionnaire" 

        elif A.main == []:
            case_arrive = chemin.Arriver(A.position_armoire, A.carte)
            if A.position in case_arrive:
                objet,casier_choisi, repli = A.Chercher(armoire.get("casiers"),afficher,ajouterTrace)
                if objet == None:
                    trace.ajouterLivraison(A.numero,scenario["demandes"][A.numero]["resident"],emotion,intensite,casier_choisi,repli,objet,False,"Armoire vide")
                    Succed[A.numero] = "F"
                    A.Suivant()
                    continue
                

            else:
                destination = A.position_armoire
                dest = "Armoire"

        else:
            case_arrive = chemin.Arriver(A.position_resident, A.carte)
            if A.position in case_arrive:
                num = A.numero
                Succed[num] = "V"
                A.Donner()
                trace.ajouterLivraison(num,scenario["demandes"][num]["resident"],emotion,intensite,casier_choisi,repli,objet,True,"None")
                trace.ajouterPas(num,A.position,A.armoire.selecteur,A.action,objet,A.perception(),None,"Objet donné au résident")
                

            else:
                destination = A.position_resident
                for num in carte['residents']:
                    if num['id'] == scenario['demandes'][A.numero]['resident']:
                        nom = num['nom']
                dest = "Résident " + scenario['demandes'][A.numero]['resident'] + " nom"

        if destination != "" :
            case_arrive = chemin.Arriver(destination, A.carte)
            C = chemin.plus_court_chemin(A.position, case_arrive, A.carte)  

        if C != "aucun chemin" and C != []:
            pos = A.position
            direction = A.donnerDirection(C[0])
            A.deplacement(C[0])
            A.Cartographie(carte)
            trace.ajouterPas(A.numero,pos,A.armoire.selecteur,A.action,direction,A.perception(),None,"Le robot avance d'un pas décidé")
        
        elif C != []:
            if destination == A.position_resident:
                num = A.numero
                Succed[num] = "F"
                A.Suivant()
                trace.ajouterPas(num,A.position,A.armoire.selecteur,A.action,None,A.perception(),None,"Aucun chemin vers le résident")
                trace.ajouterLivraison(num,scenario["demandes"][num]["resident"],emotion,intensite,casier_choisi,repli,objet,False,"Résident inaccessible")
                destination = ""
                dest = ""
                case_arrive = []
                C = []
            else:
                print("Le robot ne peux pas acceder à sa destination. Fin du programme")
                trace.ajouterLivraison(num,scenario["demandes"][num]["resident"],emotion,intensite,casier_choisi,repli,objet,False,"Le robot est bloqué")
                return 1
        else:
            pass
    
        time.sleep(0.5)
    afficher()
    trace.resume()
    trace.sauvegarder(chemin_sortie)
    return 0
    
    
if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
