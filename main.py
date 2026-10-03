import reconfort_io as rio
import random
import time


print("\033[2J\033[H", end="")

def initialisation():
    dictionnary = rio.charger_dictionnaire("donnees/dictionnaire.json")
    armory = rio.charger_armoire("donnees/armoire_standard.json")
    locker = armory.get("casiers")
    cursorPos = armory.get("casier_depart")
    lockerMap = [[None for j in range(8)] for i in range(3)]
    robotView = [['?' for j in range(8)] for i in range(3)]

    for i in range(len(locker)):
        lockerMap[locker[i].get("ligne")][locker[i].get("colonne")] = locker[i].get("objet")

    #robotView[cursorPos[0]][cursorPos[1]] = lockerMap[cursorPos[0]][cursorPos[1]]

    return dictionnary, armory, lockerMap, robotView

emotionsConverter = {
    "joie": 0,
    "confiance": 1,
    "peur": 2,
    "surprise": 3,
    "tristesse": 4,
    "degout": 5,
    "colere": 6,
    "anticipation": 7
}

intensitesConverter = {
    "faible": 0,
    "moyenne": 1,
    "forte": 2
}





def findEmotion(message, entrees):
    if not isinstance(message,str) or message == "" or entrees == []:
        raise ValueError("Emotion non reconnue")
    words = rio.normaliser(message)
    for word in words:
        for j in range(len(entrees)):
            if word in entrees[j].get("formes"):
                return [
                    word,
                    intensitesConverter[entrees[j].get("intensite")],
                    emotionsConverter[entrees[j].get("emotion")]
                ]
    return None




def displayArmory(lockerMap):
    if not isinstance(lockerMap,list):
        raise ValueError("Carte armoire inaccessible")
    print("   ", end="")
    for i in range(8):
        print(i, end="   ")
    print()

    for i in range(len(lockerMap)):
        print(i, end="  ")
        for j in range(len(lockerMap[0])):
            if lockerMap[i][j] is not None:
                print("O", end="   ")
            else:
                print("_", end="   ")
        print()


def displayRobotView(robotView,cursorPos):
    if not isinstance(robotView,list) or not isinstance(cursorPos,list):
        raise ValueError("Vision armoire du robot inaccessible")
    print("\033[H", end="")
    print("   ", end="")
    for i in range(8):
        print(i, end="   ")
    print()

    for i in range(len(robotView)):
        print(i, end="  ")
        for j in range(len(robotView[0])):
            if i == cursorPos[0] and j == cursorPos[1]:
                print('^', end="   ")
            elif len(robotView[i][j]) > 1:
                print('O', end="   ")
            else:
                print(robotView[i][j], end="   ") 
        print()
    time.sleep(1)

def moveCursor(cursorPos,direction):
    if not isinstance(cursorPos,list) or cursorPos == []:
        raise ValueError("Impossible de déplacer le curseur")
    if not isinstance(direction,chr) or direction == '':
            raise ValueError("Impossible d'effectuer ce mouvement")
    pos = cursorPos.copy() 
    match direction:
        case 'N':
            if pos[0] != 0:
                pos[0] -= 1 
            else:None 
        case 'S':
            if pos[0] != 2:
                pos[0] += 1
        case 'E':
            pos[1] = (pos[1] + 1) % 8 
        case 'O':
            pos[1] = (pos[1] - 1) % 8 # in python -x mod n = n-x if 0 < x < n
        case _:
            None
    return pos


def createPath(start,goal):
    if not isinstance(start,list) or start == [] or isinstance(goal,list) or goal == []:
        raise ValueError("Impossible de trouver une combinaison dans le casier")
    directions = []
    startI = start[0]
    startJ = start[1] 

    goalI = goal[0] 
    goalJ = goal[1]
    
    a =  (goalJ - startJ) % 8 

    if a <= 8 - a:
        for i in range(a):
            directions.append("E")
    else:
        for i in range(8-a):
            directions.append("O")

    b = abs(goalI - startI)
    if goalI > startI:
        for i in range(b):
            directions.append("S")
    else:
        for i in range(b):
            directions.append("N")

    random.shuffle(directions)
    return directions
    

def movTest(start, goal):
    cursorPos = start
    print("from ", start)
    directions = createPath(start,goal)
    for direction in directions:
        cursorPos = moveCursor(cursorPos, direction)
        print(direction, " " , cursorPos)


