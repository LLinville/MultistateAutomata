import random
import utils
class MultistateAutomata():
    def __init__(self, cellsAndRuleTable):
        self.cells = cellsAndRuleTable[0]
        self.width = len(self.cells)
        self.ruleTable = cellsAndRuleTable[1]
        self.ruleTableWidth = len(self.ruleTable)
        self.kernelWidth = 3

    def getCells(self):
        return self.cells

    def step(self):
        newCells = [0 for i in range(self.width)]
        for cellIndex, currentValue in enumerate(self.cells):
            neighbors = utils.circularSlice(self.cells,
                        (cellIndex - self.kernelWidth/2),
                        (cellIndex + self.kernelWidth/2 + 1))
            newState = [0 for i in range(self.ruleTableWidth)]
            for subruleIndex, subrule in enumerate(self.ruleTable):
                neighborStateIndexes = [neighbor[subruleIndex] for neighbor in neighbors]
                nextSubstate = utils.indexByTuple(subrule, [self.cells[cellIndex][subruleIndex]] + neighborStateIndexes)
                newState[subruleIndex] = nextSubstate
            newCells[cellIndex] = newState
        self.cells = newCells