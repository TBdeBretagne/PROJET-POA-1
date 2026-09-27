import sys

def affiche_carte(carte1, dimension, carte2):
    for i in range(dimension['hauteur']):
        for j in range(dimension['largeur']):
            print(carte1[i][j], end = "")
        print(" "*30, end = "")
        for j in range(dimension['largeur']):
            print(carte2[i][j], end = "")
        print("")

def affiche_armoire():
    print("")


def affichage(carte_complete, dimension, carte, tour, requete, numero):
    print("Carte : ")
    print("Complète : ", " "*25, "Point de vue de l'Agent :")
    affiche_carte(carte_complete, dimension, carte)
    print("")
    print("Armoire : ")
    print("Affichage de l'armoire :", " "*12, "Point de vue de l'Agent :")
    affiche_armoire()
    print("Tours :",tour)
    print("Numéro de la demande :", numero)
    print("Requete en cours :", requete)
