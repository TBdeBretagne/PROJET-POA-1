import sys

def affiche_carte(carte1, dimension, carte2):
    for i in range(dimension['hauteur']):
        for j in range(dimension['largeur']):
            print(carte1[i][j], end = "")
        print(" "*30, end = "")
        for j in range(dimension['largeur']):
            print(carte2[i][j], end = "")
        print("")

def affiche_armoire(armoire,carte_armoire,selecteur):
    casiers = armoire.get("casiers")
    mapCasier = [[None for j in range(8)] for i in range(3)]
    for i in range(len(casiers)):
        mapCasier[casiers[i].get("ligne")][casiers[i].get("colonne")] = casiers[i].get("objet")

    print("   ", end="")
    for i in range(8):
        print(i, end="   ")

    print(" "*8, end = "") 
    
    print("   ", end="")
    for i in range(8):
        print(i, end="   ")
    print()

    for i in range(len(mapCasier)):
        print(i, end="  ")
        for j in range(len(mapCasier[0])):
            if mapCasier[i][j] is not None:
                print("O", end="   ")
            else:
                print("_", end="   ")

        print(" "*11, end="") # Affichage carte de l'agent

        for j in range(len(carte_armoire[0])):
            if i == selecteur[0] and j == selecteur[1]:
                print('^', end="   ")
            elif len(carte_armoire[i][j]) > 1:
                print('O', end="   ")
            else:
                print(carte_armoire[i][j], end="   ") 
        print("\n"*2)




def affichage(carte_complete, dimension, carte, armoire, carte_armoire, selecteur, tour, requete, numero, action, main, destination):
    print("Carte : ")
    print("Complète : ", " "*25, "Point de vue de l'Agent :")
    affiche_carte(carte_complete, dimension, carte)
    print("")
    print("Armoire : ")
    print("Affichage de l'armoire :", " "*12, "Point de vue de l'Agent :")
    affiche_armoire(armoire,carte_armoire,selecteur)
    print("Tours :",tour)
    print("Numéro de la demande :", numero)
    print("Requete en cours :", requete)
    print("Action du robot lors de ce tour:", action)
    print("Main du robot :",main)
    print("Destination :",destination)