def findCandidate(position):
    if not isinstance(position,list) or position == []:
        raise ValueError("Impossible de trouver une stratégie de repli")
    candidateLocker = []
    tab = [0,1,2]
    intensities = [position[0]]                 # Allowed tab : [0,1,2] or [1,0,2] or [2,1,0]
    for i in range(3):
        if tab[i] != intensities[0]:
            intensities.append(tab[i])

    if intensities[0] == 2:             # if intensity == 2 order = [2,1,0]. So we need to switch [2,0,1]
        tmp = intensities[1]
        intensities[1] = intensities[2]
        intensities[2] = tmp

    candidateLocker.append([intensities[1],position[1]])
    candidateLocker.append([intensities[2],position[1]])

    for distance in range(1,3):
        for intensity in intensities:
            candidateLocker.append([intensity,(position[1]+distance)%8])
            candidateLocker.append([intensity,(position[1]-distance)%8])

    return candidateLocker
            
def updateRobotView(armory,cursorPos,robotView):
    if not isinstance(cursorPos,list) or cursorPos == []:
        raise ValueError("Impossible de trouver une combinaison dans le casier")
    if not isinstance(robotView,list) or robotView == []:
            raise ValueError("Vision armoire du robot inaccessible")
    locker = armory.get("casiers")
    if locker[cursorPos[0] * 8 + cursorPos[1]].get("objet") is not None:
        
        robotView[cursorPos[0]][cursorPos[1]] = 'O'
    else:
        robotView[cursorPos[0]][cursorPos[1]] = '_'

def getObjectInLocker(sentence):
    if not isinstance(sentence,str) or sentence == "":
        raise ValueError("Emotion non reconnue")
    dictionnary, armory, lockerMap, robotView = initialisation()
    inputTab = dictionnary.get("entrees")
    lockers = armory.get("casiers")
    objectFound = False
    emotion = findEmotion(sentence,inputTab)
    outputSentence =""
    if emotion is None:
        print("Emotion indeterminee")
    else:
        
        lockerPosition = [emotion[1],emotion[2]]
        cursorPos = armory.get("casier_depart").copy()
        displayRobotView(robotView,cursorPos)
        updateRobotView(armory,cursorPos,robotView)
        path = createPath(cursorPos,lockerPosition)

        for direction in path:
            cursorPos = moveCursor(cursorPos,direction)
            updateRobotView(armory,cursorPos,robotView)
            displayRobotView(robotView,cursorPos)

        if robotView[cursorPos[0]][cursorPos[1]] == 'O':
            objectFound = True
            index = cursorPos[0]*8+cursorPos[1]
            objet = lockers[index].get("objet")
            outputSentence = f"Le robot vous donne : {objet}"

            
        else:
            candidates = findCandidate(cursorPos)
            for candidateLocker in candidates:
                path = createPath(cursorPos,candidateLocker)
                for direction in path:
                    cursorPos = moveCursor(cursorPos,direction)
                    updateRobotView(armory,cursorPos,robotView)
                    displayRobotView(robotView,cursorPos)

                if robotView[cursorPos[0]][cursorPos[1]] == 'O':
                    objectFound = True
                    index = cursorPos[0]*8+cursorPos[1]
                    objet = lockers[index].get("objet")
                    outputSentence = f"Le robot vous donne : {objet}"
                    break
                

            if not objectFound:
                outputSentence= "Le robot n'a rien trouvé pour vous."
        return outputSentence

  

def main():
    dictionnary, armory, lockerMap, robotView = initialisation()
    inputTab = dictionnary.get("entrees")

    

    #########################################################################################################################
    ########################################          Tests            ######################################################
    #########################################################################################################################

    #print(findEmotion("Il pleut, ca m'apaise mais ca me rend triste aussi", inputTab))
    #displayArmory(lockerMap)
    #displayRobotView(robotView)
    #print(moveCursor([2,7],'E'))
    #print(createPath([0,0],[2,7]))
    # cursorPos = armory.get("casier_depart")
    # movTest(cursorPos,[2,5])
    #print(findCandidate([2,3]))
    #updateRobotView(armory,[2,3],robotView)
    #displayRobotView(robotView)

    print(getObjectInLocker(sentence = "J'ai le cafard aujourd'hui, sans savoir pourquoi." ))


        

    #########################################################################################################################
    ########################################          Simulation            #################################################
    #########################################################################################################################
    
    
    

    






if __name__ == "__main__":
    main()
