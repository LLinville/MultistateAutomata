import random
import utils
import math
from simplexnoise import scaled_octave_noise_3d
import colorsys

class Cartesian2DAutomata():
    def __init__(self, numCells):
        self.thetaSlots = 100
        self.rSlots = 100
        self.thetaSlotWidth = 1.0 / self.thetaSlots
        self.rSlotWidth = 1.0 / self.rSlots

        self.cells = [None for cell in range(numCells)]
        self.numCells = len(self.cells)
        self.transitionTable = []

    def indexedTransition(self, thetaIndex, rIndex):
        thetaIndex = int(thetaIndex % self.thetaSlots)
        rIndex = int(rIndex % self.rSlots)
        return self.transitionTable[thetaIndex][rIndex]

    def transition(self, (x, y)):
        theta = math.atan2(y, x) % (2 * math.pi)
        theta /= 2 * math.pi
        r = self.sigmoid(math.sqrt(x * x + y * y))

        thetaIndex = math.floor(theta / self.thetaSlotWidth)
        thetaInterpolateFraction = (theta % self.thetaSlotWidth) * self.thetaSlots
        rIndex = math.floor(r / self.rSlotWidth)
        rInterpolateFraction = (r % self.rSlotWidth) * self.rSlots

        lowerThetaInterpolated = self.interpolate(
            self.indexedTransition(thetaIndex, rIndex),
            self.indexedTransition(thetaIndex, rIndex + 1),
            rInterpolateFraction)

        upperThetaInterpolated = self.interpolate(
            self.indexedTransition(thetaIndex + 1, rIndex),
            self.indexedTransition(thetaIndex + 1, rIndex + 1),
            rInterpolateFraction)

    #    return self.interpolate(lowerThetaInterpolated, upperThetaInterpolated, thetaInterpolateFraction)
        return self.indexedTransition(thetaIndex, rIndex)


    def interpolate(self, bound1, bound2, location):

        return bound1[0] + location * (bound2[0] - bound1[0]), bound1[1] + location * (bound2[1] - bound1[1])


    def step(self):
        newCells = [None for cell in self.cells]
        for cellIndex, cell in enumerate(self.cells):
            newCells[cellIndex] = self.transition(cell)

        self.cells = newCells

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def randomizeRules(self, randomOffset=None):
        if randomOffset is None:
            randomOffset = random.randrange(0, 10000)

        thetaTable = [[scaled_octave_noise_3d(4, 0.5, 3.0,
                                              loBound=0.0,
                                              hiBound=1.0,
                                              x=(thetaIndex * self.thetaSlotWidth),
                                              y=(rIndex * self.rSlotWidth),
                                              z=randomOffset)
                       for rIndex in range(self.rSlots)] for thetaIndex in range(self.thetaSlots)]

        rTable = [[scaled_octave_noise_3d(4, 0.5, 3.0,
                                          loBound=0.0,
                                          hiBound=1.0,
                                          x=(thetaIndex * self.thetaSlotWidth),
                                          y=(rIndex * self.rSlotWidth),
                                          z=randomOffset)
                       for rIndex in range(self.rSlots)] for thetaIndex in range(self.thetaSlots)]

        self.transitionTable = [[None for rIndex in range(self.rSlots)] for thetaIndex in range(self.thetaSlots)]
        for thetaIndex in range(self.thetaSlots):
            for rIndex in range(self.rSlots):
                theta = thetaTable[thetaIndex][rIndex]
                radius = rTable[thetaIndex][rIndex]
                self.transitionTable[thetaIndex][rIndex] = self.toXY(theta, radius)

    def randomizeState(self):
        self.cells = [self.sampleUnitDisk() for i in range(self.numCells)]

    def sampleUnitDisk(self):
        theta = random.random() * 2 * math.pi
        radius = random.random()
        return (math.sqrt(radius) * math.cos(theta), math.sqrt(radius) * math.sin(theta))

    def toXY(self, theta, radius):
        return radius * math.cos(theta), radius * math.sin(theta)

    def toPolar(self, x, y):
        return math.atan2(y, x), math.sqrt(x * x + y * y)

    def getCellColors(self):
        polarStates = [self.toPolar(cell[0], cell[1]) for cell in self.cells]
        return [self.stateToColor(polarState) for polarState in polarStates]

    def stateToColor(self, state):
        state = self.toPolar(state[0], state[1])
        color = colorsys.hsv_to_rgb(state[0], 1, self.sigmoid(state[1]))
        return [int(component * 255) for component in color]

    def getTransitionTableImage(self):
        return [[self.stateToColor(self.transitionTable[thetaIndex][rIndex]) for thetaIndex in range(self.thetaSlots)] for rIndex in range(self.rSlots)]
