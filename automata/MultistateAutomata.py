import random
import utils
class MultistateAutomata():
    def __init__(self, cells, ruleTable, stateDepths, crossStateRules = None):
        self.stateDepths = stateDepths
        self.cells = cells
        self.width = len(self.cells)
        self.ruleTable = ruleTable
        self.ruleTableWidth = len(self.ruleTable)
        self.kernelWidth = 3

        if crossStateRules is None:
            self.crossStateRules = {}
            for i in range(1):
                self.addCrossStateRule(utils.randomState(self.stateDepths), utils.randomState(self.stateDepths))
        else:
            self.crossStateRules = crossStateRules

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
