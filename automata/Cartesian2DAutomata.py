import random
import utils
import math
import noise
import colorsys
import numpy.matrixlib
from automata.simplexnoise import *

class Cartesian2DAutomata():
    def __init__(self, numCells):
        self.transitionSlots = 100
        self.transitionSlotSize = 1.0 / self.transitionSlots

        self.cells = [None for cell in range(numCells)]
        self.numCells = len(self.cells)
        self.transitionTable = []
        self.noiseGenerator = noise.SimplexNoise()
        self.tweakedTotal = random.random() * 10000

    def getTransitionTable(self):
        return self.transitionTable

    def setTransitionTable(self, transitionTable):
        self.transitionTable = transitionTable

    def tweakTransitionTable(self, randomSkewMultiplier):
        self.tweakedTotal += randomSkewMultiplier
        self.randomizeRules((self.tweakedTotal, self.tweakedTotal))

    def setState(self, cells):
        self.cells = cells

    def indexedTransition(self, xIndex, yIndex):
        xIndex = int(xIndex % self.transitionSlots)
        yIndex = int(yIndex % self.transitionSlots)
        return self.transitionTable[yIndex][xIndex]

    def transition(self, (x, y)):
        # x = x if x < 1.0 else x % 1.0
        # x = x if x > 0.0 else x % 0.0
        # y = y if y < 1.0 else 1.0
        # y = y if y > 0.0 else 0.0
        x, y = x % 1.0, y % 1.0
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


    def step(self, neighborKernel = None, normalize = False, gradientMultiplier = None, transformMatrix = None):
        newCells = [None for cell in self.cells]
        for cellIndex in range(self.numCells):
            newCell = self.cells[cellIndex]
            if neighborKernel:
                newCell = self.applyKernel(self.cells, cellIndex, neighborKernel, normalize)

            newCell = self.transition(newCell)

            if gradientMultiplier:
                newCell = self.addGradient(self.cells[cellIndex], newCell, gradientMultiplier)

            if transformMatrix:
                newCell = numpy.matmul(newCell, transformMatrix)
            newCells[cellIndex] = newCell
        self.cells = newCells

    def addGradient(self, cellValue, gradient, gradientMultiplier):
        return [cellComponent + gradientMultiplier * gradientComponent for cellComponent, gradientComponent in zip(cellValue, gradient)]

    def applyKernel(self, cells, cellIndex, neighborKernel, normalize):
        neighborCells = utils.circularSlice(cells, cellIndex - len(neighborKernel) / 2, len(neighborKernel))
        if not normalize:
            return (sum(cellValue[0] * kernelMultiplier for cellValue, kernelMultiplier in zip(neighborCells, neighborKernel)),
                sum(cellValue[1] * kernelMultiplier for cellValue, kernelMultiplier in zip(neighborCells, neighborKernel)))
        else:
            return (sum(cellValue[0] * kernelMultiplier for cellValue, kernelMultiplier in zip(neighborCells, neighborKernel)) / sum(neighborKernel),
                    sum(cellValue[1] * kernelMultiplier for cellValue, kernelMultiplier in zip(neighborCells, neighborKernel)) / sum(neighborKernel))

    def sigmoid(self, x, xCompression=0.5):
        return 1 / (1 + math.exp(-(x * xCompression)))

    def randomizeRules(self, randomOffset=None):
        simplexOctaves = 5
        simplexPersistance = 0.7
        simplexDetail = 1
        if randomOffset is None:
            randomOffset = (self.tweakedTotal, self.tweakedTotal)


        thetaTable = [[scaled_octave_noise_3d(simplexOctaves, simplexPersistance, simplexDetail,
                                              loBound=0.0,
                                              hiBound=math.pi,
                                              x=1.0 * xIndex / self.transitionSlots,
                                              y=1.0 * yIndex / self.transitionSlots,
                                              z=randomOffset[0])
                       for xIndex in range(self.transitionSlots)] for yIndex in range(self.transitionSlots)]

        rTable = [[scaled_octave_noise_3d(simplexOctaves, simplexPersistance, simplexDetail,
                                              loBound=0.0,
                                              hiBound=1.0,
                                              x=1.0 * xIndex / self.transitionSlots,
                                              y=1.0 * yIndex / self.transitionSlots,
                                              z=randomOffset[1]) * (1.1 - ((xIndex + yIndex) / (self.transitionSlots * 2.0)))
                       for xIndex in range(self.transitionSlots)] for yIndex in range(self.transitionSlots)]

        self.transitionTable = [[utils.toXY(thetaTable[yIndex][xIndex], rTable[yIndex][xIndex])
                for xIndex in range(self.transitionSlots)]
                for yIndex in range(self.transitionSlots)]

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
        # if state[1] < 0:
        #     state = (state[0], 0.0)
        # if state[1] > 1:
        #     state = (state[0], 1.0)
        state = (state[0] % 1.0, state[1] % 1.0)
        color = colorsys.hls_to_rgb(state[0] * math.pi, state[1], 1.0)
        return [int(component * 255) for component in color]

    def getTransitionTableImage(self):
        return [[self.stateToColor(self.transitionTable[yIndex][xIndex]) for xIndex in range(self.transitionSlots)] for yIndex in range(self.transitionSlots)]

