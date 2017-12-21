import random
import utils
import math
import noise
import colorsys

class Cartesian2DAutomata():
    def __init__(self, numCells):
        self.transitionSlots = 300
        self.transitionSlotSize = 1.0 / self.transitionSlots

        self.cells = [None for cell in range(numCells)]
        self.numCells = len(self.cells)
        self.transitionTable = []
        self.noiseGenerator = noise.SimplexNoise()

    def getTransitionTable(self):
        return self.transitionTable

    def setTransitionTable(self, transitionTable):
        self.transitionTable = transitionTable

    def indexedTransition(self, xIndex, yIndex):
        xIndex = int(xIndex % self.transitionSlots)
        yIndex = int(yIndex % self.transitionSlots)
        return self.transitionTable[yIndex][xIndex]

    def transition(self, (x, y)):
        x = x if x > 1.0 else 1.0
        x = x if x < 0.0 else 0.0
        y = y if y > 1.0 else 1.0
        y = y if y < 0.0 else 0.0
        #xIndex = math.floor(self.sigmoid(x) * self.transitionSlots)
        #yIndex = math.floor(self.sigmoid(y) * self.transitionSlots)
        xIndex = math.floor(x * self.transitionSlots)
        yIndex = math.floor(y * self.transitionSlots)
        xInterpolateFraction = (x % self.transitionSlotSize) * self.transitionSlots
        yInterpolateFraction = (y % self.transitionSlotSize) * self.transitionSlots

        lowerXInterpolated = self.interpolate(
            self.indexedTransition(xIndex, yIndex),
            self.indexedTransition(xIndex, yIndex + 1),
            yInterpolateFraction)

        upperXInterpolated = self.interpolate(
            self.indexedTransition(xIndex + 1, yIndex),
            self.indexedTransition(xIndex + 1, yIndex + 1),
            yInterpolateFraction)

        return self.interpolate(lowerXInterpolated, upperXInterpolated, xInterpolateFraction)


    def interpolate(self, bound1, bound2, location):
        return bound1[0] + location * (bound2[0] - bound1[0]), bound1[1] + location * (bound2[1] - bound1[1])


    def step(self):
        newCells = [None for cell in self.cells]
        for cellIndex, cell in enumerate(self.cells):
            newCells[cellIndex] = self.transition(cell)

        self.cells = newCells

    def sigmoid(self, x, xCompression=0.5):
        return 1 / (1 + math.exp(-(x * xCompression)))

    def randomizeRules(self, randomOffset=None):
        simplexOctaves = 1
        simplexPersistance = 0.5
        simplexDetail = 0.005
        if randomOffset is None:
            randomOffset = (random.randrange(0, 10000), random.randrange(0, 10000))

        # xTable = [[scaled_octave_noise_4d(simplexOctaves, simplexPersistance, simplexDetail,
        #                                       loBound=0.0,
        #                                       hiBound=1.0,
        #                                       x=xIndex / self.transitionSlots,
        #                                       y=yIndex / self.transitionSlots,
        #                                       z=randomOffset[0],
        #                                       w=10)
        #                for xIndex in range(self.transitionSlots)] for yIndex in range(self.transitionSlots)]
        #
        # yTable = [[scaled_octave_noise_4d(simplexOctaves, simplexPersistance, simplexDetail,
        #                                       loBound=0.0,
        #                                       hiBound=1.0,
        #                                       x=xIndex,
        #                                       y=yIndex,
        #                                       z=randomOffset[1],
        #                                       w=0)
        #                for xIndex in range(self.transitionSlots)] for yIndex in range(self.transitionSlots)]
        #
        # self.transitionTable = [[ (xTable[yIndex][xIndex], yTable[yIndex][xIndex])
        #         for xIndex in range(self.transitionSlots)]
        #         for yIndex in range(self.transitionSlots)]

    def randomizeState(self):
        # self.cells = [self.sampleUnitDisk() for i in range(self.numCells)]
        self.cells = [(random.random(), random.random()) for i in range(self.numCells)]

    # (x,y) within 1 of origin
    def sampleUnitDisk(self):
        theta = random.random() * 2 * math.pi
        radius = random.random()
        return (math.sqrt(radius) * math.cos(theta), math.sqrt(radius) * math.sin(theta))

    def getCellColors(self):
        #polarStates = [utils.toPolar(cell[0], cell[1]) for cell in self.cells]
        return [self.stateToColor(state) for state in self.cells]

    def stateToColor(self, state):
        state = utils.toPolar(state[0], state[1])
        if state[1] < 0:
            state = (state[0], 0.0)
        if state[1] > 1:
            state = (state[0], 1.0)
        color = colorsys.hls_to_rgb(state[0], state[1], 1)
        return [int(component * 255) for component in color]

    def getTransitionTableImage(self):
        return [[self.stateToColor(self.transitionTable[yIndex][xIndex]) for xIndex in range(self.transitionSlots)] for yIndex in range(self.transitionSlots)]

