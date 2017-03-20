import pygame
from pygame.locals import *
from automata.simplexnoise import *
from automata.MultistateAutomata import MultistateAutomata
import random
from automata.utils import *
from automata.RandomDistribution import RandomDistribution
import time

class AutomataDisplay:
    def __init__(self, screenDimensions, initialCells, rule):
        self.screen = pygame.display.set_mode(screenDimensions)
        self.cells = initialCells
        self.rule = rule

    def resetToRandom(self):
        self.cells =




pygame.init()
screen = pygame.display.set_mode((1000, 1000))

running = 1

ca = rownum = None

cellsWidth = 500

doneDrawing = False

#how many values each state can take
stateDepths = [2, 2, 2]

randomDistribution = RandomDistribution(min(stateDepths) - 1)

def randomSubstateProvider():
    #return random.randint(0, min(stateDepths) - 1)
    return randomDistribution.getValue()

def reset():
    global ca
    global randomDistribution
    randomDistribution = RandomDistribution(min(stateDepths) - 1)
    ca = MultistateAutomata(
        [[random.randint(0,stateDepth-1) for stateDepth in stateDepths] for i in range(cellsWidth)],
        [indexedRandomMatrix(3, stateDepth, randomSubstateProvider) for stateDepth in stateDepths],
        stateDepths
    )
    global rownum
    rownum = 0
    screen.fill((0,0,0))
    print ca.crossStateRules
    print randomDistribution.distribution

    global doneDrawing
    doneDrawing = False

def resetState():
    global ca
    global randomDistribution
    randomDistribution = RandomDistribution(min(stateDepths) - 1)
    ca = MultistateAutomata(
        [[random.randint(0, stateDepth - 1) for stateDepth in stateDepths] for i in range(cellsWidth)],
        ca.ruleTable,
        stateDepths,
        ca.crossStateRules
    )
    global rownum
    rownum = 0
    screen.fill((0, 0, 0))

    global doneDrawing
    doneDrawing = False

reset()

while running:
    startTime = time.time()
    for event in pygame.event.get():
        print event.type
        if event.type == QUIT:
            running = 0

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                reset()
            if event.key == K_UP:
                resetState()
            if event.key == K_DOWN:
                rownum = 0
                doneDrawing = False

    if not doneDrawing:
        for cellIndex, cellValue in enumerate(ca.getCells()):
            screen.set_at((cellIndex, rownum), stateToColor(cellValue, max(stateDepths) - 1))

        pygame.draw.line(screen, (0, 0, 0), (500, rownum), (500 + len(ca.getCells()), rownum), 1)
        for mutatedIndex in ca.applyCrossStateRules():
            screen.set_at((mutatedIndex + 500, rownum), (255,255,255))

        lineDrawnTime = time.time()

        rownum += 1
        #rownum = rownum if rownum <=1000 else 0
        if rownum >= 1000:
            doneDrawing = True

        ca.step()

        stepTime = time.time()

        if rownum % 100 == 0:
            pygame.display.update(pygame.Rect(10, 10, 20, 20))

        flipTime = time.time()

    #print "\n\nline draw: " + str(lineDrawnTime - startTime) + "\nstep: " + str(stepTime - lineDrawnTime) + "\nflip: " + str(flipTime - stepTime)

pygame.quit()

