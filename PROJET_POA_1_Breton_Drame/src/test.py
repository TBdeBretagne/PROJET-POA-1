import sys

def Test_coherence(carte, scenario,armoire,dictionnaire):
    #Carte et Scénario
    if scenario['carte'] != carte['nom']:
        print("Le scenario choisi ne correspond pas à la carte. Fin du programme",file=sys.stderr)
        return 1
        
    if  carte['depart_robot'][0] >= carte['dimensions']['hauteur'] or carte['depart_robot'][1] >= carte['dimensions']['largeur'] or carte['depart_robot'][0] < 0 or carte['depart_robot'][1] < 0 or carte['grille'][carte['depart_robot'][0]][carte['depart_robot'][1]] != "R":
        print("L'emplacement de l'agent ne correspond pas à son emplacement dans la grille ou se trouve à l'exterieur. Fin du programme",file=sys.stderr)
        return 1

    if  carte['armoire']['position'][0] >= carte['dimensions']['hauteur'] or carte['armoire']['position'][1] >= carte['dimensions']['largeur'] or carte['armoire']['position'][0] < 0 or carte['armoire']['position'][1] < 0 or carte['grille'][carte['armoire']['position'][0]][carte['armoire']['position'][1]] != "A":
        print("L'emplacement de l'armoire ne correspond pas à son emplacement dans la grille ou se trouve a l'exterieur. Fin du programme",file=sys.stderr)
        return 1
        
    if  carte['dictionnaire']['position'][0] >= carte['dimensions']['hauteur'] or carte['dictionnaire']['position'][1] >= carte['dimensions']['largeur'] or carte['dictionnaire']['position'][0] < 0 or carte['dictionnaire']['position'][1] < 0 or carte['grille'][carte['dictionnaire']['position'][0]][carte['dictionnaire']['position'][1]] != "D":
        print("L'emplacement du dictionnaire ne correspond pas à son emplacement dans la grille ou se trouve a l'exterieur. Fin du programme",file=sys.stderr)
        return 1

    liste_id = []
    
    for resident in carte['residents']:
        if  resident['position'][0] >= carte['dimensions']['hauteur'] or resident['position'][1] >= carte['dimensions']['largeur'] or resident['position'][0] < 0 or resident['position'][1] < 0 or carte['grille'][resident['position'][0]][resident['position'][1]] != "P":
            print("L'emplacement d'un resident ne correspond pas à son emplacement dans la grille ou se trouve a l'exterieur. Fin du programme",file=sys.stderr)
            return 1

        if resident['id'] in liste_id:
            print("Deux residents ont le même identifiant. Fin du programme",file=sys.stderr)
            return 1
        else:
            liste_id.append(resident['id'])

        
        
    liste_numeros = []
    for identifiant in scenario['demandes']:
        if identifiant['resident'] not in liste_id:
            print("Un resident inexistant dans la carte figure dans le scenario. Fin du programme",file=sys.stderr)
            return 1
        if identifiant['numero'] in liste_numeros:
            print("Deux demandes ont le même numéro. Fin du programme",file=sys.stderr)
            return 1
        else:
            liste_numeros.append(identifiant['numero'])


    #Teste Armoire 
    if len(armoire["casiers"]) != 24:
        print("Le nombre de casier dans l'armoire est incohérent. Fin du programme",file=sys.stderr)
        return 1
    if armoire["casier_depart"][0] >= 3 or armoire["casier_depart"][1] >= 8 or armoire["casier_depart"][0] < 0 or armoire["casier_depart"][1] < 0:
        print("La position du casier_depart n'est pas dans l'armoire. Fin du programme",file=sys.stderr)
        return 1
    
    liste_emotions = ["joie","confiance","peur","surprise","tristesse","degout","colere","anticipation"]
    liste_intensites = ["faible","moyenne","forte"]
    liste_positions = []

    for emotion in armoire["emotions"]:
        if emotion not in liste_emotions:
            print(f"armoire : L'emotion : {emotion} n'est pas attendues. Fin du programme",file=sys.stderr)
            return 1

    for intensite in armoire["intensites"]:
        if intensite not in liste_intensites:
            print(f"armoire : L'intensite : {intensite} n'est pas attendues. Fin du programme",file=sys.stderr)
            return 1

    for casier in armoire["casiers"]:
        # Teste la cohérence des emplacements
        if casier["ligne"] >= 3 or casier["colonne"] >= 8 or casier["ligne"] < 0 or casier["colonne"] < 0:
            print("La position d'un casier n'est pas dans l'armoire. Fin du programme",file=sys.stderr)
            return 1
        
        # Teste les émotions et intensités
        if casier["emotion"] not in liste_emotions:
            print("L'emotion d'un casier ne correspond pas à celles reconnues. Fin du programme",file=sys.stderr)
            return 1
        if casier["intensite"] not in liste_intensites:
            print("L'intensité d'un casier ne correspond pas à celles reconnues. Fin du programme",file=sys.stderr)
            return 1

        # Teste la duplicité des casiers 
        if [casier["ligne"],casier["colonne"]] in liste_positions:
            print("Deux casiers ont la même positions. Fin du programme",file=sys.stderr)
            return 1
        else:
            liste_positions.append([casier["ligne"],casier["colonne"]])

        # Teste si les casiers ont les bonnes émotions
        if casier["emotion"] == "joie" and casier["colonne"] != 0:
            print("Un casier ne correspond à l'émotion attendue. Fin du programme",file=sys.stderr)
            return 1
        if casier["emotion"] == "confiance" and casier["colonne"] != 1:
            print("Un casier ne correspond à l'émotion attendue. Fin du programme",file=sys.stderr)
            return 1
        if casier["emotion"] == "peur" and casier["colonne"] != 2:
            print("Un casier ne correspond à l'émotion attendue. Fin du programme",file=sys.stderr)
            return 1
        if casier["emotion"] == "surprise" and casier["colonne"] != 3:
            print("Un casier ne correspond à l'émotion attendue. Fin du programme",file=sys.stderr)
            return 1
        if casier["emotion"] == "tristesse" and casier["colonne"] != 4:
            print("Un casier ne correspond à l'émotion attendue. Fin du programme",file=sys.stderr)
            return 1
        if casier["emotion"] == "degout" and casier["colonne"] != 5:
            print("Un casier ne correspond à l'émotion attendue. Fin du programme",file=sys.stderr)
            return 1
        if casier["emotion"] == "colere" and casier["colonne"] != 6:
            print("Un casier ne correspond à l'émotion attendue. Fin du programme",file=sys.stderr)
            return 1
        if casier["emotion"] == "anticipation" and casier["colonne"] != 7:
            print("Un casier ne correspond à l'émotion attendue. Fin du programme",file=sys.stderr)
            return 1

        # Teste si les casiers ont les bonnes intensités
        if casier["intensite"] == "faible" and casier["ligne"] != 0:
            print("Un casier ne correspond à l'intensité attendue. Fin du programme",file=sys.stderr)
            return 1
        if casier["intensite"] == "moyenne" and casier["ligne"] != 1:
            print("Un casier ne correspond à l'intensité attendue. Fin du programme",file=sys.stderr)
            return 1
        if casier["intensite"] == "forte" and casier["ligne"] != 2:
            print("Un casier ne correspond à l'intensité attendue. Fin du programme",file=sys.stderr)
            return 1
        

    # Test dictionnaire

    liste_formes = []
    for entree in dictionnaire["entrees"]:
        for forme in entree["formes"]:
            if forme in liste_formes:
                print("L'une des formes apparait plusieurs fois. Fin du programme",file=sys.stderr)
                return 1
            else:
                liste_formes.append(forme)
        if entree["emotion"] not in liste_emotions:
            print("L'émotion d'un mot ne correspond pas à celles reconnues. Fin du programme",file=sys.stderr)
            return 1
        if entree["intensite"] not in liste_intensites:
            print("L'intensité d'un mot ne correspond pas à celles reconnues. Fin du programme",file=sys.stderr)
            return 1

    for emotion in dictionnaire["emotions"]:
        if emotion not in liste_emotions:
            print(f"dictionnaire : L'emotion : {emotion} n'est pas attendues. Fin du programme",file=sys.stderr)
            return 1

    for intensite in dictionnaire["intensites"]:
        if intensite not in liste_intensites:
            print(f"dictionnaire : L'intensite : {intensite} n'est pas attendues. Fin du programme",file=sys.stderr)
            return 1




        
    return 0
