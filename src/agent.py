class agent():
    def __init__(self, position, dictionnaire, armoire, dimension, resident):
        self.main = [] #Initialement, l'agent ne peux prendre qu'un seul objet
        self.carte = [] #Cartographie de l'espace que l'agent a découvert
        self.position = position #Vec2 position de l'agent
        self.position_armoire = armoire #Vec2 position de l'armoire
        self.position_dictionnaire = dictionnaire # Vec2 position du dictionnaire
        self.resident = {} #enregistre la position des résidents
        self.armoire = [] #Cartographie de l'armoir que l'agent a découvert
        self.demande = "" #Demande d'un résident que l'agent est en train de traiter
        self.numero = 0 # numero de la demande
        self.id_resident = [] #Resident pris en charge

        #cartographie dans la mémoire de l'agent les différentes positions des différents éléments
        for i in range(dimension['hauteur']):
            ligne = []
            for j in range(dimension['largeur']):
                ligne += ["?"]
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
        return self.demande == ""

    #Prise en charge de la première demande qu'il n'a pas encore faite
    def prise_en_charge(self, scenario):
        self.demande = scenario[self.numero]['message']
        self.id_resident = scenario[self.numero]['resident']
        self.numero += 1


    def deplacement(self, direction):
        if direction == 'N':
            if self.carte[self.position[0]-1][self.position[1]] == ".":
                self.carte[self.position[0]-1][self.position[1]] = "R"
                self.carte[self.position[0]][self.position[1]] = "."
                self.position[0] = self.position[0] - 1
        elif direction == 'S':
            if self.carte[self.position[0]+1][self.position[1]] == ".":
                self.carte[self.position[0]+1][self.position[1]] = "R"
                self.carte[self.position[0]][self.position[1]] = "."
                self.position[0] = self.position[0] + 1
        elif direction == 'E':
            if self.carte[self.position[0]][self.position[1]-1] == ".":
                self.carte[self.position[0]][self.position[1]-1] = "R"
                self.carte[self.position[0]][self.position[1]] = "."
                self.position[1] = self.position[1] - 1
        elif direction == 'O':
            if self.carte[self.position[0]][self.position[1]+1] == ".":
                self.carte[self.position[0]][self.position[1]+1] = "R"
                self.carte[self.position[0]][self.position[1]] = "."
                self.position[1] = self.position[1] + 1
        else:
            print(f"erreur dans l'indication d'une direction : ", direction)
            return 1


    def 
        
    

        
        
