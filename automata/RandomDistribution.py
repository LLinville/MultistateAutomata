import random

def randomSlicedUnit(numGroups):
    return sorted([random.random() for i in range(numGroups - 1)] + [1.0])

def randomFromDistribution(distribution):
    selectedValue = random.random()
    return min([i for i in range(len(distribution)) if distribution[i] > selectedValue])

class RandomDistribution:
    def __init__(self, maxValue):
        self.distribution = randomSlicedUnit(maxValue + 1)

    def getValue(self):
        return randomFromDistribution(self.distribution)

