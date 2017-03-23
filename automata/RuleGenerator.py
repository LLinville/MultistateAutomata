import random

class RuleGenerator:
    def __init__(self):
        self.kernelWidth = 3

    def getRandomSingleStateRuleAlmostIdentity(self, maxStateValue, symmetric = False):
        ruleTable = [[[y for z in range(maxStateValue)] for y in range(maxStateValue)] for x in
                          range(maxStateValue)]

        mutationsToRun = 10000
        for mutateIteration in range(mutationsToRun):
            self.mutateRulePoint(ruleTable, maxStateValue, symmetric)
        return ruleTable

    def getRandomSingleStateRule(self, maxStateValue, symmetric = False):
        ruleTable = [[[0 for z in range(maxStateValue)] for y in range(maxStateValue)] for x in
                          range(maxStateValue)]

        mutationsToRun = maxStateValue ** self.kernelWidth
        for mutateIteration in range(mutationsToRun):
            if mutateIteration % 1000 is 0:
                print "Mutate " + str(mutateIteration/1000) + "k / " + str(mutationsToRun/1000) + "k"
            randomMutationType = random.random()
            if randomMutationType < 0.2:
                self.mutateRulePlane(ruleTable, maxStateValue, symmetric)
            elif randomMutationType < 0.8:
                self.mutateRuleLine(ruleTable, maxStateValue, symmetric)
            else:
                self.mutateRulePoint(ruleTable, maxStateValue, symmetric)

        return ruleTable

    def mutateRulePlane(self, ruleTable, maxStateValue, symmetric = False):
        dimensionToMutate = random.randint(0, self.kernelWidth - 1)
        randomIndexToMutate = random.randint(0, maxStateValue - 1)
        randomStateValue = random.randint(0, maxStateValue - 1)

        for x in range(maxStateValue):
            for y in range(maxStateValue):
                if dimensionToMutate is 0:
                    ruleTable[randomIndexToMutate][x][y] = randomStateValue
                    if symmetric:
                        ruleTable[y][x][randomIndexToMutate] = randomStateValue
                elif dimensionToMutate is 1:
                    ruleTable[x][randomIndexToMutate][y] = randomStateValue
                    if symmetric:
                        ruleTable[y][randomIndexToMutate][x] = randomStateValue
                else:
                    ruleTable[x][y][randomIndexToMutate] = randomStateValue
                    if symmetric:
                        ruleTable[randomIndexToMutate][y][x] = randomStateValue

    def mutateRuleLine(self, ruleTable, maxStateValue, symmetric = False):
        dimensionToMutate = random.randint(0, self.kernelWidth - 1)
        randomIndexToMutate1 = random.randint(0, maxStateValue - 1)
        randomIndexToMutate2 = random.randint(0, maxStateValue - 1)
        randomStateValue = random.randint(0, maxStateValue - 1)

        for x in range(maxStateValue):
            if dimensionToMutate is 0:
                ruleTable[randomIndexToMutate1][randomIndexToMutate2][x] = randomStateValue
                if symmetric:
                    ruleTable[x][randomIndexToMutate2][randomIndexToMutate1] = randomStateValue
            elif dimensionToMutate is 1:
                ruleTable[x][randomIndexToMutate1][randomIndexToMutate2] = randomStateValue
                if symmetric:
                    ruleTable[randomIndexToMutate2][randomIndexToMutate1][x] = randomStateValue
            else:
                ruleTable[randomIndexToMutate2][x][randomIndexToMutate1] = randomStateValue
                if symmetric:
                    ruleTable[randomIndexToMutate1][x][randomIndexToMutate2] = randomStateValue

    def mutateRulePoint(self, ruleTable, maxStateValue, symmetric = False):
        randx = random.randint(0, maxStateValue - 1)
        randy = random.randint(0, maxStateValue - 1)
        randz = random.randint(0, maxStateValue - 1)
        randstate = random.randint(0, maxStateValue - 1)
        ruleTable[randx][randy][randz] = randstate
        if symmetric:
            ruleTable[randz][randy][randx] = randstate