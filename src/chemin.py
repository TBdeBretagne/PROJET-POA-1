from src import File
def est_traversable(case):
    if case != "#" and case != "A" and case != "D" and case != "P":
        return True
    return False

def reconstruire(predecesseur, case):
    chemin = [case]
    while predecesseur[predecesseur[chemin[-1]]] != 0:
        chemin += [predecesseur[chemin[-1]]]
    return chemin[::-1]

def plus_court_chemin(depart, arrivees, carte):
    if depart in arrivees:
        return [depart]

    predecesseur = {}
    predecesseur[depart] = 0
    file = []
    File.enfiler(file, depart)
    while file != []:
        courant = File.defiler(file)
        voisins = [(courant[0],courant[1]+1), (courant[0], courant[1]-1), (courant[0]+1, courant[1]), (courant[0]-1, courant[1])]
        for voisin in voisins:
            if not(voisin in list(predecesseur.keys())):
                if est_traversable(carte[voisin[0]][voisin[1]]):
                    predecesseur[voisin] = courant
                    if voisin in arrivees:
                        return reconstruire(predecesseur, voisin)
                    File.enfiler(file, voisin)
    return "aucun chemin"


def Arriver(case, carte):
    result = []
    voisins = [(case[0],case[1]+1), (case[0], case[1]-1), (case[0]+1, case[1]), (case[0]-1, case[1])]
    for voisin in voisins:
        if est_traversable(carte['grille'][voisin[0]][voisin[1]]):
            result.append(voisin)
    return result
