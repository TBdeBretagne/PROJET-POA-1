class agent():
    def __init__(self, position, armoire, dictionnaire, dimension, resident):
        self.main = [] #Initialement, l'agent ne peux prendre qu'un seul objet
        self.carte = [] #Cartographie de l'espace que l'agent a découvert
        self.position = tuple(position) #Vec2 position de l'agent
        self.position_armoire = armoire #Vec2 position de l'armoire
        self.position_dictionnaire = dictionnaire # Vec2 position du dictionnaire
        self.resident = {} #enregistre la position des résidents
        self.armoire = [] #Cartographie de l'armoire que l'agent a découvert
        self.demande = "" #Demande d'un résident que l'agent est en train de traiter
        self.consulte = False
        self.numero = 0 # numero de la demande
        self.position_resident = [] #Resident pris en charge
        self.action = "Attendre" #Indique l'etat du robot

        #cartographie dans la mémoire de l'agent les différentes positions des différents éléments
        ligne = []
        for i in range(dimension['largeur']):
            ligne += ["#"]
        self.carte += [ligne]
        for i in range(1,dimension['hauteur']-1):
            ligne = ["#"]
            for j in range(1,dimension['largeur']-1):
                ligne += ["?"]
            ligne+= ["#"]
            self.carte += [ligne]
        ligne = []
        for i in range(dimension['largeur']):
            ligne += ["#"]
        self.carte += [ligne]
        self.carte[self.position[0]][self.position[1]] = "R"
        self.carte[self.position_armoire[0]][self.position_armoire[1]] = "A"
        self.carte[self.position_dictionnaire[0]][self.position_dictionnaire[1]] = "D"

        #Enregistre la position des résidents, ainsi que leur id
        for R in resident :
            self.resident[R['id']] = [R['nom'], R['position']]
            self.carte[self.resident[R['id']][1][0]][self.resident[R['id']][1][1]] = "P"


    #Cartographie dans la mémoire de l'agent les cases alentoures à celui-ci
    def Cartographie(self, carte):
        N = (self.position[0]-1, self.position[1])
        S = (self.position[0]+1, self.position[1])
        E = (self.position[0], self.position[1]-1)
        O = (self.position[0], self.position[1]+1)
        alentour = [N, S , E, O]

        for direction in alentour:
            if carte['grille'][direction[0]][direction[1]] == "R":
                self.carte[direction[0]][direction[1]] = "."
            else:
                self.carte[direction[0]][direction[1]] = carte['grille'][direction[0]][direction[1]]

    # Vérifie si l'agent est en train de se charger d'une demande
    def en_charge(self): 
        return self.demande != ""

    #Prise en charge de la première demande qu'il n'a pas encore faite
    def prise_en_charge(self, scenario, carte):
        self.demande = scenario[self.numero]['message']
        for num in carte['residents']:
            if num['id'] == scenario[self.numero]['resident']:
                self.position_resident = num['position']
        


    def deplacement(self, case):
        self.carte[self.position[0]][self.position[1]] = "."
        self.carte[case[0]][case[1]] = "R"
        self.position = case
        self.action = "Avancer"


    def Consulter(self):
        self.consulte = True
        self.action = "Consulte"

    def Chercher(self):
        self.main = ["quelque chose"]
        self.action = "Chercher"

    def Donner(self):
        self.main = []
        self.demande = ""
        self.consulte = False
        self.position_resident = []
        self.action = "Donner"
        self.numero += 1

    def Suivant(self):
        self.main = []
        self.demande = ""
        self.consulte = False
        self.position_resident = []
        self.action = "Impossible d'acceder à un resident, prise de la demande suivante"
        self.numero += 1
