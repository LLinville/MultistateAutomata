import random

class RuleGenerator:
    def __init__(self):
        self.kernelWidth = 3

    def getRandomSingleStateRule(self, maxStateValue):
        ruleTable = [[[0 for z in range(maxStateValue)] for y in range(maxStateValue)] for x in
                          range(maxStateValue)]

        mutationsToRun = maxStateValue ** self.kernelWidth
        for mutateIteration in range(mutationsToRun):
            if random.random() < 0.2:
                self.mutateRulePlane(ruleTable, maxStateValue)
            else:
                self.mutateRuleLine(ruleTable, maxStateValue)

        return ruleTable

    def mutateRulePlane(self, ruleTable, maxStateValue):
        dimensionToMutate = random.randint(0, self.kernelWidth - 1)
        randomIndexToMutate = random.randint(0, maxStateValue - 1)
        randomStateValue = random.randint(0, maxStateValue - 1)

        for x in range(maxStateValue):
            for y in range(maxStateValue):
                if dimensionToMutate is 0:
                    ruleTable[randomIndexToMutate][x][y] = randomStateValue
                elif dimensionToMutate is 1:
                    ruleTable[x][randomIndexToMutate][y] = randomStateValue
                else:
                    ruleTable[x][y][randomIndexToMutate] = randomStateValue

    def mutateRuleLine(self, ruleTable, maxStateValue):
        dimensionToMutate = random.randint(0, self.kernelWidth - 1)
        randomIndexToMutate1 = random.randint(0, maxStateValue - 1)
        randomIndexToMutate2 = random.randint(0, maxStateValue - 1)
        randomStateValue = random.randint(0, maxStateValue - 1)

        for x in range(maxStateValue):
            if dimensionToMutate is 0:
                ruleTable[randomIndexToMutate1][randomIndexToMutate2][x] = randomStateValue
            elif dimensionToMutate is 1:
                ruleTable[x][randomIndexToMutate1][randomIndexToMutate2] = randomStateValue
            else:
                ruleTable[randomIndexToMutate2][x][randomIndexToMutate1] = randomStateValue