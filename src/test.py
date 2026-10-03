def Test_coherence(carte, scenario):
    if scenario['carte'] != carte['nom']:
        print("Le scenario choisi ne correspond pas à la carte. Fin du programme")
        return 1
        
    if carte['grille'][carte['depart_robot'][0]][carte['depart_robot'][1]] != "R" or carte['depart_robot'][0] > carte['dimensions']['hauteur'] or carte['depart_robot'][1] > carte['dimensions']['largeur']:
        print("L'emplacement de l'agent ne correspond à son emplacement dans la grille ou se trouve à l'exterieur. Fin du programme")
        return 1

    if carte['grille'][carte['armoire']['position'][0]][carte['armoire']['position'][1]] != "A" or carte['armoire']['position'][0] > carte['dimensions']['hauteur'] or carte['depart_robot'][1] > carte['dimensions']['largeur']:
        print("L'emplacement de l'armoire ne correspond à son emplacement dans la grille ou se trouve a l'exterieur. Fin du programme")
        return 1
        
    if carte['grille'][carte['dictionnaire']['position'][0]][carte['dictionnaire']['position'][1]] != "A" or carte['dictionnaire']['position'][0] > carte['dimensions']['hauteur'] or carte['depart_robot'][1] > carte['dimensions']['largeur']:
        print("L'emplacement du dictionnaire ne correspond à son emplacement dans la grille ou se trouve a l'exterieur. Fin du programme")
        return 1

    liste_id = []
    for resident in carte['residents']:
        if carte['grille'][resident['position'][0]][resident['position'][1]] != "P" or resident['position'][0]>carte['dimensions']['hauteur'] or resident['position'][1] > carte['dimensions']['largeur']:
            print("L'emplacement d'un resident ne correspond à son emplacement dans la grille ou se trouve a l'exterieur. Fin du programme")
            return 1

        if resident['id'] in liste_id:
            print("Deux resident ont le même identifiant. Fin du programme")
            return 1
        else:
            liste_id.append(resident['id'])

    for identifiant in scenario['demandes']:
        if identifiant['resident'] not in liste_id:
            print("Un resident inexistant dans la carte figure dans le scenario. Fin du programme")
            return 1
