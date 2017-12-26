import pygame
from pygame.locals import *
from automata.Polar2DAutomata import Polar2DAutomata
from automata.Cartesian2DAutomata import Cartesian2DAutomata
from random import *
from automata.utils import *
from numpy import *
import time
import automata.utils as utils

class AutomataDisplay:
    def __init__(self, screenDimensions, automaton):
        pygame.init()
        self.screen = pygame.display.set_mode(screenDimensions)
        self.automaton = automaton
        self.screenDimensions = screenDimensions
        self.cellDrawScale = 3
        self.randomSkewMultiplier = 0.005
        self.resetState()
        self.resetDisplay(True)

    def run(self):
        running = True
        rownum = 0
        while running:
            if rownum == self.screenDimensions[1]:
                self.doneDrawing = True

            startTime = time.time()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = 0

                if event.type == KEYDOWN:
                    keysPressed = pygame.key.get_pressed()
                    modifiers = pygame.key.get_mods()
                    if modifiers & pygame.K_LSHIFT:
                        if keysPressed[pygame.K_LEFT]:
                            self.smallTweak(pygame.K_LEFT)
                        elif keysPressed[pygame.K_RIGHT]:
                            self.smallTweak(pygame.K_RIGHT)
                        elif keysPressed[pygame.K_UP]:
                            self.smallTweak(pygame.K_UP)
                        elif keysPressed[pygame.K_DOWN]:
                            self.smallTweak(pygame.K_DOWN)

                        self.drawTable(self.automaton.numCells * self.cellDrawScale + 100, 100)
                        pygame.display.flip()

                    elif event.key == K_RIGHT:
                        self.doneDrawing = False
                        automaton.tweakedTotal = random.random() * 10000
                        automaton.randomizeRules()
                        automaton.randomizeState()
                        self.resetDisplay()
                        rownum = 0
                    elif event.key == K_UP:
                        self.doneDrawing = False
                        self.automaton.randomizeState()
                        self.resetDisplay(True)
                        rownum = 0
                    elif event.key == K_DOWN:
                        rownum = 0
                        self.doneDrawing = False
                    elif event.key == K_LEFT:
                        rownum = 0
                        self.doneDrawing = False
                        automaton.tweakedTotal += self.randomSkewMultiplier
                        automaton.randomizeRules()
                        automaton.randomizeState()
                        self.drawTable(self.automaton.numCells * self.cellDrawScale + 100, 100)
                        pygame.display.flip()

            if not self.doneDrawing:
                if self.cellDrawScale == 1:
                    for cellIndex, cellColor in enumerate(self.automaton.getCellColors()):
                        self.screen.set_at((cellIndex, rownum), cellColor)
                else:
                    for cellIndex, cellColor in enumerate(self.automaton.getCellColors()):
                        pygame.draw.rect(self.screen, cellColor, (cellIndex * self.cellDrawScale, rownum * self.cellDrawScale, self.cellDrawScale, self.cellDrawScale))

                lineDrawnTime = time.time()

                rownum += 1
                # rownum = rownum if rownum <=1000 else 0
                if rownum >= self.screenDimensions[1] / self.cellDrawScale:
                    self.doneDrawing = True
                    rownum = 0
                # if rownum % 10 == 0:
                #     self.automaton.tweakTransitionTable(self.randomSkewMultiplier)
                #     self.drawTable(self.automaton.numCells * self.cellDrawScale + 100, 100)
                #     pygame.display.flip()

                t = 0.01
                transform = [[cos(t), -sin(t)], [sin(t), cos(t)]]
                self.automaton.step(neighborKernel=utils.normalKernel(5), normalize=True, gradientMultiplier=None, transformMatrix=transform)

                stepTime = time.time()

                if rownum % 100 == 0:
                    pygame.display.flip()

                rownum %= self.screenDimensions[1]

                flipTime = time.time()

                #print "\n\nline draw: " + str(lineDrawnTime - startTime) + "\nstep: " + str(stepTime - lineDrawnTime) + "\nflip: " + str(flipTime - stepTime)

        pygame.quit()

    def smallTweak(self, directionKey):
        keySkewMultipliers = {pygame.K_LEFT: -0.01,
                               pygame.K_RIGHT: 0.01,
                               pygame.K_UP: 0.1,
                               pygame.K_DOWN:-0.1}
        if directionKey in keySkewMultipliers:
            automaton.tweakedTotal += keySkewMultipliers[directionKey] * self.randomSkewMultiplier

    def drawTable(self, x, y):
        transitionTable = array(self.automaton.getTransitionTableImage())
        for rowIndex, row in enumerate(transitionTable):
            for valueIndex, value in enumerate(row):
                if self.cellDrawScale == 1:
                    self.screen.set_at((x + valueIndex, y + rowIndex), (transitionTable[rowIndex][valueIndex]))
                else:
                    pygame.draw.rect(self.screen, transitionTable[rowIndex][valueIndex], (x + valueIndex * self.cellDrawScale, y + rowIndex * self.cellDrawScale, self.cellDrawScale, self.cellDrawScale))
        pygame.display.flip()

    def resetState(self):
        state = [utils.toXY(angle, cos(angle)) for angle in
                 [thetaValue * math.pi / 2 / automaton.numCells for thetaValue in range(automaton.numCells)]]
        automaton.setState(state)

    def resetDisplay(self, randomizeState=False):
        self.screen.fill((0, 0, 0))
        self.drawTable(self.automaton.numCells * self.cellDrawScale + 100, 100)
        self.doneDrawing = False
        if randomizeState:
            self.automaton.randomizeState()
        pygame.display.flip()


automaton = Cartesian2DAutomata(300)
# transitionTable = [[(1.0 * x / automaton.transitionSlots, 1.0 * y / automaton.transitionSlots)
#                     for x in range(automaton.transitionSlots)]
#                     for y in range(automaton.transitionSlots)]
#transitionTable = [[utils.rotateXY(1.0 * cell[0], 1.0 * cell[1], 0) for cell in row] for row in transitionTable]
#transitionTable = [[(value[0] + (random.random() - 0.5) / 1000.0, value[1] + (random.random() - 0.5) / 1000.0) for value in row] for row in transitionTable]
#transitionTable = [[(sin(x / 50.0) - 0.7, sin(y / 50.0) - 0.7) for x in range(automaton.transitionSlots)] for y in range(automaton.transitionSlots)]
#automaton.setTransitionTable(transitionTable)

#automaton.setState([utils.toXY(1.0 * cellIndex / automaton.numCells, 1.0 * cellIndex / automaton.numCells) for cellIndex in range(automaton.numCells)])
#automaton.randomizeState()
automaton.randomizeRules((automaton.tweakedTotal, automaton.tweakedTotal))
display = AutomataDisplay((1500,900), automaton)
display.run()
