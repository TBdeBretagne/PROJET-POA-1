import reconfort_io as rio
import random

def initialisation():
    dictionnary = rio.charger_dictionnaire("donnees/dictionnaire.json")
    armory = rio.charger_armoire("donnees/armoire_standard.json")
    locker = armory.get("casiers")
    cursorPos = armory.get("casier_depart")
    lockerMap = [[None for j in range(8)] for i in range(3)]
    robotView = [['?' for j in range(8)] for i in range(3)]

    for i in range(len(locker)):
        lockerMap[locker[i].get("ligne")][locker[i].get("colonne")] = locker[i].get("objet")

    robotView[cursorPos[0]][cursorPos[1]] = lockerMap[cursorPos[0]][cursorPos[1]]

    return dictionnary, armory, lockerMap, robotView


def findEmotion(message, inputTab):
    words = rio.normaliser(message)
    for word in words:
        for j in range(len(inputTab)):
            if word in inputTab[j].get("formes"):
                return [word, inputTab[j].get("intensite"), inputTab[j].get("emotion")]
    return None


def displayArmory(lockerMap):
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


def displayRobotView(robotView):
    print("   ", end="")
    for i in range(8):
        print(i, end="   ")
    print()

    for i in range(len(robotView)):
        print(i, end="  ")
        for j in range(len(robotView[0])):
            if robotView[i][j] != '?':
                print("O", end="   ")
            else:
                print("?", end="   ")
        print()

def moveCursor(cursorPos,direction):
    match direction:
        case 'N':
            if cursorPos[0] != 0:
                cursorPos[0] -= 1 
            else:None 
        case 'S':
            if cursorPos[0] != 2:
                cursorPos[0] += 1
        case 'E':
            cursorPos[1] = (cursorPos[1] + 1) % 8 
        case 'O':
            cursorPos[1] = (cursorPos[1] - 1) % 8 # in python -x mod n = n-x if 0 < x < n
        case _:
            None
    return cursorPos


def createPath(start,goal):
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
            
   

def main():
    dictionnary, armory, lockerMap, robotView = initialisation()
    inputTab = dictionnary.get("entrees")

    
    #print(findEmotion("Il pleut, ca m'apaise mais ca me rend triste aussi", inputTab))
    #displayArmory(lockerMap)
    #displayRobotView(robotView)
    #print(moveCursor([2,7],'E'))
    #print(createPath([0,0],[2,7]))
    # cursorPos = armory.get("casier_depart")
    # movTest(cursorPos,[2,5])
    #print(findCandidate([2,3]))

if __name__ == "__main__":
    main()
