import random
import utils
class MultistateAutomata():
    def __init__(self, cells, ruleTable, stateDepths, numCrossStateRules = 0):
        self.stateDepths = stateDepths
        self.cells = cells
        self.neighborhoods = cells
        self.width = len(self.cells)
        self.ruleTable = ruleTable
        self.ruleTableWidth = len(self.ruleTable)
        self.kernelWidth = 3

        self.crossStateRules = {}

        if numCrossStateRules is not 0:
            for i in range(numCrossStateRules):
                randomStartState = utils.randomState(self.stateDepths)
                randomEndState = utils.randomState(self.stateDepths)
                self.addCrossStateRule(randomStartState, randomEndState)

    def addCrossStateRule(self, fromState, toState):
        self.crossStateRules[tuple(fromState)] = toState

    def getCells(self):
        return self.cells

    def applyCrossStateRules(self):
        mutatedIndexes = []
        for cellIndex, cell in enumerate(self.cells):
            if self.crossStateRules.has_key(tuple(cell)):
                self.cells[cellIndex] = self.crossStateRules[tuple(cell)]
                mutatedIndexes.append(cellIndex)
        return mutatedIndexes

    def getNeighborhoods(self):
        return self.neighborhoods

    def step(self):
        newCells = [0 for i in range(self.width)]
        for cellIndex, currentValue in enumerate(self.cells):
            neighbors = utils.circularSlice(self.cells,
                        (cellIndex - self.kernelWidth/2),
                        (cellIndex + self.kernelWidth/2 + 1))
            newState = [0 for i in range(self.ruleTableWidth)]
            for subruleIndex, subrule in enumerate(self.ruleTable):
                neighborStateIndexes = [neighbor[subruleIndex] for neighbor in neighbors]
                nextSubstate = utils.indexByTuple(subrule, neighborStateIndexes)
                newState[subruleIndex] = nextSubstate
            newCells[cellIndex] = newState
        self.cells = newCells
        self.neighborhoods = [utils.circularSlice(self.cells,
                        (cellIndex - self.kernelWidth/2),
                        (cellIndex + self.kernelWidth/2 + 1)) for cellIndex in range(self.width)]
