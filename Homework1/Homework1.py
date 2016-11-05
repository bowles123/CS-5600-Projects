class CvMGameConfiguration:

    def __init__(self, cannibals, missionaries, boatLeft):
        self.cannibalsLeft = cannibals
        self.missionariesLeft = missionaries
        self.boatLeft = boatLeft

    def printConfiguration(self):
        if self.boatLeft:
            boat = "left"
        else:
            boat = "right"
        
        print("%d Cannibals and %d Missionaries with the boat on the %s." %
              (self.cannibalsLeft, self.missionariesLeft, boat))
        
def getNextStates(state, maxM, boatSize):
    states = []

    for x in range(0, boatSize + 1):
        for y in range(0, boatSize + 1):
            if (x == 0 and y == 0) or x + y > boatSize:
                continue
            else:
                if state.boatLeft:
                    if not (state.cannibalsLeft - x < 0 or state.missionariesLeft - y < 0):
                        states.append(CvMGameConfiguration(state.cannibalsLeft - x,
                                                           state.missionariesLeft - y,
                                                           False))
                else:
                    if not (state.cannibalsLeft + x > maxM or state.missionariesLeft + y > maxM):
                        states.append(CvMGameConfiguration(state.cannibalsLeft + x,
                                                           state.missionariesLeft + y,
                                                           True))
    return states

def printStates(states):
    for i in range(0, len(states)):
        states[i].printConfiguration()

def isIllegal(state, maxMissionaries):
    if getattr(state, 'cannibalsLeft') > getattr(state, 'missionariesLeft'):
        if getattr(state, 'missionariesLeft') != 0:
            return True
    
    if getattr(state, 'cannibalsLeft') < getattr(state, 'missionariesLeft'):
        if getattr(state, 'missionariesLeft') != maxMissionaries:
            return True
    return False

def isGoal(state):
    if getattr(state, 'cannibalsLeft') == 0:
       if getattr(state, 'missionariesLeft') == 0:
           if getattr(state, 'boatLeft') == False:
                return True
    return False

def playGame(numCannibals, numMissionaries, boatSize):
    moves = 0
    i = 0
    start = CvMGameConfiguration(numCannibals, numMissionaries, True)
    nodes = getNextStates(start, numMissionaries, boatSize)
    visited = {(getattr(start, 'cannibalsLeft'), start.boatLeft): [getattr(start, 'missionariesLeft')]}
    nodeVisited = []
    state = CvMGameConfiguration(0, 2, False)

    for node in nodes:        
        if not ((getattr(node, 'cannibalsLeft'), node.boatLeft) in visited):
            visited[(getattr(node, 'cannibalsLeft'), node.boatLeft)] = []
            
        nodeVisited = visited.get((getattr(node, 'cannibalsLeft'), node.boatLeft))

        if getattr(node, 'missionariesLeft') in nodeVisited:
            i = i + 1
            continue
        
        if isIllegal(node, numMissionaries):
            i = i + 1
            nodeVisited.append(getattr(node, 'missionariesLeft'))
            continue

        if isGoal(node):
            nodeVisited.append(getattr(node, 'missionariesLeft'))
            return moves - 1

        i = i + 1
        moves = moves + 1
        nodeVisited.append(getattr(node, 'missionariesLeft'))
        nodes[i:i] = getNextStates(node, numMissionaries, boatSize)
        
    return False
