import random
import time
from src.trace import Trace

class Armoire():
    def __init__(self,armoire):
        self.carteArmoire = [['?' for j in range(8)] for i in range(3)]
        self.selecteur = armoire.get("casier_depart")
        casiers = armoire.get("casiers")
        self.contenuCasierCourant = casiers[self.selecteur[0] * 8 + self.selecteur[1]].get("objet")

    def moveCursor(self,direction):
        selecteur = self.selecteur.copy()
        match direction:
            case 'N':
                if selecteur[0] != 0:
                    selecteur[0] -= 1 
                else:None 
            case 'S':
                if selecteur[0] != 2:
                    selecteur[0] += 1
            case 'E':
                selecteur[1] = (selecteur[1] + 1) % 8 
            case 'O':
                selecteur[1] = (selecteur[1] - 1) % 8 # in python -x mod n = n-x if 0 < x < n
            case _:
                None
        return selecteur

    def createPath(self,casierBut):
        directions = []
        startI = self.selecteur[0]
        startJ = self.selecteur[1] 

        casierButI = casierBut[0] 
        casierButJ = casierBut[1]
        
        a =  (casierButJ - startJ) % 8 

        if a <= 8 - a:
            for i in range(a):
                directions.append("E")
        else:
            for i in range(8-a):
                directions.append("O")

        b = abs(casierButI - startI)
        if casierButI > startI:
            for i in range(b):
                directions.append("S")
        else:
            for i in range(b):
                directions.append("N")

        random.shuffle(directions)
        return directions


    def findCandidate(self):
        position = self.selecteur
        casierCandidat = []
        tab = [0,1,2]
        intensites = [position[0]]                 # Tab autorisé : [0,1,2] or [1,0,2] or [2,1,0]
        for i in range(3):
            if tab[i] != intensites[0]:
                intensites.append(tab[i])

        if intensites[0] == 2:             # si intensite == 2 ordre = [2,1,0]. Donc on échange pour avoir [2,0,1]
            tmp = intensites[1]
            intensites[1] = intensites[2]
            intensites[2] = tmp

        casierCandidat.append([intensites[1],position[1]])
        casierCandidat.append([intensites[2],position[1]])

        for distance in range(1,3):
            for intensite in intensites:
                casierCandidat.append([intensite,(position[1]+distance)%8])
                casierCandidat.append([intensite,(position[1]-distance)%8])

        return casierCandidat


    def updateArmoire(self,casiers):
        if casiers[self.selecteur[0] * 8 + self.selecteur[1]].get("objet") is not None:
            self.carteArmoire[self.selecteur[0]][self.selecteur[1]] = 'O'
            self.contenuCasierCourant = casiers[self.selecteur[0] * 8 + self.selecteur[1]].get("objet")
        else:
            self.carteArmoire[self.selecteur[0]][self.selecteur[1]] = '_'
            self.contenuCasierCourant = "Vide"


    


    def fouillerCasier(self,casierBut,casiers,afficher,ajouterTrace):
        self.updateArmoire(casiers)
        path = self.createPath(casierBut)
        for direction in path:
            ajouterTrace(self.selecteur,direction,self.contenuCasierCourant,"Chercher")
            self.selecteur = self.moveCursor(direction)
            self.updateArmoire(casiers)
            afficher()
            time.sleep(0.5)
            

        if self.carteArmoire[self.selecteur[0]][self.selecteur[1]] == 'O':
            index = self.selecteur[0]*8+self.selecteur[1]
            objet = casiers[index].get("objet")
            ajouterTrace(self.selecteur,objet,self.contenuCasierCourant,"Prendre")
            self.carteArmoire[self.selecteur[0]][self.selecteur[1]] = '_'
            casiers[index]["objet"] = None
            return objet,self.selecteur,"aucun"

            
        else:
            candidates = self.findCandidate()
            cpt = 0
            repli = ""
            for casierCandidat in candidates:
                path = self.createPath(casierCandidat)
                for direction in path:
                    ajouterTrace(self.selecteur,direction,self.contenuCasierCourant,"Chercher")
                    self.selecteur = self.moveCursor(direction)
                    self.updateArmoire(casiers)
                    afficher()
                    time.sleep(1)
                    

                if self.carteArmoire[self.selecteur[0]][self.selecteur[1]] == 'O':
                    index = self.selecteur[0]*8+self.selecteur[1]
                    objet = casiers[index].get("objet")
                    ajouterTrace(self.selecteur,objet,self.contenuCasierCourant,"Prendre")
                    self.carteArmoire[self.selecteur[0]][self.selecteur[1]] = '_'
                    casiers[index]["objet"] = None
                    if cpt < 2: repli ="intensite"
                    elif cpt < 9: repli ="voisine_1"
                    else : repli = "voisine_2"
                    return objet,self.selecteur,repli
                cpt += 1
        return None, None, "vide"
                    